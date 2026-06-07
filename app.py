import streamlit as st
import pandas as pd

# Set webpage browser configuration
st.set_page_config(page_title="Healing Circuits Budget Engine", layout="wide")

st.title("💡 Healing Circuits Financial Sensitivity Engine")
st.markdown("Toggle baseline presets or manually slide variables to see real-time runway, revenue shifts, and net margins.")

# ==========================================
# 1. SIDEBAR CONFIGURATION & ASSUMPTIONS
# ==========================================
st.sidebar.header("🕹️ Scenario & Driver Controls")

# Scenario Presets
scenario = st.sidebar.selectbox("Select Baseline Scenario Preset", ["Low", "Mid", "High", "Custom Custom"])

# Default driver mappings based on your sheets
preset_drivers = {
    "Low":  {"pts_per_month": 3,  "pkg_price": 2500, "active_coaches": 10},
    "Mid":  {"pts_per_month": 6,  "pkg_price": 3000, "active_coaches": 30},
    "High": {"pts_per_month": 12, "pkg_price": 3500, "active_coaches": 75}
}

# Apply presets or let user customize via sliders
if scenario != "Custom Custom":
    defaults = preset_drivers[scenario]
    pts = st.sidebar.slider("New Patients Per Month", 0, 30, defaults["pts_per_month"])
    price = st.sidebar.slider("Average Package Price ($)", 1000, 5000, defaults["pkg_price"], step=500)
    coaches = st.sidebar.slider("Active Certified Coaches (Yr 1-3)", 1, 100, defaults["active_coaches"])
else:
    pts = st.sidebar.slider("New Patients Per Month", 0, 30, 6)
    price = st.sidebar.slider("Average Package Price ($)", 1000, 5000, 3000, step=500)
    coaches = st.sidebar.slider("Active Certified Coaches (Yr 1-3)", 1, 100, 30)

# Cash Reserve input for Runway math
cash_on_hand = st.sidebar.number_input("Starting Cash on Hand ($)", value=250000, step=50000)

# ==========================================
# 2. CORE FINANCIAL LOGIC ENGINE
# ==========================================
def calculate_run_rate(pts_per_month, avg_price, active_coaches):
    # --- REVENUE ---
    # Core Patient Revenue Model 
    monthly_patient_revenue = pts_per_month * avg_price
    # Coach Tech/Platform fee ($200/mo licensing asset from your documentation)
    monthly_licensing_revenue = active_coaches * 200
    total_monthly_revenue = monthly_patient_revenue + monthly_licensing_revenue
    
    # --- FIXED EXPENSES (From Planned Spend Assets) ---
    fixed_personnel = 12500 + 2167  # Founder Salary ($12.5k) + Admin/Bookkeeping ($2.16k)
    fixed_marketing = 12500        # Baseline allocated marketing budget
    fixed_tech_saas = 500 + 500 + 1000 # CRM ($500) + Hosting ($500) + SupportedPatient ($1000)
    fixed_legal_finance = 1500 + 1200 + 1000 # Accounting ($1.5k) + Legal ($1.2k) + Insurance ($1k)
    
    total_monthly_fixed = fixed_personnel + fixed_marketing + fixed_tech_saas + fixed_legal_finance
    
    # --- VARIABLE EXPENSES (Based on Scaling Infrastructure) ---
    # Scaling out platform operational buffer per coach/client dynamic
    variable_infrastructure_cost = active_coaches * 50 
    # Processing or transactional merchant fees (approx 3% of incoming gross revenue)
    transaction_fees = total_monthly_revenue * 0.03
    
    total_monthly_variable = variable_infrastructure_cost + transaction_fees
    total_monthly_expenses = total_monthly_fixed + total_monthly_variable
    
    # --- NET PROFITS & MARGINS ---
    monthly_net_profit = total_monthly_revenue - total_monthly_expenses
    margin_pct = (monthly_net_profit / total_monthly_revenue) * 100 if total_monthly_revenue > 0 else 0.0
    
    return {
        "Revenue": total_monthly_revenue,
        "Fixed Expenses": total_monthly_fixed,
        "Variable Expenses": total_monthly_variable,
        "Total Expenses": total_monthly_expenses,
        "Net Profit": monthly_net_profit,
        "Margin %": margin_pct
    }

# Execute calculation based on interactive controls
metrics = calculate_run_rate(pts, price, coaches)

# ==========================================
# 3. INTERFACE VISUALS (THE DASHBOARD)
# ==========================================

# KPI Row
col1, col2, col3, col4 = st.columns(4)
col1.metric("Gross Monthly Revenue", f"${metrics['Revenue']:,.2f}")
col2.metric("Total Monthly Expenses", f"${metrics['Total Expenses']:,.2f}")

# Color-code Net Profit performance
if metrics['Net Profit'] >= 0:
    col3.metric("Net Monthly Runway Profit", f"${metrics['Net Profit']:,.2f}", delta=f"{metrics['Margin %']:.1f}% Margin")
else:
    col3.metric("Net Monthly Burn Rate", f"${metrics['Net Profit']:,.2f}", delta=f"{metrics['Margin %']:.1f}% Margin", delta_color="inverse")

# Runway Metric Calculation
if metrics['Net Profit'] < 0:
    burn_rate = abs(metrics['Net Profit'])
    runway_months = cash_on_hand / burn_rate
    col4.metric("Calculated Capital Runway", f"{runway_months:.1f} Months", f"Burn: ${burn_rate:,.0f}/mo", delta_color="inverse")
else:
    col4.metric("Calculated Capital Runway", "∞ (Profitable)", "No Capital Burn")

st.write("---")

# Visual Dynamic Charts
st.subheader("📊 Operational Financial Balance (Monthly)")
chart_data = pd.DataFrame({
    'Financial Metric': ['Gross Revenue', 'Fixed Burden', 'Variable Costs', 'Net Output'],
    'Value ($)': [metrics['Revenue'], metrics['Fixed Expenses'], metrics['Variable Expenses'], metrics['Net Profit']]
})
st.bar_chart(data=chart_data, x='Financial Metric', y='Value ($)', use_container_width=True)

# Breakdown Tables
st.subheader("📋 Underlying P&L Running Metrics Ledger")
breakdown_df = pd.DataFrame({
    "Financial Category": ["Total Modeled Income", "├── Core Fixed Overhead Expenses", "├── Scaling Variable Infrastructure Expenses", "└── Net Ordinary Profit Performance"],
    "Monthly Calculated Pro-Forma Value": [
        f"${metrics['Revenue']:,.2f}", 
        f"${metrics['Fixed Expenses']:,.2f}", 
        f"${metrics['Variable Expenses']:,.2f}", 
        f"${metrics['Net Profit']:,.2f}"
    ]
})
st.table(breakdown_df)