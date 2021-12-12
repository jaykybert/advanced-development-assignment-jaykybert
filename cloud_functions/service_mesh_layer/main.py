# Standard Libraries
import json
import os
# Third-Party Libraries
import requests
from dotenv import load_dotenv


def service_mesh_layer(request):
    """
    Using JSON from request select the appropriate cloud function to call,
    call it, and return the json returned from it.

    Endpoint: https://europe-west2-assignment-ad.cloudfunctions.net/service_mesh_layer

    :param request: A Request object
    :return: JSON data from the selected service
    """

    load_dotenv()

    request_json = request.get_json(silent=True)

    # Check the supplied source source, switch to the appropriate mesh service.
    mesh_source = request_json['source']

    # Service Selection
    if mesh_source == 'mongo-db-get-cart':
        service_url = os.environ.get('MONGO_DB_GET_CART_URL')

        json_data = requests.post(service_url, json={'uid': request_json['uid']},
                                  headers={'Content-type': 'application/json', 'Accept': 'text/plain'}).content
        return json_data

    elif mesh_source == 'mongo-db-update-cart':
        service_url = os.environ.get('MONGO_DB_UPDATE_CART_URL')

        json_data = requests.post(service_url, json={'uid': request_json['uid'], 'product': request_json['product']},
                                  headers={'Content-type': 'application/json', 'Accept': 'text/plain'}).content
        return json_data

    elif mesh_source == 'mongo-db-create-order':
        service_url = os.environ.get('MONGO_DB_CREATE_ORDER_URL')
        json_data = requests.post(service_url, json={'uid': request_json['uid'], 'address': request_json['address']},
                                  headers={'Content-type': 'application/json', 'Accept': 'text/plain'}).content
        return json_data

    elif mesh_source == 'mongo-db-delete-cart':
        service_url = os.environ.get('MONGO_DB_DELETE_CART_URL')
        json_data = requests.post(service_url, json={'uid': request_json['uid']},
                                  headers={'Content-type': 'application/json', 'Accept': 'text/plain'}).content
        return json_data

    elif mesh_source == 'mongo-db-get-orders':
        service_url = os.environ.get('MONGO_DB_GET_ORDERS_URL')
        json_data = requests.post(service_url, json={'uid': request_json['uid']},
                                  headers={'Content-type': 'application/json', 'Accept': 'text/plain'}).content
        return json_data

    elif mesh_source == 'cloud-sql-get-products':
        service_url = os.environ.get('CLOUD_SQL_GET_PRODUCTS_URL')
        json_data = requests.get(service_url).content
        return json_data

    else:
        return json.dumps({'error': 'invalid service requested'})
