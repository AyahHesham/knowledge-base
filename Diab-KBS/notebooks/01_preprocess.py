"""
Diab-KBS — Data Preprocessing
=============================
Lecture mapping: L2 (Big Data Analytics Workflow: Extract → Integrate → Compute → Mine → Visualize)

Cleans Dr. Hossam's 12,204-patient diabetes dataset:
  - Fix lab/anthropometric outliers (decimal/unit errors)
  - Normalize Yes/No flags
  - Compute derived clinical features (Age, BMI category, HbA1c category, FPG category)
  - Save clean CSV for downstream KBS inference and dashboard analytics
"""
from __future__ import annotations
import pandas as pd, numpy as np, json, os, datetime as dt

SRC = "/home/user/workspace/drhossamdiabetes.xlsx"
OUT_DIR = "/home/user/workspace/Diab-KBS/data"
os.makedirs(OUT_DIR, exist_ok=True)

print("[1/6] Loading raw dataset ...")
df = pd.read_excel(SRC)
print(f"     raw shape = {df.shape}")

# ---------------------------------------------------------------- Yes/No flags
yn_cols = [c for c in df.columns if df[c].dropna().astype(str).str.lower().isin(['yes', 'no']).mean() > 0.9]
for c in yn_cols:
    df[c] = df[c].astype(str).str.strip().str.lower().map({'yes': 1, 'no': 0}).astype('Int64')
print(f"[2/6] Normalised {len(yn_cols)} yes/no columns -> 0/1")

# -------------------------------------------------------------- Numeric labs
def clip_outliers(s, lo, hi):
    s = pd.to_numeric(s, errors='coerce')
    s = s.where((s >= lo) & (s <= hi), np.nan)
    return s

clip_specs = {
    'Weight':                 (25, 250),    # kg
    'Height':                 (1.20, 2.20), # m  (most rows are in m, some are mm)
    'BMI':                    (12, 70),
    'Pulse':                  (35, 180),
    'RGB':                    (40, 700),
    'Random blood sugar':     (40, 700),
    'Fasting Plasma glucose': (40, 600),
    '2hPP Plasma glucose':    (40, 700),
    'Glycated Hemoglobin - HbA1c': (3, 18),
    'Serum creatinine':       (0.2, 15),
    'Serum uric acid':        (1, 15),
    'TSH':                    (0.05, 50),
    'Fasting blood sugar':    (40, 600),
    '2hPP blood sugar':       (40, 700),
}
for col, (lo, hi) in clip_specs.items():
    if col in df.columns:
        # Try fixing common unit issues for Height (cm -> m)
        if col == 'Height':
            h = pd.to_numeric(df[col], errors='coerce')
            h = h.where(h <= 3, h / 100.0)         # cm -> m
            h = h.where(h >= 0.5, h * 100.0)       # mm-like -> still rough
            df[col] = h
        df[col] = clip_outliers(df[col], lo, hi)

# Recompute BMI when missing but weight & height present
mask = df['BMI'].isna() & df['Weight'].notna() & df['Height'].notna() & (df['Height'] > 0)
df.loc[mask, 'BMI'] = (df.loc[mask, 'Weight'] / (df.loc[mask, 'Height'] ** 2)).round(1)
print("[3/6] Clipped lab/anthro outliers and recomputed BMI where missing")

# ---------------------------------------------------------------------- Age
def to_year(x):
    try:
        return pd.to_datetime(x, errors='coerce').year
    except Exception:
        return np.nan

df['BirthYear'] = df['Date of Birth'].map(to_year)
TODAY_YEAR = 2026
df['Age'] = (TODAY_YEAR - df['BirthYear']).where(df['BirthYear'].between(1920, 2020))

# Categories used by the rule engine ----------------------------------------
def bmi_cat(b):
    if pd.isna(b): return None
    if b < 18.5: return 'underweight'
    if b < 25:   return 'normal'
    if b < 30:   return 'overweight'
    if b < 35:   return 'obese_I'
    if b < 40:   return 'obese_II'
    return 'obese_III'

def hba1c_cat(h):
    if pd.isna(h): return None
    if h < 5.7: return 'normal'
    if h < 6.5: return 'prediabetes'
    return 'diabetes_range'

