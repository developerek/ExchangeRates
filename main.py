import dataclasses
import json
import logging
import secrets

import redis
from flask import request, jsonify
from flask_swagger_ui import get_swaggerui_blueprint
from werkzeug.exceptions import BadRequest
from werkzeug.exceptions import HTTPException
from flask import Flask
from app.stub.stub import ExchangeRateAPI
from app.utils.utils import validate_request_data

app = Flask(__name__)

generic_token = secrets.token_urlsafe(16)
redis_client = redis.Redis(host='127.0.0.1', port=6379, db=0)

logging.basicConfig(filename='exchange_rate_api.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

exchange_rate_api = ExchangeRateAPI()


def requires_auth(f):
    def decorated(*args, **kwargs):
        auth_token = request.headers.get('Authorization')
        return f(*args, **kwargs)
        if auth_token != f"Bearer {generic_token}":
            return jsonify({"error": "Unauthorized access"}), 401

    decorated.__name__ = f.__name__
    return decorated


@app.route('/exchange-rate-list', methods=['GET'])
def exchange_rate_list():
    """
    This endpoint returns the exchange rate list.
    ---
    parameters:
      - name: source_currency
        in: query
        type: string
        required: true
        description: The source currency code.
      - name: target_currencies
        in: query
        type: array
        items:
          type: string
        required: true
        collectionFormat: multi
        description: List of target currency codes.
    responses:
      200:
        description: Exchange rate list successfully retrieved.
      400:
        description: Bad request.
    """
    try:

        source_currency = request.args.get('source_currency')
        target_currencies = request.args.get('target_currencies')

        if not source_currency or not target_currencies:
            raise BadRequest('Source currency and target currencies are required.')

        exchange_rates = exchange_rate_api.get_exchange_rate_list(source_currency, target_currencies)
        if exchange_rates is None:
            raise BadRequest('Invalid currency.')

        return jsonify({'exchange_rates': exchange_rates})

    except HTTPException as e:
        return jsonify({"error": e.description}), e.code


@app.route('/filter-transactions', methods=['GET'])
@requires_auth
def filter_transactions():
    """
    This endpoint filters transactions by transaction ID or conversion date range.
    ---
    parameters:
      - name: transaction_id
        in: query
        type: string
        required: false
        description: The transaction ID.
      - name: start_date
        in: query
        type: string
        required: false
        description: The start date of the conversion date range (ISO format).
      - name: end_date
        in: query
        type: string
        required: false
        description: The end date of the conversion date range (ISO format).
    responses:
      200:
        description: Transactions successfully filtered.
      400:
        description: Bad request.
    """
    transaction_id = request.args.get('transaction_id')
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    try:
        if transaction_id and (start_date or end_date):
            return jsonify({"error": "Please provide only one of the inputs: transaction_id or date range"}), 400

        transactiondata = exchange_rate_api.get_filter_conversions(transaction_id, start_date, end_date)

        return jsonify(transactiondata)
    except HTTPException as e:
        return jsonify({"error": e.description}), e.code


@app.route('/amount-list', methods=['GET'])
@requires_auth
def amount_list():
    """
    This endpoint returns the amount list in target currencies.
    ---
    parameters:
      - name: source_amount
        in: query
        type: number
        required: true
        description: The source amount for conversion.
      - name: source_currency
        in: query
        type: string
        required: true
        description: The source currency code.
      - name: target_currencies
        in: query
        type: array
        items:
          type: string
        required: true
        collectionFormat: multi
        description: List of target currency codes.
    responses:
      200:
        description: Amount list successfully retrieved.
      400:
        description: Bad request.
    """
    request_data = request.args
    try:
        validate_request_data(request_data, ['source_amount', 'source_currency', 'target_currencies'])
        source_amount = float(request_data.get('source_amount'))
        source_currency = request_data.get('source_currency')
        target_currencies = request_data.get('target_currencies')
        amount_list, transaction_id = exchange_rate_api.get_amount_list(source_amount, source_currency,
                                                                        target_currencies)
        return jsonify({"amount_list": amount_list, "transaction_id": transaction_id})
    except HTTPException as e:
        return jsonify({"error": e.description}), e.code


# Swagger UI
SWAGGER_URL = '/swagger'
API_URL = '/static/swagger.json'
swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "Exchange Rate API"
    }
)
app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)
if __name__ == '__main__':
    app.run(debug=True)
