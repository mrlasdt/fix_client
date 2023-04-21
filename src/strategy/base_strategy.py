import sys
import importlib
import inspect
from decimal import Decimal
from typing import List
from src.fix_client.dto import OrderType, OrderSide, LimitOrder
from src.fix_client.order_tracker import OrderTracker
from src.fix_client.dtl_fix_client import DTLFixClient
s_decimal_nan = Decimal("NaN")

class BaseStrategy:
    def __init__(self, exchange:DTLFixClient):
        """
        Initialising a new script strategy object.

        :param strategy_dir: Path to the strategy directory
        """
        # self.order_tracker = OrderTracker()
        self.ready_to_trade = False        
        self.exchange = exchange
        
    def tick(self, timestamp: float):
        """
        Clock tick entry point, is run every second (on normal tick setting).
        Checks if all connectors are ready, if so the strategy is ready to trade.

        :param timestamp: current tick timestamp
        """
        if not self.ready_to_trade:
            print("[WARNING]:","Waiting to logon...")
            self.ready_to_trade = self.exchange.ready
            return
        else:
            self.current_timestamp = timestamp
            # self.tracking_orders()
            self.on_tick()

    def place_order(self, order):
        self.exchange.place_order(order)
    
    def cancel(self, order_id:str) -> str:
        canceled = self.exchange.cancel_order(order_id)
        # self.order_tracker.stop_track_order(order_id)
        print("[INFO]:", "order cancelled\n {}".format(canceled.id))
        return canceled.id
    
    # def get_active_orders(self, connector_name: str) -> List[LimitOrder]:
    #     """
    #     Returns a list of active orders for a connector.
    #     :param connector_name: The name of the connector.
    #     :return: A list of active orders
    #     """
    #     return self.order_tracker.active_limit_orders
    
    # def tracking_orders(self):
    #     active_orders = self.get_active_orders()
    #     for orders in active_orders:
    #         for order in orders.values():
    #             self.exchange.print_order_info(order)
                