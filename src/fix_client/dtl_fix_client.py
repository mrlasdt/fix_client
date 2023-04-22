#!/usr/bin/python
# -*- coding: utf8 -*-
"""FIX Application"""
import sys
import quickfix as fix
import time
from datetime import datetime
from .base_fix_client import BaseFixClient
from ..common.dto import OrderCandidate
from ..common.order_tracker import OrderTracker


class DTLFixClient(BaseFixClient):
    def __init__(self, logger_name: str, log_file_path: str):
        self.ready = False
        super().__init__(logger_name, log_file_path)

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
        trstime.setString(datetime.utcnow().strftime(
            "%Y%m%d-%H:%M:%S.%f")[:-3])
        message.setField(trstime)
        # message.setField(fix.Currency("USD")) #15 = USD
        fix.Session.sendToTarget(message, self.sessionID)

    def cancel_order(self, order_id: int):
        pass

    def tick(self, timestamp: float):
        pass
    
    def onMessage(self, message, sessionID):
        msgType = message.getHeader().getField(35).getString()
        if msgType == "8":
            self.onExecutionReport(message, sessionID)
        elif msgType == "3":
            self.onReject(message, sessionID)
        elif msgType == "9":
            self.onCancelReject(message, sessionID)

    def onExecutionReport(self, message, sessionID):
        # Handle execution report
        pass

    def onReject(self, message, sessionID):
        # Handle reject
        pass

    def onCancelReject(self, message, sessionID):
        # Handle cancel reject
        pass