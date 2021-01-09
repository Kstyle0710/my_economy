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
# print(company_df)
# print(company_df.loc[company_df["회사"]=="삼성전자", ["종목코드"]].values[0][0])

def stock_info(name, std):
    code = company_df.loc[company_df["회사"]==name, ["종목코드"]].values[0][0]
    result = fdr.DataReader(code, std)
    return result



# create DataFrame

companies = ["삼성전자", "현대차"]
start = "2000-01-01"
# print(stock_info("삼성전자", "2000-01-01"))

# print(company_df.loc[company_df['회사']=="삼성전자"]["종목코드"])
# stock_list = [stock_info(company, "2000-01-01") for company in companies]

stock_list = []
for company in companies:
    df = stock_info(company, start)
    # print(df)
    df["company"] = company_df.loc[company_df["회사"]==company, ["종목코드"]].values[0][0]
    stock_list.append(df)
#
df_multi_stock = pd.concat(stock_list)
# print(df_multi_stock)

######################################################

## DASH APP LAYOUT
app = dash.Dash(__name__)
# server = app.server

app.layout = html.Div([
    ## Lottie
    html.Div(de.Lottie(options=options, width="30%", height="30%", url=url)),

    ## properties
    html.Div([
        dcc.Dropdown(
            id='first-dropdown',
            options=[
                {'label': '삼성전자', 'value': '005930'},
                {'label': '현대차', 'value': '005380'},
                {'label': 'LG화학', 'value': '051910'}
            ],
            value=["005930"],  # dafault value
            multi=True,  # 복수 항목 선택 가능
            # placeholder = "Select a Country",    # 플레이스 홀더 표시
            # disabled = True    # 드랍다운 박스 비활성화
            # clearable=False
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
        y = df1.Close.values
        y1 = pd.Series(y)

        trace_line = go.Scatter(
            x = x1,
            y = y1,
            name = company_df.loc[company_df["종목코드"]==target, ["회사"]].values[0][0]

        )
        data.append(trace_line)

    data = data

    layout = dict(
        title = "test1",
        height = 500,
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
    app.run_server(port = 4033)
    # app.run_server(debug=True)