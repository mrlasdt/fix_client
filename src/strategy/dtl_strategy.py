# import logging
from decimal import Decimal
# from enum import Enum
from typing import List
from ..fix_client.dtl_fix_client import DTLFixClient
from ..fix_client.dto import OrderCandidate, OrderType, OrderSide
from .base_strategy import BaseStrategy
import random
import quickfix as fix
class DTLStrategy(BaseStrategy):
    def __init__(self, exchange: DTLFixClient, settings:dict):
        super().__init__(exchange)    
        self._order_refresh_time = settings["order_refresh_time"]
        self._order_amount = settings["order_amount"]
        self._symbols = settings["symbols"]
        self._order_refresh_time = settings["order_refresh_time"]
        self._create_timestamp = 0
        self.exchange = exchange
    
    def on_tick(self):
        # print('-'*100)
        # print(self.create_timestamp <= self.current_timestamp)
        # print(self.create_timestamp)
        # print(self.current_timestamp)
        if self.create_timestamp <= self.current_timestamp:
            # self.cancel_all_orders()
            proposal = self.create_proposal()
            self.place_order(proposal)
            self.create_timestamp = self._order_refresh_time + self.current_timestamp

    def create_proposal(self) -> OrderCandidate:
        price = fix.Price(100) #random #TODO
        symbol = random.choice(self._symbols)
        order_side = fix.Side(random.choice(OrderSide.get_values()))
        order_type = fix.OrdType(random.choice(OrderType.get_values()))
        amount = fix.OrderQty(100) #random #TODO
        order = OrderCandidate(order_type, order_side, amount, price, symbol)
        return order

    # def cancel_all_orders(self):
    #     for orders in self.get_active_orders(connector_name=self.exchange):
    #         lorders = [order for order in orders.values()] #TODO: handle dictionary change during iteration error
    #         for order in lorders:
    #             self.cancel(self.exchange, order.trading_pair, order.order_id)
