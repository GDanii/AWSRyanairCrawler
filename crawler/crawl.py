#!/usr/bin/python
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import json
import datetime
import boto3
import sys

if len(sys.argv) < 3:
	print("Need FROM and TO airport")
	sys.exit()

start = time.time()

options = Options()  
options.add_argument("--headless") 
options.add_argument('--ignore-certificate-errors')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
driver = webdriver.Chrome(options=options)

dynamodb = boto3.resource('dynamodb', region_name='eu-west-1')
dynamodb_client = boto3.client('dynamodb', region_name='eu-west-1')

from_airport = sys.argv[1]
to_airport = sys.argv[2]

table_name = from_airport + "-" + to_airport
d = datetime.datetime.fromtimestamp(time.time())
date_end = datetime.datetime(2019,9,1,0,0)

print("Start: ",table_name,d.strftime("%Y-%m-%d"),date_end.strftime("%Y-%m-%d"))

existing_tables = dynamodb_client.list_tables()['TableNames']

if table_name not in existing_tables:
	response = dynamodb.create_table(
        AttributeDefinitions=[
            {
                'AttributeName': 'date',
                'AttributeType': 'S',
            },
            {
                'AttributeName': 'query_date',
                'AttributeType': 'N',
            },
        ],
        KeySchema=[
            {
                'AttributeName': 'date',
                'KeyType': 'HASH',
            },
            {
                'AttributeName': 'query_date',
                'KeyType': 'RANGE',
            },
        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 5,
            'WriteCapacityUnits': 5,
        },
        TableName=table_name,
    )

table = dynamodb.Table(table_name)

done_dates = []

def get_price(date):
	print("Get",date.strftime("%Y-%m-%d"))
	driver.get("https://www.ryanair.com/gb/en/booking/home/"+from_airport+"/"+to_airport+"/"+date.strftime("%Y-%m-%d")+"//1/0/0/0")

	new = driver.page_source;
	old = ""
	while old != new:
		old = new
		new = driver.page_source;
		
	date_list = driver.find_elements_by_class_name("date")
	price = driver.find_elements_by_class_name("fare")
	query_date = int(time.time())
	for d in zip(date_list, price):
		if len(d) == 2 and d[0].text != '':
			p = d[1].text.split(' ')
			if len(p) > 1 and p[1] != '0':
				current_date = datetime.datetime.strptime(date.strftime("%Y ")+d[0].text, "%Y %a %d %b").strftime("%Y-%m-%d")
				currency = d[1].text.split(" ")[0]
				price = int(float(d[1].text.split(" ")[1].replace(",","")))
				if price > 0 and current_date not in done_dates:
					print(current_date,price,currency)
					
					done_dates.append(current_date)
					
					response = table.put_item(
					   Item={
							'date': current_date,
							'query_date': query_date,
							'price': price,
							'currency': currency
						}
					)
				
td = datetime.timedelta(days=3)

while d < date_end:
	get_price(d)
	d = d + td
		
print("Took",time.time()-start)