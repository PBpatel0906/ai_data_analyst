import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import io

def analyze_data(df: pd.DataFrame) -> dict:
    """Basic data analysis summary"""
    summary = {
        "rows": df.shape[0],
        "columns": df.shape[1],
        "missing_values": int(df.isnull().sum().sum()),
        "column_names": list(df.columns)
    }
    return summary


def create_chart(df: pd.DataFrame, chart_type: str, x_col: str, y_col: str = None):
    """
    Generate chart (pie, bar, line, etc.) based on user selection.
    Returns the matplotlib figure object.
    """
    fig, ax = plt.subplots(figsize=(6, 4))

    if chart_type == "Pie Chart":
        df[x_col].value_counts().plot.pie(autopct="%1.1f%%", ax=ax)
        ax.set_ylabel("")  # remove default ylabel

    elif chart_type == "Bar Chart":
        sns.countplot(x=x_col, data=df, ax=ax)

    elif chart_type == "Histogram":
        df[x_col].plot.hist(ax=ax, bins=20)

    elif chart_type == "Line Chart" and y_col is not None:
        sns.lineplot(x=df[x_col], y=df[y_col], ax=ax)

    else:
        ax.text(0.5, 0.5, "Unsupported Chart Type or Missing Column",
                ha="center", va="center")

    plt.tight_layout()
    return fig


def download_csv(df: pd.DataFrame) -> bytes:
    """Convert DataFrame to CSV for download"""
    return df.to_csv(index=False).encode("utf-8")


def download_plot(fig) -> bytes:
    """Convert Matplotlib figure to PNG for download"""
    buf = io.BytesIO()
    fig.savefig(buf, format="png")
    buf.seek(0)
    return buf.getvalue()
