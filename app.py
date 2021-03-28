import dash
from dash.dependencies import Input, Output, State
import dash_html_components as html
import dash_core_components as dcc
import dash_table as dt

import pandas as pd

app = dash.Dash(__name__, title="White Wine Quality Dash")

markdown_text = '''
This data set assesses the quality of 4898 white wine variants from the Portuguese Vinho Verde region based on 11 physicochemical features. The region
is in the northwest of Portugal as shown in the adjacent map to the left. The data was originally used in the paper [Modeling wine preferences by data mining from physicochemical properties](https://www.sciencedirect.com/science/article/abs/pii/S0167923609001377?via%3Dihub)
by Cortez et al. (2009). The data set is posted on the [UCI Machine Learning Repository](https://archive.ics.uci.edu/ml/datasets/wine+quality), but was sourced in this project from [data.world.](https://data.world/food/wine-quality)  

The physicochemical properties of the white wine variants that act as the input variables:
- Fixed acidity
- Volatile acidity
- Citric acid
- Residual sugar
- etc...
'''
df_url = 'https://query.data.world/s/tmlt63lm3n3uzb2ujhlmkarlzoeo73'
df = pd.read_csv(df_url)


df_quality = df['quality'].dropna().sort_values().unique().astype(str)
opt_quality = [{'label': x + ' quality', 'value': x} for x in df_quality]

colors = {
     'background': '#7FDBFF',
     'text': '#745D34',
     'special': 'purple'
 }


app.layout = html.Div([
    html.H1(app.title),
    dcc.Markdown(markdown_text),
    html.Label(["Select types quality of white wine:", 
        dcc.Dropdown('my-dropdown', 
            options= opt_quality, 
            value= opt_quality[0]['value'],
            multi=True
        )
    ]),
    dt.DataTable(
        id='my-table',
        columns=[{"name": i, "id": i} for i in df.columns],
        data= df.to_dict("records")
    )
],
style={"backgroundColor": colors['background'], 'color': colors['text']})


@app.callback(
     Output('my-table', 'data'),
     Input('my-dropdown', 'value'))
def update_data(values):
    filter = df['quality'].isin(values)
    return df[filter].to_dict("records")



if __name__ == '__main__':
    app.server.run(debug=True)
    