import tkinter as tk
from tkinter import messagebox
from datetime import datetime

import os
import json

stocks_json = "stocks.json"
orders_json = "orders.json"

personnel_passcode = "220309"

def load_json(file_path):
    if os.path.exists(file_path):
        with open(file_path, "r") as fileread:
            return json.load(fileread)
    else:
        return []

def save_json(data, file_path):
    with open(file_path, "w") as filewrite:
        json.dump(data, filewrite, indent=4)

orders = load_json(orders_json)

def main():
    root = tk.Tk()
    root.title("Welcome")
    root.resizable(False, False)
    root.geometry('400x400')
    root.configure(background='#daf6da')

    user_type_var = tk.StringVar()

    label = tk.Label(root, text="Select your user type:", font=("Helvetica", 16), foreground='#435b46', bg='#daf6da')
    label.pack(pady=10)

    user_type_options = ["Customer", "Personnel"]
    user_type_dropdown = tk.OptionMenu(root, user_type_var, *user_type_options)
    user_type_dropdown.config(font=("Helvetica", 14), width=15)
    user_type_dropdown.pack(pady=10)

    def proceed():
        user_type = user_type_var.get()
        if user_type == "Customer":
            customer_window(root)
        elif user_type == "Personnel":
            ask_passcode(root)
        else:
            messagebox.showerror("Error", "Select user type.")

    proceed_button = tk.Button(root, text="Proceed", font=("Helvetica", 14), bg='#9abe9d', command=proceed, width=15)
    proceed_button.pack(pady=15)

    root.mainloop()

def ask_passcode(root):
    passcode_window = tk.Toplevel(root)
    passcode_window.title("Enter Passcode")
    passcode_window.geometry("300x150")
    passcode_window.configure(background='#daf6da')

    label = tk.Label(passcode_window, text="Enter Passcode:", font=("Helvetica", 14), foreground='#435b46', bg='#daf6da')
    label.pack(pady=10)

    passcode_var = tk.StringVar()
    passcode_entry = tk.Entry(passcode_window, textvariable=passcode_var, show="*")
    passcode_entry.pack(pady=10)

    def check_passcode():
        entered_passcode = passcode_var.get()
        if entered_passcode == personnel_passcode:
            passcode_window.destroy()
            personnel_window(root)
        else:
            messagebox.showerror("Error", "Incorrect passcode. Access denied.")
            passcode_window.destroy()

    submit_button = tk.Button(passcode_window, text="Submit", font=("Helvetica", 14), bg='#9abe9d', command=check_passcode)
    submit_button.pack(pady=10)

def customer_window(root):
    for widget in root.winfo_children():
        widget.destroy()

    label = tk.Label(root, text="Welcome to Majestique!", font=("Helvetica", 18), foreground='#435b46', bg='#daf6da')
    label.pack(pady=20)

    def open_shopping_cart():
        root.destroy() 
        ShoppingCartApp(tk.Tk()) 

    button = tk.Button(root, text="Shop Now", font=("Helvetica", 14), bg='#9abe9d', command=open_shopping_cart, width=15)
    button.pack(pady=15)

    about_us_button = tk.Button(root, text="About Us", font=("Helvetica", 14), bg='#9abe9d', command=about_us, width=15)
    about_us_button.pack(pady=15)

    back_button = tk.Button(root, text="Back", font=("Helvetica", 14), bg='#9abe9d', command=lambda: back(root), width=15)
    back_button.pack(pady=15)

class ShoppingCartApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Majestique App")
        self.master.resizable(False, False)
        self.master.configure(background='#daf6da')

        self.items = load_json(stocks_json)

        self.sorted_ascending = True  
        self.cart_items = [] 

        self.create_main_screen()

    def create_main_screen(self):

        self.sort_frame = tk.Frame(self.master, bg='#daf6da')
        self.sort_frame.pack(pady=10)

        self.sort_ascending_button = tk.Button(self.sort_frame, text="Price ↑", bg='#9abe9d', command=self.sort_ascending, width=5)
        self.sort_ascending_button.pack(side=tk.LEFT, padx=10)

        self.sort_descending_button = tk.Button(self.sort_frame, text="Price ↓", bg='#9abe9d', command=self.sort_descending, width=5)
        self.sort_descending_button.pack(side=tk.LEFT)

        self.price_label = tk.Label(self.master, text="Enter Budget: (Optional)", bg='#daf6da')
        self.price_label.pack()

        self.price_var = tk.StringVar()
        self.price_entry = tk.Entry(self.master, textvariable=self.price_var)
        self.price_entry.pack()

        self.search_show_frame = tk.Frame(self.master, bg='#daf6da')
        self.search_show_frame.pack(pady=10)

        self.show_all_button = tk.Button(self.search_show_frame, text="Show All Items", bg='#9abe9d', command=self.show_all_items, width=15)
        self.show_all_button.pack(side=tk.LEFT, padx=10)

        self.search_button = tk.Button(self.search_show_frame, text="Search Item", bg='#9abe9d', command=self.search_item_by_price, width=15)
        self.search_button.pack(side=tk.LEFT)

        self.item_frame = tk.Frame(self.master, bg='#daf6da')
        self.item_frame.pack(pady=10)

        self.item_listbox = tk.Listbox(self.item_frame, width=50, height=10)
        self.item_listbox.pack(side=tk.LEFT)

        self.scrollbar = tk.Scrollbar(self.item_frame, orient=tk.VERTICAL)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.populate_item_listbox()
        self.item_listbox.config(yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.item_listbox.yview)

        self.quantity_label = tk.Label(self.master, text="Quantity:", bg='#daf6da')
        self.quantity_label.pack()

        self.quantity_var = tk.StringVar()
        self.quantity_var.trace("w", lambda name, index, mode, sv=self.quantity_var: self.validate_quantity())
        self.quantity_entry = tk.Entry(self.master, textvariable=self.quantity_var)
        self.quantity_entry.pack()

        self.add_button = tk.Button(self.master, text="Add to Cart", bg='#9abe9d', command=self.add_to_cart, width=15)
        self.add_button.pack(pady=10)

        self.cart_label = tk.Label(self.master, text="Shopping Cart:", bg='#daf6da')
        self.cart_label.pack()

        self.cart_listbox = tk.Listbox(self.master, width=50, height=5)
        self.cart_listbox.pack()

        self.cart_button_frame = tk.Frame(self.master, bg='#daf6da')
        self.cart_button_frame.pack(pady=10)

        self.remove_button = tk.Button(self.cart_button_frame, text="Remove Item", bg='#9abe9d', command=self.remove_from_cart, width=15)
        self.remove_button.pack(side=tk.LEFT, padx=10)

        self.clear_button = tk.Button(self.cart_button_frame, text="Clear Cart", bg='#9abe9d', command=self.clear_cart, width=15)
        self.clear_button.pack(side=tk.LEFT)

        self.checkout_button = tk.Button(self.master, text="Check Out", bg='#9abe9d', command=self.confirm_checkout, width=15)
        self.checkout_button.pack(pady=10)

    def populate_item_listbox(self, target_price=None):
        self.item_listbox.delete(0, tk.END) 
        if target_price is None:
            items_to_display = self.items
        else:
            items_to_display = [item for item in self.items if item['price'] <= target_price]
        bubble_sort(items_to_display) 
        if not self.sorted_ascending:
            items_to_display.reverse()
        for item in items_to_display:
            self.item_listbox.insert(tk.END, f"{item['name']} - ₱{item['price']}   (Available: {item['stocks']} items)")

    def sort_ascending(self):
        self.sorted_ascending = True
        target_price = int(self.price_var.get()) if self.price_var.get().isdigit() else None
        self.populate_item_listbox(target_price)

    def sort_descending(self):
        self.sorted_ascending = False
        target_price = int(self.price_var.get()) if self.price_var.get().isdigit() else None
        self.populate_item_listbox(target_price)

    def search_item_by_price(self):
        target_price = int(self.price_var.get()) if self.price_var.get().isdigit() else None
        self.populate_item_listbox(target_price)

    def show_all_items(self):
        self.populate_item_listbox()

    def add_to_cart(self):
        selected_index = self.item_listbox.curselection()
        if selected_index:
            item = self.items[selected_index[0]]
            try:
                quantity = int(self.quantity_var.get())
                if quantity > 0:
                    if item["stocks"] >= quantity:
                        item["stocks"] -= quantity
                        self.populate_item_listbox()
                        self.cart_items.append({"item": item, "quantity": quantity})
                        self.populate_cart_listbox()
                    else:
                        messagebox.showinfo("Add to Cart", "Requested quantity exceeds available stock.")
                else:
                    messagebox.showinfo("Add to Cart", "Please enter a valid positive quantity.")
            except ValueError:
                messagebox.showinfo("Add to Cart", "Please enter a valid quantity.")
        else:
            messagebox.showinfo("Add to Cart", "Please select an item first.")


    def remove_from_cart(self):
        selected_index = self.cart_listbox.curselection()
        if selected_index:
            self.cart_items.pop(selected_index[0])
            self.populate_cart_listbox()
        else:
            messagebox.showinfo("Remove Item", "Please select an item to remove from the cart.")

    def clear_cart(self):
        self.cart_items = []
        self.populate_cart_listbox()

    def populate_cart_listbox(self):
        self.cart_listbox.delete(0, tk.END) 
        total_items = count_items(self.cart_items)
        cart_label_text = f"Shopping Cart: {total_items} items"
        self.cart_label.config(text=cart_label_text)
        for cart_item in self.cart_items:
            item = cart_item["item"]
            quantity = cart_item["quantity"]
            total = quantity*item['price']
            self.cart_listbox.insert(tk.END, f"{quantity} {item['name']} ₱{item['price']}  =  ₱{total}")

    def validate_quantity(self):
        if not self.quantity_var.get().isdigit():
            messagebox.showinfo("Quantity Validation", "Please enter a valid quantity.")

    def confirm_checkout(self):
        confirm = messagebox.askyesno("Confirm Order", "Are you sure you want to check out cart?")
        if confirm:
            self.checkout_order()

    def checkout_order(self):
        save_json(self.items, stocks_json)

        total_cost = self.calculate_total_cost()

        checkout_window = tk.Toplevel()
        checkout_window.title("Checkout")
        checkout_window.geometry('400x600')
        checkout_window.configure(background='#daf6da')

        tk.Label(checkout_window, text="\nCheck Out Order\n", font=("Helvetica", 16, "bold"), bg='#daf6da').pack()

        tk.Label(checkout_window, text="Total Cost:", bg='#daf6da').pack()
        tk.Entry(checkout_window, textvariable=tk.StringVar(value=f"₱{total_cost:.2f}"), state="readonly").pack()

        tk.Label(checkout_window, text="Products Bought:", bg='#daf6da').pack()
        products_text = tk.Text(checkout_window, height=10, width=50)
        products_text.pack()

        for cart_item in self.cart_items:
            item = cart_item["item"]
            quantity = cart_item["quantity"]
            total = quantity * item['price']
            products_text.insert(tk.END, f"{quantity} {item['name']} ₱{item['price']}  =  ₱{total}\n")

        tk.Label(checkout_window, text="Select Payment Option:", bg='#daf6da').pack()
        payment_var = tk.StringVar()
        payment_var.set("")  
        payment_options = ["Bank", "Gcash", "Cash on Delivery (COD)"]

        payment_dropdown = tk.OptionMenu(checkout_window, payment_var, *payment_options)
        payment_dropdown.configure(bg='#9abe9d', width=15)
        payment_dropdown.pack()

        def confirm_payment():
            payment_option = payment_var.get()
            if payment_option == "Bank":
                bank_window = tk.Toplevel(checkout_window)
                bank_window.title("Bank Payment")
                bank_window.geometry('300x150')
                bank_window.configure(background='#daf6da')

                def confirm_bank_payment():
                    confirmation_message = f"Payment of ₱{total_cost:.2f} confirmed via Bank."
                    confirmation_label.config(text=confirmation_message)
                    confirm_button.destroy()
                    done_button.pack(pady=10)

                bank_number_label = tk.Label(bank_window, text="Enter Bank Number:", bg='#daf6da')
                bank_number_label.pack()
                bank_number_entry = tk.Entry(bank_window)
                bank_number_entry.pack(pady=5)

                confirm_button = tk.Button(bank_window, text="Confirm", bg='#9abe9d', command=confirm_bank_payment, width=15)
                confirm_button.pack(pady=5)

                confirmation_label = tk.Label(bank_window, text="", bg='#daf6da')
                confirmation_label.pack()

                def close_bank_window():
                    bank_window.destroy()

                done_button = tk.Button(bank_window, text="Done", bg='#9abe9d', command=close_bank_window, width=15)

            elif payment_option == "Gcash":
                gcash_window = tk.Toplevel(checkout_window)
                gcash_window.title("Gcash Payment")
                gcash_window.geometry('300x150')
                gcash_window.configure(background='#daf6da')

                def confirm_gcash_payment():
                    confirmation_message = f"Payment of ₱{total_cost:.2f} confirmed via Gcash."
                    confirmation_label.config(text=confirmation_message)
                    confirm_button.destroy()
                    done_button.pack(pady=10)

                gcash_number_label = tk.Label(gcash_window, text="Enter Gcash Number:", bg='#daf6da')
                gcash_number_label.pack()
                gcash_number_entry = tk.Entry(gcash_window)
                gcash_number_entry.pack(pady=5)

                confirm_button = tk.Button(gcash_window, text="Confirm", bg='#9abe9d', command=confirm_gcash_payment, width=15)
                confirm_button.pack(pady=5)

                confirmation_label = tk.Label(gcash_window, text="", bg='#daf6da')
                confirmation_label.pack()

                def close_gcash_window():
                    gcash_window.destroy()

                done_button = tk.Button(gcash_window, text="Done", bg='#9abe9d', command=close_gcash_window, width=15)

            elif payment_option == "Cash on Delivery (COD)":
                cod_window = tk.Toplevel(checkout_window)
                cod_window.title("COD Payment")
                cod_window.geometry('300x150')
                cod_window.configure(background='#daf6da')

                tk.Label(cod_window, text=f"\n\nPayment via Cash On Delivery confirmed.\nPlease prepare ₱{total_cost:.2f} upon delivery.\n", bg='#daf6da').pack()
                
                done_button = tk.Button(cod_window, text="Done", bg='#9abe9d', command=cod_window.destroy, width=15).pack()

        confirm_payment_button = tk.Button(checkout_window, text="Confirm Payment", bg='#9abe9d', command=confirm_payment, width=15)
        confirm_payment_button.pack(pady=10)

        tk.Label(checkout_window, text="Name: ", bg='#daf6da').pack()
        name_entry = tk.Entry(checkout_window, width=40)
        name_entry.pack()

        tk.Label(checkout_window, text="Enter Delivery Address: (Full Address)", bg='#daf6da').pack()
        address_entry = tk.Entry(checkout_window, width=40)
        address_entry.pack()

        button_frame = tk.Frame(checkout_window, bg='#daf6da')
        button_frame.pack(pady=10)

        cancel_button = tk.Button(button_frame, text="Cancel", bg='#9abe9d', command=checkout_window.destroy, width=15)
        cancel_button.pack(side=tk.LEFT, padx=10)

        self.confirm_place_order_button = tk.Button(button_frame, text="Place Order", bg='#9abe9d', 
                                            command=lambda: self.confirm_place_order(checkout_window, payment_var.get(), name_entry.get(), address_entry.get()), width=15)

        self.confirm_place_order_button.pack(side=tk.LEFT)
        
    def confirm_place_order(self, checkout_window, payment_option, customer_name, address):
        if customer_name.strip() == "":
            messagebox.showinfo("Name Required", "Please enter your name before placing the order.")
            return

        if address.strip() == "":
            messagebox.showinfo("Address Required", "Please enter your full address before placing the order.")
            return

        confirm = messagebox.askyesno("Confirm Order", "Are you sure you want to place the order?")
        if confirm:
            total_cost = self.calculate_total_cost()
            self.display_receipt(total_cost, payment_option, customer_name, address)
            checkout_window.destroy()

    def display_receipt(self, total_cost, payment_option, customer_name, address):
        receipt_window = tk.Toplevel(self.master)
        receipt_window.title("Receipt")
        receipt_window.geometry('400x500')
        receipt_window.configure(background='#daf6da')

        tk.Label(receipt_window, text="\nPlaced Order Details\n", font=("Helvetica", 16, "bold"), bg='#daf6da').pack()

        tk.Label(receipt_window, text="Products Bought:", bg='#daf6da').pack()
        products_text = tk.Text(receipt_window, height=10, width=50)
        products_text.pack()

        for cart_item in self.cart_items:
            item = cart_item["item"]
            quantity = cart_item["quantity"]
            total = quantity*item['price']
            products_text.insert(tk.END, f"{quantity} {item['name']} ₱{item['price']}  =  ₱{total}\n")

        tk.Label(receipt_window, text=f"\nTotal Cost: ₱{total_cost:.2f}", font=("Helvetica", 10, "bold"), bg='#daf6da').pack()
        tk.Label(receipt_window, text=f"Payment Method: {payment_option}", bg='#daf6da').pack()
        tk.Label(receipt_window, text=f"\nThank you for your purchase, {customer_name}!\n\nYour order should be delivered between June 1 - 4\non {address}.", bg='#daf6da').pack()

        order_details = {
            "customer_name": customer_name,
            "customer_address": address,
            "order_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "items": self.cart_items
        }

        orders.append(order_details)
        save_json(orders, orders_json)

        button_frame = tk.Frame(receipt_window, bg='#daf6da')
        button_frame.pack(pady=10)

        done_button = tk.Button(button_frame, text="Done", bg='#9abe9d', command=self.master.destroy, width=10)
        done_button.pack(side=tk.LEFT, padx=10)

        back_button = tk.Button(button_frame, text="Back", bg='#9abe9d', command=lambda: back(self.master), width=10)
        back_button.pack(side=tk.LEFT, padx=10)

    def calculate_total_cost(self):
        total_cost = 0
        for cart_item in self.cart_items:
            item_price = cart_item["item"]["price"]
            quantity = cart_item["quantity"]
            total_cost += item_price * quantity
        return total_cost
    
