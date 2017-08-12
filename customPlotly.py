import plotly.plotly as py
import plotly.tools as tls
import plotly.graph_objs as go
import configparser
import sys
import time
import ast
import requests
import json

from datetime import datetime

tls.set_credentials_file(username='jmahhh', api_key='5m6VBRHj52c314Qy8hTc', stream_ids=['j3mkjkmnp9'])
tls.set_config_file(world_readable=False, sharing='private')

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def organize_traces(tlist):
    traceArray = []
    for symbol in tlist:
        toTrace = go.Scatter(
            x=[],
            y=[],
            name = symbol + '_to',
            mode='lines+markers+text',
            yaxis = 'transfer amount'
        )
        fromTrace = go.Scatter(
            x=[],
            y=[],
            name = symbol + '_from',
            mode='lines+markers+text',
            yaxis = 'transfer amount'
        )
        currTrace = go.Scatter(
            x=[],
            y=[],
            name = symbol,
            mode='lines+markers+text',
            yaxis = 'price'
        )
        # This order is important, see comment re trace identification in set_points
        traceArray.append(toTrace)
        traceArray.append(fromTrace)
        traceArray.append(currTrace)

    return traceArray

def set_points(x, y, symbol, amount, action):
    traceArray = []
    for token in tlist:
        if token == symbol:
            transferTrace = go.Scatter(
                x=[x],
                y=[y],
                name = symbol + '_' + action,
                mode='lines+markers+text',
                yaxis = 'transfer amount'
            )
            placeholderTrace = go.Scatter(
                x=[],
                y=[],
                name = symbol + '_' + action,
                mode='lines+markers+text',
                yaxis = 'transfer amount'
            )
            # apparently - unfortunately - plotly does not recognise traces by their name but order in the traceArray...
            if action == 'to':
                traceArray.append(transferTrace)
                traceArray.append(placeholderTrace)
            elif action == 'from':
                traceArray.append(placeholderTrace)
                traceArray.append(transferTrace)
            try:
                n = requests.get('https://api.coinmarketcap.com/v1/ticker/' + idList[0] + '/')
            except Exception as e:
                print(bcolors.FAIL + 'coinmarketcap ERROR: ' + str(e) + bcolors.ENDC)
                pass
            if n:
                n = json.loads(n.text)
                x = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
                currTrace = go.Scatter(
                    x=[x],
                    y=[n[0]['price_usd']],
                    name = symbol,
                    mode='lines+markers+text',
                    yaxis = 'price'
                )
                traceArray.append(currTrace)

        else:
            transferTrace = go.Scatter(
                x=[],
                y=[],
                name = symbol + '_' + action,
                mode='lines+markers+text',
                yaxis = 'transfer amount'
            )
            traceArray.append(transferTrace)

    # Update Plotly
    fig = go.Figure(data=traceArray)
    py.plot(fig, fileopt='extend', filename=Config['Setup']['PlotName'] + '_' + symbol, auto_open=False)
    print(bcolors.FAIL + 'Sent to plotly ({0}, {1})'.format(symbol, amount) + bcolors.ENDC + ' [' + str(datetime.now()) + ']')

Config = configparser.ConfigParser()
Config.read("config.ini")

tlist = Config.get('Tokens','List')
tlist = ast.literal_eval(tlist)

idList = Config.get('Tokens','IdList')
idList = ast.literal_eval(idList)

if len(sys.argv) > 1 and sys.argv[1] == 'setup':
    data = organize_traces(tlist)

    layout = go.Layout(title=Config['Setup']['PlotTitle'])
    fig = go.Figure(data=data, layout=layout)
    for token in tlist:
        py.plot(fig, fileopt='extend', filename=Config['Setup']['PlotName'] + '_' + token)
