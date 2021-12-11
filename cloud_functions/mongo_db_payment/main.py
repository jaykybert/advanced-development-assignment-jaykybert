# Standard
import datetime
import os
# Third-Party
from bson.json_util import dumps
from dotenv import load_dotenv
from pymongo import MongoClient


# https://europe-west2-ad-assignment-21.cloudfunctions.net/mongo_db_payment


def mongo_db_payment(request):
    load_dotenv()

    request_json = request.get_json(silent=True)

    if 'uid' in request_json and 'address' in request_json:
        uid = request_json['uid']
        address = request_json['address']

        mongo_user = os.environ.get('MONGO_DB_USERNAME')
        mongo_pass = os.environ.get('MONGO_DB_PASSWORD')

        client = MongoClient('mongodb+srv://{}:{}@advanced-development.25dxk.mongodb.net/ad-assignment?retryWrites=true&w=majority'.format(mongo_user, mongo_pass))

        db = client['ad-assignment']

        # Update cart document
        cart_collection = db['cart']
        order_date = datetime.datetime.now()

        order_date_formatted = order_date.strftime('%d %b %Y at %H:%M')

        cart_collection.update_one({'uid': uid}, {'$set': {'order': {'status': 'Processed', 'date': order_date_formatted}}})
        cart_json = cart_collection.find_one({'uid': uid})

        # Delete cart
        cart_collection.delete_one({'uid': uid})

        # Open orders, work out order id.
        order_collection = db['orders']
        order_count = order_collection.count_documents({})

        new_order_id = 'o-' + str(order_count + 1)

        cart_json['order-id'] = new_order_id
        cart_json['address'] = address

        total_price = 0
        for product in cart_json['products']:
            total_price += product['total-price']

        cart_json['total-price'] = total_price

        # Insert the cart json + an order-id into the order collection.
        order_collection.insert_one(cart_json)

        order_json = order_collection.find({'uid': uid})

        return dumps(order_json)
    else:
        return {}

