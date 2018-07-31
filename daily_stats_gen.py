import pandas as pd
pd.core.common.is_list_like = pd.api.types.is_list_like
import pandas_datareader.data as web
import numpy as np
from datetime import datetime, timedelta
import logging
from stockstats import StockDataFrame

import sys
sys.path.insert(0, '/home/jerseyfinance2018/Notebooks/API')
from DBUtil import DBUtil

logger = logging.getLogger('dail_stats_gen')
logger.setLevel(logging.DEBUG)
# create file handler which logs even debug messages
fh = logging.FileHandler('/home/jerseyfinance2018/jobScheduler/daily_stats_gen.log')
# create formatter and add it to the handlers
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
logger.addHandler(fh)

tickers = DBUtil.getAllTickers(False)
endDate = int(datetime.today().date().strftime("%Y%m%d"))
startDate = int((datetime.today() - timedelta(days=50)).date().strftime("%Y%m%d"))

for ticker in tickers:
    logger.info('generating daily stats for ' + ticker)
    try:
        df = pd.DataFrame(DBUtil.getDailyPrices(ticker, startDate, endDate))
        stock = StockDataFrame.retype(df)
        stock.get('close_5_ema')
        stock.get('close_10_ema')
        stock.get('close_20_ema')
        stock.get('close_30_ema')
        stock.get('rsi_14')
        stock.get('macd')

        DBUtil.insertLastestStat(df, ticker, 'day', 'macd', 'macds', 'macdh', 'close_5_ema', 'close_10_ema', 'close_20_ema', 'close_30_ema', 'rsi_14', 'volume_50_sma')
    except Exception as e:
            logger.error(e)
            print(e)
            continue
