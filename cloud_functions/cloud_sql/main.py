# Standard
import os
import json
# Third-Party
import pymysql
from dotenv import load_dotenv

# https://europe-west2-ad-assignment-21.cloudfunctions.net/cloud_sql_service

def cloud_sql_service(request):

    load_dotenv()

    sql_user = os.environ.get('CLOUD_SQL_USERNAME')
    sql_pass = os.environ.get('CLOUD_SQL_PASSWORD')
    sql_conn = os.environ.get('CLOUD_SQL_CONNECTION')
    sql_name = os.environ.get('CLOUD_SQL_DATABASE')

    unix_socket = '/cloudsql/{}'.format(sql_conn)
    conn = pymysql.connect(user=sql_user, password=sql_pass, unix_socket=unix_socket, db=sql_name)

    with conn.cursor() as sql_cur:
        sql_cur.execute('SELECT * FROM PRODUCT;')
        results = sql_cur.fetchall()

        return json.dumps(list(results))


