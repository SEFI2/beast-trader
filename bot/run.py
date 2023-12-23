import time
import schedule
import pandas as pd
pd.set_option('display.max_rows', None)

import time
import time
from utils.configurations import configurations
from bot.bot import Bot

import warnings
warnings.filterwarnings("ignore")

def run_all_bots():
    timeframe = "1m"

    bots = []
    for config in configurations:
        bot = Bot(
            config["account_name"],
            config["symbol"],
            timeframe,
            config["strategy_func"],
            config["leverage"],
            config["precision"],
            config["minAmount"],   
        )
        bots.append(bot)

    def execute_bots():
        for bot in bots:
            bot.run()
            time.sleep(1)

    execute_bots()
    schedule.every(10).seconds.do(execute_bots)

    while True:
        schedule.run_pending()
        time.sleep(1)

run_all_bots()
