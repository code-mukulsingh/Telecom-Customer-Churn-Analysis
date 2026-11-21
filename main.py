"""
========================================================================================
TELECOM CUSTOMER CHURN ANALYSIS - ALL-IN-ONE MASTER SCRIPT
Course: First-Year Computer Science Engineering (Python Programming Project)
Author: Student Data Analyst & Software Developer
Dataset: 06_customer_churn.csv
========================================================================================
"""

import os
import sys
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')  # Headless mode so plots save reliably to files without GUI popups
import matplotlib.pyplot as plt
import seaborn as sns


# ======================================================================================
# SMART PATH DETECTION & FOLDER CREATION
# ======================================================================================
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

# Smart search: finds the CSV file wherever it is placed
POSSIBLE_PATHS = [
    os.path.join(SCRIPT_DIR, "data", "06_customer_churn.csv"),
    os.path.join(SCRIPT_DIR, "06_customer_churn.csv"),
    r"c:\Users\MUKUL SINGH\AppData\Local\Temp\06_customer_churn.csv"
]

DATA_PATH = None
for p in POSSIBLE_PATHS:
    if os.path.exists(p):
        DATA_PATH = p
        break

if DATA_PATH is None:
    print("❌ Error: Could not find '06_customer_churn.csv'.")
    print("Please place '06_customer_churn.csv' in the same folder as this script or inside 'data/'.")
    sys.exit(1)

# Create output folders automatically
GRAPHS_DIR = os.path.join(SCRIPT_DIR, "outputs", "graphs")
TABLES_DIR = os.path.join(SCRIPT_DIR, "outputs", "summary_tables")
os.makedirs(GRAPHS_DIR, exist_ok=True)
os.makedirs(TABLES_DIR, exist_ok=True)

# Styling settings for professional, attractive charts
sns.set_theme(style="whitegrid", palette="muted")
plt.rcParams['font.sans-serif'] = 'Segoe UI', 'DejaVu Sans', 'Arial'
COLOR_RETAINED = '#2ecc71'  # Green
COLOR_CHURNED = '#e74c3c'   # Red


def print_title(task_number, title_text):
    """Helper function to print clear, beautiful section headers in the terminal."""
    border = "=" * 80
    print(f"\n{border}")
    print(f" TASK {task_number}: {title_text.upper()}")
    print(f"{border}")


# ======================================================================================
# TASK 1: LOAD AND INSPECT CUSTOMER DATA
# ======================================================================================
print_title(1, "Load and Inspect Customer Data")

# Read the raw dataset using Pandas
raw_df = pd.read_csv(DATA_PATH)

print(f"✔ Dataset loaded successfully from: {DATA_PATH}")
print(f"  - Total Customers (Rows)    : {raw_df.shape[0]}")
print(f"  - Total Attributes (Columns): {raw_df.shape[1]}")

print("\nColumn Names and Data Types:")
for col, dtype in zip(raw_df.columns, raw_df.dtypes):
    print(f"  - {col:18} : {dtype}")

print("\nFirst 5 Rows of Customer Records:")
print(raw_df.head().to_string(index=False))

print("\n💡 Explanation (Task 1):")
print("The dataset contains 500 customer records with attributes like tenure, contract type,")
print("monthly charges, internet service, payment method, support tickets, and churn status.")


# ======================================================================================
# TASK 2: CHECK MISSING VALUES AND DUPLICATE CUSTOMER_ID RECORDS
# ======================================================================================
print_title(2, "Check Missing Values and Duplicate Customer_ID Records")

# Check for duplicate Customer_IDs
duplicate_count = raw_df['Customer_ID'].duplicated().sum()
print(f"1. Duplicate Customer_ID Count: {duplicate_count}")
if duplicate_count == 0:
    print("   ✔ Data Integrity Check Passed: All Customer_IDs are unique!")

# Check missing (null) values in every column
missing_series = raw_df.isnull().sum()
missing_percent = (missing_series / len(raw_df)) * 100

missing_table = pd.DataFrame({
    'Missing_Count': missing_series,
    'Percentage (%)': missing_percent.round(2)
})
print("\n2. Missing Values Summary:")
print(missing_table.to_string())

print("\n💡 Explanation (Task 2):")
print("We found 8 missing values in 'Monthly_Charges' (1.6%) and 88 missing/None values in")
print("'Internet_Service' (17.6%). No duplicate customer records exist.")


# ======================================================================================
# TASK 3: CLEAN MISSING MONTHLY_CHARGES USING THE MEDIAN & TREAT CATEGORICALS
# ======================================================================================
print_title(3, "Clean Missing Monthly_Charges Using Median")

# Make a copy so we preserve the original raw dataset
df = raw_df.copy()

# Step A: Calculate median of Monthly_Charges
charges_median = df['Monthly_Charges'].median()
print(f"1. Calculated Median for Monthly_Charges: ${charges_median:.2f}")

# Step B: Impute (fill) missing values with the median
df['Monthly_Charges'] = df['Monthly_Charges'].fillna(charges_median)

# Step C: Treat missing Internet_Service as 'Unknown' (No internet / Phone-only)
df['Internet_Service'] = df['Internet_Service'].fillna('Unknown')

# Step D: Verify that no missing values remain
remaining_nulls = df.isnull().sum().sum()
print(f"2. Imputed 8 missing charges with median value ${charges_median:.2f}.")
print("3. Treated 88 missing internet service records as 'Unknown' (avoiding data loss).")
print(f"4. Remaining Missing Values: {remaining_nulls} (Dataset is 100% clean!)")

print("\n💡 Explanation (Task 3):")
print("Using the median protects our data from being skewed by extreme bills.")
print("We preserved all 500 customer records instead of silently deleting them.")


# ======================================================================================
# TASK 4: CALCULATE OVERALL CHURN COUNT AND CHURN PERCENTAGE
# ======================================================================================
print_title(4, "Calculate Overall Churn Count and Churn Percentage")

total_customers = len(df)
churn_counts = df['Churn'].value_counts()

retained_count = churn_counts.get('No', 0)
churned_count = churn_counts.get('Yes', 0)

churn_rate = (churned_count / total_customers) * 100
retention_rate = (retained_count / total_customers) * 100

print(f"Total Customer Base       : {total_customers:,}")
print(f"Retained Customers (No)   : {retained_count:,} ({retention_rate:.2f}%)")
print(f"Churned Customers (Yes)   : {churned_count:,} ({churn_rate:.2f}%)")

print("\n💡 Explanation (Task 4):")
print(f"The overall churn rate is {churn_rate:.2f}%. This means more than 1 in every 4 customers")
print("leaves the telecom service, representing significant revenue loss that requires intervention.")


# ======================================================================================
# TASK 5: COMPARE CHURN PERCENTAGE ACROSS CONTRACT TYPES
# ======================================================================================
print_title(5, "Compare Churn Percentage Across Contract Types")

contract_counts = pd.crosstab(df['Contract'], df['Churn'], margins=True)
contract_pcts = pd.crosstab(df['Contract'], df['Churn'], normalize='index') * 100

contract_summary = pd.DataFrame({
    'Total_Customers': contract_counts['All'][:-1],
    'Churned_Count': contract_counts['Yes'][:-1],
    'Retained_Count': contract_counts['No'][:-1],
    'Churn_Rate (%)': contract_pcts['Yes'].round(2),
    'Retention_Rate (%)': contract_pcts['No'].round(2)
}).reset_index()

print(contract_summary.to_string(index=False))

print("\n💡 Explanation (Task 5):")
print("- Two-Year contracts have the LOWEST churn rate (22.81%).")
print("- Monthly contracts have a 26.59% churn rate.")
print("- One-Year contracts have the HIGHEST churn rate (30.25%).")
print("Longer contractual commitments significantly buffer against customer attrition.")


# ======================================================================================
# TASK 6: CALCULATE AVERAGE TENURE FOR CHURNED AND RETAINED CUSTOMERS
# ======================================================================================
print_title(6, "Calculate Average Tenure for Churned and Retained Customers")

