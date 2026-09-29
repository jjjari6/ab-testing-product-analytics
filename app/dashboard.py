import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="A/B Testing Product Analytics",
    page_icon="🧪",
    layout="wide"
)

# Load data
df = pd.read_csv("data/ab_test_data.csv")

# Calculate experiment metrics
summary = (
    df.groupby("group")
    .agg(
        users=("user_id", "count"),
        conversions=("converted", "sum"),
        conversion_rate=("converted", "mean")
    )
)

control_rate = summary.loc["control", "conversion_rate"]
treatment_rate = summary.loc["treatment", "conversion_rate"]

absolute_lift = treatment_rate - control_rate
relative_lift = absolute_lift / control_rate

# Dashboard title
st.title("🧪 A/B Testing & Product Analytics")

st.write(
    "Interactive analysis of a product experiment comparing "
    "control and treatment conversion performance."
)

st.divider()

# KPI cards
col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Total Users",
    f"{len(df):,}"
)

col2.metric(
    "Control Conversion",
    f"{control_rate:.2%}"
)

col3.metric(
    "Treatment Conversion",
    f"{treatment_rate:.2%}"
)

col4.metric(
    "Relative Lift",
    f"{relative_lift:.2%}"
)

st.divider()

st.subheader("Overall Conversion Performance")

chart_data = pd.DataFrame({
    "Group": ["Control", "Treatment"],
    "Conversion Rate (%)": [
        control_rate * 100,
        treatment_rate * 100
    ]
})

st.bar_chart(
    chart_data,
    x="Group",
    y="Conversion Rate (%)"
)

st.divider()

st.subheader("Device Segment Analysis")

selected_device = st.selectbox(
    "Select Device",
    ["All"] + sorted(df["device"].unique().tolist())
)

if selected_device == "All":
    device_df = df
else:
    device_df = df[df["device"] == selected_device]

device_summary = (
    device_df.groupby("group")["converted"]
    .mean()
    .reset_index()
)

device_summary["conversion_rate_pct"] = (
    device_summary["converted"] * 100
)

st.bar_chart(
    device_summary,
    x="group",
    y="conversion_rate_pct"
)

st.divider()

st.subheader("Traffic Source Analysis")

selected_source = st.selectbox(
    "Select Traffic Source",
    ["All"] + sorted(df["traffic_source"].unique().tolist())
)

if selected_source == "All":
    source_df = df
else:
    source_df = df[df["traffic_source"] == selected_source]

source_summary = (
    source_df.groupby("group")["converted"]
    .mean()
    .reset_index()
)

source_summary["conversion_rate_pct"] = (
    source_summary["converted"] * 100
)

st.bar_chart(
    source_summary,
    x="group",
    y="conversion_rate_pct"
)

import math

st.divider()

st.subheader("Experiment Significance")

control_users = summary.loc["control", "users"]
treatment_users = summary.loc["treatment", "users"]

control_conversions = summary.loc["control", "conversions"]
treatment_conversions = summary.loc["treatment", "conversions"]

pooled_rate = (
    control_conversions + treatment_conversions
) / (
    control_users + treatment_users
)

standard_error = math.sqrt(
    pooled_rate * (1 - pooled_rate) *
    ((1 / control_users) + (1 / treatment_users))
)

z_stat = (control_rate - treatment_rate) / standard_error

p_value = 0.5 * (
    1 + math.erf(z_stat / math.sqrt(2))
)

col1, col2 = st.columns(2)

col1.metric(
    "P-value",
    f"{p_value:.4f}"
)

col2.metric(
    "Significance Level",
    "0.05"
)

if p_value < 0.05:
    st.success(
        "The treatment improvement is statistically significant at the 5% level."
    )
else:
    st.warning(
        "The treatment improvement is not statistically significant at the 5% level."
    )

difference = treatment_rate - control_rate

se_difference = math.sqrt(
    (control_rate * (1 - control_rate) / control_users) +
    (treatment_rate * (1 - treatment_rate) / treatment_users)
)

margin_of_error = 1.96 * se_difference

ci_lower = difference - margin_of_error
ci_upper = difference + margin_of_error

st.write(
    f"**Observed Lift:** {difference * 100:.2f} percentage points"
)

st.write(
    f"**95% Confidence Interval:** "
    f"{ci_lower * 100:.2f} to {ci_upper * 100:.2f} percentage points"
)

st.divider()

st.subheader("Business Recommendation")

if p_value < 0.05 and treatment_rate > control_rate:
    st.success(
        "The treatment increased overall conversion and the result is "
        "statistically significant. Consider rolling out the treatment "
        "while continuing to monitor conversion performance and key "
        "customer segments."
    )
elif treatment_rate > control_rate:
    st.warning(
        "The treatment produced a higher conversion rate, but the result "
        "is not statistically significant. Consider extending the experiment "
        "before making a full rollout decision."
    )
else:
    st.error(
        "The treatment did not improve overall conversion. A full rollout "
        "is not supported by the current experiment results."
    )