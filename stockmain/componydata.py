#-*- coding:utf-8 -*-
import os
from datetime import datetime
from DBConn import sqldata
import pandas as pd

class compan(object):

    def __init__(self):
        self.stockdb = sqldata.getInstance()
        pass

    def updatecompanylist(self):

        today = datetime.today().strftime("%Y-%m-%d")
        print(today)

        try:
            # DB Exist Check
            #results = self.stockdb.executes('''SELECT count(*) FROM sqlite_master WHERE type='table' AND name = "corplist";''')
            asql = '''SELECT EXISTS(SELECT 1 FROM Information_schema.tables WHERE table_schema = "STOCKDB" AND table_name = "corplist") as exist;'''
            results = self.stockdb.executes(asql)

            #print('test')
            print(results[0]['exist'])

            # Not Exist
            if results[0]['exist'] == 0:
                print('create compayny data')
                csql = '''CREATE TABLE corplist (RegDT varchar(20), name varchar(100), code int, kind varchar(50), product varchar(100), regdate varchar(30), endmonth varchar(30), owner varchar(30), homepage varchar(200), region varchar(30) );'''
                print(csql)
                self.stockdb.executes(csql)
            else:
                print('data check')
                # if data is 7day long then update whole data
                #csql = '''select  RegDT from corplist where RegDT < (SELECT DATE('now', '-7 day')) limit 1;'''
                #csql1 = '''select count(*) from corplist where RegDT < (SELECT DATE('now', '-7 day'));'''
                csql1 = '''select count(*) as cnt from corplist where RegDT <  DATE(NOW()) - INTERVAL 7 DAY'''
                #print(csql1)
                ret1 = self.stockdb.executes(csql1)

                # Data Exist Check
                csql2 = '''select count(*) as cnt from corplist;'''
                #print(csql2)
                ret2 = self.stockdb.executes(csql2)
                print(ret2)

                if ret1[0]['cnt'] != 0 or ret2[0]['cnt'] == 0:
                    print("Data is 7 days long, Update Processing Or Data is empty")
                    csql = '''TRUNCATE TABLE corplist;'''
                    print(csql)
                    self.stockdb.executes(csql)
                else:
                    print("Data is within 7 Days Skip update Process")
                    return

            print('Company refresh')
            code_df = pd.read_html('http://kind.krx.co.kr/corpgeneral/corpList.do?method=download&searchType=13', header=0)[0]
            #print(code_df)

            code_df.종목코드 = code_df.종목코드.map('{:06d}'.format)
            code_df = code_df.rename(
                columns={'회사명': 'name', '종목코드': 'code', '업종': 'kind', '주요제품': 'product', '상장일': 'regdate',
                         '결산월': 'endmonth',
                         '대표자명': 'owner', '홈페이지': 'homepage', '지역': 'region'})
            code_df[['code']] = code_df[['code']].astype(int)

            for i, row in code_df.iterrows():

                prod = str(row['product']).replace('\'','')

                code = str(row['code'])
                if len(code) < 6:
                    length = 6 - len(code)
                    print("Code is too shot {}".format(len(code)))
                    for i in range(0, length):
                        code = '0' + code

                insql = '''INSERT INTO corplist(RegDT, name, code, kind, product, regdate, endmonth, owner, homepage, region)
                        VALUES('{}','{}', '{}','{}', '{}', '{}', '{}', '{}', '{}', '{}' )'''.format( today , row['name'], code,
                                                                                             row['kind'],
                                                                                             prod,
                                                                                             row['regdate'],
                                                                                             row['endmonth'],
                                                                                             row['owner'],
                                                                                             row['homepage'],
                                                                                             row['region'])
                print(insql)
                self.stockdb.executes(insql)

            # Exist Update Process
            #print(self.stockdb.executes('''SELECT * FROM sqlite_master WHERE name = "corplist";'''))
            print('Skip')

        except Exception as e:
            print(insql)
            print('Error : ', e.args[0])
            print(e)
            pass

    def companylist(self):

        pass
