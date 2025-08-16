import streamlit as st
import pandas as pd
from functions import analyze_data, create_chart, download_csv, download_plot

st.set_page_config(page_title="AI Data Analyst Platform", layout="wide")
st.title("📊 AI Data Analyst Platform")

uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    st.success("✅ File uploaded successfully!")

    st.subheader("🔎 Preview of Data")
    st.dataframe(df.head())

    # Analysis
    st.subheader("📈 Data Summary")
    analysis = analyze_data(df)
    st.json(analysis)

    # Visualization
    st.subheader("📊 Create a Chart")
    chart_type = st.selectbox("Choose chart type", ["Pie Chart", "Bar Chart", "Histogram", "Line Chart"])
    x_col = st.selectbox("Select X column", df.columns)
    y_col = None
    if chart_type == "Line Chart":
        y_col = st.selectbox("Select Y column", df.columns)

    if st.button("Generate Chart"):
        fig = create_chart(df, chart_type, x_col, y_col)
        st.pyplot(fig)

        # Download chart
        st.download_button(
            label="📥 Download Chart as PNG",
            data=download_plot(fig),
            file_name="chart.png",
            mime="image/png"
        )

    # Download dataset
    st.subheader("⬇ Download Options")
    st.download_button(
        label="📥 Download Processed Data (CSV)",
        data=download_csv(df),
        file_name="processed_data.csv",
        mime="text/csv"
    )



