# Standard
import os
import sys
# Third-Party
from flask import Flask, render_template, request
import pymysql
# Application-Specific
if __name__ == '__main__':
    sys.path.append('local/')
    import local_credentials


app = Flask(__name__)


# https://google.github.io/styleguide/pyguide.html

@app.route('/')
def home():
    # Cloud Deployment
    if os.environ.get('GAE_ENV') == 'standard':
        unix_socket = '/cloudsql/{}'.format(db_connection)
        conn = pymysql.connect(user=db_user, password=db_password,
                               unix_socket=unix_socket, db=db_database)
    # Local Deployment - Use TCP connections.
    else:
        conn = pymysql.connect(user=db_user, password=db_password,
                               host='127.0.0.1', db=db_database)

    with conn.cursor() as cur:
        cur.execute('SELECT * FROM PRODUCT')
        results = cur.fetchall()
    conn.close()

    return render_template('home.html', results=results)


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/register')
def register():
    return render_template('register.html')


@app.route('/submitted', methods=['POST'])
def register_complete():
    name = request.form['name']
    email = request.form['email']

    return render_template('register_complete.html',
                           name=name, email=email)


# Page Not Found
@app.errorhandler(404)
def error_404(e):
    return render_template('error.html', error=e)


# Internal Server Error
@app.errorhandler(500)
def error_500(e):
    return render_template('error.html', error=e)


# Local Deployment
if __name__ == '__main__':
    print('--------------------- Local Deployment')
    db = local_credentials.sql_variables()
    db_user = db['SQL_USERNAME']
    db_password = db['SQL_PASSWORD']
    db_database = db['SQL_DATABASE']
    db_connection = db['SQL_CONNECTION']

    app.run(host='127.0.0.1', port=8080, debug=True)

# Cloud Deployment
else:
    print('--------------------- Cloud Deployment')
    db_user = os.environ.get('SQL_USERNAME')
    db_password = os.environ.get('SQL_PASSWORD')
    db_database = os.environ.get('SQL_DATABASE')
    db_connection = os.environ.get('SQL_CONNECTION')




