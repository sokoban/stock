create table dailystock
(
comcode int NOT NULL
, date datetime NOT NULL
, close bigint
, diff bigint
, open bigint
, high bigint
, low bigint
, volume bigint
);
ALTER TABLE dailystock ADD PRIMARY KEY (`comcode`, `date`);

CREATE TABLE corplist (
RegDT datetime
, name varchar(100)
, code int
, kind varchar(50)
, product varchar(100)
, regdate varchar(30)
, endmonth varchar(30)
, owner varchar(30)
, homepage varchar(200)
, region varchar(30)
, updateflag int DEFAULT 0
);

CREATE TABLE dart_finreport (
RegDT datetime
, id int
, rcept_no varchar(20)
, reprt_code int
, bsns_year int
, corp_code varchar(15)
, stock_code varchar(10)
, fs_div varchar(10)
, fs_nm varchar(20)
, sj_div varchar(5)
, sj_nm varchar(15)
, account_id varchar(30)
, account_nm varchar(30)
, account_detail varchar(30)
, thstrm_nm varchar(15)
, thstrm_dt varchar(25)
, thstrm_amount bigint
, frmtrm_nm varchar(15)
, frmtrm_dt varchar(25)
, frmtrm_amount bigint
, bfefrmtrm_nm varchar(15)
, bfefrmtrm_dt varchar(25)
, bfefrmtrm_amount bigint
, ord int
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


