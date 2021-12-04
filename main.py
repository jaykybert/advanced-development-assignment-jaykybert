# Third-Party
from flask import Flask, render_template
from pymongo import MongoClient
# Application
from decouple import config
# Local
import database_wrapper

app = Flask(__name__)

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


db_user = config('SQL_USERNAME')
db_password = config('SQL_PASSWORD')
db_connection = config('SQL_CONNECTION')
db_database = config('SQL_DATABASE')

# https://google.github.io/styleguide/pyguide.html

mongoCluster = MongoClient("mongodb+srv://advanced-development-admin:ada@advanced-development.25dxk.mongodb.net/ad-assignment?retryWrites=true&w=majority")
db = mongoCluster["ad-assignment"]
collection = db["cart"]


# Local Deployment - SQL variables saved in .env.
if __name__ == '__main__':
    print('--------------------- Local Deployment')
    db_wrapper = database_wrapper.DatabaseWrapper(db_user, db_password, db_connection, db_database, True)
    db_wrapper.connect()

    app.run(host='127.0.0.1', port=8080, debug=True)

# Cloud Deployment - SQL variables saved in app.yaml.
else:
    print('--------------------- Cloud Deployment')
    db_wrapper = database_wrapper.DatabaseWrapper(db_user, db_password, db_connection, db_database, False)
    db_wrapper.connect()

