'''
@author: Kanak Singh
'''

import logging

logger = logging.getLogger('piotroski')
stream_handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
stream_handler.setFormatter(formatter)
logger.addHandler(stream_handler)
logger.setLevel(logging.DEBUG)

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Output, Input, State
import requests, json
import pandas as pd

layout = html.Div([
    html.H2('Piotroski Score'),
    'Enter the ticker for which you want the Piotroski score', html.P(),
    'Ticker: ',
    dcc.Input(id='ticker', type='text', value='AAPL'), html.Br(),
    html.Button(id='submit', children='Submit'), html.Br(),
    html.H3(id='subtitle', children='Key Figures for ____'), html.Br(),
    html.Div(id='net_income', className='piotroski_item'), html.Br(),
    html.Div(id='roa', className='piotroski_item'), html.Br(), #Return on Assets in current year
    html.Div(id='ocf', className='piotroski_item'), html.Br(), #operating cash flow in the current year
    # html.Div(id='cf_vs_ni', className='piotroski_item'), html.Br(), #Quality of earnings - no new information to show here
    html.Div(id='ltd', className='piotroski_item'), html.Br(), #Long term debt
    html.Div(id='current_ratio', className='piotroski_item'), html.Br(), #Assets/ Liabilities
    html.Div(id='no_new_shares', className='piotroski_item'), html.Br(),
    html.Div(id='gross_margin', className='piotroski_item'), html.Br(),
    html.Div(id='asset_turnover_ratio', className='piotroski_item'), html.Br(),
    html.P(id='f_score', className='piotroski_score')
])

import os
API_KEY = os.environ.get('API_KEY')
assert API_KEY is not None
logger.debug("Got the following API_KEY from the environment {}".format(API_KEY))
'''
Since whoever uses this script needs to set API_KEY as an environment variable, I think it could be an issue if multiple apps are running in the same environment, and they also have an API_KEY variable requirement. But if you're using virtualenv, then each app should be in an independent environment right. So no conflict then.
'''

