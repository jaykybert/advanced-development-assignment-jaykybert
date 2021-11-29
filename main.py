# Standard
import os
# Third-Party
from flask import Flask, render_template, request
import pymysql
# Application
from decouple import config

app = Flask(__name__)

# https://google.github.io/styleguide/pyguide.html


@app.route('/')
def home():
    results = None
    # Cloud Deployment
    if os.environ.get('GAE_ENV') == 'standard':
        unix_socket = '/cloudsql/{}'.format(db_connection)
        conn = pymysql.connect(user=db_user, password=db_password,
                               unix_socket=unix_socket, db=db_database)
        with conn.cursor() as cur:
            cur.execute('SELECT * FROM PRODUCT')
            results = cur.fetchall()
        conn.close()

    # Local Deployment - Use TCP connections.
    else:
        print('No database connection')

    return render_template('home.html', results=results)


@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/login')
def login():
    print(request.cookies.get("token"))

    return render_template('login.html')


# Page Not Found
@app.errorhandler(404)
def error_404(e):
    return render_template('error.html', error=e)


# Internal Server Error
@app.errorhandler(500)
def error_500(e):
    return render_template('error.html', error=e)


# Local Deployment - SQL variables saved in .env.
if __name__ == '__main__':
    print('--------------------- Local Deployment')
    db_user = config('SQL_USERNAME')
    db_password = config('SQL_PASSWORD')
    db_database = config('SQL_DATABASE')
    db_connection = config('SQL_CONNECTION')

    app.run(host='127.0.0.1', port=8080, debug=True)
# Cloud Deployment - SQL variables saved in app.yaml.
else:
    db_user = os.environ.get('SQL_USERNAME')
    db_password = os.environ.get('SQL_PASSWORD')
    db_database = os.environ.get('SQL_DATABASE')
    db_connection = os.environ.get('SQL_CONNECTION')



