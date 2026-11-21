"""
Day 2: baseline models (TF-IDF + classic ML).
Run from project root:  python src/train_baseline.py
Outputs: models/baseline.joblib, models/baseline_results.csv, models/confusion_matrix.png
"""
import os
import sys
import joblib
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split, StratifiedKFold, cross_val_score
from sklearn.pipeline import Pipeline, FeatureUnion
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import MultinomialNB
from sklearn.svm import LinearSVC
from sklearn.metrics import (precision_score, recall_score, f1_score, accuracy_score,
                             classification_report, ConfusionMatrixDisplay)

sys.path.insert(0, "src")
from preprocess import clean_text

SEED = 42

def features():
    # word n-grams catch phrases ("account block"), char n-grams survive spelling variants ("apka"/"aapka")
    return FeatureUnion([
        ("word", TfidfVectorizer(ngram_range=(1, 2), min_df=1, sublinear_tf=True)),
        ("char", TfidfVectorizer(analyzer="char_wb", ngram_range=(3, 5), min_df=2, sublinear_tf=True)),
    ])

MODELS = {
    "Logistic Regression": LogisticRegression(max_iter=1000, class_weight="balanced"),
    "Naive Bayes": MultinomialNB(alpha=0.1),
    "Linear SVM": LinearSVC(class_weight="balanced"),
}

def main():
    df = pd.read_csv("data/clean_messages.csv")
    X, y = df["clean_text"], df["label"]
    X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=0.2, stratify=y, random_state=SEED)
    print(f"Train: {len(X_tr)}  Test: {len(X_te)}\n")

    results, fitted = [], {}
    cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=SEED)
    for name, clf in MODELS.items():
        pipe = Pipeline([("features", features()), ("clf", clf)])
        cv_f1 = cross_val_score(pipe, X_tr, y_tr, cv=cv, scoring="f1").mean()
        pipe.fit(X_tr, y_tr)
        pred = pipe.predict(X_te)
        results.append({
            "model": name,
            "accuracy": accuracy_score(y_te, pred),
            "scam_precision": precision_score(y_te, pred),
            "scam_recall": recall_score(y_te, pred),
            "scam_f1": f1_score(y_te, pred),
            "cv_f1_(train)": cv_f1,
        })
        fitted[name] = (pipe, pred)

    res = pd.DataFrame(results).round(3).sort_values("scam_f1", ascending=False)
    print(res.to_string(index=False))
    res.to_csv("models/baseline_results.csv", index=False)

    best_name = res.iloc[0]["model"]
    best_pipe, best_pred = fitted[best_name]
    print(f"\nBest model: {best_name}\n")
    print(classification_report(y_te, best_pred, target_names=["safe", "scam"]))

    ConfusionMatrixDisplay.from_predictions(y_te, best_pred, display_labels=["safe", "scam"], cmap="Blues")
    plt.title(f"Confusion matrix - {best_name}")
    plt.savefig("models/confusion_matrix.png", dpi=150, bbox_inches="tight")

    # Show mistakes: very useful for understanding the model
    errs = pd.DataFrame({"text": X_te, "true": y_te, "pred": best_pred})
    errs = errs[errs["true"] != errs["pred"]]
    print(f"Misclassified: {len(errs)}")
    if len(errs):
        print(errs.head(10).to_string())

    joblib.dump(best_pipe, "models/baseline.joblib")
    print("\nSaved models/baseline.joblib")

    # Honest test on your own messages, if you made data/my_test.csv (text,label)
    if os.path.exists("data/my_test.csv"):
        t = pd.read_csv("data/my_test.csv")
        t["clean_text"] = t["text"].apply(clean_text)
        p = best_pipe.predict(t["clean_text"])
        print("\n=== Your own test set (my_test.csv) ===")
        print(classification_report(t["label"], p, target_names=["safe", "scam"]))

if __name__ == "__main__":
    main()