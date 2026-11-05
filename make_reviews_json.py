import json
import re
import sys
from pathlib import Path

import pandas as pd

HERE = Path(__file__).resolve().parent
file = Path(sys.argv[1]) if len(sys.argv) > 1 else HERE / "imdb_study_dataset_Julia_Geller.csv"
out = HERE / "reviews.json"
df = pd.read_csv(file)

missing = [c for c in ["text", "label", "classification", "explanation"] if c not in df.columns]
if missing:
    sys.exit(f"{file} is missing column(s) {missing}. Its columns are: {list(df.columns)}")


def clean(text: str) -> str:
    """Clean IMDB reviews by turning <br /> tags into line breaks"""
    text = re.sub(r"<br\s*/?>", "\n", str(text), flags=re.IGNORECASE)
    # make excessive line break gaps smaller
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


reviews = []
for i, row in df.iterrows():
    reviews.append({
        "id": int(i),
        "text": clean(row["text"]),
        "label": int(row["label"]),
        "ai_label": int(row["classification"]),
        "ai_explanation": "" if pd.isna(row["explanation"]) else clean(row["explanation"]),
    })

with open(out, "w", encoding="utf-8") as f:
    json.dump(reviews, f, ensure_ascii=False, indent=2)

n_expl = sum(1 for r in reviews if r["ai_explanation"])
print(f"Read {file}")
print(f"Wrote {len(reviews)} reviews ({n_expl} with an explanation) to {out}")