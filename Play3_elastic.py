import requests
import json
from urllib3.exceptions import InsecureRequestWarning
import datetime
from pprint import pprint
from elasticsearch import Elasticsearch
import os

ES_USER = os.environ.get('ES_USER')
ES_PASS = os.environ.get('ES_PASS')

# Suppress only the single warning from urllib3 needed
requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)

# Elasticsearch endpoint URL
ES_URL = "https://entbas-es-master-01.wifi.uk.pri.o2.com:9200/catchall*/_search"

# Date range - past 7 days to now
now = datetime.datetime.now()
seven_days_ago = now - datetime.timedelta(days=7)

# Format timestamps for Elasticsearch
from_date = seven_days_ago.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
to_date = now.strftime("%Y-%m-%dT%H:%M:%S.%fZ")

# Query payload
payload = {
    "size": 10,  # Number of results to return
    "query": {
        "bool": {
            "must": [
                {
                    "match_phrase": {
                        "system.syslog.hostname": "entell-qfx-sys-01"
                    }
                },
                {
                    "query_string": {
                        "query": "xe-0/0/17",
                        "analyze_wildcard": True
                    }
                },
                {
                    "range": {
                        "@timestamp": {
                            "gte": from_date,
                            "lte": to_date
                        }
                    }
                }
            ]
        }
    },
    "sort": [
        {
            "@timestamp": {
                "order": "desc"
            }
        }
    ],
    "timeout": "30s"
}

# Headers
headers = {
    "Content-Type": "application/json"
}

# Make the request
response = requests.post(
    ES_URL,
    auth=(ES_USER, ES_PASS),
    headers=headers,
    data=json.dumps(payload),
    verify=False  # Note: This disables SSL verification - use only in controlled environments
)

# Check if the request was successful
if response.status_code == 200:
    result = response.json()
    print(f"Query took: {result['took']}ms")
    print(f"Total hits: {result['hits']['total']['value']}")
    
    # Print each hit
    print("\nResults:")
    for hit in result['hits']['hits']:
        # Extract the timestamp and message
        timestamp = hit['_source'].get('@timestamp', 'No timestamp')
        message = hit['_source'].get('message', 'No message')
        
        print(f"\nTimestamp: {timestamp}")
        print(f"Message: {message}")
        
        # Uncomment to print the entire document
        # print("\nFull document:")
        # pprint(hit['_source'])
        
        print("-" * 80)
else:
    print(f"Error: {response.status_code}")
    print(response.text)