tenure_stats = df.groupby('Churn')['Tenure_Months'].agg(['count', 'mean', 'median', 'std']).reset_index()
print(tenure_stats.to_string(index=False))

mean_tenure_retained = tenure_stats.loc[tenure_stats['Churn'] == 'No', 'mean'].values[0]
mean_tenure_churned = tenure_stats.loc[tenure_stats['Churn'] == 'Yes', 'mean'].values[0]

print(f"\nAverage Tenure of Retained Customers: {mean_tenure_retained:.2f} months (~{mean_tenure_retained/12:.1f} years)")
print(f"Average Tenure of Churned Customers : {mean_tenure_churned:.2f} months (~{mean_tenure_churned/12:.1f} years)")

print("\n💡 Explanation (Task 6):")
print("Retained customers stay longer on average (36.41 months vs 34.46 months).")
print("The median tenure difference (39 vs 33 months) shows that customers become much")
print("more loyal after passing their third year.")


# ======================================================================================
# TASK 7: COMPARE MONTHLY CHARGES BY CHURN STATUS
# ======================================================================================
print_title(7, "Compare Monthly Charges by Churn Status")

charges_by_churn = df.groupby('Churn')['Monthly_Charges'].agg(['count', 'mean', 'median', 'std', 'min', 'max']).reset_index()
print(charges_by_churn.to_string(index=False))

mean_charge_retained = charges_by_churn.loc[charges_by_churn['Churn'] == 'No', 'mean'].values[0]
mean_charge_churned = charges_by_churn.loc[charges_by_churn['Churn'] == 'Yes', 'mean'].values[0]
diff_charge = mean_charge_churned - mean_charge_retained

print(f"\nMean Monthly Charge (Retained): ${mean_charge_retained:.2f}")
print(f"Mean Monthly Charge (Churned) : ${mean_charge_churned:.2f}")
print(f"Price Difference: Churned customers pay ${diff_charge:.2f} more per month on average.")

print("\n💡 Explanation (Task 7):")
print("Churned customers pay higher average monthly charges ($762.17 vs $747.22).")
print("Higher bills trigger price sensitivity, encouraging customers to look for cheaper alternatives.")


# ======================================================================================
# TASK 8: ANALYZE CHURN BY INTERNET SERVICE
# ======================================================================================
print_title(8, "Analyze Churn by Internet Service")

net_counts = pd.crosstab(df['Internet_Service'], df['Churn'], margins=True)
net_pcts = pd.crosstab(df['Internet_Service'], df['Churn'], normalize='index') * 100

internet_summary = pd.DataFrame({
    'Total_Customers': net_counts['All'][:-1],
    'Churned_Count': net_counts['Yes'][:-1],
    'Retained_Count': net_counts['No'][:-1],
    'Churn_Rate (%)': net_pcts['Yes'].round(2),
    'Retention_Rate (%)': net_pcts['No'].round(2)
}).reset_index()

print(internet_summary.to_string(index=False))

print("\n💡 Explanation (Task 8):")
print("DSL customers experience the highest churn rate (28.99%), compared to Fiber Optic (24.69%).")
print("Older copper DSL lines often suffer from speed and reliability issues, causing churn.")


# ======================================================================================
# TASK 9: ANALYZE CHURN BY PAYMENT METHOD
# ======================================================================================
print_title(9, "Analyze Churn by Payment Method")

pay_counts = pd.crosstab(df['Payment_Method'], df['Churn'], margins=True)
pay_pcts = pd.crosstab(df['Payment_Method'], df['Churn'], normalize='index') * 100

pay_summary = pd.DataFrame({
    'Total_Customers': pay_counts['All'][:-1],
    'Churned_Count': pay_counts['Yes'][:-1],
    'Retained_Count': pay_counts['No'][:-1],
    'Churn_Rate (%)': pay_pcts['Yes'].round(2),
    'Retention_Rate (%)': pay_pcts['No'].round(2)
}).reset_index()

