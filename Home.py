import streamlit as st
import requests
import pandas as pd

API_BASE = "http://localhost:8000"

st.set_page_config(page_title="AI Data Analyst", layout="wide")
st.title("AI Data Analyst (MVP)")

st.markdown("Upload a CSV/XLSX to get an instant preview and quick profile.")

uploaded = st.file_uploader("Choose a CSV or Excel file", type=["csv", "xlsx", "xls"])

if uploaded is not None:
    with st.spinner("Uploading and analyzing..."):
        files = {"file": (uploaded.name, uploaded.getvalue(), uploaded.type)}
        try:
            resp = requests.post(f"{API_BASE}/upload", files=files, timeout=120)
        except requests.exceptions.RequestException as e:
            st.error(f"API connection error: {e}")
            st.stop()

        if resp.status_code != 200:
            st.error(f"Upload failed: {resp.text}")
        else:
            data = resp.json()
            st.success("File processed successfully!")

            # Preview table
            st.subheader("Preview (first ~20 rows)")
            preview = data.get("preview", [])
            if preview:
                st.dataframe(pd.DataFrame(preview), use_container_width=True)
            else:
                st.info("No preview available.")

            # Quick profile
            st.subheader("Quick Profile")
            profile = data.get("profile", {})
            cols = st.columns(4)
            cols[0].metric("Rows", profile.get("n_rows", 0))
            cols[1].metric("Columns", profile.get("n_cols", 0))
            cols[2].metric("Numeric cols", len(profile.get("numeric_summary", {})))
            cols[3].metric("Missing values (total)", sum(profile.get("missing", {}).values()))

            with st.expander("Column dtypes"):
                st.json(profile.get("dtypes", {}))

            with st.expander("Missing by column"):
                st.json(profile.get("missing", {}))

            with st.expander("Numeric summary (describe)"):
                st.json(profile.get("numeric_summary", {}))