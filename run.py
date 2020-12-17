import os
import pymongo
from bson.json_util import dumps
import sys
sys.path.insert(0, 'fortress-security-audit-engine')
import fortress-audit
from web3 import Web3
w3 = Web3(Web3.HTTPProvider('http://127.0.0.1:8545'))w3 = Web3(Web3.IPCProvider('./path/to/geth.ipc'))
import ConfigParser
from multiprocessing import Process
from pyod.models.hbos import HBOS
import json
from pandas import DataFrame
import platform
import pandas as pd
import pdb

config = ConfigParser.ConfigParser()
config.read("config.ini")
WEB3_INFURA_PROJECT_ID = config.get("variables", "WEB3_INFURA_PROJECT_ID")
PRIVATE_KEY = config.get("variables", "PRIVATE_KEY")
client = pymongo.MongoClient("localhost", 27017)
behavior_time_window = 100

def analyse_for_audit(change):
  for i in change['contracts']:
    audit_results = os.system('python file.py', change['contracts'][i])
    if not audit_results['passed']:
      if w3.isConnected():
        w3 = Web3(Web3.HTTPProvider('https://mainnet.infura.io/v3/'+WEB3_INFURA_PROJECT_ID))


def generate_dataframe(change_array):
  json_string = json.dumps(change_array)
  df = pd.read_json(json_string)
  df = df.fillna(0)
  return df


def detect_anomaly(change_array):
  df = generate_dataframe(change_array):
    clf =HBOS()
    x_values = df.index.values.reshape(df.index.values.shape[0],1)
    y_values = df.total_traded_quote_asset_volume.values.reshape(df.total_traded_quote_asset_volume.values.shape[0],1)
    clf.fit(y_values)
    y_pred = clf.predict(y_values)

    y_predict_proba = clf.predict_proba(y_values, method='unify')
    y_predict_proba = [item[1] for item in y_predict_proba]

    outlier_index = np.where(y_pred == 1)

    anomaly_score = clf.decision_function(y_values)
    anomaly_score = pd.DataFrame(anomaly_score, columns=['anomaly_score'])

    y_predict_proba = pd.DataFrame(y_predict_proba, columns=['probability'])
    prediction = pd.DataFrame(y_pred, columns=['prediction'])

    df_with_anomaly_score = pd.concat([df, anomaly_score, y_predict_proba, prediction], axis=1)

    df_sorted = df_with_anomaly_score.sort_values(by='anomaly_score', ascending=False)

    return df_sorted

def build_transaction(contract_address):
  tx = greeter.functions.greet("stopEvent").buildTransaction({'nonce': w3.eth.getTransactionCount(contract_address)})
  signed_tx = w3.eth.account.signTransaction(tx, private_key=PRIVATE_KEY)
  web3.eth.sendRawTransaction(signed_tx.rawTransaction)
  print(contract_address + ' event stopped') #fix-add better logs

if __name__ == '__main__':
  change_stream = client.changestream.collection.watch()
  change_array = []
  index = 0
  while index < len(change_stream):
      index += 1
      change = change_stream[index]
      print(dumps(change))
      change_array.append(change)
      if index % behavior_time_window == 0:
        score = detect_anomaly(change_array)
        if score > 0.50:
          build_transaction(change['contract_address'])
      if change['type'] == "event" and change['operation'] == "write":
        threat_detected = analyse_for_audit(change)
        if threat_detected:
          build_transaction(change['contract_address'])
