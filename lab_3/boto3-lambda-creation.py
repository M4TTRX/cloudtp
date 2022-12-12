import boto3
import json
import botocore


class LambdaWrapper:
    def __init__(self, lambda_client, iam_ressource):
        self.lambda_client = lambda_client
        self.iam_ressource = iam_ressource

    def create_function(self, function_name = "s3file_to_dynamodb", handler_name = "lambda_handler", iam_role = "Lambdas" ,deployment_package = "s3file_to_dynamodb.zip"):
        """
        Deploys a Lambda function.
        :param function_name: The name of the Lambda function.
        :param handler_name: The fully qualified name of the handler function. This
                             must include the file name and the function name.
        :param iam_role: The IAM role to use for the function.
        :param deployment_package: The deployment package that contains the function
                                   code in .zip format.
        :return: The Amazon Resource Name (ARN) of the newly created function.
        """
        try:

            # read the code from your zip code
            with open(deployment_package, 'rb') as f:
                zip_code = f.read()

            # use the function create_function from boto3.client
            response = self.lambda_client.create_function(
                FunctionName=function_name,
                Runtime='python3.6',
                Role=self.iam_ressource.get_role(RoleName=iam_role)['Role']['Arn'],
                Handler=handler_name,
                # trigger when an s3 bucket is added
                Triggers=[
                    {
                        'EventSourceArn': 'arn:aws:s3:::lambda-lab-3',
                        'Events': [
                            's3:ObjectCreated:*'
                        ],
                        'suffix': '.json' 
                    }
                ],
                Code={
                    'ZipFile': zip_code
                },
                Timeout=3,
                MemorySize=128,
                Publish=True
            )


            # check the response to make sure that your function is created correctly
            print('Create function successfully !')
        except botocore.exceptions.ClientError:
                print("Couldn't create function %s.", function_name)
                raise




## Test your code
lambda_client = boto3.client('lambda')
iam_ressource = boto3.client('iam')


lambda_wp = LambdaWrapper(lambda_client, iam_ressource)

lambda_wp.create_function()