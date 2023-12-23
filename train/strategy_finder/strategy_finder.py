from test_strategy.test_strategy import test_strategy
from tqdm import tqdm
import pandas as pd
import os

class StrategyFinder:
    def __init__(self, symbol, timeframe, strategies_list):
        self.symbol = symbol
        self.timeframe = timeframe
        self.strategies_list = strategies_list
        folder = 'data_strategy/'
        temp_name = f'strategies_{self.symbol}_{self.timeframe}.csv'
        temp_name = temp_name.replace("/", "_")
        self.file_name = f'{folder}{temp_name}'


    def retrieve_existing_stategies_list(self):
        if not os.path.isfile(self.file_name):
            print(f"ERR! No saved strategy exists for {self.symbol}")
            return None

        df = pd.read_csv(self.file_name)
        arr = df.values.tolist()
        for row in arr:
            name = row[0]
            profit = float(row[1])
            print("row", row)
            for strategy in self.strategies_list:
                if strategy['name'] == name:
                    strategy['profit'] = profit
        self._sort_strategies_list()
        return self.strategies_list

    def get_stategies_list(self):
        return self.strategies_list
  
    def _save_strategies_list(self):
        column_names = ["Strategy", "Profit"]
        rows = []
        for strategy in self.strategies_list:
            row = [strategy['name'], strategy['profit']]
            rows.append(row)
        df = pd.DataFrame(rows, columns=column_names)
        df.to_csv(self.file_name, index=False)

    def _sort_strategies_list(self):
        sorted_strategies = sorted(
            self.strategies_list,
            key=lambda strategy: strategy["profit"],
            reverse=True
        )
        self.strategies_list =  sorted_strategies

    def update_strategies_list(self, df):

        for strategy in tqdm(self.strategies_list):
            temp_name = f'profits_{strategy["name"]}_{self.symbol}_{self.timeframe}.csv'
            profits_file = f'data_profits/{temp_name.replace("/", "_")}'
            if os.path.exists(profits_file):
                print("WRN! Profits data for {profits_file} already exists. Skip")
                continue

            profits = test_strategy(df, strategy['func'])
            strategy["profit"] = profits[-1]
            profits.to_csv(profits_file)

        self._sort_strategies_list()

        print(f"For symbol {self.symbol}")
        print("Sorted in following order.")
        for strategy in self.strategies_list:
            print("Name: ", strategy["name"])
            print("Profit: ", strategy["profit"])
            print()

        self._save_strategies_list()

