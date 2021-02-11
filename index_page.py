import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc

import yield_page, piotroski, dice_rolls

# Since we're adding callbacks to elements that don't exist in the app.layout,
# Dash will raise an exception to warn us that we might be
# doing something wrong.
# In this case, we're adding the elements through a callback, so we can ignore
# the exception.

app = dash.Dash(__name__, suppress_callback_exceptions=True)
server = app.server

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    dbc.NavbarSimple(
        children=[
            dbc.NavItem(dbc.NavLink("Yield Calculator", href="/yield")),
            dbc.NavItem(dbc.NavLink("Piotroski Score", href="/fm1")),
            dbc.NavItem(dbc.NavLink("Simulating Dice Rolls", href="/dice"))
        ],
        brand="Finance Dashboard",
        brand_href="/",
        color="primary",
        dark=True
    ),
    html.Div(id='page-content')
])

home_layout = html.Div([
    html.H2("This is the home page."),
    html.P("Click on the different links to explore different items"),
    html.P("Created by - Kanak")
])

HOME_LINK = dcc.Link('Home', href='/')

ALL_LINKS = html.Div([
    HOME_LINK, html.Br(),
    dcc.Link('Yield Calculator', href='/yield'), html.Br(),
    dcc.Link('Piotroski Score', href='/fm1'), html.Br(),
    dcc.Link('Simulating Dice Rolls', href='/dice')
])

yield_page.register_callbacks(app)

piotroski.register_callbacks(app)

dice_rolls.register_callbacks(app)

# Financial Metrics 2 and so on...

'''
Note, we can do the above thing dynamically. Can make a folder called content-pages. Then, for each python file in that folder, we import the file, create the corresponding layout, and register the corresponding callback
'''

# Update the index
@app.callback(dash.dependencies.Output('page-content', 'children'),
              [dash.dependencies.Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/yield':
        return yield_page.layout
    elif pathname == '/fm1':
        return piotroski.layout
    elif pathname == '/dice':
        return dice_rolls.layout
    else:
        return home_layout
    # You could also return a 404 "URL not found" page here


if __name__ == '__main__':
    app.run_server(debug=True)
