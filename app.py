import streamlit as st
import pandas as pd

st.set_page_config(page_title="Healing Circuits 3-Year Financial Engine", layout="wide")

st.title("🚀 Healing Circuits 3-Year Financial Sensitivity Engine")
st.markdown("Analyze financial performance segmented into three 12-month periods (Year 1, Year 2, Year 3). Toggle inputs per year or use presets to see the compound growth.")

# ==========================================
# 1. SIDEBAR - MULTI-YEAR INPUT DRIVERS
# ==========================================
st.sidebar.header("🕹️ Multi-Year Driver Controls")

preset = st.sidebar.selectbox("Load Scenario Preset", ["Low Baseline", "Mid Growth", "High Scale", "Custom Matrix"])

# Predefined multi-year driver presets
presets = {
    "Low Baseline": {
        "yr1": {"new_coaches": 8, "total_coaches": 10, "pts_per_coach": 3, "pkg_price": 2500},
        "yr2": {"new_coaches": 12, "total_coaches": 20, "pts_per_coach": 4, "pkg_price": 2500},
        "yr3": {"new_coaches": 15, "total_coaches": 32, "pts_per_coach": 5, "pkg_price": 2500},
    },
    "Mid Growth": {
        "yr1": {"new_coaches": 12, "total_coaches": 17, "pts_per_coach": 6, "pkg_price": 3000},
        "yr2": {"new_coaches": 20, "total_coaches": 35, "pts_per_coach": 7, "pkg_price": 3000},
        "yr3": {"new_coaches": 30, "total_coaches": 60, "pts_per_coach": 8, "pkg_price": 3000},
    },
    "High Scale": {
        "yr1": {"new_coaches": 45, "total_coaches": 50, "pts_per_coach": 12, "pkg_price": 3500},
        "yr2": {"new_coaches": 75, "total_coaches": 120, "pts_per_coach": 14, "pkg_price": 3500},
        "yr3": {"new_coaches": 120, "total_coaches": 230, "pts_per_coach": 15, "pkg_price": 3500},
    }
}

# Render inputs based on preset selection
with st.sidebar.expander("📅 Year 1 Drivers", expanded=True):
    if preset != "Custom Matrix":
        y1_defaults = presets[preset]["yr1"]
        y1_new_coaches = st.slider("Y1 New Coaches Trained", 0, 150, y1_defaults["new_coaches"], key="y1_nc")
        y1_total_coaches = st.number_input("Y1 Total Active Coaches", value=y1_defaults["total_coaches"], key="y1_tc")
        y1_pts_per_coach = st.slider("Y1 Patients per Coach", 1, 25, y1_defaults["pts_per_coach"], key="y1_ppc")
        y1_pkg_price = st.slider("Y1 Patient Package Price ($)", 1000, 5000, y1_defaults["pkg_price"], step=250, key="y1_price")
    else:
        y1_new_coaches = st.slider("Y1 New Coaches Trained", 0, 150, 8, key="y1_nc")
        y1_total_coaches = st.number_input("Y1 Total Active Coaches", value=10, key="y1_tc")
        y1_pts_per_coach = st.slider("Y1 Patients per Coach", 1, 25, 3, key="y1_ppc")
        y1_pkg_price = st.slider("Y1 Patient Package Price ($)", 1000, 5000, 2500, step=250, key="y1_price")

