from tkinter import *
import tkinter as tk
import tkinter.messagebox
from tkinter import messagebox
from PIL import ImageTk, Image
import random
import time
import datetime
import json
from todayDate import userTimehour, todayTime, todayDay, displayDate, userinputday_num, userinputdate
import todayDate
from datetime import datetime
import pprint


#Dictionary containing all the stores information such as Opening/Closing times & their respective menus
file = open("NorthSpineCompiled.json", "r")
data = json.load(file)
#Dictionary containing the individual store's window images 
file2 = open("menu_image.json", "r")
data2 = json.load(file2)

todayTime = int(todayTime())
todayDay = int(todayDay())


def main():
    root = Tk()
    app = ntuMain(root)  
    
########################################################################################################################################################        
# Done by Brandon Chen
# main window layout 
class ntuMain:
    def __init__(self, master):
        self.master = master
        self.master.title("NTU North Spine Food Court")
        self.master.geometry("500x600+0+100".format(self.master.winfo_screenwidth(), self.master.winfo_screenheight()))
        self.frame = Frame(self.master)
        
        # opens background image
        mina = Image.open('Welcome to North Spine Food Court.png')
        mina2 = mina.resize((500,600), Image.ANTIALIAS)
        self.background_image2 = ImageTk.PhotoImage(mina2)    
        self.background_label = Label(self.master, image=self.background_image2)
        self.background_label.place(x=0, y=0, relwidth=1, relheight=1)
        
        self.text2 = displayDate()
        self.time_label = Label(self.master, text = self.text2)
        self.time_label.place(x=0, y=0)

##        self.master.after(200, self.time_label)
        
        #--------------------------BUTTONS-----------------------------------------------------
        # standardize font for all buttons
        myFont = ('DidactGothic', 10, 'bold')
        
        # click to open today's stalls window
        self.btn_todayStalls = Button(self.master, text="View Today's Stalls", height = 2, width = 20, font = myFont, command = self.todayStalls_window)
        self.btn_todayStalls.place(relx=0.10, rely=0.6)
        
        # click to open other day's stalls window
        self.btn_otherdayStalls = Button(self.master, text="View Stalls by Date", height = 2, width = 20, font = myFont, command = self.otherdayStalls_window)
        self.btn_otherdayStalls.place(relx=0.5, rely=0.6)
        
        # click to close all windows
        self.close = Button(self.master, text="Close",command = self.close_window)
        self.close.place(relx=0.9, rely=0.9)
        
    
    # opens new window to view today's stalls
    def todayStalls_window(self):
        enteredTime, enteredDay = todayTime, todayDay # assign enteredTime and enteredDay to today's time and day 
        self.openWindow = Toplevel(self.master)
        self.app = display_stalls(self.openWindow, enteredTime, enteredDay) # runs today's time and day as argument into the class "display_stalls" and all the functions within
        
    # opens new window for user to input date/time    
    def otherdayStalls_window(self):
        self.openWindow = Toplevel(self.master)
        self = input_stalls(self.openWindow) # calls the class "input_stalls" that attributes enteredTime and enteredDay as user input date/time
    
    # closes all windows and applications    
    def close_window(self):
        exit()

