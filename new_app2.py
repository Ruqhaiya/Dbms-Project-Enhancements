import tkinter as tk
from tkinter import ttk

class BloodBankApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Blood Bank Management System")
        self.sidebar_expanded = False  # State of the sidebar
        self.setup_ui()

    def setup_ui(self):
        # Create the sidebar frame (initially hidden)
        self.sidebar = tk.Frame(self.root, width=200, bg='black')
        
        # Main content area
        self.main_content = tk.Frame(self.root)
        self.main_content.pack(fill='both', expand=True, side='left')

        # Menu button (hamburger button)
        self.menu_button = tk.Button(self.main_content, text="☰", command=self.toggle_sidebar, font=("Helvetica", 12))
        self.menu_button.pack(anchor='nw')

        # Initial content on the main area
        self.display_welcome_message()

    def toggle_sidebar(self):
        # This function will toggle the visibility of the sidebar
        if self.sidebar_expanded:
            self.sidebar.pack_forget()  # Hide the sidebar
        else:
            self.sidebar.pack(fill='y', side='left')  # Show the sidebar
            self.populate_sidebar()  # Populate the sidebar if it's not already populated
        self.sidebar_expanded = not self.sidebar_expanded  # Toggle the state

    def populate_sidebar(self):
        # Create buttons for the sidebar (they will only show when the sidebar is visible)
        self.create_sidebar_button("View Records", self.view_records)
        self.create_sidebar_button("Run Queries", self.run_queries)

        # Check if the user is admin or employee and adjust visible options
        self.user_role = 'admin'  # Replace with actual role check
        if self.user_role == 'admin':
            self.create_sidebar_button("Edit Records", self.edit_records)
            # ... other admin-specific functionalities

        # Login to the database
        self.create_sidebar_button("Login to Database", self.login_to_database)

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
        welcome_label = tk.Label(self.main_content, text="Welcome to Blood Bank Management System", font=('Helvetica', 16))
        welcome_label.place(relx=0.5, rely=0.5, anchor='center')

    def login_to_database(self):
        # Handle login functionality
        pass

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("1024x768")  # Set the initial size of the window
    app = BloodBankApp(root)
    root.mainloop()
