
# coding: utf-8

# In[29]:


import requests
import json
import configparser
import sys

from web3 import Web3, KeepAliveRPCProvider, IPCProvider, HTTPProvider


# In[30]:


Config = configparser.ConfigParser()
Config.read("config.ini")


# In[31]:


Config['SectionOne']['NodeURL']


# In[32]:


web3 = Web3(HTTPProvider(Config['SectionOne']['NodeURL']))


# In[33]:


def new_block_callback(block_hash):
    print("New Block: {0}".format(block_hash))
    # b = web3.eth.getBlock(block_hash)
    # for t in range(0, len(b['transactions'])):
    #     r = web3.eth.getTransactionReceipt(t)
    #     if (r['from'] or r['to'] == '0x8d12a197cb00d4747a1fe03395095ce2a5cc6819') and len(r['logs']) > 0 and r['logs'][0]['topics'][0] == '0xddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef':
    #         print('HAHA!')
    #     else:
    #         print('No etherdelta', r['from'], r['to'])


# In[34]:


block_filter = web3.eth.filter('latest')
print('ok', web3.eth.getBlock('latest'))
block_filter.watch(new_block_callback)

while True:
    pass
# In[ ]:
