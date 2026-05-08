// Diab-KBS Defense Deck — pptxgenjs
// Run: node notebooks/06_deck.js
const pptxgen = require('/home/user/node_modules/pptxgenjs');

const pres = new pptxgen();
pres.layout = 'LAYOUT_WIDE'; // 13.333 x 7.5 inches
pres.author = 'Aya Hesham Ali';
pres.company = 'Faculty of Computers and AI, Helwan University';
pres.title = 'Diab-KBS - Knowledge-Based System for Diabetes Diagnosis';

// ------------------------------------------------------------------ palette
const C = {
  bg:       'F7F6F2',
  surface:  'FBFBF9',
  border:   'D4D1CA',
  text:     '1E2A2E',
  muted:    '5A6670',
  faint:    'BAB9B4',
  primary:  '01696F',
  primaryD: '0C4E54',
  accent:   'A84B2F',
  success:  '437A22',
  error:    'A12C7B',
  dark:     '1E2A2E',
  soft:     'E8E2D4',
  white:    'FFFFFF',
};

const F = { head: 'Trebuchet MS', body: 'Calibri' };

const SW = 13.333, SH = 7.5;
const ASSETS = '/home/user/workspace/Diab-KBS/assets';

// ------------------------------------------------------------------ helpers
function addBaseLight(slide) {
  slide.background = { color: C.bg };
}
function addBaseDark(slide) {
  slide.background = { color: C.dark };
}
function addHeaderBar(slide, title, eyebrow) {
  // Top header band
  slide.addShape('rect', { x: 0, y: 0, w: SW, h: 0.55, fill: { color: C.primary }, line: { color: C.primary } });
  slide.addText('Diab-KBS  ·  Diabetes Knowledge-Based System', {
    x: 0.5, y: 0.0, w: 8, h: 0.55,
    fontFace: F.body, fontSize: 11, color: C.white, valign: 'middle',
  });
  slide.addText(eyebrow || '', {
    x: SW - 4.5, y: 0.0, w: 4, h: 0.55,
    fontFace: F.body, fontSize: 11, color: C.white, align: 'right', valign: 'middle',
  });
  slide.addText(title, {
    x: 0.5, y: 0.75, w: SW - 1, h: 0.7,
    fontFace: F.head, fontSize: 30, bold: true, color: C.dark,
  });
}
function addFooter(slide, page, total) {
  slide.addText(`${page} / ${total}`, {
    x: SW - 1.0, y: SH - 0.4, w: 0.7, h: 0.3,
    fontFace: F.body, fontSize: 9, color: C.muted, align: 'right',
  });
  slide.addText('Aya Hesham Ali  ·  Helwan University, FCAI  ·  May 2026', {
    x: 0.5, y: SH - 0.4, w: 8, h: 0.3,
    fontFace: F.body, fontSize: 9, color: C.muted,
  });
}

// =================================================================== SLIDE 1 — Cover
const TOTAL = 22;
function s1() {
  const s = pres.addSlide(); addBaseDark(s);
  // Subtle accent strip
  s.addShape('rect', { x: 0, y: SH - 0.18, w: SW, h: 0.18, fill: { color: C.accent }, line: { color: C.accent } });
  // Eyebrow
  s.addText('GRADUATION-STYLE PROJECT  ·  KNOWLEDGE-BASED SYSTEMS', {
    x: 0.8, y: 1.1, w: 12, h: 0.4,
    fontFace: F.body, fontSize: 13, color: C.faint, charSpacing: 4,
  });
  // Title
  s.addText('Diab-KBS', {
    x: 0.8, y: 1.7, w: 12, h: 1.2,
    fontFace: F.head, fontSize: 72, bold: true, color: C.white,
  });
  s.addText('A Hybrid Knowledge-Based System for Diabetes Diagnosis,\nRisk Stratification & Clinical Decision Support', {
    x: 0.8, y: 3.0, w: 12, h: 1.2,
    fontFace: F.head, fontSize: 26, color: C.white,
  });
  // Divider
  s.addShape('rect', { x: 0.8, y: 4.4, w: 1.5, h: 0.05, fill: { color: C.accent }, line: { color: C.accent } });
  // Author block
  s.addText('Aya Hesham Ali', {
    x: 0.8, y: 4.7, w: 8, h: 0.5,
    fontFace: F.head, fontSize: 22, bold: true, color: C.white,
  });
  s.addText('Faculty of Computers & Artificial Intelligence  ·  Helwan University', {
    x: 0.8, y: 5.2, w: 12, h: 0.35,
    fontFace: F.body, fontSize: 14, color: C.faint,
  });
  s.addText('Course: Knowledge-Based Systems  ·  Instructor: Dr. Sayed AbdelGaber', {
    x: 0.8, y: 5.55, w: 12, h: 0.35,
    fontFace: F.body, fontSize: 14, color: C.faint,
  });
  s.addText('May 2026', {
    x: 0.8, y: 5.95, w: 12, h: 0.35,
    fontFace: F.body, fontSize: 14, color: C.faint,
  });
}

// =================================================================== SLIDE 2 — Agenda
function s2() {
  const s = pres.addSlide(); addBaseLight(s);
  addHeaderBar(s, 'Agenda', '01  ·  ROADMAP');
  const items = [
    ['01', 'Problem & Motivation'],
    ['02', 'Course-Concept Coverage'],
    ['03', 'CommonKADS — 6 Models'],
    ['04', 'System Architecture'],
    ['05', 'Knowledge Base Design'],
    ['06', 'Inference Engine + Certainty Factors'],
    ['07', 'Knowledge Acquisition Pipeline'],
    ['08', 'Big-Data Analytics'],
    ['09', 'Dashboard Walk-through'],
    ['10', 'Validation Results'],
    ['11', 'Discussion & Future Work'],
    ['12', 'Conclusion  ·  Q & A'],
  ];
  // Two columns of 6
  items.forEach((it, idx) => {
    const col = Math.floor(idx / 6);
    const row = idx % 6;
    const x = 0.8 + col * 6.2;
    const y = 1.7 + row * 0.75;
    s.addText(it[0], {
      x: x, y: y, w: 0.8, h: 0.6,
      fontFace: F.head, fontSize: 28, bold: true, color: C.accent, valign: 'middle',
    });
    s.addText(it[1], {
      x: x + 0.85, y: y, w: 5, h: 0.6,
      fontFace: F.body, fontSize: 16, color: C.dark, valign: 'middle',
    });
  });
  addFooter(s, 2, TOTAL);
}

