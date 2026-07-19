import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title="Healing Circuits Budget Matrix", layout="wide")

st.title("📊 Healing Circuits Master P&L Multi-Stream Matrix")
st.markdown("Dynamic 36-Month financial model capturing granular coach cohort lifecycle metrics, integer-based graduate tracking, and scaling paybacks.")

# ==========================================
# 1. SIDEBAR CONFIGURATION - INTERACTIVE CONTROLS
# ==========================================
st.sidebar.header("🕹️ Dynamic Model Drivers")

# --- YEAR 1 CONTROLS ---
st.sidebar.markdown("### 📅 Year 1 Controls (Months 1-12)")
y1_coaches_mo = st.sidebar.slider("Y1: New Student Coaches / Month (C7)", 0, 40, 20)
y1_pts_per_coach = st.sidebar.slider("Y1: Patients per Coach / Month (C9)", 0, 15, 6)
y1_r11_pts = st.sidebar.slider("Y1: Self-Directed Patients / Month (C11)", 0, 100, 20)
y1_r12_pts = st.sidebar.slider("Y1: Facilitated Patients / Month (C12)", 0, 100, 30)

# --- YEAR 2 CONTROLS ---
st.sidebar.markdown("### 📅 Year 2 Controls (Months 13-24)")
y2_coaches_mo = st.sidebar.slider("Y2: New Student Coaches / Month (T7)", 0, 40, 20)
y2_pts_per_coach = st.sidebar.slider("Y2: Patients per Coach / Month (T9)", 0, 15, 6)
y2_r11_pts = st.sidebar.slider("Y2: Self-Directed Patients / Month (T11)", 0, 100, 20)
y2_r12_pts = st.sidebar.slider("Y2: Facilitated Patients / Month (T12)", 0, 100, 30)

# --- YEAR 3 CONTROLS ---
st.sidebar.markdown("### 📅 Year 3 Controls (Months 25-36)")
y3_coaches_mo = st.sidebar.slider("Y3: New Student Coaches / Month (AJ7)", 0, 40, 20)
y3_pts_per_coach = st.sidebar.slider("Y3: Patients per Coach / Month (AJ9)", 0, 15, 6)
y3_r11_pts = st.sidebar.slider("Y3: Self-Directed Patients / Month (AJ11)", 0, 100, 20)
y3_r12_pts = st.sidebar.slider("Y3: Facilitated Patients / Month (AJ12)", 0, 100, 30)

st.sidebar.write("---")
starting_cash = st.sidebar.number_input("Starting Capital Balance ($)", value=250000, step=50000)

# ==========================================
# 2. CALCULATION & LIFECYCLE FORECAST ENGINE
# ==========================================

months = np.arange(1, 37)

# Enforce strict integer arrays for headcounts
coaches_added = np.array([int(y1_coaches_mo)]*12 + [int(y2_coaches_mo)]*12 + [int(y3_coaches_mo)]*12)
pts_per_coach = np.array([int(y1_pts_per_coach)]*12 + [int(y2_pts_per_coach)]*12 + [int(y3_pts_per_coach)]*12)
r11_pts_vol = np.array([int(y1_r11_pts)]*12 + [int(y2_r11_pts)]*12 + [int(y3_r11_pts)]*12)
r12_pts_vol = np.array([int(y1_r12_pts)]*12 + [int(y2_r12_pts)]*12 + [int(y3_r12_pts)]*12)

corp_pts_vol = np.array([6]*12 + [15]*12 + [25]*12)

# Revenue tracking containers
rev_row5 = np.zeros(36)
rev_row6 = np.zeros(36)
rev_row10 = np.zeros(36)

new_student_coaches = np.zeros(36, dtype=int)
total_coaches_end = np.zeros(36, dtype=int)
total_coach_graduates = np.zeros(36, dtype=int)

cohort_matrix = np.zeros((36, 36), dtype=int)

