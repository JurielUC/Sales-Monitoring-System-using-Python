#Sales Monitoring System database code/function
import sqlite3

#Back End

def salesData():
    con=sqlite3.connect("sales.db") #database name
    cur=con.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS sales(id INTEGER PRIMARY KEY, QTY text, ITEM text, NETPRICE REAL, PRICE REAL)") #database table
    con.commit()
    con.close()
    
def addRec(QTY, ITEM, NETPRICE, PRICE):
    con=sqlite3.connect("sales.db")
    cur=con.cursor()
    cur.execute("INSERT INTO sales VALUES(NULL, ?,?,?,?)",(QTY, ITEM, NETPRICE, PRICE))
    con.commit()
    con.close()
    
def viewData():
    con=sqlite3.connect("sales.db")
    cur=con.cursor()
    cur.execute("SELECT * FROM sales")
    rows = cur.fetchall()
    con.close()
    return rows
    
def deleteRec(id):
    con=sqlite3.connect("sales.db")
    cur=con.cursor()
    cur.execute("DELETE FROM sales WHERE id=?", (id,))
    con.commit()
    con.close

def searchData(QTY="", ITEM=""):
    con=sqlite3.connect("sales.db")
    cur=con.cursor()
    cur.execute("SELECT * FROM sales WHERE QTY=? OR ITEM=?", (QTY, ITEM))
    rows = cur.fetchall()
    con.close()
    return rows
    
def dataUpdate(id, QTY="", ITEM="", NETPRICE="", PRICE=""):
    con=sqlite3.connect("sales.db")
    cur=con.cursor()
    cur.execute("UPDATE sales SET QTY=?, ITEM=?, NETPRICE=?, PRICE=?", (QTY, ITEM, NETPRICE, PRICE, id))
    con.commit()
    con.close()
    
def Desc():
    con = sqlite3.connect('sales.db')
    cur = con.cursor()
    cur.execute("SELECT * FROM sales ORDER BY PRICE DESC")
    rows = cur.fetchall()
    con.close()
    return rows
       
salesData()