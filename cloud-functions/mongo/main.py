from pymongo import MongoClient
from bson.json_util import dumps


def get_mongo_db_cart(request):
    client = MongoClient("mongodb+srv://advanced-development-admin:ada@advanced-development.25dxk.mongodb.net/ad-assignment?retryWrites=true&w=majority")

    db = client["ad-assignment"]
    collection = db["cart"]

    cur = list(collection.find({}))
    json_data = dumps(cur)

    return json_data
