import pandas as pd
pd.core.common.is_list_like = pd.api.types.is_list_like
import pandas_datareader.data as web
import numpy as np
from datetime import datetime, timedelta
import logging

import sys
sys.path.insert(0, '/home/jerseyfinance2018/Notebooks/API')
from DBUtil import DBUtil

logger = logging.getLogger('dail_price_grab')
logger.setLevel(logging.DEBUG)
# create file handler which logs even debug messages
fh = logging.FileHandler('/home/jerseyfinance2018/jobScheduler/daily_price_grab.log')
# create formatter and add it to the handlers
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
logger.addHandler(fh)


today = (datetime.today() - timedelta(days=2)).date()
tickers = DBUtil.getAllTickers(True)
for ticker in tickers:
    logger.info('getting daily price for ' + ticker)
    try:
        f = web.DataReader([ticker], 'robinhood')
        df = f.loc[f.index.get_level_values('begins_at') > today.strftime("%Y-%m-%d")]
        for key, row in zip(df.index.values, df.to_dict("record")):#
            pdt = key[1].to_pydatetime()
            sdt = np.vectorize(lambda s: s.strftime('%Y%m%d'))(pdt)
            DBUtil.insertDaily(key[0] + ' US Equity', sdt, float(row['close_price']), float(row['high_price']), 
                       float(row['low_price']), float(row['open_price']), float(row['volume']))
    except Exception as e:
            logger.info(e)
            continue
