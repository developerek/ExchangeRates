from dataclasses import dataclass
from typing import List, Dict


@dataclass
class ExchangeRate:
    currency: str
    rate: float


@dataclass
class ConversionData:
    query: Dict[str, str]
    result: float


@dataclass
class ExchangeRateData:
    base: str
    date: str
    rates: List[ExchangeRate]


@dataclass
class ConversionData:
    success: bool
    query: Dict[str, str]
    info: Dict[str, float]
    historical: str
    date: str
    result: float

# Data model for historical rate data
@dataclass
class HistoricalRateData:
    base: str
    date: str
    rates: List[ExchangeRate]


# Data model for historical rates data
@dataclass
class HistoricalRatesData:
    start_date: str
    end_date: str
    base: str
    rates: Dict[str, List[ExchangeRate]]


# Data model for time series data
@dataclass
class TimeSeriesData:
    start_date: str
    end_date: str
    base: str
    rates: Dict[str, List[ExchangeRate]]