// =================================================================== SLIDE 3 — Problem
function s3() {
  const s = pres.addSlide(); addBaseLight(s);
  addHeaderBar(s, 'Problem & Motivation', '02  ·  WHY THIS PROJECT');
  // Left: stats
  const stats = [
    ['537 M', 'adults living with diabetes worldwide (IDF Atlas, 2021)'],
    ['10.9 %', 'prevalence among Egyptian adults — among the highest in MENA'],
    ['~ 50 %', 'of cases remain undiagnosed in low-resource settings'],
  ];
  stats.forEach((st, i) => {
    const y = 1.7 + i * 1.55;
    s.addShape('rect', { x: 0.5, y: y, w: 5.8, h: 1.35, fill: { color: C.surface }, line: { color: C.border, width: 1 } });
    s.addText(st[0], {
      x: 0.7, y: y + 0.1, w: 5.4, h: 0.7,
      fontFace: F.head, fontSize: 38, bold: true, color: C.primary,
    });
    s.addText(st[1], {
      x: 0.7, y: y + 0.8, w: 5.4, h: 0.55,
      fontFace: F.body, fontSize: 13, color: C.muted,
    });
  });
  // Right: solution panel
  s.addShape('rect', { x: 6.7, y: 1.7, w: 6.1, h: 4.9, fill: { color: C.dark }, line: { color: C.dark } });
  s.addText('Our Approach', {
    x: 6.95, y: 1.85, w: 5.6, h: 0.5,
    fontFace: F.head, fontSize: 22, bold: true, color: C.white,
  });
  s.addShape('rect', { x: 6.95, y: 2.4, w: 0.7, h: 0.04, fill: { color: C.accent }, line: { color: C.accent } });
  const points = [
    'Hybrid KBS — symbolic (rules + frames + semantic net) plus data-driven rule mining',
    'Built directly on a real Egyptian cohort of 12,204 patients (37 features)',
    'Forward + backward chaining inference with MYCIN certainty factors',
    'Streamlit dashboard exposes all 7 modules — diagnosis, risk, analytics, KB browser, validation',
    'Documents every CommonKADS model — explicit knowledge engineering, not a black box',
  ];
  points.forEach((p, i) => {
    s.addShape('ellipse', { x: 6.95, y: 2.7 + i * 0.78 + 0.12, w: 0.14, h: 0.14, fill: { color: C.accent }, line: { color: C.accent } });
    s.addText(p, {
      x: 7.2, y: 2.65 + i * 0.78, w: 5.4, h: 0.7,
      fontFace: F.body, fontSize: 13, color: C.white,
    });
  });
  addFooter(s, 3, TOTAL);
}

// =================================================================== SLIDE 4 — Coverage matrix
function s4() {
  const s = pres.addSlide(); addBaseLight(s);
  addHeaderBar(s, 'Course-Concept Coverage', '03  ·  EVERY LECTURE → IMPLEMENTATION');
  const rows = [
    ['Lecture', 'Topic', 'Implementation in Diab-KBS'],
    ['1', 'Data → Information → Knowledge → Wisdom', 'DIKW pyramid driving the dashboard pipeline'],
    ['2', 'KBS architecture & components', '3-tier app: KB · inference · UI (Streamlit)'],
    ['3', 'Knowledge representation', '32 production rules · 13 frames · 35-node semantic net'],
    ['4', 'Inference & reasoning', 'Forward + backward chaining + MYCIN CF algebra'],
    ['5', 'Knowledge acquisition', '5-stage pipeline: elicit · structure · validate · refine'],
    ['6', 'CommonKADS methodology', 'All 6 models documented in research paper'],
    ['7', 'Big-Data analytics', 'Apriori rule mining + cohort KPIs on 12,204 records'],
  ];
  // Build table
  const colW = [1.2, 4.3, 6.8];
  const startX = 0.5, startY = 1.55;
  const headH = 0.5;
  // Header
  s.addShape('rect', { x: startX, y: startY, w: 12.3, h: headH, fill: { color: C.primary }, line: { color: C.primary } });
  let cx = startX;
  rows[0].forEach((c, i) => {
    s.addText(c, {
      x: cx + 0.12, y: startY, w: colW[i] - 0.2, h: headH,
      fontFace: F.head, fontSize: 13, bold: true, color: C.white, valign: 'middle',
    });
    cx += colW[i];
  });
  // Body rows
  rows.slice(1).forEach((r, ri) => {
    const y = startY + headH + ri * 0.6;
    if (ri % 2 === 0) {
      s.addShape('rect', { x: startX, y: y, w: 12.3, h: 0.6, fill: { color: C.surface }, line: { color: C.border, width: 0.5 } });
    } else {
      s.addShape('rect', { x: startX, y: y, w: 12.3, h: 0.6, fill: { color: C.bg }, line: { color: C.border, width: 0.5 } });
    }
    let cx2 = startX;
    r.forEach((c, i) => {
      s.addText(c, {
        x: cx2 + 0.12, y: y, w: colW[i] - 0.2, h: 0.6,
        fontFace: F.body, fontSize: 12, color: C.dark, valign: 'middle',
      });
      cx2 += colW[i];
    });
  });
  s.addText('All seven lecture themes are explicitly traceable to a code module or paper section.', {
    x: 0.5, y: 6.7, w: 12.3, h: 0.4,
    fontFace: F.body, fontSize: 12, italic: true, color: C.muted,
  });
  addFooter(s, 4, TOTAL);
}

// =================================================================== SLIDE 5 — DIKW
function s5() {
  const s = pres.addSlide(); addBaseLight(s);
  addHeaderBar(s, 'DIKW — Convergence from Data to Intelligence', '04  ·  LECTURE 1 IN ACTION');
  // Left: pyramid image
  s.addImage({ path: `${ASSETS}/dikw_pyramid.png`, x: 0.5, y: 1.55, w: 6.5, h: 5.2 });
  // Right: per-tier annotations
  const tiers = [
    ['Data',         '12,204 raw records  ·  37 features (HbA1c, BMI, FPG, symptoms…)', C.accent],
    ['Information',  '~120 derived categorical fields (HbA1c_cat, BMI_cat, age band)',  C.success],
    ['Knowledge',    '32 production rules + 13 frames + 35-node semantic network',      C.primary],
    ['Wisdom',       'Patient-specific diagnosis + treatment plan + complication risk', C.error],
  ];
  tiers.forEach((t, i) => {
    const y = 1.7 + i * 1.25;
    s.addShape('rect', { x: 7.4, y: y, w: 0.12, h: 1.05, fill: { color: t[2] }, line: { color: t[2] } });
    s.addText(t[0], {
      x: 7.7, y: y, w: 5.2, h: 0.4,
      fontFace: F.head, fontSize: 18, bold: true, color: t[2],
    });
    s.addText(t[1], {
      x: 7.7, y: y + 0.4, w: 5.2, h: 0.65,
      fontFace: F.body, fontSize: 13, color: C.dark,
    });
  });
  addFooter(s, 5, TOTAL);
}

