#!/usr/bin/python3
import time
import os
import subprocess
import pymysql

def check_mysql():
  while True:
    try:
      conn = pymysql.connect(host = 'mysql', port = 3306, user='root', password='123456',  charset='utf8', autocommit=True)
      if conn:
        break
    except Exception as e:
      pass
    time.sleep(3)
    print('MySQL is not ready...')
  print('MySQL Connected')

check_mysql()
time.sleep(10)
check_mysql() # check twice


def run_sql(s):
  cmd = 'beeline -u "jdbc:hive2://127.0.0.1:10000" -e "{}"'.format(s)
  status, output = subprocess.getstatusoutput(cmd)
  return status == 0

os.system("su hive -m -c 'schematool -dbType mysql -initSchema'")
# CH requires a indepent metastore instance
os.system('su hive -m -c "hive --service metastore &"')
while True:
  time.sleep(3)
  if run_sql('SELECT 1'):
    break
run_sql('CREATE TABLE u_data (userid INT,  movieid INT,  rating INT,  unixtime STRING) ROW FORMAT DELIMITED FIELDS  TERMINATED BY \'\t\' LOCATION \'hdfs://namenode:8020/data/hive/data/default.db/u_data\';')
run_sql('LOAD DATA LOCAL INPATH \'/opt/ml-100k/u.data\' OVERWRITE INTO TABLE u_data;')
