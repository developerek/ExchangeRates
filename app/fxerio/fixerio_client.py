import httpx

from app.utils.datamodel import (HistoricalRatesData,
                                 HistoricalRateData,
                                 TimeSeriesData,
                                 ExchangeRate,
                                 ExchangeRateData,
                                 ConversionData)


class FixerIOClient:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "http://data.fixer.io/api/"

    def get_exchange_rate(self, base, symbols) -> ExchangeRateData:
        with httpx.AsyncClient() as client:
            url = f"{self.base_url}latest?access_key={self.api_key}&base={base}&symbols={symbols}"
            try:
                response = client.get(url)
                if response.status_code == 200:
                    data = response.json()
                    rates = [ExchangeRate(currency=currency, rate=rate) for currency, rate in data["rates"].items()]
                    return ExchangeRateData(base=data["base"], date=data["date"], rates=rates)
                else:
                    message = f"Request failed with status code {response.status_code}"
                    raise APIError(response.status_code, message)
            except httpx.HTTPStatusError as exc:
                message = f"HTTP error occurred: {exc}"
                raise APIError(500, message) from exc

    def convert(self, from_currency, to_currency, amount) -> ConversionData:
        with httpx.Client() as client:
            url = f"{self.base_url}convert?access_key={self.api_key}&from={from_currency}&to={to_currency}&amount={amount}"
            try:
                response = client.get(url)
                if response.status_code == 200:
                    data = response.json()
                    return ConversionData(query=data["query"], result=data["result"])
                else:
                    message = f"Request failed with status code {response.status_code}"
                    raise APIError(response.status_code, message)
            except httpx.HTTPStatusError as exc:
                message = f"HTTP error occurred: {exc}"
                raise APIError(500, message) from exc

    def get_historical_rate(self, date, base, symbols) -> HistoricalRateData:
        with httpx.Client() as client:
            url = f"{self.base_url}{date}?access_key={self.api_key}&base={base}&symbols={symbols}"
            try:
                response = client.get(url)
                if response.status_code == 200:
                    data = response.json()
                    rates = [ExchangeRate(currency=currency, rate=rate) for currency, rate in data["rates"].items()]
                    return HistoricalRateData(base=data["base"], date=data["date"], rates=rates)
                else:
                    message = f"Request failed with status code {response.status_code}"
                    raise APIError(response.status_code, message)
            except httpx.HTTPStatusError as exc:
                message = f"HTTP error occurred: {exc}"
                raise APIError(500, message) from exc

    def get_historical_rates(self, start_date, end_date, base, symbols) -> HistoricalRatesData:
        with httpx.Client() as client:
            url = f"{self.base_url}timeseries?access_key={self.api_key}&start_date={start_date}&end_date={end_date}" \
                  f"&base={base}&symbols={symbols}"
            try:
                response = client.get(url)
                if response.status_code == 200:
                    data = response.json()

                    rates = {date: [ExchangeRate(currency=currency, rate=rate) for currency, rate in rates.items()] for
                             date, rates in data["rates"].items()}
                    return HistoricalRatesData(start_date=data["start_date"], end_date=data["end_date"],
                                               base=data["base"], rates=rates)
                else:
                    message = f"Request failed with status code {response.status_code}"
                    raise APIError(response.status_code, message)
            except httpx.HTTPStatusError as exc:
                message = f"HTTP error occurred: {exc}"
                raise APIError(500, message) from exc

    def get_time_series(self, start_date, end_date, symbols):
        with httpx.Client() as client:
            url = f"{self.base_url}timeseries?access_key={self.api_key}&start_date={start_date}&end_date={end_date}" \
                  f"&symbols={symbols}"
            try:
                response = client.get(url)
                if response.status_code == 200:
                    data = response.json()
                    return data
                    rates = {date: [ExchangeRate(currency=currency, rate=rate) for currency, rate in rates.items()] for
                             date, rates in data["rates"].items()}
                    return TimeSeriesData(
                        start_date=data["start_date"],
                        end_date=data["end_date"],
                        base=data["base"],
                        rates=rates
                    )
                else:
                    message = f"Request failed with status code {response.status_code}"
                    raise APIError(response.status_code, message)
            except httpx.HTTPStatusError as exc:
                message = f"HTTP error occurred: {exc}"
                raise APIError(500, message) from exc


class APIError(Exception):
    def __init__(self, status_code, message):
        self.status_code = status_code
        self.message = message
