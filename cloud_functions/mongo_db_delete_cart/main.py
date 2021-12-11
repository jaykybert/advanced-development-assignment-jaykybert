# Standard
import os
# Third-Party
from dotenv import load_dotenv
from pymongo import MongoClient


# https://europe-west2-ad-assignment-21.cloudfunctions.net/mongo_db_delete_cart

def mongo_db_get_cart(request):
    load_dotenv()

    request_json = request.get_json(silent=True)

    if 'uid' in request_json:
        uid = request_json['uid']
        mongo_user = os.environ.get('MONGO_DB_USERNAME')
        mongo_pass = os.environ.get('MONGO_DB_PASSWORD')

        client = MongoClient('mongodb+srv://{}:{}@advanced-development.25dxk.mongodb.net/ad-assignment?retryWrites=true&w=majority'.format(mongo_user, mongo_pass))

        db = client['ad-assignment']
        collection = db['cart']
        collection.delete_one({'uid': uid})

    return {}
