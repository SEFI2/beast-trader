# Folders
- The `init/` directory acts as the central repository for acquiring data and conducting tests on different strategies.
- The `'data*'` directories house saved CSV files containing collected data.
- `data_collector/` - This class offers functional APIs to gather and handle data effectively.
- `plot/` - Tools and utilities used for visualizing results and data.
- `test_strategy/` - Utilizes VectorVBT for testing strategies.
- `volatility/` - Contains functions dedicated to assessing market volatility.
- `strategy_finder/` - Responsible for sorting and selecting strategies based on specific criteria.
- `symbols` - A repository that holds filtered symbols.



Distinct subaccounts have been established to mitigate leverage-associated losses. Each bot is characterized by its symbol, designated subaccount, and specific strategy. These bots are executed at regular intervals of every 20 seconds. It analyzes current positions, while deciding if it needs to close some of them based on the return. Also, it provides stop loss and take profits orders.

In the pursuit of identifying the most effective strategy, historical data was extracted and systematically backtested across different dataframes, segmented by intervals of 2 days using the powerful vectorvbt library. The outcomes were either visually depicted through plotted results or algorithmically determined by maximizing returns.

# First Bot

(First version of the bot) The initial bot employs vectorbt to dynamically select its trading strategy by rigorously testing all available bots using live data. This process enables it to intelligently discern and implement the most effective strategy based on these comprehensive test results.

# New Bot
(Last version) The new bot represents a significant improvement—a refactored and debugged version featuring enhanced order processes and better risk management. I embarked on this endeavor after realizing the frequency of errors in the initial bot was becoming an issue.

Key files within this framework include:
- new_bot_base.py: Serving as the foundational class for the Bot
- new_bot.py: Encompassing functionalities specific to the Bot
- new_bot_run.py: Enabling the simultaneous execution of all bots

Additionally, the preliminary version of the live bot, denoted as draft_bot.py, is also part of this array of functionalities.


# Challenges

1. **Setting up leverage for BitMex**: Leverage is established at the symbol level during initialization rather than being set for individual orders.

2. **Stop Loss & Take Profit Orders**: Implementing functionalities to execute stop loss and take profit orders effectively.

3. **Stop Order Limitations on BitMex**: Addressing and navigating the limitations and constraints associated with stop orders on the BitMex platform.

4. **Different Precision for Amounts**: Ensuring the precision of amounts adheres to BitMex requirements (e.g., ensuring the amount of ETH/USDT is greater than the minimum amount precision of 1000 USDT).

5. **Minimum Amount for Various Tokens**: Managing minimum amount requirements for different tokens traded on the platform.

6. **Budget Distribution for Multiple Pairs**: Developing a strategy to effectively distribute the budget when a single account engages in trading across multiple pairs.

7. **Testing Tools for Strategies**: Identifying and utilizing appropriate tools to thoroughly test and validate trading strategies before deployment. This might involve backtesting, simulations, or other forms of strategy validation.


