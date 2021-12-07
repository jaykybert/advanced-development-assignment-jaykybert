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

    # JSON passed.
    if request_json and 'source' in request_json:
        mesh_source = request_json['source']
    # Querystring passed.
    else:
        mesh_source = request.args.get('source')

    service_url = None
    # Services
    if mesh_source == 'mongo-db':
        service_url = os.environ.get('MONGO_DB_SERVICE_URL')

    elif mesh_source == 'cloud-sql':
        service_url = os.environ.get('CLOUD_SQL_SERVICE_URL')

    # Service Request
    if service_url is not None:
        json_data = requests.get(service_url)
        return json_data
    else:
        return json.dumps({'error': 'invalid service requested'})
