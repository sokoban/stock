import pandas as pd
from DBConn import sqldata
import pandas as pd
from componydata import compan
import util.utillib as utlib

if __name__ == "__main__":

    sa = sqldata.getInstance()

    sesql = '''select date from dailystock where comcode = {} order by date desc limit 1'''.format('84850')
    ret1 = sa.executes(sesql)

    if not ret1:
        # Stock data is empty, have to update whole data
        print('empty')
    else:
        print(ret1[0]['date'])
        daybet = utlib.get_datediff( ret1[0]['date'].strftime("%Y-%m-%d") ,utlib.gettoday() )
        print(daybet)
        if daybet > 0:
            print('have to update')
        print(ret1[0]['date'].strftime("%Y-%m-%d"))

    print( utlib.gettoday() )