########################################################################################################################################################
# checks enteredTime, enteredDay variable and display stalls opened as buttons (which opens new window to display respective stalls' menu when clicked upon)
class display_stalls:
    def __init__(self, master, enteredTime, enteredDay):
        self.master = master
        self.master.title("Stalls opened")
        self.master.geometry("500x600+500+100",)
        self.frame = Frame(self.master)
        self.frame.pack()
        
        # set background image. Resize picture to window size
        second_window = Image.open('Stalls that are open.png')
        second_window2 = second_window.resize((500,600), Image.ANTIALIAS)
        self.background_image2 = ImageTk.PhotoImage(second_window2)    
        self.background_label = Label(self.master, image=self.background_image2)
        self.background_label.place(x=0, y=0, relwidth=1, relheight=1)

        # returns stalls that are open based on enteredTime and enteredDay in a list
        stores_opened = self.get_stall_name(enteredTime,enteredDay)
        
        # displays buttons of stalls opened
        if len(stores_opened) == 0:
            messagebox.showinfo("Closed", "Sorry, all stalls have been closed")
            self.master.destroy()
        
        else:
            count = 0
            for storeNames in stores_opened:
                count += 1
                self.new_btn = Button(self.master, text=str(storeNames), height = 2, width = 20, command= lambda storeNames=storeNames: self.new_window(storeNames, enteredTime, enteredDay))
                self.new_btn.place(relx=0.35, rely=0.3+count*0.1)
    
    
    # Done by Jethro Phuah
    # return stalls opened in a list based on time and day
    def get_stall_name(self, time, day):
            if day == 0: # all stalls closed on a sunday
                messagebox.showinfo("Closed", "Sorry, all stalls have been closed")
                self.master.destroy()
                
            else:
                stall_names = []
                for key in data.keys(): # iterates the first level of keys 
                    if int(data[key]["Opening"]) <= time <= int(data[key]["Closing"]):# if todaytime is within opening and closing hours will print the available stalls 
                        stall_names.append(key)
                return stall_names
            
    
    # opens stall menu window when user clicks the button. Name of stall runs into class "display_menus" to call the respective stall image background
    def new_window(self, storeNames, enteredTime, enteredDay):
        openWindow = Toplevel(self.master)
        self.app = display_menus(openWindow, storeNames) # opens a new window for menu. run the name of selected stalls into the class "display_menus" as "keys"
        
        # Done by Jethro Phuah
        # returns selected stall's menu and and operating hours in a dictionary format
        def get_menu(store_name, time_general = 0, today_day = 0, year = 0, month = 0, date = 0):
            if year == 0 and month == 0 and date == 0:
                day = today_day
                time = time_general
            else:
                try:
                    day = userinputday_num(year, month, date)
                except:
                    return -1
                try:
                    time_2 = datetime.strptime(time_general, "%H:%M")
                    time = userTimehour(time_2)
                except:
                    return -2

            stall_menu_price = {}
            stall_operating_hours = {}
          
            if int(data[store_name]["Opening"]) <= time <= int(data[store_name]["Closing"]): # returns operating hours of the selected stalls in a list
                stall_operating_hours['Operating hours'] = [int(data[store_name]["Opening"]), int(data[store_name]["Closing"])]
                
                
            for key,value in data[store_name]["Menu"].items(): 
                if int(value[1]) <= time <= int(value[2]): # checks time is within the dish serving period 
                    if day != int(value[3]) and int(value[3]) != 7: # represent each day of the week with a number. 0 - Sun, 6 - Saturday and 7 - everyday. 
                        continue
                    stall_menu_price[key] = value[0]
            return stall_menu_price, stall_operating_hours # returns menu in a dictionary format
        
        menu_price, ops_hour = get_menu(storeNames, enteredTime, enteredDay) # returns menu and operating hours of selected stalls base on enteredTime and enteredDay
        
        # prints the menu into our menu window
        count = 0
        for key,value in menu_price.items():
            count += 1
            text_displayed = "{:<29}".format(key) + "$" + "{:.2f}".format(value)
            self.LabelTitle = Label(openWindow, text = text_displayed, font=('monaco', 12, 'bold'), bg = 'lavenderblush')  
            self.LabelTitle.place(relx=0.16, rely=0.40+count*0.07)
    
    
            
########################################################################################################################################################       
# stall menu window layout        
class display_menus:
    def __init__(self, master, key): #added an additional parameter "key" which is the selected store names
        self.master = master
        self.master.title("Menus")
        self.master.geometry("500x600+1000+100",)
        self.frame = Frame(self.master)
        self.frame.pack()
        
        # opens background image for the respective store 
        mina = Image.open(data2[key])
        mina2 = mina.resize((500,600), Image.ANTIALIAS)
        self.background_image2 = ImageTk.PhotoImage(mina2)    
        self.background_label = Label(self.master, image=self.background_image2)
        self.background_label.place(x=0, y=0, relwidth=1, relheight=1)

        # creates an entry box for user to key in
        self.limit_entry = input_stalls.limit_entry # calls out limit_entry function from the class input_stalls
        entryValue_time = StringVar()
        self.limit_entry(self,entryValue_time, 2) # restricts lenth of input number to 2
        self.entry_time = Entry(self.master, width=4, textvariable=entryValue_time)# creates an entry box for user to key in
        self.entry_time.place(relx=0.77, rely=0.84)
        
        #creates "check waiting time" button 
        self.btn_checkTime = Button(self.master, text="Check waiting time", height = 1, width = 15, command=self.calculate_waitingTime)
        self.btn_checkTime.place(relx=0.62, rely=0.95)
        
    
    # Done by Brandon Chen
    # calculates waiting time when user clicks button
    def calculate_waitingTime(self):
        try:
            ppl_number = int(self.entry_time.get()) # ensures number keyed in is a positive integer 
            if ppl_number < 0:
                raise NegativeError
            
            waiting_time_str = str(ppl_number * 5) + " mins"
            self.label_1 = Label(self.master, text=waiting_time_str)
            self.label_1.place(relx=0.75, rely=0.89)
        
        except:
            messagebox.showerror("Error","Please input a valid number of people!")


