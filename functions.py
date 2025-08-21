import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from io import BytesIO, StringIO
import pdfplumber

def analyze_data(df: pd.DataFrame) -> dict:
    """Enhanced data analysis summary"""
    buffer = StringIO()
    df.info(buf=buffer)
    info_str = buffer.getvalue()

    summary = {
        "rows": df.shape[0],
        "columns": df.shape[1],
        "missing_values": int(df.isnull().sum().sum()),
        "column_names": list(df.columns),
        "data_types": {col: str(df[col].dtype) for col in df.columns},
        "descriptive_stats": df.describe().to_dict(),
        "info": info_str
    }
    return summary

def create_chart(df: pd.DataFrame, chart_type: str, x_col: str, y_col: str = None, color_col: str = None):
    """Create a chart based on user selections"""
    plt.style.use('seaborn-v0_8-darkgrid')
    fig, ax = plt.subplots(figsize=(10, 6))

    if chart_type == "Pie Chart":
        if df[x_col].nunique() > 10:
            top_10 = df[x_col].value_counts().nlargest(10)
            ax.pie(top_10, labels=top_10.index, autopct='%1.1f%%', startangle=90)
            ax.set_title(f'Top 10 {x_col} Distribution')
        else:
            df[x_col].value_counts().plot.pie(autopct='%1.1f%%', ax=ax)
        ax.set_ylabel('')

    elif chart_type == "Bar Chart":
        sns.barplot(x=x_col, y=y_col, data=df, ax=ax, hue=color_col)
        ax.set_title(f'{y_col} by {x_col}')
        plt.xticks(rotation=45)

    elif chart_type == "Histogram":
        sns.histplot(data=df, x=x_col, kde=True, ax=ax, hue=color_col)
        ax.set_title(f'Distribution of {x_col}')

    elif chart_type == "Line Chart":
        sns.lineplot(data=df, x=x_col, y=y_col, ax=ax, hue=color_col)
        ax.set_title(f'{y_col} over {x_col}')
        plt.xticks(rotation=45)

    elif chart_type == "Scatter Plot":
        sns.scatterplot(data=df, x=x_col, y=y_col, hue=color_col, ax=ax)
        ax.set_title(f'Scatter plot of {y_col} vs {x_col}')

    elif chart_type == "Correlation Heatmap":
        numeric_df = df.select_dtypes(include=['number'])
        if not numeric_df.empty:
            corr = numeric_df.corr()
            sns.heatmap(corr, annot=True, cmap='coolwarm', ax=ax)
            ax.set_title('Correlation Heatmap')
        else:
            ax.text(0.5, 0.5, "No numeric data to create a heatmap.", ha='center', va='center')

    plt.tight_layout()
    return fig

def download_csv(df: pd.DataFrame) -> str:
    """Converts a dataframe to a CSV string for download"""
    return df.to_csv(index=False).encode('utf-8')

def download_plot(fig) -> bytes:
    """Saves a matplotlib plot to a bytes buffer for download"""
    buf = BytesIO()
    fig.savefig(buf, format="png", dpi=300)
    buf.seek(0)
    return buf.getvalue()

def read_pdf(file) -> pd.DataFrame:
    """Extracts tables from a PDF and returns a concatenated DataFrame"""
    with pdfplumber.open(file) as pdf:
        tables = []
        for page in pdf.pages:
            tables.extend(page.extract_tables())

    if not tables:
        return pd.DataFrame()

    dfs = []
    for table in tables:
        if table:
            # Convert list of lists to DataFrame
            df = pd.DataFrame(table[1:], columns=table[0])
            dfs.append(df)

    if not dfs:
        return pd.DataFrame()

    return pd.concat(dfs, ignore_index=True)
