# import sys
import pyodbc
import ebcdic
# import numbers
import decimal

conn1 = pyodbc.connect(
        'Driver={iSeries Access ODBC Driver};'
        'System=10.1.3.30;'
        'Port=446;'
        'Protocol=TCPIP;'
        'UID=WEBDEV1;'
        'PWD=WEBDEV1;')
conn2 = pyodbc.connect('Driver={SQL Server};'
                      'Server=10.2.4.198;'
                      'Database=DBS_TU;'
                      'uid=DBSTU1;pwd=DBSTU1;')

db2 = conn1.cursor()
mssql = conn2.cursor()

# q = "INSERT INTO WONT_ZZZZZ (PERIOD, WONO, WOSGNO, WOOPNO, NTLNO1, NTDA, MASTRI, SOURCI) VALUES(201808, '0769433   ', '01', '  ', 'WWW', 'RECONDITION HYDRAULIC CYLINDER AT TU â\x80\x93 SBY      ', ' ', ' ')"
# mssql.execute(q)
# conn2.commit()

qry = f"SELECT * FROM LIBPOCO1.WONT1808 WHERE WONO = '0769433' and WOSGNO = '01'"
rows = db2.execute(qry)
numRec = 0
for row in rows:
  numRec += 1
  val = tuple(int(r) if isinstance(r, decimal.Decimal) else r for r in row)
  q = f'INSERT INTO WONT_ZZZZZ (PERIOD, WONO, WOSGNO, WOOPNO, NTLNO1, NTDA, MASTRI, SOURCI) VALUES{val}'
  mssql.execute(q)
  if numRec % 1000 == 0:
    conn2.commit()
    
conn2.commit()
print('Finish')
