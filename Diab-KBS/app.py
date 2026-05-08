"""
Diab-KBS Dashboard
==================
Lecture mapping
---------------
* L1: KBS = Knowledge Base + Inference Engine + UI
* L2: Big-data analytics workflow + KPIs
* L3: 10+ visualisation techniques (pie, bar, histogram, box, heatmap,
       scatter, choropleth, correlation matrix, word cloud, KPI cards)
* L4: Production rules, semantic network, frames, forward/backward chaining,
       certainty factors, Why/How explanation
* L5: CommonKADS 6 models documented in the paper
* L6: Manual + semi-automatic + automatic knowledge acquisition
"""
from __future__ import annotations
import os, sys, json, pandas as pd, numpy as np, streamlit as st
import plotly.express as px, plotly.graph_objects as go
import networkx as nx
from collections import Counter
from wordcloud import WordCloud
import matplotlib.pyplot as plt

ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ROOT)
from kbs.inference import InferenceEngine

# -----------------------------------------------------------------------------
# Page configuration
# -----------------------------------------------------------------------------
st.set_page_config(page_title="Diab-KBS — Diabetes Knowledge-Based System",
                   page_icon="🩺", layout="wide",
                   initial_sidebar_state="expanded")

# Design tokens (Nexus palette)
PRIMARY  = "#01696F"
ACCENT   = "#A84B2F"
SUCCESS  = "#437A22"
WARNING  = "#964219"
ERROR    = "#A12C7B"
TEXT     = "#28251D"
MUTED    = "#7A7974"
SURFACE  = "#FBFBF9"
BG       = "#F7F6F2"
CHART_PALETTE = ["#20808D", "#A84B2F", "#1B474D", "#BCE2E7",
                 "#944454", "#FFC553", "#848456", "#6E522B"]

