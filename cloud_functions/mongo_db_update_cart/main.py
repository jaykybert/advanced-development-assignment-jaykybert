# Standard
import os
# Third-Party
from bson.json_util import dumps
from dotenv import load_dotenv
from pymongo import MongoClient


# https://europe-west2-ad-assignment-21.cloudfunctions.net/mongo_db_update_cart

def mongo_db_update_cart(request):
    load_dotenv()

    request_json = request.get_json(silent=True)

    if 'uid' in request_json and 'product' in request_json:
        uid = request_json['uid']
        product = request_json['product']

        mongo_user = os.environ.get('MONGO_DB_USERNAME')
        mongo_pass = os.environ.get('MONGO_DB_PASSWORD')

        client = MongoClient('mongodb+srv://{}:{}@advanced-development.25dxk.mongodb.net/ad-assignment?retryWrites=true&w=majority'.format(mongo_user, mongo_pass))

        db = client['ad-assignment']
        collection = db['cart']

        user_cart = collection.find_one({'uid': uid})
        user_cart['products'].append(product)

        collection.find_one_and_replace({'uid': uid}, user_cart)

        cursor = collection.find({'uid': uid})
        json_data = dumps(cursor)
        return json_data
    else:
        return {}