for m in range(36):
    C = coaches_added[m]
    new_student_coaches[m] = C
    
    if C > 0:
        cohort_matrix[m, m] = C
        rev_row5[m] += C * 3000.0
        
        if m + 1 < 36:
            surviving_m1 = int(np.round(0.80 * C))
            cohort_matrix[m, m + 1] = surviving_m1
            rev_row5[m + 1] += surviving_m1 * 1500.0
            
        if m + 2 < 36:
            cohort_matrix[m, m + 2] = int(np.round(0.80 * C))
            
        if m + 3 < 36:
            coaches_graduating = int(np.round(0.64 * C))
            cohort_matrix[m, m + 3] = 0
            rev_row5[m + 3] += coaches_graduating * 1500.0
            
            for forward_month in range(m + 3, 36):
                total_coach_graduates[forward_month] += coaches_graduating

for m in range(36):
    total_coaches_end[m] = np.sum(cohort_matrix[:, m])

for m in range(36):
    active_grads = total_coach_graduates[m]
    rev_row6[m] = active_grads * pts_per_coach[m] * 3000.0
    
    if active_grads > 0:
        if pts_per_coach[m] == 1:
            rev_row10[m] = active_grads * 2000.0
        elif pts_per_coach[m] >= 2:
            rev_row10[m] = active_grads * 4000.0

rev_row11 = r11_pts_vol * 1000.0
rev_row12_curric = r12_pts_vol * 2000.0

rev_row15_corp = corp_pts_vol * 500.0
rev_row16_corp = corp_pts_vol * 500.0
rev_row17_corp = corp_pts_vol * 500.0
rev_row18_corp = corp_pts_vol * 500.0

total_gross_revenue = (
    rev_row5 + rev_row6 + rev_row10 + rev_row11 + rev_row12_curric +
    rev_row15_corp + rev_row16_corp + rev_row17_corp + rev_row18_corp
)

exp_ic_payouts = rev_row6 * 0.60
exp_merchant_processing = total_gross_revenue * 0.03
total_variable_cogs = exp_ic_payouts + exp_merchant_processing

fixed_payroll = 12500 + 2167
fixed_marketing = 12500
fixed_tech_saas = 500 + 500 + 1000
fixed_professional_fees = 1500 + 1200 + 1000
monthly_fixed_overhead = fixed_payroll + fixed_marketing + fixed_tech_saas + fixed_professional_fees

total_operating_exp = total_variable_cogs + monthly_fixed_overhead
net_income_profile = total_gross_revenue - total_operating_exp

cash_runway = np.zeros(36)
current_bank = starting_cash
for m in range(36):
    current_bank += net_income_profile[m]
    cash_runway[m] = current_bank

# ==========================================
# 3. INTERFACE PRESENTATION LAYER
# ==========================================

col_a, col_b, col_c = st.columns(3)
col_a.metric("Total 36-Mo Revenue Projection", f"${total_gross_revenue.sum():,.2f}")
col_b.metric("Total 36-Mo Opex Outflow", f"${total_operating_exp.sum():,.2f}")
col_c.metric("Projected Capital Reserves", f"${cash_runway[-1]:,.2f}")

st.write("---")

