import time, sys
import os
from reportlab.lib import utils
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from os.path import join, dirname
from dotenv import load_dotenv
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase.pdfmetrics import stringWidth
from ftplib import FTP
from datetime import datetime
#from multiprocessing import Pool
#import itertools
#from shutil import copyfile
#os.chdir('/opt/dbs/convert/')
pdfmetrics.registerFont(TTFont('Univers_57_Condensed', 'font/Univers_57_Condensed.ttf'))
pdfmetrics.registerFont(TTFont('Univers_67_Condensed_Bold', 'font/Univers_67_Condensed_Bold.ttf'))
pdfmetrics.registerFont(TTFont('Univers_LT_67_Condensed_Bold_Oblique', 'font/Univers_LT_67_Condensed_Bold_Oblique.ttf'))

def convert_to_pdf(path, file, period):
	directory = os.getenv('CONVERT_FOLDER_DEST') + '/Invoice_PDF_' + period + '/' #+ path + '/'
	if not os.path.exists(directory):
		os.makedirs(directory)
	c = canvas.Canvas((directory + '%s.pdf' % file.replace('.TXT', '')), pagesize=A4)
	x = 5
	initY = y = 795
	space = 11
	thisLine = 0

	firstPage = True
	if os.getenv('CONVERT_LOGO') == 'TRUE':
		logo_width = img_width / 16
		logo_height = img_height / 16
		logo_position_y = y + 10

	with open(path + '/' + file) as fp:
		for line in fp:
		# TODO: Find best practice
			if (y < 30) or (line[0] == '1'):
				if not firstPage: 
					draw_footer(c)
					c.showPage()

				c.setFont('Courier', 11)
				y = initY
				thisLine = 0
				if os.getenv('CONVERT_LOGO') == 'TRUE':
					c.drawImage(img, x + 10, logo_position_y, logo_width, logo_height, mask='auto')

			if (line[0] != '1'):
				thisLine += 1				
				if thisLine == 1:
					draw_preprint_1(c, x+100, y)
					y = y - space
				elif thisLine == 3:
					draw_preprint_2(c, x+100, y)
					y = y - space
					draw_new_line(c, x, y)
					y = y - space						
					draw_preprint_3(c, x+100, y)
					y = y - space
				else: 
					addNewLine = add_new_line(line[0])
					for n in range(0, addNewLine):
						draw_new_line(c, x, y)
						y = y - space

				finString = line[1:len(line)].replace('\n', '')
				if finString.rstrip() != '':
					c.setFont('Courier', 11)
					c.drawString(x, y, finString)
					y = y - space

			firstPage = False
	draw_footer(c)
	try:
		c.save()
	except Exception as e:
		exit('[+] ' + str(e))

# Get total files on folder
# files_total = sum([len(files) for r, d, files in os.walk(os.getenv('CONVERT_FOLDER_SOURCE'))])
# print('[+] Converting %s file(s) to PDF...' % files_total);

def add_new_line(char):
	switcher = {
		#'1': "newLine",
		'0': 2,
		'-': 3,
	}

	return switcher.get(char, 0)

def draw_preprint_1(canvas, x, y):
	canvas.setFont('Univers_67_Condensed_Bold', 9)
	canvas.drawString(x, y, 'PTTrakindo Utama')

def draw_preprint_2(canvas, x, y):
	concatStr1 = 'FAKTUR PENJUALAN'
	concatStr2 = ' / INVOICE'
	canvas.setFont('Univers_67_Condensed_Bold', 11)
	canvas.drawString(x, y, concatStr1)
	txtWidth = stringWidth(concatStr1, 'Univers_67_Condensed_Bold', 11)
	x += txtWidth + 1
	canvas.setFont('Univers_57_Condensed', 11)
	canvas.drawString(x, y, concatStr2) # or x + 95

