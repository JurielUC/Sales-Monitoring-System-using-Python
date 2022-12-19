#sale monitoring system
#IMPORTS
from tkinter import *           #GUI/Tkinter
from tkinter import ttk         
import tkinter.messagebox
from tkinter import messagebox     #message box
import tkinter.font as font       #fonts
from PIL import ImageTk, Image     #image - to install, type 'pip install pillow' to window teerminal
import sqlite3                  #database
import random
import sys
import os
import stdDatabase_sms          #Database Module

#Front End
def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

#CLASSES - CL5J/Record/Help/About
class CL5J: #The main window
    def __init__(self, master):
        self.master = master
        self.master.title("HOME")
        self.master.geometry('1280x650+35+10')
        self.master.config(bg = 'black')
        self.master.resizable(0,0)
        #Exit Button Function
        def Exit():
            Exit = tkinter.messagebox.askyesno("Sales Monitoring System", "Do you want to exit?")
            if Exit > 0:
                root.destroy()
                return
        
        self.frameascv = LabelFrame(self.master, width=1100, bd=15, height=550, bg= 'white')
        self.frameascv.place(x = 85, y = 80)
        self.frame = LabelFrame(self.frameascv, text='Menu', font='Times 15 bold', width=250, height=500, bd=10, bg= 'blue')
        self.frame.place(x = 800, y = 10)
        
        framefortitle = Frame(root, bg="black", height=70)
        framefortitle.place(relwidth=1, anchor='nw')
        title = Label(root, text="CL5J Auto Supply", font = "QuickGear 40 bold", fg="blue", bg = "black", bd=2)
        title.pack(side='top')
        
        self.d = Canvas(self.frameascv, width=500, height=500, bg='white')
        self.d.place(x=150, y=8)
        
        self.img = ImageTk.PhotoImage(Image.open(r"CL5JLOGO.jpg"))
        self.d.create_image(1,1,image=self.img, anchor=NW)
        #========================================================FORM BUTTONS=====================================================
        #BUTTON TO OPEN RECORD CLASS/WINDOW
        self.btnrecord = Button(self.frame, text = "Sales Report", font='Coolveteca 12 bold', width = 21, height = 3, command = self.recordnew_window)
        self.btnrecord.place(x = 5, y = 1)
        #BUTTON TO OPEN HELP CLASS/WINDOW
        self.btnhelp = Button(self.frame, text = "Help", font='Coolveteca 12 bold', width = 21, height = 3, command = self.helpnew_window)
        self.btnhelp.place(x = 5, y = 80)
        #BUTTON TO OPEN ABOUT CLASS/WINDOW'
        self.btnabout = Button(self.frame, text = "About", font='Coolveteca 12 bold', width = 21, height = 3, command = self.aboutnew_window)
        self.btnabout.place(x = 5, y = 160)
        #BUTTON TO CLOSE THE WINDOW
        self.btnexit = Button(self.frame, text = "Exit", font='Coolveteca 12 bold underline', width = 21, height = 3, command = Exit)
        self.btnexit.place(x = 5, y = 240)
    #FUNCTION TO SHOW THE RECORD CLASS/WINDOW OR FUNCTION OF RECORD BUTTON
    def recordnew_window(self):
        warning = tkinter.messagebox.showwarning("Sales Monitoring System", "Take note that you can only save the file when you're done encoding the sales, to avoid lost of data! Once you saved the data the system will automatically shutdown.")
        self.RecordnewWindow = Toplevel(self.master)
        self.app = Record(self.RecordnewWindow)
    #FUNCTION TO SHOW THE HELP CLASS/WINDOW OR FUNCTION OF HELP BUTTON
    def helpnew_window(self):
        self.HelpnewWindow = Toplevel(self.master)
        self.app = Help(self.HelpnewWindow)
    #FUNCTION TO SHOW THE ABOUT CLASS/WINDOW OR FUNCTION OF ABOUT BUTTON
    def aboutnew_window(self):
        self.AboutnewWindow = Toplevel(self.master)
        self.app = About(self.AboutnewWindow)
        