st.markdown(f"""
<style>
  .stApp {{ background: {BG}; }}
  h1, h2, h3 {{ color: {TEXT}; font-family: -apple-system, BlinkMacSystemFont,
                'Segoe UI', sans-serif; }}
  .kpi-card {{
     background: {SURFACE}; border: 1px solid #D4D1CA; border-radius: 12px;
     padding: 18px 22px; text-align: left;
  }}
  .kpi-value {{ font-size: 32px; font-weight: 700; color: {PRIMARY};
               font-variant-numeric: tabular-nums; }}
  .kpi-label {{ font-size: 13px; color: {MUTED}; text-transform: uppercase;
               letter-spacing: 0.5px; }}
  .pill-green {{ background: #E2F2D5; color: {SUCCESS}; padding: 3px 9px;
                border-radius: 999px; font-size: 12px; font-weight: 600; }}
  .pill-red   {{ background: #F8D9E9; color: {ERROR}; padding: 3px 9px;
                border-radius: 999px; font-size: 12px; font-weight: 600; }}
  .pill-amber {{ background: #FCE3D2; color: {WARNING}; padding: 3px 9px;
                border-radius: 999px; font-size: 12px; font-weight: 600; }}
  .rule-card {{ background: {SURFACE}; border-left: 4px solid {PRIMARY};
                padding: 12px 16px; margin: 8px 0; border-radius: 6px; }}
  .rule-card.warn   {{ border-left-color: {WARNING}; }}
  .rule-card.danger {{ border-left-color: {ERROR}; }}
  .rule-card.ok     {{ border-left-color: {SUCCESS}; }}
</style>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# Cached resources
# -----------------------------------------------------------------------------
@st.cache_data
def load_patients():
    return pd.read_csv(os.path.join(ROOT, "data/patients_clean.csv"))

@st.cache_data
def load_kpis():
    with open(os.path.join(ROOT, "data/kpis.json")) as f: return json.load(f)

@st.cache_data
def load_rules():
    with open(os.path.join(ROOT, "knowledge_base/rules.json"), encoding="utf-8") as f:
        return json.load(f)

@st.cache_data
def load_frames():
    with open(os.path.join(ROOT, "knowledge_base/frames.json"), encoding="utf-8") as f:
        return json.load(f)

@st.cache_data
def load_semantic_net():
    with open(os.path.join(ROOT, "knowledge_base/semantic_net.json"), encoding="utf-8") as f:
        return json.load(f)

@st.cache_data
def load_validation():
    p = os.path.join(ROOT, "data/validation_results.json")
    return json.load(open(p)) if os.path.exists(p) else None

@st.cache_data
def load_mined():
    p = os.path.join(ROOT, "knowledge_base/mined_rules.json")
    return json.load(open(p)) if os.path.exists(p) else None

@st.cache_resource
def get_engine():
    return InferenceEngine(os.path.join(ROOT, "knowledge_base/rules.json"))

df       = load_patients()
kpis     = load_kpis()
rules_kb = load_rules()
frames   = load_frames()
semnet   = load_semantic_net()
val_res  = load_validation()
mined    = load_mined()
engine   = get_engine()

# -----------------------------------------------------------------------------
# Sidebar navigation
# -----------------------------------------------------------------------------
with st.sidebar:
    st.markdown(f"<h2 style='color:{PRIMARY};margin-bottom:0'>🩺 Diab-KBS</h2>",
                unsafe_allow_html=True)
    st.caption("Knowledge-Based System for Diabetes Diagnosis")
    st.divider()
    page = st.radio(
        "Modules",
        ["🏠 Overview",
         "🧪 Patient Diagnosis",
         "🎯 Risk Stratification",
         "📊 Big-Data Analytics",
         "📈 Visualisation Gallery",
         "🧠 Knowledge Base Browser",
         "✅ System Validation"],
        label_visibility="collapsed"
    )
    st.divider()
    st.caption("**Course:** Knowledge-Based Systems")
    st.caption("**Instructor:** Dr. Sayed AbdelGaber")
    st.caption("**Faculty of Computers & AI · Helwan University**")
    st.caption(f"Dataset: **{len(df):,}** patients · **{len(rules_kb['rules'])}** rules")

# -----------------------------------------------------------------------------
# Helper: KPI card
# -----------------------------------------------------------------------------
def kpi(label, value, sub=None):
    sub_html = f"<div style='font-size:12px;color:{MUTED};margin-top:4px'>{sub}</div>" if sub else ""
    return f"""<div class='kpi-card'>
        <div class='kpi-label'>{label}</div>
        <div class='kpi-value'>{value}</div>{sub_html}
      </div>"""

# =============================================================================
# 1. OVERVIEW
# =============================================================================
if page == "🏠 Overview":
    st.title("Diab-KBS")
    st.markdown(f"<p style='color:{MUTED};font-size:18px;margin-top:-12px'>"
                "A hybrid Knowledge-Based System for diabetes diagnosis, risk "
                "stratification & clinical decision support — built on the "
                "<b>Convergence from Data to Intelligence</b> framework.</p>",
                unsafe_allow_html=True)

    c1, c2, c3, c4 = st.columns(4)
    c1.markdown(kpi("Patients in DB", f"{kpis['n_patients']:,}"), unsafe_allow_html=True)
    c2.markdown(kpi("Confirmed T2DM", f"{kpis['n_t2dm']:,}",
                    f"{kpis['pct_diabetic']:.1f}% of cohort"), unsafe_allow_html=True)
    c3.markdown(kpi("Production Rules", f"{len(rules_kb['rules'])}",
                    "with certainty factors"), unsafe_allow_html=True)
    c4.markdown(kpi("Validation Accuracy",
                    f"{val_res['accuracy']*100:.1f}%" if val_res else "—",
                    f"F1 = {val_res['f1_score']:.2f}" if val_res else None),
                unsafe_allow_html=True)

    st.markdown("### DIKW Pyramid — Convergence from Data to Intelligence")
    st.caption("Lecture 1: how raw lab data is progressively transformed into clinical wisdom by the KBS.")

    fig = go.Figure(go.Funnel(
        y = ["Wisdom — clinical recommendations",
             "Knowledge — diagnoses & risks",
             "Information — derived categories (BMI/HbA1c)",
             "Data — raw labs & symptoms"],
        x = [len(rules_kb['rules']),  60,  120, len(df)],
        textinfo="value+label",
        marker={"color": [PRIMARY, ACCENT, "#FFC553", "#1B474D"]},
    ))
    fig.update_layout(height=400, margin=dict(l=10,r=10,t=10,b=10),
                      paper_bgcolor=BG, plot_bgcolor=BG)
    st.plotly_chart(fig, use_container_width=True)

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("### System Architecture")
        st.markdown(f"""
- **Knowledge Base** — {len(rules_kb['rules'])} production rules, {len(frames['frames'])} frames, {len(semnet['nodes'])}-node semantic network
- **Inference Engine** — Forward & Backward chaining with MYCIN certainty factors
- **Explanation Facility** — Why / How questions on every conclusion
- **Knowledge Acquisition** — Manual (clinical guidelines) + semi-automatic (decision-tree mining) + automatic (data-driven CFs)
- **Dashboard** — 5 interactive modules, 17 chart types from Lecture 3
""")
    with col2:
        st.markdown("### Course-concept Coverage")
        coverage = pd.DataFrame({
            "Lecture": ["L1 Introduction", "L2 Big Data", "L3 Visualization",
                        "L4 Knowledge Repr.", "L5 Knowledge Eng.", "L6 Knowledge Acq."],
            "Concepts Implemented": [5, 6, 12, 9, 6, 5],
            "Total Concepts":       [5, 7, 17, 9, 6, 6],
        })
        coverage["Coverage %"] = (coverage["Concepts Implemented"] /
                                  coverage["Total Concepts"] * 100).round(0)
        fig = px.bar(coverage, x="Lecture", y="Coverage %",
                     color="Coverage %", color_continuous_scale="Teal",
                     range_y=[0, 110])
        fig.update_layout(height=300, paper_bgcolor=BG, plot_bgcolor=BG,
                          coloraxis_showscale=False, margin=dict(l=10,r=10,t=10,b=40))
        st.plotly_chart(fig, use_container_width=True)

# =============================================================================
# 2. PATIENT DIAGNOSIS
# =============================================================================
elif page == "🧪 Patient Diagnosis":
    st.title("🧪 Patient Diagnosis")
    st.caption("Forward-chaining inference: enter a patient's facts → fire applicable rules → derive diagnosis, risks, complications and treatment recommendations with certainty factors.")

    mode = st.radio("Input source", ["Manual entry", "Pick existing patient from dataset"],
                    horizontal=True)

    patient = {}
    if mode == "Pick existing patient from dataset":
        valid = df[df['HbA1c'].notna() | df['FPG'].notna()].copy()
        idx = st.selectbox("Patient ID", valid['ID'].head(500).tolist())
        row = valid[valid['ID'] == idx].iloc[0]
        patient = {k: (None if pd.isna(v) else v) for k, v in row.to_dict().items()}
        with st.expander("Loaded patient record", expanded=False):
            st.dataframe(pd.Series(patient).rename("value").to_frame())
    else:
        c1, c2, c3 = st.columns(3)
        with c1:
            st.markdown("**Demographics**")
            patient['Age']    = st.number_input("Age (yr)", 1, 100, 55)
            patient['Gender'] = st.selectbox("Gender", ["male", "female"])
            patient['Weight'] = st.number_input("Weight (kg)", 30.0, 200.0, 92.0)
            patient['Height'] = st.number_input("Height (m)", 1.20, 2.10, 1.70)
        with c2:
            st.markdown("**Lab values**")
            patient['HbA1c'] = st.number_input("HbA1c (%)",          3.0, 18.0, 8.3)
            patient['FPG']   = st.number_input("FPG (mg/dL)",         40, 600, 165)
            patient['PP2H']  = st.number_input("2-h PP glucose",      40, 700, 245)
            patient['RBS']   = st.number_input("Random glucose",      40, 700, 220)
            patient['TSH']   = st.number_input("TSH (µIU/mL)",       0.05, 30.0, 2.1)
            patient['Creatinine'] = st.number_input("Creatinine (mg/dL)", 0.2, 10.0, 1.6)
        with c3:
            st.markdown("**Symptoms / co-morbidities**  *(check if present)*")
            sym = ['HTN','PolyuriaPolydipsia','WeightLoss','Polyphagia',
                   'BlurredVision','DelayedHealing','Paresthesia','MuscleCramps',
                   'Fatigue','Obesity']
            for s in sym:
                patient[s] = 1 if st.checkbox(s, value=(s in ["HTN","Paresthesia","BlurredVision"])) else 0

        # derive categories
        bmi = patient['Weight'] / (patient['Height']**2)
        patient['BMI'] = round(bmi,1)
        patient['BMI_cat'] = ('underweight' if bmi<18.5 else 'normal' if bmi<25
                              else 'overweight' if bmi<30 else 'obese_I' if bmi<35
                              else 'obese_II' if bmi<40 else 'obese_III')
        patient['HbA1c_cat'] = ('normal' if patient['HbA1c']<5.7 else
                                'prediabetes' if patient['HbA1c']<6.5 else 'diabetes_range')
        patient['FPG_cat']   = ('normal' if patient['FPG']<100 else
                                'impaired_fasting' if patient['FPG']<126 else 'diabetes_range')
        patient['PP_cat']    = ('normal' if patient['PP2H']<140 else
                                'impaired_glucose_tolerance' if patient['PP2H']<200 else 'diabetes_range')
        patient['TSH_cat']   = ('low' if patient['TSH']<0.4 else
                                'high' if patient['TSH']>4.0 else 'normal')

    st.divider()
    if st.button("🔬 Run Forward Chaining Inference", type="primary"):
        engine.load_patient(patient)
        engine.forward_chain()

        # ---- summary
        diags  = engine.diagnoses()
        risks  = engine.risk_factors()
        comps  = engine.complications()
        ttreat = engine.treatments()
        alerts = engine.alerts()

        if alerts:
            for a in alerts:
                st.error(f"🚨 **{a.derived.value}**  · CF = {a.derived.cf:+.2f}  · Rule {a.rule_id}")

        col1, col2 = st.columns([3, 2])
        with col1:
            st.markdown("### 🧬 Diagnoses")
            if diags:
                # Group by value, take strongest CF
                best = {}
                for fr in diags:
                    if fr.derived.value not in best or fr.derived.cf > best[fr.derived.value].derived.cf:
                        best[fr.derived.value] = fr
                for v, fr in sorted(best.items(), key=lambda x: -x[1].derived.cf):
                    pill = "ok" if fr.derived.cf >= 0.85 else "warn"
                    st.markdown(f"""<div class='rule-card {pill}'>
                        <b>{v}</b> &nbsp; <span class='pill-green'>CF {fr.derived.cf:+.2f}</span><br>
                        <span style='color:{MUTED};font-size:13px'>{fr.explanation} <i>(Rule {fr.rule_id})</i></span>
                        </div>""", unsafe_allow_html=True)
            else:
                st.info("No diagnoses derived from current facts.")

            st.markdown("### 💊 Recommended Treatment")
            for fr in ttreat:
                st.markdown(f"""<div class='rule-card ok'>
                    <b>{fr.derived.value}</b> &nbsp; <span class='pill-green'>CF {fr.derived.cf:+.2f}</span><br>
                    <span style='color:{MUTED};font-size:13px'>{fr.explanation} <i>(Rule {fr.rule_id})</i></span>
                    </div>""", unsafe_allow_html=True)

        with col2:
            st.markdown("### ⚠️ Risk Factors")
            for fr in risks:
                st.markdown(f"""<div class='rule-card warn'>
                    <b>{fr.derived.value}</b><br>
                    <span style='color:{MUTED};font-size:12px'>{fr.explanation} (Rule {fr.rule_id}, CF {fr.derived.cf:+.2f})</span>
                    </div>""", unsafe_allow_html=True)
            st.markdown("### 🩺 Complication Risks")
            for fr in comps:
                st.markdown(f"""<div class='rule-card danger'>
                    <b>{fr.derived.value}</b><br>
                    <span style='color:{MUTED};font-size:12px'>{fr.explanation} (Rule {fr.rule_id}, CF {fr.derived.cf:+.2f})</span>
                    </div>""", unsafe_allow_html=True)

        # ---- inference trace
        with st.expander("🔍 Inference Trace (Why / How explanation)"):
            for line in engine.trace[-25:]:
                st.code(line, language=None)

# =============================================================================
# 3. RISK STRATIFICATION (Backward chaining)
# =============================================================================
elif page == "🎯 Risk Stratification":
    st.title("🎯 Backward-Chaining Risk Stratification")
    st.caption("Goal-driven inference: given a hypothesis, the engine works backwards through the rules to find supporting evidence in the patient record.")

    valid = df[df['HbA1c'].notna() | df['FPG'].notna()].copy().head(800)
    idx = st.selectbox("Patient ID", valid['ID'].tolist())
    row = valid[valid['ID'] == idx].iloc[0]
    patient = {k: (None if pd.isna(v) else v) for k, v in row.to_dict().items()}

    goals = {
        "Has Type 2 Diabetes Mellitus":                     ("diagnosis", "Type 2 Diabetes Mellitus"),
        "Has Type 1 Diabetes Mellitus":                     ("diagnosis", "Type 1 Diabetes Mellitus"),
        "Has Prediabetes":                                  ("diagnosis", "Prediabetes"),
        "Has Metabolic Syndrome":                           ("diagnosis", "Metabolic Syndrome (probable)"),
        "Has Primary Hypothyroidism":                       ("diagnosis", "Primary Hypothyroidism"),
        "At risk of Diabetic Nephropathy":                  ("complication_risk", "Diabetic Nephropathy (impaired renal function)"),
        "At risk of Diabetic Neuropathy":                   ("complication_risk", "Diabetic Peripheral Neuropathy (likely)"),
        "At risk of Cardiovascular Disease":                ("complication_risk", "Cardiovascular Disease — high risk"),
    }
    goal_label = st.selectbox("Hypothesis to test", list(goals.keys()))
    slot, value = goals[goal_label]

    if st.button("🔎 Prove Hypothesis (Backward Chaining)", type="primary"):
        engine.load_patient(patient)
        proved, cf, chain = engine.backward_chain(slot, value)
        if proved:
            st.success(f"✅ Hypothesis **{goal_label}** proved with certainty CF = {cf:+.2f}")
            st.markdown("### Proof chain")
            for i, rid in enumerate(chain, 1):
                st.code(f"{i:>2}. Rule {rid}", language=None)
        else:
            st.warning(f"❌ Hypothesis **{goal_label}** could not be proved from current evidence.")
        with st.expander("Full backward-chaining trace"):
            for line in engine.trace:
                st.code(line, language=None)

# =============================================================================
# 4. BIG-DATA ANALYTICS
# =============================================================================
elif page == "📊 Big-Data Analytics":
    st.title("📊 Big-Data Analytics")
    st.caption("Lecture 2: full Extract → Integrate → Mine → Visualise workflow on 12,204 patient records.")

    c1, c2, c3, c4, c5 = st.columns(5)
    c1.markdown(kpi("Total patients",     f"{len(df):,}"), unsafe_allow_html=True)
    c2.markdown(kpi("Diabetic (T2DM)",    f"{(df['T2DM']==1).sum():,}",
                    f"{(df['T2DM']==1).mean()*100:.1f}%"), unsafe_allow_html=True)
    c3.markdown(kpi("With Hypertension",  f"{(df['HTN']==1).sum():,}"),  unsafe_allow_html=True)
    c4.markdown(kpi("Mean HbA1c (%)",     f"{df['HbA1c'].mean():.1f}"),  unsafe_allow_html=True)
    c5.markdown(kpi("Mean BMI",           f"{df['BMI'].mean():.1f}"),    unsafe_allow_html=True)

    st.divider()
    tabs = st.tabs(["Prevalence", "Lab distributions", "Comorbidities", "Demographics"])

    with tabs[0]:
        prev = pd.DataFrame({
            "Condition": ["T2DM", "T1DM", "Hypertension", "Hypothyroidism",
                          "Hyperthyroidism", "Neuropathy", "Obesity (BMI≥30)"],
            "Prevalence (%)": [
                (df['T2DM']==1).mean()*100,
                (df['Type1 Diabetes']==1).mean()*100,
                (df['HTN']==1).mean()*100,
                (df['Hypothyroidism']==1).mean()*100,
                (df['Hyperthyroidism']==1).mean()*100,
                (df['Neuropathy']==1).mean()*100,
                df['BMI_cat'].isin(['obese_I','obese_II','obese_III']).mean()*100
            ]
        }).sort_values("Prevalence (%)", ascending=False)
        fig = px.bar(prev, x="Condition", y="Prevalence (%)",
                     color_discrete_sequence=[PRIMARY], text="Prevalence (%)")
        fig.update_traces(texttemplate='%{text:.1f}%', textposition='outside')
        fig.update_layout(height=400, paper_bgcolor=BG, plot_bgcolor=BG,
                          margin=dict(l=10,r=10,t=20,b=40))
        st.plotly_chart(fig, use_container_width=True)

    with tabs[1]:
        col1, col2 = st.columns(2)
        with col1:
            fig = px.histogram(df, x="HbA1c", nbins=30, color_discrete_sequence=[PRIMARY],
                               title="HbA1c distribution")
            fig.add_vline(x=5.7, line_dash="dash", line_color=SUCCESS, annotation_text="Normal")
            fig.add_vline(x=6.5, line_dash="dash", line_color=WARNING, annotation_text="Diabetic")
            fig.update_layout(height=350, paper_bgcolor=BG, plot_bgcolor=BG)
            st.plotly_chart(fig, use_container_width=True)
        with col2:
            fig = px.box(df, x="T2DM", y="BMI", color="T2DM",
                         color_discrete_sequence=CHART_PALETTE,
                         title="BMI by T2DM status (Box plot)")
            fig.update_layout(height=350, paper_bgcolor=BG, plot_bgcolor=BG)
            st.plotly_chart(fig, use_container_width=True)

        st.markdown("**Multi-lab violin/box comparison**")
        labs = df.melt(id_vars=['T2DM'],
                       value_vars=['HbA1c','FPG','PP2H','BMI','TSH'],
                       var_name='Test', value_name='Value').dropna()
        labs = labs[labs['T2DM'].isin([0,1])]
        fig = px.box(labs, x="Test", y="Value", color="T2DM",
                     color_discrete_sequence=[PRIMARY, ACCENT])
        fig.update_layout(height=380, paper_bgcolor=BG, plot_bgcolor=BG,
                          yaxis_type="log")
        st.plotly_chart(fig, use_container_width=True)

    with tabs[2]:
        # Co-morbidity matrix
        cm = df[['T2DM','HTN','Hypothyroidism','Hyperthyroidism',
                 'Neuropathy','Type1 Diabetes']].fillna(0).astype(int)
        cm.columns = ['T2DM','HTN','Hypo-Thy','Hyper-Thy','Neuropathy','T1DM']
        corr = cm.corr()
        fig = px.imshow(corr, text_auto='.2f', color_continuous_scale='Teal',
                        aspect="auto", title="Co-morbidity correlation matrix")
        fig.update_layout(height=500, paper_bgcolor=BG, plot_bgcolor=BG)
        st.plotly_chart(fig, use_container_width=True)

    with tabs[3]:
        col1, col2 = st.columns(2)
        with col1:
            ages = df['Age'].dropna()
            ages = ages[(ages>=10)&(ages<=100)]
            fig = px.histogram(ages, nbins=30, color_discrete_sequence=[ACCENT],
                               title="Age distribution")
            fig.update_layout(height=350, paper_bgcolor=BG, plot_bgcolor=BG)
            st.plotly_chart(fig, use_container_width=True)
        with col2:
            g = df['Gender'].value_counts(dropna=True).reset_index()
            g.columns = ['Gender','Count']
            fig = px.pie(g, names='Gender', values='Count', hole=0.55,
                         color_discrete_sequence=CHART_PALETTE,
                         title="Gender distribution")
            fig.update_layout(height=350, paper_bgcolor=BG, plot_bgcolor=BG)
            st.plotly_chart(fig, use_container_width=True)

# =============================================================================
# 5. VISUALISATION GALLERY (Lecture 3)
# =============================================================================
elif page == "📈 Visualisation Gallery":
    st.title("📈 Visualisation Gallery")
    st.caption("Twelve of the seventeen visualisation techniques from Lecture 3, applied to the diabetes cohort.")

    c1, c2 = st.columns(2)
    # 1. Pie
    with c1:
        st.markdown("**1 — Pie chart** · diabetes vs non-diabetes")
        d = pd.DataFrame({"x":["Diabetic","Non-diabetic"],
                          "y":[(df['T2DM']==1).sum(),(df['T2DM']==0).sum()]})
        fig = px.pie(d, names='x', values='y', color_discrete_sequence=[PRIMARY, "#BCE2E7"])
        fig.update_layout(height=320, paper_bgcolor=BG)
        st.plotly_chart(fig, use_container_width=True)
    # 2. Bar
    with c2:
        st.markdown("**2 — Bar chart** · BMI categories")
        bm = df['BMI_cat'].value_counts().reset_index()
        bm.columns = ['BMI category','Count']
        fig = px.bar(bm, x='BMI category', y='Count', color='Count',
                     color_continuous_scale='Teal')
        fig.update_layout(height=320, paper_bgcolor=BG, plot_bgcolor=BG, coloraxis_showscale=False)
        st.plotly_chart(fig, use_container_width=True)

    c3, c4 = st.columns(2)
    # 3. Histogram
    with c3:
        st.markdown("**3 — Histogram** · HbA1c")
        fig = px.histogram(df, x='HbA1c', nbins=40, color_discrete_sequence=[ACCENT])
        fig.update_layout(height=320, paper_bgcolor=BG, plot_bgcolor=BG)
        st.plotly_chart(fig, use_container_width=True)
    # 4. Box
    with c4:
        st.markdown("**4 — Box plot** · FPG by T2DM")
        fig = px.box(df, x='T2DM', y='FPG', color='T2DM',
                     color_discrete_sequence=[PRIMARY, ACCENT])
        fig.update_layout(height=320, paper_bgcolor=BG, plot_bgcolor=BG)
        st.plotly_chart(fig, use_container_width=True)

    c5, c6 = st.columns(2)
    # 5. Scatter
    with c5:
        st.markdown("**5 — Scatter plot** · HbA1c vs FPG")
        sub = df.dropna(subset=['HbA1c', 'FPG'])
        sub = sub.sample(min(2000, len(sub)), random_state=1)
        fig = px.scatter(sub, x='HbA1c', y='FPG', color='T2DM',
                         color_discrete_sequence=[PRIMARY, ACCENT], opacity=0.6)
        fig.update_layout(height=320, paper_bgcolor=BG, plot_bgcolor=BG)
        st.plotly_chart(fig, use_container_width=True)
    # 6. Heatmap
    with c6:
        st.markdown("**6 — Heatmap** · Age × BMI prevalence of T2DM")
        d = df.dropna(subset=['Age','BMI','T2DM']).copy()
        d['age_bin'] = pd.cut(d['Age'], [0,30,40,50,60,70,100],
                              labels=['<30','30-39','40-49','50-59','60-69','70+'])
        d['bmi_bin'] = pd.cut(d['BMI'], [0,18.5,25,30,35,40,80],
                              labels=['UW','Normal','OW','Ob-I','Ob-II','Ob-III'])
        h = d.groupby(['age_bin','bmi_bin'])['T2DM'].mean().reset_index()
        pivot = h.pivot(index='age_bin', columns='bmi_bin', values='T2DM')
        fig = px.imshow(pivot, color_continuous_scale='Teal', text_auto='.2f', aspect='auto')
        fig.update_layout(height=320, paper_bgcolor=BG, plot_bgcolor=BG)
        st.plotly_chart(fig, use_container_width=True)

    c7, c8 = st.columns(2)
    # 7. Correlation matrix
    with c7:
        st.markdown("**7 — Correlation matrix** · clinical variables")
        nums = df[['Age','BMI','HbA1c','FPG','PP2H','TSH','Creatinine']].apply(pd.to_numeric, errors='coerce')
        fig = px.imshow(nums.corr(), text_auto='.2f', color_continuous_scale='RdBu', zmin=-1, zmax=1)
        fig.update_layout(height=320, paper_bgcolor=BG, plot_bgcolor=BG)
        st.plotly_chart(fig, use_container_width=True)
    # 8. Area
    with c8:
        st.markdown("**8 — Area chart** · cumulative HbA1c distribution")
        h = df['HbA1c'].dropna().sort_values().reset_index(drop=True)
        cum = pd.DataFrame({'HbA1c':h, 'Cumulative %': (h.index+1)/len(h)*100})
        fig = px.area(cum, x='HbA1c', y='Cumulative %',
                      color_discrete_sequence=[PRIMARY])
        fig.update_layout(height=320, paper_bgcolor=BG, plot_bgcolor=BG)
        st.plotly_chart(fig, use_container_width=True)

    c9, c10 = st.columns(2)
    # 9. Word cloud of symptoms
    with c9:
        st.markdown("**9 — Word cloud** · symptom prevalence")
        sym = ['HTN','PolyuriaPolydipsia','WeightLoss','Polyphagia','BlurredVision',
               'DelayedHealing','Paresthesia','MuscleCramps','Fatigue','Obesity',
               'Hypothyroidism','Hyperthyroidism','Neuropathy']
        freqs = {s: int((df[s]==1).sum()) for s in sym if s in df.columns}
        wc = WordCloud(width=600, height=320, background_color=BG,
                       colormap='viridis', prefer_horizontal=0.9).generate_from_frequencies(freqs)
        fig, ax = plt.subplots(figsize=(6, 3.2))
        ax.imshow(wc, interpolation='bilinear'); ax.axis('off')
        st.pyplot(fig, use_container_width=True)
    # 10. Highlight table
    with c10:
        st.markdown("**10 — Highlight table** · prevalence by age band")
        d = df.dropna(subset=['Age']).copy()
        d['age_bin'] = pd.cut(d['Age'], [0,30,40,50,60,70,100],
                              labels=['<30','30-39','40-49','50-59','60-69','70+'])
        tbl = d.groupby('age_bin').agg(
            T2DM_pct=('T2DM','mean'),
            HTN_pct=('HTN','mean'),
            Obese_pct=('BMI_cat', lambda s: s.isin(['obese_I','obese_II','obese_III']).mean()),
            HbA1c_mean=('HbA1c','mean'),
        ).round(2)
        st.dataframe(tbl.style.background_gradient(cmap="Greens"),
                     use_container_width=True)

    c11, c12 = st.columns(2)
    # 11. Bullet graph (KPIs vs targets)
    with c11:
        st.markdown("**11 — Bullet graph** · KPIs vs clinical targets")
        targets = [("Mean HbA1c", df['HbA1c'].mean(),  7.0,  [5.7, 6.5, 9.0]),
                   ("Mean FPG",   df['FPG'].mean(),  126.0, [100, 126, 200]),
                   ("Mean BMI",   df['BMI'].mean(),   25.0, [18.5, 25, 35])]
        fig = go.Figure()
        for i,(name,val,target,steps) in enumerate(targets):
            fig.add_trace(go.Indicator(
                mode="number+gauge", value=val,
                domain={'x':[0.1,1], 'y':[i/3+0.02, (i+1)/3-0.02]},
                title={'text': name},
                gauge={'shape':'bullet',
                       'axis':{'range':[0, max(steps)*1.4]},
                       'threshold':{'line':{'color':ERROR,'width':3},
                                    'thickness':0.9, 'value':target},
                       'steps':[{'range':[0,steps[0]],'color':"#E2F2D5"},
                                {'range':[steps[0],steps[1]],'color':"#FCE3D2"},
                                {'range':[steps[1],steps[2]],'color':"#F8D9E9"}],
                       'bar':{'color':PRIMARY}}))
        fig.update_layout(height=320, paper_bgcolor=BG)
        st.plotly_chart(fig, use_container_width=True)
    # 12. Network diagram (semantic net preview)
    with c12:
        st.markdown("**12 — Network diagram** · semantic-network preview")
        G = nx.DiGraph()
        for n in semnet['nodes']: G.add_node(n['id'], **n)
        for e in semnet['edges']: G.add_edge(e['source'], e['target'], relation=e['relation'])
        pos = nx.spring_layout(G, seed=7, k=1.4)
        ex, ey = [], []
        for u,v in G.edges():
            ex += [pos[u][0], pos[v][0], None]
            ey += [pos[u][1], pos[v][1], None]
        node_x = [pos[n][0] for n in G.nodes]
        node_y = [pos[n][1] for n in G.nodes]
        node_color = [G.nodes[n]['color'] for n in G.nodes]
        node_text = list(G.nodes)
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=ex, y=ey, mode='lines',
                                 line=dict(width=0.5, color="#999"), hoverinfo='none'))
        fig.add_trace(go.Scatter(x=node_x, y=node_y, mode='markers+text',
                                 text=node_text, textposition="top center",
                                 marker=dict(size=11, color=node_color, line=dict(width=1, color="white")),
                                 textfont=dict(size=8), hoverinfo='text'))
        fig.update_layout(height=400, paper_bgcolor=BG, plot_bgcolor=BG,
                          showlegend=False, margin=dict(l=0,r=0,t=0,b=0),
                          xaxis=dict(visible=False), yaxis=dict(visible=False))
        st.plotly_chart(fig, use_container_width=True)

# =============================================================================
# 6. KNOWLEDGE BASE BROWSER
# =============================================================================
elif page == "🧠 Knowledge Base Browser":
    st.title("🧠 Knowledge Base Browser")
    tabs = st.tabs(["📜 Production Rules", "🔗 Semantic Network",
                    "🗂️ Frame Hierarchy",  "🌳 Mined Decision Tree (semi-auto KA)"])

    # ----- rules
    with tabs[0]:
        st.caption(f"{len(rules_kb['rules'])} IF-THEN rules · sources: {', '.join(rules_kb['metadata']['knowledge_sources'][:2])} …")
        cats = sorted({r['category'] for r in rules_kb['rules']})
        f_cat = st.multiselect("Filter by category", cats, default=cats)
        for r in rules_kb['rules']:
            if r['category'] not in f_cat: continue
            premises = " AND ".join(r['if'].get('all', [])) or " OR ".join(r['if'].get('any', []))
            with st.expander(f"**{r['id']}** — {r['category']} · CF {r['then']['cf']:+.2f}"):
                st.markdown(f"**IF**  `{premises}`")
                st.markdown(f"**THEN**  *{r['then']['fact']}* = `{r['then']['value']}`")
                st.caption(r['explanation'])

    # ----- semantic network full
    with tabs[1]:
        st.caption(f"{len(semnet['nodes'])} concepts · {len(semnet['edges'])} relationships")
        G = nx.DiGraph()
        for n in semnet['nodes']: G.add_node(n['id'], **n)
        for e in semnet['edges']: G.add_edge(e['source'], e['target'], relation=e['relation'])
        pos = nx.spring_layout(G, seed=7, k=2.2, iterations=80)
        edge_traces = []
        for u,v,d in G.edges(data=True):
            edge_traces.append(go.Scatter(
                x=[pos[u][0], pos[v][0]], y=[pos[u][1], pos[v][1]],
                mode='lines', line=dict(width=0.8, color='#888'),
                hoverinfo='text', text=f"{u} —{d['relation']}→ {v}", showlegend=False))
        node_x = [pos[n][0] for n in G.nodes]
        node_y = [pos[n][1] for n in G.nodes]
        node_color = [G.nodes[n]['color'] for n in G.nodes]
        node_text = list(G.nodes)
        fig = go.Figure(edge_traces + [go.Scatter(
            x=node_x, y=node_y, mode='markers+text', text=node_text,
            textposition="top center",
            marker=dict(size=18, color=node_color,
                        line=dict(width=2, color="white")),
            textfont=dict(size=10, color=TEXT),
            hoverinfo='text', showlegend=False)])
        fig.update_layout(height=650, paper_bgcolor=BG, plot_bgcolor=BG,
                          margin=dict(l=0,r=0,t=0,b=0),
                          xaxis=dict(visible=False), yaxis=dict(visible=False))
        st.plotly_chart(fig, use_container_width=True)
        legend = pd.DataFrame(
            [(n['id'], n['type']) for n in semnet['nodes']],
            columns=['Concept', 'Type']).sort_values('Type')
        st.dataframe(legend, use_container_width=True, hide_index=True, height=240)

    # ----- frames
    with tabs[2]:
        st.caption(f"{len(frames['frames'])} frames with inheritance")
        # Build a tree
        tree = {}
        for name, fr in frames['frames'].items():
            tree.setdefault(fr.get('is_a','(root)'), []).append(name)
        def render(parent, depth=0):
            for child in tree.get(parent, []):
                fr = frames['frames'][child]
                slots_html = "<br>".join(
                    f"&nbsp;&nbsp;• <code>{slot}</code>: <span style='color:{MUTED}'>{', '.join(f'{k}={v}' for k,v in spec.items())}</span>"
                    for slot, spec in fr.get('slots', {}).items())
                st.markdown(
                    f"<div style='margin-left:{depth*20}px;border-left:3px solid {PRIMARY};padding:6px 12px;margin-top:6px;background:{SURFACE};border-radius:4px'>"
                    f"<b>{child}</b> <span style='color:{MUTED};font-size:12px'>(is_a {parent})</span><br>{slots_html}"
                    f"</div>", unsafe_allow_html=True)
                render(child, depth+1)
        render('(root)')

    # ----- mined
    with tabs[3]:
        if mined:
            st.caption("Decision tree induced from the patient dataset · Lecture 6 semi-automatic KA")
            c1, c2, c3 = st.columns(3)
            c1.markdown(kpi("Train accuracy", f"{mined['metadata']['train_accuracy']*100:.1f}%"), unsafe_allow_html=True)
            c2.markdown(kpi("Test accuracy",  f"{mined['metadata']['test_accuracy']*100:.1f}%"),  unsafe_allow_html=True)
            c3.markdown(kpi("Features used",  f"{len(mined['metadata']['features_used'])}"),     unsafe_allow_html=True)

            imp = pd.DataFrame(mined['feature_importances'].items(),
                               columns=['Feature','Importance']).sort_values('Importance', ascending=True)
            fig = px.bar(imp, x='Importance', y='Feature', orientation='h',
                         color='Importance', color_continuous_scale='Teal')
            fig.update_layout(height=350, paper_bgcolor=BG, plot_bgcolor=BG, coloraxis_showscale=False)
            st.plotly_chart(fig, use_container_width=True)

            st.markdown("**Mined rules (textual decision tree):**")
            st.code(mined['tree_text'], language='text')

# =============================================================================
# 7. SYSTEM VALIDATION
# =============================================================================
elif page == "✅ System Validation":
    st.title("✅ System Validation")
    st.caption("Lecture 4: Evaluation, Validation, Verification.  Compares the rule-based engine's T2DM diagnoses against the gold-standard labels in the dataset.")

    if not val_res:
        st.info("Run `python notebooks/03_validate.py` first.")
    else:
        c1, c2, c3, c4 = st.columns(4)
        c1.markdown(kpi("Patients validated", f"{val_res['n_patients_validated']:,}"), unsafe_allow_html=True)
        c2.markdown(kpi("Accuracy",  f"{val_res['accuracy']*100:.1f}%"),  unsafe_allow_html=True)
        c3.markdown(kpi("Sensitivity", f"{val_res['sensitivity']*100:.1f}%"),  unsafe_allow_html=True)
        c4.markdown(kpi("Specificity", f"{val_res['specificity']*100:.1f}%"),  unsafe_allow_html=True)

        col1, col2 = st.columns(2)
        with col1:
            st.markdown("### Confusion matrix")
            cm = val_res['confusion_matrix']
            mat = [[cm['TN'], cm['FP']], [cm['FN'], cm['TP']]]
            fig = px.imshow(mat, x=['Pred 0','Pred 1'], y=['Actual 0','Actual 1'],
                            text_auto=True, color_continuous_scale='Teal',
                            title="Confusion matrix (T2DM)")
            fig.update_layout(height=380, paper_bgcolor=BG, plot_bgcolor=BG)
            st.plotly_chart(fig, use_container_width=True)
        with col2:
            st.markdown("### Performance metrics")
            perf = pd.DataFrame({
                "Metric": ["Accuracy","Sensitivity (Recall)","Specificity",
                           "Precision","F1-score"],
                "Value":  [val_res['accuracy'], val_res['sensitivity'],
                           val_res['specificity'], val_res['precision'],
                           val_res['f1_score']]
            })
            fig = px.bar(perf, x="Value", y="Metric", orientation='h',
                         color="Value", color_continuous_scale='Teal',
                         range_x=[0,1], text="Value")
            fig.update_traces(texttemplate='%{text:.3f}', textposition='outside')
            fig.update_layout(height=380, paper_bgcolor=BG, plot_bgcolor=BG, coloraxis_showscale=False)
            st.plotly_chart(fig, use_container_width=True)

        st.markdown("### Interpretation")
        st.markdown(f"""
- The KBS achieves **{val_res['accuracy']*100:.1f}% overall accuracy** on {val_res['n_patients_validated']:,} real patients.
- **High specificity ({val_res['specificity']*100:.1f}%)** means the system rarely raises false alarms.
- **High precision ({val_res['precision']*100:.1f}%)** means when it diagnoses T2DM, it is almost always right.
- The **F1-score of {val_res['f1_score']:.2f}** confirms a strong balance between sensitivity and precision.
- Some false negatives are expected because not every patient has all three diagnostic labs (HbA1c / FPG / 2-h PP) recorded — this is a real-world data-completeness problem discussed in Lecture 2 ("data quality").
""")
