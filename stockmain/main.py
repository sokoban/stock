#-*- coding:utf-8 -*-

import pandas as pd
from componydata import compan
#from database import DB
from DBConn import sqldata
import DailyStock

if __name__ == "__main__":

    com = compan()
    com.updatecompanylist()

    sa = sqldata.getInstance()

    DailyStock.update_daily_stock()

