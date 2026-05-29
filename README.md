<div align="center">

<img src="https://capsule-render.vercel.app/api?type=rect&color=0:0a0f1e,50:0d1829,100:0a0f1e&height=200&section=header&text=TAMILNADU%20ELECTIONS%20DECODED&fontSize=36&fontColor=e2e8f0&fontAlignY=42&desc=2021%20vs%202026%20%7C%208%2C489%20Candidates%20%7C%20234%20Constituencies%20%7C%20AtliQ%20Media&descSize=13&descAlignY=66&descColor=f97316&animation=fadeIn" width="100%"/>

<br/>

<img src="https://readme-typing-svg.demolab.com?font=JetBrains+Mono&weight=600&size=16&duration=2400&pause=900&color=F97316&center=true&vCenter=true&width=780&height=40&lines=8%2C489+candidate+rows+ingested+%E2%80%94+two+CSVs%2C+one+pipeline;85.10%25+turnout+in+2026+%E2%80%94+record+high%2C+%2B12.06+pp+swing;234+constituencies+decoded+across+6+regions;Seat+flips+tracked+%E2%80%94+volatility+index+built;Board-ready+exec+deck%2C+zero+manual+formatting" alt="Typing SVG"/>

<br/><br/>

![Python](https://img.shields.io/badge/Python-3.10%2B-0f172a?style=for-the-badge&logo=python&logoColor=f97316&labelColor=0f172a)
![Pandas](https://img.shields.io/badge/Pandas-2.x-0f172a?style=for-the-badge&logo=pandas&logoColor=f97316&labelColor=0f172a)
![NumPy](https://img.shields.io/badge/NumPy-1.26-0f172a?style=for-the-badge&logo=numpy&logoColor=f97316&labelColor=0f172a)
![Plotly](https://img.shields.io/badge/Plotly-5.x-0f172a?style=for-the-badge&logo=plotly&logoColor=f97316&labelColor=0f172a)
![Streamlit](https://img.shields.io/badge/Streamlit-1.x-0f172a?style=for-the-badge&logo=streamlit&logoColor=f97316&labelColor=0f172a)
![python-pptx](https://img.shields.io/badge/python--pptx-0.6-0f172a?style=for-the-badge&logo=microsoftpowerpoint&logoColor=f97316&labelColor=0f172a)
![License](https://img.shields.io/badge/License-MIT-0f172a?style=for-the-badge&logoColor=f97316&labelColor=0f172a)

</div>

<br/>

[![-----------------------------------------------------](https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/colored.png)](#overview)

## Overview

```python
project = {
    "client"   : "AtliQ Media — Election TV Show Producer",
    "domain"   : "Tamil Nadu Legislative Assembly Elections",
    "dataset"  : ["tn_2021_results.csv", "tn_2026_results.csv", "constituency_master.csv"],
    "rows"     : {"2021": 4_232, "2026": 4_257, "total": 8_489},
    "stack"    : ["Python", "Pandas", "NumPy", "Plotly", "Streamlit", "python-pptx", "Matplotlib"],
    "pipeline" : ["Ingestion", "Cleaning", "Party Standardisation", "Winner Extraction",
                  "Flip Detection", "Streamlit Dashboard", "Widescreen PowerPoint & PDF Decks", "Swing Classifier"],
    "scope"    : {
        "constituencies" : 234,
        "regions"        : 6,   # Chennai Metro, North, Central, Kongu, Delta, South
        "parties_tracked": 13,
        "turnout_swing"  : "+12.06 pp  (73.04% → 85.10%)",
    }
}
```

Most election analytics stop at seat tallies. This pipeline goes further — cross-election swing analysis, region-level volatility scoring, constituency flip detection, and auto-generated widescreen decks purpose-built for AtliQ Media's live TV broadcast. All from two CSVs and a master table.

<br/>

[![-----------------------------------------------------](https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/colored.png)](#findings)

## Key Findings

<div align="center">

| Metric | Stat | Significance |
|:---|:---:|:---|
| Statewide turnout 2026 | **85.10%** | Record high — up from 73.04% in 2021 |
| Turnout swing | **+12.06 pp** | Driven by ECI Special Intensive Revision (SIR) shrunken base |
| Total constituencies | **234** | 188 GEN · 44 SC · 2 ST |
| Candidate rows ingested | **8,489** | 4,232 (2021) + 4,257 (2026) |
| Regions decoded | **6** | Chennai Metro, North, Central, Kongu, Delta, South |
| Parties tracked | **13+** | DMK, AIADMK, TVK, INC, BJP, PMK, VCK, NTK, CPI, CPIM … |
| Volatility / Flip Index | **163 / 234** | An unprecedented **69.7% Volatility Index** across seats |
| Executive decks | **auto-generated** | PowerPoint widescreen (.pptx) + print-ready PDF ready for broadcast |

</div>

<br/>

[![-----------------------------------------------------](https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/colored.png)](#pipeline)

## Pipeline

```
  tn_2021_results.csv       tn_2026_results.csv       constituency_master.csv
  (4,232 rows × 8 cols)     (4,257 rows × 8 cols)     (234 rows × 5 cols)
          │                         │                          │
          └─────────────────────────┴──────────────────────────┘
                                    │
                                    ▼
┌───────────────────────────────────────────────────────────────┐
│  STEP 1 — INGESTION & CLEANING (data_pipeline.py)            │
│  Strip whitespace · Standardise 13+ party name variants       │
│  Merge with constituency_master on ac_number (primary key)    │
│  Analyze official 2026 ECI turnout vs 2021 baseline           │
└──────────────────────────┬────────────────────────────────────┘
                           │
                           ▼
┌───────────────────────────────────────────────────────────────┐
│  STEP 2 — WINNER EXTRACTION & FLIP DETECTION                  │
│  idxmax(votes) per constituency → winners_2021 / winners_2026 │
│  Merge on ac_number · flag is_flip where party changed        │
│  Compute volatility index across all 234 seats                │
└──────────────────────────┬────────────────────────────────────┘
                           │
                           ▼
┌───────────────────────────────────────────────────────────────┐
│  STEP 3 — PROCESSED OUTPUTS                                   │
│  cleaned_results_2021.csv · cleaned_results_2026.csv          │
│  constituency_winners_and_flips.csv · summary_metrics.txt     │
└──────────────────────────┬────────────────────────────────────┘
                           │
                           ▼
┌───────────────────────────────────────────────────────────────┐
│  STEP 4 — INTERACTIVE STREAMLIT DASHBOARD (dashboard.py)      │
│  Streamlit app · Party seat share · Swing analysis            │
│  Const-level flip explorer · Transparent map + finger watermarks│
│  Custom broadcast-grade dark UI styling with responsive grids │
└──────────────────────────┬────────────────────────────────────┘
                           │
                           ▼
┌───────────────────────────────────────────────────────────────┐
│  STEP 5 — AUTO EXECUTIVE DECK PPTX & PDF GENERATION           │
│  generate_deck_pptx.py / generate_deck_pdf.py                 │
│  python-pptx & matplotlib dark-theme decks · Charts + insights │
│  AtliQ Media broadcast-ready · Zero manual formatting         │
└──────────────────────────┬────────────────────────────────────┘
                           │
                           ▼
┌───────────────────────────────────────────────────────────────┐
│  STEP 6 — SWING SEAT CLASSIFIER (swing_seat_classifier.py)    │
│  Pure Python Logistic Regression model via Gradient Descent   │
│  Predicts flip probability per seat using margins + turnout   │
│  Saves predictions to data/processed/swing_predictions.csv    │
└───────────────────────────────────────────────────────────────┘
```

<br/>

[![-----------------------------------------------------](https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/colored.png)](#features)

## Features

<div align="center">

| Module | What it does |
|:---|:---|
| `data_pipeline.py` | Full ingestion → cleaning → party standardisation → winner extraction → flip detection → CSV outputs |
| `dashboard.py` | Interactive Streamlit app — seat share, swing maps, transparent watermarks, flip explorer |
| `generate_deck_pptx.py` | Auto-builds dark-theme widescreen executive `.pptx` deck with Matplotlib charts and strategic insights |
| `generate_deck_pdf.py` | Auto-builds dark-theme print-ready executive `.pdf` deck with Matplotlib and standalone graphics |
| `swing_seat_classifier.py` | Pure NumPy/Pandas logistic regression swing classifier running gradient descent to predict flips |
| `atliq_media_election_deck.pptx` | Generated widescreen broadcast deck ready for AtliQ Media TV show distribution |
| `atliq_media_election_deck.pdf` | Generated print-ready broadcast deck ready for AtliQ Media TV show distribution |
| `tamil_nadu_map.png` | TN constituency map used for background Geo watermark overlays |
| `voting_finger.png` | Transparent voting finger logo used inside sidebar and background watermarks |
| `data/` | Raw CSVs — `tn_2021_results.csv`, `tn_2026_results.csv`, `constituency_master.csv` |

</div>

<br/>

[![-----------------------------------------------------](https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/colored.png)](#data)

## Data Schema

```
tn_2021_results.csv  /  tn_2026_results.csv
──────────────────────────────────────────────────────────────
  ac_number     INT     Primary key — official ECI AC number (1–234)
  constituency  STR     Assembly constituency name
  candidate     STR     Candidate name as per ECI records
  party         STR     Raw party name → standardised in pipeline
  votes         INT     Total votes received
  turnout       FLOAT   Constituency-level voter turnout %
  reserved      STR     GEN | SC | ST  (188 / 44 / 2)
  region        STR     Chennai Metro | North | Central | Kongu | Delta | South

constituency_master.csv
──────────────────────────────────────────────────────────────
  ac_number     INT     Join key
  constituency  STR     AC name
  district      STR     Administrative district
  region        STR     Six-region editorial grouping
  reserved      STR     GEN | SC | ST
```

> **Sources:** 2021 data cleaned from Trivedi Centre for Political Data (Ashoka University) via ECI. 2026 data sourced from ECI live results portal `results.eci.gov.in`.

<br/>

[![-----------------------------------------------------](https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/colored.png)](#start)

## Getting Started

**1. Clone**
```bash
git clone https://github.com/lakshyaverma2004/TamilNadu-elections-decoded.git
cd TamilNadu-elections-decoded
```

**2. Create virtual environment**
```bash
python -m venv .venv
source .venv/bin/activate        # macOS / Linux
.venv\Scripts\activate           # Windows
```

**3. Install dependencies**
```bash
pip install pandas numpy plotly streamlit python-pptx matplotlib
```

> Ensure the `data/` folder contains all three CSVs before running.

<br/>

[![-----------------------------------------------------](https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/colored.png)](#usage)

## Usage

**Run the data pipeline**
```bash
python data_pipeline.py
```

**Train the swing seat classifier**
```bash
python swing_seat_classifier.py
```

**Launch the interactive dashboard**
```bash
python -m streamlit run dashboard.py
# Open http://localhost:8501 in your browser
```

**Generate the executive decks**
```bash
# Compile PowerPoint PPTX
python generate_deck_pptx.py

# Compile Print-Ready PDF
python generate_deck_pdf.py
```

**Expected pipeline output**
```
══════════════════════════════════════════════════════════════
STEP 1: DATA INGESTION & CLEANING
══════════════════════════════════════════════════════════════
2021 dataset loaded : 4,232 rows × 8 columns
2026 dataset loaded : 4,257 rows × 8 columns
Master table loaded :   234 rows × 5 columns
Party variants standardised: 13 mappings applied

══════════════════════════════════════════════════════════════
STEP 2: WINNER EXTRACTION & FLIP DETECTION
══════════════════════════════════════════════════════════════
Winners extracted  — 2021 : 234 constituencies
Winners extracted  — 2026 : 234 constituencies
Seat flips detected        : 163 of 234  (69.7%)

══════════════════════════════════════════════════════════════
STEP 3: SUMMARY METRICS
══════════════════════════════════════════════════════════════
2026 Statewide Turnout : 85.10%  (Record High vs 73.04% in 2021)
Volatility Index       : 163 seats changed hands
Outputs saved to       : data/processed/
```

<br/>

[![-----------------------------------------------------](https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/colored.png)](#structure)

## Project Structure

```
TamilNadu-elections-decoded/
│
├── data_pipeline.py            Ingestion · cleaning · party std · flip detection · CSV outputs
├── dashboard.py                Streamlit dashboard app — seat share, swing, relative watermarks
├── generate_deck_pptx.py       Auto-generates widescreen PowerPoint executive deck
├── generate_deck_pdf.py        Auto-generates widescreen print-ready PDF presentation
├── swing_seat_classifier.py    Logistic regression swing classifier using pure numpy/pandas
├── atliq_media_election_deck.pptx  Widescreen broadcast-ready slide presentation
├── atliq_media_election_deck.pdf   Print-ready broadcast-ready presentation deck
├── tamil_nadu_map.png          TN constituency watermark map
├── voting_finger.png           Transparent voting finger logo
├── pitch_script.md             Presenter script for AtliQ Media TV segment
├── stakeholder_deck_outline.md Structured slide-by-slide deck outline
├── metadata.txt                Column descriptions and data source documentation
│
└── data/
    ├── tn_2021_results.csv         4,232 candidate rows · 234 constituencies
    ├── tn_2026_results.csv         4,257 candidate rows · 234 constituencies
    └── constituency_master.csv     234 ACs · district + region + reservation mapping
        └── processed/              Pipeline processed outputs (auto-created)
            ├── cleaned_results_2021.csv
            ├── cleaned_results_2026.csv
            ├── constituency_winners_and_flips.csv
            ├── swing_predictions.csv
            └── summary_metrics.txt
```

<br/>

[![-----------------------------------------------------](https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/colored.png)](#impact)

## Impact

<div align="center">

| Outcome | Result |
|:---|:---:|
| Elections decoded — both cycles fully merged | **234 × 2** |
| Turnout swing surfaced | **+12.06 pp** |
| Party name variants standardised | **13 mappings** |
| Manual deck formatting hours | **0 hrs** |

</div>

```
  Turnout swing quantified    ████████████████████  85.10% — record high
  Constituencies covered      ████████████████████  234 / 234 (100%)
  Party variants resolved     ████████████████░░░░  13 standardised
  Auto deck — manual hrs      ████████████████████  0 hrs
```

<br/>

[![-----------------------------------------------------](https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/colored.png)](#roadmap)

## Roadmap

```
[✓]  Data ingestion + multi-source merge pipeline
[✓]  Party name standardisation (13 variant mappings)
[✓]  Winner extraction + constituency flip detection
[✓]  Volatility index — seat-level swing quantification
[✓]  Interactive Streamlit dashboard app
[✓]  Auto-generated AtliQ Media executive deck (PPTX)
[✓]  Auto-generated AtliQ Media print deck (PDF)
[✓]  Predictive model — swing seat classifier (pure gradient descent)
[ ]  Real-time ECI results feed integration
[ ]  Multi-state expansion (Kerala, Karnataka, AP)
```

<br/>

[![-----------------------------------------------------](https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/colored.png)](#contributing)

## Contributing

```bash
# 1. Fork the repo
# 2. Create your branch
git checkout -b feature/your-feature

# 3. Commit
git commit -m "feat: describe your change"

# 4. Push and open a PR
git push origin feature/your-feature
```

Please include a short explanation of the electoral insight any new analysis surfaces.

<br/>

[![-----------------------------------------------------](https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/colored.png)](#license)

## License

Distributed under the **MIT License**.
`MIT License — Copyright (c) 2026 Lakshya Verma`

<br/>

[![-----------------------------------------------------](https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/colored.png)](#footer)

<div align="center">

<br/>

Built by **[Lakshya Verma](https://github.com/lakshyaverma2004)**

`B.Tech CSE (AI/ML) · Manipal Institute of Technology · 2027`

<br/>

![Profile Views](https://visitor-badge.laobi.icu/badge?page_id=lakshyaverma2004.TamilNadu-elections-decoded&left_color=0f172a&right_color=7c2d12&left_text=Views)

<br/>

*8,489 candidates. 234 constituencies. 5-year swing. One pipeline.*

<br/>

<img src="https://capsule-render.vercel.app/api?type=rect&color=0:0a0f1e,100:0d1829&height=70&section=footer&text=Build.%20Analyse.%20Decode.&fontSize=16&fontColor=f97316&fontAlignY=50&desc=vermalakshya12%40gmail.com&descSize=11&descColor=64748b&descAlignY=80" width="100%"/>

</div>