class Record:
    def __init__(self,master):
        self.master = master
        self.master.title("SALES MONITORING SYSTEM")
        self.master.geometry('1280x650+35+10')
        self.master.config(bg = 'black')
        self.master.resizable(0,0)
        self.frame = Frame(self.master, bg= 'black')
        self.frame.pack() 
        
        self.framefortitle = Frame(self.master, bg="black")
        self.framefortitle.place(relwidth=1, relheight=0.09, anchor='nw')
        self.title = Label(self.master, text="SALES MONITORING SYSTEM", font = "Times 40 bold", fg="blue", bg="black")
        self.title.pack(side='top')
        
        #DATABASE/ENTRY VARIABLES
        QTY = StringVar()
        ITEM = StringVar()
        NETPRICE = DoubleVar()
        PRICE = DoubleVar()
        #=============================================FUNCTION for DATABASE and BUTTON COMMANDS============================================= 
        #Funtion to ADD data into SalesList
        def addData(): 
            try:
                if(len(ITEM.get())!=0):
                    stdDatabase_sms.addRec(QTY.get(), ITEM.get(), NETPRICE.get(), PRICE.get())
                    self.salesList.delete(0, END)
                    self.salesList.insert(END,(QTY.get(), ITEM.get(), NETPRICE.get(), PRICE.get()))
                self.qtyEntry.delete(0,END)
                self.itemEntry.delete(0,END)
                self.netpEntry.delete(0,END)
                self.priceEntry.delete(0,END) 
                self.totalnetPrice.delete(0, END)
                self.totalPrice.delete(0, END)
            except TclError:
                invalid = tkinter.messagebox.showerror("Ordering System", "Invalid Input! Please try again!")
                self.RecordnewWindow = Toplevel(self.master)
                self.app = Record(self.RecordnewWindow)
        #Function to Delete data from SalesList
        def DeleteData():
            if(len(ITEM.get())!=0):
                stdDatabase_sms.deleteRec(sd[0])
                clearData()
                DisplayData()
        #Funtion to Search data  
        def searchDatabase():
            self.salesList.delete(0, END)
            for rows in stdDatabase_sms.searchData(QTY.get(), ITEM.get()):
                self.salesList.insert(END, rows)
        #Function to get the total NetPrice
        def computenet():
            try:
                con = sqlite3.connect('sales.db')
                cur = con.cursor()
                cur.execute("SELECT SUM(NETPRICE) FROM sales")
                self.totalnetPrice.delete(0, END)
                self.totalnetPrice.insert(END, cur.fetchone()[0])
                con.close()
            except TclError:
                invalid = tkinter.messagebox.showerror("Ordering System", "No Prices to Total!")
                self.RecordnewWindow = Toplevel(self.master)
                self.app = Record(self.RecordnewWindow)
        #Function to get the total Price
        def computeprice():
            con = sqlite3.connect('sales.db')
            cur = con.cursor()
            cur.execute("SELECT SUM(PRICE) FROM sales")
            self.totalPrice.delete(0, END)
            self.totalPrice.insert(END, cur.fetchone()[0])
            con.close()
        #Function to Display data to SalesList
        def DisplayData():
            self.salesList.delete(0, END)
            for rows in stdDatabase_sms.viewData():
                self.salesList.insert(END, rows)
        #Function to remove text/inputs in entry widgets on Sales Monitoring Window
        def clearData():
            self.qtyEntry.delete(0,END)
            self.itemEntry.delete(0,END)
            self.netpEntry.delete(0,END)
            self.priceEntry.delete(0,END)
            self.totalnetPrice.delete(0, END)
            self.totalPrice.delete(0, END)
        #Function to Update the Items if you want to change it
        def update():
            if(len(ITEM.get())!=0):
                stdDatabase_sms.deleteRec(sd[0])
            if(len(ITEM.get())!=0):
                stdDatabase_sms.addRec(QTY.get(), ITEM.get(), NETPRICE.get(), PRICE.get())
                self.salesList.delete(0, END)
                self.salesList.insert(END,(QTY.get(), ITEM.get(), NETPRICE.get(), PRICE.get()))
        #Function to get the Analysis and place it into Saleslist Descending by its price
        def Analysis_Des():
            self.salesList.delete(0, END)
            for rows in stdDatabase_sms.Desc():
                self.salesList.insert(END, rows)
        #Function to get the Analysis and display it into Frame5
        def Analysis_Des2():
            for widget in self.frame5.winfo_children(): #It is used to clear the widgets on frame5
                widget.destroy() 
            analysis = Listbox(self.frame5, font ='Courier 12 bold', bg='white')
            analysis.place(x=1, y=1, relwidth=1, relheight=1)
            
            con = sqlite3.connect('sales.db')
            cur = con.cursor()
            cur.execute("SELECT * FROM sales ORDER BY PRICE DESC")
            analysis.insert(END, str("Highest Amount you've Sold Today: "), str(""), cur.fetchone())
            con.close()
        #Function of the widget(SalesList)
        def salesRec(event):
            global sd
            searchStd = self.salesList.curselection()[0]
            sd = self.salesList.get(searchStd)
            
            self.qtyEntry.delete(0,END)
            self.qtyEntry.insert(END, sd[1])
            self.itemEntry.delete(0,END)
            self.itemEntry.insert(END, sd[2])
            self.netpEntry.delete(0,END)
            self.netpEntry.insert(END, sd[3])
            self.priceEntry.delete(0,END)
            self.priceEntry.insert(END, sd[4])
        #Function to change the filename of the database(SQLite)
        def clicked():
            cfname = self.fnameEntry.get()
            os.rename("sales.db", cfname)
            self.master.destroy()
        #==============================================FRAMES==============================================
        #frames for buttons
        self.frame1 = Frame(self.master, bg="black")
        self.frame1.place(relwidth=0.3, relheight=0.1, relx=0.6, rely=0.78,  anchor='w')
        self.frame2 = Frame(self.master, bg="black")
        self.frame2.place(relwidth=0.3, relheight=0.1, relx=0.6, rely=0.88,  anchor='w')
        self.framecalcu = Frame(self.master, bg="black")
        self.framecalcu.place(relwidth=0.08, relheight=0.4, relx=0.9, rely=0.3, anchor='w')
        
        #frame for entry/label
        self.frame3 = Frame(self.master, bg="blue")
        self.frame3.place(relwidth=0.5, relheight=0.2, relx=0.06, rely=0.10)
        
        #frame for database/list of sale
        self.frame4 = LabelFrame(self.master, bg="white", text='List of Sale', bd = 10, font='Times 12 bold')
        self.frame4.place(relwidth=0.5, relheight=0.7, relx=0.06, rely=0.23)
        
        #frame for calculator/analysis
        self.frame5 = LabelFrame(self.master, height=390, bd=3, bg="white")
        self.frame5.place(relwidth=0.3, relx=0.6, rely=0.4,  anchor='w')
        #===========================================LABEL AND ENTRY======================================
        #FOR FILENAME
        self.fnameLbl = Label(self.frame3, text="FILENAME(*.db):", font='Courier 12 bold underline', bg='blue', fg='white')
        self.fnameLbl.place(x=1, y=10)
        self.fnameEntry = Entry(self.frame3, width=35, font='Courier 10', bd=3)
        self.fnameEntry.place(x=150, y=10)
        self.fnameButton = ttk.Button(self.frame3, text="Save", width=11, command = clicked)
        self.fnameButton.place(x=450, y=10)
        
        #FOR QUANTITY
        self.qtyLbl = Label(self.frame3, text="QTY.", font='Courier 12 bold', bg='blue', fg='white')
        self.qtyLbl.place(x=1, y=35)
        self.qtyEntry = Entry(self.frame3, width=10, font='Courier 10', bd=2, textvariable = QTY)
        self.qtyEntry.place(x=1, y=60)
        
        #FOR ITEM
        self.itemLbl = Label(self.frame3, text="ITEM", font='Courier 12 bold', bg='blue', fg='white')
        self.itemLbl.place(x=96, y=35)
        self.itemEntry = Entry(self.frame3, width=35, font='Courier 10', bd=2, textvariable = ITEM)
        self.itemEntry.place(x=96, y=60)
        
        #FOR NETPRICE
        self.netpLbl = Label(self.frame3, text="NET PRICE", font='Courier 12 bold', bg='blue', fg='white')
        self.netpLbl.place(x=390, y=35)
        self.netpEntry = Entry(self.frame3, width=14, font='Courier 10', bd=2, textvariable = NETPRICE)
        self.netpEntry.place(x=390, y=60)
        
        #FOR PRICE
        self.priceLbl = Label(self.frame3, text="PRICE", font='Courier 12 bold', bg='blue', fg='white')
        self.priceLbl.place(x=515, y=35)
        self.priceEntry = Entry(self.frame3, width=14, font='Courier 10', bd=2, textvariable = PRICE)
        self.priceEntry.place(x=515, y=60)
        
        #FOR TOTAL NETPRICE
        self.totalnetPriceLabel = Label(self.frame4, text="TOTAL NP:", font='Courier 12 bold', bg='white', fg='black')
        self.totalnetPriceLabel.place(x=35, y=390)
        self.totalnetPrice = Entry(self.frame4, width=10, font='Courier 12 bold', bg='white', bd=1, fg='black')
        self.totalnetPrice.place(x=130, y=390)
        
        #FOR TOTAL PRICE
        self.totalPriceLabel = Label(self.frame4, text="TOTAL P:", font='Courier 12 bold', bg='white', fg='black')
        self.totalPriceLabel.place(x=280, y=390)
        self.totalPrice = Entry(self.frame4, width=10, font='Courier 12 bold', bg='white', bd=1, fg='black')
        self.totalPrice.place(x=365, y=390)
        #===============================================buttons============================================
        #ADD ITEM BUTTON
        self.addButton = Button(self.frame1,font = ('helvetica',10, 'bold'), text="Add", height=3, width=11, fg="black", bg="lavender", command = addData)
        self.addButton.pack(side='left')

        #DELETE BUTTON
        self.delButton = Button(self.frame1,font = ('helvetica',10, 'bold'), text="Delete", height=3, width=11, fg="black", bg="lavender", command = DeleteData)
        self.delButton.pack(side='left')
        
        #TOTAL SALES BUTTON
        self.totButton = Button(self.frame1, font = ('helvetica',10, 'bold'),text="Total\nSales", height=3, width=11, fg="black", bg="lavender", command = lambda:[computenet(), computeprice()])
        self.totButton.pack(side='right')
        
        #SEARCH BUTTON
        self.searchButton = Button(self.frame1,font = ('helvetica',10, 'bold'), text="Search", height=3, width=11, fg="black", bg="lavender", command = searchDatabase)
        self.searchButton.pack(side='right')
        
        #DISPLAY BUTTON
        self.dispButton = Button(self.frame2,font = ('helvetica',10, 'bold'), text="Display", height=3, width=11, fg="black", bg="lavender", command = DisplayData)
        self.dispButton.pack(side='left')
        
        #CLEAR BUTTON
        self.clearButton = Button(self.frame2,font = ('helvetica',10, 'bold'), text="Clear", height=3, width=11, fg="black", bg="lavender", command = clearData)
        self.clearButton.pack(side='left')
        
        #ANALYSIS BUTTON
        self.analysisButton = Button(self.frame2,font = ('helvetica',10, 'bold'),text="Analysis", height=3, width=11, fg="black", bg="lavender", command = lambda:[Analysis_Des(), Analysis_Des2()])
        self.analysisButton.pack(side='right')
        
        #UPDATE BUTTON
        self.updButton = Button(self.frame2, font = ('helvetica',10, 'bold'),text="Update", height=3, width=11, fg="black", bg="lavender", command = update)
        self.updButton.pack(side='right')

        #CALCULATOR BUTTON
        self.calButton = Button(self.framecalcu, font = ('helvetica',10, 'bold') ,text="Calculator", height=3, width=11, fg="black", bg="lavender", command = self.CalculatorButtons)
        self.calButton.pack(side='top')
        self.operator = ""
        self.text_Input = StringVar()
        
        #INSTRUCTION BUTTON
        self.insButton = Button(self.framecalcu, font = ('helvetica',10, 'bold'), text="Help", height=3, width=11, fg="black", bg="lavender", command = self.helpnew_window)
        self.insButton.pack(side='top')
        
        #EXIT BUTTON
        self.exitButton = Button(self.framecalcu, font = ('helvetica',10, 'bold'), text="Back", height=3, width=11, fg="black", bg="red", command = self._close)
        self.exitButton.pack(side='top')
        #==============================================LISTBOX AND SCROLL BAR==============================
        #Listbox and Scrollbar that is used to display sold item from database(SQLite)
        self.scrollbar = Scrollbar(self.frame4)
        self.scrollbar.place(x=600, y=0, relheight=1)
        
        self.salesList = Listbox(self.frame4, font ='Courier 12 bold' , yscrollcommand=self.scrollbar.set)
        self.salesList.bind('<<ListboxSelect>>', salesRec)
        self.salesList.place(x=1, relwidth=0.8, relheight=0.8)
        self.scrollbar.config(command = self.salesList.yview)
    #========================================HELP FUNCTION============================================  
    #TO SHOW THE HELP WINDOW
    def helpnew_window(self):
        self.HelpnewWindow = Toplevel(self.master)
        self.app = Help(self.HelpnewWindow)
    #========================================EXIT FUNCTION============================================
    #TO EXIT THE CLASS WINDOW
    def _close(self):
        self.master.destroy()
    #========================================CALCULATOR FUNCTIONS======================================
    def btnClick(self, number):
        global operator
        self.operator = self.operator + str (number)
        self.text_Input.set(self.operator)

    def btnClearDisplay(self):
        global operator
        self.operator = ""
        self.text_Input.set("")

    def btnEqualsInput(self):
        global operator
        self.sumup= str(eval(self.operator))
        self.text_Input.set(self.sumup)
        operator = ""     

    def CalculatorButtons(self):
        for widget in self.frame5.winfo_children():
            widget.destroy()
        self.txtDisplay = Entry(self.frame5,font = ('Times', 20, 'bold'), textvariable = self.text_Input, bd = 20, insertwidth = 4, bg = "white", justify = 'right').grid(columnspan =4)
        self.btn7= Button (self.frame5,padx = 16, bd = 8, fg= "black", font = ('Times',20, 'bold'), text = "7", bg = "blue",command =lambda:self.btnClick("7")).grid(row = 1, column = 0) 
        self.btn8= Button (self.frame5,padx = 16, bd = 8, fg= "black", font = ('Times',20, 'bold'), text = "8", bg = "blue",command =lambda:self.btnClick("8")).grid(row = 1, column = 1) 
        self.btn9= Button (self.frame5,padx = 16, bd = 8, fg= "black", font = ('Times',20, 'bold'), text = "9", bg = "blue",command =lambda:self.btnClick("9")).grid(row = 1, column = 2) 
        self.Addition= Button (self.frame5,padx = 16, bd = 8, fg= "black", font = ('Times',20, 'bold'), text = "+", bg = "blue",command =lambda:self.btnClick("+")).grid(row = 1, column = 3) 
        #===============================================================================================================================================
        self.btn4= Button (self.frame5,padx = 16, bd = 8, fg= "black", font = ('Times',20, 'bold'), text = "4", bg = "blue",command =lambda:self.btnClick("4")).grid(row = 2, column = 0) 
        self.btn5= Button (self.frame5,padx = 16, bd = 8, fg= "black", font = ('Times',20, 'bold'), text = "5", bg = "blue",command =lambda:self.btnClick("5")).grid(row = 2, column = 1) 
        self.btn6= Button (self.frame5,padx = 16, bd = 8, fg= "black", font = ('Times',20, 'bold'), text = "6", bg = "blue",command =lambda:self.btnClick("6")).grid(row = 2, column = 2) 
        self.Subtraction= Button (self.frame5,padx = 19, bd = 8, fg= "black", font = ('Times',20, 'bold'), text = "-", bg = "blue",command =lambda:self.btnClick("-")).grid(row = 2, column = 3) 
        #===============================================================================================================================================
        self.btn1= Button (self.frame5,padx = 16, bd = 8, fg= "black", font = ('Times',20, 'bold'), text = "1", bg = "blue",command =lambda:self.btnClick("1")).grid(row = 3, column = 0) 
        self.btn2= Button (self.frame5,padx = 16, bd = 8, fg= "black", font = ('Times',20, 'bold'), text = "2", bg = "blue",command =lambda:self.btnClick("2")).grid(row = 3, column = 1) 
        self.btn3= Button (self.frame5,padx = 16, bd = 8, fg= "black", font = ('Times',20, 'bold'), text = "3", bg = "blue",command =lambda:self.btnClick("3")).grid(row = 3, column = 2) 
        self.Multiply= Button (self.frame5,padx = 16, bd = 8, fg= "black", font = ('Times',20, 'bold'), text = "x", bg = "blue",command =lambda:self.btnClick("*")).grid(row = 3, column = 3)
        #===============================================================================================================================================
        self.btn0= Button (self.frame5,padx = 16, pady = 10, bd = 8, fg= "black", font = ('arial',20, 'bold'), text = "0", bg = "blue",command =lambda:self.btnClick("0")).grid(row = 4, column = 0) 
        self.btnClear = Button (self.frame5,padx = 16, pady = 10, bd = 8, fg= "black", font = ('Times',20, 'bold'), text = "c", bg = "blue", command = self.btnClearDisplay).grid(row = 4, column = 1) 
        self.btnEquals = Button (self.frame5,padx = 16, pady = 10, bd = 8, fg= "black", font = ('Times',20, 'bold'), text = "=", bg = "blue", command = self.btnEqualsInput).grid(row = 4, column = 2) 
        self.Division= Button (self.frame5,padx = 19, pady = 10, bd = 8, fg= "black", font = ('Times',20, 'bold'), text = "/", bg = "blue",command =lambda:self.btnClick("/")).grid(row = 4, column = 3)
    
