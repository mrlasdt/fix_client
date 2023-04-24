
from .dto import OrderInFlight
from datetime import timedelta, datetime


class OrderTracker:

    def __init__(self, order_lifespan: int):
        super().__init__()
        self._tracked_orders: dict[str, OrderInFlight] = {}
        self._complelete_orders: dict[str, OrderInFlight] = {}
        self._rejected_orders: dict[str, OrderInFlight] = {}
        self._untracked_orders: dict[str, OrderInFlight] = {}
        self._order_lifespan = timedelta(seconds=order_lifespan)
        self._last_completed_order_id = -1
        self._last_rejected_order_id = -1

    def get(self, order_id: str) -> OrderInFlight:
        return self._tracked_orders[order_id]

    @property
    def matured_orders(self):
        return [order_id for order_id, order in self._tracked_orders.items() if datetime.utcnow() - order.created_at > self._order_lifespan]

    @property
    def tracked_orders(self):
        return list(self._tracked_orders.keys())

    @property
    def last_completed_order_id(self):
        return self._last_completed_order_id

    @property
    def last_rejected_order_id(self):
        return self._last_rejected_order_id

    def start_track_order(self, order_id: str, order: OrderInFlight):
        self._tracked_orders[order_id] = order

    def stop_track_order(self, order_id, mode: str = ""):
        if order_id not in self._tracked_orders:
            order: OrderInFlight = -1  # type: ignore
        else:
            order = self._tracked_orders.pop(order_id)
        if mode == "rejected":
            self._rejected_orders[order_id] = order
            self._last_rejected_order_id = max(
                int(order_id), self._last_rejected_order_id)
        elif mode == "completed":
            self._complelete_orders[order_id] = order
            self._last_completed_order_id = max(
                int(order_id), self._last_completed_order_id)
        else:
            self._untracked_orders[order_id] = order

    def adjust_tracked_order_on_partially_filled(self, order_id: str, amount: float):
        self._tracked_orders[order_id].amount -= amount
