import boto3
import botocore
import uuid
import lorem
import os

# to add debugger
# boto3.set_stream_logger('botocore', level='DEBUG')


# to access the low-level client interface
s3_client = boto3.client('s3')

# similarly, to access the high-level one
s3_resource = boto3.resource('s3')


# bucket creation helper
def create_bucket_name(bucket_prefix):
    # uuid will generate a random 63 chars long string representation, to which we can our bucket_prefix to get a unique name
    return ''.join([bucket_prefix, str(uuid.uuid4())])


# you can pass either the client or the ressource interface as the s3_connection as they create buckets the same way
def create_bucket(bucket_prefix, s3_connection):
    session = boto3.session.Session()
    # current_region = session.region_name
    bucket_name = create_bucket_name(bucket_prefix)
    bucket_response = s3_connection.create_bucket(
        Bucket=bucket_name)
    # unless in us east, need to instantiate a session and provied the region_name of the session to the bucket creation method
    # CreateBucketConfiguration={
    # 'LocationConstraint': current_region}
    return bucket_name, bucket_response


# you can pass either the client or the ressource interface as the s3_connection as they create buckets the same way
def create_versioned_bucket(bucket_prefix, s3_connection):
    session = boto3.session.Session()
    # current_region = session.region_name
    bucket_name = create_bucket_name(bucket_prefix)
    bucket = s3_resource.create_bucket(
        Bucket=bucket_name)
    # unless in us east, need to instantiate a session and provied the region_name of the session to the bucket creation method
    # CreateBucketConfiguration={
    # 'LocationConstraint': current_region}
    versioning = s3_resource.BucketVersioning(bucket_name)
    versioning.enable()
    print(versioning.status)
    return bucket_name, bucket


def empty_bucket(bucket_name):

    bucket = s3_resource.Bucket(bucket_name)
    objecs_to_delete = []
    for obj in bucket.objects.all():
        objecs_to_delete.append({'Key': obj.key})

    if len(objecs_to_delete):
        bucket.delete_objects(Delete={'Objects': objecs_to_delete})

# file creation helper


def create_temp_file(file_name, file_content):
    random_file_name = ''.join([str(uuid.uuid4().hex[:6]), file_name])
    with open(random_file_name, 'w') as f:
        f.write(file_content)
    return random_file_name


client_bucket_name, client_reponse = create_versioned_bucket(
    "boto3-client-bucket", s3_client)
resource_bucket_name, resource_reponse = create_versioned_bucket(
    "boto3-resource-bucket", s3_resource)

file_prefix = "text.txt"
file_name = create_temp_file(file_prefix, lorem.text())
input('File created, press enter to upload it to the client bucket')
# Using the resource high-level classes (Bucket & Object) to abstract S3 and easily use is
client_bucket = s3_resource.Bucket(name=client_bucket_name)
file_object = s3_resource.Object(bucket_name=client_bucket_name, key=file_name)


# Note that bucket and object are submodule of one another
file_object_again = client_bucket.Object(file_name)
client_bucket_again = file_object.Bucket()


# Uploading the file to S3
# object way
file_object.upload_file(Filename=file_name)

# bucket way
# client_bucket.upload_file(Filename = file_name, Key = file_name)

# client version
# s3_resource.meta.client.upload_file(Filename = file_name, Bucket = client_bucket_name, Key = file_name)

os.remove(file_name)

for bucket in s3_resource.buckets.all():
    print(bucket.name)
    # empty_bucket(bucket.name)


for bucket in s3_resource.buckets.all():
    print(bucket.name)
    try:
        s3_resource.Bucket(bucket.name).delete()
    except botocore.exceptions.ClientError as error:
        print("The bucket is probably not empty... botocore raised ==>  {}".format(error))
