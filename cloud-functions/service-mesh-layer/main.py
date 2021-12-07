import requests
import json


def service_mesh_layer(request):
    request_json = request.get_json(silent=True)

    # Check data source, switch to the appropriate mesh service.

    # JSON passed.
    if request_json and "source" in request_json:
        mesh_source = request_json['source']
    # Querystring passed.
    else:
        mesh_source = request.args.get("source")

    if mesh_source == "mongo":
        url = "https://europe-west2-ad-assignment-21.cloudfunctions.net/mongo_db_cart"

        json_data = requests.get(url).content
        return json_data

    else:
        return json.dumps({"test": "mesh wasn't mongo"})
