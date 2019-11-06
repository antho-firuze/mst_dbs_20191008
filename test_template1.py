import os
from os.path import join, dirname
from dotenv import load_dotenv
from reportlab.lib import utils
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.units import cm
from reportlab.lib.colors import pink, black, red, blue, green
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

pdfmetrics.registerFont(TTFont('Tahoma', 'font/Tahoma.ttf'))
pdfmetrics.registerFont(TTFont('Tahoma-Bold', 'font/Tahomabd.ttf'))
pdfmetrics.registerFont(TTFont('Univers_57_Condensed', 'font/Univers_57_Condensed.ttf'))
pdfmetrics.registerFont(TTFont('Univers_67_Condensed_Bold', 'font/Univers_67_Condensed_Bold.ttf'))
pdfmetrics.registerFont(TTFont('Univers_LT_67_Condensed_Bold_Oblique', 'font/Univers_LT_67_Condensed_Bold_Oblique.ttf'))
pdfmetrics.registerFont(TTFont('Lucida_Console', 'font/Lucida_Console_Regular.ttf'))

c = Canvas('template1.pdf', pagesize=A4)

# Load environment data from .env file
dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

# Logo 
# if os.getenv('CONVERT_LOGO') == 'TRUE':
# 	img = os.getenv('CONVERT_LOGO_IMG')
# 	img_read = utils.ImageReader(img)
# 	img_width, img_height = img_read.getSize()

