import os
import yaml
import requests
import json
import logging
from dotenv import load_dotenv

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def maybe_register_service(service_json, backend_services_url, bearer, re_register):
    headers = {"Authorization": "Bearer " + bearer}
    response = requests.get(backend_services_url + '/services', headers=headers)

    service_available = False
    for service in json.loads(response.text):
        if service['name'] == service_json['name']:
            service_available = True
    if service_available:
        if not re_register:
            logger.info("Service is available - do nothing")
        else:
            logger.info("Service is available - unlink")
            response = requests.post(backend_services_url + '/unlink_service',
                                     json=service_json, headers=headers)
            service_available = False
    if not service_available:
        logger.info("Service is unavailable - registering")
        response = requests.post(backend_services_url + '/register_service',
                                 json=service_json, headers=headers)


def register_services(service_descriptions, backend_services_url, bearer="", re_register=False):
    for name, service_description in service_descriptions.items():
        maybe_register_service(service_description, backend_services_url, bearer, re_register)


if __name__ == '__main__':
    backend_url = "http://127.0.0.1:8012"

    # Only needed if api authentication is enabled

    # load_dotenv()
    # api_uname = os.getenv("API_UNAME")
    # api_password = os.getenv("API_PW")
    #
    # auth_prefix = "/api/v1/tp_auth"
    # backend_auth_url = backend_url + auth_prefix
    #
    # data = {
    #     'username': api_uname,
    #     'password': api_password,
    # }
    # answ = requests.post(url=backend_auth_url+"/token" ,data=data)
    # bearer =  json.loads(answ.text)['access_token']


    services_prefix = "/api/v1/tp_services"
    backend_services_url = backend_url + services_prefix

    with open('minimal-services.yml', 'r') as file:
        service_descriptions = yaml.safe_load(file)

    register_services(service_descriptions, backend_services_url)