# prostate_breast_cancer_context.py
"""
Prostate and Breast Cancer Clinical Context for Report Analysis
Specialized context for the Advanced Oncology Clinical Assistant
"""
from context import init_conversation as REPORT_ANALYSIS_SYSTEM

PROSTATE_CANCER_CONTEXT = """
════════════════════════════════════════════
PROSTATE CANCER - CLINICAL REFERENCE
════════════════════════════════════════════

EPIDEMIOLOGY & RISK FACTORS:
- Most common non-skin cancer in men
- Risk increases with age (rare < 40, common > 65)
- Family history: BRCA1/2, HOXB13 mutations, Lynch syndrome
- African ancestry: 2-3x higher risk and mortality
- Diet, obesity, smoking (modest associations)

SCREENING & EARLY DETECTION:
- PSA (Prostate Specific Antigen): Normal < 4.0 ng/mL
  - Gray zone: 4-10 ng/mL (25-30% cancer risk)
  - Elevated: >10 ng/mL (>50% cancer risk)
- Digital Rectal Exam (DRE): Asymmetry, nodularity, induration
- PSA density, PSA velocity, free PSA ratio
- Risk calculators: PCPT, ERSPC

DIAGNOSTIC WORKUP:
1. Confirmatory PSA (repeat if elevated)
2. Multiparametric MRI (PI-RADS score 1-5)
   - PI-RADS 1-2: Low risk, consider surveillance
   - PI-RADS 3: Equivocal, case-dependent
   - PI-RADS 4-5: High risk, target biopsy
3. MRI/TRUS fusion biopsy (12-24 cores)
4. Systematic plus targeted sampling

HISTOPATHOLOGY - GLEASON GRADING (2019 ISUP):
Primary grade (most common pattern): 1-5
Secondary grade (second most common): 1-5

Gleason Score = Primary + Secondary (e.g., 3+4=7)

Grade Groups (GG):
- GG 1: Gleason ≤6 (low risk)
- GG 2: Gleason 3+4=7 (favorable intermediate)
- GG 3: Gleason 4+3=7 (unfavorable intermediate)
- GG 4: Gleason 4+4=8 (high risk)
- GG 5: Gleason 9-10 (very high risk)

INTRADUCTAL CARCINOMA (IDC): Aggressive variant, upstages disease
CRIBRIFORM PATTERN: Associated with worse prognosis

IHC MARKERS:
- AMACR (P504S): Positive in 95% of prostate cancer (cytoplasmic)
- p63: Basal cell marker (NEGATIVE in invasive cancer)
- CK5/6: Basal cell marker (NEGATIVE in invasive cancer)
- CK8/18: Luminal marker (POSITIVE in adenocarcinoma)
- PSA: Positive in differentiated tumors
- PSMA: Positive (theragnostic target)
- ERG: Fusions in 50% (TMPRSS2-ERG)
- PTEN: Loss = worse prognosis
- p53: Abnormal expression = aggressive
- Ki-67: Proliferation index (>10% aggressive)
- AR (Androgen Receptor): Positive, target for hormonal therapy

MOLECULAR MARKERS:
- Decipher, Prolaris, Oncotype DX GPS (prognostic)
- BRCA1/2, ATM, PALB2 mutations (aggressive, PARP inhibitor eligible)
- MSI-H/dMMR (rare, immunotherapy eligible)
- SPOP, FOXA1 (mutations)

STAGING (AJCC 8th Edition - Clinical & Pathologic):
T Stage - Primary Tumor:
- TX: Cannot assess
- T0: No evidence
- T1: Clinically inapparent (not palpable/visible)
  - T1a: Incidental <5% tissue
  - T1b: Incidental >5% tissue
  - T1c: Needle biopsy (elevated PSA)
- T2: Confined to prostate
  - T2a: ≤50% one lobe
  - T2b: >50% one lobe
  - T2c: Both lobes
- T3: Extraprostatic extension
  - T3a: EPE unilateral/bilateral
  - T3b: Seminal vesicle invasion
- T4: Fixed/invades adjacent structures (bladder, rectum, pelvic wall)

N Stage - Regional Lymph Nodes:
- NX: Cannot assess
- N0: No nodal mets
- N1: Regional node metastasis (obturator, internal/external iliac)

M Stage - Distant Metastasis:
- M0: No distant mets
- M1a: Non-regional lymph nodes
- M1b: Bone(s) (osteoblastic lesions common)
- M1c: Other sites (lung, liver, brain)

RISK STRATIFICATION (NCCN):
Low Risk: T1-T2a, GG1, PSA <10
Favorable Intermediate: T2b-T2c, GG2 (3+4=7), PSA 10-20
Unfavorable Intermediate: T2b-T2c, GG3 (4+3=7), PSA 10-20, or multiple intermediate
High Risk: T3a, GG4, PSA >20
Very High Risk: T3b-T4, GG5 (9-10), or high-risk with multiple features

TREATMENT LANDSCAPE (Conceptual - Non-prescriptive):
- Active Surveillance: Very low/low risk, PSA monitoring, re-biopsy
- Radical Prostatectomy: Robotic/open (nerve-sparing when appropriate)
- Radiation: EBRT (IMRT, SBRT) or Brachytherapy (LDR/HDR)
- Androgen Deprivation Therapy: LHRH agonists/antagonists (relugolix, degarelix)
- Next-gen hormonal agents: Abiraterone, enzalutamide, apalutamide, darolutamide
- Chemotherapy: Docetaxel (castration-sensitive/resistant), cabazitaxel (post-docetaxel)
- Bone-targeting: Denosumab, zoledronic acid (prevent SREs)
- Radium-223: Bone metastases, no visceral disease
- PARP inhibitors: Olaparib, rucaparib (BRCA1/2, ATM, PALB2)
- Immunotherapy: Sipuleucel-T (asymptomatic/mildly symptomatic mCRPC)
- PSMA PET-CT: Restaging, theragnostic (Lu-177 PSMA)

SIDE EFFECTS (Educational):
- Surgery: Erectile dysfunction, urinary incontinence
- Radiation: Proctitis, cystitis, erectile dysfunction
- ADT: Hot flashes, fatigue, osteoporosis, metabolic syndrome
- Chemotherapy: Neutropenia, neuropathy, alopecia

RED FLAGS:
- Acute urinary retention (obstruction)
- Pathologic fracture (bone mets)
- Spinal cord compression (back pain + neurologic deficits)
- Hydronephrosis (bilateral obstruction)
- Disseminated intravascular coagulation (advanced)

CLINICAL NOTE:
Prostate cancer exhibits wide biological heterogeneity from indolent to aggressive. Treatment decisions integrate PSA, Gleason Grade Group, stage, patient age, life expectancy, and quality-of-life preferences. Genomic testing aids risk stratification. PSMA PET-CT has revolutionized staging and theragnostics.
"""