// =================================================================== SLIDE 6 — CommonKADS
function s6() {
  const s = pres.addSlide(); addBaseLight(s);
  addHeaderBar(s, 'CommonKADS — Six Models', '05  ·  LECTURE 6 IN ACTION');
  s.addImage({ path: `${ASSETS}/commonkads_models.png`, x: 0.6, y: 1.55, w: 7.6, h: 5.2 });
  // Right: short descriptions
  const ms = [
    ['Organisation', 'Helwan teaching-hospital outpatient clinic'],
    ['Task',         'Diagnose · risk-rank · suggest first-line treatment'],
    ['Agent',        'Endocrinologist (current) → KBS-assisted (target)'],
    ['Knowledge',    '32 rules · 13 frames · 35-node semantic net'],
    ['Communication','Web dashboard with explainable derivations'],
    ['Design',       'Python + Streamlit, 3-tier hybrid architecture'],
  ];
  ms.forEach((m, i) => {
    const y = 1.7 + i * 0.85;
    s.addText(m[0], {
      x: 8.5, y: y, w: 4.4, h: 0.35,
      fontFace: F.head, fontSize: 14, bold: true, color: C.primary,
    });
    s.addText(m[1], {
      x: 8.5, y: y + 0.35, w: 4.4, h: 0.45,
      fontFace: F.body, fontSize: 12, color: C.dark,
    });
  });
  addFooter(s, 6, TOTAL);
}

// =================================================================== SLIDE 7 — Architecture
function s7() {
  const s = pres.addSlide(); addBaseLight(s);
  addHeaderBar(s, 'System Architecture', '06  ·  3-TIER + KA PIPELINE');
  s.addImage({ path: `${ASSETS}/architecture.png`, x: 0.5, y: 1.55, w: 12.3, h: 5.0 });
  s.addText('User Interface (Streamlit)  →  Inference Engine (Python)  →  Knowledge Base (JSON)  ·  fed by the 5-stage Knowledge Acquisition pipeline.', {
    x: 0.5, y: 6.7, w: 12.3, h: 0.4,
    fontFace: F.body, fontSize: 12, italic: true, color: C.muted,
  });
  addFooter(s, 7, TOTAL);
}

// =================================================================== SLIDE 8 — Workflow
function s8() {
  const s = pres.addSlide(); addBaseLight(s);
  addHeaderBar(s, 'End-to-End Workflow', '07  ·  EXTRACT → DECIDE');
  s.addImage({ path: `${ASSETS}/workflow.png`, x: 0.5, y: 1.55, w: 12.3, h: 4.4 });
  // 6 stages with KPI
  const stages = [
    ['Extract',   'Excel  →  pandas'],
    ['Clean',     '12,204 rows kept'],
    ['Integrate', '37 features unified'],
    ['Mine',      'Apriori rules (sup ≥ 0.05)'],
    ['Visualise', 'Plotly + NetworkX'],
    ['Decide',    'Diagnosis + treatment'],
  ];
  const stW = 12.3 / 6;
  stages.forEach((st, i) => {
    const x = 0.5 + i * stW;
    s.addText(st[0], {
      x: x, y: 6.05, w: stW, h: 0.3,
      fontFace: F.head, fontSize: 12, bold: true, color: C.primary, align: 'center',
    });
    s.addText(st[1], {
      x: x, y: 6.35, w: stW, h: 0.5,
      fontFace: F.body, fontSize: 11, color: C.muted, align: 'center',
    });
  });
  addFooter(s, 8, TOTAL);
}

// =================================================================== SLIDE 9 — KB Design rules
function s9() {
  const s = pres.addSlide(); addBaseLight(s);
  addHeaderBar(s, 'Knowledge Base — Production Rules', '08  ·  32 RULES, 4 CATEGORIES');
  // Left: category breakdown
  const cats = [
    ['Diagnosis',         8,  C.primary],
    ['Risk Factor',       9,  C.success],
    ['Complication Risk', 7,  C.error],
    ['Treatment',         8,  C.accent],
  ];
  cats.forEach((c, i) => {
    const y = 1.7 + i * 1.0;
    s.addShape('rect', { x: 0.5, y: y, w: 5.8, h: 0.85, fill: { color: C.surface }, line: { color: C.border, width: 0.75 } });
    s.addShape('rect', { x: 0.5, y: y, w: 0.12, h: 0.85, fill: { color: c[2] }, line: { color: c[2] } });
    s.addText(c[0], {
      x: 0.8, y: y + 0.05, w: 4, h: 0.4,
      fontFace: F.head, fontSize: 16, bold: true, color: C.dark,
    });
    s.addText(`${c[1]} rules`, {
      x: 0.8, y: y + 0.45, w: 4, h: 0.35,
      fontFace: F.body, fontSize: 12, color: C.muted,
    });
    s.addText(String(c[1]), {
      x: 5.0, y: y, w: 1.2, h: 0.85,
      fontFace: F.head, fontSize: 30, bold: true, color: c[2], align: 'right', valign: 'middle',
    });
  });
  // Right: example rule card
  s.addShape('rect', { x: 6.6, y: 1.7, w: 6.3, h: 5.0, fill: { color: C.dark }, line: { color: C.dark } });
  s.addText('Example  ·  Rule R17', {
    x: 6.85, y: 1.85, w: 6, h: 0.4,
    fontFace: F.head, fontSize: 14, bold: true, color: C.faint, charSpacing: 2,
  });
  s.addText('IF', {
    x: 6.85, y: 2.4, w: 0.6, h: 0.4,
    fontFace: F.head, fontSize: 18, bold: true, color: C.accent,
  });
  s.addText('diagnosis = "Type 2 Diabetes Mellitus"\nAND   7.5 ≤ HbA1c < 9.0', {
    x: 7.5, y: 2.35, w: 5.3, h: 0.9,
    fontFace: F.body, fontSize: 14, color: C.white,
  });
  s.addText('THEN', {
    x: 6.85, y: 3.6, w: 0.9, h: 0.4,
    fontFace: F.head, fontSize: 18, bold: true, color: C.accent,
  });
  s.addText('recommended_treatment =\n   Dual therapy: Metformin\n   + (SGLT2-i / GLP-1 RA / DPP4-i)', {
    x: 7.85, y: 3.55, w: 5.0, h: 1.4,
    fontFace: F.body, fontSize: 14, color: C.white,
  });
  s.addText('CF = 0.85   ·   Lecture-3 reference: rule chaining w/ certainty factors', {
    x: 6.85, y: 6.05, w: 6, h: 0.5,
    fontFace: F.body, fontSize: 12, italic: true, color: C.faint,
  });
  addFooter(s, 9, TOTAL);
}

// =================================================================== SLIDE 10 — Frames + semantic
function s10() {
  const s = pres.addSlide(); addBaseLight(s);
  addHeaderBar(s, 'Frames & Semantic Network', '09  ·  STRUCTURED REPRESENTATION');
  // Frames panel
  s.addShape('rect', { x: 0.5, y: 1.6, w: 6.1, h: 5.1, fill: { color: C.surface }, line: { color: C.border, width: 0.75 } });
  s.addText('Frames — 13 total', {
    x: 0.7, y: 1.7, w: 5.6, h: 0.4,
    fontFace: F.head, fontSize: 18, bold: true, color: C.primary,
  });
  s.addText('Hierarchical inheritance modelling the diabetes domain.', {
    x: 0.7, y: 2.05, w: 5.6, h: 0.4,
    fontFace: F.body, fontSize: 12, color: C.muted,
  });
  const frameRows = [
    ['MedicalEntity',   '— root',         '2 slots'],
    ['Person',          'is_a Medical…',  '4 slots'],
    ['Patient',         'is_a Person',    '9 slots'],
    ['Disease',         'is_a Medical…',  '4 slots'],
    ['DiabetesMellitus','is_a Disease',   '4 slots'],
    ['Type1Diabetes',   'is_a Diabetes…', '5 slots'],
    ['Type2Diabetes',   'is_a Diabetes…', '5 slots'],
    ['LADA',            'is_a Diabetes…', '3 slots'],
    ['Symptom',         'is_a Medical…',  '3 slots'],
    ['LabResult',       'is_a Medical…',  '6 slots'],
  ];
  frameRows.forEach((r, i) => {
    const y = 2.55 + i * 0.4;
    s.addText(r[0], { x: 0.7, y: y, w: 2.4, h: 0.35, fontFace: F.body, fontSize: 11, bold: true, color: C.dark });
    s.addText(r[1], { x: 3.1, y: y, w: 2.0, h: 0.35, fontFace: F.body, fontSize: 11, color: C.muted });
    s.addText(r[2], { x: 5.1, y: y, w: 1.4, h: 0.35, fontFace: F.body, fontSize: 11, color: C.accent, align: 'right' });
  });
  // Semantic panel
  s.addShape('rect', { x: 6.85, y: 1.6, w: 6.0, h: 5.1, fill: { color: C.surface }, line: { color: C.border, width: 0.75 } });
  s.addText('Semantic Network — 35 nodes  ·  35 edges', {
    x: 7.05, y: 1.7, w: 5.6, h: 0.4,
    fontFace: F.head, fontSize: 18, bold: true, color: C.primary,
  });
  s.addText('Edge types relate diseases, symptoms, labs and treatments.', {
    x: 7.05, y: 2.05, w: 5.6, h: 0.4,
    fontFace: F.body, fontSize: 12, color: C.muted,
  });
  const edges = ['is_a', 'part_of', 'has_symptom', 'causes', 'treated_by', 'indicates', 'increases_risk_of'];
  edges.forEach((e, i) => {
    const col = i % 2;
    const row = Math.floor(i / 2);
    s.addShape('roundRect', {
      x: 7.05 + col * 2.85, y: 2.65 + row * 0.55, w: 2.7, h: 0.45,
      fill: { color: C.bg }, line: { color: C.primary, width: 1 },
      rectRadius: 0.08,
    });
    s.addText(e, {
      x: 7.05 + col * 2.85, y: 2.65 + row * 0.55, w: 2.7, h: 0.45,
      fontFace: F.body, fontSize: 12, color: C.primary, align: 'center', valign: 'middle',
    });
  });
  s.addText('Rendered interactively with NetworkX + Plotly\nin the dashboard\'s "Knowledge Base Browser" page.', {
    x: 7.05, y: 5.6, w: 5.6, h: 0.9,
    fontFace: F.body, fontSize: 12, italic: true, color: C.muted,
  });
  addFooter(s, 10, TOTAL);
}

// =================================================================== SLIDE 11 — Inference
function s11() {
  const s = pres.addSlide(); addBaseLight(s);
  addHeaderBar(s, 'Inference Engine', '10  ·  FORWARD + BACKWARD CHAINING');
  s.addImage({ path: `${ASSETS}/inference_flow.png`, x: 0.5, y: 1.55, w: 8.0, h: 5.0 });
  // Right panel
  s.addShape('rect', { x: 8.7, y: 1.55, w: 4.2, h: 5.0, fill: { color: C.dark }, line: { color: C.dark } });
  s.addText('Strategy', {
    x: 8.9, y: 1.7, w: 4, h: 0.4,
    fontFace: F.head, fontSize: 16, bold: true, color: C.faint, charSpacing: 2,
  });
  s.addText('Forward', {
    x: 8.9, y: 2.15, w: 4, h: 0.4,
    fontFace: F.head, fontSize: 18, bold: true, color: C.accent,
  });
  s.addText('Data-driven — from observed labs / symptoms to diagnosis & treatment.', {
    x: 8.9, y: 2.55, w: 4, h: 0.7,
    fontFace: F.body, fontSize: 12, color: C.white,
  });
  s.addText('Backward', {
    x: 8.9, y: 3.4, w: 4, h: 0.4,
    fontFace: F.head, fontSize: 18, bold: true, color: C.accent,
  });
  s.addText('Goal-driven — verify a hypothesised diagnosis by checking required premises.', {
    x: 8.9, y: 3.8, w: 4, h: 0.9,
    fontFace: F.body, fontSize: 12, color: C.white,
  });
  s.addText('Conflict resolution: highest-CF rule fires first;\nworking memory keys multi-valued slots as slot::value.', {
    x: 8.9, y: 4.85, w: 4, h: 1.2,
    fontFace: F.body, fontSize: 11, italic: true, color: C.faint,
  });
  addFooter(s, 11, TOTAL);
}

// =================================================================== SLIDE 12 — Certainty Factors
function s12() {
  const s = pres.addSlide(); addBaseLight(s);
  addHeaderBar(s, 'Certainty Factors  (MYCIN Algebra)', '11  ·  REASONING UNDER UNCERTAINTY');
  // Left: formula card
  s.addShape('rect', { x: 0.5, y: 1.65, w: 7.8, h: 5.0, fill: { color: C.surface }, line: { color: C.border, width: 0.75 } });
  s.addText('Combining evidence', {
    x: 0.7, y: 1.8, w: 7.4, h: 0.4,
    fontFace: F.head, fontSize: 18, bold: true, color: C.primary,
  });
  // Same sign
  s.addText('Same-sign:', {
    x: 0.7, y: 2.3, w: 7.4, h: 0.35,
    fontFace: F.head, fontSize: 13, bold: true, color: C.dark,
  });
  s.addText('CF(combined) = CF₁ + CF₂ · (1 − CF₁)', {
    x: 0.7, y: 2.65, w: 7.4, h: 0.5,
    fontFace: F.body, fontSize: 18, color: C.accent,
  });
  // Opposite sign
  s.addText('Opposite-sign:', {
    x: 0.7, y: 3.3, w: 7.4, h: 0.35,
    fontFace: F.head, fontSize: 13, bold: true, color: C.dark,
  });
  s.addText('CF(combined) = (CF₁ + CF₂) / (1 − min(|CF₁|,|CF₂|))', {
    x: 0.7, y: 3.65, w: 7.4, h: 0.5,
    fontFace: F.body, fontSize: 18, color: C.accent,
  });
  // Rule firing
  s.addText('When a rule fires:', {
    x: 0.7, y: 4.3, w: 7.4, h: 0.35,
    fontFace: F.head, fontSize: 13, bold: true, color: C.dark,
  });
  s.addText('CF(conclusion) = CF(rule) · max(0, CF(premise))', {
    x: 0.7, y: 4.65, w: 7.4, h: 0.5,
    fontFace: F.body, fontSize: 18, color: C.accent,
  });
  s.addText('Threshold for accepted conclusion in dashboard: |CF| ≥ 0.50', {
    x: 0.7, y: 5.5, w: 7.4, h: 0.4,
    fontFace: F.body, fontSize: 12, italic: true, color: C.muted,
  });
  s.addText('All rule CFs are stored in knowledge_base/rules.json — calibrated against ADA & WHO guidelines.', {
    x: 0.7, y: 5.85, w: 7.4, h: 0.7,
    fontFace: F.body, fontSize: 12, color: C.muted,
  });
  // Right: numeric example
  s.addShape('rect', { x: 8.5, y: 1.65, w: 4.4, h: 5.0, fill: { color: C.dark }, line: { color: C.dark } });
  s.addText('Worked Example', {
    x: 8.7, y: 1.8, w: 4, h: 0.4,
    fontFace: F.head, fontSize: 14, bold: true, color: C.faint, charSpacing: 2,
  });
  const ex = [
    ['R02', 'FPG_cat = "diabetes"',         'CF₁ = 0.92'],
    ['R01', 'HbA1c_cat = "diabetes"',       'CF₂ = 0.95'],
    ['Combined', 'same-sign rule',          'CF = 0.996'],
    ['Diagnosis', 'Type 2 Diabetes',        'accepted'],
  ];
  ex.forEach((row, i) => {
    const y = 2.35 + i * 0.95;
    s.addText(row[0], { x: 8.7, y: y, w: 4, h: 0.3, fontFace: F.head, fontSize: 14, bold: true, color: C.accent });
    s.addText(row[1], { x: 8.7, y: y + 0.3, w: 4, h: 0.3, fontFace: F.body, fontSize: 12, color: C.white });
    s.addText(row[2], { x: 8.7, y: y + 0.6, w: 4, h: 0.3, fontFace: F.body, fontSize: 12, color: C.faint });
  });
  addFooter(s, 12, TOTAL);
}

// =================================================================== SLIDE 13 — KA pipeline
function s13() {
  const s = pres.addSlide(); addBaseLight(s);
  addHeaderBar(s, 'Knowledge Acquisition Pipeline', '12  ·  LECTURE 5 IN ACTION');
  s.addImage({ path: `${ASSETS}/ka_flow.png`, x: 0.5, y: 1.55, w: 12.3, h: 4.4 });
  const stages = [
    ['1. Elicit',   'Domain literature, ADA/WHO guidelines, Egyptian protocols'],
    ['2. Structure','Encode as rules · frames · semantic edges'],
    ['3. Mine',     'Apriori on 12,204 patients (sup ≥ 0.05, conf ≥ 0.70)'],
    ['4. Validate', 'Run forward chaining on 4,893-patient hold-out'],
    ['5. Refine',   'Adjust CFs · merge mined rules · iterate'],
  ];
  stages.forEach((st, i) => {
    const x = 0.5 + i * 2.46;
    s.addText(st[0], {
      x: x, y: 6.1, w: 2.46, h: 0.35,
      fontFace: F.head, fontSize: 12, bold: true, color: C.primary, align: 'center',
    });
    s.addText(st[1], {
      x: x, y: 6.45, w: 2.46, h: 0.55,
      fontFace: F.body, fontSize: 10, color: C.muted, align: 'center',
    });
  });
  addFooter(s, 13, TOTAL);
}

// =================================================================== SLIDE 14 — Big-Data
function s14() {
  const s = pres.addSlide(); addBaseLight(s);
  addHeaderBar(s, 'Big-Data Analytics on the Cohort', '13  ·  LECTURE 7 IN ACTION');
  // Stats grid 4 across
  const kpis = [
    ['12,204', 'Patients in DB',      C.primary],
    ['4,207',  'Confirmed T2DM (34.5 %)', C.accent],
    ['3,217',  'Hypertensive (26.4 %)',  C.success],
    ['4,874',  'Obese (39.9 %)',         C.error],
  ];
  kpis.forEach((k, i) => {
    const x = 0.5 + i * 3.2;
    s.addShape('rect', { x: x, y: 1.65, w: 3.0, h: 1.55, fill: { color: C.surface }, line: { color: C.border, width: 0.75 } });
    s.addText(k[0], {
      x: x + 0.15, y: 1.75, w: 2.7, h: 0.85,
      fontFace: F.head, fontSize: 36, bold: true, color: k[2], valign: 'middle',
    });
    s.addText(k[1], {
      x: x + 0.15, y: 2.65, w: 2.7, h: 0.5,
      fontFace: F.body, fontSize: 12, color: C.muted,
    });
  });
  // Mined rules panel
  s.addShape('rect', { x: 0.5, y: 3.45, w: 12.3, h: 3.2, fill: { color: C.dark }, line: { color: C.dark } });
  s.addText('Top mined association rules — Apriori on cleaned cohort', {
    x: 0.7, y: 3.55, w: 12, h: 0.4,
    fontFace: F.head, fontSize: 16, bold: true, color: C.faint, charSpacing: 2,
  });
  const minedHead = ['LHS', 'RHS', 'Support', 'Confidence', 'Lift'];
  const mined = [
    ['HbA1c_cat = diabetes',                  'diagnosis = T2DM',    '0.34', '0.95', '2.74'],
    ['BMI_cat = obese & age ≥ 45',            'diagnosis = T2DM',    '0.18', '0.78', '2.26'],
    ['HTN = 1 & diagnosis = T2DM',            'complication = CV',   '0.12', '0.71', '1.84'],
    ['HbA1c ≥ 9 & diagnosis = T2DM',          'complication = high', '0.09', '0.83', '2.15'],
  ];
  const cwIn = [3.6, 3.0, 1.8, 2.0, 1.5];
  let cxIn = 0.7;
  minedHead.forEach((h, i) => {
    s.addText(h, { x: cxIn, y: 4.05, w: cwIn[i], h: 0.4, fontFace: F.head, fontSize: 12, bold: true, color: C.accent });
    cxIn += cwIn[i];
  });
  mined.forEach((row, ri) => {
    let cxIn2 = 0.7;
    row.forEach((cell, i) => {
      s.addText(cell, { x: cxIn2, y: 4.5 + ri * 0.5, w: cwIn[i], h: 0.4, fontFace: F.body, fontSize: 11, color: C.white });
      cxIn2 += cwIn[i];
    });
  });
  addFooter(s, 14, TOTAL);
}

