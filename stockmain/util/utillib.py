from datetime import datetime

# return : string '2020-03-01'
def gettoday():
    today = datetime.today().strftime("%Y-%m-%d")
    #print(today)
    return today

# start_date : string  '2020-03-01'
# end_date : string  '2020-03-04'
# return : int  : 3
def get_datediff(start_date, end_date):
    print ( start_date)
    print(end_date)
    betday = datetime.strptime(end_date,"%Y-%m-%d").date() - datetime.strptime(start_date,"%Y-%m-%d").date()
    return betday.days

if __name__ == "__main__":
    print(gettoday() )
    betday = get_datediff( '2020-03-27' , gettoday() )
    print( betday )