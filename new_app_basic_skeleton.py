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

        self.menu_button = tk.Button(self.root, text="☰", command=self.toggle_sidebar, font=("Helvetica", 12))
        self.menu_button.pack(anchor='nw', padx=10, pady=5)
        # Main content area
        self.main_content = tk.Frame(self.root)
        self.main_content.pack(fill='both', expand=True, side='left')

        # Menu button (hamburger button)
        # self.menu_button = tk.Button(self.root, text="☰", command=self.toggle_sidebar, font=("Helvetica", 12))
        # self.menu_button.pack(anchor='nw')
        
        # Initial content on the main area
        self.display_welcome_message()

        self.populate_sidebar()

    def toggle_sidebar(self):
        # This function will toggle the visibility of the sidebar\
        if self.sidebar_expanded:
            self.sidebar.pack_forget()  # Hide the sidebar
        else:
            self.menu_button.pack(anchor='nw', padx=10, pady=5)
            self.main_content.pack_forget()
            self.sidebar.pack(fill='y', side='left')  # Show the sidebar
        self.main_content.pack(fill='both', expand=True, side='left')
        self.sidebar_expanded = not self.sidebar_expanded  # Toggle the state

    def populate_sidebar(self):
        # self.welcome_label.pack_forget()

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
        # self.welcome_label.place(relx=0.5, rely=0.5, anchor='center')

    def create_sidebar_button(self, text, command):
        btn = tk.Button(self.sidebar, text=text, command=command, bg='black', fg='white')
        btn.pack(fill='x')

    def view_records(self):
        # Clear the main content area and show the view records interface
        pass

    def run_queries(self):
        # Clear the main content area and show the run queries interface
        for widget in self.main_content.winfo_children():
            widget.destroy()

        # Add a label to the main content for the section header
        query_label = tk.Label(self.main_content, text="Select and Run Queries", font=('Helvetica', 16))
        query_label.pack(pady=10)

        # Add a dropdown to select the query type (expand this with actual queries)
        query_options = ["Top N Donors", "Other Query 1", "Other Query 2"]  # Populate with actual query options
        self.selected_query = tk.StringVar()
        self.selected_query.set(query_options[0])  # Default value

        query_dropdown = ttk.Combobox(self.main_content, textvariable=self.selected_query, values=query_options)
        query_dropdown.pack(pady=5)

        # Slider for selecting 'N' in 'Top N Donors'
        self.slider_label = tk.Label(self.main_content, text="Select N for 'Top N Donors'")
        self.slider_label.pack()

        self.n_slider = tk.Scale(self.main_content, from_=1, to=100, orient='horizontal')
        self.n_slider.pack()

        # Button to run the selected query
        run_button = tk.Button(self.main_content, text="Run Query", command=self.login_to_database)
        run_button.pack(pady=20)



    def edit_records(self):
        # Clear the main content area and show the edit records interface
        pass

    def display_welcome_message(self):
        self.welcome_label = tk.Label(self.main_content, text="Welcome to Blood Bank Management System", font=('Helvetica', 16))
        self.welcome_label.place(relx=0.5, rely=0.5, anchor='center')

    def login_to_database(self):
        # Handle login functionality
        pass

    

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("1024x768")  # Set the initial size of the window
    app = BloodBankApp(root)
    root.mainloop()
