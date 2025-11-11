import pandas as pd
import plotly.express as px

def load_data(file_path: str) -> pd.DataFrame:
    """Load CSV data from the given path."""
    try:
        return pd.read_csv(file_path)
    except FileNotFoundError:
        raise FileNotFoundError(f" File not found: {file_path}")

def filter_countries(df: pd.DataFrame, countries: list) -> pd.DataFrame:
    """Filter DataFrame for selected countries."""
    if not countries:
        return df
    return df[df['Country'].isin(countries)]

def create_boxplot(df: pd.DataFrame, column: str):
    """Generate a boxplot using Plotly."""
    fig = px.box(
        df,
        x='Country',
        y=column,
        points="all",
        color="Country",
        title=f'{column} Distribution by Country'
    )
    fig.update_layout(showlegend=False)
    return fig

def top_regions_table(df: pd.DataFrame, metric: str = 'GHI', top_n: int = 5) -> pd.DataFrame:
    """Return top n regions by a metric."""
    if 'Region' not in df.columns:
        return pd.DataFrame()
    return (
        df.groupby('Region')[metric]
        .mean()
        .sort_values(ascending=False)
        .head(top_n)
        .reset_index()
    )