def fpg_cat(f):
    if pd.isna(f): return None
    if f < 100: return 'normal'
    if f < 126: return 'impaired_fasting'
    return 'diabetes_range'

def pp_cat(p):
    if pd.isna(p): return None
    if p < 140: return 'normal'
    if p < 200: return 'impaired_glucose_tolerance'
    return 'diabetes_range'

def tsh_cat(t):
    if pd.isna(t): return None
    if t < 0.4: return 'low'
    if t > 4.0: return 'high'
    return 'normal'

df['BMI_cat']   = df['BMI'].map(bmi_cat)
df['HbA1c_cat'] = df['Glycated Hemoglobin - HbA1c'].map(hba1c_cat)
df['FPG_cat']   = df['Fasting Plasma glucose'].map(fpg_cat)
df['PP_cat']    = df['2hPP Plasma glucose'].map(pp_cat)
df['TSH_cat']   = df['TSH'].map(tsh_cat)
print("[4/6] Computed derived clinical categories")

# ----------------------------------------------------- Friendly column names
rename_map = {
    'Glycated Hemoglobin - HbA1c': 'HbA1c',
    'Fasting Plasma glucose':      'FPG',
    '2hPP Plasma glucose':         'PP2H',
    'Random blood sugar':          'RBS',
    'Serum creatinine':            'Creatinine',
    'Serum uric acid':             'UricAcid',
    'Primary Hypothyroidism':      'Hypothyroidism',
    'Primary Hyperthyroidism':     'Hyperthyroidism',
    'D.Neuropathy':                'Neuropathy',
    'Polyuria and Polydipsia':     'PolyuriaPolydipsia',
    'Loss of weight':               'WeightLoss',
    'Blurring of Vision':          'BlurredVision',
    'Delayed Wound Healing':       'DelayedHealing',
    'Muscle Cramps':               'MuscleCramps',
    'Muscle Weakness':             'MuscleWeakness',
}
df = df.rename(columns=rename_map)

keep_cols = [
    'ID', 'Age', 'Gender', 'Address',
    'T2DM', 'Type1 Diabetes', 'T2D vs LADA',
    'HTN', 'Obesity', 'Hypothyroidism', 'Hyperthyroidism', 'Neuropathy',
    'PolyuriaPolydipsia', 'WeightLoss', 'Polyphagia', 'BlurredVision',
    'DelayedHealing', 'Paresthesia', 'MuscleCramps', 'MuscleWeakness', 'Fatigue',
    'Weight', 'Height', 'BMI', 'BMI_cat',
    'RBS', 'FPG', 'PP2H', 'HbA1c', 'HbA1c_cat', 'FPG_cat', 'PP_cat',
    'Creatinine', 'UricAcid', 'TSH', 'TSH_cat', 'Pulse'
]
keep_cols = [c for c in keep_cols if c in df.columns]
clean = df[keep_cols].copy()
out_csv = os.path.join(OUT_DIR, 'patients_clean.csv')
clean.to_csv(out_csv, index=False)
print(f"[5/6] Wrote clean dataset -> {out_csv}  ({clean.shape})")

# ------------------------------------------------------------- Quick KPIs
kpis = {
    'n_patients':            int(len(clean)),
    'n_t2dm':                int((clean['T2DM'] == 1).sum()) if 'T2DM' in clean else 0,
    'n_t1dm':                int((clean['Type1 Diabetes'] == 1).sum()) if 'Type1 Diabetes' in clean else 0,
    'n_htn':                 int((clean['HTN'] == 1).sum()) if 'HTN' in clean else 0,
    'n_obese':               int(clean['BMI_cat'].isin(['obese_I','obese_II','obese_III']).sum()),
    'mean_HbA1c':            float(clean['HbA1c'].mean()) if 'HbA1c' in clean else None,
    'mean_BMI':              float(clean['BMI'].mean()) if 'BMI' in clean else None,
    'pct_diabetic':          float((clean['T2DM']==1).mean()*100) if 'T2DM' in clean else None,
    'generated_at':          dt.datetime.now().isoformat(timespec='seconds'),
}
with open(os.path.join(OUT_DIR, 'kpis.json'), 'w') as f:
    json.dump(kpis, f, indent=2)
print(f"[6/6] KPIs: {kpis}")
