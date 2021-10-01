import pandas as pd
from DBConn import sqldata






if __name__ == "__main__":



    #Get Database instance
    sa = sqldata.getInstance()
    csql = '''select ab.comcode,bc.name ,count(*) from dailystock ab inner join corplist bc on ab.comcode = bc.code group by ab.comcode, bc.name'''
    ret1 = sa.executes(csql)

    print(ret1[0])
