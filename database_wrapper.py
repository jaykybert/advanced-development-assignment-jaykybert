# Third-Party
import pymysql


class DatabaseWrapper:

    def __init__(self, username, password, connection_string, database, is_local):
        self.username = username
        self.password = password
        self.database = database
        self.connection_string = connection_string
        self.connection = None
        self.is_local = is_local

    def connect(self):
        if self.is_local:
            print('Connecting to Cloud SQL via TCP')
            host = '127.0.0.1'
            port = 1433
            self.connection = pymysql.connect(user=self.username, password=self.password,
                                              host=host, db=self.database, port=port)
        else:
            print('Connecting to Cloud SQL via unix socket')
            unix_socket = '/cloudsql/{}'.format(self.connection_string)
            self.connection = pymysql.connect(user=self.username, password=self.password,
                                              unix_socket=unix_socket, db=self.database)

    def query(self, query):
        with self.connection.cursor() as cursor:
            cursor.execute(query)
            results = cursor.fetchall()
            return results

