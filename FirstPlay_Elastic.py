from elasticsearch import Elasticsearch
import requests
import json
import os


# Credentials and URL
ES_USER = os.environ.get('ES_USER')
ES_PASS = os.environ.get('ES_PASS')
ES_URL = "https://entbas-es-master-01.wifi.uk.pri.o2.com:9200/catchall*/_search"

# Query payload
payload = {
    "size": 9,
    "query": {
        "term": {
            "system.syslog.hostname": "entbas-dmvpn-mgmt-03"
        }
    },
    "sort": [
        {
            "@timestamp": {
                "order": "desc"
            }
        }
    ]
}

# Make the request
response = requests.get(
    ES_URL,
    auth=(ES_USER, ES_PASS),
    headers={"Content-Type": "application/json"},
    json=payload,
    verify=False  # Equivalent to -k in curl
)

data_type = response.json()

# Print the formatted JSON response
#print(json.dumps(response.json(), indent=2))

print("#" * 97)

#print(f"data type is {type(data_type)}")
#print(f"keys are {data_type.keys()}")
#print(type(data_type['hits']))
#print(data_type['hits'].keys())
Counter = 0
for x in range (len(data_type['hits']['hits'])):
    print(data_type['hits']['hits'][x]['_source']['cisco_message'])
    Counter = Counter + 1
    print( str(Counter))
    





# Optionally save to a file
#with open('output.json', 'w') as f:
    #json.dumps(response.json(), indent=2, fp=f)