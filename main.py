import requests
import json
import configparser
import sys
import signal
import ast

# should probably replace with threading
from multiprocessing import Process, Queue
from customPlotly import set_points
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

tlist = Config.get('Tokens','List')
tlist = ast.literal_eval(tlist)

# close plotly stream when SIGINT received
def signal_handler(signal, frame):
    # s.close()
    # print(': Plotly stream closed... shutting down')
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

def reader(queue):
    ## Read from the queue
    while True:
        msg = queue.get()
        if (msg == 'DONE'):
            break
        # s.write(dict(x=msg[0], y=msg[1]))
        set_points(msg[0], msg[1], msg[2], msg[3], msg[4])

def writer(array, queue):
    ## Write to the queue
    queue.put(array)   # Write 'count' numbers into the queue
    queue.put('DONE')

def new_block_callback(block_hash):
    b = web3.eth.getBlock(block_hash)
    print(bcolors.OKGREEN + "New Block: {0} | Number: {1}".format(block_hash, b['number']) + bcolors.ENDC + ' [' + str(datetime.now()) + ']')
    for t in range(0, len(b['transactions'])):
        r = web3.eth.getTransactionReceipt(b['transactions'][t])
        # first address(es) are token contracts
        # second address is hex-sha3 of ERC20 'Transfer' event
        # print(r['transactionHash'])
        if r:
            if (r['from'] in Config._sections['Exchanges'] or r['to'] in Config._sections['Exchanges']) and len(r['logs']) > 0 and r['logs'][0]['topics'][0] == Config['Setup']['TransferEvent']:
                action = ''
                edit = r['to'].split('0x')[1]
                if edit in r['logs'][0]['topics'][1]:
                    action = 'from'
                elif edit in r['logs'][0]['topics'][2]:
                    action = 'to'
                for ex in Config.items('Exchanges'):
                    if ex[0] == r['from'] or ex[0] == r['to']:
                        exchange = ex[1]
                        break

                print(bcolors.WARNING + 'Token transfer found! Exchange: {0} | Action: {1} | Block: {2}'.format(exchange, action, b['number'])+ bcolors.ENDC)
                n = False
                try:
                    n = requests.get('https://api.ethplorer.io/getTokenInfo/'+r['logs'][0]['address']+'?apiKey=freekey')
                except Exception as e:
                    print(bcolors.FAIL + 'Ethplorer ERROR: ' + str(e) + bcolors.ENDC)
                    pass

                if n:
                    n = json.loads(n.text)
                    # decimals may be undefined
                    try: 
                        decimals = int(n['decimals'])
                        amount = r['logs'][0]['data']
                        amount = int(amount, 16) # hex to dec
                        amount = amount / (10**decimals)
                        print(bcolors.OKBLUE + 'Token: ' + bcolors.ENDC + '{0} ({1})\n Amount: '.format(n['name'], n['symbol']) + bcolors.BOLD + str(amount) + bcolors.ENDC)

                        # send data to Plotly
                        if n['symbol'] in tlist:
                            # Current time on x-axis, random numbers on y-axis
                            x = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
                            y = amount
                            queue = Queue()
                            reader_p = Process(target=reader, args=((queue),))
                            reader_p.daemon = True
                            reader_p.start()    # Launch reader() as a separate python process

                            writer([x, y, n['symbol'], amount, action], queue)
                            # reader_p.join() # Wait for the reader to finish
                    except Exception as e:
                        print(bcolors.FAIL + 'ERROR: ' + str(e) + bcolors.ENDC)
                        pass
            else:
                continue
                # print('No etherdelta', r['from'], r['to'])
        else:
            print('no r? {0}'.format(r))

try:
    block_filter = web3.eth.filter('latest')
    print('Waiting for blocks...')
    block_filter.watch(new_block_callback)
except Exception as e:
    print(bcolors.FAIL + 'ERROR: ' + str(e) + bcolors.ENDC)
    pass

while True:
    pass
