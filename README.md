# 📊 Telecom Customer Churn Analysis & Retention Intelligence

A comprehensive, beginner-friendly, and portfolio-ready Python data analysis project analyzing customer churn patterns in the telecommunications industry.

Developed as a first-year Computer Science Engineering project to demonstrate foundational data science techniques using **Python**, **Pandas**, **NumPy**, **Matplotlib**, **Seaborn**, and an interactive **Streamlit** web dashboard.

---

## 📌 Table of Contents

- [Project Overview](#-project-overview)
- [Business Problem](#-business-problem)
- [Project Objectives](#-project-objectives)
- [Technologies Used](#-technologies-used)
- [Dataset Description](#-dataset-description)
- [The 15 Assignment Tasks](#-the-15-assignment-tasks)
- [Key Empirical Findings & KPIs](#-key-empirical-findings--kpis)
- [Data Visualizations Catalog](#-data-visualizations-catalog)
- [Strategic Retention Recommendations](#-strategic-retention-recommendations)
- [Project Folder Structure](#-project-folder-structure)
- [Installation & Setup](#-installation--setup)
- [How to Run the Project](#-how-to-run-the-project)
- [Software Requirements Specification (SRS)](#-software-requirements-specification-srs)
- [Future Improvements](#-future-improvements)
- [License & Acknowledgments](#-license--acknowledgments)

---

## 🎯 Project Overview

In the telecommunications sector, acquiring new customers costs significantly more than retaining existing subscribers. High customer churn directly erodes recurring monthly revenue and market share.

This project delivers a complete data analysis pipeline built on an empirical dataset of 500 telecom customer records (`06_customer_churn.csv`). It performs systematic data cleaning, executes statistical computations using Pandas and NumPy, generates 10 high-resolution visual charts, exports structured tabular summaries, and deploys an interactive Streamlit analytics dashboard.

---

## 💼 Business Problem

Telecom executives face significant uncertainty regarding why customers leave and how to strategically intervene. Key business questions addressed:
1. **Attrition Rate:** What percentage of total subscribers discontinue service?
2. **Contract Impact:** Do short-term (Month-to-Month) contracts suffer higher attrition than multi-year commitments?
3. **Tenure Relationship:** At what point during a customer's tenure is defection most pronounced?
4. **Billing Friction:** Are customers with higher monthly bills leaving for cheaper alternatives?
5. **Technology Disparity:** How does churn compare across Fiber Optic, DSL, and Phone-only users?
6. **Payment Gateways:** Do specific payment channels correlate with higher attrition?
7. **Service Inefficiencies:** Does customer support ticket frequency serve as an early warning for churn?

---

## 🎯 Project Objectives

- Implement all **15 assigned college tasks** cleanly and idiomatic to beginner Python.
- Apply non-destructive data cleaning (median imputation for charges, explicit handling of categorical values).
- Utilize **NumPy** for core numerical and statistical operations (mean, median, standard deviation, percentile IQR outlier fences).
- Produce **10 publication-quality charts** saved as 300 DPI images in `outputs/graphs/`.
- Export **8 CSV summary tables** in `outputs/summary_tables/`.
- Construct an **interactive Streamlit web dashboard** with dynamic multi-variable filtering.
- Produce a formal **Software Requirements Specification (SRS)** in Word (.docx) format.

---

## 🛠️ Technologies Used

| Technology | Role |
| :--- | :--- |
| **Python (3.10+)** | Core programming language |
| **Pandas** | DataFrame manipulation, cross-tabulations, `pd.cut()` binning, `groupby()` aggregations |
| **NumPy** | Vectorized array operations, dispersion metrics, percentile calculations |
| **Matplotlib** | Figure creation, pie charts, custom bar chart annotations, 300 DPI exports |
| **Seaborn** | Statistical graphics, KDE charge distributions, box plot outlier detection |
| **Streamlit** | Interactive web dashboard, KPI metric cards, dynamic sidebar filters |
| **Python-Docx** | Programmatic generation of the formal academic SRS document (`SRS_Document.docx`) |

---

## 📁 Dataset Description

The dataset (`06_customer_churn.csv`) contains **500 rows** and **8 columns**:

| Column Name | Data Type | Missing Count | Description / Domain |
| :--- | :--- | :--- | :--- |
| `Customer_ID` | String | 0 | Unique customer identifier (CU0001 to CU0500) |
| `Tenure_Months` | Integer | 0 | Length of customer relationship (1 to 72 months) |
| `Contract` | Categorical | 0 | Agreement type: `Monthly`, `One Year`, `Two Year` |
| `Monthly_Charges` | Float | 8 (1.6%) | Monthly billed fee ($199.00 to $1,454.05) |
| `Internet_Service` | Categorical | 88 (17.6%) | Service type: `Fiber`, `DSL`, `None` (Unknown) |
| `Payment_Method` | Categorical | 0 | Billing channel: `Bank Transfer`, `Card`, `Cash`, `UPI` |
| `Support_Tickets` | Integer | 0 | Number of technical support tickets filed (0 to 7) |
| `Churn` | Categorical | 0 | Churn status: `Yes` (Churned), `No` (Retained) |

---

## 📝 The 15 Assignment Tasks

| Task # | Assignment Task Description | Key Implementation Detail & Actual Finding |
| :---: | :--- | :--- |
| **1** | Load and inspect customer data | Ingested 500 records x 8 features using `pd.read_csv()`; inspected schemas and first rows. |
| **2** | Check missing values and duplicate IDs | 0 duplicate Customer_IDs; detected 8 missing `Monthly_Charges` and 88 missing `Internet_Service`. |
| **3** | Clean missing charges using median | Imputed 8 missing charges with median **$744.57**; labeled missing internet as `Unknown`. |
| **4** | Overall churn count and percentage | **Retained: 367 (73.40%)**, **Churned: 133 (26.60%)**. Total = 500. |
| **5** | Compare churn across contract types | Two-Year has the lowest churn (**22.81%**), Monthly (**26.59%**), One-Year (**30.25%**). |
| **6** | Average tenure by churn status | Retained customers stay longer (**36.41 months**) vs Churned customers (**34.46 months**). |
| **7** | Compare monthly charges by churn status | Churned customers pay higher monthly fees (**$762.17**) vs Retained customers (**$747.22**). |
| **8** | Analyze churn by internet service | DSL has highest churn (**28.99%**), Unknown (**27.27%**), Fiber Optic (**24.69%**). |
| **9** | Analyze churn by payment method | Bank Transfer has highest churn (**29.71%**), Card (**26.89%**), UPI (**26.40%**), Cash (**22.88%**). |
| **10** | Average support tickets by churn status | Overall mean: Retained (1.52) vs Churned (1.60). Customers with 4-5 tickets churn at **43% to 50%**. |
| **11** | Create tenure groups using `pd.cut()` | Binned into 4 cohorts: Year 1 (**28.09%**), Year 2 (**29.76%**), Years 3-4 (**27.81%**), Years 5-6 (**22.78%**). |
| **12** | NumPy charge distribution statistics | Computed via NumPy: Mean = **$751.20**, Median = **$744.57**, Min = **$199.00**, Max = **$1454.05**, Std = **$219.47**. |
| **13** | Identify unusually high charges using IQR | Q1 = $624.71, Q3 = $900.84, IQR = $276.13, Upper Fence = **$1,315.03**. Found **2 high outliers**: `CU0311` & `CU0414`. |
| **14** | Summary table using `groupby()` & `agg()` | Segment-level matrix combining Contract and Internet Service exported to CSV. |
| **15** | Five actionable customer retention recommendations | Formulated 5 data-backed strategic retention initiatives based strictly on verified findings. |

---

## 📈 Key Empirical Findings & KPIs

### Primary Business KPIs
- **Total Customer Base:** 500 subscribers
- **Retained Customers:** 367 (73.40%)
- **Churned Customers:** 133 (26.60%)
- **Average Customer Tenure:** 35.89 months (~3.0 years)
- **Median Monthly Charge:** $744.57
- **Mean Monthly Charge:** $751.20

### Contract Comparison Table
| Contract Type | Total Customers | Churned | Retained | Churn Rate (%) | Retention Rate (%) |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **Monthly** | 267 | 71 | 196 | 26.59% | 73.41% |
| **One Year** | 119 | 36 | 83 | 30.25% | 69.75% |
| **Two Year** | 114 | 26 | 88 | **22.81%** | **77.19%** |

### Tenure Cohort Comparison Table (`pd.cut()`)
| Tenure Cohort | Total Customers | Churned | Retained | Churn Rate (%) | Retention Rate (%) |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **0-12 Months (Year 1)** | 89 | 25 | 64 | 28.09% | 71.91% |
| **13-24 Months (Year 2)** | 84 | 25 | 59 | **29.76%** | 70.24% |
| **25-48 Months (Years 3-4)** | 169 | 47 | 122 | 27.81% | 72.19% |
| **49-72 Months (Years 5-6)** | 158 | 36 | 122 | **22.78%** | **77.22%** |

---

## 🖼️ Data Visualizations Catalog

All graphs are generated programmatically and saved in `outputs/graphs/` at 300 DPI resolution:

1. `01_overall_churn_distribution.png`: Elegant exploded pie chart highlighting the 73.4% retention vs 26.6% churn split.
2. `02_churn_by_contract_type.png`: Grouped bar chart comparing retention and churn percentages across Monthly, 1-Year, and 2-Year contracts.
3. `03_average_tenure_by_churn.png`: Bar chart contrasting average tenure (36.41 months for retained vs 34.46 months for churned).
4. `04_monthly_charges_by_churn.png`: Bar chart displaying average monthly billing ($747.22 vs $762.17).
5. `05_churn_by_internet_service.png`: Bar chart demonstrating DSL's elevated churn (28.99%) compared to Fiber (24.69%).
6. `06_churn_by_payment_method.png`: Comparison of attrition across Bank Transfer (29.71%), Card (26.89%), UPI (26.40%), and Cash (22.88%).
7. `07_support_tickets_by_churn.png`: Bar chart comparing mean support ticket counts by churn status.
8. `08_churn_by_tenure_group.png`: Grouped bar plot analyzing churn progression through the four discretized tenure cohorts.
9. `09_monthly_charges_distribution.png`: Histogram with Kernel Density Estimation (KDE), annotating mean ($751.20) and median ($744.57).
10. `10_monthly_charges_outliers_boxplot.png`: Box plot pinpointing the upper IQR fence ($1,315.03) and 2 identified high outliers.

---

## 💡 Strategic Retention Recommendations

Based on the actual findings of this analysis, telecom management should implement these **five practical recommendations**:

### 1. Incentivize Multi-Year Contract Transitions
- **Data Finding:** Two-year contract customers exhibit the lowest churn rate (**22.81%**) compared to one-year (**30.25%**) and monthly contracts (**26.59%**).
- **Action Plan:** Offer structured incentives—such as a 10% annual billing discount, free device upgrades, or bundled OTT streaming subscriptions—to transition monthly and 1-year subscribers into 2-year contracts.

### 2. Dedicated Early-Tenure Onboarding (First 24 Months)
- **Data Finding:** Churn peaks in Year 2 (**29.76%**) and Year 1 (**28.09%**), but drops significantly to **22.78%** once customers surpass 48 months.
- **Action Plan:** Implement a proactive 90-day onboarding workflow featuring welcome calls, automated speed tests, usage tutorials, and milestone loyalty credits awarded at months 6, 12, and 18.

### 3. DSL Infrastructure Modernization & Fiber Migration
- **Data Finding:** DSL subscribers suffer the highest churn rate (**28.99%**) versus Fiber optic subscribers (**24.69%**).
- **Action Plan:** Launch a targeted migration campaign offering subsidized or free Fiber optic installation kits and introductory price-matching to migrate DSL users before they switch to competing high-speed fiber providers.

### 4. Bill-Shock Protection & Modular Plan Right-Sizing
- **Data Finding:** Churned customers pay higher monthly fees on average (**$762.17 vs $747.22**), and extreme outliers paying over $1,300/month face high defection risk (e.g. `CU0414` paying $1,454.05 churned).
- **Action Plan:** Deploy automated billing health checks that flag accounts paying above the 75th percentile ($900+) and proactively offer modular plan recommendations to match real consumption without bill shock.

### 5. "Red-Flag" Ticket Escalation Protocol
- **Data Finding:** While customers with 0–3 tickets experience 23%–27% churn, customers submitting 4 or 5 tickets experience an alarming **42.86% to 50.00%** churn rate.
- **Action Plan:** Institute an automated service alert: any account submitting their 3rd support ticket within a 60-day window must be automatically escalated to a Senior Technical Specialist and offered an immediate courtesy service credit.

---

## 📂 Project Folder Structure

```
Telecom-Customer-Churn-Analysis/
│
├── data/
│   └── 06_customer_churn.csv              # Original telecom customer dataset (500 records)
│
├── outputs/
│   ├── graphs/                            # 10 High-resolution (300 DPI) visualization charts
│   │   ├── 01_overall_churn_distribution.png
│   │   ├── 02_churn_by_contract_type.png
│   │   ├── 03_average_tenure_by_churn.png
│   │   ├── 04_monthly_charges_by_churn.png
│   │   ├── 05_churn_by_internet_service.png
│   │   ├── 06_churn_by_payment_method.png
│   │   ├── 07_support_tickets_by_churn.png
│   │   ├── 08_churn_by_tenure_group.png
│   │   ├── 09_monthly_charges_distribution.png
│   │   └── 10_monthly_charges_outliers_boxplot.png
│   │
│   └── summary_tables/                    # 8 Exported CSV analytical summary tables
│       ├── charges_by_churn_summary.csv
│       ├── contract_churn_summary.csv
│       ├── contract_internet_detailed_summary.csv
│       ├── internet_service_churn_summary.csv
│       ├── kpi_summary.csv
│       ├── monthly_charges_statistics.csv
│       ├── payment_method_churn_summary.csv
│       └── tenure_group_churn_summary.csv
│
├── churn_analysis.py                      # Main standalone Python script (Tasks 1-15)
├── dashboard.py                           # Interactive Streamlit analytics web application
├── requirements.txt                       # Project dependency specifications
├── README.md                              # Professional GitHub portfolio documentation
├── SRS_Document.docx                      # Formal Software Requirements Specification (Word)
└── .gitignore                             # Git configuration ignoring cache & build artifacts
```

---

## ⚙️ Installation & Setup

### Prerequisites
- Python 3.10, 3.11, 3.12, 3.13, 3.14, or 3.15 installed.
- Git (optional, for repository management).

### 1. Clone or Open the Repository
```bash
git clone https://github.com/your-username/Telecom-Customer-Churn-Analysis.git
cd Telecom-Customer-Churn-Analysis
```

### 2. Create and Activate a Virtual Environment (Recommended)
```bash
# Windows (Command Prompt / PowerShell)
python -m venv venv
venv\Scripts\activate

# macOS / Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Required Dependencies
```bash
pip install -r requirements.txt
```

---

## 🚀 How to Run the Project

### Option A: Run the Complete Batch Python Analysis (Tasks 1-15)
Execute the main script to perform all data cleaning, print statistics to the console, and generate all graphs and CSV summary tables:
```bash
python churn_analysis.py
```
*Expected Output:* Clear section banners, tabular statistics, business interpretations for all 15 tasks, 10 generated PNG charts in `outputs/graphs/`, and 8 CSV files in `outputs/summary_tables/`.

### Option B: Launch the Interactive Streamlit Web Dashboard
Launch the web interface for executive exploration and dynamic filtering:
```bash
streamlit run dashboard.py
```
*Expected Output:* Your default web browser will automatically open to `http://localhost:8501`, displaying:
- Top-level KPI summary cards.
- Sidebar filters for Contract, Internet Service, Payment Method, Tenure Slider, and Charges Slider.
- Tabbed views for Churn Drivers, Financial Outliers, Tenure Analysis, Data Export, and Recommendations.

---

## 📄 Software Requirements Specification (SRS)

A comprehensive, formal academic **Software Requirements Specification (SRS)** document has been prepared in DOCX format:
- **File:** `SRS_Document.docx`
- **Sections Included (17 Sections):**
  1. Project Title
  2. Introduction
  3. Problem Statement
  4. Project Objectives
  5. Scope of the Project
  6. Hardware Requirements
  7. Software Requirements
  8. Technologies Used
  9. Dataset Description
  10. Functional Requirements (FR-01 to FR-11)
  11. Non-Functional Requirements (Performance, Fidelity, Usability, Portability)
  12. Methodology (CRISP-DM)
  13. Data Cleaning Process
  14. Data Analysis Tasks (Detailed Results for all 15 Tasks)
  15. Expected Outputs
  16. Limitations
  17. Conclusion

---

## 🔮 Future Improvements

1. **Predictive Machine Learning:** Train and evaluate classification models (Logistic Regression, Random Forest, XGBoost) to predict individual customer churn probabilities.
2. **Feature Importance & SHAP Values:** Use SHAP (SHapley Additive exPlanations) to explain individual subscriber risk factors.
3. **Automated Churn Alert API:** Build a RESTful Flask or FastAPI endpoint allowing CRM systems to query churn risk in real-time.
4. **Cloud Database Integration:** Connect to PostgreSQL or Snowflake for automated, scheduled batch ingestion.

---

## 📜 License & Acknowledgments

- **Course:** Computer Science Engineering (Python Programming)
- **Author:** Student Data Analyst & Software Developer
- **Dataset:** Telecom Customer Churn (`06_customer_churn.csv`)
- **License:** Open for academic and portfolio demonstration purposes.
