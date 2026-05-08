"""Generate architecture, DIKW, CommonKADS, workflow, and inference-flow diagrams."""
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
import os

PRIMARY = "#01696F"
ACCENT  = "#A84B2F"
SUCCESS = "#437A22"
ERROR   = "#A12C7B"
BG      = "#F7F6F2"
DARK    = "#1E2A2E"
LIGHT   = "#FFFFFF"
GREY    = "#5A6670"

ASSETS = "/home/user/workspace/Diab-KBS/assets"
os.makedirs(ASSETS, exist_ok=True)

plt.rcParams["font.family"] = "DejaVu Sans"


def save(fig, name):
    path = f"{ASSETS}/{name}.png"
    fig.savefig(path, dpi=180, bbox_inches="tight", facecolor=BG)
    plt.close(fig)
    print(f"saved {path}")


def box(ax, xy, w, h, text, color=PRIMARY, text_color=LIGHT,
        fontsize=10, weight="bold", radius=0.04):
    x, y = xy
    fb = FancyBboxPatch((x, y), w, h,
                        boxstyle=f"round,pad=0.02,rounding_size={radius}",
                        linewidth=1.2, edgecolor=DARK, facecolor=color)
    ax.add_patch(fb)
    ax.text(x + w/2, y + h/2, text, ha="center", va="center",
            fontsize=fontsize, color=text_color, weight=weight)


def header_strip(ax, xy, w, h, text, color=PRIMARY, fontsize=12):
    """Solid header strip with title only (no content overlapping)."""
    x, y = xy
    fb = FancyBboxPatch((x, y), w, h,
                        boxstyle="round,pad=0.02,rounding_size=0.03",
                        linewidth=1.2, edgecolor=DARK, facecolor=color)
    ax.add_patch(fb)
    ax.text(x + w/2, y + h/2, text, ha="center", va="center",
            fontsize=fontsize, color=LIGHT, weight="bold")


def container(ax, xy, w, h, color):
    """Outline container (no fill) — child boxes go inside."""
    x, y = xy
    fb = FancyBboxPatch((x, y), w, h,
                        boxstyle="round,pad=0.02,rounding_size=0.03",
                        linewidth=2.0, edgecolor=color, facecolor="white", alpha=0.4)
    ax.add_patch(fb)


def arrow(ax, p1, p2, color=DARK, style="->", lw=1.6, mut=14):
    a = FancyArrowPatch(p1, p2, arrowstyle=style, mutation_scale=mut,
                        color=color, lw=lw, shrinkA=4, shrinkB=4)
    ax.add_patch(a)


