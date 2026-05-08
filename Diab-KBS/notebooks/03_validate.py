"""
KBS Validation (Lecture 4: Evaluation, Validation, Verification)
================================================================
Runs the rule-based inference engine on every patient in the cleaned
dataset and compares its T2DM diagnosis against the gold-standard label.
"""
from __future__ import annotations
import sys, os, json, pandas as pd, numpy as np
sys.path.insert(0, "/home/user/workspace/Diab-KBS")

from kbs.inference import InferenceEngine

DATA = "/home/user/workspace/Diab-KBS/data/patients_clean.csv"
RULES = "/home/user/workspace/Diab-KBS/knowledge_base/rules.json"

df = pd.read_csv(DATA)
eng = InferenceEngine(RULES)

# Patients with at least one diagnostic lab present
mask = (df['HbA1c'].notna() | df['FPG'].notna() | df['PP2H'].notna() | df['RBS'].notna())
sub = df[mask].copy()
print(f"Validating against {len(sub):,} patients with diagnostic labs ...")

predicted = []
for _, row in sub.iterrows():
    eng.load_patient({k: (None if pd.isna(v) else v) for k, v in row.to_dict().items()})
    eng.forward_chain()
    diags = [fr.derived.value for fr in eng.diagnoses()]
    predicted.append(1 if any("Type 2 Diabetes" in d for d in diags) else 0)

sub = sub.assign(pred_T2DM=predicted)
y_true = sub['T2DM'].fillna(0).astype(int).values
y_pred = np.array(predicted)

tp = int(((y_pred == 1) & (y_true == 1)).sum())
tn = int(((y_pred == 0) & (y_true == 0)).sum())
fp = int(((y_pred == 1) & (y_true == 0)).sum())
fn = int(((y_pred == 0) & (y_true == 1)).sum())

acc  = (tp + tn) / max(1, len(y_pred))
sens = tp / max(1, tp + fn)
spec = tn / max(1, tn + fp)
prec = tp / max(1, tp + fp)
f1   = 2 * prec * sens / max(1e-9, prec + sens)

result = {
    "n_patients_validated": int(len(y_pred)),
    "confusion_matrix": {"TP": tp, "TN": tn, "FP": fp, "FN": fn},
    "accuracy":    round(acc,  4),
    "sensitivity": round(sens, 4),
    "specificity": round(spec, 4),
    "precision":   round(prec, 4),
    "f1_score":    round(f1,   4),
}
print(json.dumps(result, indent=2))

with open("/home/user/workspace/Diab-KBS/data/validation_results.json", "w") as f:
    json.dump(result, f, indent=2)
print("\nSaved -> data/validation_results.json")
