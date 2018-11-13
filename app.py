import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from get_histogram import *
import plotly.plotly as py
import plotly.graph_objs as go
import sqlalchemy

engine = sqlalchemy.create_engine('sqlite:///beers.db', echo=True)


app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1("Do you know your beer style?"),

    dcc.Dropdown(
        id = 'dropdown',
        options = dropdown(),
        value = 'Brown Porter',
        clearable = False
        ),
    dcc.Graph(id = 'beer-histogram',
              figure = {
              'data': [plot_words('American IPA')],
              'layout' : {
                'title': 'testing'
                      }
                        }
        )

])
import pdb
@app.callback(
    dash.dependencies.Output('beer-histogram', 'figure'),
    [dash.dependencies.Input('dropdown', 'value')])
def update_figure(selected_style):
    return {
            'data': [plot_words(selected_style)],
            'layout' : {'title': 'Top Descriptor Words'}
        }

if __name__ == '__main__':
    app.run_server(debug=True)
