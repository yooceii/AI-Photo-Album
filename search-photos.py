import json
import datetime
import boto3
import os
import time
from botocore.vendored import requests

elasticSearchClient = boto3.client('es')
host = 'vpc-photos-qbrh5jqxhw4bjehfjreauzjxfa.us-east-1.es.amazonaws.com'
index = 'photos'
url = 'https://' + host + '/' + index + '/_search'

lexClient = boto3.client('lex-runtime')

def lambda_handler(event, context):
    os.environ['TZ'] = 'America/New_York'
    time.tzset()
    
    return dispatch(event)

def dispatch(event):
    print(event)
    response = sentToLex(event)
    labels = parseKeywords(response)
    return elasticSearchByLabels(labels)
        
def sentToLex(event):
    print(1)
    searchText = event['queryStringParameters']['q']
    response = lexClient.post_text(botName='AlbumBot',
      botAlias='Beta',
      userId='test',
      inputText=searchText)
    print(2)
    
    return response
      
def parseKeywords(response):
    labels = [response["slots"]["PhotoLabelOne"],response["slots"]["PhotoLabelTwo"]]
    return labels

def elasticSearchByLabels(labels):
    searchBucket = 'https://s3.amazonaws.com/photos-cs9223/'
    headers = { "Content-Type": "application/json" }
    query = { 
        "query": {
             "bool": {
                 "should":[
                    ]
                }
            }
        }
    for label in labels:
        if label != None:
            query["query"]["bool"]["should"].append({"match": {"labels": label}})
    searchResult = requests.get(url, headers=headers, data=json.dumps(query))
    response = {
        "statusCode": 200,
        "headers": {
            "Access-Control-Allow-Origin": '*'
        },
        "isBase64Encoded": "true"
    }
    hits = json.loads(searchResult.text)['hits']
    urls = []
    body = {
        'hits': {
            'total': hits['total'],
            'max_score': hits['max_score'],
            'results':[]
        } 
    }
    results = []
    for hit in hits['hits']:
        source = hit['_source']
        results.append(source['objectKey'])
        
    formatList = list(set(results))
    
    for result in formatList:
        body['hits']['results'].append({
            'objectKey': result,
            'url': searchBucket+result
        })
    body['hits']['total'] = len(formatList)
    response['body'] = json.dumps(body)
    
    return response