class Help:
    def __init__(self,master):
        self.master = master
        self.master.title("HELP")
        self.master.geometry('800x500+270+70')
        self.master.config(bg = 'blue')
        self.master.resizable(0,0)
        
        self.helpframe = LabelFrame(self.master, font='Times 15 bold', text='System Instruction', width=700, height=400, bd=10, fg='white', bg='black')
        self.helpframe.place(x=45, y=40)
        self.marklbl = Label(self.helpframe, font='times 200 bold', text='?', bg='black', fg='white')
        self.marklbl.place(x=50, y=1)
        #==========================================FUNCTIONS================================================
        #THESE FUNCTIONS CONTAINS USER GUIDE AND INSTRUCTIONS, IT HAS LABEL TO DISPLAY THE TEXT/INSTRUCTION
        def InstructionOne():
            for widget in self.HelpList.winfo_children():
                widget.destroy()
            one = Label(self.HelpList, text = "User Guide\n\nHome Window:\n==========================================\n➜There are 4 options; \
                                                       \n>>>SALES REPORT BUTTON - To open the \n   Sales Monitoring window. \
                                                       \n>>>HELP BUTTON - To see the System\n   Instruction. \
                                                       \n>>>ABOUT BUTTON - For system background. \
                                                       \n>>>EXIT BUTTON - To close the system.", font='Courier 12 bold', fg='white', bg='black', justify='left')
            one.place(x=1, y=1)
            
        def InstructionTwo():
            for widget in self.HelpList.winfo_children():
                widget.destroy()
            two = Label(self.HelpList, text = "User Guide\n\nSales Monitoring System Window: \
                                                        \n========================================== \
                                                        \nUSES OF BUTTONS: \
                                                        \n>>>ADD BUTTON - After entering the item\n   press[Add Button] to save it. \
                                                        \n>>>DELETE BUTTON - From list select an \n   item that you want to remove then\n   pressthe[Delete Button]. \
                                                        \n>>>SEARCH BUTTON - Enter the item you want\n   to get to the Textbox then\n   press[Search Button]. \
                                                        \n>>>TOTAL SALES BUTTON - Press this [Total\n   Sales Button] to display the total\n   sale income.", font='Courier 12 bold', fg='white', bg='black', justify='left')
            two.place(x=1, y=1)
            
        def InstructionThree():
            for widget in self.HelpList.winfo_children():
                widget.destroy()
            three = Label(self.HelpList, text = "User Guide\n\nSales Monitoring System Window: \
                                                        \n========================================== \
                                                        \nUSES OF BUTTONS: \
                                                        \n>>>DISPLAY BUTTON - To display the Sales\n   list press [Display Button]. \
                                                        \n>>>CLEAR BUTTON - To clear data on textbox\n   press [Clear Button]. \
                                                        \n>>>UPDATE BUTTON - To change an item from\n   mistake, select an item and change\n   it then press[Update Button]. \
                                                        \n>>>ANALYSIS BUTTON - To display the \n   analysis of the Sales press[Analysis\n   Button].", font='Courier 12 bold', fg='white', bg='black', justify='left')
            three.place(x=1, y=1)
            
        def InstructionFour():
            for widget in self.HelpList.winfo_children():
                widget.destroy()
            four = Label(self.HelpList, text = "User Guide\n\nSales Monitoring System Window: \
                                                        \n========================================== \
                                                        \nUSES OF BUTTONS: \
                                                        \n>>>CALCULATOR BUTTON - To display the \n   calculator press[Calculator Button]. \
                                                        \n>>>HELP BUTTON - To show the System \n   Instruction press[Help Button]. \
                                                        \n>>>BACK BUTTON - To go to home window\n   press[Back Button]. \
                                                        \nRemember: Do not press the [save button]\nor even save the filename when you're not\nyet done encoding to avoid lost of data. \
                                                        \nOnce you saved the data the system \nwill automatically shutdown.", font='Courier 12 bold', fg='white', bg='black', justify='left')
            four.place(x=1, y=1)
        #TO CLOSE THE WINDOW  
        def Exit():
            self.master.destroy()
        #WE USED THIS FRAME TO DISPLAY WIDGETS OF FUNCTION
        self.HelpList = Frame(self.helpframe, width=425, height=320, bg='black')
        self.HelpList.place(x=250, y=1)
        
        self.Instruc = Label(self.HelpList, text = "User Guide\n\nWELCOME SYSTEM ADMIN!!! \
                                                        \n========================================== \
                                                        \nDo you need help? \
                                                        \nPress the Buttons below. Thank you!", font='Courier 12 bold', fg='white', bg='black', justify='left')
        self.Instruc.place(x=1, y=1)
        #BUTTONS TO DISPLAY THE FUNCTION/INSTRUCTION
        self.btnOne = ttk.Button(self.helpframe, text = 'INS 1', command = InstructionOne)
        self.btnOne.place(x=250, y=330)

        self.btnTwo = ttk.Button(self.helpframe, text = 'INS 2', command = InstructionTwo)
        self.btnTwo.place(x=330, y=330)
        
        self.btnThree = ttk.Button(self.helpframe, text = 'INS 3', command = InstructionThree)
        self.btnThree.place(x=410, y=330)
        
        self.btnFour = ttk.Button(self.helpframe, text = 'INS 4', command = InstructionFour)
        self.btnFour.place(x=490, y=330)
        
        self.btnExit = ttk.Button(self.helpframe, text = 'EXIT', command = Exit)
        self.btnExit.place(x=570, y=330)
    
