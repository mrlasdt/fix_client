from enum import Enum
from dataclasses import dataclass
import quickfix as fix
from datetime import datetime


class OrderType(Enum):
    # MARKET = fix.OrdType_MARKET
    LIMIT = fix.OrdType_LIMIT

    @staticmethod
    def get_values():
        return [e.value for e in OrderType]


class OrderSide(Enum):
    # BUY = fix.Side_BUY
    # SELL = fix.Side_SELL
    SHORT = fix.Side_SELL_SHORT

    @staticmethod
    def get_values():
        return [e.value for e in OrderSide]


class Symbol(Enum):
    # MSFT = "MSFT"
    # AAPL = "AAPL"
    BAC = "BAC"

    @staticmethod
    def get_values():
        return [e.value for e in Symbol]


@dataclass
class OrderCandidate:
    order_type: OrderType
    order_side: OrderSide
    amount: int
    price: int
    symbol: Symbol


class OrderStatus(Enum):
    ACTIVE = 1
    SHADOWED = 0


@dataclass
class OrderInFlight:
    created_at: datetime
    status: OrderStatus
