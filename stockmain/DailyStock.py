import null as null
import pandas as pd
import requests
from bs4 import BeautifulSoup

from componydata import compan
#from database import DB
from DBConn import sqldata
import util.utillib as utlib

def get_url( item_name, code_df):
    code = code_df.query("name=='{}'".format(item_name))['code'].to_string(index=False)
    code = code.strip()
    url = 'http://finance.naver.com/item/sise_day.nhn?code={code}'.format(code=code)

    print("요청 URL = {}".format(url))
    return url

def get_stock_data(item_name, code, pagenumber):

    #url = get_url(item_name, code)
    url = 'http://finance.naver.com/item/sise_day.nhn?code={code}'.format(code=code)
    print(url)

    hdr = {
        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 9_3_2 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13F69 Safari/601.1',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3', 'Accept-Encoding': 'none',
        'Accept-Language': 'en-US,en;q=0.8', 'Connection': 'keep-alive'}

    df = pd.DataFrame()

    if pagenumber == 0:
        pagenumber = 12

    for page in range(1, pagenumber):
        pg_url = '{url}&page={page}'.format(url=url, page=page)
        res = requests.get(pg_url, headers = hdr )
        soup = BeautifulSoup(res.content, 'html.parser')
        table = soup.find_all('table')

        ret = pd.read_html(str(table),header=0)[0]
        df = df.append(ret, ignore_index=True)


    df = df.dropna()
    df = df.rename(columns={'날짜': 'date', '종가': 'close', '전일비': 'diff', '시가': 'open',
                            '고가': 'high', '저가': 'low', '거래량': 'volume'})

    df[['close', 'diff', 'open', 'high', 'low', 'volume']] \
        = df[['close', 'diff', 'open', 'high', 'low', 'volume']].astype(int)

    df['date'] = pd.to_datetime(df['date'])
    df = df.sort_values(by=['date'], ascending=True)

    return df

def update_stockday(days, allflag):
    result = 0

    if allflag:
        print('all')
    else:
        print('some')

    return result

def update_daily_stock():

    sa = sqldata.getInstance()

    sesql = '''SELECT name, code FROM corplist  '''
    ret = sa.executes(sesql)

    for i in ret:
        print(i)
        comname = str(i['name'])
        code = str(i['code'])
        print(comname, code)

        if len(code) < 6:
            length = 6-len(code)
            print("Code is too shot {}".format(len(code)))
            for i in range(0, length):
                code = '0'+code

        sesql = '''select date from dailystock where comcode = '{}' order by date desc limit 1'''.format(code)
        print(sesql)
        ret1 = sa.executes(sesql)


        if not ret1:
            # Stock data is empty, have to update whole data
            print('Whole data')
            ddf = get_stock_data(comname, code, 20)
            print(ddf)
            try:
                for i, row in ddf.iterrows():

                    try:

                        insql = '''INSERT INTO dailystock(comcode, date, close, diff, open, high, low, volume )
                        VALUES( '{}','{}', {}, {}, {}, {}, {}, {} )'''.format(code, row['date'], row['close'],
                                                                            row['diff'],
                                                                            row['open'], row['high'], row['low'],
                                                                            row['volume'])

                        sa.executes(insql)
                    except Exception as e:
                        print("Daily Stock Data Insert Error")
                        print(e)

                upsql = '''UPDATE corplist SET updateflag = {} WHERE code = {} '''.format('1', code)
                # print(upsql)
                sa.executes(upsql)

            except Exception as e:
                print(e)
                upsql = '''UPDATE corplist SET updateflag = {} WHERE code = {} '''.format('2', code)
                sa.executes(upsql)


        else:
            print('achaive data')
            print(ret1[0]['date'])
            daybet = utlib.get_datediff(ret1[0]['date'].strftime("%Y-%m-%d"), utlib.gettoday())
            print(daybet)
            if daybet > 0:
                pagenumber = 2

                if daybet < 30:
                    pagenumber = 4

                if daybet < 20:
                    pagenumber = 3

                if daybet < 10:
                    pagenumber = 2

                print('Page Number is {}'.format(str(pagenumber) ))
                ddf = get_stock_data(comname, code, pagenumber)

                try:
                    for i, row in ddf.iterrows():
                        daybet2 = utlib.get_datediff(row['date'].strftime("%Y-%m-%d"), ret1[0]['date'].strftime("%Y-%m-%d") )
                        print(daybet2)

                        if daybet2 < 0:
                            insql = '''INSERT INTO dailystock(comcode, date, close, diff, open, high, low, volume )
                            VALUES( '{}','{}', {}, {}, {}, {}, {}, {} )'''.format(code, row['date'], row['close'],
                                                                                row['diff'],
                                                                                row['open'], row['high'], row['low'],
                                                                                row['volume'])
                            sa.executes(insql)

                    upsql = '''UPDATE corplist SET updateflag = {} WHERE code = {} '''.format('3', code)
                    # print(upsql)
                    sa.executes(upsql)

                except Exception as e:
                    print('UPDATE Daily Stock : {}'.format(e))
                    upsql = '''UPDATE corplist SET updateflag = {} WHERE code = {} '''.format('2', code)
                    sa.executes(upsql)

    return



if __name__ == "__main__":

    update_daily_stock()

