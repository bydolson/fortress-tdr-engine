import os
import pymongo
from bson.json_util import dumps
import sys
sys.path.insert(0, 'fortress-security-audit-engine')
import fortress-audit
from web3 import Web3
w3 = Web3(Web3.HTTPProvider('http://127.0.0.1:8545'))w3 = Web3(Web3.IPCProvider('./path/to/geth.ipc'))
import ConfigParser

config = ConfigParser.ConfigParser()
config.read("config.ini")
WEB3_INFURA_PROJECT_ID = config.get("myvars", "addprojectid")

client = pymongo.MongoClient("localhost", 27017)
change_stream = client.changestream.collection.watch()
for change in change_stream:
    print(dumps(change))
    print('') # for readability
    if change['type'] == "event" and change['opetaion'] == "write":
      analyse_for_audit(change)


def analyse_for_audit(change):
  for i in change['contracts']:
    audit_results = os.system('python file.py', change['contracts'][i])
    if not audit_results['passed']:
      if w3.isConnected():
        w3 = Web3(Web3.HTTPProvider('https://mainnet.infura.io/v3/'+WEB3_INFURA_PROJECT_ID))








def check_abnormal_behaviour:
