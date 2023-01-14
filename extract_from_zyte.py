import requests
import pandas as pd
import os
import boto3
import json
from boto3.dynamodb.types import TypeSerializer
from decimal import Decimal

API_KEY_EWEN = "b7410f99c9144c5cb8309cea1fd66dbf"
Project_ID_Ewen = "632087"
spider_id_Ewen = "3"

session = boto3.Session(
    aws_access_key_id="AKIAQMIZMT6J4FTOFHFH",
    aws_secret_access_key="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",
    region_name="us-east-1"
)
dynamodb = session.resource('dynamodb')
table = dynamodb.Table("ZyteTable")

if(os.path.exists("./zyte/response.txt")):
    print("file exists")
else:
    url = 'https://storage.scrapinghub.com/items/'+Project_ID_Ewen+'/'+spider_id_Ewen
    auth = (API_KEY_EWEN,'')
    response = requests.get(url, auth=auth, stream=True)
    response_text = response.text
    with open('./zyte/response.txt', 'w',encoding='utf-8') as f:
        f.write(response_text)

data = []
with open('./zyte/response.txt', 'r',encoding='utf-8') as f:
    # Read each line in the file
    for line in f:
        # Load the JSON object from the line
        obj = json.loads(line)
        # Append the object to the data list
        data.append(obj)

# Create a dataframe from the data
df = pd.DataFrame(data)
df = df[df['price'] != -1]
df = df.drop(columns=['categories','_type'])
df["ID"] = range(len(df))
df = df.astype(str)

for _, row in df.iterrows():
    json_row = row.to_json()
    json_row = json.loads(json_row)
    table.put_item(Item=json_row)

print('caca')