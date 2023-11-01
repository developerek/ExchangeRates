from fixerio_client import APIError
from fixerio_client import FixerIOClient
from app.utils.datamodel import ExchangeRateData, ConversionData, TimeSeriesData, HistoricalRatesData, \
    HistoricalRateData


class FixerIOAdapter:
    def __init__(self, api_key):
        self.fixer_client = FixerIOClient(api_key)

    def get_exchange_rate(self, date, base, symbols) -> HistoricalRateData:
        try:
            data = self.fixer_client.get_historical_rate(date, base, symbols)
            if data is not None:
                return data
            else:
                return None
        except APIError as exc:
            print(f"API error occurred with status code {exc.status_code}: {exc.message}")
            return None

    def convert_currency(self, from_currency, to_currency, amount) -> ConversionData:
        try:
            data = self.fixer_client.convert(from_currency, to_currency, amount)
            if data is not None:
                return ConversionData(query=data["query"], result=data["result"])
            else:
                return None
        except APIError as exc:
            print(f"API error occurred with status code {exc.status_code}: {exc.message}")
            return None

    def get_historical_exchange_rate(self, date, base, symbols) -> HistoricalRateData:
        try:
            data = self.fixer_client.get_historical_rate(date, base, symbols)
            if data is not None:
                return data
            else:
                return None
        except APIError as exc:
            print(f"API error occurred with status code {exc.status_code}: {exc.message}")
            return None

    def get_historical_exchange_rates(self, start_date, end_date, base, symbols) -> HistoricalRatesData:
        try:
            data = self.fixer_client.get_historical_rates(start_date, end_date, base, symbols)
            if data is not None:
                return data
            else:
                return None
        except APIError as exc:
            print(f"API error occurred with status code {exc.status_code}: {exc.message}")
            return None

    def get_time_series_data(self, start_date, end_date, symbols) ->TimeSeriesData:
        try:
            data = self.fixer_client.get_time_series(start_date, end_date, symbols)
            if data is not None:
                return data
            else:
                return None
        except APIError as exc:
            print(f"API error occurred with status code {exc.status_code}: {exc.message}")
            return None