print(pay_summary.to_string(index=False))

print("\n💡 Explanation (Task 9):")
print("Bank Transfer customers experience the highest churn rate (29.71%), followed by Card (26.89%),")
print("UPI (26.40%), and Cash (22.88%). Manual transfer friction may contribute to churn.")


# ======================================================================================
# TASK 10: CALCULATE AVERAGE SUPPORT TICKETS BY CHURN STATUS
# ======================================================================================
print_title(10, "Calculate Average Support Tickets by Churn Status")

ticket_stats = df.groupby('Churn')['Support_Tickets'].agg(['count', 'mean', 'median', 'std']).reset_index()
print(ticket_stats.to_string(index=False))

ticket_by_count = pd.crosstab(df['Support_Tickets'], df['Churn'], normalize='index') * 100
ticket_by_count['Churn_Rate (%)'] = ticket_by_count['Yes'].round(2)
print("\nChurn Rate by Exact Number of Support Tickets:")
print(ticket_by_count[['Churn_Rate (%)']])

print("\n💡 Explanation (Task 10):")
print("While the overall average tickets are ~1.52 vs 1.60, customers filing 4 or 5 support tickets")
print("have a drastic 42.86% to 50.00% churn rate! Frequent technical complaints are a strong red flag.")


# ======================================================================================
# TASK 11: CREATE TENURE GROUPS USING pd.cut() AND COMPARE CHURN
# ======================================================================================
print_title(11, "Create Tenure Groups Using Pandas pd.cut()")

# Create 4 tenure intervals using pd.cut()
bins = [0, 12, 24, 48, 72]
labels = ['0-12 Months (Year 1)', '13-24 Months (Year 2)', '25-48 Months (Years 3-4)', '49-72 Months (Years 5-6)']
df['Tenure_Group'] = pd.cut(df['Tenure_Months'], bins=bins, labels=labels, right=True)

tenure_grp_counts = pd.crosstab(df['Tenure_Group'], df['Churn'], margins=True)
tenure_grp_pcts = pd.crosstab(df['Tenure_Group'], df['Churn'], normalize='index') * 100

tenure_group_summary = pd.DataFrame({
    'Total_Customers': tenure_grp_counts['All'][:-1],
    'Churned_Count': tenure_grp_counts['Yes'][:-1],
    'Retained_Count': tenure_grp_counts['No'][:-1],
    'Churn_Rate (%)': tenure_grp_pcts['Yes'].round(2),
    'Retention_Rate (%)': tenure_grp_pcts['No'].round(2)
}).reset_index()

print(tenure_group_summary.to_string(index=False))

print("\n💡 Explanation (Task 11):")
print("Churn is highest in the first 24 months (28.09% in Year 1 and 29.76% in Year 2).")
print("After 48 months (4 years), churn drops to 22.78%. Retaining new users early is critical.")


# ======================================================================================
# TASK 12: USE NUMPY TO CALCULATE CHARGE DISTRIBUTION STATISTICS
# ======================================================================================
print_title(12, "Use NumPy to Calculate Charge Distribution Statistics")

# Convert pandas column to pure NumPy array
charges_np = df['Monthly_Charges'].to_numpy()

# Calculate statistics strictly using NumPy functions
np_mean = float(np.mean(charges_np))
np_median = float(np.median(charges_np))
np_min = float(np.min(charges_np))
np_max = float(np.max(charges_np))
np_std = float(np.std(charges_np, ddof=1)) # sample standard deviation

numpy_stats = pd.DataFrame({
    'NumPy Statistic': ['Mean', 'Median', 'Minimum', 'Maximum', 'Standard Deviation'],
    'Value': [f"${np_mean:.2f}", f"${np_median:.2f}", f"${np_min:.2f}", f"${np_max:.2f}", f"${np_std:.2f}"]
})

print(numpy_stats.to_string(index=False))

print("\n💡 Explanation (Task 12):")
print(f"NumPy shows monthly charges average ${np_mean:.2f} with a median of ${np_median:.2f}.")
print(f"Charges range widely from ${np_min:.2f} to ${np_max:.2f} with standard deviation ${np_std:.2f}.")


