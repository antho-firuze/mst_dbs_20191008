import pyodbc

conn = pyodbc.connect(
        'Driver={iSeries Access ODBC Driver};'
        'System=10.1.3.30;'
        'Port=446;'
        'Protocol=TCPIP;'
        'UID=WEBDEV1;'
        'PWD=WEBDEV1;')

# conn = pyodbc.connect(
#         'Driver={IBM i Access ODBC Driver};'
#         'System=10.1.3.30;'
#         'Port=446;'
#         'Protocol=TCPIP;'
#         'UID=WEBDEV1;'
#         'PWD=WEBDEV1;')

# conn = pyodbc.connect('Driver={SQL Server};'
#                       'Server=10.2.4.198;'
#                       'Database=DBS_TU;'
#                       'uid=DBSTU1;pwd=DBSTU1;')
cursor = conn.cursor()

# conn = 'SYSTEM=%s;db2:DSN=%s;UID=%s;PWD=%s;DRIVER=%s;' % ('10.1.3.30', '{IBM DB2 ODBC DRIVER}', 'WEBDEV1', 'WEBDEV1', '{IBM DB2 ODBC Driver}')
# conn = pyodbc.connect(conn)
# import ibm_db
# conn = ibm_db.connect('LIBPOCO1', 'WEBDEV1', 'WEBDEV1')
# import ibm_db_dbi
# conn = ibm_db_dbi.Connection(ibm_db_conn)
# conn.tables('SYSCAT', '%')
# import ibm_db
# import ibm_db_dbi
# dsn_driver = "IBM DB2 ODBC DRIVER"
# dsn_database = "LIBPOCO1"           
# dsn_hostname = "10.1.3.30" 
# dsn_port = "446"                
# dsn_protocol = "TCPIP"      
# dsn_uid = "WEBDEV1"        
# dsn_pwd = "WEBDEV1"
# dsn = (
# "DRIVER={{IBM DB2 ODBC DRIVER}};"
# "DATABASE={0};"
# "HOSTNAME={1};"
# "PORT={2};"
# "PROTOCOL=TCPIP;"
# "UID={3};"
# "PWD={4};").format(dsn_database, dsn_hostname, dsn_port, dsn_uid, dsn_pwd)

# conn = ibm_db.connect(dsn, "", "")
# pconn = ibm_db_dbi.Connection(conn)
# some_query = "SELECT *....."         # just an example
# df = pd.read_sql(some_query, pconn)

# qry = f"SELECT count(*) FROM WONT1808"
# rowc = cursor.execute(qry).fetchone()[0]
# qry = f"SELECT * FROM [mst-dbsarchiving]"
qry = f"SELECT * FROM LIBPOCO1.WONT1808 WHERE WONO = '0769433' and WOSGNO = '01'"
# qry = f"SELECT * FROM LIBPOCO1.WONT1808 FETCH FIRST 10 ROWS ONLY"
rows = cursor.execute(qry)

# print(rowc)

for row in rows:
        print(row)