def count_items(items):
    if not items:
        return 0
    else:
        return 1 + count_items(items[1:])
    
def bubble_sort(items):
        n = len(items)
        for i in range(n):
            for j in range(0, n-i-1):
                if items[j]['price'] > items[j+1]['price']:
                    items[j], items[j+1] = items[j+1], items[j]

def binary_search(items, target_price):
    low = 0
    high = len(items) - 1
    while low <= high:
        mid = (low + high) // 2
        if items[mid]['price'] == target_price:
            return mid
        elif items[mid]['price'] < target_price:
            low = mid + 1
        else:
            high = mid - 1
    return -1
    
def about_us():
    about_us_window = tk.Toplevel()
    about_us_window.title("About Us")
    about_us_window.geometry('600x600')
    about_us_window.configure(background='#daf6da')

    tk.Label(about_us_window, text="\nAbout Us", font=("Helvetica", 16, "bold"), bg='#daf6da').pack()
    tk.Label(about_us_window, text="Majestique - Elevate your style.\n\nAt Majestique, we're passionate about providing you with stylish accessories\nthat complement your unique personality and enhance your everyday style.\nOur goal is to make shopping for accessories a delightful experience,\noffering a curated selection of high-quality products at affordable prices.\n\n",  font="Helvetica", bg='#daf6da').pack()
    tk.Label(about_us_window, text="Why Choose Us?", font=("Helvetica", 14, "bold"), bg='#daf6da').pack()
    tk.Label(about_us_window, text="We're here to help you express your individuality through our carefully curated\ncollection of accessories, each handpicked for its quality, style, and versatility.\nWe source our accessories from trusted suppliers to ensure durability and style.\nEnjoy browsing on our user-friendly platform and find the perfect accessories\nin just a few clicks.\nHave a question or need assistance? Our friendly support team is here to help.", font="Helvetica", bg='#daf6da').pack()
    tk.Label(about_us_window, text="",  bg='#daf6da').pack()
    tk.Label(about_us_window, text="Join Our Community", font=("Helvetica", 14, "bold"), bg='#daf6da').pack()
    tk.Label(about_us_window, text="Become part of our growing community of accessory enthusiasts.\nFollow us on social media for style inspiration, promotions,\nand exclusive offers.\n\nThank you for choosing Majestique for your accessory needs!", font="Helvetica", bg='#daf6da').pack()

    close_button = tk.Button(about_us_window, text="Close", bg='#9abe9d', command=about_us_window.destroy, width=15)
    close_button.pack(pady=30)