with st.sidebar.expander("📅 Year 2 Drivers", expanded=False):
    if preset != "Custom Matrix":
        y2_defaults = presets[preset]["yr2"]
        y2_new_coaches = st.slider("Y2 New Coaches Trained", 0, 150, y2_defaults["new_coaches"], key="y2_nc")
        y2_total_coaches = st.number_input("Y2 Total Active Coaches", value=y2_defaults["total_coaches"], key="y2_tc")
        y2_pts_per_coach = st.slider("Y2 Patients per Coach", 1, 25, y2_defaults["pts_per_coach"], key="y2_ppc")
        y2_pkg_price = st.slider("Y2 Patient Package Price ($)", 1000, 5000, y2_defaults["pkg_price"], step=250, key="y2_price")
    else:
        y2_new_coaches = st.slider("Y2 New Coaches Trained", 0, 150, 12, key="y2_nc")
        y2_total_coaches = st.number_input("Y2 Total Active Coaches", value=20, key="y2_tc")
        y2_pts_per_coach = st.slider("Y2 Patients per Coach", 1, 25, 4, key="y2_ppc")
        y2_pkg_price = st.slider("Y2 Patient Package Price ($)", 1000, 5000, 2500, step=250, key="y2_price")

with st.sidebar.expander("📅 Year 3 Drivers", expanded=False):
    if preset != "Custom Matrix":
        y3_defaults = presets[preset]["yr3"]
        y3_new_coaches = st.slider("Y3 New Coaches Trained", 0, 150, y3_defaults["new_coaches"], key="y3_nc")
        y3_total_coaches = st.number_input("Y3 Total Active Coaches", value=y3_defaults["total_coaches"], key="y3_tc")
        y3_pts_per_coach = st.slider("Y3 Patients per Coach", 1, 25, y3_defaults["pts_per_coach"], key="y3_ppc")
        y3_pkg_price = st.slider("Y3 Patient Package Price ($)", 1000, 5000, y3_defaults["pkg_price"], step=250, key="y3_price")
    else:
        y3_new_coaches = st.slider("Y3 New Coaches Trained", 0, 150, 15, key="y3_nc")
        y3_total_coaches = st.number_input("Y3 Total Active Coaches", value=32, key="y3_tc")
        y3_pts_per_coach = st.slider("Y3 Patients per Coach", 1, 25, 5, key="y3_ppc")
        y3_pkg_price = st.slider("Y3 Patient Package Price ($)", 1000, 5000, 2500, step=250, key="y3_price")

st.sidebar.write("---")
st.sidebar.markdown("**Global Cost Settings:**")
coach_payout_pct = st.sidebar.slider("IC Coach Revenue Share (%)", 40, 70, 60)

# ==========================================
# 2. FINANCIAL CALCULATIONS ENGINE
# ==========================================
def calculate_year_projection(new_coaches, total_coaches, pts_per_coach, price, payout_pct):
    # Calculations based on monthly calculations scaled to 12 months
    
    # --- REVENUE STREAMS (Annualized) ---
    # Coach Training (cohort intake happens during the year)
    rev_coach_training = new_coaches * 10000.0
    
    # Patient Packages (monthly volume times 12)
    total_active_patients = total_coaches * pts_per_coach
    rev_patient_packages = total_active_patients * price * 12
    
    # SaaS Licensing Fee ($200/mo fee per active coach times 12)
    rev_saas_licensing = total_coaches * 200.0 * 12
    
    gross_annual_revenue = rev_coach_training + rev_patient_packages + rev_saas_licensing
    
    # --- VARIABLE COSTS (Annualized COGS) ---
    cogs_coach_payouts = rev_patient_packages * (payout_pct / 100.0)
    cogs_merchant_fees = gross_annual_revenue * 0.03
    total_variable_costs = cogs_coach_payouts + cogs_merchant_fees
    
    # --- FIXED OVERHEAD BURDEN (Annualized: Monthly * 12) ---
    fixed_personnel = (12500 + 2167) * 12
    fixed_marketing = 12500 * 12
    fixed_tech_saas = (500 + 500 + 1000) * 12
    fixed_professional = (1500 + 1200 + 1000) * 12
    total_fixed_overhead = fixed_personnel + fixed_marketing + fixed_tech_saas + fixed_professional
    
    # --- TOTAL NETS ---
    total_expenses = total_variable_costs + total_fixed_overhead
    net_profit = gross_annual_revenue - total_expenses
    margin = (net_profit / gross_annual_revenue) * 100 if gross_annual_revenue > 0 else 0
    
    return {
        "Rev_Training": rev_coach_training,
        "Rev_Patients": rev_patient_packages,
        "Rev_SaaS": rev_saas_licensing,
        "Gross_Revenue": gross_annual_revenue,
        "Cost_Payouts": cogs_coach_payouts,
        "Cost_Merchant": cogs_merchant_fees,
        "Total_Variable": total_variable_costs,
        "Total_Fixed": total_fixed_overhead,
        "Total_Expenses": total_expenses,
        "Net_Profit": net_profit,
        "Margin_Pct": margin,
        "Active_Patients": total_active_patients
    }

