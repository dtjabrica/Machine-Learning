import tkinter as tk
import time
import mysql.connector
from collections import deque

class OrderQueueSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("Order Queue System")
        self.root.geometry("800x400")

        # Connect to the MySQL database
        self.db_connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Doffy@2002",
            database="order_queue_db"
        )

        # Create the orders table if it doesn't exist
        self.create_orders_table()

        # Create labels, entry fields, and buttons
        self.customer_label = tk.Label(root, text="Customer Name:")
        self.customer_label.grid(row=0, column=0, padx=10, pady=10)
        self.customer_entry = tk.Entry(root)
        self.customer_entry.grid(row=0, column=1, padx=10, pady=10)

        self.order_label = tk.Label(root, text="Order Item:")
        self.order_label.grid(row=1, column=0, padx=10, pady=10)
        self.order_entry = tk.Entry(root)
        self.order_entry.grid(row=1, column=1, padx=10, pady=10)

        self.quantity_label = tk.Label(root, text="Quantity:")
        self.quantity_label.grid(row=2, column=0, padx=10, pady=10)
        self.quantity_entry = tk.Entry(root)
        self.quantity_entry.grid(row=2, column=1, padx=10, pady=10)

        self.add_order_button = tk.Button(root, text="Add Order", command=self.add_order)
        self.add_order_button.grid(row=0, column=2, padx=10, pady=10)

        self.add_to_queue_button = tk.Button(root, text="Add to Queue", command=self.add_to_queue)
        self.add_to_queue_button.grid(row=1, column=2, padx=10, pady=10)

        self.serve_queue_button = tk.Button(root, text="Serve Queue", command=self.serve_queue)
        self.serve_queue_button.grid(row=2, column=2, padx=10, pady=10)

        self.queue_label = tk.Label(root, text="ACTIVITY WINDOW:")
        self.queue_label.grid(row=3, column=0, padx=10, pady=10)

        self.display_field = tk.Text(root, height=10, width=50)
        self.display_field.grid(row=4, column=0, padx=10, pady=10)

        self.customer_display_label = tk.Label(root, text="Customers in Queue:")
        self.customer_display_label.grid(row=4, column=1, padx=10, pady=10)

        self.customer_display_field = tk.Text(root, height=10, width=25)
        self.customer_display_field.grid(row=4, column=2, padx=10, pady=10)

        # Initialize order queue
        self.order_queue = deque()
        self.load_queue_from_database()

    def create_orders_table(self):
        cursor = self.db_connection.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS orders (OrderNo INT PRIMARY KEY AUTO_INCREMENT, CustomerName VARCHAR(255), OrderItem VARCHAR(255), Quantity VARCHAR(45))")
        self.db_connection.commit()

    def add_order(self):
        customer_name = self.customer_entry.get()
        order_item = self.order_entry.get()
        quantity = int(self.quantity_entry.get())

        # Insert the order into the database
        cursor = self.db_connection.cursor()
        query = "INSERT INTO orders (CustomerName, OrderItem, Quantity) VALUES (%s, %s, %s)"
        values = (customer_name, order_item, quantity)
        cursor.execute(query, values)
        self.db_connection.commit()

        # Clear entry fields
        self.customer_entry.delete(0, tk.END)
        self.order_entry.delete(0, tk.END)
        self.quantity_entry.delete(0, tk.END)

        # Load and display the updated queue
        self.load_queue_from_database()

    def add_to_queue(self):
        if len(self.order_queue) == 0:
            self.display_field.insert(tk.END, "No orders to queue.\n")
            return

        # Get the next order to add to the queue
        next_order = self.order_queue.popleft()

        # Load and display the updated queue
        self.load_queue_from_database()

        # Display the added order
        self.display_field.insert(tk.END, f"Added to Queue: Order No.: {next_order[0]}, Customer Name: {next_order[1]}, Order Item: {next_order[2]}, Quantity: {next_order[3]}\n")

    def serve_queue(self):
        if len(self.order_queue) == 0:
            self.display_field.insert(tk.END, "No orders in the queue.\n")
            return

        # Get the first order from the queue
        served_order = self.order_queue[0]

        # Delete the served order from the database
        cursor = self.db_connection.cursor()
        query = "DELETE FROM orders WHERE OrderNo = %s"
        cursor.execute(query, (served_order[0],))
        self.db_connection.commit()

        # Load and display the updated queue
        self.load_queue_from_database()

        # Display the served order
        self.display_field.insert(tk.END, f"Served Order: Order No.: {served_order[0]}, Customer Name: {served_order[1]}, Order Item: {served_order[2]}, Quantity: {served_order[3]}\n")

    def load_queue_from_database(self):
        # Clear the existing order queue
        self.order_queue.clear()

        # Fetch orders from the database
        cursor = self.db_connection.cursor()
        cursor.execute("SELECT * FROM orders")
        orders = cursor.fetchall()

        # Add orders to the queue
        for order in orders:
            self.order_queue.append(order)

        # Display the queue in the display field
        self.display_field.delete("1.0", tk.END)
        for order in self.order_queue:
            self.display_field.insert(tk.END, f"Order No.: {order[0]}, Customer Name: {order[1]}, Order Item: {order[2]}, Quantity: {order[3]}\n")

        # Display customer names in the customer display field
        self.customer_display_field.delete("1.0", tk.END)
        customer_names = [order[1] for order in self.order_queue]
        self.customer_display_field.insert(tk.END, "\n".join(customer_names))

    def run(self):
        self.root.mainloop()

# Create the main window
root = tk.Tk()

# Initialize the order queue system
order_queue_system = OrderQueueSystem(root)

# Run the application
order_queue_system.run()