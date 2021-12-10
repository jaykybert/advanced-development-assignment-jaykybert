# Local
import os
# Third-Party
from flask import Flask, redirect, render_template, url_for, request, jsonify, session
import requests
# Application
from dotenv import load_dotenv

# ------------------------------------------------------------------

# TODO: Customise authentication login - store address data in firestore.
#           -> Also include user type in firestore
#           -> See https://medium.com/@bariskarapinar/firebase-authentication-web-app-javascript-3165ebc92b68

# TODO: save product images somewhere (?)

# TODO: Add product tracking (mongo?)

# TODO: On payment, get json object from mongo, move to another collection
#           -> then delete the one from cart.

# https://google.github.io/styleguide/pyguide.html

# ------------------------------------------------------------------

# Load environment variables from .env, start Flask app.
load_dotenv()

app = Flask(__name__)
app.secret_key = os.environ.get('APP_SECRET_KEY')

# Standard
import datetime
import os
import json
# Third-Party
from bson.json_util import dumps
from bson import BSON
from dotenv import load_dotenv
from pymongo import MongoClient


# https://europe-west2-ad-assignment-21.cloudfunctions.net/mongo_db_payment


def mongo_db_payment(user_id):
    load_dotenv()

    request_json = request.get_json(silent=True)

    uid = user_id

    mongo_user = os.environ.get('MONGO_DB_USERNAME')
    mongo_pass = os.environ.get('MONGO_DB_PASSWORD')

    client = MongoClient('mongodb+srv://{}:{}@advanced-development.25dxk.mongodb.net/ad-assignment?retryWrites=true&w=majority'.format(mongo_user, mongo_pass))

    db = client['ad-assignment']
    cart_collection = db['cart']

    order_date = str(datetime.datetime.now())

    # Update cart document
    cart_collection.update_one({'uid': uid}, {'$set': {'order': {'status': 'Processed', 'date': order_date}}})
    cursor = cart_collection.find_one({'uid': uid})
    print(cursor)
    print(type(cursor))
    cursor_json = dumps(cursor)
    print(cursor_json)

    # Open orders, work out order id.
    order_collection = db['orders']
    order_count = order_collection.count_documents({})

    new_order_id = 'o-' + str(order_count + 1)

    cart_collection.insert_one({'oid': new_order_id})





    return dumps(cursor)

    # Todo delete basket.


@app.route('/')
def home():

    cart_json = None

    cart_json = mongo_db_payment("YMU9OpJC1YcXX2Ix1nUF6WQAKTA2")


    """
    if 'user' in session:

        req = requests.post(os.environ.get('SERVICE_MESH_URL'),
                            json={'source': 'mongo-db-get-cart', 'uid': session['user']['uid']},
                            headers={'Content-type': 'application/json', 'Accept': 'text/plain'})
        cart_json = req.content
        print(cart_json)
    """

    return render_template('home.html', mongoTest=cart_json)


@app.route('/products')
def products():
    req = requests.post(os.environ.get('SERVICE_MESH_URL'),
                        json={'source': 'cloud-sql'},
                        headers={'Content-type': 'application/json', 'Accept': 'text/plain'})
    products_json = req.json()

    return render_template('products.html', products=products_json)


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/account', methods=['GET', 'POST'])
def account():
    # Account access via post - order just made.
    if request.form.get('address1') is not None:
        print('Order made.')

    else:
        print('No order made.')

    return render_template('account.html')


# Request Routes
@app.route('/cart', methods=['GET', 'POST'])
def cart():
    cart_json = {}
    if request.method == 'POST' and 'user' in session:
        cart_data = request.get_json()

        print(cart_data)

        req = requests.post(os.environ.get('SERVICE_MESH_URL'),
                            json={'source': 'mongo-db-update-cart', 'uid': session['user']['uid'], 'product': cart_data},
                            headers={'Content-type': 'application/json', 'Accept': 'text/plain'})
        cart_json = req.content
        print(cart_json)

    return cart_json


@app.route('/payment', methods=['GET'])
def payment():

    req = requests.post(os.environ.get('SERVICE_MESH_URL'),
                        json={'source': 'mongo-db-payment', 'uid': session['user']['uid']},
                        headers={'Content-type': 'application/json', 'Accept': 'text/plain'})

    results = req.content
    print(results)

    return redirect(url_for('account'))


@app.route('/login', methods=['POST'])
def login():
    user = request.get_json()
    if 'uid' in user:

        session['user'] = user
    print('Logging in...')

    return jsonify({'status': 200})


@app.route('/logout', methods=['POST'])
def logout():
    user = request.get_json()

    if 'logged-out' in user:
        session.pop('user', None)

    return jsonify({'status': 200})


# Page Not Found
@app.errorhandler(404)
def error_404(e):
    return render_template('error.html', error=e)


# Internal Server Error
@app.errorhandler(500)
def error_500(e):
    return render_template('error.html', error=e)


if __name__ == '__main__':
    print('--------------------- Local Deployment')
    app.run(host='127.0.0.1', port=8080, debug=True)

else:
    print('--------------------- Cloud Deployment')