# =========================================================================
# 1) SYSTEM ARCHITECTURE
# =========================================================================
def make_architecture():
    fig, ax = plt.subplots(figsize=(14, 9.5))
    ax.set_xlim(0, 14); ax.set_ylim(0, 9.5); ax.axis("off")
    ax.set_facecolor(BG)
    ax.text(7, 9.15, "Diab-KBS — System Architecture",
            ha="center", fontsize=18, weight="bold", color=DARK)
    ax.text(7, 8.78, "Hybrid knowledge-based expert system for diabetes diagnosis & decision support",
            ha="center", fontsize=11, color=GREY, style="italic")

    # PRESENTATION LAYER (header + module boxes below)
    header_strip(ax, (0.4, 8.05), 13.2, 0.55,
                 "PRESENTATION  LAYER  —  Streamlit Dashboard (7 Modules)",
                 color=PRIMARY, fontsize=12)
    modules = ["Overview", "Patient Diagnosis", "Risk Stratification",
               "Big-Data Analytics", "Visualisation Gallery", "KB Browser", "Validation"]
    mw = (13.2 - 0.3) / 7
    for i, m in enumerate(modules):
        box(ax, (0.55 + i*mw, 7.40), mw - 0.1, 0.55, m,
            color=LIGHT, text_color=DARK, fontsize=8.6, weight="bold", radius=0.025)

    # MIDDLE BAND — KB | Inference | Explanation
    # KB container
    header_strip(ax, (0.4, 5.95), 3.6, 0.5, "KNOWLEDGE  BASE",
                 color=SUCCESS, fontsize=11)
    container(ax, (0.4, 3.55), 3.6, 2.4, SUCCESS)
    box(ax, (0.55, 5.30), 3.3, 0.50, "32 Production Rules",
        color=LIGHT, text_color=DARK, fontsize=9.5, weight="bold", radius=0.02)
    box(ax, (0.55, 4.70), 3.3, 0.50, "Frames & Inheritance",
        color=LIGHT, text_color=DARK, fontsize=9.5, weight="bold", radius=0.02)
    box(ax, (0.55, 4.10), 3.3, 0.50, "Semantic Network",
        color=LIGHT, text_color=DARK, fontsize=9.5, weight="bold", radius=0.02)
    box(ax, (0.55, 3.65), 3.3, 0.35, "JSON storage  ·  Mined decision tree",
        color=SUCCESS, text_color=LIGHT, fontsize=8, weight="normal", radius=0.015)

    # INFERENCE ENGINE container
    header_strip(ax, (4.30, 5.95), 5.4, 0.5, "INFERENCE  ENGINE",
                 color=ACCENT, fontsize=11)
    container(ax, (4.30, 3.55), 5.4, 2.4, ACCENT)
    sub_w = (5.4 - 0.6) / 3
    for i, t in enumerate(["Forward\nChaining", "Backward\nChaining", "Certainty\nFactors"]):
        box(ax, (4.45 + i*(sub_w + 0.15), 5.05), sub_w, 0.75, t,
            color=LIGHT, text_color=DARK, fontsize=10, weight="bold", radius=0.025)
    box(ax, (4.45, 4.30), 5.10, 0.55,
        "Working Memory  ·  Conflict Resolution",
        color=LIGHT, text_color=DARK, fontsize=9.5, weight="bold", radius=0.02)
    box(ax, (4.45, 3.65), 5.10, 0.55, "Why  ·  How  Explanation Facility",
        color=LIGHT, text_color=DARK, fontsize=9.5, weight="bold", radius=0.02)

    # EXPLANATION & VALIDATION container
    header_strip(ax, (10.00, 5.95), 3.6, 0.5, "EXPLANATION  &  VALIDATION",
                 color=ERROR, fontsize=11)
    container(ax, (10.00, 3.55), 3.6, 2.4, ERROR)
    box(ax, (10.15, 5.30), 3.3, 0.50, "Why / How Trace",
        color=LIGHT, text_color=DARK, fontsize=9.5, weight="bold", radius=0.02)
    box(ax, (10.15, 4.70), 3.3, 0.50, "Confusion Matrix",
        color=LIGHT, text_color=DARK, fontsize=9.5, weight="bold", radius=0.02)
    box(ax, (10.15, 4.10), 3.3, 0.50, "Accuracy 81.4%   F1 = 0.84",
        color=LIGHT, text_color=DARK, fontsize=9.5, weight="bold", radius=0.02)
    box(ax, (10.15, 3.65), 3.3, 0.35, "Verification · validation · evaluation",
        color=ERROR, text_color=LIGHT, fontsize=8, weight="normal", radius=0.015)

    # KNOWLEDGE ACQUISITION
    header_strip(ax, (0.4, 2.85), 13.2, 0.5,
                 "KNOWLEDGE  ACQUISITION  PIPELINE",
                 color=DARK, fontsize=12)
    container(ax, (0.4, 1.40), 13.2, 1.45, DARK)
    ka_w = (13.2 - 0.6) / 3
    for i, (t, c) in enumerate([
        ("MANUAL\nClinical guidelines (ADA, WHO)\nDr. Hossam protocol", PRIMARY),
        ("SEMI-AUTOMATIC\nDecision-tree induction\nfrom 12,204 patients", ACCENT),
        ("AUTOMATIC\nCertainty-factor calibration\nfrom data co-occurrence", SUCCESS),
    ]):
        box(ax, (0.55 + i*(ka_w + 0.15), 1.55), ka_w, 1.15, t,
            color=c, fontsize=9.5, weight="bold", radius=0.025)

    # DATA LAYER
    header_strip(ax, (0.4, 0.40), 13.2, 0.85,
                 "DATA  LAYER  —  12,204 patients × 37 features  ·  Dr. Hossam Diabetes Cohort",
                 color=GREY, fontsize=11)

    # Arrows
    arrow(ax, (7, 7.40), (7, 6.45), color=DARK, lw=1.8)
    # Bidirectional connectors between KB <-> IE <-> E&V (thick lines, large arrowheads)
    arrow(ax, (3.93, 4.75), (4.30, 4.75), color=DARK, style="<|-|>", lw=2.5, mut=24)
    arrow(ax, (9.70, 4.75), (10.07, 4.75), color=DARK, style="<|-|>", lw=2.5, mut=24)
    arrow(ax, (7, 3.55), (7, 3.35), color=DARK)
    arrow(ax, (7, 1.40), (7, 1.25), color=DARK)

    save(fig, "architecture")