BREAST_CANCER_CONTEXT = """
════════════════════════════════════════════
BREAST CANCER - CLINICAL REFERENCE
════════════════════════════════════════════

EPIDEMIOLOGY & RISK FACTORS:
- Most common cancer in women worldwide
- Age: Peak 60-70 years, but can occur in 20s-30s
- Genetic: BRCA1/2, PALB2, CHEK2, ATM, PTEN (Cowden), TP53 (Li-Fraumeni)
- Hormonal: Early menarche, late menopause, nulliparity, late first pregnancy
- Lifestyle: Alcohol, obesity, physical inactivity, hormone replacement therapy
- History: Prior breast cancer, atypical hyperplasia, LCIS

SCREENING & EARLY DETECTION:
- Mammography: Every 1-2 years starting age 40-50 (guideline dependent)
- Tomosynthesis (3D mammography): Higher sensitivity, fewer recalls
- Breast ultrasound: Dense breasts, palpable abnormalities, cystic vs solid
- Breast MRI: High-risk patients (BRCA, strong family history, lobular histology)
- Clinical breast exam (CBE): Every 1-3 years
- BIRADS Assessment Categories 0-6
  - BIRADS 1-2: Negative/Benign (routine screening)
  - BIRADS 3: Probably benign (<2% malignancy, short interval follow-up)
  - BIRADS 4A: Low suspicion (2-10%)
  - BIRADS 4B: Moderate suspicion (10-50%)
  - BIRADS 4C: High suspicion (50-95%)
  - BIRADS 5: Highly suggestive (>95%)
  - BIRADS 6: Known biopsy-proven cancer

DIAGNOSTIC WORKUP:
1. Diagnostic mammogram + targeted ultrasound
2. Core needle biopsy (preferred over FNA): 14-gauge, multiple samples
3. Vacuum-assisted biopsy for microcalcifications
4. MRI-guided biopsy for MRI-only lesions
5. Clip placement for biopsy site marking
6. Lymph node sampling: FNA/US of suspicious nodes, sentinel lymph node biopsy

HISTOPATHOLOGY - TUMOR TYPES:
Ductal Carcinoma In Situ (DCIS):
- Grade: Low, intermediate, high
- Necrosis: Comedo (central), punctate
- Architecture: Cribriform, solid, micropapillary, papillary

Invasive Ductal Carcinoma (IDC, NST): 70-80%
- Grade: Nuclear pleomorphism, tubule formation, mitotic count (1-3; sum 3-9)
- Nottingham grade: I (3-5), II (6-7), III (8-9)
- Features: Desmoplastic stroma, lymphovascular invasion

Invasive Lobular Carcinoma (ILC): 10-15%
- E-cadherin NEGATIVE (diagnostic)
- Single-file infiltration, targetoid pattern
- Often bilateral/multicentric
- Subtle mammographic findings

Special Subtypes:
- Tubular: >90% tubule formation, excellent prognosis
- Mucinous (Colloid): Abundant extracellular mucin, good prognosis
- Medullary: Pushing borders, lymphocytic infiltrate, syncytial growth
- Micropapillary: Aggressive, high nodal involvement
- Metaplastic: Heterologous elements (squamous, sarcomatoid)
- Apocrine: AR positive, often triple negative but distinct
- Papillary: Intraductal or encapsulated, favorable

IHC MARKERS - DIAGNOSTIC:
- GATA3: Highly sensitive/specific for breast origin (90-95%)
- CK7: Positive in breast, lung, ovary
- CK20: Usually negative in breast
- ER (Estrogen Receptor): Nuclear stain, ≥1% positive
- PR (Progesterone Receptor): Nuclear stain, ≥1% positive
- HER2/neu (ERBB2):
  - IHC: 0, 1+ (negative), 2+ (equivocal → FISH), 3+ (positive)
  - FISH: Ratio >2.0 or copy number >6 → amplified
- Ki-67/MIB1: Proliferation index (cutoffs vary: low <10-14%, intermediate, high >20-30%)
- E-cadherin: Membrane staining, LOST in ILC, positive in IDC
- p120 catenin: Diffuse cytoplasmic in ILC (vs membrane in IDC)
- p63, CK5/6: Myoepithelial markers (present in DCIS, absent in invasion)

MOLECULAR SUBTYPES (Based on IHC/proxies):
Luminal A (ER+, PR+, HER2-, Ki-67 <14-20%):
- Most common, best prognosis
- Endocrine therapy responsive
- Chemotherapy benefit low (low grade tumors)

Luminal B (ER+, HER2- with high Ki-67 OR HER2+):
- Higher grade, worse prognosis than Luminal A
- Chemotherapy + endocrine therapy
- HER2+ version: Add anti-HER2 therapy

HER2-Enriched (ER-/PR-/HER2+, or high HER2 by IHC/FISH):
- Aggressive, but targetable
- Trastuzumab, pertuzumab, T-DM1, T-DXd
- Chemotherapy + dual HER2 blockade

Triple Negative (ER-/PR-/HER2-):
- 15-20% of breast cancers
- Aggressive, peaks early, visceral predilection
- Chemotherapy sensitive (neoadjuvant)
- PARP inhibitors (BRCA1/2)
- Immunotherapy (PD-L1+: pembrolizumab)
- New agents: Sacituzumab govitecan (Trop-2)

Normal-Like: Rare, gene expression resembles adipose

ADJUNCTIVE MOLECULAR TESTS:
- Oncotype DX (21-gene): Recurrence score (RS)
  - RS <18: Endocrine therapy alone (TAILORx)
  - RS 18-25: Clinically dependent
  - RS 26-100: Chemotherapy benefit
- MammaPrint (70-gene): Low/high risk
- Prosigna/PAM50: Intrinsic subtype assignment
- EndoPredict: 11-gene, endocrine sensitivity
- FoundationOne/CDx: Comprehensive genomic profiling

STAGING (AJCC 8th - Anatomic + Prognostic):
T Stage - Primary Tumor:
- TX: Primary cannot be assessed
- T0: No evidence
- Tis: DCIS or Paget's without invasion
- T1: ≤2.0 cm
  - T1mi: ≤0.1 cm
  - T1a: >0.1-0.5 cm
  - T1b: >0.5-1.0 cm
  - T1c: >1.0-2.0 cm
- T2: 2.0-5.0 cm
- T3: >5.0 cm
- T4: Chest wall/skin invasion
  - T4a: Chest wall (not pectoralis alone)
  - T4b: Edema/ulceration/satellite nodules
  - T4c: Both T4a+T4b
  - T4d: Inflammatory carcinoma

N Stage - Regional Lymph Nodes:
- N0: No nodal mets
- N1: Micromets or 1-3 axillary nodes
  - N1mi: Micrometastasis >0.2mm ≤2mm
  - N1a: 1-3 axillary nodes
  - N1b: Internal mammary nodes (clinically detected)
  - N1c: Both N1a+N1b
- N2: 4-9 axillary nodes or internal mammary
- N3: ≥10 axillary nodes, infra/supraclavicular

M Stage:
- M0: No distant mets
- M1: Distant metastasis (bone, lung, liver, brain, etc.)

STAGE GROUPS (Anatomic, simplified):
Stage 0: Tis N0
Stage I: T1 N0
Stage IIA: T0-1 N1 OR T2 N0
Stage IIB: T2 N1 OR T3 N0
Stage IIIA: T0-2 N2 OR T3 N1-2
Stage IIIB: T4 N0-2
Stage IIIC: Any T N3
Stage IV: Any T Any N M1

TREATMENT PRINCIPLES (Conceptual - Non-prescriptive):
Local Therapy:
- Breast-conserving surgery (lumpectomy) + radiation
- Mastectomy (simple, skin-sparing, nipple-sparing)
- Sentinel lymph node biopsy (blue dye + radiotracer)
- Axillary dissection (if node positive/confirmed)

Radiation Therapy:
- Whole breast (WBRT): 40-50 Gy in 15-25 fractions
- Hypofractionated: Shorter course (3-4 weeks)
- Partial breast (APBI): Selected low-risk patients
- Chest wall (post-mastectomy) + regional nodes
- Boost to tumor bed (lumpectomy cavity)

Systemic Therapy:
Endocrine Therapy (ER+):
- Tamoxifen (premenopausal, any stage)
- Aromatase inhibitors: Letrozole, anastrozole, exemestane (postmenopausal)
- Ovarian suppression/ablation (premenopausal high risk)
- Duration: 5-10 years (extended therapy)
- CDK4/6 inhibitors: Palbociclib, ribociclib, abemaciclib (advanced/metastatic)

Chemotherapy:
- Neoadjuvant: Downstage, assess response, pCR predictor
- Adjuvant: High-risk features (young, high grade, node+, triple negative)
- Regimens: AC-T (doxorubicin, cyclophosphamide, paclitaxel/docetaxel)
- TC (docetaxel, cyclophosphamide) for HER2- low risk
- Platinum (carboplatin) in triple negative/BRCA

Anti-HER2 Therapy:
- Trastuzumab (Herceptin): Monoclonal antibody
- Pertuzumab (Perjeta): Dimerization inhibitor
- T-DM1 (Kadcyla): Antibody-drug conjugate (residual disease after neoadjuvant)
- T-DXd (Enhertu): Superior in HER2-low and refractory
- Neratinib: TKI (extended adjuvant after trastuzumab)

Immunotherapy:
- Pembrolizumab (Keytruda): PD-1 inhibitor
  - High-risk early triple negative (neoadjuvant + adjuvant)
  - PD-L1+ metastatic triple negative (CPS ≥10)
- Atezolizumab (Tecentriq): PD-L1 inhibitor (withdrawn for breast)

PARP Inhibitors:
- Olaparib (Lynparza): BRCA1/2+, high-risk HER2- (adjuvant, metastatic)
- Talazoparib (Talzenna): BRCA1/2+ metastatic

SIDE EFFECTS (Educational):
- Surgery: Lymphedema, seroma, range of motion restriction
- Radiation: Skin reaction, fatigue, pneumonitis, cardiac (left breast)
- Endocrine therapy: Hot flashes, arthralgias, endometrial cancer risk (tamoxifen), bone loss (AIs)
- Chemotherapy: Myelosuppression, nausea, neuropathy, cardiotoxicity (anthracyclines)
- Anti-HER2: Cardiotoxicity (LVEF monitoring required)
- CDK4/6: Neutropenia, fatigue, diarrhea (abemaciclib)
- PARP inhibitors: Fatigue, nausea, anemia
- Immunotherapy: Pneumonitis, colitis, hepatitis, endocrinopathies

RED FLAGS (Require urgent evaluation):
- Inflammatory breast cancer features: Erythema, edema (peau d'orange), warmth - do NOT delay biopsy
- Spinal cord compression (back pain, neurologic deficits, history of bone mets)
- Superior vena cava syndrome (facial/upper extremity swelling, dyspnea)
- Leptomeningeal disease (headaches, cranial neuropathies, radiculopathy)
- Hypercalcemia (bone mets): Nausea, confusion, polyuria, constipation
- Pathologic fracture (bone mets, bisphosphonate/denosumab patients - jaw pain)

CLINICAL NOTE:
Breast cancer treatment is driven by tumor biology (ER/PR/HER2/Ki-67), stage, and patient factors. Neoadjuvant therapy provides in vivo chemosensitivity testing and prognostic information (pCR predicts improved EFS especially in aggressive subtypes). Genomic assays guide chemotherapy decisions in early-stage HR+/HER2- disease. Metastatic disease is treated as chronic illness with sequential therapies; median survival has improved significantly with targeted agents. Regular surveillance for recurrence is recommended with history, exam, and mammography (no routine labs/imaging for asymptomatic patients).
"""

