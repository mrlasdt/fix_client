from enum import Enum
from dataclasses import dataclass
import quickfix as fix


class OrderType(Enum):
    MARKET = fix.OrdType_MARKET
    LIMIT = fix.OrdType_LIMIT
    @staticmethod
    def get_values():
        return [e for e in OrderType]
class OrderSide(Enum):
    BUY = fix.Side_BUY
    SELL = fix.Side_SELL
    SHORT = fix.Side_SELL_SHORT
    @staticmethod
    def get_values():
        return [e for e in OrderSide]

@dataclass
class OrderCandidate:
    order_type: fix.OrdType
    order_side: fix.Side
    amount: fix.OrderQty
    price: fix.Price
    symbol: str
    order_id: int = -1
    