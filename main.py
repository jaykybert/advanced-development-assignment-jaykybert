# Local
import os
# Third-Party
from flask import Flask, render_template
import requests
# Application
from dotenv import load_dotenv

# ------------------------------------------------------------------

# TODO: Customise authentication login - store address data in firestore.
#           -> Also include user type in firestore
#           -> See https://medium.com/@bariskarapinar/firebase-authentication-web-app-javascript-3165ebc92b68

# TODO: service mesh layer
#           -> create mesh, move database stuff to cloud functions.
#           -> mongo db, cloudsql

# TODO: save product images somewhere (?)

# TODO: Add product tracking (mongo?)

# https://google.github.io/styleguide/pyguide.html

#   ./cloud_sql_proxy -instances=ad-assignment-21:europe-west2:advanced-development=tcp:127.0.0.1:1433

# ------------------------------------------------------------------


app = Flask(__name__)


@app.route('/')
def home():

    req = requests.post(os.environ.get('SERVICE_MESH_URL'),
                        json={'source': 'mongo-db'},
                        headers={'Content-type': 'application/json', 'Accept': 'text/plain'})
    cart_json = req.json()

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


load_dotenv()


mongo_user = os.environ.get('MONGO_DB_USERNAME')
mongo_pass = os.environ.get('MONGO_DB_PASSWORD')


if __name__ == '__main__':
    print('--------------------- Local Deployment')
    app.run(host='127.0.0.1', port=8080, debug=True)

else:
    print('--------------------- Cloud Deployment')


