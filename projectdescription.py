import dash
import dash_html_components as html
import dash_core_components as dcc

markdown_text = '''

The dash app can be seen in the "app.py" on my [Github](https://github.com/xavier414/Python_Dash_Project).

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

app = dash.Dash(__name__, title="Description - White Wine Quality Dash")

app.layout = html.Div([
    html.H1(app.title),
    dcc.Markdown(markdown_text)
])

if __name__ == '__main__':
    app.server.run(debug=True)