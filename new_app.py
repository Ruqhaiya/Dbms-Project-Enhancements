import tkinter as tk
from tkinter import ttk

class BloodBankApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Blood Bank Management System")
        self.setup_ui()

    def setup_ui(self):
        # Create the sidebar frame
        self.sidebar = tk.Frame(self.root, width=200, bg='black')
        self.sidebar.pack(fill='y', side='left')

        # Main content area
        self.main_content = tk.Frame(self.root)
        self.main_content.pack(fill='both', expand=True, side='right')

        # Sidebar buttons
        self.create_sidebar_button("View Records", self.view_records)
        self.create_sidebar_button("Run Queries", self.run_queries)
        # ... add more buttons

        # Check if the user is admin or employee and adjust visible options
        self.user_role = 'admin'  # Replace this with actual check
        if self.user_role == 'admin':
            self.create_sidebar_button("Edit Records", self.edit_records)
            # ... other admin-specific functionalities

        # Login to the database
        self.create_sidebar_button("Login to Database", self.login_to_database)

        # Initial content on the main area
        self.display_welcome_message()

    def create_sidebar_button(self, text, command):
        btn = tk.Button(self.sidebar, text=text, command=command, bg='black', fg='white')
        btn.pack(fill='x')

    def view_records(self):
        # Clear the main content area and show the view records interface
        pass

    def run_queries(self):
        # Clear the main content area and show the run queries interface
        pass

    def edit_records(self):
        # Clear the main content area and show the edit records interface
        pass

    def display_welcome_message(self):
        for widget in self.main_content.winfo_children():
            widget.destroy()
        welcome_label = tk.Label(self.main_content, text="Welcome to Blood Bank Management System", font=('Helvetica', 16))
        welcome_label.pack()

    def login_to_database(self):
        # Handle login functionality
        pass

    # ... other methods

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("1024x768")  # Set the initial size of the window
    app = BloodBankApp(root)
    root.mainloop()
