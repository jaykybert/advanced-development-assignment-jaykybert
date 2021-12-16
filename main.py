# Standard Libraries
import os
# Third-Party Libraries
import requests
from dotenv import load_dotenv
from flask import Flask, render_template, request, jsonify, session


load_dotenv()
app = Flask(__name__)
app.secret_key = os.environ.get('APP_SECRET_KEY')


@app.route('/')
def home():
    """
    The default page for the website.
    :return: The homepage
    """

    return render_template('home.html')


@app.route('/products')
def products():
    """
    Contains a list of all of the products retrieved from
    the Cloud SQL database.

    :return: The products page
    """

    req = requests.post(os.environ.get('SERVICE_MESH_URL'), json={'source': 'cloud-sql-get-products'},
                        headers={'Content-type': 'application/json', 'Accept': 'text/plain'})
    products_json = req.json()

    if 'user' in session:
        requests.post(os.environ.get('SERVICE_MESH_URL'),
                      json={'source': 'mongo-db-get-cart', 'uid': session['user']['uid']},
                      headers={'Content-type': 'application/json', 'Accept': 'text/plain'})

    return render_template('products.html', products=products_json)


@app.route('/about')
def about():
    """
    Contains (dummy) information about the company
    and their website.

    :return: The about us page
    """

    return render_template('about.html')


@app.route('/account', methods=['GET', 'POST'])
def account():
    """
    Contains user account information and a
    list of the user's orders.

    :return: The account page
    """

    user_orders = []

    if 'user' in session:
        # Order just made. Update order collection.
        if request.form.get('address-line-1') is not None:

            address = {
                'address1': request.form.get('address-line-1'),
                'address2': request.form.get('address-line-2'),
                'postcode': request.form.get('postcode'),
                'country': request.form.get('country'),
                'mobile': request.form.get('mobile')
            }
            requests.post(os.environ.get('SERVICE_MESH_URL'),
                          json={'source': 'mongo-db-create-order', 'uid': session['user']['uid'], 'address': address},
                          headers={'Content-type': 'application/json', 'Accept': 'text/plain'})

        # Get all user orders.
        req = requests.post(os.environ.get('SERVICE_MESH_URL'),
                            json={'source': 'mongo-db-get-orders', 'uid': session['user']['uid']},
                            headers={'Content-type': 'application/json', 'Accept': 'text/plain'})

        user_orders = req.json()

    return render_template('account.html', user_orders=user_orders, user=session.get('user', None))


# ---------- Request Routes ---------- #
@app.route('/cart', methods=['GET', 'POST'])
def cart():
    """
    Called via front-end Ajax requests.
    Queries the cart collection and returns the results.

    :return: The user's cart data in JSON
    """

    cart_json = {}
    # Post Request - Delete and Update Cart
    if request.method == 'POST' and 'user' in session:
        cart_data = request.get_json()

        # Delete the user's cart.
        if 'delete' in cart_data:
            req = requests.post(os.environ.get('SERVICE_MESH_URL'),
                                json={'source': 'mongo-db-delete-cart', 'uid': session['user']['uid']},
                                headers={'Content-type': 'application/json', 'Accept': 'text/plain'})
            cart_json = req.content

        # Update the user's cart.
        else:
            req = requests.post(os.environ.get('SERVICE_MESH_URL'),
                                json={'source': 'mongo-db-update-cart', 'uid': session['user']['uid'], 'product': cart_data},
                                headers={'Content-type': 'application/json', 'Accept': 'text/plain'})
            cart_json = req.content

    # Get Request - Get Cart
    if request.method == 'GET' and 'user' in session:

        req = requests.post(os.environ.get('SERVICE_MESH_URL'),
                            json={'source': 'mongo-db-get-cart', 'uid': session['user']['uid']},
                            headers={'Content-type': 'application/json', 'Accept': 'text/plain'})
        cart_json = req.content

    return cart_json


@app.route('/login', methods=['POST'])
def login():
    """
    Called via a front-end Ajax request.
    Creates a session for the authenticated user.

    :return: Status code 200 (OK)
    """

    user = request.get_json()
    if 'uid' in user:
        session['user'] = user

    return jsonify({'code': 200})


@app.route('/logout', methods=['POST'])
def logout():
    """
    Called via a front-end Ajax request.
    Removes the authenticated user from the session.

    :return: Status code 200 (OK)
    """

    user = request.get_json()

    if 'logged-out' in user:
        session.pop('user', None)

    return jsonify({'code': 200})


# ---------- Error Handling ---------- #
@app.errorhandler(404)
def error_404(e):
    """
    Handles a 404 (File Not Found) error.

    :param e: The error raised
    :return: The error page
    """

    return render_template('error.html', error=e)


@app.errorhandler(500)
def error_500(e):
    """
    Handles a 500 (Internal Server Error) error.

    :param e: The error raised
    :return: The error page
    """

    return render_template('error.html', error=e)


# For Local Deployment
if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)
