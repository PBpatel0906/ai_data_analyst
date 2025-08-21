import streamlit as st
import pandas as pd
from functions import (analyze_data, create_chart, download_csv,
                      download_plot, read_pdf)

st.set_page_config(page_title="AI Data Analyst Platform", layout="wide")

# --- Sidebar Setup ---
st.sidebar.title("📊 AI Data Analyst Platform")
st.sidebar.markdown("Upload your data file and see the magic happen!")

file_type = st.sidebar.radio("Choose file type", ('CSV', 'PDF'))

if file_type == 'CSV':
    uploaded_file = st.sidebar.file_uploader("Upload a CSV file", type=["csv"])
else:
    uploaded_file = st.sidebar.file_uploader("Upload a PDF file", type=["pdf"])


if uploaded_file is not None:
    st.sidebar.success("✅ File uploaded successfully!")
    try:
        if file_type == 'CSV':
            df = pd.read_csv(uploaded_file)
        else:
            df = read_pdf(uploaded_file)

        if df.empty:
            st.error("The uploaded file is empty or no tables could be extracted.")
        else:
            st.title("Data Analysis Report")

            # --- Main Page Tabs ---
            tab1, tab2, tab3 = st.tabs(["🔎 Data Preview", "📈 Data Summary", "📊 Visualization"])

            with tab1:
                st.header("Data Preview")
                st.dataframe(df)

            with tab2:
                st.header("Data Summary")
                analysis = analyze_data(df)
                st.json(analysis)
                st.subheader("Descriptive Statistics")
                st.dataframe(pd.DataFrame(analysis['descriptive_stats']))
                st.subheader("Data Info")
                st.text(analysis['info'])

            with tab3:
                st.header("Create a Chart")

                numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
                all_cols = df.columns.tolist()

                chart_type = st.selectbox("Choose chart type",
                                         ["Bar Chart", "Line Chart", "Scatter Plot",
                                          "Histogram", "Pie Chart", "Correlation Heatmap"])

                if chart_type not in ["Pie Chart", "Histogram", "Correlation Heatmap"]:
                    x_col = st.selectbox("Select X-axis column", all_cols)
                    y_col = st.selectbox("Select Y-axis column", numeric_cols)
                elif chart_type == "Correlation Heatmap":
                    x_col, y_col = None, None # Not needed
                else:
                    x_col = st.selectbox("Select column for chart", all_cols)
                    y_col = None

                color_col = st.selectbox("Select color dimension (optional)", [None] + all_cols)

                if st.button("Generate Chart"):
                    with st.spinner('Generating chart...'):
                        fig = create_chart(df, chart_type, x_col, y_col, color_col)
                        st.pyplot(fig)

                        st.download_button(
                            label="📥 Download Chart as PNG",
                            data=download_plot(fig),
                            file_name=f"{chart_type.lower().replace(' ', '_')}.png",
                            mime="image/png"
                        )

            # --- Download Options in Sidebar ---
            st.sidebar.subheader("⬇ Download Options")
            st.sidebar.download_button(
                label="📥 Download Processed Data (CSV)",
                data=download_csv(df),
                file_name="processed_data.csv",
                mime="text/csv"
            )

    except Exception as e:
        st.error(f"An error occurred: {e}")

else:
    st.info("Awaiting for file to be uploaded.")
    