def personnel_window(root):
    for widget in root.winfo_children():
        widget.destroy()

    label = tk.Label(root, text="Personnel Dashboard", font=("Helvetica", 18), foreground='#435b46', bg='#daf6da')
    label.pack(pady=20)

    manage_inventory_button = tk.Button(root, text="Manage Inventory", font=("Helvetica", 14), bg='#9abe9d', command=manage_inventory_window, width=15)
    manage_inventory_button.pack(pady=15)

    view_orders_button = tk.Button(root, text="View Orders", font=("Helvetica", 14), bg='#9abe9d', command=view_orders, width=15)
    view_orders_button.pack(pady=15)

    back_button = tk.Button(root, text="Back", font=("Helvetica", 14), bg='#9abe9d', command=lambda: back(root), width=15)
    back_button.pack(pady=15)


def manage_inventory_window():
    inventory_window = tk.Toplevel()
    inventory_window.title("Manage Inventory")
    inventory_window.geometry('400x450')
    inventory_window.configure(background='#daf6da')

    items = load_json(stocks_json)

    def add_stocks():
        selected_index = item_listbox.curselection()
        if selected_index:
            item_index = selected_index[0]
            try:
                added_stocks = int(add_stocks_var.get())
                if added_stocks > 0:
                    items[item_index]["stocks"] += added_stocks
                    save_json(items, stocks_json)
                    populate_item_listbox()
                    add_stocks_entry.delete(0, tk.END)
                else:
                    messagebox.showinfo("Add Stocks", "Please enter a valid positive number of stocks.")
            except ValueError:
                messagebox.showinfo("Add Stocks", "Please enter a valid number.")

    tk.Label(inventory_window, text="Items:", font=("Helvetica", 14), bg='#daf6da').pack(pady=10)
    item_listbox = tk.Listbox(inventory_window, width=50, height=10)
    item_listbox.pack()

    def populate_item_listbox():
        item_listbox.delete(0, tk.END)
        for item in items:
            item_listbox.insert(tk.END, f"{item['name']} - ₱{item['price']}   (Stocks: {item['stocks']})")

    populate_item_listbox()

    tk.Label(inventory_window, text="Stocks to be added:", font=("Helvetica", 10), bg='#daf6da').pack(pady=10)
    add_stocks_var = tk.StringVar()
    add_stocks_entry = tk.Entry(inventory_window, textvariable=add_stocks_var, font=("Helvetica", 12))
    add_stocks_entry.pack()

    add_stocks_button = tk.Button(inventory_window, text="Add Stocks", font=("Helvetica", 14), bg='#9abe9d', command=add_stocks, width=15)
    add_stocks_button.pack(pady=15)

    close_button = tk.Button(inventory_window, text="Close", font=("Helvetica", 14), bg='#9abe9d', command=inventory_window.destroy, width=15)
    close_button.pack(pady=10)
 
