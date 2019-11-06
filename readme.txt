# Flow steps for convert report from *.txt => *.pdf:
# ==================================================
* Step 01:
=> Get report *.txt from FTP [10.1.3.30|AS/400] to [source_folder]
* Step 02:
=> Convert report *.txt from [source_folder] to [destination_folder]
* Step 03:
=> Synchronize report *.pdf from [destination_folder] to [AWS_S3]
=> Get meta-link from [AWS_S3], insert into MSSQL [10.2.8.40|DBS_TU]

# Requirement:
# ============
=> Python 3.7.5 (install)
=> python cli command installation: 

	pip install [package_name]

Package Name: 
- reportlab
- pyodbc
- python-dotenv
- boto3
- awscli


# Hierarchy path name for AWS:
# ============================
https://mst-dbsarchiving.s3-ap-southeast-1.amazonaws.com/dbs/200212/eminv/eminv_123456789012_20021204_123000.pdf
https://mst-dbsarchiving.s3-ap-southeast-1.amazonaws.com/inv/200212/inv_SI300001412_20021204.pdf

bucket	= mst-dbsarchiving 
prefix	= dbs/YYYYMM/filename_identity/filename.pdf

prefix(1) = dbs | static identification
prefix(2) = YYYYMM | etc: 200201
prefix(3) = filename_identity | lower case | etc: inv or eminv
prefix(4) = filename.pdf | original filename with extension *.pdf

# Report Types:
# =============
=> ppnrue-invoice	
=> parts-invoice
=> service-invoice
=> warranty-claim
=> warranty-settlement
=> job-closing-summary
=> sims-report