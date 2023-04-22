from enum import Enum
from dataclasses import dataclass
import quickfix as fix


class OrderType(Enum):
    MARKET = fix.OrdType(fix.OrdType_MARKET)
    LIMIT = fix.OrdType(fix.OrdType_LIMIT)
    @staticmethod
    def get_values():
        return [e.value for e in OrderType]
class OrderSide(Enum):
    BUY = fix.Side(fix.Side_BUY)
    SELL = fix.Side(fix.Side_SELL)
    # SHORT = fix.Side_SELL_SHORT
    @staticmethod
    def get_values():
        return [e.value for e in OrderSide]

class Symbol(Enum):
    MSFT = fix.Symbol("MSFT")
    AAPL = fix.Symbol("AAPL")
    BAC = fix.Symbol("BAC")
    @staticmethod
    def get_values():
        return [e.value for e in OrderSide]
    
@dataclass
class OrderCandidate:
    order_type: fix.OrdType
    order_side: fix.Side
    amount: fix.OrderQty
    price: fix.Price
    symbol: fix.Symbol
    order_id: int = -1
    