def template_wc(c):
  c.translate(cm,cm)
  x = 1*cm
  y = 1*cm
  c.setStrokeColor(green)
  c.setFillColor(red)
  c.setFont("Tahoma", 9)
  c.drawCentredString(x+8.3*cm, y-0.5*cm, "DEALER CLAIM COPY")
  c.setFillColor(green)
  c.setFont("Tahoma", 7)
  c.setLineWidth(1)
  #1 AUTHORIZER & DEALERSHIP
  c.grid([x, x+4.5*cm, x+13.7*cm, x+16.5*cm],[y+0, y+1*cm, y+2*cm])
  c.drawCentredString(x+2.25*cm, y+0.7*cm, "AUTHORIZER'S NAME")
  c.drawCentredString(x+9*cm, y+0.7*cm, "CLAIM AUTHORIZER'S SIGNATURE")
  c.drawCentredString(x+15*cm, y+0.7*cm, "DATE")
  c.drawCentredString(x+2.25*cm, y+1.7*cm, "DEALERSHIP NAME")
  c.drawCentredString(x+9*cm, y+1.7*cm, "AUTHORIZED DEALER SIGNATURE(S)")
  c.drawCentredString(x+15*cm, y+1.7*cm, "DATE")
  #2 PARTS
  c.grid([x, x+2.7*cm, x+4.9*cm, x+7.1*cm, x+9.5*cm, x+11.8*cm, x+16.5*cm],[y+2*cm, y+3*cm])
  c.drawCentredString(x+1.4*cm, y+2.7*cm, "PARTS")
  c.drawCentredString(x+3.8*cm, y+2.7*cm, "LABOR")
  c.drawCentredString(x+6*cm, y+2.7*cm, "TRAVEL")
  c.drawCentredString(x+8.3*cm, y+2.7*cm, "VEHICLE")
  c.drawCentredString(x+10.7*cm, y+2.7*cm, "MISC.")
  c.drawCentredString(x+13.9*cm, y+2.7*cm, "SETTLEMENT NOTICE")
  #3 CLAIMED
  c.setLineWidth(2)
  c.grid([x, x+16.5*cm],[y+2*cm, y+3.5*cm])
  c.setFont("Tahoma", 9)
  c.drawCentredString(x+8.3*cm, y+3.1*cm, "CLAIMED DEALER EXPENSES (DEALER USE)")
  #4 REPETITION
  c.setLineWidth(1)
  c.grid([x, x+16.5*cm],[y+3.5*cm, y+12.9*cm, y+13.9*cm, y+14.6*cm, y+15.3*cm])
  c.setFont("Tahoma", 7)
  c.drawCentredString(x+0.5*cm, y+13.3*cm, "ID")
  c.drawCentredString(x+1.5*cm, y+13.3*cm, "QTY")
  c.drawCentredString(x+3.3*cm, y+13.3*cm, "PART NO")
  c.drawCentredString(x+6.2*cm, y+13.3*cm, "DESCRIPTION")
  # t = c.beginText()
  # t.setTextOrigin(x+8.8*cm, y+13.3*cm)
  # t.textLine('''DESC.\nCODE''')
  # c.drawText(t)
  c.drawCentredString(x+8.8*cm, y+13.4*cm, "DESC.")
  c.drawCentredString(x+8.8*cm, y+13.1*cm, "CODE")
  c.drawCentredString(x+10.5*cm, y+13.3*cm, "RATE")
  c.drawCentredString(x+13*cm, y+13.3*cm, "TOTAL")
  c.drawCentredString(x+14.1*cm, y+13.3*cm, "CURR")
  c.drawCentredString(x+15.2*cm, y+13.4*cm, "DEC")
  c.drawCentredString(x+15.2*cm, y+13.1*cm, "POS")
  #5 HOURS
  c.grid([x, x+1.3*cm, x+3.5*cm, x+4.9*cm, x+7.1*cm, x+9.3*cm, x+11.8*cm],[y+15.3*cm, y+16.1*cm])
  c.setFont("Tahoma", 7)
  c.drawCentredString(x+0.6*cm, y+15.8*cm, "HOURS")
  c.drawCentredString(x+2.3*cm, y+15.8*cm, "AMOUNT")
  c.drawCentredString(x+4.2*cm, y+15.8*cm, "HOURS")
  c.drawCentredString(x+6.1*cm, y+15.8*cm, "AMOUNT")
  c.drawCentredString(x+8.5*cm, y+15.8*cm, "MI/KM")
  c.drawCentredString(x+11*cm, y+15.8*cm, "AMOUNT")
  c.drawCentredString(x+13*cm, y+16.2*cm, "OTHER")
  c.drawCentredString(x+13*cm, y+15.9*cm, "AMOUNT")
  c.drawCentredString(x+14.8*cm, y+16.2*cm, "CURR")
  c.drawCentredString(x+14.8*cm, y+15.9*cm, "CODE")
  c.drawCentredString(x+16*cm, y+16.2*cm, "DEC")
  c.drawCentredString(x+16*cm, y+15.9*cm, "POS")
  #6 REPAIR
  c.grid([x, x+3.5*cm, x+7.1*cm, x+11.8*cm, x+14.1*cm, x+15.6*cm, x+16.5*cm],[y+15.3*cm, y+16.6*cm])
  c.drawCentredString(x+1.8*cm, y+16.3*cm, "REPAIR")
  c.drawCentredString(x+5.2*cm, y+16.3*cm, "TRAVEL")
  c.drawCentredString(x+9.5*cm, y+16.3*cm, "MILEAGE")
  #7 NON-CLAIMED
  c.setLineWidth(2)
  c.grid([x, x+16.5*cm],[y+15.3*cm, y+17.2*cm])
  c.setFont("Tahoma", 9)
  c.drawCentredString(x+8.3*cm, y+16.8*cm, "NON-CLAIMED DEALER EXPENSES")
  #8 
  c.setLineWidth(1)
  c.grid([x, x+1.6*cm, x+2.7*cm, x+5.3*cm, x+6.6*cm, x+8.3*cm],[y+17.2*cm, y+18*cm])
  c.setFont("Tahoma", 7)
  c.drawCentredString(x+0.8*cm, y+17.7*cm, "MAKE")
  c.drawCentredString(x+2.2*cm, y+17.7*cm, "CAB")
  c.drawCentredString(x+4*cm, y+17.7*cm, "SERIAL NO")
  c.drawCentredString(x+6*cm, y+17.7*cm, "PARTS")
  c.drawCentredString(x+7.5*cm, y+17.7*cm, "LABOR")
  c.setFont("Tahoma", 9)
  c.drawCentredString(x+9.1*cm, y+18.1*cm, "IMPORT")
  c.drawCentredString(x+10.8*cm, y+18.1*cm, "CLAIM")
  c.drawCentredString(x+12.5*cm, y+18.1*cm, "POLICY")
  c.drawCentredString(x+14.8*cm, y+18.1*cm, "CATERPILLAR")
  c.setFont("Tahoma", 7)
  c.drawCentredString(x+9.1*cm, y+17.8*cm, "PERCENT")
  c.drawCentredString(x+10.8*cm, y+17.8*cm, "AUTHO.NO.")
  c.drawCentredString(x+12.5*cm, y+17.8*cm, "CODE")
  c.drawCentredString(x+14.8*cm, y+17.8*cm, "CLAIM NO.")
  #9
  c.grid([x, x+5.3*cm, x+8.3*cm, x+10*cm, x+11.7*cm, x+13.3*cm, x+16.5*cm],[y+17.2*cm, y+18.5*cm])
  c.setFillColor(green, 0.3)
  c.rect(x+13.3*cm, y+17.2*cm, 3.2*cm, 1.3*cm, fill=1)
  c.setFillColor(green)
  c.setFont("Tahoma", 9)
  c.drawCentredString(x+2.7*cm, y+18.1*cm, "RELATED EQIPMENT")
  c.drawCentredString(x+6.7*cm, y+18.1*cm, "CUST.CREDIT%")
  #10
  c.grid([x, x+6.7*cm, x+16.5*cm],[y+18.5*cm, y+19.8*cm])
  c.setFont("Tahoma", 9)
  c.drawCentredString(x+3.3*cm, y+19.5*cm, "FINDINGS/COMMENTS")
  c.drawCentredString(x+11.5*cm, y+19.5*cm, "FOR DEALER USE")
  #11.1 s/d 11.4
  c.grid([x, x+2.7*cm, x+6*cm],[y+19.8*cm, y+20.6*cm])
  c.grid([x+6*cm, x+7*cm],[y+19.8*cm, y+21.1*cm])
  c.grid([x+7*cm, x+10*cm, x+13.3*cm],[y+19.8*cm, y+20.6*cm])
  c.grid([x+13.3*cm, x+16.5*cm],[y+19.8*cm, y+21.1*cm])
  c.setFillColor(green, 0.3)
  c.rect(x+2.7*cm, y+19.8*cm, 3.3*cm, 0.8*cm, fill=1)
  c.rect(x+10*cm, y+19.8*cm, 3.3*cm, 0.8*cm, fill=1)
  c.setFillColor(green)
  c.setFont("Tahoma", 7)
  c.drawCentredString(x+1.4*cm, y+20.3*cm, "PART NO")
  c.drawCentredString(x+4.3*cm, y+20.3*cm, "PART NAME")
  c.drawCentredString(x+6.5*cm, y+20.4*cm, "CODE")
  c.drawCentredString(x+8.5*cm, y+20.3*cm, "GROUP NO.")
  c.drawCentredString(x+11.6*cm, y+20.3*cm, "GROUP NAME")
  #12
  c.grid([x, x+6*cm],[y+19.8*cm, y+21.1*cm])
  c.grid([x+7*cm, x+13.3*cm],[y+19.8*cm, y+21.1*cm])
  c.setFont("Tahoma", 9)
  c.drawCentredString(x+3*cm, y+20.7*cm, "PART CAUSING FAILURE")
  c.drawCentredString(x+6.5*cm, y+20.7*cm, "DESC")
  c.drawCentredString(x+10.2*cm, y+20.7*cm, "GROUP CONTAINING FAILED PART")
  #13
  c.grid([x, x+1.5*cm, x+4.5*cm],[y+21.1*cm, y+21.9*cm])
  c.setFont("Tahoma", 7)
  c.drawCentredString(x+0.8*cm, y+21.6*cm, "CODE")
  c.drawCentredString(x+3*cm, y+21.6*cm, "CLAIM NO")
  c.drawCentredString(x+5.4*cm, y+21.7*cm, "TYPE")
  c.drawCentredString(x+7.3*cm, y+21.7*cm, "SERIAL NO")
  c.drawCentredString(x+9.7*cm, y+21.7*cm, "HR/MI/KM")
  c.drawCentredString(x+12.3*cm, y+21.7*cm, "HR/MI/KM")
  c.drawCentredString(x+14.8*cm, y+21.7*cm, "HOURS")
  #14
  c.grid([x, x+4.5*cm, x+6.3*cm, x+8.2*cm, x+11.2*cm, x+13.2*cm, x+16.5*cm],[y+21.1*cm, y+22.4*cm])
  c.setFont("Tahoma", 9)
  c.drawCentredString(x+2.3*cm, y+22*cm, "INITIAL DEALER")
  c.drawCentredString(x+5.4*cm, y+22*cm, "COVERAGE")
  c.drawCentredString(x+7.3*cm, y+22*cm, "PROD ID")
  c.drawCentredString(x+9.7*cm, y+22*cm, "PRODUCT")
  c.drawCentredString(x+12.3*cm, y+22*cm, "PARTS")
  c.drawCentredString(x+14.8*cm, y+22*cm, "REPAIR")
  #15
  c.grid([x, x+1.5*cm, x+4.5*cm, x+6.3*cm, x+9.2*cm, x+11.4*cm, x+13.7*cm, x+16.5*cm],[y+22.4*cm, y+23.7*cm])
  c.setFillColor(green, 0.3)
  c.rect(x+6.3*cm, y+22.4*cm, 2.9*cm, 1.3*cm, fill=1)
  c.setFillColor(green)
  c.setFont("Tahoma", 7)
  c.drawCentredString(x+0.8*cm, y+23*cm, "CODE")
  c.drawCentredString(x+3.1*cm, y+23*cm, "CLAIM NO")
  c.drawCentredString(x+5.5*cm, y+23*cm, "CODE")
  c.drawCentredString(x+7.8*cm, y+23*cm, "MODEL NO")
  c.drawCentredString(x+10.3*cm, y+23*cm, "DDMMMYY")
  c.drawCentredString(x+12.5*cm, y+23*cm, "DDMMMYY")
  c.drawCentredString(x+15*cm, y+23*cm, "DDMMMYY")
  c.setFont("Tahoma", 9)
  c.drawCentredString(x+0.8*cm, y+23.3*cm, "DEALER")
  c.drawCentredString(x+3.1*cm, y+23.3*cm, "DEALER")
  c.drawCentredString(x+5.5*cm, y+23.3*cm, "TEPS")
  c.drawCentredString(x+7.8*cm, y+23.3*cm, "SALES")
  c.drawCentredString(x+10.3*cm, y+23.3*cm, "DELIVERY")
  c.drawCentredString(x+12.5*cm, y+23.3*cm, "PARTS START")
  c.drawCentredString(x+15*cm, y+23.3*cm, "REPAIR DATE")
  #16
  c.grid([x+11*cm, x+11.8*cm, x+12.6*cm, x+13.4*cm, x+14.2*cm, x+15*cm, x+15.8*cm, x+16.5*cm],[y+23.7*cm, y+24.5*cm])
  c.setFont("Tahoma", 7)
  c.drawCentredString(x+11.5*cm, y+24.2*cm, "EM")
  c.drawCentredString(x+12.2*cm, y+24.2*cm, "TE")
  c.drawCentredString(x+13*cm, y+24.2*cm, "IE")
  c.drawCentredString(x+13.7*cm, y+24.2*cm, "ME")
  c.drawCentredString(x+14.5*cm, y+24.2*cm, "LT")
  c.drawCentredString(x+15.3*cm, y+24.2*cm, "PT")
  c.drawCentredString(x+16.2*cm, y+24.2*cm, "OT")
  #17
  c.grid([x+11*cm, x+16.5*cm],[y+24.5*cm, y+25*cm])
  c.setFont("Tahoma", 9)
  c.drawCentredString(x+13.7*cm, y+24.6*cm, "PRODUCT ABBREVIATION")
  #LOGO
  img = "files/CBM_E_TrakindoLogo.png"
  img_read = utils.ImageReader(img)
  img_width, img_height = img_read.getSize()
  c.drawImage(img, x, y+24*cm, img_width / 16, img_height / 16, mask='auto')
  c.setFont("Tahoma-Bold", 12)
  c.drawCentredString(x+8*cm, y+24.6*cm, "SERVICE")
  c.drawCentredString(x+8*cm, y+24.2*cm, "CLAIM")
  c.setFont("Tahoma", 7)
  c.drawCentredString(x+14*cm, y+25.7*cm, "PAGE _____________")

