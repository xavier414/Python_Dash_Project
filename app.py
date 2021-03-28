import dash
from dash.dependencies import Input, Output, State
import plotly.express as px
import dash_html_components as html
import dash_core_components as dcc
import dash_table as dt

import pandas as pd

import json

app = dash.Dash(
    __name__, title="White Wine Quality Dash")

markdown_text = '''
This data set assesses the quality of 4898 white wine variants from the Portuguese Vinho Verde region based on 11 physicochemical features. The data was originally used in the paper [Modeling wine preferences by data mining from physicochemical properties](https://www.sciencedirect.com/science/article/abs/pii/S0167923609001377?via%3Dihub)
by Cortez et al. (2009). The data set was posted originally on the [UCI Machine Learning Repository](https://archive.ics.uci.edu/ml/datasets/wine+quality), but was sourced in this project from [data.world.](https://data.world/food/wine-quality)

The physicochemical properties of the white wine variants that act as the input variables:
- Fixed acidity
- Volatile acidity
- Citric acid
- Residual sugar
- Chlorides
- Free sulfur dioxide
- Total sulfur dioxide
- Density
- pH
- Alcohol

The output variable is *quality* on a scale of 1 to 10, however values 0,1,2 and 10 do not - indicating there is no wine that is of perfect or no quality.

In this analysis, there is a table which can be filtered by mulitple qualities of wine. There is also range slider to adjust the range reviewed for the fixed acidity varaible.
An interactive scatterplot is also provided in another tab where you can see the fixed acidity plotted against the volatile acidity of wine varieties. The data is coloured 
by quality. The range slider can also be used in the graph as well and the qualities can be selected too. In addition, the lasso feature can be used on the scatter plot to
select data points and all the physicochemical properties can be seen for those data points selected below the plot.\

'''

df_url = 'https://query.data.world/s/tmlt63lm3n3uzb2ujhlmkarlzoeo73'
df = pd.read_csv(df_url)


df_quality = df['quality'].dropna().sort_values().unique().astype(str)
opt_quality = [{'label': x + ' quality', 'value': x} for x in df_quality]

min_fixed_acidity = min(df['fixed acidity'].dropna())
max_fixed_acidity = max(df['fixed acidity'].dropna())
step_fixed_acidity = (max_fixed_acidity - min_fixed_acidity)/10

df_cols = [{"name": i, "id": i} for i in df.columns]


table_tab = dt.DataTable(
    id='my-table',
    columns=[{"name": i, "id": i} for i in df.columns],
    data=df.to_dict("records")
)

graph_tab = html.Div([
    dcc.Graph(id="my_graph",
              figure=px.scatter(
                  df, x="fixed acidity", y="volatile acidity", color="quality")
              ),
    dt.DataTable(id="selected_data",
                 columns=df_cols

                 )
])

app.layout = html.Div([
    html.Div([
        html.H1(app.title,  className="app-header--title")
    ],  className="app-header"),
    html.Div([dcc.Markdown(markdown_text),
              html.Label(["Select types quality of white wine:",
                          dcc.Dropdown('my-dropdown',
                                       options=opt_quality,
                                       value=opt_quality[0]['value'],
                                       multi=True
                                       )
                          ]),
              html.Div(id="data", style={'display': 'none'}),
              dcc.RangeSlider(id="range",
                              min=min_fixed_acidity,
                              max=max_fixed_acidity,
                              step=step_fixed_acidity,
                              marks={min_fixed_acidity + i * step_fixed_acidity: '{}'.format(
                                  round(min_fixed_acidity + i * step_fixed_acidity, 2)) for i in range(10)},
                              value=[min_fixed_acidity, max_fixed_acidity]
                              ),
              dcc.Tabs(id="tabs", value='tab-t', children=[
                  dcc.Tab(label='Table', value='tab-t'),
                  dcc.Tab(label='Graph', value='tab-g'),
              ]),

              html.Div(id="tabs-content")

              ], className="app-body")  # end of html div for dropdown and table
])


@app.callback(
    Output('my-table', 'data'),
    Input('data', 'children'),
    State('tabs', 'value'))
def update_table(data, tab):
    if tab != 'tab-t':
        return None
    dff = pd.read_json(data)
    return dff.to_dict("records")


@app.callback(
    Output('my_graph', 'figure'),
    Input('data', 'children'),
    State('tabs', 'value'))
def update_figure(data, tab):
    if tab != 'tab-g':
        return None
    dff = pd.read_json(data)
    return px.scatter(dff, x="fixed acidity", y="volatile acidity", custom_data=["quality"], color="quality")


@app.callback(
    Output('selected_data', 'data'),
    Input('my_graph', 'selectedData'))
def display_selected_data(selectedData):
    if selectedData is None:
        return None
    names = [o["customdata"][0] for o in selectedData["points"]]
    filter = df['quality'].isin(names)
    return df[filter].to_dict("records")


@app.callback(
    Output('data', 'children'),
    Input('range', 'value'),
    Input('my-dropdown', 'value'))
def update_data(range, values):
    filter = df['quality'].isin(
        list(values)) & df['fixed acidity'].between(range[0], range[1])
    return df[filter].to_json()


@ app.callback(Output('tabs-content', 'children'),
               Input('tabs', 'value'))
def update_tabs(v):
    if v == 'tab-g':
        return graph_tab
    return table_tab


if __name__ == '__main__':
    app.server.run(debug=True)
