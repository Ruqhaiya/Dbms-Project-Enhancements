import tkinter as tk
from tkinter import ttk, simpledialog, Toplevel
from tkinter import font as tkFont
import mysql.connector
from mysql.connector import Error
from tkcalendar import Calendar
from PIL import Image, ImageTk
from datetime import datetime
from tkinter import Label, Entry, Button, Toplevel, messagebox,Frame
import webbrowser
from datetime import datetime

class BloodBankApp:
    def __init__(self, root):
        self.root = root
        self.connection_status = tk.Label(self.root, text="Not Connected", fg="red")
        self.connection_status.pack(padx=10, pady=(10, 5))

        self.root.title("Blood Bank Management System")
        self.sidebar_expanded = False  # State of the sidebar
        self.setup_ui()

        self.tree = ttk.Treeview(root, columns=(1), show="headings", height="15")


        self.customFontTitle = tkFont.Font(family="Helvetica", size=18, weight="bold")
        self.customFontTitle2 = tkFont.Font(family="Helvetica", size=16, weight="bold")
        self.customFontButton = tkFont.Font(family="Helvetica", size=8)
        self.tableau_btn_font = tkFont.Font(family="Helvetica", size=10)
        self.customFontTitle2 = tkFont.Font(family="Helvetica", size=16, weight="bold")
        self.customFontFrameButton = tkFont.Font(family="Helvetica", size=10)
        self.tableau_btn_style = {'padx': 5, 'pady': 5, 'bg': 'lightblue', 'fg': 'black', 'borderwidth': 1, 'relief': 'raised'}
        menu_buttons_style = {'width': 30, 'height': 2, 'bg': 'lightblue', 'fg': 'black'}
        button_style = {'width': 20, 'height': 2, 'bg': 'lightyellow', 'fg': 'black'}


        self.connection_details = {}
        self.result_title_label = tk.Label(root, font = self.customFontTitle2)
        self.no_result_label = tk.Label(root, text="0 rows returned", font = self.customFontTitle2)

        # self.credentials_btn = Button(self.button_frame, text="Login to your Database", 
        #                               command=self.show_credentials_window, font = self.customFontFrameButton,  **button_style )
        # self.credentials_btn.pack(side = tk.RIGHT, padx=10, pady=(10,5))

        # self.menu_button_frame = tk.Frame(self.root)
        # self.menu_button_frame.pack(pady=10)

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
        self.create_sidebar_button("Login to Database", self.show_credentials_window)
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

        menu_buttons_style = {'width': 30, 'height': 2, 'bg': 'lightblue', 'fg': 'black'}


        self.q3_btn = tk.Button(self.main_content, text="Blood Supply Vs Demand - Hospital", 
                                command=self.get_user_input_q3, font = self.customFontButton, **menu_buttons_style)
        self.q3_btn.pack(padx=20, pady=(15, 5))
        self.q3_btn.bind("<Enter>", lambda e, btn=self.q3_btn: self.on_enter(e, btn))
        self.q3_btn.bind("<Leave>", lambda e, btn=self.q3_btn: self.on_leave(e, btn))

        self.q4_btn = tk.Button(self.main_content, text="Get Total Number of Donations for a Month/Day", 
                                command=self.open_query_4_window, font = self.customFontButton, **menu_buttons_style)
        self.q4_btn.pack(padx=20, pady=(15, 5))
        self.q4_btn.bind("<Enter>", lambda e, btn=self.q4_btn: self.on_enter(e, btn))
        self.q4_btn.bind("<Leave>", lambda e, btn=self.q4_btn: self.on_leave(e, btn))

        self.q6_btn = tk.Button(self.main_content, text="Get top donors list", 
                                command=self.open_query_6_window, font = self.customFontButton, **menu_buttons_style)
        self.q6_btn.pack(padx=20, pady=(15, 5))
        self.q6_btn.bind("<Enter>", lambda e, btn=self.q6_btn: self.on_enter(e, btn))
        self.q6_btn.bind("<Leave>", lambda e, btn=self.q6_btn: self.on_leave(e, btn))

        self.q1_btn = tk.Button(self.main_content, text="Total Number of Donors by Blood Group", 
                                command=self.execute_query1, font = self.customFontButton, **menu_buttons_style)
        self.q1_btn.pack(padx=20, pady=(15, 5))
        self.q1_btn.bind("<Enter>", lambda e, btn=self.q1_btn: self.on_enter(e, btn))
        self.q1_btn.bind("<Leave>", lambda e, btn=self.q1_btn: self.on_leave(e, btn))

        self.q2_btn = tk.Button(self.main_content, text="Search Donor's Information by ID", 
                                command=self.execute_query2, font = self.customFontButton, **menu_buttons_style)
        self.q2_btn.pack(padx=20, pady=(15, 5))
        self.q2_btn.bind("<Enter>", lambda e, btn=self.q2_btn: self.on_enter(e, btn))
        self.q2_btn.bind("<Leave>", lambda e, btn=self.q2_btn: self.on_leave(e, btn))

        self.q5_btn = tk.Button(self.main_content, text="Blood Group Compatibility Table", 
                                command=self.execute_query5, font = self.customFontButton, **menu_buttons_style)
        self.q5_btn.pack(padx=20, pady=(15, 5))
        self.q5_btn.bind("<Enter>", lambda e, btn=self.q5_btn: self.on_enter(e, btn))
        self.q5_btn.bind("<Leave>", lambda e, btn=self.q5_btn: self.on_leave(e, btn))


    def execute_query1(self):
        blood_group = simpledialog.askstring("Input", "Enter Blood Group:")

        if blood_group:
            if self.connection is not None:
                try:
                    cursor = self.connection.cursor()
                    query = "SELECT BloodGroup, COUNT(*) AS NumberOfDonors FROM Donor WHERE BloodGroup = %s GROUP BY BloodGroup;"
                    cursor.execute(query, (blood_group,))
                    records = cursor.fetchall()
                    self.result_title_label.configure(text = "Number of Donor by Blood Group")
                    self.result_title_label.pack(padx=10, pady=(10, 5))
                    if records:
                        self.no_result_label.pack_forget()
                        columns = [desc[0] for desc in cursor.description]
                        self.tree['columns'] = columns
                        self.tree.pack(padx=20, pady=(20, 10), side='top', fill='x', expand=True)
                        for col in columns:
                            self.tree.heading(col, text=col)
                            self.display_results(records, columns)
                    else:
                        # self.credentials_btn.pack_forget()
                        self.tree.pack_forget()
                        self.no_result_label.pack(padx=20, pady=(30, 20))
                        # self.button_frame.pack(pady=40)

                except Error as e:
                    print("Error executing query1", e)
                finally:
                    cursor.close()
    def execute_query2(self):
        donorid = simpledialog.askinteger("Input", "Enter Donor ID:")
        if donorid:
            if self.connection is not None:
                try:
                    cursor = self.connection.cursor()
                    query = '''SELECT DonorID, CONCAT(FirstName,' ', LastName) AS \'Full Name\', 
                                DOB AS \'Date Of Birth\', Gender, BloodGroup, Phone, Address, LastDonationDate
                                FROM Donor 
                                WHERE DonorID = %s;'''
                    cursor.execute(query, (donorid,))
                    records = cursor.fetchall()
                    self.result_title_label.configure(text = "Donor's Information")
                    self.result_title_label.pack(padx=10, pady=(10, 5))
                    if records:
                        self.no_result_label.pack_forget()
                        columns = [desc[0] for desc in cursor.description]
                        self.tree['columns'] = columns
                        self.tree.pack(padx=20, pady=(20, 10), side='top', fill='x', expand=True)
                        for col in columns:
                            self.tree.heading(col, text=col)
                        self.display_results(records, columns)
                    else:
                        # self.credentials_btn.pack_forget()
                        self.tree.pack_forget()
                        self.no_result_label.pack(padx=20, pady=(30, 20))
                        # self.button_frame.pack(pady=40)

                except Error as e:
                    print("Error executing query2", e)
                finally:
                    cursor.close()

    
    def get_user_input_q3(self):
        self.input_window = tk.Toplevel(self.root)
        self.input_window.title("Enter Query Parameters")

        # Hospital ID Entry
        tk.Label(self.input_window, text="Hospital ID:").pack()
        self.hospital_id_entry = tk.Entry(self.input_window)
        self.hospital_id_entry.pack()

        # Blood Group Entry
        tk.Label(self.input_window, text="Blood Group:").pack()
        self.blood_group_entry = tk.Entry(self.input_window)
        self.blood_group_entry.pack()

        # Name input
        tk.Label(self.input_window, text="Enter Name or Starting Letter:").pack()
        self.hospital_name_entry = tk.Entry(self.input_window)
        self.hospital_name_entry.pack()

        # Submit Button
        submit_button = tk.Button(self.input_window, text="Submit", command=self.execute_query3)
        submit_button.pack()
    
    def execute_query3(self):
        self.hospital_id = self.hospital_id_entry.get()
        self.blood_group = self.blood_group_entry.get()
        self.hospital_name = self.hospital_name_entry.get()

        if self.blood_group == '':
            self.blood_group = None
        if self.hospital_id == '':
            self.hospital_id = None
        if self.hospital_name == '':
            self.hospital_name = None
        else:
            self.hospital_name = self.hospital_name + '%'

        if self.connection is not None:
            try:
                cursor = self.connection.cursor()
                query = """SELECT 
                            h.HospitalID,
                            h.HospitalName,
                            COALESCE(SUM(dr.Quantity), 0) - COALESCE(SUM(br.Quantity), 0) AS SupplyDemandGap,
                            COALESCE(SUM(dr.Quantity), 0) AS TotalBloodDonated,
                            COALESCE(SUM(br.Quantity), 0) AS TotalBloodRequested,
                            h.Address,
                            h.Phone,
                            h.Email,
                            h.ContactPersonName
                        FROM 
                            Hospital h
                        LEFT JOIN 
                            BloodRequest br ON h.HospitalID = br.HospitalID AND (br.BloodGroup = %s OR %s IS NULL)
                        LEFT JOIN 
                            DonationEntry dr ON br.BloodRequestID = dr.BloodRequestID
                        WHERE 
                            (h.HospitalID = %s OR %s IS NULL)
                            AND (h.HospitalName LIKE %s OR %s IS NULL)
                        GROUP BY 
                            h.HospitalID, h.HospitalName
                        ORDER BY 
                            SupplyDemandGap DESC;"""
                
                params = (self.blood_group, self.blood_group, 
                          self.hospital_id, self.hospital_id,
                          self.hospital_name, self.hospital_name)
                # print(query)
                cursor.execute(query, params)
                records = cursor.fetchall()
                
                self.result_title_label.configure(text = "Blood Supply Vs Demand")
                self.result_title_label.pack(padx=10, pady=(10, 5))
                if records:
                    self.no_result_label.pack_forget()
                    columns = [desc[0] for desc in cursor.description]
                    self.tree['columns'] = columns

                    self.tree.pack(padx=20, pady=(20, 10), side='top', fill='x', expand=True)
                    for col in columns:
                        self.tree.heading(col, text=col)
                    self.display_results(records, columns)
                else:
                    # self.credentials_btn.pack_forget()
                    self.tree.pack_forget()
                    self.no_result_label.pack(padx=20, pady=(30, 20))
                    # self.button_frame.pack(pady=40)
            except Error as e:
                print("Error executing query7", e)
            finally:
                cursor.close()

    def execute_query4(self):
        date_selected = self.selected_date
        month_selected = self.month_combobox.get()
        year_selected = self.year_combobox.get()

        if date_selected:
            date_formatted = datetime.strptime(date_selected, "%m/%d/%y")
            date_year = date_formatted.year

            if date_formatted.month<10:
                date_month = '0'+ str(date_formatted.month)
            else:
                date_month = date_formatted.month

            if date_formatted.day<10:
                date_day = '0'+ str(date_formatted.day)
            else:
                date_day = date_formatted.day

        if self.connection is not None:
            try:
                cursor = self.connection.cursor()
                if month_selected and year_selected:
                    if len(month_selected) == 1:
                        month_selected = '0'+month_selected
                    query = '''SELECT 
                                DATE_FORMAT(DonationTS, '%Y-%m') AS YearMonth, 
                                COUNT(DonationEntryID) AS NumberOfDonations, 
                                SUM(Quantity) AS TotalQuantityDonated
                                FROM DonationEntry
                                WhERE  DATE_FORMAT(DonationTS, '%Y-%m') = \'{}-{}\'
                                GROUP BY DATE_FORMAT(DonationTS, '%Y-%m')
                                ORDER BY YearMonth desc;'''.format(year_selected,month_selected)
                else:
                    query = '''
                        SELECT 
                        DATE_FORMAT(DonationTS, '%Y-%m-%d') AS Date, 
                        COUNT(DonationEntryID) AS NumberOfDonations, 
                        SUM(Quantity) AS TotalQuantityDonated
                        FROM DonationEntry
                        WhERE  DATE_FORMAT(DonationTS, '%Y-%m-%d') = \'{}-{}-{}\'
                        GROUP BY DATE_FORMAT(DonationTS, '%Y-%m-%d');'''.format(date_year, date_month, date_day)

                cursor.execute(query)
                records = cursor.fetchall()
                self.result_title_label.configure(text = "Total Number of Donations")
                self.result_title_label.pack(padx=10, pady=(10, 5))
                if records:
                    self.no_result_label.pack_forget()
                    columns = [desc[0] for desc in cursor.description]
                    self.tree['columns'] = columns
                    self.tree.pack(padx=20, pady=(20, 10), side='top', fill='x', expand=True)
                    for col in columns:
                        self.tree.heading(col, text=col)
                    self.display_results(records, columns)
                else:
                    # self.credentials_btn.pack_forget()
                    self.tree.pack_forget()
                    self.no_result_label.pack(padx=20, pady=(30, 20))
                    # self.button_frame.pack(pady=40)

            except Error as e:
                print("Error executing query1", e)
            finally:
                    cursor.close()

    def open_query_4_window(self):
        self.new_window = Toplevel(self.root)
        self.new_window.title("Total Donations by Month, Year, Day")        
        month_options = [i for i in range(1,12)]
        year_options = list(range(2018, 2024 + 1))

        # month input
        self.selected_month_label = tk.Label(self.new_window, text="Select Month:")
        self.selected_month_label.pack()
        self.month_combobox = ttk.Combobox(self.new_window, values=month_options)
        self.month_combobox.pack(pady=10)


        # ID input
        self.year_label = tk.Label(self.new_window, text="Select Year:")
        self.year_label.pack()
        self.year_combobox = ttk.Combobox(self.new_window, values=year_options)
        self.year_combobox.pack(pady=10)

        self.cal = Calendar(self.new_window, selectmode="day", year=2022, month=2, day=28)
        self.cal.pack(pady=20)

        self.select_date_button = tk.Button(self.new_window, text="Select Date", command=self.on_date_selected)
        self.select_date_button.pack(pady=10)
        
        self.selected_date_label = tk.Label(self.new_window, text="")
        self.selected_date_label.pack(pady=10)

        self.execute_query_4_btn = tk.Button(self.new_window, text="Get total donations", command=self.execute_query4)
        self.execute_query_4_btn.pack(pady=10)

    def on_date_selected(self):
        self.selected_date = self.cal.get_date()
        self.selected_date_label.config(text=f"Selected Date: {self.selected_date}")
        
    def execute_query5(self):

        if True:
            if self.connection is not None:
                try:
                    cursor = self.connection.cursor()
                    query = "SELECT * FROM BloodGroupCompatibility"
                    cursor.execute(query)
                    records = cursor.fetchall()
                    self.result_title_label.configure(text = "Blood Group Compatibility Table")
                    self.result_title_label.pack(padx=5, pady=(10, 5))
                    if records:
                        self.no_result_label.pack_forget()
                        columns = [desc[0] for desc in cursor.description]
                        self.tree['columns'] = columns
                        self.tree.pack(padx=20, pady=(20, 10), side='top', fill='x', expand=True)
                        for col in columns:
                            self.tree.heading(col, text=col)
                        self.display_results(records, columns)
                    else:
                        # self.credentials_btn.pack_forget()
                        self.tree.pack_forget()
                        self.no_result_label.pack(padx=20, pady=(30, 20))
                        # self.button_frame.pack(pady=40)

                except Error as e:
                    print("Error executing query1", e)
                finally:
                    cursor.close()
                    # self.connection.close()
                    

    def open_query_6_window(self):
        # Create a new Toplevel window
        self.new_window = Toplevel(self.root)
        self.new_window.title("Top N Donors")

        options = ["5", "10", "15", "20"]
        self.combobox = ttk.Combobox(self.new_window, values=options)
        self.combobox.pack(pady=10)
        self.execute_query_6_btn = tk.Button(self.new_window, text="Get Top Donors List", command=self.execute_query6)
        self.execute_query_6_btn.pack(pady=10)

    def execute_query6(self):
        no_of_donors = self.combobox.get()
        if no_of_donors:
            if self.connection is not None:
                try:
                    cursor = self.connection.cursor()
                    query ='''SELECT d.DonorID, CONCAT(d.FirstName, d.LastName) AS \'Full Name\',
                    TIMESTAMPDIFF(YEAR, DOB, CURDATE()) AS Age, COUNT(de.DonationEntryID) AS DonationEntryCount
                    FROM DonationEntry de
                    JOIN Donor d ON de.DonorID = d.DonorID
                    GROUP BY d.DonorID
                    ORDER BY DonationEntryCount DESC
                    LIMIT {};'''.format(no_of_donors)
                    cursor.execute(query)
                    records = cursor.fetchall()
                    s= 'List of Top {} Donors'.format(no_of_donors)
                    self.result_title_label.configure(text = s)
                    self.result_title_label.pack(padx=10, pady=(10, 5))
                    if records:
                        self.no_result_label.pack_forget()
                        columns = [desc[0] for desc in cursor.description]
                        self.tree['columns'] = columns
                        self.tree.pack(padx=20, pady=(20, 10), side='top', fill='x', expand=True)
                        for col in columns:
                            self.tree.heading(col, text=col)
                        self.display_results(records, columns)
                    else:
                        # self.credentials_btn.pack_forget()
                        self.tree.pack_forget()
                        self.no_result_label.pack(padx=20, pady=(30, 20))
                        # self.button_frame.pack(pady=40)
                except Error as e:
                    print("Error executing query1", e)
                finally:
                    cursor.close()
                    # self.connection.close()
    

    def edit_records(self):
        # Clear the main content area and show the edit records interface
        pass

    def display_welcome_message(self):
        self.welcome_label = tk.Label(self.main_content, text="Welcome to Blood Bank Management System", font=('Helvetica', 16))
        self.welcome_label.place(relx=0.5, rely=0.5, anchor='center')

    def get_login_input(self):
        self.connection_details = {
            'host': self.host_entry.get(),
            'database': self.database_entry.get(),
            'user': self.user_entry.get(),
            'password': self.password_entry.get()
        }
        self.login_to_database()

    def login_to_database(self):
        try:
            self.connection = mysql.connector.connect(host=self.connection_details['host'], 
                                                      database= self.connection_details['database'],
                                                      user = self.connection_details['user'],
                                                      password = self.connection_details['password'])
            messagebox.showinfo("Success", "Connection to the database was successful.")
            if self.connection.is_connected():
                self.connection_status.configure(text="Connected", fg="green")
                self.cred_window.destroy()
        except Error as e:
            messagebox.showerror("Connection Failed", "Failed to connect to the database: {}".format(e))
            self.connection_status.configure(text="Not Connected", fg="red")

        
    def show_credentials_window(self):
        self.cred_window = Toplevel(self.root)
        self.cred_window.title("Database Credentials")
        
        self.cred_window.configure(background='#f0f0f0')

        window_width = 300
        window_height = 250  

        # Get the screen dimensions
        screen_width = self.cred_window.winfo_screenwidth()
        screen_height = self.cred_window.winfo_screenheight()

        # Calculate the center position
        center_x = int(screen_width / 2 - window_width / 2)
        center_y = int(screen_height / 2 - window_height / 2)

        # Set the position and size of the window
        self.cred_window.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')

        label_style = {'background': '#f0f0f0', 'padx': 5, 'pady': 5}
        entry_style = {'borderwidth': 2, 'relief': 'groove', 'width': 20}
        button_frame_style = {'padx': 10, 'pady': 10, 'background': '#f0f0f0'}
        
        # Create a frame to hold the buttons and give it the same background as the window
        button_frame = Frame(self.cred_window, **button_frame_style)
        button_frame.grid(row=4, column=0, columnspan=2)

        entry_font = tkFont.Font(family="Helvetica", size=12)
        label_font = tkFont.Font(family="Helvetica", size=12)

        Label(self.cred_window, text="Host:", **label_style, font=label_font).grid(row=0, column=0, sticky='e')
        self.host_entry = Entry(self.cred_window, font=entry_font, **entry_style)
        self.host_entry.grid(row=0, column=1, padx=5, pady=10)
        self.host_entry.insert(0, "CSSQL")  # Default host

        Label(self.cred_window, text="Database:", **label_style, font=label_font).grid(row=1, column=0, sticky='e')
        self.database_entry = Entry(self.cred_window, font=entry_font, **entry_style)
        self.database_entry.grid(row=1, column=1, padx=5, pady=10)
        self.database_entry.insert(0, "mm_team02_02")  # Default database

        Label(self.cred_window, text="User:", **label_style, font=label_font).grid(row=2, column=0, sticky='e')
        self.user_entry = Entry(self.cred_window, font=entry_font, **entry_style)
        self.user_entry.grid(row=2, column=1, padx=5, pady=10)
        self.user_entry.insert(0, "mm_team02_02")  # Default user

        Label(self.cred_window, text="Password:", **label_style, font=label_font).grid(row=3, column=0, sticky='e')
        self.password_entry = Entry(self.cred_window, show="*", font=entry_font, **entry_style)
        self.password_entry.grid(row=3, column=1, padx=5, pady=10)
        self.password_entry.insert(0, "mm_team02_02Pass-")

        reset_button = Button(button_frame, text="Reset Form", command=self.reset_form, width=10,background= '#d9d9d9')
        connect_button = Button(button_frame, text="Connect", command=self.get_login_input, width=10,background= '#d9d9d9')
        reset_button.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10), pady=10)
        connect_button.pack(side=tk.RIGHT, fill=tk.X, expand=True)


    def reset_form(self):
        self.host_entry.delete(0, tk.END)
        self.database_entry.delete(0, tk.END)
        self.user_entry.delete(0, tk.END)
        self.password_entry.delete(0, tk.END)

    def display_results(self, records, columns):
        for col in columns:
            self.tree.heading(col, text=col, anchor=tk.W)
            self.tree.column(col, anchor=tk.W, width=tkFont.Font().measure(col.title()))

        # Configure row tags for striped row colors
        self.tree.tag_configure('oddrow', background='lightblue')
        self.tree.tag_configure('evenrow', background='white')

        # Clear previous results
        for i in self.tree.get_children():
            self.tree.delete(i)

        # Insert new records with striped rows
        for index, row in enumerate(records):
            tag = 'evenrow' if index % 2 == 0 else 'oddrow'
            self.tree.insert("", tk.END, values=row, tags=(tag,))
    
    def on_enter(self, e, btn):
        e.widget['background'] = 'white'  # Color when mouse enters the button area

    def on_leave(self, e, btn):
        e.widget['background'] =  'lightblue' # Color when mouse leaves the button area

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("1024x768")  # Set the initial size of the window
    app = BloodBankApp(root)
    root.mainloop()
