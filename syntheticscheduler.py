import sys
import argparse
import configparser
import requests




config = configparser.ConfigParser()
config.read('config.ini')

api_url_base = config['default']['api_url_base']
#print(api_url_base)
api_token = config['default']['api_token']
#print(api_token)
synthetic_api= config['default']['synthetic_api']

parser = argparse.ArgumentParser(description='Use cron to manage the dynatrace synthetics')
parser.add_argument('--tags', help='CSV list of tags the Dyntrace Synthetic tansaction needs to have in addition to APIManaged', dest='tags')
parser.add_argument('--enabled', help='--enabled [True|False], should the synthetics be enabled', dest='enabled')

args = parser.parse_args()

headers = {'accept': 'application/json; charset=utf-8',
           'Content-type': 'application/json',
           'Authorization': 'Api-Token {0}'.format(api_token)}

def get_synthetic_list(tags):
   api_url = '{0}{1}?{2}'.format(api_url_base, synthetic_api, tags)
   #print(api_url)
   response = requests.get(api_url, headers=headers)
   return response;

def get_synthetic_details(entityId):
   api_url = '{0}{1}/{2}'.format(api_url_base, synthetic_api, entityId)
   #print(api_url)
   response = requests.get(api_url, headers=headers)
   return response;

def update_synthetic(entityId, data):
   api_url = '{0}{1}/{2}'.format(api_url_base, synthetic_api, entityId)
   response = requests.put(api_url, headers=headers, json=data)
   return response


#print(args.tags)
#print(args.enabled)

tags = "tag=APIManaged"
inputTagsList = args.tags.split(",")

for tag in inputTagsList:
	tags =  tags + '&tag=' + tag

#print(tags)
r = get_synthetic_list(tags)
#print(r)

if r.status_code != 200:
  sys.exit('RestAPI Error')

syntheticList = r.json()['monitors']

#print(syntheticList)

if len(syntheticList) == 0:
  sys.exit('No synthetic txs match')

for tx in syntheticList:
  #print(tx['entityId'])
  r=get_synthetic_details(tx['entityId'])
  if r.status_code != 200:
    sys.exit('RestAPI Error get details for ' + entityId)
  tx_details = r.json()
  tx_details['enabled'] = args.enabled
  #print(tx_details)
  r = update_synthetic(tx_details['entityId'], tx_details)
  #print(r)
  if r.status_code != 204:
    sys.exit('RestAPI Error updating details for ' + entityId)

  
