"""Assemble Max's full-report version (HIT140 A3, Darwin Group 27).
Stephen's and Quentin's sections are copied verbatim (run text + bold/italic) from their own .docx files;
only formatting is unified. The single content change is author attribution in Quentin's section
("Max" -> "Quentin" for authorship of 2.2; A2 references -> "the group's Assessment 2")."""
import copy, re
from pathlib import Path
import pandas as pd
import docx
from docx import Document
from docx.shared import Pt, Cm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.section import WD_SECTION
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

A3 = Path(__file__).resolve().parents[1]
_first = lambda c: next((p for p in c if p.exists()), c[-1])
STEPHEN = _first([A3.parent / "Assessment 3 dataset and python codes (stephen Kenyi)" / "Linear regression Report.docx",
                  Path("/workspace/hit140/stephen/Linear regression Report.docx")])
QUENTIN = _first([A3.parent / "Assessment 3.docx", Path("/workspace/hit140/quentin/q.docx")])
OUTDOCX = A3 / "report" / "HIT140_A3_Group27_Report_MaxVersion.docx"
ASSETS = A3 / "report_assets"
BODY = 10; SMALL = 8
W = qn

def attrib_quentin(t):
    t = t.replace("developed independently by Max", "developed independently by Quentin")
    t = t.replace("Max's assessment 2", "the group's Assessment 2").replace("max's a2", "the group's A2")
    t = t.replace("Max's specific academic lineage", "the group's Assessment 2 lineage")
    t = t.replace("In Assessment 2, Max assessed", "In Assessment 2, the group assessed")
    t = t.replace("Max's Assessment 2 presentation", "the group's Assessment 2 presentation")
    t = t.replace("Max's independent workload", "Quentin's independent workload")
    t = t.replace("(Max)", "(Quentin)")
    assert not re.search(r"Max's|max's|by Max|Max assessed|\(Max\)", t), t
    return t

doc = Document()
sec = doc.sections[0]
sec.page_width, sec.page_height = Cm(21.0), Cm(29.7)
for side in ("left_margin", "right_margin"): setattr(sec, side, Cm(1.3))
sec.top_margin = sec.bottom_margin = Cm(1.2)
st = doc.styles["Normal"]; st.font.name = "Calibri"; st.font.size = Pt(BODY)
st.element.rPr.rFonts.set(qn("w:eastAsia"), "Calibri")
pf = st.paragraph_format; pf.space_before = Pt(0); pf.space_after = Pt(2); pf.line_spacing = 1.0
for lvl, size in ((1, 11.5), (2, 10.5), (3, 10)):
    h = doc.styles[f"Heading {lvl}"]; h.font.name = "Calibri"; h.font.size = Pt(size); h.font.bold = True
    h.font.color.rgb = RGBColor(0x1F, 0x3A, 0x5F) if lvl < 3 else RGBColor(0x33, 0x33, 0x33)
    h.element.rPr.rFonts.set(qn("w:asciiTheme"), "minorHAnsi") if False else None
    rf = h.element.rPr.find(qn("w:rFonts"))
    if rf is not None:
        for a in list(rf.attrib): del rf.attrib[a]
        rf.set(qn("w:ascii"), "Calibri"); rf.set(qn("w:hAnsi"), "Calibri")
    h.paragraph_format.space_before = Pt(5 if lvl == 1 else 3); h.paragraph_format.space_after = Pt(1)
    h.paragraph_format.keep_with_next = True

def para(text="", bold_prefix=None, size=BODY, italic=False, align=None, after=2, style=None):
    p = doc.add_paragraph(style=style)
    if bold_prefix:
        r = p.add_run(bold_prefix); r.bold = True; r.font.size = Pt(size)
    r = p.add_run(text); r.font.size = Pt(size); r.italic = italic
    p.paragraph_format.space_after = Pt(after)
    if align: p.alignment = align
    return p