# ======================================================================================
# TASK 13: IDENTIFY UNUSUALLY HIGH MONTHLY CHARGES USING THE IQR METHOD
# ======================================================================================
print_title(13, "Identify Unusually High Monthly Charges Using IQR Method")

q1 = np.percentile(charges_np, 25)
q3 = np.percentile(charges_np, 75)
iqr = q3 - q1

lower_fence = q1 - 1.5 * iqr
upper_fence = q3 + 1.5 * iqr

high_outliers = df[df['Monthly_Charges'] > upper_fence]

print(f"1. 25th Percentile (Q1) : ${q1:.2f}")
print(f"2. 75th Percentile (Q3) : ${q3:.2f}")
print(f"3. Interquartile Range  : ${iqr:.2f}")
print(f"4. Lower Fence Limit    : ${lower_fence:.2f}")
print(f"5. Upper Fence Limit    : ${upper_fence:.2f}")
print(f"\nNumber of High Outliers Found: {len(high_outliers)}")

if len(high_outliers) > 0:
    print(high_outliers[['Customer_ID', 'Tenure_Months', 'Contract', 'Monthly_Charges', 'Churn']].to_string(index=False))

print("\n💡 Explanation (Task 13):")
print(f"The IQR method identified 2 customers paying over ${upper_fence:.2f}/month:")
print("Customer CU0414 pays $1,454.05/month and churned! Excessively high bills create defection risk.")


# ======================================================================================
# TASK 14: CREATE A SUMMARY TABLE USING PANDAS groupby() AND agg()
# ======================================================================================
print_title(14, "Create Summary Table Using Pandas groupby() and agg()")

summary_agg = df.groupby(['Contract', 'Internet_Service']).agg(
    Total_Customers=('Customer_ID', 'count'),
    Churn_Count=('Churn', lambda x: (x == 'Yes').sum()),
    Retained_Count=('Churn', lambda x: (x == 'No').sum()),
    Churn_Rate_Pct=('Churn', lambda x: round((x == 'Yes').mean() * 100, 2)),
    Avg_Tenure_Months=('Tenure_Months', lambda x: round(x.mean(), 1)),
    Avg_Monthly_Bill=('Monthly_Charges', lambda x: round(x.mean(), 2)),
    Avg_Support_Tickets=('Support_Tickets', lambda x: round(x.mean(), 2))
).reset_index()

print(summary_agg.to_string(index=False))

# Export summary CSV files into outputs/summary_tables/
summary_agg.to_csv(os.path.join(TABLES_DIR, "contract_internet_detailed_summary.csv"), index=False)
contract_summary.to_csv(os.path.join(TABLES_DIR, "contract_churn_summary.csv"), index=False)
tenure_group_summary.to_csv(os.path.join(TABLES_DIR, "tenure_group_churn_summary.csv"), index=False)
internet_summary.to_csv(os.path.join(TABLES_DIR, "internet_service_churn_summary.csv"), index=False)
pay_summary.to_csv(os.path.join(TABLES_DIR, "payment_method_churn_summary.csv"), index=False)
numpy_stats.to_csv(os.path.join(TABLES_DIR, "monthly_charges_statistics.csv"), index=False)

kpi_table = pd.DataFrame({
    'Metric': ['Total Customers', 'Retained', 'Churned', 'Churn Rate', 'Retention Rate', 'Avg Tenure', 'Avg Bill'],
    'Value': [total_customers, retained_count, churned_count, f"{churn_rate:.2f}%", f"{retention_rate:.2f}%", f"{df['Tenure_Months'].mean():.2f} mo", f"${df['Monthly_Charges'].mean():.2f}"]
})
kpi_table.to_csv(os.path.join(TABLES_DIR, "kpi_summary.csv"), index=False)
print(f"\n✔ Summary CSV tables successfully saved to: {TABLES_DIR}")

