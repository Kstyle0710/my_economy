import plotly.graph_objects as go
import pandas as pd
import FinanceDataReader as fdr
from urllib.request import urlopen
import dash
import dash_table
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Output, Input, State
import dash_extensions as de

## add Lotties##
url = "https://assets7.lottiefiles.com/packages/lf20_DaD4lb.json"
options = dict(loop=True, autoplay=True, rendererSettings=dict(preserveAspectRatio='xMidYMid slice'))

## 기업별 주가정보 호출 함수
company_df = pd.read_excel("./src/KRX종목코드.xlsx", dtype=object)

def stock_info(name, std):
    code = company_df.loc[company_df["회사"]==name, ["종목코드"]].values[0][0]
    result = fdr.DataReader(code, std)
    return result

# create DataFrame

companies = company_df["회사"].to_list()
start = "2000-01-01"


stock_list = []
for company in companies:
    df = stock_info(company, start)
    # print(df)
    df["company"] = company_df.loc[company_df["회사"]==company, ["종목코드"]].values[0][0]
    stock_list.append(df)
#
df_multi_stock = pd.concat(stock_list)

######################################################

## DASH APP LAYOUT
app = dash.Dash(__name__)
# server = app.server

app.layout = html.Div([
    ## Lottie
    html.Div(de.Lottie(options=options, width="20%", height="20%", url=url)),

    ## properties
    html.Div([
        dcc.Dropdown(
            id='first-dropdown',
            options=[
                {'label': '삼성전자', 'value': '005930'},
                {'label': '현대차', 'value': '005380'},
                {'label': 'LG화학', 'value': '051910'},
                {'label': 'POSCO', 'value': '005490'},
                {'label': '카카오', 'value': '035720'},
                {'label': 'NAVER', 'value': '035420'},
                {'label': '삼성바이오로직스', 'value': '207940'},
                {'label': '셀트리온', 'value': '068270'},
                {'label': '한국조선해양', 'value': '009540'},
                {'label': '현대중공업지주', 'value': '267250'},
                {'label': '코스피', 'value': 'KS11'}
            ],
            value=["005930"],  # dafault value
            multi=True,  # 복수 항목 선택 가능
        ),
        html.Button(id='submit-button', n_clicks=0, children="Submit")
    ]),

    ## graph
    html.Div([
        html.Div([
            dcc.Graph(
                id="graph-stock", figure={}
            )
        ])
    ]),
])

## CALLBACK FUNCTION

@app.callback(Output("graph-stock", "figure"),
              [Input("submit-button", "n_clicks")],
              [State("first-dropdown", "value")],
              prevent_initial_call=False)
def update_fig(n_clicks, targets):
    data = []
    for target in targets:

        df1 = df_multi_stock[df_multi_stock['company'] == target]
        x = df1.index.values
        x1 = pd.Series(x)
        y_open = df1.Open.values
        y_close = df1.Close.values
        y_high = df1.High.values
        y_low = df1.Low.values

        if target == "KS11":
            trace_line = go.Scatter(
                x=x1,
                y=y_close,
                yaxis="y2",
                name="KOSPI"
            )
            trace_candle = go.Candlestick(
                x=x1,
                open=y_open,
                high=y_high,
                low=y_low,
                close=y_close,
                yaxis="y2",
                visible=False,
                name="KOSPI",
                showlegend=False,
                increasing_line_color='red', decreasing_line_color='blue'
            )
            trace_bar = go.Ohlc(
                x=x1,
                open=y_open,
                high=y_high,
                low=y_low,
                close=y_close,
                yaxis="y2",
                visible=False,
                name="KOSPI",
                showlegend=False,
                increasing_line_color='red', decreasing_line_color='blue'
            )


        else:
            trace_line = go.Scatter(
                x=x1,
                y=y_close,
                name=company_df.loc[company_df["종목코드"] == target, ["회사"]].values[0][0]
            )

            trace_candle = go.Candlestick(
                x=x1,
                open=y_open,
                high=y_high,
                low=y_low,
                close=y_close,
                visible=False,
                name=company_df.loc[company_df["종목코드"]==target, ["회사"]].values[0][0],
                showlegend=False,
                increasing_line_color='red', decreasing_line_color='blue'
                )
            trace_bar = go.Ohlc(
                x=x1,
                open=y_open,
                high=y_high,
                low=y_low,
                close=y_close,
                visible=False,
                name=company_df.loc[company_df["종목코드"]==target, ["회사"]].values[0][0],
                showlegend=False,
                increasing_line_color='red', decreasing_line_color='blue'
                )

        data.append(trace_line)
        data.append(trace_candle)
        data.append(trace_bar)

    data = data

    layout = dict(
        title = "Stock Market",
        height = 700,
        yaxis1=dict(title='yaxis1'),
        yaxis2=dict(title='yaxis2',
                    overlaying='y',
                    side='right',
                    ),


        # graph type
        updatemenus=list([
                        dict(
                            buttons=list([
                                dict(
                                    args=[{'visible' : [True, False, False]}],
                                    label='Line',
                                    method='update'
                                    ),
                                dict(
                                    args=[{'visible' : [False, True, False]}],
                                    label='Candle',
                                    method='update'
                                    ),
                                dict(
                                    args=[{'visible' : [False, False, True]}],
                                    label='Ohlc',
                                    method='update'
                                    )
                                ]),
                            direction='down',
                            pad={'r':10, 't':10},
                            showactive=True,
                            x=0,
                            xanchor='left',
                            y=1.05,
                            yanchor='top'
                            )
                        ]),
                    autosize=False,

        ## 기간 범위 선택
        xaxis=dict(
            rangeselector=dict(
                buttons=list([
                    dict(count=1,
                         label="1m",
                         step="month",
                         stepmode="backward"),
                    dict(count=6,
                         label="6m",
                         step="month",
                         stepmode="backward"),
                    dict(count=1,
                         label="YTD",
                         step="year",
                         stepmode="todate"),
                    dict(count=1,
                         label="1y",
                         step="year",
                         stepmode="backward"),
                    dict(count=2,
                         label="2y",
                         step="year",
                         stepmode="backward"),
                    dict(count=3,
                         label="3y",
                         step="year",
                         stepmode="backward"),
                    dict(step="all")
                ])
            ),
            rangeslider=dict(
                visible=True
            ),
        )
    )
    return {
        "data":data,
        "layout":layout
    }

if __name__ == '__main__':
    # app.run_server(port=4042)
    app.run_server(debug=False)