// =================================================================== SLIDE 15 — Dashboard tour 1
function s15() {
  const s = pres.addSlide(); addBaseLight(s);
  addHeaderBar(s, 'Dashboard — Overview Page', '14  ·  STREAMLIT FRONT-END');
  s.addImage({ path: `${ASSETS}/screens/dashboard_overview.png`, x: 0.5, y: 1.55, w: 9.5, h: 5.0 });
  // Right callouts
  s.addShape('rect', { x: 10.2, y: 1.55, w: 2.7, h: 5.0, fill: { color: C.surface }, line: { color: C.border, width: 0.75 } });
  s.addText('Modules', {
    x: 10.35, y: 1.65, w: 2.45, h: 0.4,
    fontFace: F.head, fontSize: 14, bold: true, color: C.primary,
  });
  ['Overview', 'Patient Diagnosis', 'Risk Stratification', 'Big-Data Analytics', 'Visualisation Gallery', 'KB Browser', 'Validation'].forEach((m, i) => {
    s.addShape('ellipse', { x: 10.35, y: 2.15 + i * 0.55 + 0.1, w: 0.12, h: 0.12, fill: { color: C.accent }, line: { color: C.accent } });
    s.addText(m, {
      x: 10.55, y: 2.1 + i * 0.55, w: 2.3, h: 0.5,
      fontFace: F.body, fontSize: 12, color: C.dark,
    });
  });
  addFooter(s, 15, TOTAL);
}

// =================================================================== SLIDE 16 — Validation
function s16() {
  const s = pres.addSlide(); addBaseLight(s);
  addHeaderBar(s, 'Validation Results', '15  ·  N = 4,893 PATIENTS');
  // KPI cards (5 cards across 12.3in: card 2.3 + gap 0.2)
  const ks = [
    ['81.4 %', 'Accuracy',    C.primary],
    ['78.2 %', 'Sensitivity', C.accent],
    ['87.2 %', 'Specificity', C.success],
    ['91.7 %', 'Precision',   C.error],
    ['0.844',  'F1 Score',    C.dark],
  ];
  const kpiW = 2.3, kpiGap = (12.3 - 5 * kpiW) / 4;
  ks.forEach((k, i) => {
    const x = 0.5 + i * (kpiW + kpiGap);
    s.addShape('rect', { x: x, y: 1.65, w: kpiW, h: 1.55, fill: { color: C.surface }, line: { color: C.border, width: 0.75 } });
    s.addText(k[0], {
      x: x + 0.15, y: 1.75, w: kpiW - 0.3, h: 0.85,
      fontFace: F.head, fontSize: 28, bold: true, color: k[2], valign: 'middle',
    });
    s.addText(k[1], {
      x: x + 0.15, y: 2.65, w: kpiW - 0.3, h: 0.5,
      fontFace: F.body, fontSize: 12, color: C.muted,
    });
  });
  // Confusion matrix
  s.addText('Confusion matrix', {
    x: 0.5, y: 3.55, w: 6, h: 0.4,
    fontFace: F.head, fontSize: 16, bold: true, color: C.primary,
  });
  const cmHead = ['', 'Predicted Diabetic', 'Predicted Healthy'];
  const cmRows = [
    ['Actual Diabetic',  ['TP = 2,467', C.success], ['FN = 688',  C.error]],
    ['Actual Healthy',   ['FP = 223',   C.error],   ['TN = 1,515', C.success]],
  ];
  const cmX = 0.5, cmY = 4.0, cmW = [3.2, 2.6, 2.6];
  // header
  let cxC = cmX;
  cmHead.forEach((h, i) => {
    s.addShape('rect', { x: cxC, y: cmY, w: cmW[i], h: 0.5, fill: { color: C.primary }, line: { color: C.primary } });
    s.addText(h, { x: cxC + 0.1, y: cmY, w: cmW[i] - 0.2, h: 0.5, fontFace: F.head, fontSize: 13, bold: true, color: C.white, valign: 'middle', align: i === 0 ? 'left' : 'center' });
    cxC += cmW[i];
  });
  cmRows.forEach((r, ri) => {
    let cxC2 = cmX;
    s.addShape('rect', { x: cmX, y: cmY + 0.5 + ri * 0.7, w: cmW[0], h: 0.7, fill: { color: C.surface }, line: { color: C.border, width: 0.5 } });
    s.addText(r[0], { x: cmX + 0.1, y: cmY + 0.5 + ri * 0.7, w: cmW[0] - 0.2, h: 0.7, fontFace: F.head, fontSize: 13, bold: true, color: C.dark, valign: 'middle' });
    cxC2 += cmW[0];
    [1, 2].forEach((idx) => {
      s.addShape('rect', { x: cxC2, y: cmY + 0.5 + ri * 0.7, w: cmW[idx], h: 0.7, fill: { color: C.bg }, line: { color: C.border, width: 0.5 } });
      s.addText(r[idx][0], { x: cxC2, y: cmY + 0.5 + ri * 0.7, w: cmW[idx], h: 0.7, fontFace: F.head, fontSize: 14, bold: true, color: r[idx][1], align: 'center', valign: 'middle' });
      cxC2 += cmW[idx];
    });
  });
  // Right: notes
  s.addShape('rect', { x: 9.3, y: 3.55, w: 3.6, h: 3.0, fill: { color: C.dark }, line: { color: C.dark } });
  s.addText('Reading the numbers', {
    x: 9.5, y: 3.7, w: 3.3, h: 0.4,
    fontFace: F.head, fontSize: 14, bold: true, color: C.faint, charSpacing: 2,
  });
  const notes = [
    '91.7 % precision: when the KBS predicts diabetes, it is correct ~9 times out of 10.',
    '78.2 % sensitivity: 22 % of cases missed — next iteration adds prediabetes rules.',
    'Specificity 87.2 % keeps the false-alarm rate manageable for clinic workflow.',
  ];
  notes.forEach((n, i) => {
    s.addShape('ellipse', { x: 9.5, y: 4.15 + i * 0.78 + 0.08, w: 0.12, h: 0.12, fill: { color: C.accent }, line: { color: C.accent } });
    s.addText(n, {
      x: 9.7, y: 4.05 + i * 0.78, w: 3.1, h: 0.75,
      fontFace: F.body, fontSize: 11, color: C.white,
    });
  });
  addFooter(s, 16, TOTAL);
}

