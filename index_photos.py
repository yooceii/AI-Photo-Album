import json
import boto3
import datetime
import certifi
from elasticsearch import Elasticsearch

BUCKET = "photos-cs9223"
REGION = "us-east-1"
HOST="vpc-photos-qbrh5jqxhw4bjehfjreauzjxfa.us-east-1.es.amazonaws.com"
DATA={
	'objectKey': '',
	'bucket': '',
	'createdTimestamp': '',
	'labels': []
}
INDEX='photos'


def detect_labels(bucket, key, max_labels=10, min_confidence=90, region="us-east-1"):
	rekognition = boto3.client("rekognition", region)
	response = rekognition.detect_labels(
		Image={
			"S3Object": {
				"Bucket": bucket,
				"Name": key,
			}
		},
		MaxLabels=max_labels,
		MinConfidence=min_confidence,
	)
	return response['Labels']
	
def store(index,data):
	es = Elasticsearch([{'host':HOST,'port':443}],use_ssl=True,ca_certs=certifi.where())
	es.index(index,doc_type='photo',body=data)

def lambda_handler(event, context):
    # TODO implement
	print(event['Records'][0]['s3']['object']['key'])
	es = Elasticsearch([{'host':HOST,'port':443}])
	key=event['Records'][0]['s3']['object']['key']
	labels=detect_labels(BUCKET,key)
	DATA['objectKey']=key
	DATA['bucket']=BUCKET
	DATA['createdTimestamp']=datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
	DATA['labels']= [label['Name'] for label in labels]
	store(INDEX,DATA)