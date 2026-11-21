"""
========================================================================================
TELECOM CUSTOMER CHURN ANALYSIS - INTERACTIVE STREAMLIT DASHBOARD
Course Project: Computer Science Engineering (First Year Python Project)
Author: Student Data Analyst & Software Developer
Dataset: 06_customer_churn.csv
========================================================================================
"""

import os
import numpy as np
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns

# Set Streamlit Page Configuration
st.set_page_config(
    page_title="Telecom Customer Churn Analytics",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Styling for polished dashboard aesthetic
st.markdown("""
<style>
    .main-header {
        font-size: 2.2rem;
        font-weight: 700;
        color: #1E3A8A;
        margin-bottom: 0.2rem;
    }
    .sub-header {
        font-size: 1.05rem;
        color: #4B5563;
        margin-bottom: 1.5rem;
    }
    .metric-card {
        background-color: #F8FAFC;
        border: 1px solid #E2E8F0;
        border-radius: 8px;
        padding: 1rem;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
    }
    .badge-churn {
        background-color: #FEE2E2;
        color: #991B1B;
        padding: 0.2rem 0.5rem;
        border-radius: 4px;
        font-weight: 600;
    }
    .badge-retained {
        background-color: #DCFCE7;
        color: #166534;
        padding: 0.2rem 0.5rem;
        border-radius: 4px;
        font-weight: 600;
    }
</style>
""", unsafe_allow_html=True)


# ======================================================================================
# DATA LOADING & CLEANING (CACHED)
# ======================================================================================
@st.cache_data
def load_and_clean_data():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    csv_path = os.path.join(base_dir, "data", "06_customer_churn.csv")
    
    # Fallback paths
    if not os.path.exists(csv_path):
        csv_path = "06_customer_churn.csv"
        
    df = pd.read_csv(csv_path)
    
    # Impute missing Monthly_Charges using median
    median_charges = df['Monthly_Charges'].median()
    df['Monthly_Charges'] = df['Monthly_Charges'].fillna(median_charges)
    
    # Treat missing Internet_Service as Unknown
    df['Internet_Service'] = df['Internet_Service'].fillna('Unknown')
    
    # Create Tenure Cohorts
    bins = [0, 12, 24, 48, 72]
    labels = ['0-12 Months', '13-24 Months', '25-48 Months', '49-72 Months']
    df['Tenure_Group'] = pd.cut(df['Tenure_Months'], bins=bins, labels=labels, right=True)
    
    return df, median_charges


df_full, median_charges = load_and_clean_data()


# ======================================================================================
# SIDEBAR FILTERS
# ======================================================================================
st.sidebar.image("https://img.icons8.com/color/96/telecom.png", width=70)
st.sidebar.title("Filter Customers")
st.sidebar.markdown("Use these interactive controls to slice and analyze customer segments:")

# Contract Filter
all_contracts = sorted(df_full['Contract'].unique().tolist())
selected_contracts = st.sidebar.multiselect(
    "Contract Type:",
    options=all_contracts,
    default=all_contracts
)

# Internet Service Filter
all_internet = sorted(df_full['Internet_Service'].unique().tolist())
selected_internet = st.sidebar.multiselect(
    "Internet Service:",
    options=all_internet,
    default=all_internet
)

# Payment Method Filter
all_payments = sorted(df_full['Payment_Method'].unique().tolist())
selected_payments = st.sidebar.multiselect(
    "Payment Method:",
    options=all_payments,
    default=all_payments
)

# Tenure Range Slider
min_tenure = int(df_full['Tenure_Months'].min())
max_tenure = int(df_full['Tenure_Months'].max())
tenure_range = st.sidebar.slider(
    "Customer Tenure (Months):",
    min_value=min_tenure,
    max_value=max_tenure,
    value=(min_tenure, max_tenure)
)

# Monthly Charges Range Slider
min_charge = float(df_full['Monthly_Charges'].min())
max_charge = float(df_full['Monthly_Charges'].max())
charge_range = st.sidebar.slider(
    "Monthly Charges ($):",
    min_value=float(np.floor(min_charge)),
    max_value=float(np.ceil(max_charge)),
    value=(float(np.floor(min_charge)), float(np.ceil(max_charge)))
)

# Apply Filters
filtered_df = df_full[
    (df_full['Contract'].isin(selected_contracts)) &
    (df_full['Internet_Service'].isin(selected_internet)) &
    (df_full['Payment_Method'].isin(selected_payments)) &
    (df_full['Tenure_Months'] >= tenure_range[0]) &
    (df_full['Tenure_Months'] <= tenure_range[1]) &
    (df_full['Monthly_Charges'] >= charge_range[0]) &
    (df_full['Monthly_Charges'] <= charge_range[1])
]

# Reset filters button
if st.sidebar.button("🔄 Reset All Filters"):
    st.rerun()

st.sidebar.markdown("---")
st.sidebar.info("💡 **Academic Project:** First Year Computer Science Engineering\n\n**Dataset:** Telecom Customer Churn (500 records)")


# ======================================================================================
# MAIN HEADER & KPI DASHBOARD CARDS
# ======================================================================================
st.markdown('<div class="main-header">Telecom Customer Churn Analytics Dashboard</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Interactive exploratory data analysis & business intelligence for telecom customer retention.</div>', unsafe_allow_html=True)

# Calculate dynamic KPIs based on filtered data
total_filtered = len(filtered_df)
churn_count = (filtered_df['Churn'] == 'Yes').sum()
retained_count = (filtered_df['Churn'] == 'No').sum()

if total_filtered > 0:
    churn_rate = (churn_count / total_filtered) * 100
    retention_rate = (retained_count / total_filtered) * 100
    avg_tenure = filtered_df['Tenure_Months'].mean()
    avg_charges = filtered_df['Monthly_Charges'].mean()
else:
    churn_rate = 0.0
    retention_rate = 0.0
    avg_tenure = 0.0
    avg_charges = 0.0

col1, col2, col3, col4, col5 = st.columns(5)
with col1:
    st.metric("Total Customers", f"{total_filtered:,}", f"{total_filtered/len(df_full)*100:.0f}% of total" if total_filtered > 0 else "")
with col2:
    st.metric("Churned Customers", f"{churn_count:,}", f"{churn_rate:.1f}% Churn Rate", delta_color="inverse")
with col3:
    st.metric("Retained Customers", f"{retained_count:,}", f"{retention_rate:.1f}% Retention", delta_color="normal")
with col4:
    st.metric("Average Tenure", f"{avg_tenure:.1f} Mo.", f"~{avg_tenure/12:.1f} Years")
with col5:
    st.metric("Avg Monthly Bill", f"${avg_charges:.2f}", f"Median: ${median_charges:.2f}")

st.markdown("---")


# ======================================================================================
# TABS FOR STRUCTURED EXPLORATION
# ======================================================================================
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📈 Churn Drivers Analysis",
    "💵 Financial & Outliers",
    "⏱️ Tenure & Loyalty",
    "📋 Segment Summary & Raw Data",
    "💡 Strategic Recommendations"
])

