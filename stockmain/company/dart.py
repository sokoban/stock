import pandas as pd
import sys, os
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from DBConn import sqldata

import requests

'''
DART OPEN API search

https://opendart.fss.or.kr/api/fnlttSinglAcntAll.json?crtfc_key=&corp_code= &bsns_year=2018&reprt_code=11011&fs_div=OFS

API key : 2ed06d7648ff205ef6e47bfb4f992a5d9d818ee5
crtfc_key
corp_code
bsns_year=2019
reprt_code=11014
'00260985
00401111
1분기보고서 : 11013
반기보고서 : 11012
3분기보고서 : 11014
사업보고서 : 11011
https://opendart.fss.or.kr/api/fnlttSinglAcnt.json?crtfc_key=2ed06d7648ff205ef6e47bfb4f992a5d9d818ee5&corp_code=00356370&bsns_year=2018&reprt_code=11011
https://opendart.fss.or.kr/api/fnlttSinglAcnt.json?crtfc_key=2ed06d7648ff205ef6e47bfb4f992a5d9d818ee5&corp_code=00414416&bsns_year=2019&reprt_code=11011
https://opendart.fss.or.kr/api/fnlttMultiAcnt.json?crtfc_key=2ed06d7648ff205ef6e47bfb4f992a5d9d818ee5&corp_code=00414416&bsns_year=2019&reprt_code=11011
https://opendart.fss.or.kr/api/corpCode.xml?crtfc_key=2ed06d7648ff205ef6e47bfb4f992a5d9d818ee5
https://opendart.fss.or.kr/api/fnlttMultiAcnt.json?crtfc_key=2ed06d7648ff205ef6e47bfb4f992a5d9d818ee5&corp_code=00414416&bsns_year=2019&reprt_code=11014

https://opendart.fss.or.kr/api/list.json?crtfc_key=2ed06d7648ff205ef6e47bfb4f992a5d9d818ee5&corp_code=068270&bgn_de=20191010&end_de=20200310
https://opendart.fss.or.kr/api/company.json?crtfc_key=2ed06d7648ff205ef6e47bfb4f992a5d9d818ee5&corp_code=06827
'''


if __name__ == "__main__":

    sa = sqldata.getInstance()
    apikey = '2ed06d7648ff205ef6e47bfb4f992a5d9d818ee5'
    corpcode = '00356370'
    bsnsyear = '2019'

    selsql = '''SELECT corp_code , corp_name, stock_code FROM corpfnlist where stock_code <> "" and getflag = 0 '''
    ret = sa.executes(selsql)

    dtcol = [ 'rcept_no','reprt_code','bsns_year','corp_code','stock_code','fs_div'
            ,'fs_nm','sj_div','sj_nm','account_nm','thstrm_nm','thstrm_dt','thstrm_amount','frmtrm_nm'
            ,'frmtrm_dt','frmtrm_amount','bfefrmtrm_nm','bfefrmtrm_dt','bfefrmtrm_amount','ord']

    for i in ret:
        print(i)
        corp_code = str(i['corp_code'])
        corp_name = str(i['corp_name'])
        stock_code = str(i['stock_code'])
        print(corp_code, corp_name,stock_code )

        #darturl = 'https://opendart.fss.or.kr/api/fnlttSinglAcntAll.json?crtfc_key={}&corp_code={}&bsns_year={}&reprt_code=11011&fs_div=OFS'.format(apikey,corp_code,bsnsyear)
        darturl = 'https://opendart.fss.or.kr/api/fnlttSinglAcnt.json?crtfc_key={}&corp_code={}&bsns_year={}&reprt_code=11011'.format(apikey,corp_code,bsnsyear)
        print(darturl)

        try:
            ret = requests.get(darturl).json()

            if ret['status'] == '000':
                print('Data Get Success')
                df = pd.DataFrame.from_dict(ret['list'])

                for i, row in df.iterrows():
                    #for key, value in row.iteritems():
                    #    print(key, value)

                    for ditrow in dtcol:
                        if ditrow not in row:
                            row[ditrow] = '-'

                    insql = '''INSERT INTO dart_finreport(RegDT
                            ,rcept_no,reprt_code,bsns_year,corp_code
                            ,stock_code,fs_div,fs_nm,sj_div,sj_nm
                            ,account_nm,thstrm_nm,thstrm_dt
                            ,thstrm_amount,frmtrm_nm,frmtrm_dt
                            ,frmtrm_amount,bfefrmtrm_nm,bfefrmtrm_dt,bfefrmtrm_amount
                            ,ord
                            ) VALUES( NOW(),'{}',{},{},'{}','{}'
                               ,'{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}',{}) '''.format(
                            row['rcept_no']
                            ,row['reprt_code']
                            ,row['bsns_year']
                            ,row['corp_code']
                            ,row['stock_code']
                            ,row['fs_div']
                            ,row['fs_nm']
                            ,row['sj_div']
                            ,row['sj_nm']
                            ,row['account_nm']
                            ,row['thstrm_nm']
                            ,row['thstrm_dt']
                            ,row['thstrm_amount']
                            ,row['frmtrm_nm']
                            ,row['frmtrm_dt']
                            ,row['frmtrm_amount']
                            ,row['bfefrmtrm_nm']
                            ,row['bfefrmtrm_dt']
                            ,row['bfefrmtrm_amount']
                            ,row['ord'] )
                    sa.executes(insql)
                print(df)

                upsql = '''UPDATE corpfnlist SET getflag = {} , ErrMsg = '{}' WHERE corp_code = '{}' '''.format( '1', ret['message'], corp_code)
                print(upsql)
                sa.executes(upsql)
            else:
                print (ret['status'] , ret['message'])
                print ('Data Get Error')
                upsql = '''UPDATE corpfnlist SET getflag = {} , ErrMsg = '{}' WHERE corp_code = '{}' '''.format( ret['status'], ret['message'], corp_code)
                print(upsql)
                sa.executes(upsql)

        except Exception as e:
            print('Error {}'.format(e))
            exit(1)
            #exit(0)


    #Get Database instance
    #sa = sqldata.getInstance()
    #csql = '''select ab.comcode,bc.name ,count(*) from dailystock ab inner join corplist bc on ab.comcode = bc.code group by ab.comcode, bc.name'''
    #ret1 = sa.executes(csql)

    #print(ret1[0])

