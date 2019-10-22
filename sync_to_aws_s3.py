# ======================================================
# Python Script for synchronize file to AWS S3 Cloud Server 
#
# Created By  : Hertanto Purwanto
# Email       : antho.firuze@gmail.com
# Created at  : 2019-10-18
# File name   : sync_to_aws_s3.py
# Version     : 1.0
# ======================================================

import boto3
import os, datetime, time, sys, re
import os.path
import pathlib
import threading
import logging
import queue
from os.path import join, dirname
from dotenv import load_dotenv
from botocore.exceptions import ClientError

my_queue = queue.Queue()

# Load environment data from .env file
dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

def storeInQueue(f):
  def wrapper(*args):
    my_queue.put(f(*args))
  return wrapper

def progrezz(t, msg, var=''):
  eli_count = 0
  while t.is_alive():
    print(msg, '.'*(eli_count+1), ' '*(2-eli_count), end='\r')
    eli_count = (eli_count + 1) % 3
    time.sleep(0.1)
  t.join()
  if not var:
    print(msg, '.....[Done]')
  else:
    print('{} {}.....[Done]'.format(msg, var))

def save_log(strLog):
	now = datetime.datetime.now()
	directory = './Logs/'
	if not os.path.exists(directory):
		os.makedirs(directory)
	f = open(directory + "LOG_" + now.strftime("%Y%m%d") + ".txt", "a+")
	f.write(strLog)
	f.close()

def hms_string(sec_elapsed):
    h = int(sec_elapsed / (60 * 60))
    m = int((sec_elapsed % (60 * 60)) / 60)
    s = sec_elapsed % 60.
    return "{}:{:>02}:{:>05.2f}".format(h, m, s)

def deleteFile(fullFileName, dirDelete=False):
  dirFile = os.path.dirname(fullFileName)
  
  if os.path.isfile(fullFileName):
    os.remove(fullFileName)

    if dirDelete:
      if not os.listdir(dirFile):
        os.rmdir(dirFile)

    return True
  else:
    if dirDelete:
      if not os.listdir(dirFile):
        os.rmdir(dirFile)

    return False

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

@storeInQueue
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

@storeInQueue
def synchronize(folder, file, f, deleteSource=False):
  if put_object(folder, file, f):
    if deleteSource:
      deleteFile(f, True)

    return True
  else:
    return False

def main():
  argDeleteSource = input('Delete source file after succeed [y/N], (Default: N)? ')
  argDeleteSource = argDeleteSource.upper() if argDeleteSource != '' else 'N'
  if not argDeleteSource in ('Y','N'):
    print('Option not valid')
    sys.exit(1)
  else:
    argDeleteSource = False if argDeleteSource == 'N' else True

  try:
    # Start timer
    start_datetime = datetime.datetime.now()
    start_time = time.time()
    numFile = 0
    successFile = 0
    errFile = 0
    strLog = '=============================================================\n'
    source_dir = os.getenv('CONVERT_FOLDER_DEST')
    a = [ name for name in os.listdir(source_dir) if os.path.isdir(os.path.join(source_dir, name)) ]
    # b = list_bucket()
    t = threading.Thread(target=list_bucket, args=())
    t.start()
    progrezz(t, 'Sync Folder')
    b = my_queue.get()

    # print(a)
    # print(b)
    for dir in a:
      if not dir in b:
        region = 'ap-southeast-1'
        t = threading.Thread(target=create_bucket, args=(dir, region,))
        t.start()
        progrezz(t, 'Create Folder', dir)

        # print('Create Folder [{}].....[Done]'.format(dir))
        # if create_bucket(dir, 'ap-southeast-1'):
        #   print('Bucket [{}] has been created'.format(dir))
        # else:
        #   print('Bucket [{}] cannot be create'.format(dir))
        #   sys.exit(1)

    for root, dirs, files in os.walk(os.getenv('CONVERT_FOLDER_DEST')):
      for file in files:
        fld = root.split('\\')[-1]
        if fld != 'destination':
          numFile += 1
          f = root + '\\' + file

          t = threading.Thread(target=synchronize, args=(fld, file, f, argDeleteSource,))
          t.start()
          progrezz(t, 'Sync File', file)
          if my_queue.get():
            successFile += 1
          else:
            errFile += 1
          

        if numFile % 1000 == 0:
          print('[+] {} files have been syncronized...'.format(numFile))

    # Get execution time
    strLog += '[+] Time start : {}\n'.format(start_datetime)
    strLog += '[+] Total [*.txt] files : {}\n'.format(numFile)
    strLog += '[+] Total files can be sync : {}\n'.format(successFile)
    strLog += '[+] Total files cannot be sync : {}\n'.format(errFile)
    strLog += '[+] Execution time for synchronize : {} seconds\n'.format(hms_string(time.time() - start_time))
    strLog += '[+] Time finish : {}\n'.format(datetime.datetime.now())
    save_log(strLog)			 
    print(strLog)

  except Exception as e:
    save_log("\n\nAn error occured...\n")
    save_log(str(e))
    print(e)

if __name__ == '__main__':
  main()