########################################################################################################################################################
# Done by Brandon Chen
# input user date and time window layout 
class input_stalls:
    def __init__(self, master):
        self.master = master
        self.master.title("Search by date")
        self.master.geometry("400x200+120+120",)
        self.frame = Frame(self.master)
        self.frame.pack()
        self.master.configure(background='white')
        mina = Image.open('input.gif')
        mina2 = mina.resize((400,200), Image.ANTIALIAS)
        self.background_image2 = ImageTk.PhotoImage(mina2)    
        self.background_label = Label(self.master, image=self.background_image2)
        self.background_label.place(x=0, y=0, relwidth=1, relheight=1)
        
        self.label_1 = Label(self.master, text='Date (DD/MM/YYYY): ')
        self.label_1.place(x=0,y=20)
        
        entryValue_day = StringVar() 
        self.limit_entry(entryValue_day, 2)
        self.entry_day = Entry(self.master, width=2, textvariable=entryValue_day)
        self.entry_day.place(x=150,y=20)
        self.label_2 = Label(self.master, text='/')
        self.label_2.place(x=180,y=20)
        
        entryValue_month = StringVar()
        self.limit_entry(entryValue_month, 2)
        self.entry_month = Entry(self.master, width=2, textvariable=entryValue_month)
        self.entry_month.place(x=198,y=20)
        self.label_3 = Label(self.master, text='/')
        self.label_3.place(x=230,y=20)
        
        entryValue_year = StringVar()
        self.limit_entry(entryValue_year, 4)
        self.entry_year = Entry(self.master, width=4, textvariable=entryValue_year)
        self.entry_year.place(x=250,y=20)
        
        
        self.label_4 = Label(self.master, text='Time (HH:MM): ')
        self.label_4.place(x=0,y=60)
        
        entryValue_hour = StringVar()
        self.limit_entry(entryValue_hour, 2)
        self.entry_hour = Entry(self.master, width=2, textvariable=entryValue_hour)
        self.entry_hour.place(x=150,y=60)
        self.label_3 = Label(self.master, text=':')
        self.label_3.place(x=180,y=60)
        
        entryValue_min = StringVar()
        self.limit_entry(entryValue_min, 2)
        self.entry_min = Entry(self.master, width=2, textvariable=entryValue_min)
        self.entry_min.place(x=198,y=60)
        
        self.close = Button(self.master, text="Search",command= self.search_results)
        self.close.place(relx=0.8, rely=0.8)
    
    # limits the entry in the box to a specific length
    def limit_entry(self, str_var,length):
            def callback(str_var):
                c = str_var.get()[0:length]
                str_var.set(c)
            str_var.trace("w", lambda name, index, mode, str_var=str_var: callback(str_var)) 
    
    # Done by Jethro Phuah
    # checks whether user input is valid and opens new window with stall's menu
    def search_results(self):
        try:
            year = int(self.entry_year.get())
            month = int(self.entry_month.get())
            date = int(self.entry_day.get())
           
            if year <= 2017 or year > 2020: # restrict to only years between 2018-2020
                raise YearError
            else:
                for i in todayDate.public_holiday: # check whether date input is a public holiday
                    if i == userinputdate(year, month, date):
                        raise PublicHolidayError
        
            userDay = userinputday_num(year, month, date) # returns day keyed in into a number

            time_1 = self.entry_hour.get() + ":" + self.entry_min.get()
            time_2 = datetime.strptime(time_1, "%H:%M")
            userTime = userTimehour(time_2) # returns the hour only

        except YearError:
            messagebox.showerror("Error", "Error message. Please key in within year 2018 to 2020.")
##            self.master.destroy()


        except PublicHolidayError:
            messagebox.showerror("Error","Sorry its a public holiday. Go home.")
##            self.master.destroy()
            

        except:
            self = tkinter.Tk()
            self.withdraw()
            messagebox.showerror("Error", "Error message. Please key in a valid input.")
##            self.master.destroy()

        
        enteredTime, enteredDay = userTime, userDay #enteredTime and enteredDay are attributed with user input values
        self.openWindow = Toplevel(self.master)
        self.app = display_stalls(self.openWindow, enteredTime, enteredDay)

# Done by Jethro Phuah
class YearError(Exception):
    pass

class PublicHolidayError(Exception):
    pass

class NegativeError(Exception):
    pass


# runs whole program
if __name__ == '__main__':
    main()
