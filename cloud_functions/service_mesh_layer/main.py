# Standard
import json
import os
# Third-Party
import requests
from dotenv import load_dotenv


# https://europe-west2-ad-assignment-21.cloudfunctions.net/service_mesh_layer


def service_mesh_layer(request):

    load_dotenv()

    request_json = request.get_json(silent=True)

    # Check data source, switch to the appropriate mesh service.

    mesh_source = request_json['source']

    # Services
    if mesh_source == 'mongo-db-get-cart':
        service_url = os.environ.get('MONGO_DB_GET_CART_URL')

        json_data = requests.post(service_url,
                        json={'uid': request_json['uid']},
                        headers={'Content-type': 'application/json', 'Accept': 'text/plain'}).content
        return json_data

    elif mesh_source == 'mongo-db-update-cart':
        service_url = os.environ.get('MONGO_DB_UPDATE_CART_URL')

        json_data = requests.post(service_url,
                        json={'uid': request_json['uid'], 'product': request_json['product']},
                        headers={'Content-type': 'application/json', 'Accept': 'text/plain'}).content
        return json_data

    elif mesh_source == 'mongo-db-payment':
        service_url = os.environ.get('MONGO_DB_PAYMENT_URL')
        json_data = requests.post(service_url,
                json={'uid': request_json['uid']},
                headers={'Content-type': 'application/json', 'Accept': 'text/plain'}).content
        return json_data

    elif mesh_source == 'cloud-sql':
        service_url = os.environ.get('CLOUD_SQL_SERVICE_URL')
        json_data = requests.get(service_url).content
        return json_data
    else:
        return json.dumps({'error': 'invalid service requested'})
