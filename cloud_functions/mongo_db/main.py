# Standard
import os
# Third-Party
from bson.json_util import dumps
from dotenv import load_dotenv
from pymongo import MongoClient


def mongo_db_service(request):
    load_dotenv()

    request_json = request.get_json(silent=True)
    uid = request_json['uid']
    action = request_json['action']

    mongo_user = os.environ.get('MONGO_DB_USERNAME')
    mongo_pass = os.environ.get('MONGO_DB_PASSWORD')

    client = MongoClient('mongodb+srv://{}:{}@advanced-development.25dxk.mongodb.net/ad-assignment?retryWrites=true&w=majority'.format(mongo_user, mongo_pass))

    db = client['ad-assignment']
    collection = db['cart']

    # Retrieve the current user's cart.
    if action == 'GET':
        cursor = collection.find({'uid': uid})
        json_data = dumps(cursor)
        return json_data

    elif action == 'POST':
        product = request_json['product']

        collection.update_one({'uid': uid}, {'$set': {product['id']: product}})
        cursor = collection.find({'uid': uid})
        json_data = dumps(cursor)
        return json_data

    else:
        cursor = collection.find({'test': True})
        json_data = dumps(cursor)

        return json_data
