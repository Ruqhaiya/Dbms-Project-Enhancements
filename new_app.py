import tkinter as tk
from tkinter import ttk

class BloodBankApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Blood Bank Management System")
        self.sidebar_expanded = True  # Start with the sidebar expanded
        self.setup_ui()

    def setup_ui(self):
        # Sidebar Frame
        self.sidebar = tk.Frame(self.root, width=200, bg='black', relief='sunken', borderwidth=2)
        self.sidebar.pack(fill='y', side='left')

        # Hamburger Menu Button - Placed inside the sidebar frame
        self.menu_button = tk.Button(self.sidebar, text="☰", command=self.toggle_sidebar, font=("Helvetica", 14), bg='black', fg='white')
        self.menu_button.pack(anchor='nw', padx=10, pady=5)

        # Main content area - Positioned after the sidebar frame
        self.main_content = tk.Frame(self.root)
        self.main_content.pack(fill='both', expand=True, side='left')

        # Populate sidebar with buttons
        self.populate_sidebar()

        # Initial content on the main area
        self.display_welcome_message()

    def toggle_sidebar(self):
        if self.sidebar_expanded:
            # Configure the sidebar's width to be narrow
            self.sidebar.configure(width=50)
            # Hide all child widgets except the menu button
            for widget in self.sidebar.winfo_children():
                if widget != self.menu_button:
                    widget.pack_forget()
        else:
            # Expand the sidebar to its original width
            self.sidebar.configure(width=200)
            # Show all child widgets
            self.populate_sidebar()
        self.sidebar_expanded = not self.sidebar_expanded

    def populate_sidebar(self):
        # Only add the buttons if the sidebar is expanded
        if self.sidebar_expanded:
            self.create_sidebar_button("View Records", self.view_records)
            self.create_sidebar_button("Run Queries", self.run_queries)


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

    # def display_welcome_message(self):
    #     self.welcome_label = tk.Label(self.main_content, text="Welcome to Blood Bank Management System", font=('Helvetica', 16))
    #     self.welcome_label.place(relx=0.5, rely=0.5, anchor='center')

    def login_to_database(self):
        # Handle login functionality
        pass


    def display_welcome_message(self):
        # This method displays a welcome message in the main content area
        welcome_label = tk.Label(self.main_content, text="Welcome to Blood Bank Management System", font=('Helvetica', 16))
        welcome_label.place(relx=0.5, rely=0.5, anchor='center')

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("1024x768")  # Initial size of the window
    app = BloodBankApp(root)
    root.mainloop()
