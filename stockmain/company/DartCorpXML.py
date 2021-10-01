#-*- coding:utf-8 -*-
import sys, os
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
import xml.etree.ElementTree as et
from DBConn import sqldata

'''
Company Finance Information Code ( By DART)
Download link : https://opendart.fss.or.kr/api/corpCode.xml (GET)
parameterr : crtfc_key : API auth key

CREATE TABLE corpfnlist (
corp_code varchar(10)
, corp_name varchar(50)
, stock_code varchar(20)
, modifydate varchar(10)
)
'''

if __name__ == "__main__":

    sa = sqldata.getInstance()

    xtree = et.parse("/Users/sokoban/git/stocak/CORPCODE.xml")
    xroot = xtree.getroot()

    df_cols = ["corp_code", "corp_name", "stock_code", "modify_date"]
    rows = []

    for node in xroot:
        corpcode = node.find("corp_code").text if node is not None else None
        corpname = node.find("corp_name").text if node is not None else None
        stockcode = node.find("stock_code").text if node is not None else None
        modidate = node.find("modify_date").text if node is not None else None

        insql = '''INSERT INTO corpfnlist(corp_code,corp_name,stock_code,modifydate)
                   VALUES('{}','{}','{}','{}')'''.format(corpcode, corpname, stockcode,modidate)
        sa.executes(insql)
