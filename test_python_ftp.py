import os
import ftplib
from dotenv import load_dotenv
from os.path import join, dirname

def grabFile(ftp, filename, to_dir):
  localfile = open(f'{to_dir}/{filename}', 'wb')
  ftp.retrbinary('RETR ' + filename, localfile.write, 1024)
  localfile.close()

def placeFile(ftp, filename, from_dir):
  ftp.storbinary('STOR '+filename, open(f'{from_dir}/{filename}', 'rb'))

def fileLineCallback(line):
  print(f'## {line} #')

def main():
  # Load environment data from .env file
  dotenv_path = join(dirname(__file__), '.env')
  load_dotenv(dotenv_path)

  # The with command will automatically close the connection to the server for Python 3 code
  with ftplib.FTP(os.getenv('FTP_SERVER')) as ftp:
    try:
        ftp.login(user=os.getenv('FTP_USER'), passwd=os.getenv('FTP_PASS')) 
        ftp.cwd('/cvtpdfJWC/')
        # ftp.cwd('/AMT/')

        filename = 'WC_BA00250 _20101217_135949.TXT'

        # ftp.dir(files.append)

        # print(files)
        # print(ftp.dir())
        # print(ftp.nlst())
        ftp.retrlines(f'RETR {filename}', print)
        # files = []
        # ftp.retrlines(f'RETR {filename}', files.append)
        # print(files)
            
    except ftplib.all_errors as e:
        print('FTP error:', e)
        
    # ftp.login(user=os.getenv('FTP_USER'), passwd=os.getenv('FTP_PASS'))
    # ftp.cwd('/cvtpdf/')
    # ftp.cwd('/cvtpdfJWC/')
    # print(len(ftp.nlst()))
    # print(traverse(ftp, '/cvtpdfJWC/'))
    # ftp_walk(ftp, '/cvtpdfJWC/')

    # filename = 'WC_BA00250 _20101217_135949.TXT'
    # ftp.retrlines(f'RETR {filename}', fileLineCallback)
    # dir_dest = os.getenv('CONVERT_FOLDER_SOURCE')
    # fil_dest = f'{dir_dest}/{filename}'
    # localfile = open(fil_dest, 'wb')
    # ftp.retrbinary('RETR ' + filename, localfile.write, 1024)
    # ftp.quit()
    # localfile.close()

  print('Done')

if __name__ == '__main__':
  main()