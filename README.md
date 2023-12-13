The 'init/' directory serves as the repository for acquiring data and testing various strategies.

Distinct subaccounts have been established to mitigate leverage-associated losses. Each bot is characterized by its symbol, designated subaccount, and specific strategy. These bots are executed at regular intervals of every 2 minutes.

In the pursuit of identifying the most effective strategy, historical data was extracted and systematically backtested across different dataframes, segmented by intervals of 2 days using the powerful vectorvbt library. The outcomes were either visually depicted through plotted results or algorithmically determined by maximizing returns.

Key files within this framework include:

- new_bot_base.py: Serving as the foundational class for the Bot
- new_bot.py: Encompassing functionalities specific to the Bot
- new_bot_run.py: Enabling the simultaneous execution of all bots

Additionally, the preliminary version of the live bot, denoted as draft_bot.py, is also part of this array of functionalities.