// =================================================================== SLIDE 17 — Implementation stack
function s17() {
  const s = pres.addSlide(); addBaseLight(s);
  addHeaderBar(s, 'Implementation Stack', '16  ·  PYTHON · STREAMLIT · JSON');
  const tech = [
    ['Front-end',     'Streamlit  ·  Plotly  ·  NetworkX'],
    ['Inference',     'Custom Python engine  ·  MYCIN CF algebra'],
    ['Knowledge Base','JSON  ·  rules · frames · semantic_net · mined_rules'],
    ['Data layer',    'pandas  ·  numpy  ·  CSV / Excel'],
    ['Mining',        'mlxtend Apriori  ·  scikit-learn metrics'],
    ['Visuals',       'matplotlib  ·  Plotly Express  ·  PIL'],
    ['Reports',       'ReportLab  ·  python-pptx / pptxgenjs'],
  ];
  tech.forEach((t, i) => {
    const col = i % 2;
    const row = Math.floor(i / 2);
    const x = 0.5 + col * 6.4;
    const y = 1.7 + row * 0.8;
    s.addShape('rect', { x: x, y: y, w: 6.0, h: 0.7, fill: { color: C.surface }, line: { color: C.border, width: 0.75 } });
    s.addText(t[0], {
      x: x + 0.2, y: y, w: 1.8, h: 0.7,
      fontFace: F.head, fontSize: 13, bold: true, color: C.primary, valign: 'middle',
    });
    s.addText(t[1], {
      x: x + 2.05, y: y, w: 3.85, h: 0.7,
      fontFace: F.body, fontSize: 12, color: C.dark, valign: 'middle',
    });
  });
  // Repo layout
  s.addShape('rect', { x: 0.5, y: 5.2, w: 12.3, h: 1.5, fill: { color: C.dark }, line: { color: C.dark } });
  s.addText('Repository layout', {
    x: 0.7, y: 5.3, w: 12, h: 0.35,
    fontFace: F.head, fontSize: 12, bold: true, color: C.faint, charSpacing: 2,
  });
  s.addText([
    { text: 'Diab-KBS/',                                                            options: { breakLine: true } },
    { text: '  ├── app.py                  Streamlit dashboard (7 pages)',          options: { breakLine: true } },
    { text: '  ├── kbs/                    inference engine + certainty factors', options: { breakLine: true } },
    { text: '  ├── knowledge_base/         rules · frames · semantic_net · mined_rules (.json)', options: { breakLine: true } },
    { text: '  ├── data/                   patients_clean.csv · kpis.json · validation_results.json', options: { breakLine: true } },
    { text: '  ├── notebooks/              preprocess · mine · validate · diagrams · paper · deck', options: { breakLine: true } },
    { text: '  └── docs/                   Research_Paper.pdf · Defense.pptx · assets/*.png' },
  ], {
    x: 0.7, y: 5.65, w: 12, h: 1.0,
    fontFace: 'Courier New', fontSize: 10, color: C.white,
  });
  addFooter(s, 17, TOTAL);
}

// =================================================================== SLIDE 18 — Discussion
function s18() {
  const s = pres.addSlide(); addBaseLight(s);
  addHeaderBar(s, 'Discussion — Strengths & Limits', '17  ·  HONEST APPRAISAL');
  // Strengths
  s.addShape('rect', { x: 0.5, y: 1.65, w: 6.1, h: 5.0, fill: { color: C.surface }, line: { color: C.border, width: 0.75 } });
  s.addText('Strengths', {
    x: 0.7, y: 1.8, w: 5.6, h: 0.4,
    fontFace: F.head, fontSize: 18, bold: true, color: C.success,
  });
  const strengths = [
    'Every decision is explainable — full rule chain visible to the clinician',
    'Knowledge cleanly separated from inference — KB editable as JSON',
    'Hybrid: hand-curated rules + data-mined rules complement each other',
    'Real Egyptian cohort grounds the system in local epidemiology',
    'CommonKADS coverage demonstrates rigorous knowledge engineering',
  ];
  strengths.forEach((p, i) => {
    s.addShape('ellipse', { x: 0.85, y: 2.4 + i * 0.65 + 0.12, w: 0.14, h: 0.14, fill: { color: C.success }, line: { color: C.success } });
    s.addText(p, { x: 1.1, y: 2.35 + i * 0.65, w: 5.3, h: 0.6, fontFace: F.body, fontSize: 12, color: C.dark });
  });
  // Limits
  s.addShape('rect', { x: 6.85, y: 1.65, w: 6.0, h: 5.0, fill: { color: C.surface }, line: { color: C.border, width: 0.75 } });
  s.addText('Limits & Future Work', {
    x: 7.05, y: 1.8, w: 5.6, h: 0.4,
    fontFace: F.head, fontSize: 18, bold: true, color: C.error,
  });
  const limits = [
    'Sensitivity 78 % — currently misses borderline / prediabetes cases',
    'Static rule base — no online learning from new patients yet',
    'Single-cohort validation — needs prospective multi-site study',
    'No NLP yet — clinician notes ingested only as structured fields',
    'Future: integrate ontology (SNOMED-CT) and federated learning',
  ];
  limits.forEach((p, i) => {
    s.addShape('ellipse', { x: 7.2, y: 2.4 + i * 0.65 + 0.12, w: 0.14, h: 0.14, fill: { color: C.error }, line: { color: C.error } });
    s.addText(p, { x: 7.45, y: 2.35 + i * 0.65, w: 5.3, h: 0.6, fontFace: F.body, fontSize: 12, color: C.dark });
  });
  addFooter(s, 18, TOTAL);
}