def rich(parts, size=BODY, after=2):
    """parts: list of (text, bold) tuples."""
    p = doc.add_paragraph()
    for t, b in parts:
        r = p.add_run(t); r.bold = b; r.font.size = Pt(size)
    p.paragraph_format.space_after = Pt(after)
    return p

def copy_para(src_p, transform=lambda t: t, size=BODY, after=2, style=None):
    p = doc.add_paragraph(style=style)
    for item in src_p.iter_inner_content():          # runs and hyperlinks, in order
        runs = item.runs if hasattr(item, "address") else [item]
        for r in runs:
            t = transform(r.text)
            if not t: continue
            nr = p.add_run(t); nr.bold = r.bold; nr.italic = r.italic; nr.font.size = Pt(size)
            if r.font.superscript: nr.font.superscript = True
    p.paragraph_format.space_after = Pt(after)
    return p

def set_cell_margins(table, m=40):
    tblPr = table._tbl.tblPr
    mar = OxmlElement("w:tblCellMar")
    for side in ("top", "bottom", "left", "right"):
        e = OxmlElement(f"w:{side}"); e.set(qn("w:w"), str(m if side in ("left", "right") else 0)); e.set(qn("w:type"), "dxa"); mar.append(e)
    tblPr.append(mar)

def add_table(rows, widths=None, size=SMALL, header=True, transform=lambda t: t):
    t = doc.add_table(rows=len(rows), cols=len(rows[0])); t.style = "Table Grid"
    set_cell_margins(t)
    if widths:
        t.autofit = False
        tblPr = t._tbl.tblPr
        tw = tblPr.find(qn("w:tblW"))
        if tw is None: tw = OxmlElement("w:tblW"); tblPr.append(tw)
        tw.set(qn("w:w"), str(int(sum(widths) * 567))); tw.set(qn("w:type"), "dxa")
        lay = OxmlElement("w:tblLayout"); lay.set(qn("w:type"), "fixed"); tblPr.append(lay)
        grid = t._tbl.tblGrid
        for gc, wcm in zip(grid.findall(qn("w:gridCol")), widths): gc.set(qn("w:w"), str(int(wcm * 567)))
    for i, row in enumerate(rows):
        for j, val in enumerate(row):
            c = t.cell(i, j); c.text = ""
            p = c.paragraphs[0]; r = p.add_run(transform(str(val))); r.font.size = Pt(size)
            r.bold = header and i == 0
            p.paragraph_format.space_after = Pt(0)
            p.paragraph_format.keep_with_next = i < len(rows) - 1   # keep table on one page
            if widths: c.width = Cm(widths[j])
    doc.add_paragraph().paragraph_format.space_after = Pt(0)
    doc.paragraphs[-1].runs or doc.paragraphs[-1].add_run("").font.size
    doc.paragraphs[-1].paragraph_format.line_spacing = Pt(4)
    return t

def picture(path, width_cm, caption=None):
    p = doc.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_after = Pt(0); p.paragraph_format.keep_with_next = True
    p.add_run().add_picture(str(path), width=Cm(width_cm))
    if caption:
        c = para(caption, size=SMALL, italic=True, align=WD_ALIGN_PARAGRAPH.CENTER, after=3)

# ------------------------------------------------------------------ title block
t = para("HIT140 Assessment 3 (Objective 2): Linear Regression Models of FIFA World Cup 2026 Goal Difference and Team Goals",
         size=13, align=WD_ALIGN_PARAGRAPH.CENTER, after=1); t.runs[0].bold = True
para("Darwin Group 27: Robert \u201cMax\u201d Turner (24467305) \u00b7 Junxian \u201cQuentin\u201d Qiu ([ID]) \u00b7 Stephen K Kenyi ([ID])",
     size=BODY, align=WD_ALIGN_PARAGRAPH.CENTER, after=0)
para("Python code and datasets: https://github.com/vfbmdcccxciii/HIT140_Group_Project (see code-link .txt in the submission)",
     size=SMALL, align=WD_ALIGN_PARAGRAPH.CENTER, after=2, italic=True)

