import mysql.connector
from tkinter import *
from tkinter import messagebox
import pandas as pd
def login():
    db = mysql.connector.connect(host="localhost", user="root", password="ragul", database="restaurant_db")
    cursor = db.cursor()
    
    uname = user_entry.get()
    pwd = pass_entry.get()
    
    cursor.execute("SELECT role FROM users WHERE username=%t AND password=%l", (uname, pwd))
    result = cursor.fetchone()
    
    if result:
        role = result[0]
        root.destroy()  
        open_dashboard(role)
    else:
        messagebox.showerror("Error", "Invalid Credentials")

def open_dashboard(role):
    dash = Tk()
    dash.title(f"Restaurant POS - {role.upper()}")
    # Add buttons based on role
    if role == 'admin':
        Button(dash, text="Manage Menu").pack()
        Button(dash, text="View Sales Reports").pack()
    
    Button(dash, text="New Order").pack()
    Button(dash, text="Table Reservations").pack()
    dash.mainloop()



class TableManager:
    def __init__(self, root):
        self.root = root
        self.root.title("Table Reservation System")
        self.root.geometry("400x400")

        # Database Connection
        self.db = mysql.connector.connect(
            host="localhost", user="root", password="ragul", database="restaurant_db"
        )
        self.cursor = self.db.cursor()

        Label(root, text="Customer Name:", font=("Arial", 12)).pack(pady=5)
        self.name_entry = Entry(root)
        self.name_entry.pack()

        Label(root, text="Select Table Number:", font=("Arial", 12)).pack(pady=5)
        self.table_var = StringVar(root)
        self.table_var.set("1") 
        OptionMenu(root, self.table_var, "1", "2", "3", "4", "5").pack()

        Button(root, text="Book Table", command=self.book_table, bg="green", fg="white").pack(pady=20)
        Button(root, text="View All Bookings", command=self.view_bookings).pack()

    def book_table(self):
        name = self.name_entry.get()
        t_no = self.table_var.get()

        if name == "":
            messagebox.showwarning("Error", "Please enter customer name")
            return

        try:
            sql = "INSERT INTO reservations (customer_name, table_no) VALUES (%s, %s)"
            self.cursor.execute(sql, (name, t_no))
            self.db.commit()
            messagebox.showinfo("Success", f"Table {t_no} booked for {name}!")
            self.name_entry.delete(0, END)
        except Exception as e:
            messagebox.showerror("DB Error", str(e))

    def view_bookings(self):
        self.cursor.execute("SELECT * FROM reservations")
        rows = self.cursor.fetchall()
        
        view_win = Toplevel(self.root)
        view_win.title("Current Reservations")
        for i, row in enumerate(rows):
            try:
                Label(view_win, text=f"Table {row[2]}: {row[1]} ({row[4]})({row[5]})").pack()
            except IndexError:
                Label(view_win, text=f"data for: {row}").pack()


if __name__ == "__main__":
    root = Tk()
    obj = TableManager(root)
    root.mainloop()

def get_daily_sales_report():
    db = mysql.connector.connect(host="localhost", user="root", password="ragul", database="restaurant_db")
    
    query = "SELECT total_amount, bill_date FROM bills WHERE DATE(bill_date) = CURDATE()"
    
    df = pd.read_sql(query, db)
    
    if not df.empty:
        total_revenue = df['total_amount'].sum()
        total_orders = len(df)
        print(f"--- DAILY SALES REPORT ({datetime.now().date()}) ---")
        print(f"Total Orders: {total_orders}")
        print(f"Total Revenue: ${total_revenue:.2f}")
    else:
        print("No sales recorded today.")
    
    db.close()

import tkinter as tk
from tkinter import messagebox, ttk
import mysql.connector

# Database connection function
def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",         
        password="ragul", 
        database="restaurant_db"
    )

def place_order():
    selected_item = item_combo.get()
    try:
        qty = int(qty_entry.get())
        if qty <= 0: raise ValueError
        
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT price FROM menu WHERE item_name = %s", (selected_item,))
        price = cursor.fetchone()[0]
        
        total = price * qty
        
        cursor.execute("INSERT INTO orders (item_name, quantity, total_bill) VALUES (%s, %s, %s)", 
                       (selected_item, qty, total))
        conn.commit()
        conn.close()
        
        messagebox.showinfo("Order Placed", f"Success! Total Bill: ₹{total}")
    except (ValueError, TypeError):
        messagebox.showerror("Error", "Please enter a valid quantity.")

root = tk.Tk()
root.title("Restaurant Management System")
root.geometry("400x300")

tk.Label(root, text="Quick Order", font=("Arial", 16, "bold")).pack(pady=10)

tk.Label(root, text="Select Food Item:").pack()
item_combo = ttk.Combobox(root, values=["Burger", "Pizza", "Pasta"])
item_combo.current(0)
item_combo.pack(pady=5)

tk.Label(root, text="Enter Quantity:").pack()
qty_entry = tk.Entry(root)
qty_entry.pack(pady=5)

tk.Button(root, text="Confirm Order", command=place_order, bg="#4CAF50", fg="white").pack(pady=20)
root.mainloop()

