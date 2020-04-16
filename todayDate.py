# list of public holidays from 2019-2020
public_holiday = ["01/01/19", "02/05/19", "02/06/19", "04/19/19", "05/01/19", "05/19/19", "05/20/19", "06/04/19", "06/05/19", "08/09/19", "08/11/19", "08/12/19", "10/28/19", "12/25/19", "01/01/2020", "02/25/2020","02/28/2020","04/10/2020","05/01/2020","05/07/2020","05/23/2020","05/24/2020","07/30/2020","07/31/2020","08/10/2020","11/14/2020","12/25/2020"]


# display date in required format
def displayDate():
    from datetime import datetime
    todayDate = datetime.now()
    display_date = todayDate.strftime("%A, %m %B %x, %X %p")
    return display_date


# returns today time in hour only
def todayTime():
    from datetime import datetime
    todayDate = datetime.now()
    todayTime = todayDate.strftime("%H")
    return todayTime

#returns today day in numerical format
def todayDay():
    from datetime import datetime
    todayDate = datetime.now()
    todayDay = todayDate.strftime("%w")
    return todayDay
    
# returns user input date in month/day/year
def userinputdate(year, month, date):
    from datetime import datetime
    x = datetime(year, month, date)
    y = x.strftime("%x")
    return y 
  
# returns user input day into a numerical number (0 rep Sunday and 6 represent Saturday)
def userinputday_num(year, month, date):
    from datetime import datetime
    x = datetime(year, month, date)
    z = x.strftime("%w")
    return int(z)
    
# returns user input time into hour only(0 rep Sunday and 6 represent Saturday)   
def userTimehour(time_2):
    from datetime import datetime
    userTime_input = str(time_2).split()#splits time into 2 elements 
    userTime_hour = int(userTime_input[1][:2])#takes the hour only 
    return userTime_hour



 