COMMON_ABBREVIATIONS = """
════════════════════════════════════════════
ONCOLOGY ABBREVIATIONS REFERENCE
════════════════════════════════════════════

PROSTATE CANCER:
PSA - Prostate Specific Antigen
DRE - Digital Rectal Exam
mpMRI - Multiparametric Magnetic Resonance Imaging
PI-RADS - Prostate Imaging Reporting and Data System
TRUS - Transrectal Ultrasound
GG - Grade Group
IDC - Intraductal Carcinoma
SVI - Seminal Vesicle Invasion
EPE - Extraprostatic Extension
LN - Lymph Node
ADT - Androgen Deprivation Therapy
CRPC - Castration-Resistant Prostate Cancer
CSPC - Castration-Sensitive Prostate Cancer
mHSPC - Metastatic Hormone-Sensitive Prostate Cancer
mCRPC - Metastatic Castration-Resistant Prostate Cancer
SRE - Skeletal-Related Event
LHRH - Luteinizing Hormone-Releasing Hormone
EBRT - External Beam Radiation Therapy
SBRT - Stereotactic Body Radiation Therapy
LDR/HDR - Low/High Dose Rate (brachytherapy)
PSMA - Prostate Specific Membrane Antigen
PARP - Poly (ADP-Ribose) Polymerase
MSI-H - Microsatellite Instability-High
dMMR - Mismatch Repair Deficient
HRR - Homologous Recombination Repair

BREAST CANCER:
ER - Estrogen Receptor
PR - Progesterone Receptor
HER2 - Human Epidermal Growth Factor Receptor 2
IHC - Immunohistochemistry
FISH - Fluorescence In Situ Hybridization
DCIS - Ductal Carcinoma In Situ
LCIS - Lobular Carcinoma In Situ
IDC - Invasive Ductal Carcinoma
ILC - Invasive Lobular Carcinoma
NST - No Special Type
LVI - Lymphovascular Invasion
SNB - Sentinel Node Biopsy
ALND - Axillary Lymph Node Dissection
BIRADS - Breast Imaging Reporting and Data System
BCT - Breast-Conserving Therapy
BCS - Breast-Conserving Surgery (lumpectomy)
WBRT - Whole Breast Radiation Therapy
APBI - Accelerated Partial Breast Irradiation
pCR - Pathologic Complete Response
ER+ - Estrogen Receptor Positive
TNBC - Triple Negative Breast Cancer
HR+ - Hormone Receptor Positive
AI - Aromatase Inhibitor
CDK4/6 - Cyclin-Dependent Kinase 4/6
ADC - Antibody-Drug Conjugate
T-DM1 - Trastuzumab Emtansine
T-DXd - Trastuzumab Deruxtecan
CPS - Combined Positive Score (PD-L1)
DFS - Disease-Free Survival
EFS - Event-Free Survival
OS - Overall Survival
NACT - Neoadjuvant Chemotherapy
ADJ - Adjuvant Therapy

GENERAL ONCOLOGY:
AJCC - American Joint Committee on Cancer
TNM - Tumor Node Metastasis
IHC - Immunohistochemistry
FISH - Fluorescence In Situ Hybridization
NGS - Next-Generation Sequencing
PCR - Polymerase Chain Reaction
CT - Computed Tomography
MRI - Magnetic Resonance Imaging
PET - Positron Emission Tomography
MDT - Multidisciplinary Team
ECOG - Eastern Cooperative Oncology Group (performance status)
PS - Performance Status
AE - Adverse Event
SAE - Serious Adverse Event
IRB - Institutional Review Board
IND - Investigational New Drug
"""

