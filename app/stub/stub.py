import datetime
import json
from secrets import token_urlsafe
import redis
from flask import jsonify
from werkzeug.exceptions import HTTPException

from app.fxerio.fixerio_adapter import FixerIOAdapter
from app.utils.datamodel import HistoricalRateData


class ExchangeRateAPI:
    def __init__(self):
        self.c = FixerIOAdapter('041ee95e5f1f50d4acf51a726a5659ef')

        self.redis = redis.Redis(host='127.0.0.1', port=6379, db=0)
        self.today = datetime.date.today()

    def get_exchange_rate_list(self, source_currency, target_currencies) -> HistoricalRateData:

        exchange_rate_list = []
        try:

            exchange_rate = self.c.get_exchange_rate(self.today, source_currency, target_currencies)

            return exchange_rate
        except Exception as e:
            print(f"Error: {e}")
            return []

    def get_supported_currencies(self):
        return list(self.rates.keys())

    def get_filter_conversions(self, transaction_id=None, start_date=None, end_date=None) :
        if transaction_id:
            transaction_data = self.redis.get(transaction_id)
            if transaction_data:
                transaction_data = json.loads(transaction_data)
                return [transaction_data]
            else:
                return jsonify({"error": "Transaction not found"}), 404

        if start_date and end_date:
            transactions = []
            keys = self.redis.keys()
            for key in keys:
                transaction_data = json.loads(self.redis.get(key))
                transaction_date = datetime.datetime.fromisoformat(transaction_data["date"])
                if start_date <= transaction_date <= end_date:
                    transactions.append(transaction_data)
            return transactions

    def get_amount_list(self, source_amount, source_currency, target_currencies):

        amount_list = []
        transaction_id = token_urlsafe(8)
        try:
            import time
            today = time.strftime("%Y-%m-%d")
            current_date = today
            exchange_rate = self.c.get_exchange_rate(current_date, source_currency, target_currencies)

            for currency in exchange_rate.rates:
                # u'rates': {u'GBP': 0.76245, u'USD': 1.1168}}
                amount = currency.rate * source_amount
                amount_list.append({currency.currency: amount})

            # Store transaction data in Redis
            transaction_data = {
                "transaction_id": transaction_id,
                "date": current_date,
                "amount_list": amount_list
            }
            self.redis.set(transaction_id, json.dumps(transaction_data))

            return amount_list, transaction_id

        except Exception as e:
            error_message = f"Exchange rates not available for {source_currency} to {', '.join(target_currencies)}"
            raise HTTPException(description=error_message, response=None, code=500)