class Order:
    def __init__(self, customer_name, address, order_date, items):
        self.customer_name = customer_name
        self.address= address
        self.order_date = order_date
        self.items = items

def view_orders():
    global orders  

    orders_window = tk.Toplevel()
    orders_window.title("View Orders")
    orders_window.geometry('400x300')
    orders_window.configure(background='#daf6da')

    orders_label = tk.Label(orders_window, text="Order List", font=("Helvetica", 18), foreground='#435b46', bg='#daf6da')
    orders_label.pack(pady=10)

    orders_text = tk.Text(orders_window, height=10, width=50)
    orders_text.pack()

    for order in orders:
        customer_name = order["customer_name"]
        customer_address = order["customer_address"]
        order_date = order["order_date"]
        items_text = ", ".join([f"{item['quantity']} {item['item']['name']}" for item in order["items"]])
        orders_text.insert(tk.END, f"Customer: {customer_name}\nAddress: {customer_address}\nOrder Date: {order_date}\nItems: {items_text}\n\n")

    tk.Button(orders_window, text="Close", bg='#9abe9d', command=orders_window.destroy, width=15).pack(pady=10)

def back(root):
    for widget in root.winfo_children():
        if widget.winfo_class() != 'TFrame':
            widget.destroy()

    label = tk.Label(root, text="Select your user type:", font=("Helvetica", 16), foreground='#435b46', bg='#daf6da')
    label.pack(pady=10)

    user_type_var = tk.StringVar()
    user_type_options = ["Customer", "Personnel"]
    user_type_dropdown = tk.OptionMenu(root, user_type_var, *user_type_options)
    user_type_dropdown.config(font=("Helvetica", 14), width=15)
    user_type_dropdown.pack(pady=10)

    def proceed():
        user_type = user_type_var.get()
        if user_type == "Customer":
            customer_window(root)
        elif user_type == "Personnel":
            ask_passcode(root)
        else:
            messagebox.showerror("Error", "Select user type.")

    proceed_button = tk.Button(root, text="Proceed", font=("Helvetica", 14), bg='#9abe9d', command=proceed, width=15)
    proceed_button.pack(pady=15)

    root.geometry('400x400')
    root.update_idletasks()
    
if __name__ == "__main__":
    main()

