# Diab-KBS — Diabetes Knowledge-Based System

A hybrid Knowledge-Based System for diabetes diagnosis, risk stratification, and clinical decision support. Built as a graduation-style project for the **Knowledge-Based Systems** course (Faculty of Computers & AI, Helwan University) under **Dr. Sayed AbdelGaber**.

---

## Highlights

- **12,204-patient cohort** with 37 cleaned features (Egyptian outpatient clinic dataset)
- **32 production rules** with MYCIN-style certainty factors, **13 frames** with inheritance, **35-node semantic network**
- **Forward + backward chaining** inference engine with explainable derivations
- **Apriori rule mining** complements hand-curated knowledge
- **7-page Streamlit dashboard** — overview, patient diagnosis, risk stratification, big-data analytics, visualisation gallery, KB browser, system validation
- **Validation**: Accuracy 81.4 %, Sensitivity 78.2 %, Specificity 87.2 %, Precision 91.7 %, F1 = 0.844 on 4,893 hold-out patients

---

## Repository layout

```
Diab-KBS/
├── app.py                     # Streamlit dashboard (7 pages)
├── kbs/                       # Inference engine
│   ├── inference.py           #   Forward + backward chaining
│   └── certainty.py           #   MYCIN certainty-factor algebra
├── knowledge_base/            # Knowledge artefacts (JSON)
│   ├── rules.json             #   32 production rules
│   ├── frames.json            #   13 frames + inheritance
│   ├── semantic_net.json      #   35 nodes · 35 edges
│   └── mined_rules.json       #   Apriori-mined associations
├── data/                      # Cleaned dataset & metrics
│   ├── patients_clean.csv     #   12,204 × 37
│   ├── kpis.json              #   Cohort KPIs
│   └── validation_results.json
├── notebooks/                 # Reproducible build scripts
│   ├── 01_preprocess.py       #   Excel → cleaned CSV
│   ├── 02_mine_rules.py       #   Apriori + decision-tree induction
│   ├── 03_validate.py         #   Hold-out validation
│   ├── 04_diagrams.py         #   6 publication-ready PNGs
│   ├── 05_paper.py            #   Research_Paper.pdf (ReportLab)
│   └── 06_deck.js             #   Defense.pptx (pptxgenjs)
├── docs/                      # Final deliverables
│   ├── Research_Paper.pdf     #   25 pages, 6 figures, 12 references
│   └── Defense.pptx           #   22-slide defense deck
└── assets/                    # Architecture diagrams & screenshots
```

---

## Quick start

```bash
# 1. Install dependencies
pip install streamlit pandas numpy plotly networkx mlxtend scikit-learn reportlab matplotlib pillow openpyxl

# 2. Launch the dashboard
streamlit run app.py

# 3. (Optional) regenerate artefacts
python notebooks/01_preprocess.py    # rebuild data/patients_clean.csv
python notebooks/02_mine_rules.py    # mine association rules
python notebooks/03_validate.py      # recompute validation metrics
python notebooks/04_diagrams.py      # rebuild architecture PNGs
python notebooks/05_paper.py         # rebuild Research_Paper.pdf
node   notebooks/06_deck.js          # rebuild Defense.pptx (pptxgenjs)
```

The dashboard binds to `localhost:8501` by default. Use the sidebar to navigate the 7 modules.

---

## Course-concept coverage

Every lecture in the course material maps to a concrete artefact in this repo:

| Lecture | Topic                              | Implementation                                          |
|---------|------------------------------------|--------------------------------------------------------|
| 1       | DIKW pyramid                       | `assets/dikw_pyramid.png` · dashboard Overview page    |
| 2       | KBS architecture & components      | 3-tier app · `assets/architecture.png`                 |
| 3       | Knowledge representation           | `knowledge_base/*.json` (rules · frames · semantic net) |
| 4       | Inference & reasoning              | `kbs/inference.py` (forward + backward chaining)       |
| 5       | Knowledge acquisition              | `assets/ka_flow.png` · 5-stage pipeline                 |
| 6       | CommonKADS methodology             | `docs/Research_Paper.pdf` § 4 — all 6 models           |
| 7       | Big-Data analytics                 | `notebooks/02_mine_rules.py` + Big-Data Analytics page |

---

## Deliverables

- **`docs/Research_Paper.pdf`** — 25-page paper covering all 6 CommonKADS models, validation, and 12 references
- **`docs/Defense.pptx`** — 22-slide defense deck (pptxgenjs, system fonts only)
- **`app.py`** — interactive Streamlit dashboard
- **`knowledge_base/`** — full KB exposed as inspectable JSON
- **`data/patients_clean.csv`** — reproducible cleaned cohort
- **`assets/*.png`** — 6 publication-ready architecture & workflow diagrams

---

## Author

**Aya Hesham Ali**  
Faculty of Computers & Artificial Intelligence, Helwan University  
`aya.hesham.ali.pbis2026@commerce.helwan.edu.eg`  
May 2026
