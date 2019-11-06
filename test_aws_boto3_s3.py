import logging
import boto3
import sys
from botocore.exceptions import ClientError

def bucket_exists(bucket_name):
    """Determine whether bucket_name exists and the user has permission to access it

    :param bucket_name: string
    :return: True if the referenced bucket_name exists, otherwise False
    """
    s3 = boto3.client('s3')
    try:
        response = s3.head_bucket(Bucket=bucket_name)
    except ClientError as e:
        logging.debug(e)
        return False
    return True

def list_bucket():
    s3 = boto3.client('s3')
    try:
      response = s3.list_buckets()
    except ClientError as e:
      logging.error(e)
      return None
    
    if len(response['Buckets']) > 0:
        return [bucket["Name"] for bucket in response['Buckets']]

    return None

def list_bucket_objects(bucket_name):
    """List the objects in an Amazon S3 bucket

    :param bucket_name: string
    :return: List of bucket objects. If error, return None.
    """

    # Retrieve the list of bucket objects
    s_3 = boto3.client('s3')
    try:
        response = s_3.list_objects_v2(Bucket=bucket_name)
    except ClientError as e:
        # AllAccessDisabled error == bucket not found
        logging.error(e)
        return None

    # Only return the contents if we found some keys
    if response['KeyCount'] > 0:
        return response['Contents']

    return None

def put_object(dest_bucket_name, dest_object_name, src_data):
    """Add an object to an Amazon S3 bucket

    The src_data argument must be of type bytes or a string that references
    a file specification.

    :param dest_bucket_name: string
    :param dest_object_name: string
    :param src_data: bytes of data or string reference to file spec
    :return: True if src_data was added to dest_bucket/dest_object, otherwise
    False
    """

    # Construct Body= parameter
    if isinstance(src_data, bytes):
        object_data = src_data
    elif isinstance(src_data, str):
        try:
            object_data = open(src_data, 'rb')
            # possible FileNotFoundError/IOError exception
        except Exception as e:
            logging.error(e)
            return False
    else:
        logging.error('Type of ' + str(type(src_data)) +
                      ' for the argument \'src_data\' is not supported.')
        return False

    # Put the object
    s3 = boto3.client('s3')
    try:
        s3.put_object(Bucket=dest_bucket_name, Key=dest_object_name, Body=object_data, StorageClass='GLACIER')
    except ClientError as e:
        # AllAccessDisabled error == bucket not found
        # NoSuchKey or InvalidRequest error == (dest bucket/obj == src bucket/obj)
        logging.error(e)
        return False
    finally:
        if isinstance(src_data, str):
            object_data.close()
    return True

def upload_file(file_name, bucket, object_name=None):
    """Upload a file to an S3 bucket

    :param file_name: File to upload
    :param bucket: Bucket to upload to
    :param object_name: S3 object name. If not specified then same as file_name
    :return: True if file was uploaded, else False
    """

    # If S3 object_name was not specified, use file_name
    if object_name is None:
        object_name = file_name

    # Upload the file
    s3_client = boto3.client('s3')
    try:
        response = s3_client.upload_file(file_name, bucket, object_name)
    except ClientError as e:
        logging.error(e)
        return False
    return True

def restore_object(bucket_name, object_name, days, retrieval_type='Standard'):
    """Restore an archived S3 Glacier object in an Amazon S3 bucket

    :param bucket_name: string
    :param object_name: string
    :param days: number of days to retain restored object
    :param retrieval_type: 'Standard' | 'Expedited' | 'Bulk'
    :return: True if a request to restore archived object was submitted, otherwise
    False
    """

    # Create request to restore object
    request = {'Days': days,
               'GlacierJobParameters': {'Tier': retrieval_type}}

    # Submit the request
    s3 = boto3.client('s3')
    try:
        s3.restore_object(Bucket=bucket_name, Key=object_name, RestoreRequest=request)
    except ClientError as e:
        # NoSuchBucket, NoSuchKey, or InvalidObjectState error == the object's
        # storage class was not GLACIER
        logging.error(e)
        return False
    return True

def create_bucket(bucket_name, region=None):
    """Create an S3 bucket in a specified region

    If a region is not specified, the bucket is created in the S3 default
    region (us-east-1).

    :param bucket_name: Bucket to create
    :param region: String region to create bucket in, e.g., 'us-west-2'
    :return: True if bucket created, else False
    """
    # Create bucket
    try:
        if region is None:
            s3_client = boto3.client('s3')
            s3_client.create_bucket(Bucket=bucket_name)
        else:
            s3_client = boto3.client('s3', region_name=region)
            location = {'LocationConstraint': region}
            s3_client.create_bucket(Bucket=bucket_name,
                                    CreateBucketConfiguration=location)
    except ClientError as e:
        logging.error(e)
        return False
    return True

def delete_bucket(bucket_name):
    """Delete an empty S3 bucket

    If the bucket is not empty, the operation fails.

    :param bucket_name: string
    :return: True if the referenced bucket was deleted, otherwise False
    """

    # Delete the bucket
    s3 = boto3.client('s3')
    try:
        s3.delete_bucket(Bucket=bucket_name)
    except ClientError as e:
        logging.error(e)
        return False
    return True
    
def delete_object(bucket_name, object_name):
    """Delete an object from an S3 bucket

    :param bucket_name: string
    :param object_name: string
    :return: True if the referenced object was deleted, otherwise False
    """

    # Delete the object
    s3 = boto3.client('s3')
    try:
        s3.delete_object(Bucket=bucket_name, Key=object_name)
    except ClientError as e:
        logging.error(e)
        return False
    return True

def delete_objects(bucket_name, object_names):
    """Delete multiple objects from an Amazon S3 bucket

    :param bucket_name: string
    :param object_names: list of strings
    :return: True if the referenced objects were deleted, otherwise False
    """

    # Convert list of object names to appropriate data format
    objlist = [{'Key': obj} for obj in object_names]

    # Delete the objects
    s3 = boto3.client('s3')
    try:
        s3.delete_objects(Bucket=bucket_name, Delete={'Objects': objlist})
    except ClientError as e:
        logging.error(e)
        return False
    return True
    
def get_object(bucket_name, object_name):
    """Retrieve an object from an Amazon S3 bucket

    :param bucket_name: string
    :param object_name: string
    :return: botocore.response.StreamingBody object. If error, return None.
    """

    # Retrieve the object
    s3 = boto3.client('s3')
    try:
        response = s3.get_object(Bucket=bucket_name, Key=object_name)
    except ClientError as e:
        # AllAccessDisabled error == bucket or object not found
        logging.error(e)
        return None
    # Return an open StreamingBody object
    return response['Body']

def main():
  bucket = 'mst-dbsarchiving'
  # create_bucket(bucket,'ap-southeast-1')
  print(list_bucket_objects(bucket))
  # delete_bucket(bucket)
  # print(list_bucket())

if __name__ == '__main__':
    main()