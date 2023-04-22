
from .dto import OrderInFlight


class OrderTracker:
    def __init__(self):
        super().__init__()
        self._tracked_orders: dict[str, OrderInFlight] = {}

    # @property
    # def active_orders(self):
    #     limit_orders = []
    #     for market, limit_order in self._tracked_orders.items():
    #         limit_orders.append((market, limit_order))
    #     return limit_orders

    def start_track_order(self, order_id):
        # self._tracked_orders[order_id] = OrderInFlight()
        pass

    def stop_track_order(self, order_id):
        self._tracked_orders.pop(order_id)
