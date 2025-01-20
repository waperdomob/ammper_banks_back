import os
import requests
from flask import Blueprint
from flask_jwt_extended import jwt_required

banks_bp = Blueprint('banks', __name__)

SECRET_ID = os.getenv("BELVO_SECRET_ID")
SECRET_PASSWORD = os.getenv("BELVO_SECRET_PASSWORD")

@banks_bp.route('/', methods=['GET'])
@jwt_required()
def get_banks():
    url = os.getenv("BELVO_URL") + "/api/institutions/"
    response = requests.get(url, auth=(SECRET_ID, SECRET_PASSWORD))
    if response.status_code == 200:
        return response.json(), 200
    else:
        return {"error": "Failed to fetch banks", "details": response.text}, response.status_code

@banks_bp.route('/links', methods=['POST'])
@jwt_required()
def create_link():
    url = os.getenv("BELVO_URL") + "/api/links/"

    payload = {
        "institution": "planet_mx_employment",
        "username": "BLPM951331IONVGR54",
        "external_id": "getting_started_link",
        "access_mode": "single",
        "fetch_resources": ["OWNERS", "EMPLOYMENT_RECORDS"]
    }

    response = requests.post(url, json=payload, auth=(SECRET_ID, SECRET_PASSWORD))

    if response.status_code == 201:
        return response.json(), 201
    else:
        return {"error": "Failed to create link", "details": response.text}, response.status_code


@banks_bp.route('/transactions/<link_id>', methods=['POST'])
@jwt_required()
def get_transactions(link_id):
    url = os.getenv("BELVO_URL") + f"/api/transactions/?link={link_id}"
    response = requests.get(url, auth=(SECRET_ID, SECRET_PASSWORD))
    if response.status_code == 200:
        return response.json(), 200
    else:
        return {"error": "Failed to fetch transactions", "details": response.text}, response.status_code
