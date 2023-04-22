#!/usr/bin/python
# -*- coding: utf8 -*-
"""FIX Application"""
import sys
import quickfix as fix
import time
from datetime import datetime
from .base_fix_client import BaseFixClient
from ..common.dto import OrderCandidate
__SOH__ = chr(1)

class DTLFixClient(BaseFixClient):
    def __init__(self, logger_name: str):
        self.ready=False
        super().__init__(logger_name)

    def place_order(self, order:OrderCandidate):
        """Request sample new order single"""
        message = fix.Message()
        header = message.getHeader()
        header.setField(fix.MsgType(fix.MsgType_NewOrderSingle)) #39 = D 
        message.setField(fix.ClOrdID(self.genExecID())) #11 = Unique Sequence Number
        message.setField(order.order_side) #43 = 1 BUY 
        message.setField(order.symbol) #55 = MSFT
        message.setField(order.amount) #38 = 1000
        message.setField(order.price)
        message.setField(order.order_type) #40=2 Limit Order 
        message.setField(fix.HandlInst(fix.HandlInst_MANUAL_ORDER_BEST_EXECUTION)) #21 = 3
        message.setField(fix.TimeInForce('0'))
        message.setField(fix.Text("NewOrderSingle"))
        trstime = fix.TransactTime()
        trstime.setString(datetime.utcnow().strftime("%Y%m%d-%H:%M:%S.%f")[:-3])
        message.setField(trstime)
        # message.setField(fix.Currency("USD")) #15 = USD
        fix.Session.sendToTarget(message, self.sessionID)
        
    def cancel_order(self, order_id:int):
        pass
    
    def tick(self, timestamp: float):
        pass