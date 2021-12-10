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


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/products')
def products():
    req = requests.post(os.environ.get('SERVICE_MESH_URL'),
                        json={'source': 'cloud-sql'},
                        headers={'Content-type': 'application/json', 'Accept': 'text/plain'})
    products_json = req.json()

    if 'user' in session:

        req = requests.post(os.environ.get('SERVICE_MESH_URL'),
                            json={'source': 'mongo-db-get-cart', 'uid': session['user']['uid']},
                            headers={'Content-type': 'application/json', 'Accept': 'text/plain'})

    return render_template('products.html', products=products_json)


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/account', methods=['GET', 'POST'])
def account():
    # Account access via post - order just made.
    if request.form.get('address-line-1') is not None:

        address = {
            'address1': request.form.get('address-line-1'),
            'address2': request.form.get('address-line-2'),
            'postcode': request.form.get('postcode'),
            'country': request.form.get('country'),
            'mobile': request.form.get('mobile')
        }

        req = requests.post(os.environ.get('SERVICE_MESH_URL'),
                            json={'source': 'mongo-db-payment', 'uid': session['user']['uid'], 'address': address},
                            headers={'Content-type': 'application/json', 'Accept': 'text/plain'})

        results = req.json()
        print(results)
    else:
        print('No order made.')

    return render_template('account.html')


# Request Routes
@app.route('/cart', methods=['GET', 'POST'])
def cart():
    cart_json = {}
    if request.method == 'POST' and 'user' in session:
        cart_data = request.get_json()

        req = requests.post(os.environ.get('SERVICE_MESH_URL'),
                            json={'source': 'mongo-db-update-cart', 'uid': session['user']['uid'], 'product': cart_data},
                            headers={'Content-type': 'application/json', 'Accept': 'text/plain'})
        cart_json = req.content

    if request.method == 'GET' and 'user' in session:
        print('getting')
        req = requests.post(os.environ.get('SERVICE_MESH_URL'),
                            json={'source': 'mongo-db-get-cart', 'uid': session['user']['uid']},
                            headers={'Content-type': 'application/json', 'Accept': 'text/plain'})
        cart_json = req.content

    return cart_json


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


