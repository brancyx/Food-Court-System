# Done by Wang Liang Yi

import unittest
from datetime import datetime
from todayDate import displayDate, todayTime, todayDay, userinputdate, userinputday_num, userTimehour, userTimedisplay

data = {"Chicken rice": {"Opening": 8, "Closing": 18, "Menu": {"Roasted Chicken Rice": [3.00,8,18,7], "Curry Chicken Noodle": [3.00,8,18,2], "Thai Style Beancurd": [2.00,8,11,7]}}}

'''Functions to be tested'''           
def get_stalls(time, day):#return stalls base on user input time/todayTime
    if day == 0:
        print("Sorry all stalls are closed")
    else:
        stall_names = []
        for key in data.keys():
            if int(data[key]["Opening"]) <= time < int(data[key]["Closing"]):#if todaytime is within opening and closing hours will print the available stalls 
                stall_names.append(key)
        return stall_names            

def get_menus(store_name, time_general = 0, today_day = 0, year = 0, month = 0, date = 0):
    if year == 0 and month == 0 and date == 0:
        day = today_day
        time = time_general
    else:
        try:
            day = userinputday_num(year, month, date)
        except:
            return -1
        try:
            time_2 = datetime.strptime(time_general, "%H:%M:%S")
            time = userTimehour(time_2)
        except:
            return -2

    stall_menu_price = {}
    stall_operating_hours = {}

    if int(data[store_name]["Opening"]) <= time <= int(data[store_name]["Closing"]): #returns opening and closing hours of the individual stall
        stall_operating_hours['Operating hours'] = [int(data[store_name]["Opening"]), int(data[store_name]["Closing"])]
        
    for key,value in data[store_name]["Menu"].items(): #data[store_name]["Menu"] calls out the menu keys and values
        if int(value[1]) <= time <= int(value[2]):
            if day != int(value[3]) and int(value[3]) != 7:
                continue
            stall_menu_price[key] = value[0]
    return stall_menu_price, stall_operating_hours #returns menu in a dictionary format

# calculates waiting time when user clicks button
def calculate_waitingTime(self):
    try:
        ppl_number = int(self)
        if ppl_number < 0:
            raise NegativeError
        
        return ppl_number * 5
    except:
        return -1

'''Test Cases'''
class User_Input_Test_Case(unittest.TestCase):
    
    # if all input is valid
    def test_valid_input(self):
        result = (get_menus("Chicken rice", time_general = '09:10:10', today_day = 0, year = 2019, month = 11, date = 11))
        self.assertEqual(result, ({'Roasted Chicken Rice': 3.0, 'Thai Style Beancurd': 2.0}, {'Operating hours': [8, 18]}))
        
    # if day is invalid
    def test_invalid_day(self):
        result = (get_menus("Chicken rice", time_general = '09:10:10', today_day = 0, year = 'a', month = 11, date = 11))
        self.assertEqual(result, -1)
        
    # if time is invalid
    def test_invalid_time(self):
        result = (get_menus("Chicken rice", time_general = 'b', today_day = 0, year = 2019, month = 11, date = 11))
        self.assertEqual(result, -2)
        
class Open_Stores_Test_Case(unittest.TestCase):
    
    # when time is before opening time eg 4am
    def test_invalid_operating_hour_before_opening(self):
        result = get_stalls(4, 3)
        self.assertEqual(result, [])    

    # when time is after closing time eg 11pm
    def test_invalid_operating_hour_after_closing(self):
        result = get_stalls(22, 3)
        self.assertEqual(result, [])

    # when time is at closing time eg 8pm
    def test_invalid_operating_hour_at_closing(self):
        result = get_stalls(18, 3)
        self.assertEqual(result, [])
        
    # when time is at opening time eg 8am
    def test_valid_operating_hour_at_opening(self):
        result = get_stalls(8, 3)
        self.assertEqual(result, ["Chicken rice"])

    # when time is with opening and closing time eg 12pm
    def test_valid_operating_hour_after_opening_before_closing(self):
        result = get_stalls(12, 3)
        self.assertEqual(result, ["Chicken rice"])

class Menus_Test_Case(unittest.TestCase):
    
    # when time is during breakfast time eg 9am
    def test_breakfast_menu(self):
        result = (get_menus("Chicken rice", time_general = '09:10:10', today_day = 0, year = 2019, month = 11, date = 11))
        self.assertEqual(result, ({'Roasted Chicken Rice': 3.0, 'Thai Style Beancurd': 2.0}, {'Operating hours': [8, 18]}))    

    # when time is after breakfast time eg 4pm
    def test_after_breakfast_menu(self):
        result = (get_menus("Chicken rice", time_general = '16:10:10', today_day = 0, year = 2019, month = 11, date = 11))
        self.assertEqual(result, ({'Roasted Chicken Rice': 3.0}, {'Operating hours': [8, 18]}))

    # when day has a special menu eg Tuesday
    def test_special_day_menu(self):
        result = (get_menus("Chicken rice", time_general = '16:10:10', today_day = 2, year = 2019, month = 11, date = 12))
        self.assertEqual(result, ({'Roasted Chicken Rice': 3.0, "Curry Chicken Noodle": 3.0}, {'Operating hours': [8, 18]}))
        
    # when day does not have a special menu eg Thursday
    def test_valid_operating_hour_at_opening(self):
        result = (get_menus("Chicken rice", time_general = '09:10:10', today_day = 0, year = 2019, month = 11, date = 11))
        self.assertEqual(result, ({'Roasted Chicken Rice': 3.0, 'Thai Style Beancurd': 2.0}, {'Operating hours': [8, 18]}))

class Calculate_Wait_Time_Test_Case(unittest.TestCase):
    
    # if input is an integer
    def test_valid_integer(self):
        result = calculate_waitingTime(2)
        self.assertEqual(result, 10)

    # if input is anything else
    def test_invalid_input(self):
        result = calculate_waitingTime('a')
        self.assertEqual(result, -1)


''' Starts the test suite, will only run those functions that start with test_'''
if __name__ == "__main__":
     unittest.main()        