annual_matrix = {
    "Metrics & Financial Line Items": [
        "TOTAL COMPOSITE INCOME INFLOW",
        "├── Row 5: Student Coach Trainings (@ $10k)",
        "├── Row 6: Coach-Led Direct Deliveries (@ $3k)",
        "├── Row 10: Graduate Training Payback Revenue ($2k x 2 Pts)",
        "├── Row 11: Self-Directed Group Programs (@ $1k)",
        "├── Row 12: Facilitated Curriculums (@ $2k)",
        "└── Rows 15-18: Combined Institutional Corporate Payers",
        "├── Less: Variable IC Coach Compensation (60%)",
        "├── Less: Variable Credit Card Merchant Fees (3%)",
        "├── Less: Fixed Operational General Overhead Burden",
        "NET TOTAL BUSINESS OPERATING PROFIT"
    ],
    "Year 1 Summary": [
        total_gross_revenue[0:12].sum(),
        rev_row5[0:12].sum(), rev_row6[0:12].sum(), rev_row10[0:12].sum(), rev_row11[0:12].sum(), rev_row12_curric[0:12].sum(),
        (rev_row15_corp[0:12].sum() + rev_row16_corp[0:12].sum() + rev_row17_corp[0:12].sum() + rev_row18_corp[0:12].sum()),
        -exp_ic_payouts[0:12].sum(), -exp_merchant_processing[0:12].sum(),
        -(monthly_fixed_overhead*12), net_income_profile[0:12].sum()
    ],
    "Year 2 Summary": [
        total_gross_revenue[12:24].sum(),
        rev_row5[12:24].sum(), rev_row6[12:24].sum(), rev_row10[12:24].sum(), rev_row11[12:24].sum(), rev_row12_curric[12:24].sum(),
        (rev_row15_corp[12:24].sum() + rev_row16_corp[12:24].sum() + rev_row17_corp[12:24].sum() + rev_row18_corp[12:24].sum()),
        -exp_ic_payouts[12:24].sum(), -exp_merchant_processing[12:24].sum(),
        -(monthly_fixed_overhead*12), net_income_profile[12:24].sum()
    ],
    "Year 3 Summary": [
        total_gross_revenue[24:36].sum(),
        rev_row5[24:36].sum(), rev_row6[24:36].sum(), rev_row10[24:36].sum(), rev_row11[24:36].sum(), rev_row12_curric[24:36].sum(),
        (rev_row15_corp[24:36].sum() + rev_row16_corp[24:36].sum() + rev_row17_corp[24:36].sum() + rev_row18_corp[24:36].sum()),
        -exp_ic_payouts[24:36].sum(), -exp_merchant_processing[24:36].sum(),
        -(monthly_fixed_overhead*12), net_income_profile[24:36].sum()
    ]
}

# Convert directory data to dataframe and format columns as currency cleanly
df_annual = pd.DataFrame(annual_matrix).set_index("Metrics & Financial Line Items")
st.table(df_annual.style.format("${:,.2f}"))

st.write("---")

# ==========================================
# 4. AREA CHART COMPONENT
# ==========================================
st.subheader("📈 Multi-Stream Revenue Contribution Mix")
df_monthly_chart = pd.DataFrame({
    "Month": months,
    "Coach Training (R5)": rev_row5,
    "Coach-Led Vol (R6)": rev_row6,
    "Coach Paybacks (R10)": rev_row10,
    "Self-Directed (R11)": rev_row11,
    "Facilitated (R12)": rev_row12_curric,
    "B2B Corporate (R15-18)": rev_row15_corp + rev_row16_corp + rev_row17_corp + rev_row18_corp
}).set_index("Month")

st.area_chart(df_monthly_chart, use_container_width=True)

st.write("---")

st.subheader("📅 Complete 36-Month Operational Matrix Ledger View")
df_monthly_ledger = pd.DataFrame({
    "Month": [f"Month {i}" for i in months],
    "Line 5: New Student Coaches (Month N)": new_student_coaches,
    "Line 6: Total Coaches (End of Month)": total_coaches_end,
    "Line 8: Total Coach Graduates (End of Month)": total_coach_graduates,
    "Line 5 Rev": rev_row5,
    "Line 6 Rev": rev_row6,
    "Line 10 Payback": rev_row10,
    "Line 11 Rev": rev_row11,
    "Line 12 Rev": rev_row12_curric,
    "TOTAL GROSS INCOME": total_gross_revenue,
    "Variable COGS": total_variable_cogs,
    "NET OPERATING OUTCOME": net_income_profile,
    "CASH BANK BALANCE": cash_runway
})

with st.expander("Click to open the raw monthly operating database view"):
    st.dataframe(df_monthly_ledger.style.format({c: "${:,.2f}" for c in df_monthly_ledger.columns if not "Coaches" in c and not "Graduates" in c and c != "Month"}), use_container_width=True)