# ------------------------------------------------------------------ 1. Data & methods (Max)
doc.add_heading("1. Data and Methods (Max Turner)", level=1)
rich([("Task and design. ", True), ("Model 2.1 predicts goal difference for the 104 matches; Model 2.2 predicts one team\u2019s goals (208 team-match rows). Each uses exactly eight pre-match explanatory variables, with at most four shared. Members built their models independently (Sections 2\u20133); Max compiled a benchmark dataset and a common validation design so every model is compared on equal terms (Section 4).", False)])
rich([("Sources and pre-match features. ", True), ("Scores (72 group, 32 knockout, 9 after extra time; 308 goals) come from the openfootball mirror of FIFA results, cross-checked against eloratings.net (all 208 team scores agree). Max added pre-tournament FIFA rank, Transfermarkt squad value, age and World Cup experience, and each team\u2019s pre-match Elo and goals for/against over its previous 10 internationals (eloratings.net histories, so first matches need no imputation). Rank and value are log-transformed. Max\u2019s 2.1 uses team1\u2212team2 differences; his 2.2 pairs own strength and attack with opponent strength and defence (plus host and knockout), so his two models share 0 variables. FIFA tournament statistics are post-match totals and were not used.", False)])
rich([("Validation. ", True), ("All models are scored with repeated 5-fold cross-validation (5\u00d720, seed 140), with scaling and tuning fitted inside each training fold, reporting held-out R\u00b2, RMSE and MAE against a mean-only baseline. Members\u2019 CSVs are used unchanged (validate_team_models.py).", False)])

# ------------------------------------------------------------------ 2. Stephen (verbatim)
doc.add_heading("2. Linear Regression 2.1: Goal Difference (Stephen K Kenyi)", level=1)
sd = docx.Document(STEPHEN)
for el in sd.element.body.iterchildren():
    if el.tag != qn("w:p"): continue
    p = docx.text.paragraph.Paragraph(el, sd)
    has_img = bool(el.findall(".//" + qn("a:blip")) if False else el.findall('.//{http://schemas.openxmlformats.org/drawingml/2006/main}blip'))
    if has_img:
        picture(ASSETS / "stephen_summary_table_web.jpg", 11.0, "Figure 1. " + p.text.strip())
        continue
    if not p.text.strip(): continue
    copy_para(p)

# ------------------------------------------------------------------ 3. Quentin (verbatim, attribution fixed)
doc.add_heading("3. Linear Regression 2.2: Match-Level Team Goals (Junxian \u201cQuentin\u201d Qiu)", level=1)
qd = docx.Document(QUENTIN)
q_refs, q_appendix, mode = [], [], "body"
for el in qd.element.body.iterchildren():
    tag = el.tag.split("}")[1]
    if tag == "p":
        p = docx.text.paragraph.Paragraph(el, qd); txt = p.text.strip()
        has_img = bool(el.findall('.//{http://schemas.openxmlformats.org/drawingml/2006/main}blip'))
        if txt.startswith("Assessment 3: Group Project Report"): continue          # title -> section heading
        if txt == "7. References": mode = "refs"; continue
        if p.style.name.startswith("Heading") and "Appendix" in txt: mode = "appendix"; continue
        if has_img:
            picture(ASSETS / "quentin_diagnostics_web.jpg", 9.0); continue
        if not txt: continue
        if mode == "refs": q_refs.append(txt); continue
        if mode == "appendix": q_appendix.append(attrib_quentin(p.text)); continue
        if p.style.name.startswith("Heading"):
            doc.add_heading(attrib_quentin(txt), level=3); continue
        if p.style.name == "Caption":
            para(attrib_quentin(txt).replace("Figure 1", "Figure 2."), size=SMALL, italic=True, align=WD_ALIGN_PARAGRAPH.CENTER, after=3); continue
        copy_para(p, attrib_quentin, style="List Bullet" if p.style.name == "List Paragraph" else None)
    elif tag == "tbl" and mode == "body":
        tb = docx.table.Table(el, qd)
        rows = [[c.text for c in r.cells] for r in tb.rows]
        ncol = len(rows[0])
        widths = {4: [3.3, 2.6, 1.9, 10.3], 6: [3.6, 1.5, 1.5, 1.5, 1.5, 1.5], 7: [3.3, 1.7, 1.5, 1.6, 1.4, 2.8, 5.8]}.get(ncol)
        add_table(rows, widths=widths, transform=attrib_quentin)

# ------------------------------------------------------------------ 4. Validation (Max)
doc.add_heading("4. Independent Validation and Benchmark Models (Max Turner)", level=1)
rich([("Benchmarks. ", True), ("Max\u2019s OLS 2.1 reaches R\u00b2 0.531 (adj. 0.491, p < 0.001) and CV R\u00b2 0.379 \u00b1 0.16 (RMSE 1.52, MAE 1.23; baseline RMSE 2.01, i.e. 24% less error). Squad value is the strongest predictor: a squad worth 10\u00d7 more is worth about +1.65 goals (p < 0.001); hosts gain +0.96 (p = 0.027). Elo and rank are not individually significant once value is included (VIF 4\u20137). Out-of-fold, it picks the winner in 82.5% of decisive matches; the largest misses are blow-outs such as Canada 6\u20130 Qatar. Max\u2019s OLS 2.2 reaches R\u00b2 0.306 and CV R\u00b2 0.210 \u00b1 0.12 (RMSE 1.206 vs 1.390); own squad value is again the key predictor (b = 1.18, p < 0.001) and knockout stage has no effect (p = 0.46). Ridge (CV R\u00b2 0.387) and Lasso (0.371) barely change 2.1 and Lasso is best for 2.2 (0.225), while Random Forest (0.341; 0.178) and Gradient Boosting do worse at n = 104: the relationships are essentially linear.", False)])
v = pd.read_csv(A3 / "outputs" / "validate_team_models.csv")
rows = [["Model (author)", "Terms", "CV R\u00b2 (SD)", "Fold range", "RMSE", "MAE"]]
for _, r in v.iterrows():
    rows.append([r.model, int(r.k), f"{r.cv_r2:.3f} ({r.cv_r2_sd:.3f})", f"{r.cv_r2_min:.2f} to {r.cv_r2_max:.2f}", f"{r.cv_rmse:.3f}", f"{r.cv_mae:.3f}"])
para("Table 1. Members\u2019 models re-scored as specified (data unchanged, scaler fitted inside folds), 100 held-out folds.", size=SMALL, italic=True, after=1).paragraph_format.keep_with_next = True
add_table(rows, widths=[8.4, 1.2, 2.4, 2.4, 1.4, 1.4])
rich([("Both members\u2019 models beat the baseline on every metric. Stephen\u2019s Ridge reaches CV R\u00b2 0.290, a little below his single split (0.379) and single 5-fold run (0.323), with a wide fold spread typical of n = 104; his eight base variables alone give the same accuracy (0.292). Quentin\u2019s OLS moves from in-sample R\u00b2 0.239 to CV R\u00b2 0.093 (0.113 with match-grouped folds), consistent with only the two FIFA-rank variables carrying signal. Stephen\u2019s and Max\u2019s 2.1 models reach similar accuracy from largely different variables, so pre-match strength robustly explains about a third of goal-difference variance.", False)])