# Function to combine contexts for report analysis
def get_prostate_context() -> str:
    """Returns combined prostate cancer context and abbreviations."""
    return f"{PROSTATE_CANCER_CONTEXT}\n\n{COMMON_ABBREVIATIONS}"

def get_breast_context() -> str:
    """Returns combined breast cancer context and abbreviations."""
    return f"{BREAST_CANCER_CONTEXT}\n\n{COMMON_ABBREVIATIONS}"

def get_full_context() -> str:
    """Returns all contexts combined."""
    return f"{PROSTATE_CANCER_CONTEXT}\n\n{BREAST_CANCER_CONTEXT}\n\n{COMMON_ABBREVIATIONS}"

# Example clinical report templates for testing
EXAMPLE_PROSTATE_REPORT = """
HISTOPATHOLOGY REPORT
Patient: 72-year-old male
Specimen: MRI/TRUS fusion biopsy, right peripheral zone
Clinical indication: PSA 12.4 ng/mL, PI-RADS 4 lesion

GROSS DESCRIPTION:
Six core biopsies received, labeled R1-R6. Core R3 measures 1.8 cm, firm, white-tan.

MICROSCOPIC DESCRIPTION:
Core R3 shows prostatic adenocarcinoma involving 80% of core length.
Gleason pattern: 4 (cribriform) + 3 = 7.
Perineural invasion identified. No lymphovascular invasion seen.
Remaining cores show benign prostatic tissue with chronic inflammation.

IMMUNOHISTOCHEMISTRY:
AMACR: Positive (cytoplasmic, strong)
p63: Negative in tumor glands (basal cell loss)
CK5/6: Negative
PSA: Positive

DIAGNOSIS:
Prostatic adenocarcinoma, Grade Group 2 (Gleason 3+4=7)
Involving 1 of 6 cores
Perineural invasion present

COMMENT:
Cribriform morphology (Gleason pattern 4) is associated with adverse pathology at prostatectomy. Clinical correlation recommended.
"""

