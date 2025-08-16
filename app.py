import streamlit as st
import pandas as pd

from functions import analyze_data   # we'll write this in functions.py

st.set_page_config(page_title="AI Data Analyst Platform", layout="wide")
st.title("📊 AI Data Analyst Platform")

# File uploader
uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"])

if uploaded_file is not None:
    # Read CSV
    df = pd.read_csv(uploaded_file)

    st.success("✅ File uploaded successfully!")

    # Show preview
    st.subheader("🔎 Preview of Data")
    st.dataframe(df.head())

    # Run analysis
    st.subheader("📈 Data Summary")
    analysis = analyze_data(df)
    st.json(analysis)

    # Show stats
    st.subheader("📊 Statistical Overview")
    st.write(df.describe())