# =========================================================================
# 2) DIKW PYRAMID
# =========================================================================
def make_dikw():
    fig, ax = plt.subplots(figsize=(11, 7.5))
    ax.set_xlim(0, 11); ax.set_ylim(0, 7.5); ax.axis("off")
    ax.set_facecolor(BG)
    ax.text(5.5, 7.15, "DIKW Hierarchy in Diab-KBS",
            ha="center", fontsize=17, weight="bold", color=DARK)
    ax.text(5.5, 6.80, "Lecture 1 — From raw data to actionable clinical wisdom",
            ha="center", fontsize=10.5, color=GREY, style="italic")

    # bottom-up: widest at base (DATA), narrowest at apex (WISDOM)
    levels = [
        ("DATA",       8.0,  9.0, "#437A22",
            "12,204 patient records  ·  37 cleaned features"),
        ("INFORMATION", 6.0,  8.0, "#01696F",
            "HbA1c category  ·  BMI class  ·  Risk score"),
        ("KNOWLEDGE",  4.0,  6.0, "#A84B2F",
            "32 rules  ·  Frames  ·  Semantic net"),
        ("WISDOM",     2.0,  4.0, "#7B2D26",
            "Action  ·  Triage urgency"),
    ]
    y_base = 1.0
    h = 1.15
    for label, w_top, w_bot, color, descr in levels:
        x_top = (11 - w_top)/2
        x_bot = (11 - w_bot)/2
        poly = plt.Polygon([(x_bot, y_base), (x_bot + w_bot, y_base),
                            (x_top + w_top, y_base + h), (x_top, y_base + h)],
                            facecolor=color, edgecolor=DARK, linewidth=1.5)
        ax.add_patch(poly)
        ax.text(5.5, y_base + h*0.62, label, ha="center", va="center",
                color=LIGHT, fontsize=14, weight="bold")
        ax.text(5.5, y_base + h*0.28, descr, ha="center", va="center",
                color=LIGHT, fontsize=8.8, style="italic")
        y_base += h

    # Right-side ascending arrow with labels
    ax.annotate("", xy=(10.3, 5.4), xytext=(10.3, 1.3),
                arrowprops=dict(arrowstyle="->", color=DARK, lw=2))
    ax.text(10.5, 1.7,  "+ structure",  fontsize=9.5, color=DARK)
    ax.text(10.5, 2.85, "+ patterns",   fontsize=9.5, color=DARK)
    ax.text(10.5, 4.00, "+ inference",  fontsize=9.5, color=DARK)
    ax.text(10.5, 5.15, "+ judgment",   fontsize=9.5, color=DARK)

    save(fig, "dikw_pyramid")


