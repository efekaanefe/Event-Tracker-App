from tkinter import *
from tkcalendar import *
import sqlite3
from datetime import datetime

now = datetime.now()
year = int(now.strftime("%Y"))
month = int(now.strftime("%m"))
day = int(now.strftime("%d"))

root = Tk()
root.title("Event Tracker")

def add_data():
    event_title = entry_event_title.get()
    # date = entry_date.get()
    date = cal.get_date()


    con = sqlite3.connect("data.db")
    cur = con.cursor()

    # CREATE TABLE
    # cur.execute("""
    #     CREATE TABLE data (
    #         event_title text, 
    #         date text
    #         )
    # """)

    #INSERT DATA
    cur.execute(f"INSERT INTO data VALUES (?, ?)", (event_title, date))

    con.commit()
    con.close()

    show_data()

def show_data():
    global label_data
    con = sqlite3.connect("data.db")
    cur = con.cursor()

    cur.execute("SELECT rowid, * FROM data ORDER BY date")
    data = cur.fetchall()
    string_data = "ID - Event: Month/Day/Year\n"+"-"*42+"\n"
    data_exist = False
    for rowid, name, date in data:
        string_data += f"{rowid} - {name}: {date}\n"
        # print(name, date)

    string = string_data if len(data) != 0 else "There is no event"
    
    label_data.configure(text = string)
    

    con.commit()
    con.close()

def update_data():
    update_window = Toplevel(root)
    update_window.title("Update Event")

    con = sqlite3.connect("data.db")
    cur = con.cursor()

    id = entry_id.get()

    cur.execute("SELECT * FROM data WHERE rowid = ?", id)
    title, date = cur.fetchone()
    date = date.split("/")
    month, day, year  = int(date[0]), int(date[1]), int(date[2])+2000

    label_event_title = Label(update_window, text = "Event Title", font = ("Arial", 18))
    label_event_title.grid(row =  0, column =  0)
    entry_event_title = Entry(update_window, font = ("Arial", 18))
    entry_event_title.grid(row = 0, column = 1, ipadx = 25, padx = 10, pady=10)
    entry_event_title.delete(0, END)
    entry_event_title.insert(0,title)

    label_date = Label(update_window, text = "Date", font = ("Arial", 18))
    label_date.grid(row = 1, column = 0)
    cal = Calendar(update_window, selectmode="day", year = year, month = month, day = day) 
    cal.grid(row = 1, column = 1, pady = 10)

    

    con.commit()
    con.close()

    def save():
        con = sqlite3.connect("data.db")
        cur = con.cursor()

        new_title, new_date = entry_event_title.get(), cal.get_date()

        cur.execute("""
                    UPDATE data SET 
                    event_title = :new_title,
                    date = :new_date
                    WHERE rowid = :id""", 
                    {"new_title": new_title, "new_date":new_date, "id":id})
                    
        txt = f"New Title: {new_title}\nNew Date {new_date}\nSAVED"
        label_saved.configure(text = txt)
        
        con.commit()
        con.close()

    button_save = Button(update_window, text = "Save Changes", command = save)
    button_save.grid(row = 2, column = 0, columnspan=2, pady = 10)

    label_saved = Label(update_window, text = "", font = ("Arial", 18))
    label_saved.grid(row = 3, column = 0, columnspan=2)

    update_window.mainloop()

def delete_data():
    con = sqlite3.connect("data.db")
    cur = con.cursor()

    ids = entry_id.get()
    deleted_ids = ""
    if ids.lower() != "all":
        ids.split(",")
        for id in ids:
            deleted_ids+=id 
            deleted_ids+=", " if id != ids[-1] else ""
            cur.execute("DELETE FROM data WHERE rowid=?", id)
    else:
        deleted_ids = "ALL"
        cur.execute("DELETE FROM data")



    con.commit()
    con.close()

    #label_data.config(text = f"{deleted_ids} DELETED")
    # root.update()
    show_data()

#ADDING AND DISPLAYING DATA
label_event_title = Label(root, text = "Event Title", font = ("Arial", 18))
label_event_title.grid(row =  0, column =  0)
entry_event_title = Entry(root, font = ("Arial", 18))
entry_event_title.grid(row = 0, column = 1, ipadx = 25, padx = 10, pady=10)

label_date = Label(root, text = "Date", font = ("Arial", 18))
label_date.grid(row = 1, column = 0)
cal = Calendar(root, selectmode="day", year = year, month = month, day = day) 
cal.grid(row = 1, column = 1, pady = 10)

button_add_data = Button(root, text = "Add Data", command = add_data)
button_add_data.grid(row = 2, column = 0, columnspan=2, pady = 8)

button_show_data = Button(root, text = "Show Data", command = show_data)
button_show_data.grid(row = 3, column = 0, columnspan=2, pady = 8)

#MODIFYING DATA
label_id = Label(root, text = "Enter ID(s)", font=("Arial", 18))
label_id.grid(row = 4, column = 0)

entry_id = Entry(root, font = ("Arial", 18))
entry_id.grid(row = 4, column = 1, ipadx = 25)

button_update_data = Button(root, text = "Update Data", command = update_data)
button_update_data.grid(row = 5, column = 0, columnspan = 2, pady = 8)

button_delete_data = Button(root, text = "Delete Data", command = delete_data)
button_delete_data.grid(row = 6, column = 0, columnspan = 2, pady = 8)

label_data = Label(root, text="You can delete multiple or all events\n with typing 'all' in enter id(s) box at once\nBut update must be done seperately\nWaiting for your command...", font = ("arial", 20))
label_data.grid(row = 7, column = 0, columnspan = 2)

root.mainloop()
