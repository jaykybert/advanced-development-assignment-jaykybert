# Standard Libraries
import os
# Third-Party Libraries
from dotenv import load_dotenv
from pymongo import MongoClient


def mongo_db_delete_cart(request):
    """
    Using the request JSON, delete the user's cart.

    Endpoint: https://europe-west2-assignment-ad.cloudfunctions.net/mongo_db_delete_cart

    :param request: A request object
    :return: An empty object
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
        collection = db['cart']
        collection.delete_one({'uid': uid})

        cart_structure = {'uid': uid, 'products': []}
        collection.insert_one(cart_structure)

    return {}
