# Standard Libraries
import os
# Third-Party Libraries
from bson.json_util import dumps
from dotenv import load_dotenv
from pymongo import MongoClient


def mongo_db_get_orders(request):
    """
    Using the request JSON, get all of a user's orders from the
    orders collection.

    Endpoint: https://europe-west2-assignment-ad.cloudfunctions.net/mongo_db_get_orders

    :param request: A Request object
    :return: All of a user's orders in JSON
    """

    load_dotenv()

    request_json = request.get_json(silent=True)

    if 'uid' in request_json:
        uid = request_json['uid']

        mongo_user = os.environ.get('MONGO_DB_USERNAME')
        mongo_pass = os.environ.get('MONGO_DB_PASSWORD')

        client = MongoClient('mongodb+srv://{}:{}@advanced-development.25dxk.mongodb.net/'
                             'ad-assignment?retryWrites=true&w=majority'.format(mongo_user, mongo_pass))

        db = client['ad-assignment']
        collection = db['orders']
        user_orders = collection.find({'uid': uid})

        json_data = dumps(user_orders)
        return json_data

    else:
        return {}
