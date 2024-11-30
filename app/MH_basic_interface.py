import tkinter as tk
from tkinter import ttk
from tkinter import filedialog, messagebox
from tkcalendar import DateEntry
import Generaltab_interface
import people_interface  # Ensure this module contains a class named people_interface
import MH_assessment
import MH_treatmentPlan_interface
import va_tab_interface
import case_notes
import database_lookup_search
import psycopg2
from datetime import datetime
import configparser
import os
import math  # For pagination calculations


class MHBasicInterface(tk.Frame):

    def __init__(self, parent, controller):

        tk.Frame.__init__(self, parent)

        self.controller = controller
        
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Create a canvas and a scrollbar
        canvas = tk.Canvas(self)
        scrollbar = ttk.Scrollbar(self, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)

        # Configure the canvas and scrollbar
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        # Window in the canvas
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")

        # Scrollbar to canvas
        canvas.configure(yscrollcommand=scrollbar.set)

        # Use grid over pack for interface linking
        canvas.grid(row=0, column=0, sticky="nsew")
        scrollbar.grid(row=0, column=1, sticky="ns")

        # Navigation Buttons
        button_frame = ttk.Frame(scrollable_frame)
        button_frame.grid(row=0, column=0, columnspan=7, padx=5, pady=5, sticky='w')

        # Create a list of tuples with button text and corresponding function placeholders
        nav_buttons = [
            ("Lookup", self.show_lookup_page),
            ("General", self.show_general_tab),
            ("People", self.show_people_tab),
            ("Mental Health - Basic", self.show_mh_basic),
            ("Mental Health - Assessment", self.show_mh_assessment),
            ("Mental Health - Treatment Plan", self.show_mh_treatment_plan),
            ("VA", self.show_va_tab),
            ("Case Notes", self.show_case_notes),
        ]

        for btn_text, btn_command in nav_buttons:
            button = ttk.Button(button_frame, text=btn_text, command=btn_command)
            button.pack(side='left', padx=5)

        # Reload button - fully reloads the application
        refresh_button = ttk.Button(button_frame, text="Reload", command=controller.refresh)
        refresh_button.pack(side='right', padx=5)

        # Initialize identifiers
        self.case_id = 1  # Default value; adjust as needed
        self.cac_id = 1   # Default value; adjust as needed

        # Initialize database connection
        self.conn = self.connect_to_database()
        self.cur = self.conn.cursor()

        # In-memory storage for referrals and POCs
        self.referrals_data = []  # List to store referrals
        self.poc_data = []        # List to store points of contact

        # Function for line numbering
        def create_line_numbered_label(frame, text, line_number):
            line_number_label = ttk.Label(frame, text=f"({line_number})")
            line_number_label.grid(row=line_number - 1, column=0, sticky="w", padx=5)
            label = ttk.Label(frame, text=text)
            label.grid(row=line_number - 1, column=1, sticky="w", padx=5)

        # Save and Cancel Buttons
        button_frame = ttk.Frame(scrollable_frame)
        button_frame.grid(row = 1, column=0, pady=10, padx=10)
        save_button = ttk.Button(button_frame, text="Save", command=self.save_data)
        save_button.pack(side="left", padx=5)
        cancel_button = ttk.Button(button_frame, text="Cancel", command=self.cancel)
        cancel_button.pack(side="left", padx=5)

        # MDT Review checkbox at the top
        ready_mdt_var = tk.BooleanVar(value=False)
        self.ready_mdt_var = ready_mdt_var
        mdt_frame = tk.Frame(scrollable_frame)
        mdt_frame.grid(row=2, column=0, pady=10)
        ttk.Checkbutton(mdt_frame, text="Ready for MDT Review", variable=ready_mdt_var).pack()

        # Incoming Referral section
        incoming_frame = tk.LabelFrame(scrollable_frame, text="Incoming Referral", padx=10, pady=10)
        incoming_frame.grid(row=3, column=0, padx=10, pady=5, sticky='w')

        # Date (uses DateEntry)
        ttk.Label(incoming_frame, text="Date").grid(row=0, column=0, padx=5, pady=5)
        date_entry = DateEntry(incoming_frame, width=12, background='darkblue', foreground='white', borderwidth=2)
        date_entry.grid(row=0, column=1, padx=5, pady=5)
        self.date_entry = date_entry

        ttk.Label(incoming_frame, text="Referral Source:").grid(row=1, column=0, sticky="w")
        referral_source = ttk.Combobox(incoming_frame, values=self.get_existing_agencies())
        referral_source.grid(row=1, column=1, padx=5, pady=5)
        self.referral_source = referral_source

        # "+ Add" button for referral source dropdown
        ttk.Button(incoming_frame, text="+ Add", command=self.add_referral_source_popup).grid(row=1, column=2, padx=5, pady=5)

        ttk.Label(incoming_frame, text="Person").grid(row=2, column=0, padx=5, pady=5)
        person_combo = ttk.Combobox(incoming_frame, values=self.get_existing_personnel())
        person_combo.grid(row=2, column=1, padx=5, pady=5)
        self.person_combo = person_combo

        # "+ Add" button next to personnel dropdown
        ttk.Button(incoming_frame, text="+ Add", command=self.add_personnel_popup).grid(row=2, column=2, padx=5, pady=5)

        # Custom fields section
        custom_frame = tk.LabelFrame(scrollable_frame, text="Custom Fields", padx=10, pady=10)
        custom_frame.grid(row=4, column=0, padx=10, pady=5, sticky='w')

        # MH- Abuse Type
        ttk.Label(custom_frame, text="MH- Abuse Type").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        abuse_type_yes_var = tk.BooleanVar(value=False)
        abuse_type_no_var = tk.BooleanVar(value=False)
        ttk.Checkbutton(custom_frame, text="Yes", variable=abuse_type_yes_var).grid(row=0, column=1, sticky="w")
        ttk.Checkbutton(custom_frame, text="No", variable=abuse_type_no_var).grid(row=0, column=2, sticky="w")
        self.abuse_type_yes_var = abuse_type_yes_var
        self.abuse_type_no_var = abuse_type_no_var

        # Abuse types checkboxes
        abuse_types = ["Bullying", "Addiction", "DV", "PA", "SA"]
        self.abuse_type_vars = {}
        for idx, abuse in enumerate(abuse_types):
            var = tk.BooleanVar(value=False)
            self.abuse_type_vars[abuse] = var
            ttk.Checkbutton(custom_frame, text=abuse, variable=var).grid(row=1 + idx // 3, column=1 + idx % 3, sticky="w")

        # Line numbering continues after MH- Abuse Type
        line_number = 3  # Starting line number after abuse types

        create_line_numbered_label(custom_frame, "Referred for Mental Health Services", line_number)
        mh_services_var = tk.BooleanVar(value=False)
        no_mh_services_var = tk.BooleanVar(value=False)
        ttk.Checkbutton(custom_frame, text="Yes", variable=mh_services_var).grid(row=line_number - 1, column=2, sticky="w")
        ttk.Checkbutton(custom_frame, text="No", variable=no_mh_services_var).grid(row=line_number - 1, column=3, sticky="w")
        self.mh_services_var = mh_services_var
        self.no_mh_services_var = no_mh_services_var

        line_number += 1
        create_line_numbered_label(custom_frame, "Status of Mental Health Referral", line_number)
        status_accepted_var = tk.BooleanVar(value=False)
        status_declined_var = tk.BooleanVar(value=False)
        ttk.Checkbutton(custom_frame, text="Accepted: Attending Therapy Sessions", variable=status_accepted_var).grid(row=line_number - 1, column=2, sticky="w")
        ttk.Checkbutton(custom_frame, text="Declined: Already receiving therapy services", variable=status_declined_var).grid(row=line_number - 1, column=3, sticky="w")
        self.status_accepted_var = status_accepted_var
        self.status_declined_var = status_declined_var

        line_number += 1
        create_line_numbered_label(custom_frame, "Seen For MH Services Elsewhere", line_number)
        mh_services_elsewhere = ttk.Entry(custom_frame)
        mh_services_elsewhere.grid(row=line_number - 1, column=2, columnspan=2, padx=5, pady=5, sticky="we")
        self.mh_services_elsewhere = mh_services_elsewhere

        line_number += 1
        create_line_numbered_label(custom_frame, "Psyco/Social Notes", line_number)
        psyc_notes_entry = ttk.Entry(custom_frame)
        psyc_notes_entry.grid(row=line_number - 1, column=2, columnspan=2, padx=5, pady=5, sticky="we")
        self.psyc_notes_entry = psyc_notes_entry

        line_number += 1
        create_line_numbered_label(custom_frame, "MH Extended Services Candidate", line_number)
        # The options for the dropdown based on NCA-Trak
        options = ["If Needed"] + [str(i) for i in range(4, 34)] + ["If Space Allows"]
        mh_extended_services = ttk.Combobox(custom_frame, values=options)
        mh_extended_services.grid(row=line_number - 1, column=2, columnspan=2, padx=5, pady=5, sticky="we")
        self.mh_extended_services = mh_extended_services

        line_number += 1
        create_line_numbered_label(custom_frame, "MH - Services Custom", line_number)
        custom_field_6 = ttk.Entry(custom_frame)
        custom_field_6.grid(row=line_number - 1, column=2, columnspan=2, padx=5, pady=5, sticky="we")
        self.custom_field_6 = custom_field_6

        line_number += 1
        create_line_numbered_label(custom_frame, "MH - Services Custom", line_number)
        custom_field_7 = ttk.Entry(custom_frame)
        custom_field_7.grid(row=line_number - 1, column=2, columnspan=2, padx=5, pady=5, sticky="we")
        self.custom_field_7 = custom_field_7

        line_number += 1
        create_line_numbered_label(custom_frame, "Client Declined Services", line_number)
        client_declined_var = tk.BooleanVar(value=False)
        no_client_declined_var = tk.BooleanVar(value=False)
        ttk.Checkbutton(custom_frame, text="Yes", variable=client_declined_var).grid(row=line_number - 1, column=2, sticky="w")
        ttk.Checkbutton(custom_frame, text="No", variable=no_client_declined_var).grid(row=line_number - 1, column=3, sticky="w")
        self.client_declined_var = client_declined_var
        self.no_client_declined_var = no_client_declined_var

        line_number += 1
        create_line_numbered_label(custom_frame, "Why Client Declined Services", line_number)
        client_declined_reason = ttk.Entry(custom_frame)
        client_declined_reason.grid(row=line_number - 1, column=2, columnspan=2, padx=5, pady=5, sticky="we")
        self.client_declined_reason = client_declined_reason

        # Telehealth Services Section
        telehealth_frame = tk.LabelFrame(scrollable_frame, text="Telehealth Services", padx=10, pady=10)
        telehealth_frame.grid(row=5, column=0, padx=10, pady=5, sticky='w')

        # Number of miles saved
        ttk.Label(telehealth_frame, text="Number of Miles Saved Providing Telehealth Services Per Session:").grid(row=0, column=0, padx=5, pady=5)
        miles_saved_combo = ttk.Combobox(telehealth_frame, values=["0-10 miles", "10-20 miles", "20+ miles"])
        miles_saved_combo.grid(row=0, column=1, padx=5, pady=5)
        self.miles_saved_combo = miles_saved_combo

        # Barriers encountered
        ttk.Label(telehealth_frame, text="Barriers Encountered During Mental Health Services:").grid(row=1, column=0, padx=5, pady=5, sticky="w")

        # List to store the BooleanVar instances
        barriers = [
            "Center doesn't offer the services needed",
            "Concerned about what others think",
            "Cost of services",
            "Distance to clinic",
            "Lack of transportation",
            "No insurance",
            "Scheduling difficulty",
            "Waitlist too long",
            "Other"
        ]
        self.barrier_vars = {}
        for i, barrier in enumerate(barriers):
            var = tk.BooleanVar(value=False)
            self.barrier_vars[barrier] = var
            ttk.Checkbutton(telehealth_frame, text=barrier, variable=var).grid(row=i + 2, column=0, sticky="w")

        # Mental Health Provider Log Section
        provider_log_frame = tk.LabelFrame(scrollable_frame, text="Mental Health Provider Log", padx=10, pady=10)
        provider_log_frame.grid(row=6, column=0, padx=10, pady=5, sticky='w')

        # Provider and details buttons
        provider_log_buttons_frame = tk.Frame(provider_log_frame)
        provider_log_buttons_frame.grid(row=0, column=0, sticky="w")
        ttk.Button(provider_log_buttons_frame, text="+ Add Provider", command=lambda: self.add_provider_popup()).pack(side="left", padx=5, pady=5)
        ttk.Button(provider_log_buttons_frame, text="Details").pack(side="left", padx=5, pady=5)

        # Treeview for provider log with Edit/Delete columns
        self.provider_tree = ttk.Treeview(provider_log_frame, columns=("Edit", "Delete", "Date Offered", "Agency", "Therapist", "Case #"), show='headings')
        self.provider_tree.heading("Edit", text="Edit")
        self.provider_tree.heading("Delete", text="Delete")
        self.provider_tree.heading("Date Offered", text="Date Services Offered")
        self.provider_tree.heading("Agency", text="Agency")
        self.provider_tree.heading("Therapist", text="Therapist")
        self.provider_tree.heading("Case #", text="Case #")
        self.provider_tree.column("Edit", width=50, anchor='center')
        self.provider_tree.column("Delete", width=60, anchor='center')
        self.provider_tree.column("Date Offered", width=120)
        self.provider_tree.column("Agency", width=150)
        self.provider_tree.column("Therapist", width=150)
        self.provider_tree.column("Case #", width=100)
        self.provider_tree.grid(row=1, column=0, padx=5, pady=5, sticky="nsew")

        # Bind click event to the Treeview
        self.provider_tree.bind('<Button-1>', self.on_provider_tree_click)

        # Outside Referrals Section
        outside_referrals_frame = tk.LabelFrame(scrollable_frame, text="Outside Referrals", padx=10, pady=10)
        outside_referrals_frame.grid(row=7, column=0, padx=10, pady=5, sticky='w')

        # "+ Add New Referral" button
        ttk.Button(outside_referrals_frame, text="+ Add New Referral", command=self.add_new_referral_popup).grid(row=0, column=0, padx=5, pady=5, sticky="w")

        # Treeview to display existing referrals
        self.referrals_page = 1
        self.referrals_per_page = 5
        self.referrals_tree = ttk.Treeview(outside_referrals_frame, columns=("Date", "Referred To", "Comment"), show='headings')
        self.referrals_tree.heading("Date", text="Date")
        self.referrals_tree.heading("Referred To", text="Referred To")
        self.referrals_tree.heading("Comment", text="Comment")
        self.referrals_tree.column("Date", width=100)
        self.referrals_tree.column("Referred To", width=200)
        self.referrals_tree.column("Comment", width=300)
        self.referrals_tree.grid(row=1, column=0, padx=5, pady=5, sticky="nsew")

        # Pagination controls for referrals
        referrals_pagination_frame = ttk.Frame(outside_referrals_frame)
        referrals_pagination_frame.grid(row=2, column=0, pady=5)
        self.referrals_prev_button = ttk.Button(referrals_pagination_frame, text="Previous", command=self.load_previous_referrals)
        self.referrals_prev_button.pack(side='left', padx=5)
        self.referrals_next_button = ttk.Button(referrals_pagination_frame, text="Next", command=self.load_next_referrals)
        self.referrals_next_button.pack(side='left', padx=5)
        self.referrals_page_label = ttk.Label(referrals_pagination_frame, text="Page 1")
        self.referrals_page_label.pack(side='left', padx=5)

        # Additional Points of Contact Section
        additional_poc_frame = tk.LabelFrame(scrollable_frame, text="Additional Points of Contact", padx=10, pady=10)
        additional_poc_frame.grid(row=8, column=0, padx=10, pady=5, sticky = 'w')

        # "+ Add New Point of Contact" button
        ttk.Button(additional_poc_frame, text="+ Add New Point of Contact", command=self.add_new_poc_popup).grid(row=0, column=0, padx=5, pady=5, sticky="w")

        # Treeview to display existing points of contact
        self.poc_page = 1
        self.poc_per_page = 5
        self.poc_tree = ttk.Treeview(additional_poc_frame, columns=("Agency", "Name", "Phone", "Email"), show='headings')
        self.poc_tree.heading("Agency", text="Agency")
        self.poc_tree.heading("Name", text="Name")
        self.poc_tree.heading("Phone", text="Phone")
        self.poc_tree.heading("Email", text="Email")
        self.poc_tree.column("Agency", width=150)
        self.poc_tree.column("Name", width=150)
        self.poc_tree.column("Phone", width=120)
        self.poc_tree.column("Email", width=200)
        self.poc_tree.grid(row=1, column=0, padx=5, pady=5, sticky="nsew")

        # Pagination controls for POC
        poc_pagination_frame = ttk.Frame(additional_poc_frame)
        poc_pagination_frame.grid(row=2, column=0, pady=5)
        self.poc_prev_button = ttk.Button(poc_pagination_frame, text="Previous", command=self.load_previous_poc)
        self.poc_prev_button.pack(side='left', padx=5)
        self.poc_next_button = ttk.Button(poc_pagination_frame, text="Next", command=self.load_next_poc)
        self.poc_next_button.pack(side='left', padx=5)
        self.poc_page_label = ttk.Label(poc_pagination_frame, text="Page 1")
        self.poc_page_label.pack(side='left', padx=5)

        # Contact Info Section
        contact_info_frame = tk.LabelFrame(scrollable_frame, text="Contact Info", padx=10, pady=10)
        contact_info_frame.grid(row=9, column=0, sticky='w', padx=10, pady=5)

        # Client Contact Info
        ttk.Label(contact_info_frame, text="Client Contact Info").grid(row=0, column=0, padx=5, pady=5, sticky="w", columnspan=2)
        client_name_label = ttk.Label(contact_info_frame, text="")
        client_name_label.grid(row=1, column=0, padx=5, pady=5, sticky="w", columnspan=2)
        self.client_name_label = client_name_label

        client_address_label = ttk.Label(contact_info_frame, text="")
        client_address_label.grid(row=2, column=0, padx=5, pady=5, sticky="w", columnspan=2)
        self.client_address_label = client_address_label

        # Parent Contact Info
        ttk.Label(contact_info_frame, text="Parent Contact Info").grid(row=3, column=0, padx=5, pady=5, sticky="w", columnspan=2)
        parent_name_label = ttk.Label(contact_info_frame, text="")
        parent_name_label.grid(row=4, column=0, padx=5, pady=5, sticky="w", columnspan=2)
        self.parent_name_label = parent_name_label

        parent_address_label = ttk.Label(contact_info_frame, text="")
        parent_address_label.grid(row=5, column=0, padx=5, pady=5, sticky="w", columnspan=2)
        self.parent_address_label = parent_address_label

        # Date Therapy Completed
        ttk.Label(contact_info_frame, text="Date Therapy Completed").grid(row=6, column=0, padx=5, pady=5, sticky="e")
        date_therapy_completed = DateEntry(contact_info_frame, width=12, background='darkblue', foreground='white', borderwidth=2)
        date_therapy_completed.grid(row=6, column=1, padx=5, pady=5, sticky="w")
        self.date_therapy_completed = date_therapy_completed

        # Document Upload Section
        upload_frame = tk.LabelFrame(scrollable_frame, text="Document Upload", padx=10, pady=10)
        upload_frame.grid(row=10, column=0, sticky='w', padx=10, pady=5)

        ttk.Label(upload_frame, text="File Name:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        file_name_var = tk.StringVar()  # Variable to hold the filename
        file_name_entry = ttk.Entry(upload_frame, textvariable=file_name_var, width=50, state="readonly")
        file_name_entry.grid(row=0, column=1, padx=5, pady=5, sticky="w")
        self.file_name_var = file_name_var

        # Function to open file dialog and set the filename
        def select_file():
            file_path = filedialog.askopenfilename(title="Select a file", filetypes=[("All files", "*.*")])
            if file_path:  # If a file is selected
                file_name_var.set(os.path.basename(file_path))  # Set the filename in the entry

        # Button to trigger file selection
        ttk.Button(upload_frame, text="Select Files...", command=select_file).grid(row=0, column=2, padx=5, pady=5)

        # Upload status label
        upload_status_label = ttk.Label(upload_frame, text="Maximum allowed file size is 10 MB.")
        upload_status_label.grid(row=1, column=0, columnspan=3, padx=5, pady=5)

        # Initialize missing attributes for pagination
        self.referrals_total_pages = 1
        self.poc_total_pages = 1

        # Load existing data
        self.load_data()

    def connect_to_database(self):
        # Read database configuration from database.ini
        config = configparser.ConfigParser()
        config_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'database', 'database.ini')
        config.read(config_path)

        db_params = {
            'host': config.get('postgresql', 'host'),
            'database': config.get('postgresql', 'database'),
            'user': config.get('postgresql', 'user'),
            'password': config.get('postgresql', 'password')
        }

        # Connect to the PostgreSQL database
        try:
            conn = psycopg2.connect(**db_params)
            print("Database connection established.")
            return conn
        except (Exception, psycopg2.DatabaseError) as error:
            print(f"Error connecting to database: {error}")
            messagebox.showerror("Database Connection Error", f"Unable to connect to the database: {error}")
            raise

    def get_existing_personnel(self):
        # Fetch existing personnel from the database
        try:
            self.cur.execute("SELECT first_name || ' ' || last_name FROM employee;")
            personnel = [row[0] for row in self.cur.fetchall()]
            return personnel
        except Exception as e:
            print(f"Error fetching personnel: {e}")
            self.conn.rollback()
            return []

    def get_existing_agencies(self):
        # Fetch existing agencies from the database
        try:
            self.cur.execute("SELECT agency_name FROM cac_agency;")
            agencies = [row[0] for row in self.cur.fetchall()]
            return agencies
        except Exception as e:
            print(f"Error fetching agencies: {e}")
            self.conn.rollback()
            return []

    def get_state_list(self):
        # Hardcoded list of US state abbreviations
        return [
            "- Please select a state -", "AL", "AK", "AZ", "AR", "CA", "CO", "CT",
            "DE", "FL", "GA", "HI", "ID", "IL", "IN", "IA", "KS", "KY", "LA",
            "ME", "MD", "MA", "MI", "MN", "MS", "MO", "MT", "NE", "NV", "NH",
            "NJ", "NM", "NY", "NC", "ND", "OH", "OK", "OR", "PA", "RI", "SC",
            "SD", "TN", "TX", "UT", "VT", "VA", "WA", "WV", "WI", "WY"
        ]

    def add_personnel_popup(self):
        popup = tk.Toplevel(self)
        popup.title("New Personnel")
        popup.geometry("600x800")

        # Instructions
        ttk.Label(popup, text="Below is a list of existing personnel. If the desired person is on this list, do not add again. Instead click Cancel to return to the previous screen and select them from the person pick list").pack(pady=5)

        # Frame for existing personnel with scrollbar
        personnel_frame = tk.Frame(popup)
        personnel_frame.pack(fill='both', expand=True, padx=10)

        canvas = tk.Canvas(personnel_frame)
        scrollbar = ttk.Scrollbar(personnel_frame, orient="vertical", command=canvas.yview)
        scrollable_personnel_frame = ttk.Frame(canvas)

        scrollable_personnel_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_personnel_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        existing_personnel = self.get_existing_personnel()

        for person in existing_personnel:
            person_row = tk.Frame(scrollable_personnel_frame)
            person_row.pack(fill='x', pady=2)

            person_label = ttk.Label(person_row, text=person)
            person_label.pack(side='left', padx=5)

            use_button = ttk.Button(person_row, text='Use Person', command=lambda p=person: self.select_person(p, popup))
            use_button.pack(side='right', padx=5)

        # Separator
        ttk.Separator(popup, orient='horizontal').pack(fill='x', pady=10)

        # Input fields for new personnel
        ttk.Label(popup, text="First Name *", foreground='red').pack(padx=5, pady=5)
        first_name_entry = ttk.Entry(popup)
        first_name_entry.pack(padx=5, pady=5)

        ttk.Label(popup, text="Last Name *", foreground='red').pack(padx=5, pady=5)
        last_name_entry = ttk.Entry(popup)
        last_name_entry.pack(padx=5, pady=5)

        # **Added Agency Selection**
        ttk.Label(popup, text="Agency *", foreground='red').pack(padx=5, pady=5)
        agencies = self.get_existing_agencies()
        if not agencies:
            messagebox.showerror("No Agencies Found", "No agencies found. Please add an agency first.")
            popup.destroy()
            return
        agency_combo = ttk.Combobox(popup, values=agencies)
        agency_combo.pack(padx=5, pady=5)
        agency_combo.set(agencies[0])  # Set default to first agency
        self.agency_combo = agency_combo

        ttk.Label(popup, text="Job Title").pack(padx=5, pady=5)
        job_title_entry = ttk.Entry(popup)
        job_title_entry.pack(padx=5, pady=5)

        ttk.Label(popup, text="Email").pack(padx=5, pady=5)
        email_entry = ttk.Entry(popup)
        email_entry.pack(padx=5, pady=5)

        ttk.Label(popup, text="Phone").pack(padx=5, pady=5)
        phone_entry = ttk.Entry(popup)
        phone_entry.pack(padx=5, pady=5)

        # Save/Cancel buttons
        button_frame = ttk.Frame(popup)
        button_frame.pack(pady=10)
        ttk.Button(button_frame, text="Save", command=lambda: [
            self.save_personnel(
                first_name_entry.get(),
                last_name_entry.get(),
                agency_combo.get(),
                job_title_entry.get(),
                email_entry.get(),
                phone_entry.get()
            ),
            popup.destroy(),
            self.load_personnel_list()
        ]).pack(side='left', padx=5)
        ttk.Button(button_frame, text="Cancel", command=popup.destroy).pack(side='left', padx=5)

    def select_person(self, person_name, popup):
        self.person_combo.set(person_name)
        popup.destroy()

    def add_referral_source_popup(self):
        popup = tk.Toplevel(self)
        popup.title("Add New Referral Source")
        popup.geometry("700x700")

        # Instructions
        ttk.Label(popup, text="Below is a list of existing agencies. If the desired agency is on this list then click 'Use Agency'. If the agency is not on the list enter the agency name below and click 'Save'.").pack(pady=5)

        # Frame for existing agencies with scrollbar
        agency_frame = tk.Frame(popup)
        agency_frame.pack(fill='both', expand=True, padx=10)

        canvas = tk.Canvas(agency_frame)
        scrollbar = ttk.Scrollbar(agency_frame, orient="vertical", command=canvas.yview)
        scrollable_agency_frame = ttk.Frame(canvas)

        scrollable_agency_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_agency_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Table headings
        headings_frame = tk.Frame(scrollable_agency_frame)
        headings_frame.pack(fill='x')

        ttk.Label(headings_frame, text="Agency", width=50).grid(row=0, column=0, padx=5, pady=5)
        ttk.Label(headings_frame, text="Action", width=20).grid(row=0, column=1, padx=5, pady=5)

        existing_agencies = self.get_existing_agencies()

        for idx, agency in enumerate(existing_agencies):
            agency_row = tk.Frame(scrollable_agency_frame)
            agency_row.pack(fill='x', pady=2)

            agency_label = ttk.Label(agency_row, text=agency, width=50)
            agency_label.grid(row=idx + 1, column=0, padx=5, pady=2, sticky='w')

            use_button = ttk.Button(agency_row, text='Use Agency', command=lambda a=agency: self.select_agency(a, popup))
            use_button.grid(row=idx + 1, column=1, padx=5, pady=2, sticky='e')

        # Separator
        ttk.Separator(popup, orient='horizontal').pack(fill='x', pady=10)

        # Input fields for new referral source
        ttk.Label(popup, text="Agency Name *", foreground='red').pack(padx=5, pady=5)
        agency_name_entry = ttk.Entry(popup)
        agency_name_entry.pack(padx=5, pady=5)

        ttk.Label(popup, text="Address Line 1").pack(padx=5, pady=5)
        address_line1_entry = ttk.Entry(popup)
        address_line1_entry.pack(padx=5, pady=5)

        ttk.Label(popup, text="Address Line 2").pack(padx=5, pady=5)
        address_line2_entry = ttk.Entry(popup)
        address_line2_entry.pack(padx=5, pady=5)

        # Removed city as it may not exist in your database
        # ttk.Label(popup, text="City").pack(padx=5, pady=5)
        # city_entry = ttk.Entry(popup)
        # city_entry.pack(padx=5, pady=5)
        city_entry = None  # Placeholder

        ttk.Label(popup, text="State").pack(padx=5, pady=5)
        state_combo = ttk.Combobox(popup, values=self.get_state_list())
        state_combo.current(0)
        state_combo.pack(padx=5, pady=5)
        self.state_combo = state_combo

        ttk.Label(popup, text="Zip Code").pack(padx=5, pady=5)
        zip_code_entry = ttk.Entry(popup)
        zip_code_entry.pack(padx=5, pady=5)

        ttk.Label(popup, text="Phone Number").pack(padx=5, pady=5)
        phone_number_entry = ttk.Entry(popup)
        phone_number_entry.pack(padx=5, pady=5)

        # Save/Cancel buttons
        button_frame = ttk.Frame(popup)
        button_frame.pack(pady=10)
        ttk.Button(button_frame, text="Save", command=lambda: [
            self.save_agency(
                agency_name_entry.get(),
                address_line1_entry.get(),
                address_line2_entry.get(),
                None,  # Since city may not exist
                state_combo.get(),
                zip_code_entry.get(),
                phone_number_entry.get()
            ),
            popup.destroy(),
            self.load_agency_list()
        ]).pack(side='left', padx=5)
        ttk.Button(button_frame, text="Cancel", command=popup.destroy).pack(side='left', padx=5)

    def select_agency(self, agency_name, popup):
        self.referral_source.set(agency_name)
        popup.destroy()

    def add_mh_provider_agency_popup(self):
        popup = tk.Toplevel(self)
        popup.title("Add New MH Provider Agency")
        popup.geometry("800x700")

        # Instructions
        ttk.Label(popup, text="Below is a list of existing agencies. If the desired agency is on this list then click 'Use Agency'. If the agency is not on the list enter the agency name below and click 'Save'.").pack(pady=5)

        # Frame for existing agencies with scrollbar
        agency_frame = tk.Frame(popup)
        agency_frame.pack(fill='both', expand=True, padx=10)

        canvas = tk.Canvas(agency_frame)
        scrollbar = ttk.Scrollbar(agency_frame, orient="vertical", command=canvas.yview)
        scrollable_agency_frame = ttk.Frame(canvas)

        scrollable_agency_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_agency_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Table headings
        headings_frame = tk.Frame(scrollable_agency_frame)
        headings_frame.pack(fill='x')

        ttk.Label(headings_frame, text="Agency", width=40).grid(row=0, column=0, padx=5, pady=5)
        ttk.Label(headings_frame, text="Is MH Agency", width=20).grid(row=0, column=1, padx=5, pady=5)
        ttk.Label(headings_frame, text="Action", width=20).grid(row=0, column=2, padx=5, pady=5)

        existing_agencies = self.get_existing_agencies()

        is_mh_agency_vars = {}

        for idx, agency in enumerate(existing_agencies):
            agency_row = tk.Frame(scrollable_agency_frame)
            agency_row.pack(fill='x', pady=2)

            agency_label = ttk.Label(agency_row, text=agency, width=40)
            agency_label.grid(row=idx + 1, column=0, padx=5, pady=2, sticky='w')

            var = tk.BooleanVar()
            is_mh_agency_vars[agency] = var
            mh_check = ttk.Checkbutton(agency_row, variable=var)
            mh_check.grid(row=idx + 1, column=1, padx=5, pady=2)

            use_button = ttk.Button(agency_row, text='Use Agency', command=lambda a=agency: self.select_mh_agency(a, popup))
            use_button.grid(row=idx + 1, column=2, padx=5, pady=2, sticky='e')

        # Separator
        ttk.Separator(popup, orient='horizontal').pack(fill='x', pady=10)

        # Input fields for new referral source
        ttk.Label(popup, text="Agency Name *", foreground='red').pack(padx=5, pady=5)
        agency_name_entry = ttk.Entry(popup)
        agency_name_entry.pack(padx=5, pady=5)

        ttk.Label(popup, text="Address Line 1").pack(padx=5, pady=5)
        address_line1_entry = ttk.Entry(popup)
        address_line1_entry.pack(padx=5, pady=5)

        ttk.Label(popup, text="Address Line 2").pack(padx=5, pady=5)
        address_line2_entry = ttk.Entry(popup)
        address_line2_entry.pack(padx=5, pady=5)

        # Removed city as it may not exist
        # ttk.Label(popup, text="City").pack(padx=5, pady=5)
        # city_entry = ttk.Entry(popup)
        # city_entry.pack(padx=5, pady=5)
        city_entry = None  # Placeholder

        ttk.Label(popup, text="State").pack(padx=5, pady=5)
        state_combo = ttk.Combobox(popup, values=self.get_state_list())
        state_combo.current(0)
        state_combo.pack(padx=5, pady=5)
        self.state_combo_mh = state_combo

        ttk.Label(popup, text="Zip Code").pack(padx=5, pady=5)
        zip_code_entry = ttk.Entry(popup)
        zip_code_entry.pack(padx=5, pady=5)

        ttk.Label(popup, text="Phone Number").pack(padx=5, pady=5)
        phone_number_entry = ttk.Entry(popup)
        phone_number_entry.pack(padx=5, pady=5)

        # Is MH Agency checkbox
        is_mh_agency_var = tk.BooleanVar()
        ttk.Checkbutton(popup, text="Is MH Agency", variable=is_mh_agency_var).pack(padx=5, pady=5)
        self.is_mh_agency_var = is_mh_agency_var

        # Save/Cancel buttons
        button_frame = ttk.Frame(popup)
        button_frame.pack(pady=10)
        ttk.Button(button_frame, text="Save", command=lambda: [
            self.save_agency(
                agency_name_entry.get(),
                address_line1_entry.get(),
                address_line2_entry.get(),
                None,  # City placeholder
                state_combo.get(),
                zip_code_entry.get(),
                phone_number_entry.get(),
                is_mh_agency_var.get()
            ),
            popup.destroy(),
            self.load_agency_list()
        ]).pack(side='left', padx=5)
        ttk.Button(button_frame, text="Cancel", command=popup.destroy).pack(side='left', padx=5)

    def select_mh_agency(self, agency_name, popup):
        self.agency_entry.set(agency_name)
        popup.destroy()

    def add_mh_service_provider_popup(self):
        popup = tk.Toplevel(self)
        popup.title("Add New MH Service Provider")
        popup.geometry("600x700")

        # Instructions
        ttk.Label(popup, text="Below is a list of existing personnel. If the desired person is on this list, do not add again. Instead click Cancel to return to the previous screen and select them from the person pick list").pack(pady=5)

        # Frame for existing personnel with scrollbar
        personnel_frame = tk.Frame(popup)
        personnel_frame.pack(fill='both', expand=True, padx=10)

        canvas = tk.Canvas(personnel_frame)
        scrollbar = ttk.Scrollbar(personnel_frame, orient="vertical", command=canvas.yview)
        scrollable_personnel_frame = ttk.Frame(canvas)

        scrollable_personnel_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_personnel_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        existing_personnel = self.get_existing_personnel()

        for person in existing_personnel:
            person_row = tk.Frame(scrollable_personnel_frame)
            person_row.pack(fill='x', pady=2)

            person_label = ttk.Label(person_row, text=person)
            person_label.pack(side='left', padx=5)

            use_button = ttk.Button(person_row, text='Use Person', command=lambda p=person: self.select_mh_provider(p, popup))
            use_button.pack(side='right', padx=5)

        # Separator
        ttk.Separator(popup, orient='horizontal').pack(fill='x', pady=10)

        # Input fields for new personnel
        ttk.Label(popup, text="First Name *", foreground='red').pack(padx=5, pady=5)
        first_name_entry = ttk.Entry(popup)
        first_name_entry.pack(padx=5, pady=5)

        ttk.Label(popup, text="Last Name *", foreground='red').pack(padx=5, pady=5)
        last_name_entry = ttk.Entry(popup)
        last_name_entry.pack(padx=5, pady=5)

        # **Added Agency Selection for Service Provider**
        ttk.Label(popup, text="Agency *", foreground='red').pack(padx=5, pady=5)
        agencies = self.get_existing_agencies()
        if not agencies:
            messagebox.showerror("No Agencies Found", "No agencies found. Please add an agency first.")
            popup.destroy()
            return
        agency_combo = ttk.Combobox(popup, values=agencies)
        agency_combo.pack(padx=5, pady=5)
        agency_combo.set(agencies[0])  # Set default to first agency
        self.agency_combo_mh_service = agency_combo

        ttk.Label(popup, text="Job Title").pack(padx=5, pady=5)
        job_title_entry = ttk.Entry(popup)
        job_title_entry.pack(padx=5, pady=5)

        ttk.Label(popup, text="Email").pack(padx=5, pady=5)
        email_entry = ttk.Entry(popup)
        email_entry.pack(padx=5, pady=5)

        ttk.Label(popup, text="Phone").pack(padx=5, pady=5)
        phone_entry = ttk.Entry(popup)
        phone_entry.pack(padx=5, pady=5)

        # Save/Cancel buttons
        button_frame = ttk.Frame(popup)
        button_frame.pack(pady=10)
        ttk.Button(button_frame, text="Save", command=lambda: [
            self.save_personnel(
                first_name_entry.get(),
                last_name_entry.get(),
                agency_combo.get(),
                job_title_entry.get(),
                email_entry.get(),
                phone_entry.get()
            ),
            popup.destroy(),
            self.load_personnel_list()
        ]).pack(side='left', padx=5)
        ttk.Button(button_frame, text="Cancel", command=popup.destroy).pack(side='left', padx=5)

    def select_mh_provider(self, person_name, popup):
        self.provider_entry.set(person_name)
        popup.destroy()

    def save_personnel(self, first_name, last_name, agency_name, job_title='', email='', phone=''):
        # Save new personnel to the database with a unique employee_id
        try:
            if not first_name or not last_name or not agency_name:
                messagebox.showerror("Missing Information", "Please fill in all mandatory fields.")
                return

            # Fetch the agency_id based on agency_name
            self.cur.execute("SELECT agency_id FROM cac_agency WHERE agency_name = %s LIMIT 1;", (agency_name,))
            agency_result = self.cur.fetchone()
            if agency_result:
                agency_id = agency_result[0]
            else:
                messagebox.showerror("Error", f"Agency '{agency_name}' not found.")
                return

            # Fetch the next employee_id
            self.cur.execute("SELECT MAX(employee_id) FROM employee;")
            result = self.cur.fetchone()
            next_employee_id = result[0] + 1 if result and result[0] else 1

            # Insert the new employee
            self.cur.execute("""
                INSERT INTO employee (employee_id, agency_id, cac_id, email_addr, first_name, last_name, job_title, phone_number)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s);
            """, (next_employee_id, agency_id, self.cac_id, email, first_name, last_name, job_title, phone))
            self.conn.commit()
            messagebox.showinfo("Success", "Personnel saved successfully.")
            self.load_personnel_list()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save personnel: {e}")
            self.conn.rollback()

    def save_agency(self, agency_name, address1='', address2='', city='', state='', zip_code='', phone='', is_mh_agency=False):
        # Save new agency to the database with a unique agency_id
        try:
            if not agency_name:
                messagebox.showerror("Missing Information", "Agency Name is required.")
                return

            # Validate state_abbr
            valid_states = self.get_state_list()[1:]  # Exclude the first prompt option
            if state not in valid_states:
                messagebox.showerror("Invalid State", "Please select a valid state abbreviation.")
                return

            # Fetch the next agency_id
            self.cur.execute("SELECT MAX(agency_id) FROM cac_agency;")
            result = self.cur.fetchone()
            next_agency_id = result[0] + 1 if result and result[0] else 1

            # Insert the new agency
            self.cur.execute("""
                INSERT INTO cac_agency (agency_id, cac_id, agency_name, addr_line_1, addr_line_2, state_abbr, zip_code, phone_number)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s);
            """, (next_agency_id, self.cac_id, agency_name, address1, address2, state, zip_code, phone))
            self.conn.commit()
            messagebox.showinfo("Success", "Agency saved successfully.")
            self.load_agency_list()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save agency: {e}")
            self.conn.rollback()

    def save_provider(self, agency, provider, case_number, therapy_date, record_created, therapy_accepted, therapy_completed_date, provider_id=None):
        # Save provider information to the database with a unique id
        try:
            # Validate mandatory fields
            if not agency or not provider or not therapy_date:
                messagebox.showerror("Missing Information", "Please fill in all required fields.")
                return

            # Get agency_id
            self.cur.execute("SELECT agency_id FROM cac_agency WHERE agency_name = %s LIMIT 1;", (agency,))
            agency_result = self.cur.fetchone()
            if agency_result:
                agency_id = agency_result[0]
            else:
                messagebox.showerror("Error", f"Agency '{agency}' not found.")
                return

            # Get employee_id
            self.cur.execute("SELECT employee_id FROM employee WHERE first_name || ' ' || last_name = %s LIMIT 1;", (provider,))
            provider_result = self.cur.fetchone()
            if provider_result:
                provider_employee_id = provider_result[0]
            else:
                messagebox.showerror("Error", f"Provider '{provider}' not found.")
                return

            if provider_id:
                # Update existing record
                self.cur.execute("""
                    UPDATE case_mh_provider SET
                        agency_id = %s,
                        case_number = %s,
                        lead_employee_id = %s,
                        therapy_accepted = %s,
                        therapy_complete_date = %s,
                        therapy_offered_date = %s,
                        therapy_record_created = %s
                    WHERE id = %s;
                """, (
                    agency_id,
                    case_number,
                    provider_employee_id,
                    therapy_accepted,
                    therapy_completed_date,
                    therapy_date,
                    record_created,
                    provider_id
                ))
            else:
                # Fetch the next id for case_mh_provider
                self.cur.execute("SELECT MAX(id) FROM case_mh_provider;")
                result = self.cur.fetchone()
                next_id = result[0] + 1 if result and result[0] else 1

                # Insert into case_mh_provider
                self.cur.execute("""
                    INSERT INTO case_mh_provider (
                        id, agency_id, case_id, case_number, lead_employee_id, therapy_accepted, therapy_complete_date, therapy_offered_date, therapy_record_created
                    )
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s);
                """, (
                    next_id,
                    agency_id,
                    self.case_id,
                    case_number,
                    provider_employee_id,
                    therapy_accepted,
                    therapy_completed_date,
                    therapy_date,
                    record_created
                ))
                provider_id = next_id  # Set provider_id for later use

            self.conn.commit()
            messagebox.showinfo("Success", "Provider saved successfully.")
            # Reload the provider log
            self.load_provider_log()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save provider: {e}")
            self.conn.rollback()

    def load_personnel_list(self):
        # Refresh personnel list in the dropdowns
        self.person_combo['values'] = self.get_existing_personnel()
        if hasattr(self, 'provider_entry'):
            self.provider_entry['values'] = self.get_existing_personnel()

    def load_agency_list(self):
        # Refresh agency list in the dropdowns
        self.referral_source['values'] = self.get_existing_agencies()
        if hasattr(self, 'agency_entry'):
            self.agency_entry['values'] = self.get_existing_agencies()

    def load_data(self):
        # Load existing data for the case and populate the fields
        # Fetch data from the database based on self.case_id
        try:
            self.cur.execute("SELECT * FROM cac_case WHERE case_id = %s;", (self.case_id,))
            data = self.cur.fetchone()
            if data:
                # Map data to field indices based on column order
                columns = [desc[0] for desc in self.cur.description]
                data_dict = dict(zip(columns, data))

                # Populate fields with data
                mh_referral_date = data_dict.get('mh_referral_date')
                if mh_referral_date:
                    self.date_entry.set_date(mh_referral_date)

                mh_referral_agency_id = data_dict.get('mh_referral_agency_id')
                if mh_referral_agency_id:
                    self.cur.execute("SELECT agency_name FROM cac_agency WHERE agency_id = %s;", (mh_referral_agency_id,))
                    agency = self.cur.fetchone()
                    if agency:
                        self.referral_source.set(agency[0])

                mh_lead_employee_id = data_dict.get('mh_lead_employee_id')
                if mh_lead_employee_id:
                    self.cur.execute("SELECT first_name || ' ' || last_name FROM employee WHERE employee_id = %s;", (mh_lead_employee_id,))
                    person = self.cur.fetchone()
                    if person:
                        self.person_combo.set(person[0])

                mh_therapy_accepted = data_dict.get('mh_therapy_accepted')
                if mh_therapy_accepted is not None:
                    self.status_accepted_var.set(mh_therapy_accepted)
                    self.no_mh_services_var.set(not mh_therapy_accepted)

                # Populate other fields as needed
                mh_services_elsewhere = data_dict.get('mh_services_elsewhere')
                if mh_services_elsewhere:
                    self.mh_services_elsewhere.insert(0, mh_services_elsewhere)

                psyc_notes = data_dict.get('psyc_notes')
                if psyc_notes:
                    self.psyc_notes_entry.insert(0, psyc_notes)

                mh_extended_services = data_dict.get('mh_extended_services_candidate')
                if mh_extended_services:
                    self.mh_extended_services.set(mh_extended_services)

                custom_field_6 = data_dict.get('mh_services_custom_6')
                if custom_field_6:
                    self.custom_field_6.insert(0, custom_field_6)

                custom_field_7 = data_dict.get('mh_services_custom_7')
                if custom_field_7:
                    self.custom_field_7.insert(0, custom_field_7)

                client_declined_services = data_dict.get('client_declined_services')
                if client_declined_services:
                    self.client_declined_var.set(client_declined_services)
                    self.no_client_declined_var.set(not client_declined_services)

                client_declined_reason = data_dict.get('why_client_declined_services')
                if client_declined_reason:
                    self.client_declined_reason.insert(0, client_declined_reason)

            # Load provider log
            self.load_provider_log()

            # Load referrals
            self.load_referrals()

            # Load additional points of contact
            self.load_poc()

            # Load contact info
            self.load_contact_info()

        except Exception as e:
            print(f"Error loading data: {e}")
            self.conn.rollback()

    def load_provider_log(self):
        # Clear existing entries
        for item in self.provider_tree.get_children():
            self.provider_tree.delete(item)
        # Load provider log data
        try:
            self.cur.execute("""
                SELECT 
                    id,
                    therapy_offered_date, 
                    (SELECT agency_name FROM cac_agency WHERE agency_id = cmp.agency_id) AS agency_name, 
                    (SELECT first_name || ' ' || last_name FROM employee WHERE employee_id = cmp.lead_employee_id) AS therapist, 
                    case_number 
                FROM case_mh_provider cmp
                WHERE cmp.case_id = %s;
            """, (self.case_id,))
            providers = self.cur.fetchall()
            for provider in providers:
                provider_id = provider[0]
                date_offered = provider[1].strftime("%Y-%m-%d") if provider[1] else ""
                agency_name = provider[2] if provider[2] else ""
                therapist = provider[3] if provider[3] else ""
                case_number = provider[4] if provider[4] else ""
                self.provider_tree.insert('', 'end', iid=str(provider_id), values=(
                    "Edit",
                    "Delete",
                    date_offered,
                    agency_name,
                    therapist,
                    case_number
                ))
        except Exception as e:
            print(f"Error loading provider log: {e}")
            self.conn.rollback()

    def on_provider_tree_click(self, event):
        # Identify the row and column
        region = self.provider_tree.identify("region", event.x, event.y)
        if region != "cell":
            return
        column = self.provider_tree.identify_column(event.x)
        row = self.provider_tree.identify_row(event.y)
        if not row:
            return

        # Get the provider_id from iid
        provider_id = int(row)

        # Check if the click was on Edit or Delete column
        if column == "#1":  # Edit column
            self.edit_provider(provider_id)
        elif column == "#2":  # Delete column
            self.delete_provider(provider_id)

    def edit_provider(self, provider_id):
        # Open the add_provider_popup with provider_id to edit
        self.add_provider_popup(provider_id=provider_id)

    def delete_provider(self, provider_id):
        # Confirm deletion
        if messagebox.askyesno("Confirm Deletion", "Are you sure you want to delete this provider?"):
            try:
                self.cur.execute("DELETE FROM case_mh_provider WHERE id = %s;", (provider_id,))
                self.conn.commit()
                # Remove from Treeview
                self.provider_tree.delete(str(provider_id))
                messagebox.showinfo("Deleted", "Provider deleted successfully.")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to delete provider: {e}")
                self.conn.rollback()

    def add_provider_popup(self, provider_id=None):
        # Popup for adding or editing a provider
        popup = tk.Toplevel(self)
        if provider_id:
            popup.title("Edit Provider")
        else:
            popup.title("Add Provider")
        popup.geometry("700x700")

        # Labels and entry fields
        ttk.Label(popup, text="MH Provider Agency").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        agency_entry = ttk.Combobox(popup, values=self.get_existing_agencies())
        agency_entry.grid(row=0, column=1, padx=5, pady=5, sticky="w")
        self.agency_entry = agency_entry

        # Add button next to MH Provider Agency
        ttk.Button(popup, text="+ Add", command=self.add_mh_provider_agency_popup).grid(row=0, column=2, padx=5, pady=5)

        ttk.Label(popup, text="Mental Health Service Provider").grid(row=1, column=0, padx=5, pady=5, sticky="e")
        provider_entry = ttk.Combobox(popup, values=self.get_existing_personnel())
        provider_entry.grid(row=1, column=1, padx=5, pady=5, sticky="w")
        self.provider_entry = provider_entry

        # Add button next to Mental Health Service Provider
        ttk.Button(popup, text="+ Add", command=self.add_mh_service_provider_popup).grid(row=1, column=2, padx=5, pady=5)

        ttk.Label(popup, text="MH Case #").grid(row=2, column=0, padx=5, pady=5, sticky="e")
        case_number_entry = ttk.Entry(popup)
        case_number_entry.grid(row=2, column=1, padx=5, pady=5, sticky="w")

        ttk.Label(popup, text="Date Therapy Offered to Family").grid(row=3, column=0, padx=5, pady=5, sticky="e")
        therapy_date_entry = DateEntry(popup, width=12, background='darkblue', foreground='white', borderwidth=2)
        therapy_date_entry.grid(row=3, column=1, padx=5, pady=5, sticky="w")

        # Removed non-existent fields
        # Remove the following fields as they may not exist in your database
        # ttk.Label(popup, text="Reason Sessions Ended").grid(row=4, column=0, padx=5, pady=5, sticky="e")
        # reason_combo = ttk.Combobox(popup, values=["Select Treatment Status...", "Completed", "Client withdrew", "Transferred", "Other"])
        # reason_combo.current(0)
        # reason_combo.grid(row=4, column=1, padx=5, pady=5, sticky="w")

        ttk.Label(popup, text="Record Created").grid(row=5, column=0, padx=5, pady=5, sticky="e")
        record_created_var = tk.BooleanVar(value=False)
        ttk.Checkbutton(popup, variable=record_created_var).grid(row=5, column=1, padx=5, pady=5, sticky="w")

        # Removed referral_type and waiting_list fields
        # ttk.Label(popup, text="Referral Type").grid(row=6, column=0, padx=5, pady=5, sticky="e")
        # referral_type_combo = ttk.Combobox(popup, values=["Select Referral Type...", "In House", "Private Outside", "Community", "Residential"])
        # referral_type_combo.current(0)
        # referral_type_combo.grid(row=6, column=1, padx=5, pady=5, sticky="w")

        # ttk.Label(popup, text="Waiting List").grid(row=7, column=0, padx=5, pady=5, sticky="e")
        # waiting_list_var = tk.BooleanVar(value=False)
        # ttk.Checkbutton(popup, variable=waiting_list_var).grid(row=7, column=1, padx=5, pady=5, sticky="w")

        ttk.Label(popup, text="Child/Family Accepted Therapy Services").grid(row=8, column=0, padx=5, pady=5, sticky="e")
        therapy_accepted_var = tk.BooleanVar(value=False)
        ttk.Checkbutton(popup, variable=therapy_accepted_var).grid(row=8, column=1, padx=5, pady=5, sticky="w")

        ttk.Label(popup, text="Therapy Completed Date").grid(row=9, column=0, padx=5, pady=5, sticky="e")
        therapy_completed_entry = DateEntry(popup, width=12, background='darkblue', foreground='white', borderwidth=2)
        therapy_completed_entry.grid(row=9, column=1, padx=5, pady=5, sticky="w")

        # If editing, populate fields with existing data
        if provider_id:
            self.cur.execute("""
                SELECT 
                    agency_id,
                    lead_employee_id,
                    case_number,
                    therapy_offered_date,
                    therapy_complete_date,
                    therapy_accepted,
                    therapy_record_created
                FROM case_mh_provider
                WHERE id = %s;
            """, (provider_id,))
            data = self.cur.fetchone()
            if data:
                agency_id, lead_employee_id, case_number, therapy_offered_date, therapy_complete_date, therapy_accepted, therapy_record_created = data

                # Get agency name
                self.cur.execute("SELECT agency_name FROM cac_agency WHERE agency_id = %s;", (agency_id,))
                agency_name = self.cur.fetchone()[0]
                agency_entry.set(agency_name)

                # Get provider name
                self.cur.execute("SELECT first_name || ' ' || last_name FROM employee WHERE employee_id = %s;", (lead_employee_id,))
                provider_name = self.cur.fetchone()[0]
                provider_entry.set(provider_name)

                case_number_entry.insert(0, case_number)
                therapy_date_entry.set_date(therapy_offered_date)
                if therapy_complete_date:
                    therapy_completed_entry.set_date(therapy_complete_date)
                therapy_accepted_var.set(therapy_accepted)
                record_created_var.set(therapy_record_created)
                # Populate other fields as necessary

        # Save/Cancel buttons
        button_frame = ttk.Frame(popup)
        button_frame.grid(row=10, column=0, columnspan=3, pady=20)
        ttk.Button(button_frame, text="Update", command=lambda: [
            self.save_provider(
                agency_entry.get(),
                provider_entry.get(),
                case_number_entry.get(),
                therapy_date_entry.get_date(),
                record_created_var.get(),
                therapy_accepted_var.get(),
                therapy_completed_entry.get_date(),
                provider_id  # Pass provider_id for updates
            ),
            popup.destroy()
        ]).pack(side='left', padx=5)
        ttk.Button(button_frame, text="Cancel", command=popup.destroy).pack(side='left', padx=5)

    def add_new_referral_popup(self):
        # Popup for adding new referral
        popup = tk.Toplevel(self)
        popup.title("Add New Referral")
        popup.geometry("600x400")

        ttk.Label(popup, text="Date:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        date_entry = DateEntry(popup, width=12, background='darkblue', foreground='white', borderwidth=2)
        date_entry.grid(row=0, column=1, padx=5, pady=5, sticky="w")

        ttk.Label(popup, text="Referred To:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
        referred_to_entry = ttk.Combobox(popup, values=self.get_existing_agencies())
        referred_to_entry.grid(row=1, column=1, padx=5, pady=5, sticky="w")

        ttk.Label(popup, text="Comment:").grid(row=2, column=0, padx=5, pady=5, sticky="ne")
        comment_text = tk.Text(popup, height=10, width=40)
        comment_text.grid(row=2, column=1, padx=5, pady=5, sticky="w")

        # Save/Cancel buttons
        button_frame = ttk.Frame(popup)
        button_frame.grid(row=3, column=0, columnspan=2, pady=20)
        ttk.Button(button_frame, text="Update", command=lambda: [
            self.save_referral(
                date_entry.get_date(),
                referred_to_entry.get(),
                comment_text.get("1.0", tk.END).strip()
            ),
            popup.destroy()
        ]).pack(side='left', padx=5)
        ttk.Button(button_frame, text="Cancel", command=popup.destroy).pack(side='left', padx=5)

    def save_referral(self, date, referred_to, comment):
        # Save referral information to in-memory list
        try:
            if not date or not referred_to:
                messagebox.showerror("Missing Information", "Please fill in all mandatory fields.")
                return

            # Append the referral to the in-memory list
            self.referrals_data.append({
                'date': date,
                'referred_to': referred_to,
                'comment': comment
            })

            # Reload referrals
            self.load_referrals()

            messagebox.showinfo("Success", "Referral saved successfully.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save referral: {e}")

    def load_referrals(self):
        # Load existing referrals from in-memory list
        try:
            total_referrals = len(self.referrals_data)

            # Calculate total pages
            self.referrals_total_pages = max(1, math.ceil(total_referrals / self.referrals_per_page))

            # Adjust current page if necessary
            if self.referrals_page > self.referrals_total_pages:
                self.referrals_page = self.referrals_total_pages

            # Clear existing entries
            for item in self.referrals_tree.get_children():
                self.referrals_tree.delete(item)

            # Fetch referrals for the current page
            start_index = (self.referrals_page - 1) * self.referrals_per_page
            end_index = start_index + self.referrals_per_page
            current_referrals = self.referrals_data[start_index:end_index]

            for referral in current_referrals:
                referral_date = referral['date'].strftime("%Y-%m-%d") if referral['date'] else ""
                referred_to = referral['referred_to']
                comment = referral['comment']
                self.referrals_tree.insert('', 'end', values=(
                    referral_date,
                    referred_to,
                    comment
                ))

            # Update page label
            self.referrals_page_label.config(text=f"Page {self.referrals_page} of {self.referrals_total_pages}")

            # Disable/enable buttons
            if self.referrals_page <= 1:
                self.referrals_prev_button.state(['disabled'])
            else:
                self.referrals_prev_button.state(['!disabled'])
            if self.referrals_page >= self.referrals_total_pages:
                self.referrals_next_button.state(['disabled'])
            else:
                self.referrals_next_button.state(['!disabled'])

        except Exception as e:
            print(f"Error loading referrals: {e}")

    def load_previous_referrals(self):
        if self.referrals_page > 1:
            self.referrals_page -= 1
            self.load_referrals()

    def load_next_referrals(self):
        if self.referrals_page < self.referrals_total_pages:
            self.referrals_page += 1
            self.load_referrals()

    def add_new_poc_popup(self):
        # Popup for adding new point of contact
        popup = tk.Toplevel(self)
        popup.title("Add New Point of Contact")
        popup.geometry("600x400")

        ttk.Label(popup, text="Agency:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        agency_entry = ttk.Combobox(popup, values=self.get_existing_agencies())
        agency_entry.grid(row=0, column=1, padx=5, pady=5, sticky="w")
        if self.get_existing_agencies():
            agency_entry.set(self.get_existing_agencies()[0])
        self.agency_poc_combo = agency_entry

        ttk.Label(popup, text="Name:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
        name_entry = ttk.Entry(popup)
        name_entry.grid(row=1, column=1, padx=5, pady=5, sticky="w")

        ttk.Label(popup, text="Phone:").grid(row=2, column=0, padx=5, pady=5, sticky="e")
        phone_entry = ttk.Entry(popup)
        phone_entry.grid(row=2, column=1, padx=5, pady=5, sticky="w")

        ttk.Label(popup, text="Email:").grid(row=3, column=0, padx=5, pady=5, sticky="e")
        email_entry = ttk.Entry(popup)
        email_entry.grid(row=3, column=1, padx=5, pady=5, sticky="w")

        # Save/Cancel buttons
        button_frame = ttk.Frame(popup)
        button_frame.grid(row=4, column=0, columnspan=2, pady=20)
        ttk.Button(button_frame, text="Update", command=lambda: [
            self.save_poc(
                agency_entry.get(),
                name_entry.get(),
                phone_entry.get(),
                email_entry.get()
            ),
            popup.destroy()
        ]).pack(side='left', padx=5)
        ttk.Button(button_frame, text="Cancel", command=popup.destroy).pack(side='left', padx=5)

    def save_poc(self, agency, name, phone, email):
        # Save point of contact information to in-memory list
        try:
            if not agency or not name:
                messagebox.showerror("Missing Information", "Please fill in all mandatory fields.")
                return

            # Append the point of contact to the in-memory list
            self.poc_data.append({
                'agency': agency,
                'name': name,
                'phone': phone,
                'email': email
            })

            # Reload POCs
            self.load_poc()

            messagebox.showinfo("Success", "Point of Contact saved successfully.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save point of contact: {e}")

    def load_poc(self):
        # Load existing points of contact from in-memory list
        try:
            total_pocs = len(self.poc_data)

            # Calculate total pages
            self.poc_total_pages = max(1, math.ceil(total_pocs / self.poc_per_page))

            # Adjust current page if necessary
            if self.poc_page > self.poc_total_pages:
                self.poc_page = self.poc_total_pages

            # Clear existing entries
            for item in self.poc_tree.get_children():
                self.poc_tree.delete(item)

            # Fetch POCs for the current page
            start_index = (self.poc_page - 1) * self.poc_per_page
            end_index = start_index + self.poc_per_page
            current_pocs = self.poc_data[start_index:end_index]

            for poc in current_pocs:
                agency_name = poc['agency']
                name = poc['name']
                phone = poc['phone']
                email = poc['email']
                self.poc_tree.insert('', 'end', values=(
                    agency_name,
                    name,
                    phone,
                    email
                ))

            # Update page label
            self.poc_page_label.config(text=f"Page {self.poc_page} of {self.poc_total_pages}")

            # Disable/enable buttons
            if self.poc_page <= 1:
                self.poc_prev_button.state(['disabled'])
            else:
                self.poc_prev_button.state(['!disabled'])
            if self.poc_page >= self.poc_total_pages:
                self.poc_next_button.state(['disabled'])
            else:
                self.poc_next_button.state(['!disabled'])

        except Exception as e:
            print(f"Error loading POCs: {e}")

    def load_previous_poc(self):
        if self.poc_page > 1:
            self.poc_page -= 1
            self.load_poc()

    def load_next_poc(self):
        if self.poc_page < self.poc_total_pages:
            self.poc_page += 1
            self.load_poc()

    def load_contact_info(self):
        # Load client and parent contact info based on the case
        try:
            # Fetch client information
            self.cur.execute("""
                SELECT first_name, last_name
                FROM person
                WHERE person_id = (
                    SELECT person_id
                    FROM case_person
                    WHERE case_id = %s AND role_id = 1 LIMIT 1
                );
            """, (self.case_id,))
            client = self.cur.fetchone()
            if client:
                first_name, last_name = client
                self.client_name_label.config(text=f"{first_name} {last_name}")
                self.client_address_label.config(text="")  # Placeholder as city/state may not exist
            else:
                self.client_name_label.config(text="")
                self.client_address_label.config(text="")

            # Fetch parent information
            self.cur.execute("""
                SELECT first_name, last_name
                FROM person
                WHERE person_id = (
                    SELECT person_id
                    FROM case_person
                    WHERE case_id = %s AND role_id = 2 LIMIT 1
                );
            """, (self.case_id,))
            parent = self.cur.fetchone()
            if parent:
                first_name, last_name = parent
                self.parent_name_label.config(text=f"{first_name} {last_name}")
                self.parent_address_label.config(text="")  # Placeholder
            else:
                self.parent_name_label.config(text="")
                self.parent_address_label.config(text="")
        except Exception as e:
            print(f"Error loading contact info: {e}")
            self.conn.rollback()

    def save_data(self):
        # Collect data from the interface and save to the database
        try:
            # Collecting data
            date = self.date_entry.get_date()
            referral_source = self.referral_source.get()
            person = self.person_combo.get()
            mh_services = self.mh_services_var.get()
            status_accepted = self.status_accepted_var.get()
            psyc_notes = self.psyc_notes_entry.get()
            # Collect data from the added sections
            abuse_type_yes = self.abuse_type_yes_var.get()
            abuse_type_no = self.abuse_type_no_var.get()
            abuse_types_selected = [abuse for abuse, var in self.abuse_type_vars.items() if var.get()]
            # outside_referrals = self.referrals_tree.get_children()
            # additional_poc = self.poc_tree.get_children()

            # Get agency_id for referral_source
            self.cur.execute("SELECT agency_id FROM cac_agency WHERE agency_name = %s LIMIT 1;", (referral_source,))
            agency_result = self.cur.fetchone()
            if agency_result:
                referral_agency_id = agency_result[0]
            else:
                referral_agency_id = None

            # Get employee_id for person
            if person:
                self.cur.execute("SELECT employee_id FROM employee WHERE first_name || ' ' || last_name = %s LIMIT 1;", (person,))
                person_result = self.cur.fetchone()
                if person_result:
                    mh_lead_employee_id = person_result[0]
                else:
                    mh_lead_employee_id = None
            else:
                mh_lead_employee_id = None

            # Convert BooleanVars to booleans
            mh_services_bool = mh_services
            status_accepted_bool = status_accepted

            # Since there are no database columns for the abuse types, referrals, and additional POCs, handle accordingly
            # For example, you can print them or integrate with existing tables if available
            selected_abuse_types = [abuse for abuse, var in self.abuse_type_vars.items() if var.get()]
            print("Abuse Type Yes:", abuse_type_yes)
            print("Abuse Type No:", abuse_type_no)
            print("Selected Abuse Types:", selected_abuse_types)

            # Insert or update into cac_case
            self.cur.execute("""
                INSERT INTO cac_case (
                    cac_id,
                    case_id, 
                    mh_referral_date, 
                    mh_referral_agency_id, 
                    mh_lead_employee_id, 
                    mh_therapy_accepted, 
                    mh_na
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (case_id) DO UPDATE SET
                    mh_referral_date = EXCLUDED.mh_referral_date,
                    mh_referral_agency_id = EXCLUDED.mh_referral_agency_id,
                    mh_lead_employee_id = EXCLUDED.mh_lead_employee_id,
                    mh_therapy_accepted = EXCLUDED.mh_therapy_accepted,
                    mh_na = EXCLUDED.mh_na;
            """, (
                self.cac_id,
                self.case_id,
                date,
                referral_agency_id,
                mh_lead_employee_id,
                status_accepted_bool,
                not mh_services_bool
            ))
            self.conn.commit()
            messagebox.showinfo("Success", "Data saved successfully.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save data: {e}")
            self.conn.rollback()

    def cancel(self):
        # Reset or close the interface
        self.controller.show_frame(Generaltab_interface.GeneraltabInterface)

    def show_lookup_page(self):
        self.controller.show_frame(database_lookup_search.lookup_interface)

    def show_general_tab(self):
        self.controller.show_frame(Generaltab_interface.GeneraltabInterface)

    def show_people_tab(self):
        self.controller.show_frame(people_interface.people_interface)

    def show_mh_basic(self):
        self.controller.show_frame(MHBasicInterface)

    def show_mh_assessment(self):
        self.controller.show_frame(MH_assessment.MHassessment)

    def show_mh_treatment_plan(self):
        self.controller.show_frame(MH_treatmentPlan_interface.MH_treatment_plan_interface)

    def show_va_tab(self):
        self.controller.show_frame(va_tab_interface.va_interface)

    def show_case_notes(self):
        self.controller.show_frame(case_notes.case_notes_interface)

    def __del__(self):
        # Close database connection when the interface is destroyed
        try:
            if hasattr(self, 'cur') and self.cur:
                self.cur.close()
            if hasattr(self, 'conn') and self.conn:
                self.conn.close()
        except Exception as e:
            print(f"Error closing database connection: {e}")
