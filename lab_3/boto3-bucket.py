
import json
import urllib.parse
import boto3

print('Loading function')

# initiate a session with client id
access_key = "access_key"
secret_key = "secret_key"
session = boto3.Session(aws_access_key_id=access_key, aws_secret_access_key=secret_key)

# use session to create s3 client
s3 = session.client('s3')

# use session to create dynamodb client
dynamodb = boto3.resource('dynamodb')

# get the customers table
table = dynamodb.Table('customers')

def lambda_handler(event, context):
    #print("Received event: " + json.dumps(event, indent=2))

    # Get the object from the event and show its content type
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = urllib.parse.unquote_plus(event['Records'][0]['s3']['object']['key'], encoding='utf-8')
    try:
        response = s3.get_object(Bucket=bucket, Key=key)
        print("CONTENT TYPE: " + response['ContentType'])
        file_content = response['Body'].read().decode('utf-8')
        json_content = json.loads(file_content)
        table.put_item(Item=json_content)
        return None
    except Exception as e:
        print(e)
        print('Error getting object {} from bucket {}. Make sure they exist and your bucket is in the same region as this function.'.format(key, bucket))
        raise e