# Run engine for all three years
y1_data = calculate_year_projection(y1_new_coaches, y1_total_coaches, y1_pts_per_coach, y1_pkg_price, coach_payout_pct)
y2_data = calculate_year_projection(y2_new_coaches, y2_total_coaches, y2_pts_per_coach, y2_pkg_price, coach_payout_pct)
y3_data = calculate_year_projection(y3_new_coaches, y3_total_coaches, y3_pts_per_coach, y3_pkg_price, coach_payout_pct)

# ==========================================
# 3. INTERACTIVE LAYOUT & VISUALS
# ==========================================

# Toggle View Mode
view_mode = st.radio("Select View Mode", ["Annualized Totals", "Monthly Averages"], horizontal=True)

# Helper function to divide by 12 if monthly view selected
def format_val(val, as_currency=True):
    factor = 12.0 if view_mode == "Monthly Averages" else 1.0
    adjusted = val / factor
    if as_currency:
        return f"${adjusted:,.2f}"
    return f"{adjusted:,.1f}"

# Metric Headers
col_y1, col_y2, col_y3 = st.columns(3)

with col_y1:
    st.subheader("📅 Year 1 Segment")
    st.metric("Gross Revenue", format_val(y1_data['Gross_Revenue']), delta=f"{y1_data['Margin_Pct']:.1f}% Net Margin")
    st.metric("Total Expenses", format_val(y1_data['Total_Expenses']))
    st.metric("Net Income", format_val(y1_data['Net_Profit']))

with col_y2:
    st.subheader("📅 Year 2 Segment")
    st.metric("Gross Revenue", format_val(y2_data['Gross_Revenue']), delta=f"{y2_data['Margin_Pct']:.1f}% Net Margin")
    st.metric("Total Expenses", format_val(y2_data['Total_Expenses']))
    st.metric("Net Income", format_val(y2_data['Net_Profit']))

with col_y3:
    st.subheader("📅 Year 3 Segment")
    st.metric("Gross Revenue", format_val(y3_data['Gross_Revenue']), delta=f"{y3_data['Margin_Pct']:.1f}% Net Margin")
    st.metric("Total Expenses", format_val(y3_data['Total_Expenses']))
    st.metric("Net Income", format_val(y3_data['Net_Profit']))

st.write("---")

# Visual chart comparisons
col_chart_left, col_chart_right = st.columns(2)

with col_chart_left:
    st.subheader("📈 Revenue Inflow Streams Comparison")
    # Prepare comparison dataframe
    factor = 12.0 if view_mode == "Monthly Averages" else 1.0
    comparison_df = pd.DataFrame({
        "Segment": ["Year 1", "Year 1", "Year 1", "Year 2", "Year 2", "Year 2", "Year 3", "Year 3", "Year 3"],
        "Revenue Line Item": ["Coach Training", "Patient Packages", "SaaS Licensing"] * 3,
        "Value ($)": [
            y1_data['Rev_Training']/factor, y1_data['Rev_Patients']/factor, y1_data['Rev_SaaS']/factor,
            y2_data['Rev_Training']/factor, y2_data['Rev_Patients']/factor, y2_data['Rev_SaaS']/factor,
            y3_data['Rev_Training']/factor, y3_data['Rev_Patients']/factor, y3_data['Rev_SaaS']/factor
        ]
    })
    st.bar_chart(data=comparison_df, x="Segment", y="Value ($)", color="Revenue Line Item", use_container_width=True)

