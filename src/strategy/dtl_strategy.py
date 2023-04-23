
import random
import sys
import time 
from ..fix_client.dtl_fix_client import DTLFixClient
from ..common.dto import OrderCandidate, OrderType, OrderSide, Symbol
from .base_strategy import BaseStrategy



class DTLStrategy(BaseStrategy):
    def __init__(self, exchange: DTLFixClient, settings: dict):
        super().__init__(exchange)
        self.refresh_time = settings["refresh_time"]
        self._order_amount = settings["order_amount"]
        self.max_n_orders = settings["max_n_orders"]
        self.create_timestamp = 0
        self.exchange = exchange

    def on_tick(self):
        # print('-'*100)
        # print(self.create_timestamp <= self.current_timestamp)
        # print(self.create_timestamp)
        # print(self.current_timestamp)
        if self.create_timestamp <= self.current_timestamp and self.max_n_orders>0:
            # self.cancel_all_orders()
            proposal = self.create_proposal()
            self.place_order(proposal)
            random_order_id = self.get_random_order_id()
            if random_order_id:
                self.cancel(self.get_random_order_id())
            self.create_timestamp = self.refresh_time + self.current_timestamp
            self.max_n_orders -= 1
        if self.max_n_orders == 0:
            sys.exit(1)
    def create_proposal(self) -> OrderCandidate:
        price = 101  # random #TODO
        symbol = random.choice(Symbol.get_values())
        order_side = random.choice(OrderSide.get_values())
        order_type = random.choice(OrderType.get_values())
        amount = self._order_amount  # random #TODO
        order = OrderCandidate(order_type, order_side, amount, price, symbol)
        return order

    def get_random_order_id(self) -> str:
        lorders = self.exchange.order_tracker.tracked_orders
        return "" if len(lorders)==0 else random.choice(lorders)
