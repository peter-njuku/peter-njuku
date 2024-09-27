import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import pymysql

class hostel():
    def __init__(self,root):
        self.root = root
        self.root.title("Hostel Accommodation")
        
        icon = tk.PhotoImage(file = "hostel.png")
        self.root.iconphoto(True, icon)      
        
        
        self.width = self.root.winfo_screenwidth() 
        self.height = self.root.winfo_screenheight()
        self.root.geometry(f'{self.width }x{self.height - 20}+0+0')
        
        titlelbl = tk.Label(self.root, text="Hostel Accomodation System", bg="Red", fg="White", border=4, relief="groove",font=("Consolas", 50, "bold"))
        titlelbl.pack(side="top", fill="x")
        
        #Input Frame
        
        inframe = tk.Frame(self.root, bg="light green", bd=4,relief="ridge")
        inframe.place(width=(self.width / 3), height=self.height - 180, x=50, y=100)
        
        tlabel = tk.Label(inframe, bg="light green", fg="Blue", font=("Consolas", 20,"bold"), text="Personal information")
        tlabel.grid(row=0,column=0,columnspan=2 )
        
        rnlabel = tk.Label(inframe, bg="light green", fg="Black", font=("Consolas", 15), text="RollNo")
        rnlabel.grid(row=1, column=0, padx=20,pady= 40)        
        self.rnIn = tk.Entry(inframe, bd=2, width=20, font=("Consolas", 15,"bold"))
        self.rnIn.grid(row=1, column=1, padx=20, pady=40)
        
        namelbl = tk.Label(inframe,bg="light green", fg="Black", font=("Consolas", 15), text="Name")
        namelbl.grid(row=2, column=0, padx=20, pady=30)
        self.nameIn = tk.Entry(inframe, bd=2, width=20, font=("Consolas", 15,"bold"))
        self.nameIn.grid(row=2, column=1, padx=20, pady=30)
        
        classlbl = tk.Label(inframe,bg="light green", fg="Black", font=("Consolas", 15), text="Class")
        classlbl.grid(row=3, column=0, padx=20, pady=30)
        self.classIn = tk.Entry(inframe, bd=2, width=20, font=("Consolas", 15,"bold"))
        self.classIn.grid(row=3, column=1, padx=20, pady=30)
        
        
        fnamelbl = tk.Label(inframe,bg="light green", fg="Black", font=("Consolas", 15), text="Surname")
        fnamelbl.grid(row=4, column=0, padx=20, pady=30)
        self.fnameIn = tk.Entry(inframe, bd=2, width=20, font=("Consolas", 15,"bold"))
        self.fnameIn.grid(row=4, column=1, padx=20, pady=30)
        
        okbtn = tk.Button(inframe, bd=3, relief="raised", text="Submit",  width=20, font=("Consolas", 20, "bold"), command=self.reservefun)
        okbtn.grid(row=5, column=0, columnspan=2, padx=40 , pady=30)
        
        #Output Frame
        
        self.outframe = tk.Frame(self.root, bg="light pink", bd=4, relief="ridge")
        self.outframe.place(width=self.width /2 , height=self.height - 180, x=self.width/3+100, y=100)
        self.tabfunc()
        
        
    def tabfunc(self):
        tabframe = tk.Frame(self.outframe, bg="sky blue", bd=3, relief="sunken")
        tabframe.place(x=40, y=30,width=(self.width /2)-80, height=self.height - 260)
        
        x_scroll = tk.Scrollbar(tabframe, orient="horizontal")
        x_scroll.pack(side='bottom', fill="x")
        
        y_scroll = tk.Scrollbar(tabframe,orient='vertical')
        y_scroll.pack(side="right", fill='y')
        
        self.table = ttk.Treeview(tabframe, columns=("RollNo", "Name", "Class", "Fname"), xscrollcommand=x_scroll.set, yscrollcommand=y_scroll.set)
        
        x_scroll.config(command=self.table.xview)
        y_scroll.config(command=self.table.yview)
        
        self.table.heading("RollNo", text="Roll_No")
        self.table.heading("Name", text="Name")
        self.table.heading("Class", text="Class")
        self.table.heading("Fname", text="Father_Name")
        self.table["show"] = "headings"
        
        self.table.column("RollNo", width=100)
        self.table.column("Name", width=100)
        self.table.column("Class", width=150)
        self.table.column("Fname", width=150)
        
        self.table.pack(fill="both", expand=1)
        
    def reservefun(self):
        try:        
            rn = int(self.rnIn.get())
            name = self.nameIn.get()
            class_ = self.classIn.get()
            fname = self.fnameIn.get()
           
            con = pymysql.connect(host= "localhost", user="root", password="pE25+tERNjuku", database="hostel_management_system")
            cur = con.cursor()
        
            if rn and name and class_ and fname:
                cur.execute("select room_id, available_beds from rooms where available_beds > 0 limit 1")
                room_data = cur.fetchone()
                
                if room_data:
                    room_id = room_data[0]
                    available_beds = room_data[1]
                    cur.execute("Insert into hostel(roll_no, name_,class,fname) values(%s,%s,%s,%s)", (rn,name,class_,fname))   
                    con.commit()
                    
                    if available_beds > 0:
                        new_available_beds = available_beds - 1
                        cur.execute("update rooms set available_beds = %s where room_id = %s", (new_available_beds,room_id))
                        con.commit()
                
                    tk.messagebox.showinfo("Success", f'Bed No. {4-new_available_beds} reserved in room No. {room_id}')
                    cur.execute("select * from hostel")
                    data =cur.fetchall()
              
                    self.table.delete(*self.table.get_children())
              
                    for i in data:
                        self.table.insert('',tk.END,values=i)
                    
                else:
                    tk.messagebox.showerror("Error", "All rooms reserved")
            else:
                tk.messagebox.showerror("Error", "Please input all fields")
        except ValueError:
                    tk.messagebox.showerror("Error", "Roll number must be an integer")
        #except Exception as e:
        #    tk.messagebox.showerror("Error", f"An error occurred: {str(e)}")
        finally:
            cur.close()
            con.close()
                
        
        
root = tk.Tk()
obj = hostel(root)
root.mainloop()