def register_callbacks(app):
    # @app.callback(
    #     Output(component_id='test2', component_property='children'),
    #     [Input(component_id='test', component_property='n_clicks')]
    # )
    # def test_update(n_clicks):
    #     # os.mkdir('test')
    #     print(os.getcwd())
    #     return "Done"

    @app.callback([
        Output(component_id='subtitle', component_property='children'),
        Output(component_id='net_income', component_property='children'),
        Output(component_id='roa', component_property='children'),
        Output(component_id='ocf', component_property='children'),
        # Output(component_id='cf_vs_ni', component_property='children'),
        Output(component_id='ltd', component_property='children'),
        Output(component_id='current_ratio', component_property='children'),
        Output(component_id='no_new_shares', component_property='children'),
        Output(component_id='gross_margin', component_property='children'),
        Output(component_id='asset_turnover_ratio', component_property='children'),
        Output(component_id='f_score', component_property='children')
    ],[
        Input(component_id='submit', component_property='n_clicks')
    ],[
        State(component_id='ticker', component_property='value')
    ])
    def update_cells(n_clicks, ticker):
        ticker = ticker.upper()
        if not os.path.exists('financial-statements'):
            os.mkdir('financial-statements')
            logger.debug("Created folder financial-statements")
        pathname = f'financial-statements/{ticker.upper()}'
        fileprefix = pathname + '/{}'

        if not os.path.exists(pathname):
            logger.debug(f'Fetching financial statements for {ticker}')
            os.mkdir(pathname)
            
            is_df = pd.DataFrame(requests.get(f'https://financialmodelingprep.com/api/v3/income-statement/{ticker}?period=annual&apikey={API_KEY}').json()).T
            print(is_df.head())
            is_df.columns = is_df.iloc[0]
            is_df = is_df.iloc[1:]
            is_df.to_csv(fileprefix.format('income-statement.csv'))

            bs_df = pd.DataFrame(requests.get(f'https://financialmodelingprep.com/api/v3/balance-sheet-statement/{ticker}?period=annual&apikey={API_KEY}').json()).T
            bs_df.columns = bs_df.iloc[0]
            bs_df = bs_df.iloc[1:]
            bs_df.to_csv(fileprefix.format('balance-sheet-statement.csv'))

            cfs_df = pd.DataFrame(requests.get(f'https://financialmodelingprep.com/api/v3/cash-flow-statement/{ticker}?period=annual&apikey={API_KEY}').json()).T
            cfs_df.columns = cfs_df.iloc[0]
            cfs_df = cfs_df.iloc[1:]
            cfs_df.to_csv(fileprefix.format('cash-flow-statement.csv'))

        is_df = pd.read_csv(fileprefix.format('income-statement.csv'), index_col=0)
        bs_df = pd.read_csv(fileprefix.format('balance-sheet-statement.csv'), index_col=0)
        cfs_df = pd.read_csv(fileprefix.format('cash-flow-statement.csv'), index_col=0)

        output = [f'Key Figures for {ticker}']
        piotroski_score = 0

        # NET INCOME
        net_income = float(is_df.loc['netIncome'][0])
        output.append('Net income: ${:+,.2f}'.format(net_income))
        piotroski_score += (net_income > 0)

        # ROA
        old_assets = float(bs_df.loc['totalAssets'][1])
        current_assets = float(bs_df.loc['totalAssets'][0])
        avg_assets = (old_assets + current_assets)/2
        roa = net_income/ avg_assets
        output.append('ROA: {:+,.2f}'.format(roa))
        piotroski_score += (roa > 0)

        # OCF
        ocf = float(cfs_df.loc['operatingCashFlow'][0])
        output.append('OCF: ${:+,.2f}'.format(ocf))
        piotroski_score += (ocf > 0)

        # Quality of Earnings
        ''' Nothing to display here. But this is counted in Piotroski score '''
        piotroski_score += (ocf > net_income)

        # Long Term Debt
        old_ltd = float(bs_df.loc['longTermDebt'][1])
        current_ltd = float(bs_df.loc['longTermDebt'][0])
        output.append('Long Term Debt: Last year ${:+,.2f} Current year ${:+,.2f}'.format(old_ltd, current_ltd))
        piotroski_score += (current_ltd < old_ltd)

        # Current Ratio
        old_assets = float(bs_df.loc['totalCurrentAssets'][1])
        old_liabilities = float(bs_df.loc['totalCurrentLiabilities'][1])
        current_assets = float(bs_df.loc['totalCurrentAssets'][0])
        current_liabilities = float(bs_df.loc['totalCurrentLiabilities'][0])
        old_current_ratio = old_assets/ old_liabilities
        current_current_ratio = current_assets/ current_liabilities
        output.append('Current Ratio: Last year {:+,.2f} Current year {:+,.2f}'.format(old_current_ratio, current_current_ratio))
        piotroski_score += (current_current_ratio > old_current_ratio)

        # No New Shares
        old_common_stock = float(bs_df.loc['commonStock'][1])
        current_common_stock = float(bs_df.loc['commonStock'][0])
        output.append(f'Common Stock: Last year {old_common_stock:+,.2f} Current year {current_common_stock:+,.2f}')
        piotroski_score += (current_common_stock <= old_common_stock)

        # Gross Margin
        old_gross_profit_ratio = float(is_df.loc['grossProfitRatio'][1])
        current_gross_profit_ratio = float(is_df.loc['grossProfitRatio'][0])
        output.append(f'Gross Profit Ratio: Last year {old_gross_profit_ratio:+,.2f} Current year {current_gross_profit_ratio:+,.2f}')
        piotroski_score += (current_gross_profit_ratio > old_gross_profit_ratio)

        # Asset Turnover Ratio
        old_avg_assets = 0.5*(float(bs_df.loc['totalAssets'][1]) + float(bs_df.loc['totalAssets'][2]))
        old_revenue = float(is_df.loc['revenue'][1])
        old_asset_turnover_ratio = old_revenue / old_avg_assets
        current_avg_assets = 0.5*(float(bs_df.loc['totalAssets'][0]) + float(bs_df.loc['totalAssets'][1]))
        current_revenue = float(is_df.loc['revenue'][0])
        current_asset_turnover_ratio = current_revenue / current_avg_assets
        output.append(f'Asset Turnover Ratio: Last year {old_asset_turnover_ratio:+,.2f} Current year {current_asset_turnover_ratio:+,.2f}')
        piotroski_score += (current_asset_turnover_ratio > old_asset_turnover_ratio)

        # F Score (Piotroski)
        output.append(html.B(f'Piotroski score: {piotroski_score}'))

        return output

'''
TODO: Make this part of the webpage and readme
Notes/ Financial Analysis of author

Why Piotroski:
- Intended as a tool of 'Value Investing', meaning, look at the fundamentals of a company, and invest based on that, instead of things like high-volatility I'm guessing.
- Worked well in the past - shown to have 23.75% annual return on stocks (going long on high F-score stocks and short on low) when tested on stock market between 1976 - 1999

Cons:
- The discretization can sometimes ignore important differences. A company with net income $1 will get the same 1 point in first category as a company with net income $1 billion.

'''