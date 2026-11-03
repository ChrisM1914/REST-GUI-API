# app.py
import tkinter as tk
from tkinter import ttk, messagebox
from decimal import Decimal, InvalidOperation
import json
import urllib.request  # part of stdlib; no external libs needed
import urllib.error
 
API_URL = "http://localhost:5000/submit"
MAX_PRICE = Decimal("1000.00")
 
root = tk.Tk()
root.title("Purchase Form")
 
# ---------- FORM VARIABLES ----------
product_id_var = tk.StringVar()
description_var = tk.StringVar()
price_var = tk.StringVar()  # StringVar so decimals like 19.99 can be typed
name_var = tk.StringVar()
email_var = tk.StringVar()
online_var = tk.BooleanVar()  # checked = online, unchecked = in-store
 
# ---------- LAYOUT ----------
frame = ttk.Frame(root, padding="10")
frame.grid(row=0, column=0, sticky=(tk.W, tk.E))
 
# Product ID
ttk.Label(frame, text="Product ID:").grid(column=0, row=0, sticky=tk.W)
ttk.Entry(frame, width=30, textvariable=product_id_var).grid(column=1, row=0)
 
# Description
ttk.Label(frame, text="Description:").grid(column=0, row=1, sticky=tk.W)
ttk.Entry(frame, width=30, textvariable=description_var).grid(column=1, row=1)
 
# Price
ttk.Label(frame, text="Price ($):").grid(column=0, row=2, sticky=tk.W)
ttk.Entry(frame, width=12, textvariable=price_var).grid(column=1, row=2, sticky=tk.W)
 
# Name
ttk.Label(frame, text="Name:").grid(column=0, row=3, sticky=tk.W)
ttk.Entry(frame, width=30, textvariable=name_var).grid(column=1, row=3)
 
# Email
ttk.Label(frame, text="Email:").grid(column=0, row=4, sticky=tk.W)
ttk.Entry(frame, width=30, textvariable=email_var).grid(column=1, row=4)
 
# Online / in-store checkbox
ttk.Checkbutton(
    frame,
    text="Online purchase (uncheck for in-store)",
    variable=online_var,
).grid(columnspan=2, row=5, sticky=tk.W)
 
# Submit button
submit_btn = ttk.Button(frame, text="Submit", command=lambda: submit_form())
submit_btn.grid(row=6, columnspan=2, pady=(10, 0))
 
 
def validate() -> bool:
    """Return True if all fields are valid; otherwise show an error."""
    if not product_id_var.get().strip():
        messagebox.showerror("Validation Error", "Product ID cannot be empty.")
        return False
 
    if not description_var.get().strip():
        messagebox.showerror("Validation Error", "Description cannot be empty.")
        return False
 
    # Price must be a number, greater than 0, and <= $1000.00
    try:
        price = Decimal(price_var.get().strip())
    except InvalidOperation:
        messagebox.showerror("Validation Error", "Price must be a number, e.g. 19.99.")
        return False
    if price <= 0 or price > MAX_PRICE:
        messagebox.showerror(
            "Validation Error", "Price must be greater than $0 and no more than $1000.00."
        )
        return False
 
    name = name_var.get().strip()
    if len(name) < 5 or not name.replace(" ", "").isalpha():
        messagebox.showerror(
            "Validation Error",
            "Name must be at least 5 characters and contain only letters.",
        )
        return False
 
    # Same email rule as the original guide
    email = email_var.get().strip()
    if not email or "@" not in email:
        messagebox.showerror("Validation Error", "Enter a valid email address.")
        return False
 
    return True
 
 
def collect_data() -> dict:
    """Return a dictionary that represents the form."""
    return {
        "product_id": product_id_var.get().strip(),
        "description": description_var.get().strip(),
        "price": float(Decimal(price_var.get().strip())),
        "name": name_var.get().strip(),
        "email": email_var.get().strip(),
        "purchase_type": "online" if online_var.get() else "in-store",
    }
 
 
def submit_form() -> None:
    if not validate():
        return  # abort if validation failed
 
    payload = collect_data()
    json_payload = json.dumps(payload).encode("utf-8")
 
    req = urllib.request.Request(
        API_URL,
        data=json_payload,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
 
    try:
        with urllib.request.urlopen(req) as resp:
            result = json.loads(resp.read().decode())
            messagebox.showinfo("Success", f"Server replied: {result}")
    except urllib.error.HTTPError as e:
        error_msg = e.read().decode()
        messagebox.showerror("API Error", f"{e.code} – {error_msg}")
    except Exception as exc:
        messagebox.showerror("Connection Error", str(exc))
 
 
if __name__ == "__main__":
    root.mainloop()