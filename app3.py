import dash
from dash.dependencies import Input, Output, State
import plotly.express as px
import dash_html_components as html
import dash_core_components as dcc
import dash_table as dt

import pandas as pd

app = dash.Dash(__name__, title="White Wine Quality Dash")

df_url = 'https://query.data.world/s/tmlt63lm3n3uzb2ujhlmkarlzoeo73'
df = pd.read_csv(df_url)


df_quality = df['quality'].dropna().sort_values().unique().astype(str)