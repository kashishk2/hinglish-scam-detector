"""
Cleans data/raw_messages.csv -> data/clean_messages.csv
Run from project root:  python src/preprocess.py
"""
import re
import pandas as pd

URL_RE = re.compile(r"(https?://\S+|www\.\S+|\b\S+\.(?:in|com|xyz|top|click|info|ly|net)\S*)", re.I)
PHONE_RE = re.compile(r"\b[6-9]\d{9}\b")
NUM_RE = re.compile(r"\b\d[\d,\.]*\b")

# Common Hinglish spelling variants -> one standard form
NORMALIZE = {
    "apka": "aapka", "karen": "karein", "kare": "karein",
    "abi": "abhi", "varna": "warna", "turat": "turant", "ghnte": "ghante",
    "acc": "account", "rs.": "rs", "rupaye": "rs", "rupay": "rs",
    "h": "hai",
}

def clean_text(text: str) -> str:
    t = str(text).lower().strip()
    t = t.replace("a/c", "account").replace("aap ka", "aapka")
    t = URL_RE.sub(" <url> ", t)
    t = PHONE_RE.sub(" <phone> ", t)
    t = NUM_RE.sub(" <num> ", t)
    t = re.sub(r"[^a-z<>\s]", " ", t)        # keep letters and our tokens
    words = [NORMALIZE.get(w, w) for w in t.split()]
    return re.sub(r"\s+", " ", " ".join(words)).strip()

if __name__ == "__main__":
    df = pd.read_csv("data/raw_messages.csv")
    before = len(df)
    df["clean_text"] = df["text"].apply(clean_text)
    df = df[df["clean_text"].str.len() > 0].drop_duplicates(subset="clean_text")
    df.to_csv("data/clean_messages.csv", index=False, encoding="utf-8")
    print(f"{before} -> {len(df)} rows after cleaning")
    print(df[["text", "clean_text", "label"]].head(6).to_string())