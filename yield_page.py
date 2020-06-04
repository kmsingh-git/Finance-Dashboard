import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State

layout = html.Div([
    # html.Form() # This will be the right way to do a form, complete with validations. But no need right now
    html.H2("Yield Calculator"), html.Br(),
    html.Span('Face Value ($): '),
    dcc.Input(id='face_value', type='number', value=1000),
    html.Br(),
    html.Span('Maturity (yrs): '),
    dcc.Input(id='T', type='number', value=10),
    html.Br(),
    html.Span('Price today ($): '),
    dcc.Input(id='P', type='number', value=900),
    html.Br(),
    html.Button(id='yield_submit', children='Submit'),
    html.Br(),
    html.P(id='yield_output', children='Press Submit')
], id='yield_div')

def register_callbacks(app):
    YIELD_LABEL = 'The effective yield is {:+.2f}%'

    @app.callback(Output(component_id='yield_output', component_property='children'),
        [Input(component_id='yield_submit', component_property='n_clicks')],
        [State(component_id='face_value', component_property='value'),
        State(component_id='T', component_property='value'),
        State(component_id='P', component_property='value')])
    def update_yield(n_clicks, F, T, P):
        if not (F and T and P):
            return "Please fill all the above fields"
        return YIELD_LABEL.format(((F/P)**(1/T) - 1)*100)