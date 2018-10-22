#!/usr/bin/python
import time
import json
import datetime
import decimal
import boto3
from boto3.dynamodb.conditions import Key, Attr

start = time.time()

dynamodb = boto3.resource('dynamodb', region_name='eu-west-1')

table = dynamodb.Table('BUD-BCN')

def show_price(date):
	response = table.query(
		KeyConditionExpression=Key('date').eq(date.strftime("%Y-%m-%d"))
	)
	
	print("--- ",date.strftime("%Y-%m-%d"))
	prev_price = 0
	for i in response['Items']:
		if i['price'] != prev_price:
			print(time.strftime('%Y %b %d %H:%M:%S', time.localtime(i['query_date'])), i['price'])
		prev_price = i['price']
		
	
date_end = datetime.datetime(2019,2,2,0,0)
d = datetime.datetime(2018,10,11,0,0)
td = datetime.timedelta(days=1)

while d < date_end:
	show_price(d)
	d = d + td