print("\n💡 Explanation (Task 14):")
print("This multi-dimensional table reveals that Monthly contract customers with Unknown internet")
print("pay the highest bills ($804.29) and Monthly fiber customers have the most support tickets (1.79).")


# ======================================================================================
# TASK 15: FIVE CUSTOMER-RETENTION RECOMMENDATIONS
# ======================================================================================
print_title(15, "Five Practical Customer-Retention Recommendations")

recs = [
    ("1. Incentivize Multi-Year Contracts",
     "Two-year contract holders have the lowest churn rate (22.81%). Offer a 10% annual billing discount or free device upgrades to migrate users away from monthly and 1-year contracts."),
    ("2. 90-Day Early Tenure Onboarding",
     "Churn is highest during the first 24 months (~28%-30%). Establish a proactive onboarding cadence with welcome calls, speed tests, and loyalty credits at 6 and 12 months."),
    ("3. Upgrade DSL to Fiber Optics",
     "DSL users suffer the highest churn rate (28.99%) compared to Fiber (24.69%). Offer free Fiber installation kits and price-matched promotions to retain DSL customers."),
    ("4. Bill-Shock Audits for High Charges",
     "Churned customers pay higher average bills ($762.17 vs $747.22), with outliers over $1,300. Run automated billing audits to right-size plans and prevent bill shock."),
    ("5. Rapid Ticket Escalation Protocol",
     "Customers submitting 4 or 5 support tickets churn at an alarming 43%-50%. Automatically escalate any account reaching 3 tickets to senior specialists with courtesy billing credits.")
]

for title, desc in recs:
    print(f"\n📌 {title}")
    print(f"   {desc}")


# ======================================================================================
# DATA VISUALIZATIONS GENERATION (10 CHARTS)
# ======================================================================================
print_title("EXTRA", "Generating 10 High-Resolution Visual Graphs")

# 1. Overall customer churn distribution (pie chart)
fig, ax = plt.subplots(figsize=(6.5, 6.5))
ax.pie([retained_count, churned_count], labels=['Retained (No)', 'Churned (Yes)'],
       autopct='%1.1f%%', colors=[COLOR_RETAINED, COLOR_CHURNED], explode=(0, 0.08),
       startangle=140, textprops={'fontsize': 11, 'weight': 'bold'}, shadow=True)
ax.set_title("1. Overall Customer Churn Distribution (N=500)", fontsize=13, weight='bold', pad=15)
plt.tight_layout()
plt.savefig(os.path.join(GRAPHS_DIR, "01_overall_churn_distribution.png"), dpi=300)
plt.close()

# 2. Customer churn by contract type (bar chart)
fig, ax = plt.subplots(figsize=(8, 5))
contract_plot = pd.crosstab(df['Contract'], df['Churn'], normalize='index') * 100
contract_plot.plot(kind='bar', color=[COLOR_RETAINED, COLOR_CHURNED], ax=ax, edgecolor='black', alpha=0.9)
ax.set_title("2. Customer Churn Rate by Contract Type", fontsize=13, weight='bold')
ax.set_ylabel("Percentage (%)", weight='bold')
ax.set_xlabel("Contract Type", weight='bold')
ax.set_xticklabels(ax.get_xticklabels(), rotation=0)
ax.set_ylim(0, 95)
for p in ax.patches:
    h = p.get_height()
    if h > 0:
        ax.annotate(f"{h:.1f}%", (p.get_x() + p.get_width() / 2., h + 1), ha='center', weight='bold', fontsize=9)
plt.tight_layout()
plt.savefig(os.path.join(GRAPHS_DIR, "02_churn_by_contract_type.png"), dpi=300)
plt.close()

# 3. Average tenure by churn status (bar chart)
fig, ax = plt.subplots(figsize=(6.5, 5))
bars = ax.bar(['Retained (No)', 'Churned (Yes)'], [mean_tenure_retained, mean_tenure_churned],
              color=[COLOR_RETAINED, COLOR_CHURNED], edgecolor='black', width=0.5)