# =========================================================================
# 3) CommonKADS 6 MODELS
# =========================================================================
def make_commonkads():
    fig, ax = plt.subplots(figsize=(13.5, 9))
    ax.set_xlim(0, 13.5); ax.set_ylim(0, 9); ax.axis("off")
    ax.set_facecolor(BG)
    ax.text(6.75, 8.65, "CommonKADS — Six Models Applied to Diab-KBS",
            ha="center", fontsize=17, weight="bold", color=DARK)
    ax.text(6.75, 8.30, "Lecture 5 — Knowledge Engineering methodology",
            ha="center", fontsize=10.5, color=GREY, style="italic")

    # Layer labels
    ax.text(0.35, 6.80, "CONTEXT", fontsize=10.5, color=GREY,
            weight="bold", rotation=90, va="center")
    ax.text(0.35, 4.10, "CONCEPT", fontsize=10.5, color=GREY,
            weight="bold", rotation=90, va="center")
    ax.text(0.35, 1.55, "ARTEFACT", fontsize=10.5, color=GREY,
            weight="bold", rotation=90, va="center")

    # CONTEXT layer — three boxes
    ctx = [
        ("1. ORGANISATION  MODEL",
         "Hospital diabetes clinic\nStakeholders: physician,\nnurse, lab, patient\nBottleneck: high case load"),
        ("2. TASK  MODEL",
         "Diagnose type / stage\nAssess risks\nRecommend therapy\nTriage urgency"),
        ("3. AGENT  MODEL",
         "Physician  (final decision)\nDiab-KBS  (advisor)\nPatient  (input provider)\nLab system  (data feed)"),
    ]
    bw = 4.0
    for i, (title, body) in enumerate(ctx):
        x = 0.9 + i*(bw + 0.15)
        header_strip(ax, (x, 7.55), bw, 0.45, title, color=PRIMARY, fontsize=10.5)
        box(ax, (x, 5.85), bw, 1.65, body, color=LIGHT, text_color=DARK,
            fontsize=9.5, weight="normal", radius=0.025)

    # CONCEPT layer — two wider boxes
    concepts = [
        ("4. KNOWLEDGE  MODEL",
         "Domain knowledge:  diabetes ontology, frames, semantic net\n"
         "Inference knowledge: classify, abstract, match\n"
         "Task knowledge: diagnosis → risk → therapy\n"
         "32 production rules  +  decision-tree induced rules"),
        ("5. COMMUNICATION  MODEL",
         "Dialogue:  patient form → KBS → explanation\n"
         "Information items: symptoms, labs, vitals\n"
         "Transactions: query, assert, retract, why?, how?\n"
         "Streamlit UI as communication channel"),
    ]
    cw = 6.10
    for i, (title, body) in enumerate(concepts):
        x = 0.9 + i*(cw + 0.20)
        header_strip(ax, (x, 5.10), cw, 0.45, title, color=ACCENT, fontsize=10.5)
        box(ax, (x, 3.10), cw, 1.95, body, color=LIGHT, text_color=DARK,
            fontsize=9.5, weight="normal", radius=0.025)

    # ARTEFACT layer
    header_strip(ax, (0.9, 2.45), 12.30, 0.45, "6. DESIGN  MODEL",
                 color=SUCCESS, fontsize=10.5)
    box(ax, (0.9, 0.30), 12.30, 2.10,
        "Architecture:  3-tier  (UI ↔ Inference Engine ↔ Knowledge Base)\n"
        "Implementation:  Python 3 · Streamlit · Pandas · scikit-learn\n"
        "KB format:  JSON (rules, frames, semantic net, mined rules)\n"
        "Inference:  forward + backward chaining with MYCIN-style certainty factor algebra\n"
        "Validation: confusion matrix on 4 893 patients → 81.4% accuracy, F1 = 0.84",
        color=LIGHT, text_color=DARK, fontsize=10, weight="normal", radius=0.025)

    save(fig, "commonkads_models")


# =========================================================================
# 4) BIG-DATA WORKFLOW
# =========================================================================
def make_workflow():
    fig, ax = plt.subplots(figsize=(14, 5.0))
    ax.set_xlim(0, 14); ax.set_ylim(0, 5); ax.axis("off")
    ax.set_facecolor(BG)
    ax.text(7, 4.65, "Big-Data Analytics Workflow",
            ha="center", fontsize=17, weight="bold", color=DARK)
    ax.text(7, 4.30, "Lecture 2  —  Extract → Integrate → Mine → Visualise → Decide",
            ha="center", fontsize=10.5, color=GREY, style="italic")

    stages = [
        ("EXTRACT",    "Excel ingest\n12,204 records\n68 raw cols",          PRIMARY),
        ("CLEAN",      "Type coerce\nNull handling\nUnit alignment",         ACCENT),
        ("INTEGRATE",  "Feature derive\nHbA1c cat\nBMI class",               SUCCESS),
        ("MINE",       "Decision tree\nAssoc rules\nCF calibration",         ERROR),
        ("VISUALISE",  "12 chart types\nDashboard\nNetwork",                  PRIMARY),
        ("DECIDE",     "Inference\nDiagnosis\nExplanation",                  ACCENT),
    ]
    n = len(stages)
    box_w, box_h, gap = 1.95, 2.10, 0.18
    total = n*box_w + (n-1)*gap
    x0 = (14 - total)/2
    y0 = 1.5
    for i, (title, body, color) in enumerate(stages):
        x = x0 + i*(box_w + gap)
        header_strip(ax, (x, y0+box_h-0.55), box_w, 0.55, title, color=color, fontsize=11)
        box(ax, (x, y0), box_w, box_h-0.55, body,
            color=LIGHT, text_color=DARK, fontsize=9.5, weight="normal", radius=0.025)
        if i < n-1:
            arrow(ax, (x+box_w, y0+box_h/2), (x+box_w+gap, y0+box_h/2),
                  color=DARK, mut=18, lw=2)

    ax.text(7, 0.95, "Each stage logs to the workspace; mined artefacts feed back into the Knowledge Base.",
            ha="center", fontsize=9.5, color=GREY, style="italic")

    save(fig, "workflow")


