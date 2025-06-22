import tkinter as tk
from tkinter import messagebox, scrolledtext
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import datetime

# GST calculator
def calculate_gst(bill_amount, gst_rate=0.18):
    return bill_amount * gst_rate

# Email sender
def send_email(to_email, subject, body):
    from_email = "your_email@gmail.com"  
    from_password = "your_app_password"  # Use app password for Gmail

    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(from_email, from_password)
        server.sendmail(from_email, to_email, msg.as_string())
        server.quit()
        messagebox.showinfo("Success", f"Email sent successfully to {to_email}!")
    except Exception as e:
        messagebox.showerror("Email Error", f"Failed to send email: {e}")

# Add product to list
def add_product():
    name = entry_product_name.get()
    try:
        price = float(entry_product_price.get())
        products.append((name, price))
        update_bill_area()
        entry_product_name.delete(0, tk.END)
        entry_product_price.delete(0, tk.END)
    except ValueError:
        messagebox.showerror("Invalid Input", "Enter a valid price.")

# Update bill text area
def update_bill_area():
    bill_area.delete(1.0, tk.END)
    total = sum(price for _, price in products)
    gst = calculate_gst(total)
    final = total + gst
    now = datetime.datetime.now()

    bill = f"--- Bill Details ---\n"
    bill += f"Name: {entry_name.get()}\n"
    bill += f"Email: {entry_email.get()}\n"
    bill += f"Date: {now.strftime('%Y-%m-%d')}\nTime: {now.strftime('%H:%M:%S')}\n"
    bill += "\nProducts Purchased:\n"
    for p, pr in products:
        bill += f"- {p}: ₹{pr:.2f}\n"
    bill += f"\nTotal: ₹{total:.2f}\nGST (18%): ₹{gst:.2f}\nFinal Bill: ₹{final:.2f}\n"
    bill += "---------------------"
    bill_area.insert(tk.END, bill)

# Send the bill via email
def process_bill():
    if not entry_name.get() or not entry_email.get():
        messagebox.showwarning("Missing Info", "Please enter name and email.")
        return
    if not products:
        messagebox.showwarning("No Products", "Please add at least one product.")
        return

    send_email(entry_email.get(), "Your Supermarket Bill", bill_area.get(1.0, tk.END))

# GUI window
root = tk.Tk()
root.title("Supermarket Billing System")
root.geometry("600x600")

products = []

# Name and Email
tk.Label(root, text="Customer Name:").pack()
entry_name = tk.Entry(root, width=40)
entry_name.pack()

tk.Label(root, text="Customer Email:").pack()
entry_email = tk.Entry(root, width=40)
entry_email.pack()

# Product entry
tk.Label(root, text="Product Name:").pack()
entry_product_name = tk.Entry(root, width=40)
entry_product_name.pack()

tk.Label(root, text="Product Price:").pack()
entry_product_price = tk.Entry(root, width=40)
entry_product_price.pack()

# Buttons
tk.Button(root, text="Add Product", command=add_product).pack(pady=5)
tk.Button(root, text="Send Bill", command=process_bill).pack(pady=5)

# Bill area
bill_area = scrolledtext.ScrolledText(root, width=60, height=20)
bill_area.pack(pady=10)

root.mainloop()
