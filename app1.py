import streamlit as st
import pandas as pd
import plotly.express as px

#--------------------------------------------------------
# PAGE CONFIG
#--------------------------------------------------------
st.set_page_config(
    page_title="Inequality Dashboard",
    layout="wide"
)

#--------------------------------------------------------
# LOAD + CLEAN DATA (CACHED)
#--------------------------------------------------------
@st.cache_data
def load_data():
    df = pd.read_excel("WIID_Cleaned_Imputed_Renamed.xlsx")

    df = df.rename(columns={
        "country_name": "Country",
        "gini_index": "Gini Index",
        "palma_ratio": "Palma Ratio",
        "gdp_per_capita": "gdp_per_capita",
        "income_group": "income_group",
        "region_united_nations": "Region",
        "year": "year",
        "iso3": "iso3"
    })

    # optimise types
    df["Region"] = df["Region"].astype("category")
    df["income_group"] = df["income_group"].astype("category")
    df["Country"] = df["Country"].astype("category")

    return df

df = load_data()

#--------------------------------------------------------
# CUSTOM CSS FOR KPI CARDS
#--------------------------------------------------------
card_style = """
<style>
div[data-testid="metric-container"] {
    background-color: #B57EDC;
    border-radius: 12px;
    padding: 20px;
    text-align: center;
    color: white;
}
div[data-testid="metric-container"] > div {
    color: white;
}
</style>
"""
st.markdown(card_style, unsafe_allow_html=True)

#--------------------------------------------------------
# TITLE
#--------------------------------------------------------
st.markdown("<h1 style='text-align:center;'>Global Inequality Dashboard</h1>", unsafe_allow_html=True)
st.write("")

#--------------------------------------------------------
# KPI CARDS
#--------------------------------------------------------
k1, k2, k3, k4 = st.columns(4)

with k1:
    st.metric("Total Countries Analyzed", df["Country"].nunique())

with k2:
    st.metric("Global Average Gini Index", round(df["Gini Index"].mean(), 2))

with k3:
    st.metric("Average GDP Per Capita (USD)", f"{df['gdp_per_capita'].mean():,.2f}")

with k4:
    st.metric("Average Palma Ratio", round(df["Palma Ratio"].mean(), 2))

#--------------------------------------------------------
# FILTERS (SIDEBAR)
#--------------------------------------------------------
st.sidebar.header("Filters")

year = st.sidebar.multiselect("Select Year", sorted(df["year"].unique()))
region = st.sidebar.multiselect("Select Region", sorted(df["Region"].unique()))
income = st.sidebar.multiselect("Income Group", sorted(df["income_group"].unique()))

filtered = df.copy()

if year:
    filtered = filtered[filtered["year"].isin(year)]

if region:
    filtered = filtered[filtered["Region"].isin(region)]

if income:
    filtered = filtered[filtered["income_group"].isin(income)]

# small subset for plots
filtered_small = filtered[
    [
        "Country",
        "Gini Index",
        "Region",
        "year",
        "income_group",
        "iso3",
        "gdp_per_capita",
        "population_total",
        "decile_1_share",
        "decile_2_share",
        "decile_3_share",
        "decile_4_share",
        "decile_5_share",
        "decile_6_share",
        "decile_7_share",
        "decile_8_share",
        "decile_9_share",
        "decile_10_share",
    ]
]

#--------------------------------------------------------
# ROW 1 : MAP + PIE
#--------------------------------------------------------
r1c1, r1c2 = st.columns([2, 1])

# 🌍 Choropleth World Map
with r1c1:
    st.subheader("World Map: Gini Index by Country")

    show_map = st.checkbox("Show World Map", value=True)

    if show_map:
        if "iso3" in filtered_small.columns:
            fig_map = px.choropleth(
                filtered_small,
                locations="iso3",
                color="Gini Index",
                hover_name="Country",
                color_continuous_scale="Viridis"
            )
            st.plotly_chart(fig_map, use_container_width=True)
        else:
            st.error("ISO3 column not found in data.")

# 🥧 Pie: Income Classification
with r1c2:
    st.subheader("Countries by Income Classification")
    fig_pie = px.pie(
        filtered_small,
        names="income_group",
        title="Income Group Distribution"
    )
    st.plotly_chart(fig_pie, use_container_width=True)

#--------------------------------------------------------
# ROW 2 : BAR (Top inequality) + SCATTER (GDP vs Gini)
#--------------------------------------------------------
r2c1, r2c2 = st.columns(2)

# 📊 Bar: Top inequality countries
with r2c1:
    st.subheader("Countries with Highest Inequality (Top 10)")

    top_10 = (
        filtered_small.groupby("Country")["Gini Index"]
        .mean()
        .nlargest(10)
        .reset_index()
    )

    fig_bar = px.bar(
        top_10,
        x="Gini Index",
        y="Country",
        orientation="h",
        title="Top 10 Most Unequal Countries"
    )
    st.plotly_chart(fig_bar, use_container_width=True)

# 🔵 Scatter: GDP vs Gini
with r2c2:
    st.subheader("Relationship Between GDP and Income Inequality")

    scatter_df = filtered_small.dropna(subset=["gdp_per_capita", "Gini Index"])

    fig_scatter = px.scatter(
        scatter_df,
        x="gdp_per_capita",
        y="Gini Index",
        color="income_group",
        size="population_total",
        hover_name="Country",
        title="GDP per Capita vs Gini Index",
        labels={"gdp_per_capita": "GDP per Capita (USD)"}
    )
    st.plotly_chart(fig_scatter, use_container_width=True)

#--------------------------------------------------------
# ROW 3 : STACKED BAR (Income distribution) + REGION TREND
#--------------------------------------------------------
r3c1, r3c2 = st.columns(2)

# 🧱 Stacked bar: Income distribution (deciles)
with r3c1:
    st.subheader("How Income Is Distributed: Richest to Poorest (Deciles)")

    decile_cols = [
        "decile_1_share",
        "decile_2_share",
        "decile_3_share",
        "decile_4_share",
        "decile_5_share",
        "decile_6_share",
        "decile_7_share",
        "decile_8_share",
        "decile_9_share",
        "decile_10_share",
    ]

    # Take average distribution across countries in filtered data
    decile_avg = (
        filtered_small[decile_cols]
        .mean()
        .reset_index()
        .rename(columns={"index": "Decile", 0: "Share"})
    )
    decile_avg["Decile"] = decile_avg["Decile"].str.replace("_share", "").str.replace("decile_", "Decile ")

    fig_stack = px.bar(
        decile_avg,
        x="Decile",
        y="Share",
        title="Average Income Share by Decile",
    )
    st.plotly_chart(fig_stack, use_container_width=True)

# 📈 Region trend: Gini over time
with r3c2:
    st.subheader("How Inequality Changed by Region (2010–2023)")

    trend_df = filtered_small.dropna(subset=["year", "Gini Index"]).copy()
    # keep reasonable year range if needed
    # trend_df = trend_df[(trend_df["year"] >= 2010) & (trend_df["year"] <= 2023)]

    fig_trend = px.line(
        trend_df,
        x="year",
        y="Gini Index",
        color="Region",
        title="Gini Index Trend by Region"
    )
    st.plotly_chart(fig_trend, use_container_width=True)
