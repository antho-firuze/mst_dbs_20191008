# ======================================================
# Python Script for getting report file from FTP to [source_folder] 
#
# Created By  : Hertanto Purwanto
# Email       : antho.firuze@gmail.com
# Created at  : 2019-10-30
# File name   : 01-get_report.py
# Version     : 1.0
# ======================================================

import os, datetime, time, sys, re
import threading
import multiprocessing 
import ftplib
import queue
from dotenv import load_dotenv
from os.path import join, dirname
from itertools import islice
from functools import partial

my_queue = queue.Queue()
countProcess = 1

def storeInQueue(f):
  def wrapper(*args):
    my_queue.put(f(*args))
  return wrapper

def loadEnv():
  # Load environment data from .env file
  dotenv_path = join(dirname(__file__), '.env')
  load_dotenv(dotenv_path)

def grabFile(ftp, filename, to_dir):
  with open(f'{to_dir}/{filename}', 'wb') as localfile:
    ftp.retrbinary('RETR ' + filename, localfile.write, 1024)

# @storeInQueue
def grabFile_x(fld, filename, to_dir):
  with ftplib.FTP(os.getenv('FTP_SERVER')) as ftp:
    try:
      ftp.login(user=os.getenv('FTP_USER'), passwd=os.getenv('FTP_PASS')) 
      ftp.cwd(f'/{fld}/')
      with open(f'{to_dir}/{filename}', 'wb') as localfile:
        ftp.retrbinary('RETR ' + filename, localfile.write, 1024)
    
      # return True

    except ftplib.all_errors as e:
      print('FTP error:', e)
      # return False

def grabFile_x2(fld, to_dir, filename):
  if filename.lower().endswith(".txt"):
    if not os.path.isfile(f'{to_dir}/{filename}'):
      with ftplib.FTP(os.getenv('FTP_SERVER')) as ftp:
        try:
          ftp.login(user=os.getenv('FTP_USER'), passwd=os.getenv('FTP_PASS')) 
          ftp.cwd(f'/{fld}/')
          with open(f'{to_dir}/{filename}', 'wb') as localfile:
            ftp.retrbinary('RETR ' + filename, localfile.write, 1024)
        
          # return True

        except ftplib.all_errors as e:
          print('FTP error:', e)
          # return False

def main():
  global countProcess

  while True:
    loadEnv()
    copiedFiles = 0
    skippedFiles = 0
    # The with command will automatically close the connection to the server for Python 3 code
    with ftplib.FTP(os.getenv('FTP_SERVER')) as ftp:
      try:
          ftp.login(user=os.getenv('FTP_USER'), passwd=os.getenv('FTP_PASS')) 

          ftp_folder = os.getenv('FTP_FOLDER').split(',')
          for fld in ftp_folder:
            ftp.cwd(f'/{fld}/')
            files = ftp.nlst()
            source_folder = f"{os.getenv('CONVERT_FOLDER_SOURCE')}/{fld}"
            # Check the folder is exists
            if not os.path.exists(source_folder):
              os.makedirs(source_folder)

            with multiprocessing.Pool(processes=100) as pool:
              func = partial(grabFile_x2, fld, source_folder)
              pool.map(func, files)
              pool.close()
              pool.join()

            # for idx, f in enumerate(files):
            #   if f.lower().endswith(".txt"):
            #     # Check the file is exists
            #     if not os.path.isfile(f'{source_folder}/{f}'):
            #       # grabFile(ftp, f, source_folder)
            #       # t = threading.Thread(target=grabFile_x, args=(fld, f, source_folder,))
            #       # t.start()
            #       # t.join()

            #       # p = multiprocessing.Process(target=grabFile_x, args=(fld, f, source_folder,))
            #       # p.start()
            #       # p.join()

            #       copiedFiles += 1
            #       if idx % 100 == 0:
            #         print(f' Copying process (*.txt) => [{idx}] files copied.', end='\r')
            #     else:
            #       skippedFiles += 1
            #       # print(f'{idx}:skip:{f}')

            #   # if idx > 100:
            #   #   break

            # # print(f'{fld} = {len(files)}')

      except ftplib.all_errors as e:
          print('FTP error:', e)
    
    header = f"========== Process #{countProcess} =========="
    logger = f"\n{header}"
    cp = f'{copiedFiles:0,.0f}'
    sk = f'{skippedFiles:0,.0f}'
    logger += f"\n{' Copied of file/s':<20}{cp:>11}"
    logger += f"\n{' Skipped of file/s':<20}{sk:>11}"
    logger += f"\n{'='*len(header)}"
    print(logger)
    countProcess += 1
    time.sleep(10)

if __name__ == '__main__':
  main()