colors = {'No': '#2ecc71', 'Yes': '#e74c3c'}

if total_filtered == 0:
    st.warning("⚠️ No customer records match the current filter criteria. Please adjust your sidebar filters.")
else:
    # ----------------------------------------------------------------------------------
    # TAB 1: CHURN DRIVERS ANALYSIS
    # ----------------------------------------------------------------------------------
    with tab1:
        st.subheader("Key Drivers of Customer Churn")
        
        c1, c2 = st.columns(2)
        with c1:
            st.markdown("#### Overall Churn Distribution")
            fig, ax = plt.subplots(figsize=(6, 5))
            wedges, texts, autotexts = ax.pie(
                [retained_count, churn_count],
                labels=['Retained (No)', 'Churned (Yes)'],
                autopct='%1.1f%%',
                startangle=140,
                colors=[colors['No'], colors['Yes']],
                explode=(0, 0.07),
                textprops={'fontsize': 11, 'weight': 'bold'}
            )
            for at in autotexts:
                at.set_color('white')
            ax.set_title(f"Customer Churn Distribution (N={total_filtered})", fontsize=12, weight='bold')
            st.pyplot(fig)
            plt.close()
            
        with c2:
            st.markdown("#### Churn by Contract Type")
            fig, ax = plt.subplots(figsize=(6, 5))
            contract_data = pd.crosstab(filtered_df['Contract'], filtered_df['Churn'], normalize='index') * 100
            contract_data.plot(kind='bar', color=[colors.get(c, '#999') for c in contract_data.columns], ax=ax, edgecolor='black', alpha=0.9)
            ax.set_ylabel("Percentage (%)", fontsize=11, weight='bold')
            ax.set_xlabel("Contract Type", fontsize=11, weight='bold')
            ax.set_xticklabels(ax.get_xticklabels(), rotation=0)
            ax.legend(["Retained (No)", "Churned (Yes)"], title="Churn Status")
            for p in ax.patches:
                h = p.get_height()
                if h > 0:
                    ax.annotate(f"{h:.1f}%", (p.get_x() + p.get_width() / 2., h + 1), ha='center', fontsize=9, weight='bold')
            ax.set_ylim(0, 100)
            st.pyplot(fig)
            plt.close()

        c3, c4 = st.columns(2)
        with c3:
            st.markdown("#### Churn by Internet Service")
            fig, ax = plt.subplots(figsize=(6, 5))
            net_data = pd.crosstab(filtered_df['Internet_Service'], filtered_df['Churn'], normalize='index') * 100
            net_data.plot(kind='bar', color=[colors.get(c, '#999') for c in net_data.columns], ax=ax, edgecolor='black', alpha=0.9)
            ax.set_ylabel("Percentage (%)", fontsize=11, weight='bold')
            ax.set_xlabel("Internet Service", fontsize=11, weight='bold')
            ax.set_xticklabels(ax.get_xticklabels(), rotation=0)
            ax.legend(["Retained (No)", "Churned (Yes)"], title="Churn Status")
            for p in ax.patches:
                h = p.get_height()
                if h > 0:
                    ax.annotate(f"{h:.1f}%", (p.get_x() + p.get_width() / 2., h + 1), ha='center', fontsize=9, weight='bold')
            ax.set_ylim(0, 100)
            st.pyplot(fig)
            plt.close()

        with c4:
            st.markdown("#### Churn by Payment Method")
            fig, ax = plt.subplots(figsize=(6, 5))
            pay_data = pd.crosstab(filtered_df['Payment_Method'], filtered_df['Churn'], normalize='index') * 100
            pay_data.plot(kind='bar', color=[colors.get(c, '#999') for c in pay_data.columns], ax=ax, edgecolor='black', alpha=0.9)
            ax.set_ylabel("Percentage (%)", fontsize=11, weight='bold')
            ax.set_xlabel("Payment Method", fontsize=11, weight='bold')
            ax.set_xticklabels(ax.get_xticklabels(), rotation=0)
            ax.legend(["Retained (No)", "Churned (Yes)"], title="Churn Status")
            for p in ax.patches:
                h = p.get_height()
                if h > 0:
                    ax.annotate(f"{h:.1f}%", (p.get_x() + p.get_width() / 2., h + 1), ha='center', fontsize=9, weight='bold')
            ax.set_ylim(0, 100)
            st.pyplot(fig)
            plt.close()

    # ----------------------------------------------------------------------------------
    # TAB 2: FINANCIAL & OUTLIERS
    # ----------------------------------------------------------------------------------
    with tab2:
        st.subheader("Monthly Charges & Outlier Detection (NumPy & IQR)")
        
        c1, c2 = st.columns(2)
        with c1:
            st.markdown("#### Monthly Charge Distribution")
            fig, ax = plt.subplots(figsize=(6, 5))
            charges = filtered_df['Monthly_Charges'].to_numpy()
            sns.histplot(charges, kde=True, color='#3498db', ax=ax, edgecolor='black', alpha=0.6)
            if len(charges) > 0:
                ax.axvline(np.mean(charges), color='red', linestyle='--', label=f"Mean: ${np.mean(charges):.2f}")
                ax.axvline(np.median(charges), color='green', linestyle='-', label=f"Median: ${np.median(charges):.2f}")
            ax.set_xlabel("Monthly Charges ($)", weight='bold')
            ax.set_ylabel("Customer Count", weight='bold')
            ax.legend()
            st.pyplot(fig)
            plt.close()

        with c2:
            st.markdown("#### Outliers Box Plot (IQR Method)")
            fig, ax = plt.subplots(figsize=(6, 5))
            sns.boxplot(x=filtered_df['Monthly_Charges'], ax=ax, color='#f1c40f', flierprops={'marker': 'o', 'markerfacecolor': 'red', 'markersize': 8})
            
            # Global IQR fence
            q1 = np.percentile(df_full['Monthly_Charges'], 25)
            q3 = np.percentile(df_full['Monthly_Charges'], 75)
            iqr = q3 - q1
            upper_fence = q3 + 1.5 * iqr
            ax.axvline(upper_fence, color='red', linestyle=':', label=f"Upper Fence: ${upper_fence:.2f}")
            ax.set_xlabel("Monthly Charges ($)", weight='bold')
            ax.legend()
            st.pyplot(fig)
            plt.close()

        # Outlier details table
        outliers_in_filtered = filtered_df[filtered_df['Monthly_Charges'] > upper_fence]
        st.markdown(f"**Identified High-Charge Outliers (> ${upper_fence:.2f})**: {len(outliers_in_filtered)} Customers")
        if len(outliers_in_filtered) > 0:
            st.dataframe(outliers_in_filtered[['Customer_ID', 'Tenure_Months', 'Contract', 'Monthly_Charges', 'Internet_Service', 'Payment_Method', 'Churn']])

    # ----------------------------------------------------------------------------------
    # TAB 3: TENURE & LOYALTY
    # ----------------------------------------------------------------------------------
    with tab3:
        st.subheader("Customer Tenure & Support Ticket Impact")
        
        c1, c2 = st.columns(2)
        with c1:
            st.markdown("#### Average Tenure by Churn Status")
            fig, ax = plt.subplots(figsize=(6, 5))
            tenure_by_churn = filtered_df.groupby('Churn')['Tenure_Months'].mean()
            if 'No' in tenure_by_churn and 'Yes' in tenure_by_churn:
                bars = ax.bar(['Retained (No)', 'Churned (Yes)'], [tenure_by_churn['No'], tenure_by_churn['Yes']],
                              color=[colors['No'], colors['Yes']], edgecolor='black', width=0.5)
                for b in bars:
                    h = b.get_height()
                    ax.annotate(f"{h:.1f} Mo.", (b.get_x() + b.get_width() / 2., h / 2),
                                ha='center', va='center', color='white', weight='bold', fontsize=12)
            ax.set_ylabel("Mean Tenure (Months)", weight='bold')
            ax.set_ylim(0, 45)
            st.pyplot(fig)
            plt.close()

        with c2:
            st.markdown("#### Churn Rate by Tenure Cohort")
            fig, ax = plt.subplots(figsize=(6, 5))
            if 'Tenure_Group' in filtered_df.columns:
                t_grp_data = pd.crosstab(filtered_df['Tenure_Group'], filtered_df['Churn'], normalize='index') * 100
                t_grp_data.plot(kind='bar', color=[colors.get(c, '#999') for c in t_grp_data.columns], ax=ax, edgecolor='black', alpha=0.9)
                ax.set_ylabel("Percentage (%)", weight='bold')
                ax.set_xlabel("Tenure Cohort", weight='bold')
                ax.set_xticklabels(ax.get_xticklabels(), rotation=15)
                ax.legend(["Retained (No)", "Churned (Yes)"], title="Churn Status")
                for p in ax.patches:
                    h = p.get_height()
                    if h > 0:
                        ax.annotate(f"{h:.1f}%", (p.get_x() + p.get_width() / 2., h + 1), ha='center', fontsize=9, weight='bold')
                ax.set_ylim(0, 100)
            st.pyplot(fig)
            plt.close()

        st.markdown("#### Support Ticket Frequency Impact")
        fig, ax = plt.subplots(figsize=(10, 4))
        ticket_cross = pd.crosstab(filtered_df['Support_Tickets'], filtered_df['Churn'], normalize='index') * 100
        if 'Yes' in ticket_cross.columns:
            ticket_cross['Yes'].plot(kind='line', marker='o', color='#e74c3c', linewidth=2.5, markersize=8, ax=ax, label="Churn Rate (%)")
            for x, y in zip(ticket_cross.index, ticket_cross['Yes']):
                ax.annotate(f"{y:.1f}%", (x, y + 2), ha='center', weight='bold')
            ax.set_ylabel("Churn Rate (%)", weight='bold')
            ax.set_xlabel("Number of Support Tickets Filed", weight='bold')
            ax.set_title("Escalating Churn Risk with Support Tickets", weight='bold')
            ax.set_ylim(0, 70)
            ax.grid(True, linestyle='--', alpha=0.7)
            st.pyplot(fig)
            plt.close()

    # ----------------------------------------------------------------------------------
    # TAB 4: SEGMENT SUMMARY & RAW DATA
    # ----------------------------------------------------------------------------------
    with tab4:
        st.subheader("Segment Analysis & Aggregated Summary")
        
        summary_agg = filtered_df.groupby(['Contract', 'Internet_Service']).agg(
            Total_Customers=('Customer_ID', 'count'),
            Churned=('Churn', lambda x: (x == 'Yes').sum()),
            Retained=('Churn', lambda x: (x == 'No').sum()),
            Churn_Rate_Pct=('Churn', lambda x: round((x == 'Yes').mean() * 100, 2)),
            Avg_Tenure_Months=('Tenure_Months', lambda x: round(x.mean(), 1)),
            Avg_Monthly_Bill=('Monthly_Charges', lambda x: round(x.mean(), 2)),
            Avg_Support_Tickets=('Support_Tickets', lambda x: round(x.mean(), 2))
        ).reset_index()
        
        st.dataframe(summary_agg, use_container_width=True)
        
        st.markdown("#### Filtered Customer Dataset")
        st.dataframe(filtered_df, use_container_width=True)
        
        # Download button for filtered CSV
        csv_download = filtered_df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Download Filtered Data as CSV",
            data=csv_download,
            file_name="telecom_filtered_customers.csv",
            mime="text/csv"
        )

    # ----------------------------------------------------------------------------------
    # TAB 5: STRATEGIC RECOMMENDATIONS
    # ----------------------------------------------------------------------------------
    with tab5:
        st.subheader("Data-Backed Customer Retention Strategy")
        
        recs = [
            ("1. Multi-Year Contract Incentives",
             "Two-year contracts produce the lowest churn rate (22.81%). Introduce structured incentives (10% bill discounts, bundled OTT subscriptions) to migrate users away from high-churn 1-year (30.25%) and monthly contracts.",
             "🎯 Target: Customers on Month-to-Month & 1-Year plans"),
            ("2. Proactive 90-Day Early-Tenure Onboarding",
             "Customers in Year 1 & Year 2 exhibit churn rates of ~28% - 30%, which significantly stabilizes to 22.78% in Year 5-6. Implement automated onboarding check-ins, satisfaction calls, and loyalty milestone rewards at 6 and 12 months.",
             "🎯 Target: Customers with tenure ≤ 24 months"),
            ("3. DSL Infrastructure Modernization & Fiber Migration",
             "DSL subscribers have the highest churn rate (28.99%) compared to Fiber (24.69%). Offer complimentary Fiber equipment upgrades and transitional bill credits to eliminate speed and reliability churn.",
             "🎯 Target: All active DSL subscribers"),
            ("4. Bill-Shock Audits & Modular Plan Right-Sizing",
             "Churned customers pay higher average monthly charges ($762.17) compared to retained customers ($747.22). Extremely high outliers (> $1,300/mo) are vulnerable to defection. Establish proactive usage audits to ensure plan-fit.",
             "🎯 Target: High-spend accounts (> $900/month)"),
            ("5. 'Red-Flag' Ticket Escalation Protocol",
             "Customers logging 4 or 5 support tickets suffer a drastic 43%-50% churn rate. Route any account with ≥ 3 tickets directly to a senior technical support specialist and issue immediate courtesy service credits.",
             "🎯 Target: Accounts with ≥ 3 support tickets")
        ]
        
        for title, desc, target in recs:
            st.markdown(f"### {title}")
            st.write(desc)
            st.info(target)
            st.markdown("---")