with col_chart_right:
    st.subheader("📉 Cost Outflow Structuring Comparison")
    comparison_costs_df = pd.DataFrame({
        "Segment": ["Year 1", "Year 1", "Year 1", "Year 2", "Year 2", "Year 2", "Year 3", "Year 3", "Year 3"],
        "Cost Tier": ["Fixed Overhead", "Variable IC Payouts", "Variable Transaction Fees"] * 3,
        "Value ($)": [
            y1_data['Total_Fixed']/factor, y1_data['Cost_Payouts']/factor, y1_data['Cost_Merchant']/factor,
            y2_data['Total_Fixed']/factor, y2_data['Cost_Payouts']/factor, y2_data['Cost_Merchant']/factor,
            y3_data['Total_Fixed']/factor, y3_data['Cost_Payouts']/factor, y3_data['Cost_Merchant']/factor
        ]
    })
    st.bar_chart(data=comparison_costs_df, x="Segment", y="Value ($)", color="Cost Tier", use_container_width=True)

# Granular multi-year ledger
st.write("---")
st.subheader("📋 Granular Multi-Year Financial Ledger")

ledger_data = {
    "Financial Category / Line Item": [
        "1. REVENUE STREAMS",
        "   ├── Coach Training Revenue",
        "   ├── Patient Package Revenue",
        "   └── SaaS Platform & Tech Licensing",
        "TOTAL GROSS REVENUE",
        "2. VARIABLE EXPENSES (COGS)",
        "   ├── IC Coach Revenue Share Compensation",
        "   └── Merchant / Gateway CC Fees",
        "TOTAL VARIABLE EXPENSES",
        "3. FIXED OVERHEAD BURDEN",
        "TOTAL SYSTEM OUTFLOW (Fixed + Variable)",
        "NET RUNNING PROFIT PERFORMANCE"
    ],
    "Year 1": [
        "",
        format_val(y1_data['Rev_Training']),
        format_val(y1_data['Rev_Patients']),
        format_val(y1_data['Rev_SaaS']),
        format_val(y1_data['Gross_Revenue']),
        "",
        format_val(y1_data['Cost_Payouts']),
        format_val(y1_data['Cost_Merchant']),
        format_val(y1_data['Total_Variable']),
        format_val(y1_data['Total_Fixed']),
        format_val(y1_data['Total_Expenses']),
        format_val(y1_data['Net_Profit'])
    ],
    "Year 2": [
        "",
        format_val(y2_data['Rev_Training']),
        format_val(y2_data['Rev_Patients']),
        format_val(y2_data['Rev_SaaS']),
        format_val(y2_data['Gross_Revenue']),
        "",
        format_val(y2_data['Cost_Payouts']),
        format_val(y2_data['Cost_Merchant']),
        format_val(y2_data['Total_Variable']),
        format_val(y2_data['Total_Fixed']),
        format_val(y2_data['Total_Expenses']),
        format_val(y2_data['Net_Profit'])
    ],
    "Year 3": [
        "",
        format_val(y3_data['Rev_Training']),
        format_val(y3_data['Rev_Patients']),
        format_val(y3_data['Rev_SaaS']),
        format_val(y3_data['Gross_Revenue']),
        "",
        format_val(y3_data['Cost_Payouts']),
        format_val(y3_data['Cost_Merchant']),
        format_val(y3_data['Total_Variable']),
        format_val(y3_data['Total_Fixed']),
        format_val(y3_data['Total_Expenses']),
        format_val(y3_data['Net_Profit'])
    ]
}

st.table(pd.DataFrame(ledger_data))