# =========================================================================
# 5) INFERENCE FLOW (forward + backward)
# =========================================================================
def make_inference_flow():
    fig, axes = plt.subplots(1, 2, figsize=(14, 8))
    fig.patch.set_facecolor(BG)
    fig.suptitle("Inference Engine — Forward & Backward Chaining",
                 fontsize=17, weight="bold", color=DARK, y=0.98)

    def panel(ax, title, color, steps, footer):
        ax.set_xlim(0, 7); ax.set_ylim(0, 7.2); ax.axis("off")
        ax.set_facecolor(BG)
        ax.text(3.5, 6.80, title, ha="center", fontsize=13, weight="bold", color=color)
        y = 5.95
        for txt, c in steps:
            box(ax, (1.3, y), 4.4, 0.65, txt, color=c, fontsize=9.5,
                weight="normal", radius=0.025)
            arrow(ax, (3.5, y), (3.5, y-0.18), color=DARK)
            y -= 0.85
        box(ax, (1.3, y+0.15), 4.4, 0.55, footer,
            color=DARK, fontsize=9.5, weight="bold", radius=0.025)

    panel(axes[0], "Forward Chaining  (data-driven)", PRIMARY, [
        ("Start with patient facts in WM", PRIMARY),
        ("For each rule  check IF antecedents", ACCENT),
        ("Combine evidence with CF algebra", SUCCESS),
        ("Fire rule  assert conclusion", ERROR),
        ("Add new facts to working memory", PRIMARY),
        ("Iterate until fixed point reached", ACCENT),
    ], "→  Diagnosis · Risks · Treatments")

    panel(axes[1], "Backward Chaining  (goal-driven)", ACCENT, [
        ("Start with goal (e.g. T2DM?)", ACCENT),
        ("Find rules whose THEN matches goal", PRIMARY),
        ("For each rule, prove IF antecedents", SUCCESS),
        ("Antecedent in WM?  → proven", ERROR),
        ("Else recurse: antecedent = sub-goal", PRIMARY),
        ("Aggregate CFs ↑  return final CF", ACCENT),
    ], "→  Goal proven with CF, full trace")

    fig.savefig(f"{ASSETS}/inference_flow.png", dpi=180,
                bbox_inches="tight", facecolor=BG)
    plt.close(fig)
    print(f"saved {ASSETS}/inference_flow.png")


# =========================================================================
# 6) KA FLOW
# =========================================================================
def make_ka_flow():
    fig, ax = plt.subplots(figsize=(13, 6))
    ax.set_xlim(0, 13); ax.set_ylim(0, 6); ax.axis("off")
    ax.set_facecolor(BG)
    ax.text(6.5, 5.65, "Knowledge Acquisition — 5 Steps × 3 Sources",
            ha="center", fontsize=17, weight="bold", color=DARK)
    ax.text(6.5, 5.30, "Lecture 6  —  Manual · Semi-automatic · Automatic",
            ha="center", fontsize=10.5, color=GREY, style="italic")

    steps = ["Identify\nKnowledge", "Conceptualise", "Formalise", "Implement", "Validate"]
    n = len(steps)
    box_w, box_h, gap = 2.15, 0.85, 0.20
    total = n*box_w + (n-1)*gap
    x0 = (13 - total)/2
    y_top = 4.05
    for i, s in enumerate(steps):
        x = x0 + i*(box_w + gap)
        box(ax, (x, y_top), box_w, box_h, s, color=PRIMARY, fontsize=10.5)
        if i < n-1:
            arrow(ax, (x+box_w, y_top+box_h/2),
                  (x+box_w+gap, y_top+box_h/2), color=DARK, mut=18)

    sources = [
        ("MANUAL  —  ADA · WHO · Dr. Hossam protocol",                  ACCENT,  2.85),
        ("SEMI-AUTOMATIC  —  Decision-tree induction · scikit-learn",   SUCCESS, 1.85),
        ("AUTOMATIC  —  CF calibration · co-occurrence statistics",     ERROR,   0.85),
    ]
    for txt, color, y in sources:
        box(ax, (0.4, y), 12.2, 0.75, txt, color=color, fontsize=11)

    save(fig, "ka_flow")


for fn in (make_architecture, make_dikw, make_commonkads,
           make_workflow, make_inference_flow, make_ka_flow):
    fn()
print("ALL DIAGRAMS DONE")