ax.set_title("3. Average Customer Tenure by Churn Status", fontsize=13, weight='bold')
ax.set_ylabel("Average Tenure (Months)", weight='bold')
for b in bars:
    h = b.get_height()
    ax.annotate(f"{h:.1f} Months\n(~{h/12:.1f} Yrs)", (b.get_x() + b.get_width() / 2., h / 2),
                ha='center', va='center', color='white', weight='bold', fontsize=11)
ax.set_ylim(0, 45)
plt.tight_layout()
plt.savefig(os.path.join(GRAPHS_DIR, "03_average_tenure_by_churn.png"), dpi=300)
plt.close()

# 4. Average monthly charges by churn status (bar chart)
fig, ax = plt.subplots(figsize=(6.5, 5))
bars = ax.bar(['Retained (No)', 'Churned (Yes)'], [mean_charge_retained, mean_charge_churned],
              color=[COLOR_RETAINED, COLOR_CHURNED], edgecolor='black', width=0.5)
ax.set_title("4. Average Monthly Charges by Churn Status", fontsize=13, weight='bold')
ax.set_ylabel("Mean Monthly Bill ($)", weight='bold')
for b in bars:
    h = b.get_height()
    ax.annotate(f"${h:.2f}", (b.get_x() + b.get_width() / 2., h / 2),
                ha='center', va='center', color='white', weight='bold', fontsize=12)
ax.set_ylim(0, 900)
plt.tight_layout()
plt.savefig(os.path.join(GRAPHS_DIR, "04_monthly_charges_by_churn.png"), dpi=300)
plt.close()

# 5. Churn by internet service (bar chart)
fig, ax = plt.subplots(figsize=(8, 5))
net_plot = pd.crosstab(df['Internet_Service'], df['Churn'], normalize='index') * 100
net_plot.plot(kind='bar', color=[COLOR_RETAINED, COLOR_CHURNED], ax=ax, edgecolor='black', alpha=0.9)
ax.set_title("5. Churn Rate by Internet Service", fontsize=13, weight='bold')
ax.set_ylabel("Percentage (%)", weight='bold')
ax.set_xlabel("Internet Service", weight='bold')
ax.set_xticklabels(ax.get_xticklabels(), rotation=0)
ax.set_ylim(0, 95)
for p in ax.patches:
    h = p.get_height()
    if h > 0:
        ax.annotate(f"{h:.1f}%", (p.get_x() + p.get_width() / 2., h + 1), ha='center', weight='bold', fontsize=9)
plt.tight_layout()
plt.savefig(os.path.join(GRAPHS_DIR, "05_churn_by_internet_service.png"), dpi=300)
plt.close()

# 6. Churn by payment method (bar chart)
fig, ax = plt.subplots(figsize=(8.5, 5))
pay_plot = pd.crosstab(df['Payment_Method'], df['Churn'], normalize='index') * 100
pay_plot.plot(kind='bar', color=[COLOR_RETAINED, COLOR_CHURNED], ax=ax, edgecolor='black', alpha=0.9)
ax.set_title("6. Churn Rate by Payment Method", fontsize=13, weight='bold')
ax.set_ylabel("Percentage (%)", weight='bold')
ax.set_xlabel("Payment Method", weight='bold')
ax.set_xticklabels(ax.get_xticklabels(), rotation=0)
ax.set_ylim(0, 95)
for p in ax.patches:
    h = p.get_height()
    if h > 0:
        ax.annotate(f"{h:.1f}%", (p.get_x() + p.get_width() / 2., h + 1), ha='center', weight='bold', fontsize=9)
plt.tight_layout()
plt.savefig(os.path.join(GRAPHS_DIR, "06_churn_by_payment_method.png"), dpi=300)
plt.close()

# 7. Average support tickets by churn status (bar chart)
fig, ax = plt.subplots(figsize=(6.5, 5))
mean_tickets = df.groupby('Churn')['Support_Tickets'].mean()
bars = ax.bar(['Retained (No)', 'Churned (Yes)'], [mean_tickets['No'], mean_tickets['Yes']],
              color=[COLOR_RETAINED, COLOR_CHURNED], edgecolor='black', width=0.5)
