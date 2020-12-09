import os
import pymongo
from bson.json_util import dumps
import sys
sys.path.insert(0, 'fortress-security-audit-engine')
import fortress-audit


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







def check_abnormal_behaviour: