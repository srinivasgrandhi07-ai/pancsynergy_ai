import os
import pptx
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE

def build_presentation():
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)

    blank_layout = prs.slide_layouts[6]

    # Color Palette
    C_DARK = RGBColor(15, 23, 42)       # Slate 900
    C_CARD = RGBColor(30, 41, 59)       # Slate 800
    C_TEAL = RGBColor(13, 148, 136)     # Teal 600
    C_EMERALD = RGBColor(16, 185, 129)  # Emerald 500
    C_CYAN = RGBColor(6, 182, 212)      # Cyan 500
    C_AMBER = RGBColor(245, 158, 11)    # Amber 500
    C_WHITE = RGBColor(255, 255, 255)
    C_LIGHT_GRAY = RGBColor(241, 245, 249) # Slate 100
    C_TEXT_MUTED = RGBColor(148, 163, 184) # Slate 400
    C_BORDER = RGBColor(51, 65, 85)     # Slate 700

    def add_header(slide, title_text, category_text="PANCSYNERGY AI • COMPUTATIONAL ONCOLOGY"):
        # Header category badge
        cat_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.4), Inches(11.7), Inches(0.35))
        tf_c = cat_box.text_frame
        tf_c.word_wrap = True
        tf_c.margin_left = tf_c.margin_top = tf_c.margin_right = tf_c.margin_bottom = 0
        p_c = tf_c.paragraphs[0]
        p_c.text = category_text.upper()
        p_c.font.size = Pt(10)
        p_c.font.bold = True
        p_c.font.color.rgb = C_EMERALD

        # Slide Title
        t_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.75), Inches(11.7), Inches(0.6))
        tf_t = t_box.text_frame
        tf_t.word_wrap = True
        tf_t.margin_left = tf_t.margin_top = tf_t.margin_right = tf_t.margin_bottom = 0
        p_t = tf_t.paragraphs[0]
        p_t.text = title_text
        p_t.font.size = Pt(22)
        p_t.font.bold = True
        p_t.font.color.rgb = C_WHITE

    def add_card(slide, left, top, width, height, bg_color=C_CARD, border_color=C_BORDER):
        shape = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
        shape.fill.solid()
        shape.fill.fore_color.rgb = bg_color
        if border_color:
            shape.line.color.rgb = border_color
            shape.line.width = Pt(1)
        else:
            shape.line.fill.background()
        return shape

    def set_slide_background(slide, color=C_DARK):
        background = slide.background
        fill = background.fill
        fill.solid()
        fill.fore_color.rgb = color

    # =========================================================================
    # SLIDE 1: Title Slide
    # =========================================================================
    s1 = prs.slides.add_slide(blank_layout)
    set_slide_background(s1, C_DARK)

    # Accent decorative background pill
    add_card(s1, Inches(0.8), Inches(1.8), Inches(11.733), Inches(4.5), bg_color=C_CARD, border_color=C_TEAL)

    # Badge
    b_box = s1.shapes.add_textbox(Inches(1.3), Inches(2.3), Inches(8), Inches(0.4))
    tf_b = b_box.text_frame
    p_b = tf_b.paragraphs[0]
    p_b.text = "NEXT-GENERATION CHEMINFORMATICS & COMPUTATIONAL ONCOLOGY"
    p_b.font.size = Pt(11)
    p_b.font.bold = True
    p_b.font.color.rgb = C_EMERALD

    # Main Title
    title_box = s1.shapes.add_textbox(Inches(1.3), Inches(2.8), Inches(10.7), Inches(1.3))
    tf = title_box.text_frame
    tf.word_wrap = True
    p1 = tf.paragraphs[0]
    p1.text = "PancSynergy AI"
    p1.font.size = Pt(44)
    p1.font.bold = True
    p1.font.color.rgb = C_WHITE

    # Subtitle
    sub_box = s1.shapes.add_textbox(Inches(1.3), Inches(4.1), Inches(10.5), Inches(0.9))
    tf_sub = sub_box.text_frame
    tf_sub.word_wrap = True
    p_sub = tf_sub.paragraphs[0]
    p_sub.text = "Machine-Learning-Assisted Screening of Drug-Combination Synergy, Synthesis Reaction Kinetics, and Pharmacodynamic Eradication Dynamics in PANC-1 Pancreatic Cancer"
    p_sub.font.size = Pt(15)
    p_sub.font.color.rgb = C_LIGHT_GRAY

    # Author/Platform metadata
    meta_box = s1.shapes.add_textbox(Inches(1.3), Inches(5.2), Inches(10.5), Inches(0.6))
    tf_m = meta_box.text_frame
    p_m = tf_m.paragraphs[0]
    p_m.text = "Powered by Random Forest Regressor (Test r = 0.8016) • USPTO-50K Chemical Reaction Engine • Continuous PK/PD Hill-Emax Simulator"
    p_m.font.size = Pt(11)
    p_m.font.color.rgb = C_TEXT_MUTED

    # =========================================================================
    # SLIDE 2: The Clinical & Biological Challenge
    # =========================================================================
    s2 = prs.slides.add_slide(blank_layout)
    set_slide_background(s2, C_DARK)
    add_header(s2, "The Clinical Challenge: Pancreatic Cancer & Combination Therapy", "CLINICAL RATIONALE & UNMET NEED")

    # Card 1: Pancreatic Cancer Urgency
    c1 = add_card(s2, Inches(0.8), Inches(1.6), Inches(3.64), Inches(5.2))
    tb1 = s2.shapes.add_textbox(Inches(1.1), Inches(1.9), Inches(3.04), Inches(4.6))
    tf1 = tb1.text_frame
    tf1.word_wrap = True
    p = tf1.paragraphs[0]
    p.text = "Pancreatic Ductal Adenocarcinoma (PDAC)"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = C_EMERALD

    items1 = [
        ("Deadliest Major Cancer", "5-year survival rate remains below 11%. Projected to become the 2nd leading cause of cancer death."),
        ("Dense Fibrotic Stroma", "Desmoplastic microenvironment creates extreme interstitial fluid pressure, starving tumors of blood flow."),
        ("KRAS & TP53 Mutations", "Over 90% of PANC-1 tumors carry mutant KRAS (G12D) driving aggressive uncontrolled proliferation.")
    ]
    for h, desc in items1:
        p_h = tf1.add_paragraph()
        p_h.text = f"\n• {h}:"
        p_h.font.bold = True
        p_h.font.size = Pt(12)
        p_h.font.color.rgb = C_WHITE
        p_d = tf1.add_paragraph()
        p_d.text = desc
        p_d.font.size = Pt(11)
        p_d.font.color.rgb = C_TEXT_MUTED

    # Card 2: Monotherapy Failure
    c2 = add_card(s2, Inches(4.84), Inches(1.6), Inches(3.64), Inches(5.2))
    tb2 = s2.shapes.add_textbox(Inches(5.14), Inches(1.9), Inches(3.04), Inches(4.6))
    tf2 = tb2.text_frame
    tf2.word_wrap = True
    p = tf2.paragraphs[0]
    p.text = "Why Single-Drug Therapies Fail"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = C_AMBER

    items2 = [
        ("Adaptive Resistance", "Targeting a single kinase (e.g. MEK) triggers rapid compensatory feedback activation of parallel survival loops."),
        ("Severe Chemotoxicity", "Pushing single agents (Gemcitabine, FOLFIRINOX) to cytotoxic thresholds induces dose-limiting toxicity in patients."),
        ("Clonal Heterogeneity", "Pre-existing resistant subclones survive monotherapy, driving rapid patient relapse within months.")
    ]
    for h, desc in items2:
        p_h = tf2.add_paragraph()
        p_h.text = f"\n• {h}:"
        p_h.font.bold = True
        p_h.font.size = Pt(12)
        p_h.font.color.rgb = C_WHITE
        p_d = tf2.add_paragraph()
        p_d.text = desc
        p_d.font.size = Pt(11)
        p_d.font.color.rgb = C_TEXT_MUTED

    # Card 3: The Combinatorial Explosion Bottleneck
    c3 = add_card(s2, Inches(8.88), Inches(1.6), Inches(3.64), Inches(5.2))
    tb3 = s2.shapes.add_textbox(Inches(9.18), Inches(1.9), Inches(3.04), Inches(4.6))
    tf3 = tb3.text_frame
    tf3.word_wrap = True
    p = tf3.paragraphs[0]
    p.text = "The Combinatorial Bottleneck"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = C_CYAN

    items3 = [
        ("Combinatorial Explosion", "Screening just 1,000 oncology compounds pairwise requires 499,500 combination assays!"),
        ("Cost & Time Prohibitive", "Full 8x8 dose-matrix titration in cell culture costs millions of dollars and decades of laboratory time."),
        ("The AI Solution", "PancSynergy AI replaces brute-force screening with instant computational inference in < 200 milliseconds.")
    ]
    for h, desc in items3:
        p_h = tf3.add_paragraph()
        p_h.text = f"\n• {h}:"
        p_h.font.bold = True
        p_h.font.size = Pt(12)
        p_h.font.color.rgb = C_WHITE
        p_d = tf3.add_paragraph()
        p_d.text = desc
        p_d.font.size = Pt(11)
        p_d.font.color.rgb = C_TEXT_MUTED

    # =========================================================================
    # SLIDE 3: The 4 Core Pillars of PancSynergy AI
    # =========================================================================
    s3 = prs.slides.add_slide(blank_layout)
    set_slide_background(s3, C_DARK)
    add_header(s3, "Platform Solution: The Four Pillars of PancSynergy AI", "COMPUTATIONAL SUITE")

    pillars = [
        ("1. Drug Synergy Predictor", "Predicts continuous Gamma (Γ) synergy scores using an 802-dimensional symmetric representation. Classifies pairs into High Synergy (Γ < 0.5), Moderate (0.5 ≤ Γ < 1.0), Additive, or Antagonistic.", C_EMERALD, Inches(0.8), Inches(1.6)),
        ("2. Reaction & Kinetics Lab", "Classifies synthetic chemical feasibility across 10 USPTO patent transformation classes. Estimates combination time required (2-6h vs 6-16h), temperature, solvents, catalysts, and yield.", C_CYAN, Inches(6.8), Inches(1.6)),
        ("3. Cancer Impact Dynamics", "Continuous PK/PD simulation mapping in-vitro cancer viability curves over 0-96 hours. Calculates half-maximal eradication time (T50) and apoptotic morphological trigger points.", C_AMBER, Inches(0.8), Inches(4.3)),
        ("4. High-Throughput Batch Lab", "Allows researchers to upload multi-pair CSV matrices. Screens dozens of combinations in seconds with interactive distribution histograms and potency scatter plots.", C_TEAL, Inches(6.8), Inches(4.3)),
    ]

    for title, desc, col, l, t in pillars:
        add_card(s3, l, t, Inches(5.733), Inches(2.4), bg_color=C_CARD, border_color=col)
        tb = s3.shapes.add_textbox(l + Inches(0.3), t + Inches(0.25), Inches(5.133), Inches(1.9))
        tf_p = tb.text_frame
        tf_p.word_wrap = True
        p = tf_p.paragraphs[0]
        p.text = title
        p.font.size = Pt(16)
        p.font.bold = True
        p.font.color.rgb = col
        p_d = tf_p.add_paragraph()
        p_d.text = f"\n{desc}"
        p_d.font.size = Pt(11.5)
        p_d.font.color.rgb = C_LIGHT_GRAY

    # =========================================================================
    # SLIDE 4: Data Engineering & Cleaning Pipeline
    # =========================================================================
    s4 = prs.slides.add_slide(blank_layout)
    set_slide_background(s4, C_DARK)
    add_header(s4, "Data Engineering: Hygiene, Imputation & Leak-Free Validation", "DATA PREPROCESSING PIPELINE")

    steps = [
        ("Header & String Sanitization", "Stripped leading/trailing whitespace, \\r\\n line breaks, and UTF-8 encoding noise across all compound names, MOAs, and SMILES.", "100% clean headers"),
        ("Strict Numerical Typing", "Forced pd.to_numeric(errors='coerce') on Gamma, Label, and Log AC50. Converted invalid tokens (e.g. '--', 'N/A') into standard NaNs.", "Strict float32/int32 types"),
        ("Target Zero-Tolerance Purge", "Dropped any row with missing target Gamma or empty SMILES strings. Target values were NEVER imputed to eliminate circular data poisoning.", "Zero synthetic targets"),
        ("Empirical Median Imputation", "Missing monotherapy potencies (Log AC50) were imputed with the dataset median of -6.0 M (1.0 µM NCATS screening standard).", "Preserved rare synergy pairs"),
        ("RDKit Structure Sanitizer", "Validated valence, aromaticity, and tetrahedral stereochemistry. Invalid structures yield zeroed vectors rather than fatal exceptions.", "Chemically verified SMILES"),
        ("USPTO-50K Salt Stripping", "Ranked reactants by heavy atom count. Discarded spectator counter-ions (Na+, Cl-) and solvent molecules to isolate organic drug pairs.", "Noise-free reaction models")
    ]

    for idx, (title, desc, badge) in enumerate(steps):
        row = idx // 2
        col = idx % 2
        left = Inches(0.8) if col == 0 else Inches(6.8)
        top = Inches(1.6) + Inches(row * 1.7)
        add_card(s4, left, top, Inches(5.733), Inches(1.5), bg_color=C_CARD, border_color=C_BORDER)

        tb = s4.shapes.add_textbox(left + Inches(0.25), top + Inches(0.15), Inches(5.2), Inches(1.2))
        tf_s = tb.text_frame
        tf_s.word_wrap = True
        p = tf_s.paragraphs[0]
        p.text = f"{idx+1}. {title}"
        p.font.size = Pt(13)
        p.font.bold = True
        p.font.color.rgb = C_WHITE

        p_b = tf_s.add_paragraph()
        p_b.text = f"Status: {badge}"
        p_b.font.size = Pt(9.5)
        p_b.font.bold = True
        p_b.font.color.rgb = C_EMERALD

        p_d = tf_s.add_paragraph()
        p_d.text = desc
        p_d.font.size = Pt(10.5)
        p_d.font.color.rgb = C_TEXT_MUTED

    # =========================================================================
    # SLIDE 5: Molecular Featurization & Symmetrization Math
    # =========================================================================
    s5 = prs.slides.add_slide(blank_layout)
    set_slide_background(s5, C_DARK)
    add_header(s5, "Cheminformatics: Circular Fingerprints & Symmetrization Math", "MATHEMATICAL FEATURE ENGINEERING")

    # Left Card: Single Molecule (266 dims)
    add_card(s5, Inches(0.8), Inches(1.6), Inches(4.5), Inches(5.2), bg_color=C_CARD, border_color=C_TEAL)
    tb_l = s5.shapes.add_textbox(Inches(1.05), Inches(1.85), Inches(4.0), Inches(4.7))
    tfl = tb_l.text_frame
    tfl.word_wrap = True
    p = tfl.paragraphs[0]
    p.text = "Single Drug Vector (266 Dims)"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = C_TEAL

    p1 = tfl.add_paragraph()
    p1.text = "\n1. 256-Bit Morgan Fingerprint (ECFP4)"
    p1.font.bold = True
    p1.font.size = Pt(12)
    p1.font.color.rgb = C_WHITE
    p1_d = tfl.add_paragraph()
    p1_d.text = "Circular radius = 2 bonds (diameter 4). Identifies functional binding motifs (hydroxamic acids, kinase heterocycles) folded into 256 bits."
    p1_d.font.size = Pt(10.5)
    p1_d.font.color.rgb = C_TEXT_MUTED

    p2 = tfl.add_paragraph()
    p2.text = "\n2. 10 2D Physicochemical Descriptors"
    p2.font.bold = True
    p2.font.size = Pt(12)
    p2.font.color.rgb = C_WHITE
    p2_d = tfl.add_paragraph()
    p2_d.text = "• MolWt (Molecular Weight)\n• MolLogP (Lipophilicity / solubility)\n• TPSA (Polar surface area)\n• H-Bond Donors & Acceptors (HBD/HBA)\n• Rotatable Bonds (Flexibility)\n• Fraction CSP3 (3D complexity)\n• Ring Count & Aromatic Rings\n• Heavy Atom Count"
    p2_d.font.size = Pt(10)
    p2_d.font.color.rgb = C_LIGHT_GRAY

    # Right Card: The 802-Dim Symmetrizer
    add_card(s5, Inches(5.6), Inches(1.6), Inches(6.933), Inches(5.2), bg_color=C_CARD, border_color=C_EMERALD)
    tb_r = s5.shapes.add_textbox(Inches(5.9), Inches(1.85), Inches(6.333), Inches(4.7))
    tfr = tb_r.text_frame
    tfr.word_wrap = True
    p = tfr.paragraphs[0]
    p.text = "Order-Invariant Symmetrization (802 Dims)"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = C_EMERALD

    sym_text = [
        ("The Permutational Problem:", "In biology, Drug A + Drug B is identical to Drug B + Drug A. Concatenating [v_A, v_B] creates order bias and double-counting."),
        ("Vector Sum (v_A + v_B) — 266 dims:", "Captures the total combined chemical functionalities and molecular bulk."),
        ("Absolute Difference |v_A - v_B| — 266 dims:", "Captures structural divergence and chemical complementarity between the drugs."),
        ("Hadamard Product (v_A ⊙ v_B) — 266 dims:", "Captures shared pharmacophore motifs present in both compounds."),
        ("Symmetric Potency Vector — 4 dims:", "[min(AC50), max(AC50), |AC50_1 - AC50_2|, AC50_1 + AC50_2]"),
        ("Mathematical Invariance Proof:", "f(A, B) ≡ f(B, A) is mathematically guaranteed at the input level.")
    ]
    for h, d in sym_text:
        ph = tfr.add_paragraph()
        ph.text = f"\n• {h} "
        ph.font.bold = True
        ph.font.size = Pt(11.5)
        ph.font.color.rgb = C_WHITE
        pd = tfr.add_paragraph()
        pd.text = d
        pd.font.size = Pt(10.5)
        pd.font.color.rgb = C_TEXT_MUTED

    # =========================================================================
    # SLIDE 6: Machine Learning Benchmark Leaderboard & Visual Snapshot
    # =========================================================================
    s6 = prs.slides.add_slide(blank_layout)
    set_slide_background(s6, C_DARK)
    add_header(s6, "Machine Learning Evaluation: 8-Model Benchmark Leaderboard", "MODEL SELECTION & EVALUATION")

    # Embed snapshot image
    img_path1 = os.path.join(os.path.dirname(os.path.abspath(__file__)), "docs", "images", "ml_evaluation_snapshot.png")
    if os.path.exists(img_path1):
        s6.shapes.add_picture(img_path1, Inches(0.8), Inches(1.6), Inches(7.2), Inches(3.2))

    # Leaderboard Table Card
    add_card(s6, Inches(8.2), Inches(1.6), Inches(4.333), Inches(5.2), bg_color=C_CARD, border_color=C_EMERALD)
    tb_lead = s6.shapes.add_textbox(Inches(8.4), Inches(1.8), Inches(3.933), Inches(4.7))
    tf_l = tb_lead.text_frame
    tf_l.word_wrap = True
    p = tf_l.paragraphs[0]
    p.text = "Benchmark Leaderboard"
    p.font.size = Pt(15)
    p.font.bold = True
    p.font.color.rgb = C_EMERALD

    l_items = [
        ("🏆 Random Forest", "r = 0.8016", "R² = 0.5710"),
        ("2. Gradient Boosting", "r = 0.7913", "R² = 0.6015"),
        ("3. Hist Gradient Boosting", "r = 0.7833", "R² = 0.5991"),
        ("4. Lasso Regression", "r = 0.7723", "R² = 0.4756"),
        ("5. ElasticNet", "r = 0.7615", "R² = 0.5259"),
        ("6. Extra Trees", "r = 0.7481", "R² = 0.5344"),
        ("7. Ridge Regression", "r = 0.5611", "R² = 0.1576"),
        ("8. Deep MLP Neural Net", "r = 0.4074", "R² = -0.1413"),
    ]
    for name, r_val, r2_val in l_items:
        p_row = tf_l.add_paragraph()
        p_row.text = f"{name}: {r_val} | {r2_val}"
        p_row.font.size = Pt(11)
        if "🏆" in name:
            p_row.font.bold = True
            p_row.font.color.rgb = C_AMBER
        else:
            p_row.font.color.rgb = C_LIGHT_GRAY

    # Bottom summary box on the left
    add_card(s6, Inches(0.8), Inches(5.0), Inches(7.2), Inches(1.8), bg_color=C_CARD, border_color=C_BORDER)
    tb_obs = s6.shapes.add_textbox(Inches(1.0), Inches(5.15), Inches(6.8), Inches(1.5))
    tf_o = tb_obs.text_frame
    tf_o.word_wrap = True
    p_ob = tf_o.paragraphs[0]
    p_ob.text = "Empirical Finding: Why Random Forest Won"
    p_ob.font.bold = True
    p_ob.font.size = Pt(12)
    p_ob.font.color.rgb = C_WHITE
    p_ob_d = tf_o.add_paragraph()
    p_ob_d.text = "With N = 498 samples and 802 features, Deep MLP suffered from over-parameterization. Random Forest, through bootstrap bagging and m = sqrt(802) ≈ 28 randomized feature sampling, constrained tree variance while capturing non-linear biological thresholds."
    p_ob_d.font.size = Pt(10.5)
    p_ob_d.font.color.rgb = C_TEXT_MUTED

    # =========================================================================
    # SLIDE 7: Biological Insights & Top Validated Combinations
    # =========================================================================
    s7 = prs.slides.add_slide(blank_layout)
    set_slide_background(s7, C_DARK)
    add_header(s7, "Biological Findings: Epigenetic & Proteasome Synthetic Lethality", "EXPERIMENTAL VALIDATION")

    img_path2 = os.path.join(os.path.dirname(os.path.abspath(__file__)), "docs", "images", "top_synergies_and_mechanisms.png")
    if os.path.exists(img_path2):
        s7.shapes.add_picture(img_path2, Inches(0.8), Inches(1.6), Inches(7.5), Inches(3.2))

    # Right Card: Biological Mechanism Breakdown
    add_card(s7, Inches(8.5), Inches(1.6), Inches(4.033), Inches(5.2), bg_color=C_CARD, border_color=C_AMBER)
    tb_bio = s7.shapes.add_textbox(Inches(8.75), Inches(1.85), Inches(3.533), Inches(4.7))
    tf_b2 = tb_bio.text_frame
    tf_b2.word_wrap = True
    p = tf_b2.paragraphs[0]
    p.text = "Top Synergy Mechanisms"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = C_AMBER

    bio_items = [
        ("HDACi + Proteasome Inhibitors", "Panobinostat + Carfilzomib (Γ = 0.0414) and Oprozomib + Panobinostat produce severe proteotoxic crisis overloading ubiquitinated protein clearance."),
        ("Survivin Inhibition", "Trichostatin A + Sepantronium bromide disables the cellular anti-apoptotic shield."),
        ("Antifolate + NAMPT Blockade", "Pralatrexate + Daporinad starves PANC-1 cells simultaneously of purines and NAD+ energy."),
        ("Prevalent Target Classes", "Proteasome inhibitors (>110 occurrences), PLK-1, HDAC inhibitors, and Mutant p53 activators represent 70% of all synergistic hits.")
    ]
    for h, d in bio_items:
        ph = tf_b2.add_paragraph()
        ph.text = f"\n• {h}:"
        ph.font.bold = True
        ph.font.size = Pt(11.5)
        ph.font.color.rgb = C_WHITE
        pd = tf_b2.add_paragraph()
        pd.text = d
        pd.font.size = Pt(10.5)
        pd.font.color.rgb = C_TEXT_MUTED

    # Bottom summary box
    add_card(s7, Inches(0.8), Inches(5.0), Inches(7.5), Inches(1.8), bg_color=C_CARD, border_color=C_BORDER)
    tb_bot = s7.shapes.add_textbox(Inches(1.0), Inches(5.15), Inches(7.1), Inches(1.5))
    tf_bt = tb_bot.text_frame
    tf_bt.word_wrap = True
    p = tf_bt.paragraphs[0]
    p.text = "Validation Significance"
    p.font.bold = True
    p.font.size = Pt(12)
    p.font.color.rgb = C_WHITE
    p_d = tf_bt.add_paragraph()
    p_d.text = "The model accurately identified that epigenetic chromatin remodeling (HDAC inhibition) relaxes transcription factors, exposing pancreatic cancer DNA to crosslinkers and sensitizing cells to proteasome-mediated apoptosis."
    p_d.font.size = Pt(10.5)
    p_d.font.color.rgb = C_LIGHT_GRAY

    # =========================================================================
    # SLIDE 8: Reaction Kinetics & USPTO-50K Chemical Synthesis
    # =========================================================================
    s8 = prs.slides.add_slide(blank_layout)
    set_slide_background(s8, C_DARK)
    add_header(s8, "Chemical Synthesis Lab: USPTO-50K Reaction Pathways & Kinetics", "MEDICINAL SYNTHESIS ENGINE")

    # 3 Column Cards
    col_w = Inches(3.64)
    # Col 1: The Problem
    add_card(s8, Inches(0.8), Inches(1.6), col_w, Inches(5.2), bg_color=C_CARD, border_color=C_BORDER)
    tb_c1 = s8.shapes.add_textbox(Inches(1.0), Inches(1.8), Inches(3.24), Inches(4.7))
    tf_c1 = tb_c1.text_frame
    tf_c1.word_wrap = True
    p = tf_c1.paragraphs[0]
    p.text = "Synthetic Feasibility"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = C_CYAN
    items_c1 = [
        ("Beyond Synergy", "Oncologists need to know if two drugs can be linked into an antibody-drug conjugate (ADC) or covalent bispecific."),
        ("Chemical Incompatibility", "Prevents accidental degradation or precipitation when mixing drugs in infusion bags."),
        ("USPTO-50K Dataset", "Trained on 50,000+ patented chemical reactions across 10 standardized transformation classes.")
    ]
    for h, d in items_c1:
        ph = tf_c1.add_paragraph()
        ph.text = f"\n• {h}:"
        ph.font.bold = True
        ph.font.size = Pt(11.5)
        ph.font.color.rgb = C_WHITE
        pd = tf_c1.add_paragraph()
        pd.text = d
        pd.font.size = Pt(10.5)
        pd.font.color.rgb = C_TEXT_MUTED

    # Col 2: The Model
    add_card(s8, Inches(4.84), Inches(1.6), col_w, Inches(5.2), bg_color=C_CARD, border_color=C_TEAL)
    tb_c2 = s8.shapes.add_textbox(Inches(5.04), Inches(1.8), Inches(3.24), Inches(4.7))
    tf_c2 = tb_c2.text_frame
    tf_c2.word_wrap = True
    p = tf_c2.paragraphs[0]
    p.text = "HistGradientBoosting"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = C_TEAL
    items_c2 = [
        ("1,571 Features", "512-bit Morgan fingerprints + 7 physicochemical descriptors per reactant symmetrized: [sum, diff, product]."),
        ("Histogram Binning", "Discretizes 1,571 continuous features into 255 integer bins, accelerating gradient splits by 20x."),
        ("Multi-Class Cross Entropy", "Outputs softmax probabilities across all 10 synthetic organic classes.")
    ]
    for h, d in items_c2:
        ph = tf_c2.add_paragraph()
        ph.text = f"\n• {h}:"
        ph.font.bold = True
        ph.font.size = Pt(11.5)
        ph.font.color.rgb = C_WHITE
        pd = tf_c2.add_paragraph()
        pd.text = d
        pd.font.size = Pt(10.5)
        pd.font.color.rgb = C_TEXT_MUTED

    # Col 3: Kinetic Predictions
    add_card(s8, Inches(8.88), Inches(1.6), col_w, Inches(5.2), bg_color=C_CARD, border_color=C_EMERALD)
    tb_c3 = s8.shapes.add_textbox(Inches(9.08), Inches(1.8), Inches(3.24), Inches(4.7))
    tf_c3 = tb_c3.text_frame
    tf_c3.word_wrap = True
    p = tf_c3.paragraphs[0]
    p.text = "Kinetic Predictions"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = C_EMERALD
    items_c3 = [
        ("Combination Time", "Predicts reaction duration: 2-6 hours (Amide Coupling) vs 6-16 hours (Suzuki cross-coupling)."),
        ("Optimal Temperature", "Specifies kinetic window: 0-25 °C (ambient) vs 70-110 °C reflux."),
        ("Solvent & Catalysts", "Recommends DCM/DMF with HATU/DIPEA for acylation; Dioxane/Pd(dppf)Cl2 for C-C couplings."),
        ("Isolated Yield Range", "Expected yield: 80 - 95%.")
    ]
    for h, d in items_c3:
        ph = tf_c3.add_paragraph()
        ph.text = f"\n• {h}:"
        ph.font.bold = True
        ph.font.size = Pt(11.5)
        ph.font.color.rgb = C_WHITE
        pd = tf_c3.add_paragraph()
        pd.text = d
        pd.font.size = Pt(10.5)
        pd.font.color.rgb = C_TEXT_MUTED

    # =========================================================================
    # SLIDE 9: Cancer Impact Dynamics & PK/PD Kinetic Engine
    # =========================================================================
    s9 = prs.slides.add_slide(blank_layout)
    set_slide_background(s9, C_DARK)
    add_header(s9, "Cancer Impact Dynamics: Continuous PK/PD Kill Engine & T50", "PHARMACODYNAMIC TIME-COURSE")

    # Left: Mathematical Formulas
    add_card(s9, Inches(0.8), Inches(1.6), Inches(5.7), Inches(5.2), bg_color=C_CARD, border_color=C_EMERALD)
    tb_pk = s9.shapes.add_textbox(Inches(1.05), Inches(1.8), Inches(5.2), Inches(4.7))
    tf_pk = tb_pk.text_frame
    tf_pk.word_wrap = True
    p = tf_pk.paragraphs[0]
    p.text = "Dynamic PK/PD Mathematical Equations"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = C_EMERALD

    eqs = [
        ("1. Potency Shift:", "Δ_i = -(Log AC50_i - (-6.0 M))\nHigh potency (-8.0 M) yields Δ = +2.0 (faster target engagement)."),
        ("2. Single-Agent Rate Constant:", "k_i = clamp(0.018 × 1.35^(Δ_i) × DoseMultiplier, 0.008, 0.065) h⁻¹"),
        ("3. Continuous Synergy Multiplier:", "S = clamp((1.0 / γ)^0.92, 0.35, 3.80)\nSynergy (γ = 0.38) speeds up kill by 2.45×; Antagonism (γ = 1.68) slows to 0.62×."),
        ("4. Combined Kill Velocity:", "k_combo = (k_A + k_B) × S"),
        ("5. Half-Maximal Eradication Time (T50):", "T50 = ln(2) / k_combo ≈ 0.69315 / k_combo hours")
    ]
    for h, d in eqs:
        ph = tf_pk.add_paragraph()
        ph.text = f"\n• {h} "
        ph.font.bold = True
        ph.font.size = Pt(11.5)
        ph.font.color.rgb = C_WHITE
        pd = tf_pk.add_paragraph()
        pd.text = d
        pd.font.size = Pt(10.5)
        pd.font.color.rgb = C_TEXT_MUTED

    # Right: Biological Apoptotic Phases
    add_card(s9, Inches(6.8), Inches(1.6), Inches(5.733), Inches(5.2), bg_color=C_CARD, border_color=C_AMBER)
    tb_ap = s9.shapes.add_textbox(Inches(7.05), Inches(1.8), Inches(5.2), Inches(4.7))
    tf_ap = tb_ap.text_frame
    tf_ap.word_wrap = True
    p = tf_ap.paragraphs[0]
    p.text = "Biological Phases on the 0-96h Time Scrubber"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = C_AMBER

    phases = [
        ("0 - 6 Hours (Phase I: Target Engagement)", "Drug enters plasma membrane; G1/S cell cycle arrest begins; priming of Caspase-8/9."),
        ("6 - 18 Hours (Phase II: Mitochondrial Collapse)", "Loss of mitochondrial outer membrane potential (MOMP); release of Cytochrome C (T25 milestone reached)."),
        ("18 - 36 Hours (Phase III: Executioner Caspases)", "Massive cleavage of Caspase-3/7 and PARP-1. Severe nuclear DNA fragmentation (T50 milestone reached)."),
        ("36 - 72 Hours (Phase IV: Apoptotic Lysis)", "> 90% of PANC-1 tumor cells eliminated; complete loss of membrane integrity and phagocytic clearance."),
        ("72 - 96 Hours (Phase V: Resistance Prevention)", "Synergistic pressure permanently prevents surviving resistant clones from repopulating.")
    ]
    for h, d in phases:
        ph = tf_ap.add_paragraph()
        ph.text = f"\n• {h}:"
        ph.font.bold = True
        ph.font.size = Pt(11)
        ph.font.color.rgb = C_WHITE
        pd = tf_ap.add_paragraph()
        pd.text = d
        pd.font.size = Pt(10)
        pd.font.color.rgb = C_TEXT_MUTED

    # =========================================================================
    # SLIDE 10: Complete System Architecture & Cloud Blueprint
    # =========================================================================
    s10 = prs.slides.add_slide(blank_layout)
    set_slide_background(s10, C_DARK)
    add_header(s10, "System Architecture: End-to-End Enterprise Cloud Blueprint", "SYSTEM ARCHITECTURE")

    img_path3 = os.path.join(os.path.dirname(os.path.abspath(__file__)), "docs", "images", "demo_reference_cloud_arch.png")
    if os.path.exists(img_path3):
        s10.shapes.add_picture(img_path3, Inches(0.8), Inches(1.6), Inches(5.5), Inches(5.2))

    # Right Card: Architecture Mapping
    add_card(s10, Inches(6.6), Inches(1.6), Inches(5.933), Inches(5.2), bg_color=C_CARD, border_color=C_CYAN)
    tb_arch = s10.shapes.add_textbox(Inches(6.85), Inches(1.8), Inches(5.4), Inches(4.7))
    tf_ar = tb_arch.text_frame
    tf_ar.word_wrap = True
    p = tf_ar.paragraphs[0]
    p.text = "Enterprise Architecture Mapping"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = C_CYAN

    arch_items = [
        ("Client Tier (React 18 + Vite SPA)", "Single-page dashboard with Tailwind CSS and Recharts; responsive sub-second page transitions."),
        ("API Gateway (FastAPI • Port 8081)", "Asynchronous ASGI backend with Pydantic v2 validation, CORS middleware, and automated OpenAPI/Swagger docs."),
        ("Inference Engine (RDKit + Scikit-Learn)", "Pre-loaded in-memory Random Forest and HistGradientBoosting models executing inference in < 200ms."),
        ("Data & Model Tier", "Storage containers holding .pkl models, NCATS matrix datasets, and 51+ curated oncology compounds."),
        ("Deployment Slots (Staging ➔ Production)", "Enables zero-downtime blue/green deployment when promoting newly trained models."),
        ("GitHub CI/CD Automation", "Automated deployment directly from srinivasgrandhi07-ai/pancsynergy_ai.")
    ]
    for h, d in arch_items:
        ph = tf_ar.add_paragraph()
        ph.text = f"\n• {h}:"
        ph.font.bold = True
        ph.font.size = Pt(11)
        ph.font.color.rgb = C_WHITE
        pd = tf_ar.add_paragraph()
        pd.text = d
        pd.font.size = Pt(10)
        pd.font.color.rgb = C_TEXT_MUTED

    # =========================================================================
    # SLIDE 11: Demonstration & High-Throughput Batch Screening
    # =========================================================================
    s11 = prs.slides.add_slide(blank_layout)
    set_slide_background(s11, C_DARK)
    add_header(s11, "Live Demonstration: High-Throughput Batch Screening", "PLATFORM DEMO")

    # Left: Steps
    add_card(s11, Inches(0.8), Inches(1.6), Inches(5.5), Inches(5.2), bg_color=C_CARD, border_color=C_EMERALD)
    tb_demo = s11.shapes.add_textbox(Inches(1.05), Inches(1.8), Inches(5.0), Inches(4.7))
    tf_dm = tb_demo.text_frame
    tf_dm.word_wrap = True
    p = tf_dm.paragraphs[0]
    p.text = "Demonstration Workflow"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = C_EMERALD

    demo_steps = [
        ("Step 1: Upload CSV Matrix", "Upload demo_batch_screening.csv (contains 10 curated oncology combinations) directly into the web UI."),
        ("Step 2: Instant Client Validation", "PapaParse validates SMILES lengths and headers; displays an interactive 10/10 green checkmark table."),
        ("Step 3: High-Throughput Inference", "Queries POST /api/v1/predict/batch; evaluates all 802-dimensional vectors in parallel in < 0.3s."),
        ("Step 4: Interactive Visualizations", "Renders dynamic Gamma histogram, potency-vs-synergy scatter plot, and ranked table."),
        ("Step 5: One-Click Export", "Exports enriched results with predicted Gamma, synergy classification, and strength tags back to CSV.")
    ]
    for h, d in demo_steps:
        ph = tf_dm.add_paragraph()
        ph.text = f"\n• {h}:"
        ph.font.bold = True
        ph.font.size = Pt(11.5)
        ph.font.color.rgb = C_WHITE
        pd = tf_dm.add_paragraph()
        pd.text = d
        pd.font.size = Pt(10.5)
        pd.font.color.rgb = C_TEXT_MUTED

    # Right: Results Table Preview
    add_card(s11, Inches(6.6), Inches(1.6), Inches(5.933), Inches(5.2), bg_color=C_CARD, border_color=C_BORDER)
    tb_res = s11.shapes.add_textbox(Inches(6.85), Inches(1.8), Inches(5.4), Inches(4.7))
    tf_rs = tb_res.text_frame
    tf_rs.word_wrap = True
    p = tf_rs.paragraphs[0]
    p.text = "Verified Results in demo_batch_screening.csv"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = C_WHITE

    res_list = [
        ("Panobinostat + Carfilzomib", "Γ = 0.3278", "High Synergy", C_EMERALD),
        ("Pralatrexate + Daporinad", "Γ = 0.9872", "Moderate Synergy", C_TEAL),
        ("Oprozomib + Panobinostat", "Γ = 0.4386", "High Synergy", C_EMERALD),
        ("Sepantronium + Daporinad", "Γ = 0.9755", "Moderate Synergy", C_TEAL),
        ("GMX-1778 + Daporinad", "Γ = 0.7757", "Moderate Synergy", C_TEAL),
        ("Gemcitabine + Cisplatin", "Γ = 0.9631", "Moderate Synergy", C_TEAL),
        ("Paclitaxel + Vorinostat", "Γ = 0.9635", "Moderate Synergy", C_TEAL),
        ("Irinotecan + 5-FU", "Γ = 1.0301", "Additive / Weak", C_AMBER),
        ("Methotrexate + Aminopterin", "Γ = 0.8645", "Moderate Synergy", C_TEAL),
        ("Parogrelil + Osanetant", "Γ = 0.9713", "Moderate Synergy", C_TEAL),
    ]
    for pair, g_val, cl_val, col in res_list:
        p_row = tf_rs.add_paragraph()
        p_row.text = f"• {pair} ➔ {g_val} ({cl_val})"
        p_row.font.size = Pt(10.5)
        p_row.font.color.rgb = col

    # =========================================================================
    # SLIDE 12: Future Horizons & Clinical Roadmap
    # =========================================================================
    s12 = prs.slides.add_slide(blank_layout)
    set_slide_background(s12, C_DARK)
    add_header(s12, "Future Horizons: From In-Silico Prediction to Clinical Translation", "ROADMAP & NEXT STEPS")

    future_cards = [
        ("Patient Multi-Omics Integration", "Incorporate patient-specific RNA-seq transcriptomics and specific KRAS allele mutations (G12D vs G12V vs G12R) to personalize synergy predictions for individual patients.", C_CYAN, Inches(0.8), Inches(1.6)),
        ("In-Vivo PDX Translation", "Validate top computational hits (Panobinostat + Carfilzomib) in patient-derived xenograft (PDX) mouse models to establish in-vivo tumor regression and toxicity thresholds.", C_EMERALD, Inches(6.8), Inches(1.6)),
        ("Automated Robotic Synthesis", "Connect the USPTO-50K synthesis engine directly to automated flow-chemistry robotic synthesizers for continuous compound generation.", C_AMBER, Inches(0.8), Inches(4.3)),
        ("Open Science & API Ecosystem", "Publish the trained model weights and RESTful endpoints for integration into academic hospital computational oncology pipelines.", C_TEAL, Inches(6.8), Inches(4.3)),
    ]

    for title, desc, col, l, t in future_cards:
        add_card(s12, l, t, Inches(5.733), Inches(2.4), bg_color=C_CARD, border_color=col)
        tb = s12.shapes.add_textbox(l + Inches(0.3), t + Inches(0.25), Inches(5.133), Inches(1.9))
        tf_f = tb.text_frame
        tf_f.word_wrap = True
        p = tf_f.paragraphs[0]
        p.text = title
        p.font.size = Pt(16)
        p.font.bold = True
        p.font.color.rgb = col
        p_d = tf_f.add_paragraph()
        p_d.text = f"\n{desc}"
        p_d.font.size = Pt(11.5)
        p_d.font.color.rgb = C_LIGHT_GRAY

    # Save presentation
    output_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "PancSynergy_AI_Presentation.pptx")
    prs.save(output_path)
    print(f"Presentation saved successfully to: {output_path}")

if __name__ == "__main__":
    build_presentation()
