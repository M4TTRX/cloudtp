import boto3
import uuid
from progress.bar import Bar


def create_dynamo_db_table(name):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.create_table(
        TableName=name,
        KeySchema=[
            {
                'AttributeName': 'id',
                'KeyType': 'HASH'
            }
        ],
        AttributeDefinitions=[
            {
                'AttributeName': 'id',
                'AttributeType': 'S'
            },
        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 2,
            'WriteCapacityUnits': 2
        }
    )
    table.meta.client.get_waiter('table_exists').wait(TableName=name)
    print(table.item_count)


def save_csv_to_dynamo_db(table_name, csv_path):
    dynamodb = boto3.client('dynamodb')
    with open(csv_path,
              'r') as f:
        first_line = f.readline().split(',')
        for line in Bar('Processing').iter(f):
            line = line.strip()
            if line:
                line = line.split(',')
                item = {column: {"S": line[i]}
                        for i, column in enumerate(first_line)}
                item['id'] = {"S": str(uuid.uuid4())}
                dynamodb.put_item(TableName=table_name, Item=item)

                # item = {
                #     "id": 'sdnfdqhlsfdsu',
                #     'city': {'S': 'New York'},
                # }


table_name = 'tp_' + str(uuid.uuid4())
create_dynamo_db_table(table_name)
print('Table created: '+table_name)
save_csv_to_dynamo_db(table_name, './toy_dataset.csv')
print('Data saved')
