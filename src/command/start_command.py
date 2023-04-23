import time
import quickfix as fix
from src.common.clock import Clock
from src.strategy.dtl_strategy import DTLStrategy as Strategy
from src.fix_client.dtl_fix_client import DTLFixClient as FixClient


class StartCommand:
    def _initialize_fix_client(self):
        exchange = FixClient(self._settings["exchange"])
        exchange.init_order_tracker()
        fix_settings = fix.SessionSettings(
            self._settings["exchange"]["config_path"])
        storefactory = fix.FileStoreFactory(fix_settings)
        logfactory = fix.FileLogFactory(fix_settings)
        self._initiator = fix.SocketInitiator(
            exchange, storefactory, fix_settings, logfactory)
        return exchange

    def _initialize_strategy(self):
        exchange = self._initialize_fix_client()
        self.strategy = Strategy(exchange, self._settings["strategy"])

    def warmup(self):
        self._initialize_strategy()

    def start(self):
        self._initiator.start()
        self.start_time = time.time() * 1e3  # Time in milliseconds
        tick_size = self._settings["tick_size"]
        print('[INFO]:', f"Creating the clock with tick size: {tick_size}")
        self.clock = Clock(tick_size=tick_size)
        if self.strategy:
            self.clock.add_iterator(self.strategy.exchange)
            self.clock.add_iterator(self.strategy)
        self.clock.run()
        keep_run = True
        while keep_run:
            keep_run = self.strategy.report()
        return
