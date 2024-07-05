import threading
import time

from engine import *


class Pairs:

    def __init__(self, client_bot):
        self.client = client_bot
        self.all_futures_symbols = {}
        self.symbols_with_usdt = []
        self.final_symbols_more_6m = []
        self.final_symbols_less_6m = []

    def _get_info(self):
        self.all_futures_symbols = self.client.futures_exchange_info()['symbols']

        for symbol in self.all_futures_symbols:
            if symbol['symbol'].endswith('USDT'):
                self.symbols_with_usdt.append(symbol['symbol'])

    def get_one_pair(self, symbol_name):
        klines = self.client.futures_historical_klines(symbol=symbol_name, interval='1M', start_str=1644308894652)
        if len(klines) > 6:
            logger.trace(f'Символ {symbol_name}: {len(klines)}')
            self.final_symbols_more_6m.append(symbol_name)
        else:
            self.final_symbols_less_6m.append(symbol_name)

    def get_all_pairs(self) -> list:
        self._get_info()
        tasks = []
        for symbol_name in self.symbols_with_usdt:
            t = threading.Thread(target=self.get_one_pair, args=(symbol_name,))
            tasks.append(t)
        for task in tasks:
            task.start()
            time.sleep(0.1)
        logger.trace("Обновлен список пар")
        return self.final_symbols_more_6m
