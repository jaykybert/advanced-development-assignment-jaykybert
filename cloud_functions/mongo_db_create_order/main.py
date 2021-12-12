# Standard Libraries
import datetime
import os
# Third-Party Libraries
from bson.json_util import dumps
from dotenv import load_dotenv
from pymongo import MongoClient


def mongo_db_create_order(request):
    """
    Using the request JSON, delete the user's cart, add order date and status,
    and save the updated cart object into the orders collection.

    Endpoint: https://europe-west2-assignment-ad.cloudfunctions.net/mongo_db_create_order

    :param request: A Request object
    :return: The newly-created order JSON object
    """

    load_dotenv()

    request_json = request.get_json(silent=True)

    if 'uid' in request_json and 'address' in request_json:
        uid = request_json['uid']
        address = request_json['address']

        mongo_user = os.environ.get('MONGO_DB_USERNAME')
        mongo_pass = os.environ.get('MONGO_DB_PASSWORD')

        client = MongoClient('mongodb+srv://{}:{}@advanced-development.25dxk.mongodb.net/'
                             'ad-assignment?retryWrites=true&w=majority'.format(mongo_user, mongo_pass))

        db = client['ad-assignment']

        # Update cart object with order status and date.
        cart_collection = db['cart']
        order_date = datetime.datetime.now()

        order_date_f = order_date.strftime('%d %b %Y at %H:%M')

        cart_collection.update_one({'uid': uid}, {'$set': {'order': {'status': 'Processed', 'date': order_date_f}}})
        cart_json = cart_collection.find_one({'uid': uid})

        # Delete from the cart collection.
        cart_collection.delete_one({'uid': uid})

        # Add the cart object with an order id to the orders collection.
        order_collection = db['orders']

        o_id = datetime.datetime.now()
        new_order_id = int(o_id.timestamp())

        cart_json['order-id'] = new_order_id
        cart_json['address'] = address

        total_price = 0
        for product in cart_json['products']:
            total_price += product['total-price']

        cart_json['total-price'] = total_price

        order_collection.insert_one(cart_json)
        order_json = order_collection.find({'uid': uid})

        return dumps(order_json)

    else:
        return {}
