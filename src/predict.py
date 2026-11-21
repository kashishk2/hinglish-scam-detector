"""Prediction + word-level explanation, used by app.py."""
import os
import sys
import html
import joblib
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from preprocess import clean_text

MODEL_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "models", "baseline.joblib")


def load_model(path=MODEL_PATH):
    return joblib.load(path)


def raw_score(model, text):
    """Higher = more scam-like. Works for LR / SVM pipelines."""
    c = clean_text(text)
    if not c:
        return -5.0
    if hasattr(model, "decision_function"):
        return float(model.decision_function([c])[0])
    p = float(np.clip(model.predict_proba([c])[0][1], 1e-6, 1 - 1e-6))
    return float(np.log(p / (1 - p)))


def scam_probability(model, text):
    c = clean_text(text)
    if not c:
        return 0.0
    if hasattr(model, "predict_proba"):
        return float(model.predict_proba([c])[0][1])
    return float(1 / (1 + np.exp(-2 * raw_score(model, text))))  # approximate, not calibrated


def analyze(model, text, top_k=6, min_drop=0.05):
    """Predict, and find the words that push the score towards 'scam'.
    Method: remove each word in turn; the bigger the score drop, the more suspicious the word."""
    base = raw_score(model, text)
    tokens = text.split()
    drops = []
    for i in range(len(tokens)):
        reduced = " ".join(tokens[:i] + tokens[i + 1:])
        drops.append(base - raw_score(model, reduced))
    flagged = set()
    if base > 0:
        for i in np.argsort(drops)[::-1][:top_k]:
            if drops[i] >= min_drop:
                flagged.add(int(i))
    return {
        "label": "scam" if base > 0 else "safe",
        "probability": scam_probability(model, text),
        "tokens": tokens,
        "flagged": flagged,
    }


def highlight_html(tokens, flagged):
    parts = []
    for i, t in enumerate(tokens):
        t = html.escape(t)
        if i in flagged:
            parts.append(f"<mark style='background:#ffb3b3;color:#000;padding:1px 3px;border-radius:3px'>{t}</mark>")
        else:
            parts.append(t)
    return " ".join(parts)