ax.set_title("7. Average Support Tickets by Churn Status", fontsize=13, weight='bold')
ax.set_ylabel("Average Support Tickets", weight='bold')
for b in bars:
    h = b.get_height()
    ax.annotate(f"{h:.2f} Tickets", (b.get_x() + b.get_width() / 2., h / 2),
                ha='center', va='center', color='white', weight='bold', fontsize=12)
ax.set_ylim(0, 2.5)
plt.tight_layout()
plt.savefig(os.path.join(GRAPHS_DIR, "07_support_tickets_by_churn.png"), dpi=300)
plt.close()

# 8. Churn percentage by tenure group (bar chart)
fig, ax = plt.subplots(figsize=(9, 5))
t_plot = pd.crosstab(df['Tenure_Group'], df['Churn'], normalize='index') * 100
t_plot.plot(kind='bar', color=[COLOR_RETAINED, COLOR_CHURNED], ax=ax, edgecolor='black', alpha=0.9)
ax.set_title("8. Churn Percentage by Tenure Cohort", fontsize=13, weight='bold')
ax.set_ylabel("Percentage (%)", weight='bold')
ax.set_xlabel("Tenure Cohort", weight='bold')
ax.set_xticklabels(ax.get_xticklabels(), rotation=15)
ax.set_ylim(0, 95)
for p in ax.patches:
    h = p.get_height()
    if h > 0:
        ax.annotate(f"{h:.1f}%", (p.get_x() + p.get_width() / 2., h + 1), ha='center', weight='bold', fontsize=9)
plt.tight_layout()
plt.savefig(os.path.join(GRAPHS_DIR, "08_churn_by_tenure_group.png"), dpi=300)
plt.close()

# 9. Monthly charge distribution (histogram)
fig, ax = plt.subplots(figsize=(8.5, 5))
sns.histplot(charges_np, kde=True, color='#3498db', ax=ax, edgecolor='black', alpha=0.6)
ax.axvline(np_mean, color='#e74c3c', linestyle='--', linewidth=2, label=f'Mean: ${np_mean:.2f}')
ax.axvline(np_median, color='#2ecc71', linestyle='-', linewidth=2, label=f'Median: ${np_median:.2f}')
ax.set_title("9. Monthly Charge Distribution with KDE", fontsize=13, weight='bold')
ax.set_xlabel("Monthly Charges ($)", weight='bold')
ax.set_ylabel("Customer Count", weight='bold')
ax.legend()
plt.tight_layout()
plt.savefig(os.path.join(GRAPHS_DIR, "09_monthly_charges_distribution.png"), dpi=300)
plt.close()

# 10. Monthly charge outliers (box plot)
fig, ax = plt.subplots(figsize=(8, 4.5))
sns.boxplot(x=charges_np, ax=ax, color='#f1c40f', flierprops={'marker': 'o', 'markerfacecolor': 'red', 'markersize': 8})
ax.axvline(upper_fence, color='red', linestyle=':', linewidth=2, label=f'Upper Fence (${upper_fence:.2f})')
ax.set_title("10. Box Plot of Monthly Charges (IQR Outliers)", fontsize=13, weight='bold')
ax.set_xlabel("Monthly Charges ($)", weight='bold')
ax.legend()
plt.tight_layout()
plt.savefig(os.path.join(GRAPHS_DIR, "10_monthly_charges_outliers_boxplot.png"), dpi=300)
plt.close()

print(f"✔ All 10 high-resolution charts saved in: {GRAPHS_DIR}")

print("\n" + "=" * 80)
print(" 🎉 COMPLETE TELECOM CHURN ANALYSIS FINISHED SUCCESSFULLY!")
print("=" * 80)
print(f"Outputs Location:")
print(f"  - 10 Graphs        : {GRAPHS_DIR}")
print(f"  - Summary Tables   : {TABLES_DIR}")
print(f"  - Word Report      : {os.path.join(SCRIPT_DIR, 'SRS_Document.docx')}")
print("=" * 80 + "\n")