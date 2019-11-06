import pyodbc
conn = pyodbc.connect('Driver={SQL Server};'
                      'Server=10.2.4.198;'
                      'Database=DBS_TU;'
                      'uid=DBSTU1;pwd=DBSTU1;')
cursor = conn.cursor()

def main():
  doc_type = 'inv'
  doc_no = 'AR7654321'
  link = 'https://mst-dbsarchiving.s3-ap-southeast-1.amazonaws.com/inv/200212/inv_SI300001412_20021204.pdf'

  # qry = 'SELECT * FROM [mst-dbsarchiving]'
  qry = f"insert into [mst-dbsarchiving] (type,doc_no,link) values('{doc_type}','{doc_no}','{link}')"
  # print(qry)
  cursor.execute(qry)
  conn.commit()

  # cursor.execute(qry)
  # for row in cursor:
  #   print(row)

if __name__ == '__main__':
    main()