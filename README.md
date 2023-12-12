`init/` folder to get the data and test strategies

Different subaccounts have been created to save leverages losses.
Each bot consist of the symbol, name of the subaccount, and the strategy.
They are are run every each 2 minutes.

To find the best strategy, the past data was retrieved and backtested for each dataframe grouped by every 2 days using vectorvbt. Plot the results or automatically choose the strategy based on the returns.

new_bot_base.py - Base class for the Bot
new_bot.py - Bot with functionalities for the Bot
new_bot_run.py - To run all the bots

draft_bot.py - First version of the live bot