def draw_preprint_3(canvas, x, y):
	canvas.setFont('Univers_57_Condensed', 11)
	canvas.drawString(x, y, 'SOLD TO')
	canvas.drawString(x+260, y, 'CONSIGNED TO')

def draw_new_line(canvas, x, y):
	canvas.setFont('Courier', 11)
	canvas.drawString(x, y, '')

def draw_footer(canvas):
	strFooter1 = 'Barang-barang tidak boleh dikembalikan. Keberatan/pengaduan tidak dilayani jika barang telah keluar dari gudang kami'
	strFooter2 = 'Goods are not returnable. Claims will not be accepted once goods have left our ware house'
	canvas.setFont('Univers_57_Condensed', 8)
	canvas.drawString(100, 15, strFooter1)
	canvas.setFont('Univers_LT_67_Condensed_Bold_Oblique', 8)
	canvas.drawString(100, 5, strFooter2)

def save_log(strLog):
	now = datetime.now()
	directory = os.getenv('CONVERT_FOLDER_DEST') + '/Logs/' #+ path + '/'
	if not os.path.exists(directory):
		os.makedirs(directory)
	f = open(directory + "LOG_" + now.strftime("%y%m%d") + ".txt", "a+")
	f.write(strLog)
	f.close()

def hms_string(sec_elapsed):
    h = int(sec_elapsed / (60 * 60))
    m = int((sec_elapsed % (60 * 60)) / 60)
    s = sec_elapsed % 60.
    return "{}:{:>02}:{:>05.2f}".format(h, m, s)

# Start timer
start_datetime = datetime.now()
start_time = time.time()

# Load environment data from .env file
dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

# os.chdir(os.getenv('INIT_DIR'))

# Logo on header
if os.getenv('CONVERT_LOGO') == 'TRUE':
	img = os.getenv('CONVERT_LOGO_IMG')
	img_read = utils.ImageReader(img)
	img_width, img_height = img_read.getSize()
	
# Looping files on directory and convert txt files to PDF
numFile = 0
errFile = 0
strExecTime = '=============================================================\n'
#period = input("Enter the period of invoices to convert (YYYYMM) : ")
if(len(sys.argv) < 2):
	period = '200212'
else: 
	period = sys.argv[1]
print("Generating Invoice PDF for period {} ...".format(period))

try:
	#string = numFile + ' files ...'
	#print(string)
	for root, dirs, files in os.walk(os.getenv('CONVERT_FOLDER_SOURCE')):
	    for file in files:
	        if file.lower().endswith(".txt") and file[4:10] == period and file.find('*') == -1: # and numFile < 3 and file.upper()[13:24]=="SI**0295424":
	            convert_to_pdf(os.path.join(root), file, period)
	            ##print_to_cmd(os.path.join(root), file)
	            ##copyfile(os.path.join(root) + '/' + file, os.getenv('CONVERT_FOLDER_DEST') + '/Invoice_PDF_' + period + '/' + file)
	            numFile += 1
	            if numFile%1000 == 0:
	            	print('[+] {} files have been converted...'.format(numFile))
	        elif file[4:10] == period and file.find('*') != -1:
	        	strExecTime += '[+] File {} has been skipped.\n'.format(file)
	        	errFile += 1
	    #with Pool(5) as p:
	    #	p.map(run_program, itertools.repeat(os.path.join(root), len(files)), files)

	# Get execution time

	strExecTime += '[+] Time start : {}\n'.format(start_datetime)
	strExecTime += '[+] Total converted PDF files : {}\n'.format(numFile)
	strExecTime += '[+] Total files can not be converted : {}\n'.format(errFile)
	strExecTime += '[+] Execution time for converting file on period {} : {} seconds\n'.format(period, hms_string(time.time() - start_time))
	strExecTime += '[+] Time Finish : {}\n'.format(datetime.now())
	save_log(strExecTime)			 
	print(strExecTime)
except Exception as e:
	save_log("\n\nAn error occured...\n")
	save_log(str(e))
	print(e)