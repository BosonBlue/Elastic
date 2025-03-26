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
    "size": 10,
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
                            "gte": "2025-03-16T00:00:00.000Z",  # 24 hours before your latest result
                            "lt": "2025-03-19T00:00:00.000Z"
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

# Make the request
response = requests.get(
    ES_URL,
    auth=(ES_USER, ES_PASS),
    headers={"Content-Type": "application/json"},
    json=payload,
    verify=False  # Equivalent to -k in curl
)

# Print the formatted JSON response
print(json.dumps(response.json(), indent=2))

# Optionally save to a file
#with open('output.json', 'w') as f:
 #   json.dump(response.json(), indent=2, fp=f)