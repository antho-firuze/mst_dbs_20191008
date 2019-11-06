import datetime, time, sys, re
import os
from os.path import join, dirname
from dotenv import load_dotenv

import threading
import multiprocessing
# Load environment data from .env file
# dotenv_path = join(dirname(__file__), '.env')
# load_dotenv(dotenv_path)

# for root, dirs, files in os.walk(os.getenv('CONVERT_FOLDER_SOURCE')):
#   print(len(files))
#   for file in files:
#     # filetype=*.txt
#     if file.lower().endswith(".txt"):
#       filename = (file.upper()).replace('.TXT','')
#       print(filename)

result = None

def calc_square(number):
  print('Square : ' , number * number)
  result = number * number
  print(result)
def calc_quad(number):
  print('Quad : ' , number * number * number * number)
if __name__ == "__main__":
  number = 7
  # p1 = multiprocessing.Process(target=calc_square, args=(number,))
  # p2 = multiprocessing.Process(target=calc_quad, args=(number,))
  p1 = threading.Thread(target=calc_square, args=(number,))
  p2 = threading.Thread(target=calc_quad, args=(number,))
  p1.start()
  p2.start()
  p1.join()
  p2.join()

  # Wont print because processes run using their own memory location                     
  print(result)