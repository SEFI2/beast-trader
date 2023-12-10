from test_strategy import test_strategy

class StrategyFinder:
    def __init__(self, symbol, strategies_list):
        self.symbol = symbol
        self.strategies_list = 
    
    def get_stategies_list(self):
        return self.strategies_list

    def update_strategies_list(self, df):
        for strategy in self.strategies_list:
            profit = test_strategy(df, strategy['func'])
            strategy["profit"] = profit

        sorted_functions = sorted(
            self.strategies_list,
            key=lambda strategy: strategy["profit"],
            reverse=True
        )
        print(f"For symbol {self.symbol}")
        print("Sorted in following order.")
        for strategy in sorted_functions:
            print("Name: ", strategy["name"])
            print("Profit: ", strategy["profit"])
            print()
        self.strategies_list = sorted_functions

