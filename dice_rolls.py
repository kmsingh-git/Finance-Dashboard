import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import plotly.graph_objects as go
import pandas as pd
import random

layout = html.Div([
    html.H2("Simulate unbiased dice rolls, and observe Histogram of sum"), html.Br(),
    html.Span('Number of dice (k): '),
    dcc.Input(id='num_dice', type='number', value=2), html.Br(),
    html.Span('Number of rolls (n): '),
    dcc.Input(id='num_rolls', type='number', value=50), html.Br(),
    html.Button(id='submit', children='Submit'),
    dcc.Graph(id='histogram')
])

def register_callbacks(app):
    @app.callback(Output(component_id='histogram', component_property='figure'),
        [Input(component_id='submit', component_property='n_clicks')],
        [State(component_id='num_dice', component_property='value'),
        State(component_id='num_rolls', component_property='value')])
    def get_counts(n_clicks, k, n):
        d = {i: 0 for i in range(k, 6*k+1)}
        for _ in range(n):
            rolls = []
            for _ in range(k):
                rolls.append(random.randint(1, 6))
            d[sum(rolls)] += 1

        # d = {i: d[i]/n for i in d} # This converts it into relative frequencies

        df = pd.DataFrame(d, index=[0]).T

        barchart = go.Figure(data=[
            go.Bar(y=df[0], x=list(range(k, 6*k+1)))
        ])
        barchart.update_layout(
            title='Counts for {} rolls of {} Dice'.format(n, k),
            xaxis = dict(
                tickmode = 'linear',
                title='Sum on dice'
            ),
            yaxis = dict(
                title='Count'
            ),
            paper_bgcolor='#24252A',
            plot_bgcolor='#24252A',
            font=dict(
                color='#edf0f1'
            ),
            height=500,
            width=800
        )
        return barchart

'''
TODO: This should be part of the readme, or actual webpage, not a comment

You can see both the Central Limit Theorem, and The (weak) Law of Large Numbers at work here.

Say X_i is the output of the i_th die rolled
'''