# ------------------------------------------------------------------ 5. Discussion (Max)
doc.add_heading("5. Discussion, Limitations and Conclusion (Max Turner)", level=1)
rich([("Variable rules. ", True), ("Stephen\u2019s 2.1 and Quentin\u2019s 2.2 share no identically defined variable; one concept overlaps (rest days), so 1 variable is shared (limit 4). Stephen\u2019s dataset has eight collected variables; his specification adds a knockout flag and two interactions (11 terms), so the eight-variable version is also reported in Table 1.", False)])
rich([("Data caveats. ", True), ("(i) Quentin\u2019s is_host_or_home equals 1 for the first-listed team (51.9% of rows) rather than only the three hosts, so it partly reflects listing order; first-match scoring form and rest days use fixed starting values. (ii) Stephen\u2019s Elo gaps differ from eloratings.net pre-match values (e.g. Mexico v South Africa 274 vs 357; median gap 66 points, r = 0.93), probably a different snapshot date. (iii) Transfermarkt values are current, not pre-tournament, so the value effect may be slightly inflated. (iv) eloratings.net is not a listed source; it was used because the listed sites do not publish Elo or full match histories. (v) Small samples and count-valued targets limit inference; Poisson models would suit goals.", False)])
rich([("Conclusion. ", True), ("Pre-match team strength (squad value, rank, Elo) explains about a third of the variance in goal difference and a fifth of a team\u2019s goals; the rest is match-level randomness. Linear models are adequate, and cross-validation rather than in-sample R\u00b2 gives the honest picture for every model.", False)])

# ------------------------------------------------------------------ 6. Contributions
doc.add_heading("6. Group Contributions", level=1)
rich([("Max Turner: ", True), ("data sourcing and compilation, pre-match feature engineering, benchmark pipeline for both objectives (run_all.py), validation design and validate_team_models.py, Sections 1, 4 and 5, and integration of this report. ", False),
      ("Stephen K Kenyi: ", True), ("Model 2.1 dataset (FBref, eloratings.net), stage-aware Ridge model and Python code, summary table and plots, Section 2. ", False),
      ("Junxian \u201cQuentin\u201d Qiu: ", True), ("Model 2.2 dataset, OLS model, diagnostics and notebook, Section 3. ", False),
      ("Collaboration was coordinated on the unit\u2019s Microsoft Teams space and the shared GitHub repository.", False)], after=1)
if q_appendix:
    txt = " ".join(q_appendix).replace("\n", " ")
    para(txt, size=SMALL, after=2)

# ------------------------------------------------------------------ References (two columns, small)
doc.add_heading("References", level=1)
new = doc.add_section(WD_SECTION.CONTINUOUS)
cols = new._sectPr.xpath("./w:cols")
c = cols[0] if cols else OxmlElement("w:cols")
c.set(qn("w:num"), "2"); c.set(qn("w:space"), "284")
if not cols: new._sectPr.append(c)
max_refs = [
    "eloratings.net, 2026. World Football Elo Ratings: team match histories. https://www.eloratings.net/ (accessed 16 Oct 2026).",
    "FBref, 2026. FIFA World Cup 2026 statistics. https://fbref.com/en/.",
    "openfootball, 2026. worldcup.json: 2026 World Cup results. https://github.com/openfootball/worldcup.json.",
    "Pedregosa, F. et al., 2011. Scikit-learn: Machine learning in Python. Journal of Machine Learning Research, 12, pp.2825\u20132830.",
    "Seabold, S. and Perktold, J., 2010. Statsmodels: Econometric and statistical modeling with Python. Proceedings of the 9th Python in Science Conference, pp.92\u201396.",
    "Transfermarkt, 2026. World Cup 2026 participants (squad values, age). https://www.transfermarkt.com/weltmeisterschaft-2026/teilnehmer/pokalwettbewerb/FIWC/saison_id/2025.",
    "Wikipedia, 2026. 2026 FIFA World Cup: qualified teams and FIFA rankings. https://en.wikipedia.org/wiki/2026_FIFA_World_Cup.",
]
for rtxt in sorted(q_refs + max_refs, key=lambda s: s.lower()):
    p = para(rtxt, size=7, after=1)
    p.paragraph_format.left_indent = Cm(0.3); p.paragraph_format.first_line_indent = Cm(-0.3)

OUTDOCX.parent.mkdir(parents=True, exist_ok=True)
doc.save(OUTDOCX)
print("saved", OUTDOCX)
