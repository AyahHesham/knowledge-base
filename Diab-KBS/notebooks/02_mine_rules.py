"""
Semi-Automatic Knowledge Acquisition (Lecture 6)
================================================
Uses a Decision Tree induced from the cleaned dataset to discover
empirical IF-THEN rules that complement the manually-encoded clinical
rules in rules.json. Demonstrates the L6 'semi-automatic' KA path.
"""
from __future__ import annotations
import pandas as pd, numpy as np, json, os
from sklearn.tree import DecisionTreeClassifier, export_text
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix

DATA = "/home/user/workspace/Diab-KBS/data/patients_clean.csv"
OUT  = "/home/user/workspace/Diab-KBS/knowledge_base/mined_rules.json"

print("Loading patients ...")
df = pd.read_csv(DATA)
features = ['Age', 'BMI', 'HbA1c', 'FPG', 'PP2H', 'RBS',
            'HTN', 'Obesity', 'PolyuriaPolydipsia',
            'WeightLoss', 'Fatigue', 'Paresthesia']
features = [f for f in features if f in df.columns]
X = df[features].apply(pd.to_numeric, errors='coerce').fillna(df[features].median(numeric_only=True))
y = df['T2DM'].fillna(0).astype(int)
mask = ~y.isna()
X, y = X[mask], y[mask]

X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=0.25,
                                          random_state=42, stratify=y)

clf = DecisionTreeClassifier(max_depth=4, min_samples_leaf=80, random_state=42)
clf.fit(X_tr, y_tr)
print(f"Train acc = {clf.score(X_tr, y_tr):.3f}")
print(f"Test  acc = {clf.score(X_te, y_te):.3f}")

print("\n--- Classification report (test) ---")
print(classification_report(y_te, clf.predict(X_te), digits=3))

print("\n--- Confusion matrix ---")
print(confusion_matrix(y_te, clf.predict(X_te)))

print("\n--- Induced decision tree (textual rules) ---")
tree_txt = export_text(clf, feature_names=features, max_depth=5)
print(tree_txt)

# Save mined rules + metrics for the dashboard / paper
out = {
    "metadata": {
        "method": "Decision Tree induction (CART, depth=4, min_leaf=80)",
        "target": "T2DM (1=diabetic, 0=non-diabetic)",
        "features_used": features,
        "n_train": int(len(X_tr)),
        "n_test":  int(len(X_te)),
        "train_accuracy": float(clf.score(X_tr, y_tr)),
        "test_accuracy":  float(clf.score(X_te, y_te)),
    },
    "tree_text": tree_txt,
    "feature_importances": dict(zip(features,
                                    [float(v) for v in clf.feature_importances_]))
}
os.makedirs(os.path.dirname(OUT), exist_ok=True)
with open(OUT, "w") as f:
    json.dump(out, f, indent=2)
print(f"\nSaved -> {OUT}")
