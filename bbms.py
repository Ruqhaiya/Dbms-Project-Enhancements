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


class MySQLApp:
    def __init__(self, root):
        super().__init__()
        self.root = root
        self.root.title("Blood Bank Management System")
        self.root.attributes('-fullscreen', True)

        self.customFontTitle = tkFont.Font(family="Helvetica", size=18, weight="bold")
        self.customFontTitle2 = tkFont.Font(family="Helvetica", size=16, weight="bold")
        self.customFontButton = tkFont.Font(family="Helvetica", size=12)
        self.tableau_btn_font = tkFont.Font(family="Helvetica", size=10)
        self.customFontTitle2 = tkFont.Font(family="Helvetica", size=16, weight="bold")
        self.customFontFrameButton = tkFont.Font(family="Helvetica", size=10)
        self.tableau_btn_style = {'padx': 5, 'pady': 5, 'bg': 'lightblue', 'fg': 'black', 'borderwidth': 1, 'relief': 'raised'}
        menu_buttons_style = {'width': 45, 'height': 2, 'bg': 'lightblue', 'fg': 'black'}
        button_style = {'width': 20, 'height': 2, 'bg': 'lightyellow', 'fg': 'black'}

        
        self.tree = ttk.Treeview(root, columns=(1), show="headings", height="15")
        self.bloodgroup_entry = tk.Entry(root, text="Enter Blood Group(A-,A+,B-,B+,AB-,AB+,O-,O+)", width=40,  font = self.customFontTitle2)
        self.no_result_label = tk.Label(root, text="0 rows returned", font = self.customFontTitle2)
        self._entry_button = tk.Button(root, text="Ok", command=self.execute_query1,  font = self.customFontTitle2)

        # Automatically show the credentials window when the application starts
        self.root.after(3000, self.show_credentials_window)
        self.connection_details = {}
        self.selected_date = ''
        self.connection = None
        self.result_title_label = tk.Label(root, font = self.customFontTitle2)

        self.connection_status = tk.Label(self.root, text="Not Connected", fg="red")
        self.connection_status.pack(padx=10, pady=(10, 5))
        
        self.welcome_label = tk.Label(root, text="Welcome to Blood Bank Management System", font = self.customFontTitle, bg='lightblue', fg='black', height=2)
        self.welcome_label.pack(padx=20, pady=(20, 10))
        self.welcome_label.config(borderwidth=3, relief="groove", width = 40)

        self.tableau_links_frame = tk.Frame(self.root)
        self.tableau_links_frame.pack(pady=20)
        
        # URLs for your Tableau visualizations
        tableau_urls = ["https://public.tableau.com/app/profile/janani.krishnamurthy2697/viz/BloodGroup-CountBlood/BloodGroup-CountBlood?publish=yes",
                        "https://public.tableau.com/app/profile/janani.krishnamurthy2697/viz/BloodGroup-CountBlood/DonationCamp-CountBlood?publish=yes", 
                        "https://public.tableau.com/app/profile/janani.krishnamurthy2697/viz/BloodGroup-CountBlood/BloodRequestDates-CountBloodRequests?publish=yes", 
                        "https://public.tableau.com/app/profile/janani.krishnamurthy2697/viz/BloodGroup-CountBlood/Hospital-CountBloodRequests?publish=yes"]

        # Create and pack buttons side by side
        for i, url in enumerate(tableau_urls, start=0):
            tableau_vis_names = ['Count of Blood Bags', 
                                 'Total Donations - Donation Camp', 
                                 'Blood Request Trend', 
                                 'Blood requests - each Hospital']
            
            button = tk.Button(self.tableau_links_frame, text=f"{tableau_vis_names[i]}", 
                               command=lambda u=url: self.open_tableau_viz(u), font= self.tableau_btn_font, width = 25, **self.tableau_btn_style)
            button.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True, pady=10)
            button.bind("<Enter>", lambda e, btn=button: self.on_enter(e, btn))
            button.bind("<Leave>", lambda e, btn=button: self.on_leave(e, btn))

        self.query_label = tk.Label(root, text="Choose a SQL query:", font = self.customFontTitle2)
        self.query_label.pack(padx=10, pady=(10, 5))

        self.menu_button_frame = tk.Frame(self.root)
        self.menu_button_frame.pack(pady=10)

        self.q3_btn = tk.Button(self.menu_button_frame, text="Blood Supply Vs Demand - Hospital", 
                                command=self.wrap_command(self.get_user_input_q3), font = self.customFontButton, **menu_buttons_style)
        self.q3_btn.pack(padx=20, pady=(15, 5))
        self.q3_btn.bind("<Enter>", lambda e, btn=self.q3_btn: self.on_enter(e, btn))
        self.q3_btn.bind("<Leave>", lambda e, btn=self.q3_btn: self.on_leave(e, btn))

        self.q4_btn = tk.Button(self.menu_button_frame, text="Get Total Number of Donations for a Month/Day", 
                                command=self.wrap_command(self.open_query_4_window), font = self.customFontButton, **menu_buttons_style)
        self.q4_btn.pack(padx=20, pady=(15, 5))
        self.q4_btn.bind("<Enter>", lambda e, btn=self.q4_btn: self.on_enter(e, btn))
        self.q4_btn.bind("<Leave>", lambda e, btn=self.q4_btn: self.on_leave(e, btn))

        self.q6_btn = tk.Button(self.menu_button_frame, text="Get top donors list", 
                                command=self.wrap_command(self.open_query_6_window), font = self.customFontButton, **menu_buttons_style)
        self.q6_btn.pack(padx=20, pady=(15, 5))
        self.q6_btn.bind("<Enter>", lambda e, btn=self.q6_btn: self.on_enter(e, btn))
        self.q6_btn.bind("<Leave>", lambda e, btn=self.q6_btn: self.on_leave(e, btn))

        self.q1_btn = tk.Button(self.menu_button_frame, text="Total Number of Donors by Blood Group", 
                                command=self.wrap_command(self.execute_query1), font = self.customFontButton, **menu_buttons_style)
        self.q1_btn.pack(padx=20, pady=(15, 5))
        self.q1_btn.bind("<Enter>", lambda e, btn=self.q1_btn: self.on_enter(e, btn))
        self.q1_btn.bind("<Leave>", lambda e, btn=self.q1_btn: self.on_leave(e, btn))

        self.q2_btn = tk.Button(self.menu_button_frame, text="Search Donor's Information by ID", 
                                command=self.wrap_command(self.execute_query2), font = self.customFontButton, **menu_buttons_style)
        self.q2_btn.pack(padx=20, pady=(15, 5))
        self.q2_btn.bind("<Enter>", lambda e, btn=self.q2_btn: self.on_enter(e, btn))
        self.q2_btn.bind("<Leave>", lambda e, btn=self.q2_btn: self.on_leave(e, btn))

        self.q5_btn = tk.Button(self.menu_button_frame, text="Blood Group Compatibility Table", 
                                command=self.wrap_command(self.execute_query5), font = self.customFontButton, **menu_buttons_style)
        self.q5_btn.pack(padx=20, pady=(15, 5))
        self.q5_btn.bind("<Enter>", lambda e, btn=self.q5_btn: self.on_enter(e, btn))
        self.q5_btn.bind("<Leave>", lambda e, btn=self.q5_btn: self.on_leave(e, btn))

        # self.customFontButton = tkFont.Font(family="Helvetica", size=14)

        self.button_frame = tk.Frame(self.root)
        self.button_frame.pack(pady=10)

        self.main_menu_btn = tk.Button(root, text="Main Menu", 
                                       command=self.wrap_command(self.show_buttons), font = self.customFontButton, **button_style)
        
        self.exit_fullscreen_btn = tk.Button(self.button_frame, text="Exit Full screen", 
                                             command=self.exit_fullscreen, font = self.customFontFrameButton, **button_style)
        self.exit_fullscreen_btn.pack(side = tk.LEFT, padx=10, pady=(10,5))

        self.credentials_btn = Button(self.button_frame, text="Login to your Database", 
                                      command=self.show_credentials_window, font = self.customFontFrameButton,  **button_style )
        self.credentials_btn.pack(side = tk.RIGHT, padx=10, pady=(10,5))

        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)


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
                        self.credentials_btn.pack_forget()
                        self.tree.pack_forget()
                        self.no_result_label.pack(padx=20, pady=(30, 20))
                        self.button_frame.pack(pady=40)

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
                        self.credentials_btn.pack_forget()
                        self.tree.pack_forget()
                        self.no_result_label.pack(padx=20, pady=(30, 20))
                        self.button_frame.pack(pady=40)

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
                    self.credentials_btn.pack_forget()
                    self.tree.pack_forget()
                    self.no_result_label.pack(padx=20, pady=(30, 20))
                    self.button_frame.pack(pady=40)
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
                    self.credentials_btn.pack_forget()
                    self.tree.pack_forget()
                    self.no_result_label.pack(padx=20, pady=(30, 20))
                    self.button_frame.pack(pady=40)

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

        self.execute_query_4_btn = tk.Button(self.new_window, text="Get total donations", command=self.wrap_command(self.execute_query4))
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
                        self.credentials_btn.pack_forget()
                        self.tree.pack_forget()
                        self.no_result_label.pack(padx=20, pady=(30, 20))
                        self.button_frame.pack(pady=40)

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
        self.execute_query_6_btn = tk.Button(self.new_window, text="Get Top Donors List", command=self.wrap_command(self.execute_query6))
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
                        self.credentials_btn.pack_forget()
                        self.tree.pack_forget()
                        self.no_result_label.pack(padx=20, pady=(30, 20))
                        self.button_frame.pack(pady=40)
                except Error as e:
                    print("Error executing query1", e)
                finally:
                    cursor.close()
                    # self.connection.close()
    
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

    def open_tableau_viz(self, url):
        webbrowser.open(url)

    def reset_form(self):
        self.host_entry.delete(0, tk.END)
        self.database_entry.delete(0, tk.END)
        self.user_entry.delete(0, tk.END)
        self.password_entry.delete(0, tk.END)

    def open_fullscreen(self):
        self.root.attributes('-fullscreen', True)
        # self.open_fullscreen_btn.pack_forget()
        self.exit_fullscreen_btn.configure(text="Exit Full screen", command=self.exit_fullscreen)

    def exit_fullscreen(self):
        self.root.attributes('-fullscreen', False)
        # self.exit_fullscreen_btn.pack_forget()
        # self.open_fullscreen_btn.pack(padx=20, pady=(20, 10))
        self.exit_fullscreen_btn.configure(text="Full screen", command=self.open_fullscreen)

    def on_enter(self, e, btn):
        e.widget['background'] = 'white'  # Color when mouse enters the button area

    def on_leave(self, e, btn):
        e.widget['background'] =  'lightblue' # Color when mouse leaves the button area

    def wrap_command(self, original_command):
        def command_wrapper():
            self.welcome_label.configure(text="Blood Bank Management System", width = 30)
            self.tableau_links_frame.pack_forget()
            self.main_menu_btn.pack(padx=10, pady=(10, 5))
            self.button_frame.pack_forget()
            self.no_result_label.pack_forget()
            self.tree.pack_forget() 
            self.query_label.pack_forget()
            self.menu_button_frame.pack_forget()
            original_command()
            self.button_frame.pack(pady=40)
        return command_wrapper
    
    def show_buttons(self):
            self.result_title_label.pack_forget()
            self.main_menu_btn.pack_forget()
            self.tree.pack_forget()
            self._entry_button.pack_forget()
            self.tableau_links_frame.pack(pady=20)
            self.welcome_label.pack(padx=20, pady=(20, 10))
            self.query_label.pack(padx=20, pady=(20, 10))
            self.menu_button_frame.pack(pady=10)
            self.button_frame.pack(pady=40)

    def on_closing(self):
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            self.close_connection() 
            self.root.destroy() 

    def close_connection(self):
        if self.connection is not None:
            self.connection.close()
            print("Database connection closed.")

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

    def get_login_input(self):
        self.connection_details = {
            'host': self.host_entry.get(),
            'database': self.database_entry.get(),
            'user': self.user_entry.get(),
            'password': self.password_entry.get()
        }
        self.connect_to_database()

    def connect_to_database(self):
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

class SplashScreen(Toplevel):
    def __init__(self, master, image_path, duration):
        super().__init__(master)
        self.overrideredirect(True)  # Remove window decorations

        image = Image.open(image_path)
        photo_image = ImageTk.PhotoImage(image)
        label = tk.Label(self, image=photo_image)
        label.image = photo_image  # Keep a reference so it's not garbage collected
        label.pack()

        # Center the splash screen on the screen
        self.update_idletasks()  # Update geometry
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = (screen_width - image.width) // 2
        y = (screen_height - image.height) // 2
        self.geometry(f'+{x}+{y}')  # Set the position of the window

        # Show the splash screen for the specified duration then destroy
        self.after(duration, self.destroy)

    def close_splash(self):
        self.destroy()
        root.deiconify()

if __name__ == '__main__':
    root = tk.Tk()
    app = MySQLApp(root)
    root.withdraw()  # Hide the main root window

    # Show the splash screen
    splash = SplashScreen(root, 'splash_image.jpg', 2000)

    def on_splash_screen_destroy():
            root.deiconify()  # Re-display the root window


    # Call on_splash_screen_destroy when the splash screen is destroyed
    splash.bind('<Destroy>', lambda e: on_splash_screen_destroy())

    root.mainloop()