def template_inv(c):
  c.translate(cm,cm)
  x = 1*cm
  y = 1*cm
  # LOGO
  img = "files/CBM_E_TrakindoLogo.png"
  img_read = utils.ImageReader(img)
  img_width, img_height = img_read.getSize()
  c.drawImage(img, x, y+24*cm, img_width / 16, img_height / 16, mask='auto')
	# 1
  c.setFont('Univers_67_Condensed_Bold', 9)
  c.drawString(x+3.2*cm, y+23.7*cm, 'PTTrakindo Utama')
	# 2
  c.setFont('Univers_67_Condensed_Bold', 11)
  c.drawString(x+3.2*cm, y+21.7*cm, 'FAKTUR PENJUALAN')
  c.setFont('Univers_57_Condensed', 11)
  c.drawString(x+6.7*cm, y+21.7*cm, ' / INVOICE') 
  # 3
  c.setFont('Univers_57_Condensed', 11)
  c.drawString(x+3.2*cm, y+21*cm, 'SOLD TO')
  c.drawString(x+12.4*cm, y+21*cm, 'CONSIGNED TO')
  # 4
  strFooter1 = 'Barang-barang tidak boleh dikembalikan. Keberatan/pengaduan tidak dilayani jika barang telah keluar dari gudang kami'
  strFooter2 = 'Goods are not returnable. Claims will not be accepted once goods have left our ware house'
  c.setFont('Univers_57_Condensed', 8)
  c.drawCentredString(9.5*cm, -0.2*cm, strFooter1)
  c.setFont('Univers_LT_67_Condensed_Bold_Oblique', 8)
  c.drawCentredString(9.5*cm, -0.5*cm, strFooter2)

template_inv(c)


c.showPage()
c.save() 