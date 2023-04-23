#!/usr/bin/python
# -*- coding: utf8 -*-
"""FIX Application"""
import quickfix as fix
import time
from datetime import datetime, timedelta
from .base_fix_client import BaseFixClient
from ..common.dto import OrderCandidate, OrderInFlight
from ..common.order_tracker import OrderTracker
import pandas as pd

class DTLFixClient(BaseFixClient):
    DT_FORMAT = "%Y%m%d-%H:%M:%S.%f"

    def init_order_tracker(self):
        self.order_tracker = OrderTracker(self._settings["order_lifespan"])

    def place_order(self, order: OrderCandidate):
        """Request sample new order single"""
        message = fix.Message()
        header = message.getHeader()
        header.setField(fix.MsgType(fix.MsgType_NewOrderSingle))  # 39 = D
        # 11 = Unique Sequence Number
        message.setField(fix.ClOrdID(self.genExecID()))
        message.setField(fix.Side(order.order_side))  # 54 = 1 BUY
        message.setField(fix.Symbol(order.symbol))  # 55 = MSFT
        message.setField(fix.OrderQty(order.amount))  # 38 = 1000
        message.setField(fix.OrdType(order.order_type))  # 40=2 Limit Order
        # if order.order_type != OrderType.MARKET.value:
        message.setField(fix.Price(order.price))
        message.setField(fix.HandlInst(
            fix.HandlInst_MANUAL_ORDER_BEST_EXECUTION))  # 21 = 3
        message.setField(fix.TimeInForce('0'))
        message.setField(fix.Text("NewOrderSingle"))
        trstime = fix.TransactTime()
        trstime.setString(datetime.utcnow().strftime(DTLFixClient.DT_FORMAT)[:-3])
        message.setField(trstime)
        fix.Session.sendToTarget(message, self.sessionID)

    def cancel_order(self, order_id: str):
        """Request sample new order single"""
        order = self.order_tracker.get(order_id)
        message = fix.Message()
        header = message.getHeader()
        header.setField(fix.MsgType(fix.MsgType_OrderCancelRequest))     #35 = F
        message.setField(fix.ClOrdID(self.genExecID()))
        message.setField(fix.OrigClOrdID(order_id))
        message.setField(fix.Symbol(order.symbol))  # 55 = MSFT
        message.setField(fix.OrderQty(order.amount))  # 38 = 1000
        # message.setField(fix.OrderID(order.order_assigned_id))  37
        message.setField(fix.Side(order.order_side))  # 54 = 1 BUY
        trstime = fix.TransactTime()
        trstime.setString(datetime.utcnow().strftime(DTLFixClient.DT_FORMAT)[:-3])
        message.setField(trstime)
        fix.Session.sendToTarget(message, self.sessionID)

    def tick(self, timestamp: float):
        self.current_timestamp = timestamp
        if self.create_timestamp <= self.current_timestamp:
            for order_id in self.order_tracker.matured_orders:
                print("Cancelling order: {}".format(order_id))
                self.cancel_order(order_id)
            self.create_timestamp = self.refresh_time + self.current_timestamp
    def onMessage(self, message, sessionID):
        msgType = message.getHeader().getField(35)
        if msgType == "8":
            self.onExecutionReport(message, sessionID)
        elif msgType == "3":
            self.onReject(message, sessionID)
        elif msgType == "9":
            self.onCancelReject(message, sessionID)
        else:
            print("[WARNING]: Unknown message type %s", message.toString().replace(BaseFixClient.__SOH__, "|"))

    def onExecutionReport(self, message, sessionID):
        # Handle execution report
        msgType = message.getField(150)
        order_id = message.getField(11)
        if msgType == "0": #new order
            order_assigned_id = message.getField(37)
            order_side = message.getField(54)
            symbol = message.getField(55)
            order_type = message.getField(40)
            amount = float(message.getField(38))
            price = float(message.getField(44))
            created_at = datetime.strptime(message.getHeader().getField(52), DTLFixClient.DT_FORMAT)            
            self.order_tracker.start_track_order(order_id, OrderInFlight(order_assigned_id, created_at, order_type, order_side, amount, price, symbol))
        elif msgType in ["1", "2"]: #partially filled or filled
            amount = float(message.getField(32))
            price = float(message.getField(31))
            symbol = message.getField(55)
            order_side = message.getField(54)
            self._data_report.append({"order_id": order_id, "symbol": symbol, "order_side": order_side, "amount": amount, "price": price})
            self.order_tracker.adjust_tracked_order_on_partially_filled(order_id, amount) 
            if msgType == "2":
                self.order_tracker.stop_track_order(order_id, "completed")
        elif msgType == "8": #filled
            self.onReject(message, sessionID)
        else:
            print("[WARNING]: Unknown message type %s", message.toString().replace(BaseFixClient.__SOH__, "|"))


    def onReject(self, message, sessionID):
        # Handle reject
        order_id = message.getField(11)
        rej_reason = message.getField(58)
        print("[WARNING]: Failed to send the order {} due to {}".format(order_id, rej_reason))
        self.order_tracker.stop_track_order(order_id, "rejected")
        
    def onCancelReject(self, message, sessionID):
        # Handle cancel reject
        order_id = message.getField(41)
        rej_reason = message.getField(58)
        print("[WARNING]: Failed to cancel the order {} due to {}".format(order_id, rej_reason))

    def report(self) -> bool:
        df = pd.DataFrame(self._data_report)
        if len(self._data_report) == self.order_tracker.n_completed_orders: #wating for all orders to be processed
            return False
        return True