class About:   
    def __init__(self,master):
        self.master = master
        self.master.title("ABOUT")
        self.master.geometry('800x500+270+70')
        self.master.config(bg = 'blue')
        self.master.resizable(0,0)
        #TO CLOSED THE WINDOW
        def Exit():
            self.master.destroy()
        
        self.aboutframe = LabelFrame(self.master, font='Times 15 bold', text='About', width=700, height=400, bd=10, fg='white', bg='black')
        self.aboutframe.place(x=45, y=40)
        
        self.c = Canvas(self.aboutframe, width=300, height=350, bg='black')
        self.c.place(x=365, y=1)
        #IT IS USED TO DISPLAY IMAGE
        self.img = ImageTk.PhotoImage(Image.open(r"LOGO.jpg"))
        self.c.create_image(2,1,image=self.img, anchor=NW)
        
        self.aboutList = Frame(self.aboutframe, width=350, height=320, bg='black')
        self.aboutList.place(x=5, y=1)
        #THIS LABEL IS USED TO DISPLAY WHAT ABOUT THE PROGRAM
        self.About = Label(self.aboutList, text = "=================================================\nPROGRAMMER: \
                                                        \nJuriel U. Comia - System Design and Function \
                                                        \nGlydel Ann E. Reyes - System Design and Function \
                                                        \n================================================ \
                                                        \nDOCUMENTATION: \
                                                        \nGlydel Ann E. Reyes - Remaining Part of the paper. \
                                                        \nJuriel U. Comia - Methodology \
                                                        \n================================================ \
                                                        \nCourse: BSIT - 2107 / 1ST Semester \
                                                        \nProject Title: Sales Monitoring System \
                                                        \n\nSubmitted to: Ms. Richelle Sulit \
                                                        \n================================================ \
                                                        \n            BATANGAS STATE UNIVERSITY  \
                                                        \n================================================ \
                                                        \n               created with PYTHON", font='Courier 8 bold', fg='white', bg='black', justify='left')
        self.About.place(x=1, y=1)
        #BUTTON FOR EXIT FUNCTION
        self.btnExit = ttk.Button(self.aboutframe, text = 'EXIT', command = Exit)
        self.btnExit.place(x=10, y=320)
    
root = Tk()
app = CL5J(root) #Main Window
root.mainloop()