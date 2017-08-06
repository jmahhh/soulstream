import requests
import json
import configparser
import sys

from customPlotly import s
from datetime import datetime

from web3 import Web3, KeepAliveRPCProvider, IPCProvider, HTTPProvider

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

Config = configparser.ConfigParser()
Config.read("config.ini")

web3 = Web3(HTTPProvider(Config['Setup']['NodeURL']))

def new_block_callback(block_hash):
    b = web3.eth.getBlock(block_hash)
    print(bcolors.OKGREEN + "New Block: {0} | Number: {1}".format(block_hash, b['number']) + bcolors.ENDC + ' [' + str(datetime.now()) + ']')
    for t in range(0, len(b['transactions'])):
        r = web3.eth.getTransactionReceipt(b['transactions'][t])
        # first address(es) are token contracts
        # second address is hex-sha3 of ERC20 'Transfer' event
        # print(r['transactionHash'])
        if (r['from'] in Config._sections['Exchanges'] or r['to'] in Config._sections['Exchanges']) and len(r['logs']) > 0 and r['logs'][0]['topics'][0] == Config['Setup']['TransferEvent']:
            if r['from'] in Config._sections['Exchanges']:
                action = 'from'
            else:
                action = 'to'
            for ex in Config.items('Exchanges'):
                if ex[0] == r['from'] or ex[0] == r['to']:
                    exchange = ex[1]
                    break

            print(bcolors.WARNING + 'Token transfer found! Exchange: {0} | Action: {1} | Block: {2}'.format(exchange, action, b['number'])+ bcolors.ENDC)
            n = requests.get('https://api.ethplorer.io/getTokenInfo/'+r['logs'][0]['address']+'?apiKey=freekey')
            n = json.loads(n.text)
            decimals = int(n['decimals'])
            amount = r['logs'][0]['data']
            amount = str(int(amount, 16)) # hex to dec
            keepIndex = len(amount) - decimals # adjust for decimals defined in token SC
            amount = amount[0:keepIndex]+'.'+amount[keepIndex:-1]
            print(bcolors.OKBLUE + 'Token: ' + bcolors.ENDC + '{0} ({1})\n Amount: '.format(n['name'], n['symbol']) + bcolors.BOLD + amount + bcolors.ENDC + '\n')

            # send data to Plotly
            if n['symbol'] == 'OMG':
                # Current time on x-axis, random numbers on y-axis
                x = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
                y = amount

                # Send data to your plot
                s.write(dict(x=x, y=y))
                print(bcolors.FAIL + 'Sent to plotly\n' + bcolors.ENDC)

                #     Write numbers to stream to append current data on plot,
                #     write lists to overwrite existing data on plot

                # Close the stream when done plotting
                # s.close()

        else:
            continue
            # print('No etherdelta', r['from'], r['to'])

block_filter = web3.eth.filter('latest')
print('Waiting for blocks...')
block_filter.watch(new_block_callback)

while True:
    pass
