# Third-Party
from flask import Flask, render_template
from pymongo import MongoClient
import pymysql
# Application
from decouple import config
# Local
import database_wrapper

app = Flask(__name__)

# TODO: Customise authentication login - store address data in firestore.
#           -> Also include user type in firestore
#           -> See https://medium.com/@bariskarapinar/firebase-authentication-web-app-javascript-3165ebc92b68

# TODO: service mesh layer
#           -> create mesh, move database stuff to cloud functions.
#           -> mongo db, cloudsql

# TODO: save product images somewhere (?)

# TODO: Add product tracking (mongo?)


@app.route('/')
def home():
    items = []
    results = collection.find({"product": "test-product"})
    for result in results:
        items.append(result)

    return render_template('home.html', mongoTest=items)


@app.route('/products')
def products():

    results = db_wrapper.query('SELECT * FROM PRODUCT;')
    print(results)
    return render_template('products.html', products=results)


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/account')
def account():
    return render_template('account.html')


# Page Not Found
@app.errorhandler(404)
def error_404(e):
    return render_template('error.html', error=e)


# Internal Server Error
@app.errorhandler(500)
def error_500(e):
    return render_template('error.html', error=e)


sql_user = config('CLOUD_SQL_USERNAME')
sql_pass = config('CLOUD_SQL_PASSWORD')
sql_conn = config('CLOUD_SQL_CONNECTION')
sql_name = config('CLOUD_SQL_DATABASE')

mongo_user = config('MONGO_USERNAME')
mongo_pass = config('MONGO_PASSWORD')

# https://google.github.io/styleguide/pyguide.html

mongoCluster = MongoClient("mongodb+srv://advanced-development-admin:ada@advanced-development.25dxk.mongodb.net/ad-assignment?retryWrites=true&w=majority")
db = mongoCluster["ad-assignment"]
collection = db["cart"]

if __name__ == '__main__':
    print('--------------------- Local Deployment')
    db_wrapper = database_wrapper.DatabaseWrapper(sql_user, sql_pass, sql_conn, sql_name, True)
    try:
        db_wrapper.connect()
    except pymysql.OperationalError as exc:
        print('Could not connect to Cloud SQL.')
        print(exc)

    app.run(host='127.0.0.1', port=8080, debug=True)

else:
    print('--------------------- Cloud Deployment')
    db_wrapper = database_wrapper.DatabaseWrapper(sql_user, sql_pass, sql_conn, sql_name, False)
    db_wrapper.connect()

