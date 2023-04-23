
import random
import sys
import time
import pandas as pd
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
        if self.create_timestamp <= self.current_timestamp and self.max_n_orders > 0:
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
        return "" if len(lorders) == 0 else random.choice(lorders)

    def _calculate_vwap_single_instrument(self, df_receive_single: pd.DataFrame) -> float:
        total_volume = df_receive_single.amount.sum()
        total_value = (df_receive_single['amount'].mul(
            df_receive_single['price'])).sum()
        vwap = total_value/total_volume
        return vwap

    def calculate_vwap(self, df_receive: pd.DataFrame) -> dict[str, float]:
        dvwap = {}
        for symbol in Symbol.get_values():
            df_receive_single = df_receive[df_receive.symbol == symbol]
            vwap = self._calculate_vwap_single_instrument(df_receive_single)
            dvwap[symbol] = vwap
        return dvwap

    def calculate_total_value(self, df_receive: pd.DataFrame) -> float:
        return df_receive['amount'].mul(df_receive['price']).sum()

    def _calculate_profit_of_buy_or_sell(self, df_receive_single: pd.DataFrame, order_side: OrderSide) -> float:
        trade = df_receive_single[df_receive_single.order_side == order_side]
        last_price = df_receive_single.iloc[-1].price
        total_volume = trade.amount.sum()
        total_value = (trade['amount'].mul(trade['price'])).sum()
        profit = total_value - total_volume*last_price
        return -profit if order_side == OrderSide.BUY else profit

    def _calculate_profit_of_short(self, df_receive_single: pd.DataFrame, df_sent_single: pd.DataFrame) -> float:
        return 0

    def calculate_profit(self, df_receive: pd.DataFrame, df_sent: pd.DataFrame) -> float:
        profit = 0
        for symbol in Symbol.get_values():
            df_receive_single = df_receive[df_receive.symbol == symbol]
            df_sent_single = df_sent[df_sent.symbol == symbol]
            for order_side in OrderSide.get_values():
                if order_side != OrderSide.SHORT:
                    profit += self._calculate_profit_of_buy_or_sell(
                        df_receive_single, order_side)
                else:

                    profit += self._calculate_profit_of_short(
                        df_receive_single, df_sent_single)
        return profit

    def report(self) -> bool:
        if self.exchange.last_sent_order_id != self.exchange.order_tracker.last_rejected_order_id and self.exchange.last_sent_order_id != self.exchange.order_tracker.last_completed_order_id:
            return True
        df_receive = pd.DataFrame(self.exchange.data_received)
        df_sent = pd.DataFrame(self.exchange.data_sent)
        dvwap = self.calculate_vwap(df_receive)
        print("[INFO]: Total volume is {:.2f} USD".format(
            self.calculate_total_value(df_receive)))
        print("[INFO]: PNL is {:.2f} USD".format(
            self.calculate_profit(df_receive, df_sent)))
        for symbol, vwap in dvwap.items():
            print("[INFO]: VWAP of {} is {:.2f}".format(symbol, vwap))
        # wating for all orders to be processed
        return False
