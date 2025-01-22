import os
import requests
import time
from flask import Blueprint, request, jsonify
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
        return jsonify({"error": "Failed to fetch banks", "details": response.text}), response.status_code

@banks_bp.route('/transactions', methods=['POST'])
@jwt_required()
def create_link_and_get_transactions():
    url_links = os.getenv("BELVO_URL") + "/api/links/"
    data = request.json
    payload = {
        "institution": data["institution"],
        "username": "username",
        "password": "password"
    }

    response_link = requests.post(url_links, json=payload, auth=(SECRET_ID, SECRET_PASSWORD))

    if response_link.status_code == 201:
        link_id = response_link.json()["id"]

        # Intentar obtener transacciones con reintentos
        max_retries = 5
        for _ in range(max_retries):
            url_transactions = os.getenv("BELVO_URL") + f"/api/transactions/?link={link_id}"
            response_transactions = requests.get(url_transactions, auth=(SECRET_ID, SECRET_PASSWORD))
            
            if response_transactions.status_code == 200 and response_transactions.json()['results']:
                transactions = response_transactions.json()
                
                # Calcula el KPI (Balance = Ingresos - Egresos)
                ingresos = sum(txn['amount'] for txn in transactions['results'] if txn['type'] == 'INFLOW')
                egresos = sum(txn['amount'] for txn in transactions['results'] if txn['type'] == 'OUTFLOW')
                balance = ingresos - egresos
                
                # Prepara la respuesta
                result = {
                    "KPI": {
                        "Balance": round(balance, 2),
                        "Ingresos": round(ingresos, 2),
                        "Egresos": round(egresos, 2)
                    },
                    "Movimientos": transactions['results']
                }
                
                return jsonify(result), 200
            else:
                time.sleep(1)  # Esperar 1 segundo antes de reintentar
        print(f"response_transactions.json() {response_transactions.json()}", flush=True)
        return jsonify(response_transactions.json()), 200
    else:
        return jsonify({"error": "Failed to create link", "details": response_link.text}), response_link.status_code