// =================================================================== SLIDE 19 — Conclusion
function s19() {
  const s = pres.addSlide(); addBaseDark(s);
  s.addShape('rect', { x: 0, y: 0, w: SW, h: 0.55, fill: { color: C.primary }, line: { color: C.primary } });
  s.addText('Diab-KBS  ·  Diabetes Knowledge-Based System', {
    x: 0.5, y: 0, w: 8, h: 0.55, fontFace: F.body, fontSize: 11, color: C.white, valign: 'middle',
  });
  s.addText('18  ·  TAKEAWAYS', {
    x: SW - 4.5, y: 0, w: 4, h: 0.55, fontFace: F.body, fontSize: 11, color: C.white, align: 'right', valign: 'middle',
  });
  s.addText('Conclusion', {
    x: 0.8, y: 1.2, w: 12, h: 1.0,
    fontFace: F.head, fontSize: 56, bold: true, color: C.white,
  });
  s.addShape('rect', { x: 0.8, y: 2.3, w: 1.5, h: 0.05, fill: { color: C.accent }, line: { color: C.accent } });
  const lines = [
    'Diab-KBS demonstrates the full course material — DIKW, KR, inference, KA, CommonKADS, big-data analytics — on a real 12,204-patient cohort.',
    'Forward + backward chaining with MYCIN certainty factors deliver explainable, calibrated diagnoses (Accuracy 81.4 %, F1 0.844).',
    'A Streamlit dashboard surfaces the entire knowledge base for clinicians, students, and examiners.',
    'The architecture is reusable for any guideline-driven medical KBS — swap the knowledge base, keep the engine.',
  ];
  lines.forEach((l, i) => {
    // Anchor each circle to a fixed top offset so they stay perfectly aligned even when text wraps
    const y = 2.95 + i * 0.95;
    s.addShape('ellipse', { x: 0.8, y: y + 0.08, w: 0.16, h: 0.16, fill: { color: C.accent }, line: { color: C.accent } });
    s.addText(l, {
      x: 1.1, y: y - 0.05, w: 11.55, h: 0.85,
      fontFace: F.body, fontSize: 16, color: C.white, valign: 'top',
    });
  });
  addFooter(s, 19, TOTAL);
}

// =================================================================== SLIDE 20 — Repository
function s20() {
  const s = pres.addSlide(); addBaseLight(s);
  addHeaderBar(s, 'Deliverables', '19  ·  WHAT YOU RECEIVE');
  const items = [
    ['Source code',          'Diab-KBS/  ·  app.py + kbs/ + notebooks/'],
    ['Knowledge base',       'rules.json · frames.json · semantic_net.json · mined_rules.json'],
    ['Cleaned dataset',      'data/patients_clean.csv  ·  12,204 × 37'],
    ['Research paper',       'docs/Research_Paper.pdf  ·  25 pages, 6 figures, 12 references'],
    ['Defense deck',         'docs/Defense.pptx  ·  this presentation'],
    ['Dashboard',            'Streamlit app — 7 interactive pages'],
    ['Diagrams',             'assets/*.png  ·  6 publication-ready figures'],
  ];
  items.forEach((it, i) => {
    const y = 1.7 + i * 0.7;
    s.addShape('rect', { x: 0.5, y: y, w: 12.3, h: 0.6, fill: { color: C.surface }, line: { color: C.border, width: 0.5 } });
    s.addShape('rect', { x: 0.5, y: y, w: 0.12, h: 0.6, fill: { color: C.primary }, line: { color: C.primary } });
    s.addText(it[0], { x: 0.75, y: y, w: 3.2, h: 0.6, fontFace: F.head, fontSize: 14, bold: true, color: C.dark, valign: 'middle' });
    s.addText(it[1], { x: 4.0, y: y, w: 8.6, h: 0.6, fontFace: F.body, fontSize: 12, color: C.muted, valign: 'middle' });
  });
  addFooter(s, 20, TOTAL);
}

// =================================================================== SLIDE 21 — References
function s21() {
  const s = pres.addSlide(); addBaseLight(s);
  addHeaderBar(s, 'Selected References', '20  ·  KEY SOURCES');
  const refs = [
    'Shortliffe, E. H. (1976). Computer-Based Medical Consultations: MYCIN. Elsevier.',
    'Buchanan, B. G., & Shortliffe, E. H. (1984). Rule-Based Expert Systems. Addison-Wesley.',
    'Schreiber, G. et al. (2000). Knowledge Engineering and Management — The CommonKADS Methodology. MIT Press.',
    'Studer, R., Benjamins, V. R., & Fensel, D. (1998). Knowledge engineering: principles and methods. Data & Knowledge Engineering, 25(1–2), 161–197.',
    'Russell, S., & Norvig, P. (2020). Artificial Intelligence: A Modern Approach (4th ed.), Chs 8–9. Pearson.',
    'American Diabetes Association (2024). Standards of Medical Care in Diabetes. Diabetes Care 47(Suppl 1).',
    'World Health Organization (2019). Classification of diabetes mellitus.',
    'El-Sappagh, S. et al. (2018). Ontology + rule clinical DSS for diabetes. J Biomed Inform 84:124–138.',
    'International Diabetes Federation (2021). IDF Diabetes Atlas, 10th edition.',
    'Newell, A. (1982). The knowledge level. Artificial Intelligence, 18(1), 87–127.',
  ];
  refs.forEach((r, i) => {
    s.addText(`[${i + 1}]  ${r}`, {
      x: 0.5, y: 1.6 + i * 0.48, w: 12.3, h: 0.45,
      fontFace: F.body, fontSize: 11, color: C.dark,
    });
  });
  addFooter(s, 21, TOTAL);
}

// =================================================================== SLIDE 22 — Q&A
function s22() {
  const s = pres.addSlide(); addBaseDark(s);
  s.addShape('rect', { x: 0, y: SH - 0.18, w: SW, h: 0.18, fill: { color: C.accent }, line: { color: C.accent } });
  s.addText('Thank you', {
    x: 0.8, y: 2.2, w: 12, h: 1.4,
    fontFace: F.head, fontSize: 88, bold: true, color: C.white,
  });
  s.addText('Questions & Discussion', {
    x: 0.8, y: 3.7, w: 12, h: 0.7,
    fontFace: F.head, fontSize: 28, color: C.faint,
  });
  s.addShape('rect', { x: 0.8, y: 4.55, w: 1.5, h: 0.05, fill: { color: C.accent }, line: { color: C.accent } });
  s.addText('Aya Hesham Ali  ·  Faculty of Computers & AI, Helwan University', {
    x: 0.8, y: 4.85, w: 12, h: 0.4,
    fontFace: F.body, fontSize: 16, color: C.white,
  });
  s.addText('Course: Knowledge-Based Systems  ·  Instructor: Dr. Sayed AbdelGaber', {
    x: 0.8, y: 5.25, w: 12, h: 0.4,
    fontFace: F.body, fontSize: 14, color: C.faint,
  });
  s.addText('aya.hesham.ali.pbis2026@commerce.helwan.edu.eg', {
    x: 0.8, y: 5.7, w: 12, h: 0.4,
    fontFace: F.body, fontSize: 14, color: C.faint,
  });
}

// =================================================================== build
[s1, s2, s3, s4, s5, s6, s7, s8, s9, s10, s11, s12, s13, s14, s15, s16, s17, s18, s19, s20, s21, s22].forEach(fn => fn());

const out = '/home/user/workspace/Diab-KBS/docs/Defense.pptx';
pres.writeFile({ fileName: out }).then(p => {
  console.log('PPTX saved ->', p);
});
