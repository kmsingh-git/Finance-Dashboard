import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State

import yield_page

app = dash.Dash('test')

test_div = html.Div([
    html.Div(id='test', children=yield_page.layout)
])

app.layout = test_div

if __name__ == "__main__":
    print(dash.Dash.__doc__)