import numpy as np
import plotly.plotly as py
import plotly.tools as tls
import plotly.graph_objs as go
import sys
import time

tls.set_credentials_file(username='jmahhh', api_key='5m6VBRHj52c314Qy8hTc', stream_ids=['j3mkjkmnp9'])
tls.set_config_file(world_readable=True, sharing='public')

# stream_ids = tls.get_credentials_file()['stream_ids']

# Get stream id from stream id list
# stream_id = stream_ids[0]

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def set_points(x, y, symbol, amount):
    print('x: {0}'.format(x))
    print('y: {0}'.format(y))
    trace1 = go.Scatter(
        x=[x],
        y=[y],
        mode='lines+markers',
    )

    data = go.Data([trace1])

    # Add title to layout object
    layout = go.Layout(title='Time Series')

    # Make a figure object
    fig = go.Figure(data=data, layout=layout)

    # Send fig to Plotly, initialize streaming plot, open new tab
    py.plot(fig, fileopt='extend', filename='python-streaming', auto_open=False)
    print(bcolors.FAIL + 'Sent to plotly ({0}, {1})\n'.format(symbol, amount) + bcolors.ENDC)

if len(sys.argv) > 1 and sys.argv[1] == 'setup':
    print('Entering plotly setup...')
    trace1 = go.Scatter(
        x=[],
        y=[],
        mode='lines+markers',
    )

    data = go.Data([trace1])

    # Add title to layout object
    layout = go.Layout(title='Time Series')

    # Make a figure object
    fig = go.Figure(data=data, layout=layout)

    # Send fig to Plotly, initialize streaming plot, open new tab
    py.plot(fig, fileopt='extend', filename='python-streaming')
    # Make instance of stream id object
    # stream_1 = go.Stream(
    #     token=stream_id,  # link stream id to 'token' key
    #     maxpoints=60      # keep a max of 60 pts on screen
    # )



# We will provide the stream link object the same token that's associated with the trace we wish to stream to
# s = py.Stream(stream_id)

# We then open a connection
# s.open()
# print('Plotly stream opened...')

# give time to open ~J
# time.sleep(5)

# (*) Import module keep track and format current time
# import datetime
# import time

# i = 0    # a counter
# k = 5    # some shape parameter

# this bit was moved to main.py ~J

# Delay start of stream by 5 sec (time to switch tabs)
# time.sleep(5)