EXAMPLE_BREAST_REPORT = """
HISTOPATHOLOGY REPORT
Patient: 54-year-old female
Specimen: Ultrasound-guided core needle biopsy, left breast 2 o'clock, 3 cm from nipple
Clinical indication: Palpable mass, BIRADS 4C

GROSS DESCRIPTION:
Four core biopsies received, aggregate 2.5 cm. Specimen placed in formalin.

MICROSCOPIC DESCRIPTION:
Invasive carcinoma with solid and cribriform architecture.
Tumor cells show moderate nuclear pleomorphism, increased mitotic activity (3/10 HPF).
Lymphovascular invasion not identified.
Background breast tissue shows fibrocystic changes.

IMMUNOHISTOCHEMISTRY:
ER: Positive, 95% strong nuclear staining
PR: Positive, 80% moderate nuclear staining
HER2/neu: 2+ (equivocal) → pending FISH
Ki-67: 25% nuclear staining
E-cadherin: Positive, membrane staining (intact)
CK7: Positive
GATA3: Positive

DIAGNOSIS:
Invasive ductal carcinoma, Nottingham Grade 2 (7/9)
ER positive, PR positive, HER2 equivocal

COMMENT:
HER2 FISH ordered for amplification status. Clinical correlation and surgical consultation recommended.
"""

# Utility function to generate report analysis system prompt with context
def get_contextualized_report_system(cancer_type: str = "full") -> str:
    """
    Returns the report analysis system prompt with disease-specific context.

    Args:
        cancer_type: One of "prostate", "breast", or "full"

    Returns:
        Enhanced system prompt with clinical context
    """
    if cancer_type == "prostate":
        context = get_prostate_context()
    elif cancer_type == "breast":
        context = get_breast_context()
    else:
        context = get_full_context()

    return f"""{REPORT_ANALYSIS_SYSTEM}

CLINICAL CONTEXT FOR REFERENCE:
{context}

When interpreting reports, apply this disease-specific knowledge. Use the staging, grading, and IHC interpretation guidelines provided above."""