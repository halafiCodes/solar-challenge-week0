import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from utils import load_data, filter_countries, create_boxplot, top_regions_table


st.set_page_config(page_title="Solar Data Dashboard", layout="wide")
st.title("☀️ Solar Data Interactive Dashboard")


st.sidebar.header("Filter Options")

selected_countries = st.sidebar.multiselect(
    "Select countries",
    options=["Benin", "Sierra Leone", "Togo"],  
    default=["Benin"]
)


regions = ["Region 1", "Region 2", "Region 3"]
selected_regions = st.sidebar.multiselect("Select regions (optional)", options=regions)


data_path = "data/all_countries_clean.csv"



df = pd.DataFrame({
    "Country": np.random.choice(["Benin", "Sierra Leone", "Togo"], 100),
    "Region": np.random.choice(["Region 1", "Region 2", "Region 3"], 100),
    "Year": np.random.choice(range(2010, 2024), 100),
    "GHI": np.random.rand(100) * 100,
    "Undernourishment": np.random.rand(100) * 50
})


df_filtered = filter_countries(df, selected_countries)
if selected_regions:
    df_filtered = df_filtered[df_filtered["Region"].isin(selected_regions)]


st.markdown("### Key Metrics")
if not df_filtered.empty:
    col1, col2, col3 = st.columns(3)
    col1.metric("Average GHI", f"{df_filtered['GHI'].mean():.2f}")
    col2.metric("Min GHI", f"{df_filtered['GHI'].min():.2f}")
    col3.metric("Max GHI", f"{df_filtered['GHI'].max():.2f}")
else:
    st.warning("No data available for selected filters.")


st.subheader("GHI Distribution by Country")
st.plotly_chart(create_boxplot(df_filtered, "GHI"), use_container_width=True)


st.subheader("GHI Trend Over Time")
if "Year" in df_filtered.columns:
    ghi_trend = df_filtered.groupby(["Year", "Country"])["GHI"].mean().reset_index()
    fig_line = px.line(ghi_trend, x="Year", y="GHI", color="Country", markers=True,
                       title="Average GHI Over Time")
    st.plotly_chart(fig_line, use_container_width=True)


st.subheader("Correlation Between Numeric Variables")
numeric_cols = df_filtered.select_dtypes(include="number")
if not numeric_cols.empty:
    corr = numeric_cols.corr()
    fig_corr = px.imshow(corr, text_auto=True, color_continuous_scale="Blues",
                         title="Correlation Heatmap")
    st.plotly_chart(fig_corr, use_container_width=True)
else:
    st.info("No numeric columns available for correlation heatmap.")


st.subheader("Top Regions by GHI")
st.dataframe(top_regions_table(df_filtered))


st.download_button(
    label="Download Filtered Data as CSV",
    data=df_filtered.to_csv(index=False).encode("utf-8"),
    file_name="filtered_solar_data.csv",
    mime="text/csv"
)


st.markdown("---")
st.caption("Developed by Weldesilassie • Dashboard enhanced with advanced analytics features ⚡")
