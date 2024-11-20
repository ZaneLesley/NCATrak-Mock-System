import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkcalendar import DateEntry
import Generaltab_interface
import people_interface
import MH_basic_interface
import MH_assessment
import MH_treatmentPlan_interface
from database.config import load_config
from database.connect import connect
import psycopg2
import random
from datetime import datetime, timedelta

class va_interface(tk.Frame):

    def __init__(self, parent, controller):

        tk.Frame.__init__(self, parent)
        
        self.grid_rowconfigure(2, weight=1)
        self.grid_columnconfigure(0, weight=1)
        
        # label = ttk.Label(self, text="back to main page", font = ("Verdana", 35))
        # label.grid(row = 0, column=0, padx = 5, pady = 5)

        button1 = ttk.Button(self, text="General", 
                            command=lambda: controller.show_frame(Generaltab_interface.GeneraltabInterface))
        button1.grid(row=0, column=0, padx=5, pady=5)

        button2 = ttk.Button(self, text="People", 
                            command=lambda: controller.show_frame(people_interface.people_interface))
        button2.grid(row=0, column=1, padx=5, pady=5)

        button3 = ttk.Button(self, text="Mental Health - Basic", 
                            command=lambda: controller.show_frame(MH_basic_interface.MHBasicInterface))
        button3.grid(row=0, column=2, padx=5, pady=5)

        button4 = ttk.Button(self, text="Mental Health - Assessment", 
                            command=lambda: controller.show_frame(MH_assessment.MHassessment))
        button4.grid(row=0, column=3, padx=5, pady=5)

        button5 = ttk.Button(self, text="Mental Health - Treatment Plan", 
                            command=lambda: controller.show_frame(MH_treatmentPlan_interface.MH_treatment_plan_interface))
        button5.grid(row=0, column=4, padx=5, pady=5)

        button6 = ttk.Button(self, text="VA", 
                            command=lambda: controller.show_frame(va_interface))
        button6.grid(row=0, column=5, padx=5, pady=5)
        
        
        # Create a canvas and a scrollbar
        canvas = tk.Canvas(self)
        scrollbar = ttk.Scrollbar(self, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)

        # Configure the canvas and scrollbar
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        widget_frame = ttk.Frame(self)
        widget_frame.grid(row=1, column=0, pady=20)

        save_button = ttk.Button(widget_frame, text='SAVE')
        cancel_button = ttk.Button(widget_frame, text='CANCEL')

        save_button.grid(row=1, column=0, sticky="w", padx=5)
        cancel_button.grid(row=1, column=1, sticky="w", padx=5)

        scrollable_frame = ttk.Frame(canvas)
        # Configure the canvas and scrollbar
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        # Create a window in the canvas
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")

        # Link scrollbar to the canvas
        canvas.configure(yscrollcommand=scrollbar.set)

        # Use grid over pack for interface linking
        canvas.grid(row=2, column=0, sticky="nsew")
        scrollbar.grid(row=2, column=1, sticky="ns")

        # VA tab title
        va_frame = tk.Frame(scrollable_frame)
        va_frame.pack(anchor="center", pady=10, padx=10)
        ttk.Label(va_frame, text="VA").pack()

        def get_all_states():
            try:
                config = load_config()
                with psycopg2.connect(**config) as conn:
                    with conn.cursor() as cur:
                        cur.execute("select * from state_table;")
                        states = cur.fetchall()
                        stateMap = {state[0]: state[1] for state in states}
                        return stateMap
            except (psycopg2.DatabaseError, Exception) as error:
                print(f"{error}")
                exit()

        def get_all_agencies():
            try:
                config = load_config()
                with psycopg2.connect(**config) as conn:
                    with conn.cursor() as cur:
                        cur.execute("select * from cac_agency;")
                        agencies = cur.fetchall()
                        agencyMap = {agency[2]: agency[0] for agency in agencies}
                        return agencyMap
            except (psycopg2.DatabaseError, Exception) as error:
                print(f"{error}")
                exit()

        def insert_new_agency(name, address1, address2, city, state, zipcode, phone):
            sqlQuery = """insert into cac_agency (agency_id, cac_id, agency_name, addr_line_1, 
            addr_line_2, city, state_abbr, phone_number, zip_code)
            values (%s, %s, %s, %s, %s, %s, %s, %s, %s)"""
            try:
                config = load_config()
                with psycopg2.connect(**config) as conn:
                    with conn.cursor() as cur:
                        cur.execute(sqlQuery, (random.randint(1, 99999999), 1, name, address1, address2, city, state, 
                                               phone, zipcode))
                        conn.commit
            except (psycopg2.DatabaseError, Exception) as error:
                print(f"{error}")
                exit()

        def add_agency_popup():
            popup = tk.Toplevel(self)
            popup.title("New Agency")
            popup.geometry("550x550")

            agencies = get_all_agencies()

            states = get_all_states()

            popup.grid_columnconfigure(0, weight=1)  
            popup.grid_columnconfigure(1, weight=1)  
            popup.grid_rowconfigure(3, weight=1)  


            ttk.Label(popup, text="Below is a list of existing agencies.", foreground='black').grid(row=0, column=0, padx=5, pady=5, sticky='w')
            ttk.Label(popup, text="If the desired agency is on this list do not add again.", foreground='black').grid(row=1, column=0, padx=5, pady=5, sticky='w')
            ttk.Label(popup, text="If the agency is not on the list enter agency information into fields marked with (*) and click 'Save'.", foreground='red').grid(row=2, column=0, padx=5, pady=5, sticky='w')

            listbox_frame = ttk.Frame(popup)
            listbox_frame.grid(row=3, column=0, padx=10, pady=10, sticky='w')

            # Add a scrollbar for the listbox
            scrollbar = ttk.Scrollbar(listbox_frame, orient="vertical")

            # Listbox with adjusted width and integrated scrollbar
            agency_listbox = tk.Listbox(listbox_frame, height=10, width=50, yscrollcommand=scrollbar.set)
            scrollbar.config(command=agency_listbox.yview)
            for agency_name in agencies.keys():
                agency_listbox.insert(tk.END, agency_name)
            agency_listbox.grid(row=0, column=0, sticky='ns')
            scrollbar.grid(row=0, column=1, sticky='ns')

            field_frame = ttk.Frame(popup)
            field_frame.grid(row=5, column=0, padx=5, pady=5, sticky='w')

            fields = [
                ("Agency Name *", ttk.Entry),
                ("Address Line 1 *", ttk.Entry),
                ("Address Line 2", ttk.Entry),
                ("City *", ttk.Entry),
                ("State *", ttk.Combobox),
                ("Zip Code *", ttk.Entry),
                ("Phone Number *", ttk.Entry),
            ]

            entries = []
            for idx, (label_text, widget_type) in enumerate(fields):
                ttk.Label(field_frame, text=label_text, foreground='black').grid(row=idx, column=0, padx=5, pady=5, sticky='w')
                if label_text == 'State *':
                    widget = widget_type(field_frame, values=list(states.keys()))
                else:
                    widget = widget_type(field_frame)
                widget.grid(row=idx, column=1, padx=5, pady=5, sticky='w')
                entries.append(widget)

            button_frame = ttk.Frame(popup)
            button_frame.grid(row=6, column=0, padx=5, pady=5)

            # Update and Cancel buttons
            ttk.Button(button_frame, text="Save", command=lambda: [insert_new_agency(entries[0].get(), entries[1].get(), entries[2].get(), 
                                                                              entries[3].get(), entries[4].get(), entries[5].get(), entries[6].get()
                                                                              ), popup.destroy()]).grid(row=14, column=0, padx=5, pady=5, sticky='w')
            ttk.Button(button_frame, text="Cancel", command=lambda: [popup.destroy()]).grid(row=14, column=1, padx=5, pady=5, sticky='w')

        def get_all_personnel():
            try:
                config = load_config()
                with psycopg2.connect(**config) as conn:
                    with conn.cursor() as cur:
                        cur.execute("select employee_id, first_name, last_name from employee;")
                        personnel = cur.fetchall()
                        personMap = {(person[1] + " " + person[2]): person[0] for person in personnel}
                        return personMap
            except (psycopg2.DatabaseError, Exception) as error:
                print(f"{error}")
                exit()

        def insert_new_personnel(email, first, last, title, number):
            sqlQuery = """insert into employee (employee_id, agency_id, cac_id, email_addr, 
            first_name, last_name, job_title, phone_number)
            values (%s, %s, %s, %s, %s, %s, %s, %s)"""
            try:
                config = load_config()
                with psycopg2.connect(**config) as conn:
                    with conn.cursor() as cur:
                        cur.execute(sqlQuery, (random.randint(1, 99999999), 64669736, 1, email, first, last, title, number))
                        conn.commit
            except (psycopg2.DatabaseError, Exception) as error:
                print(f"{error}")
                exit()

        def add_personnel_popup():
            popup = tk.Toplevel(self)
            popup.title("New Personnel")
            popup.geometry("550x550")

            popup.grid_columnconfigure(0, weight=1)  
            popup.grid_columnconfigure(1, weight=1) 

            # existing personnel 
            personnelList = get_all_personnel()

            ttk.Label(popup, text="Below is a list of existing personnel.", foreground='black').grid(row=0, column=0, padx=5, pady=5, sticky='w')
            ttk.Label(popup, text="If the desired person is on this list, do not add again.", foreground='black').grid(row=1, column=0, padx=5, pady=5, sticky='w')
            ttk.Label(popup, text="If the person is not on the list enter person information into fields marked with (*) and click 'Save'.", foreground='red').grid(row=2, column=0, padx=5, pady=5, sticky='w')

            listbox_frame = ttk.Frame(popup)
            listbox_frame.grid(row=3, column=0, padx=10, pady=10, sticky='w')

            # Add a scrollbar for the listbox
            scrollbar = ttk.Scrollbar(listbox_frame, orient="vertical")

            # Listbox with adjusted width and integrated scrollbar
            personnel_listbox = tk.Listbox(listbox_frame, height=10, width=50, yscrollcommand=scrollbar.set)
            scrollbar.config(command=personnel_listbox.yview)
            for person in personnelList.keys():
                personnel_listbox.insert(tk.END, person)
            personnel_listbox.grid(row=0, column=0, sticky='ns')
            scrollbar.grid(row=0, column=1, sticky='ns')

            field_frame = ttk.Frame(popup)
            field_frame.grid(row=5, column=0, padx=5, pady=5, sticky='w')

            fields = [
                ("First Name *", ttk.Entry),
                ("Last Name *", ttk.Entry),
                ("Preface", ttk.Entry),
                ("Credentials", ttk.Entry),
                ("Job title *", ttk.Entry),
                ("Email", ttk.Entry),
                ("Phone Number *", ttk.Entry),
            ]

            entries = []
            for idx, (label_text, widget_type) in enumerate(fields):
                ttk.Label(field_frame, text=label_text, foreground='black').grid(row=idx, column=0, padx=5, pady=5, sticky='w')
                widget = widget_type(field_frame)
                widget.grid(row=idx, column=1, padx=5, pady=5, sticky='w')
                entries.append(widget)

            button_frame = ttk.Frame(popup)
            button_frame.grid(row=6, column=0, padx=5, pady=5)

            # Update and Cancel buttons
            ttk.Button(button_frame, text="Save", command=lambda: [insert_new_personnel(entries[5].get(), entries[0].get(), entries[1].get(), entries[4].get(), entries[6].get()), popup.destroy()]).grid(row=14, column=0, padx=5, pady=5)
            ttk.Button(button_frame, text="Cancel", command=lambda: [popup.destroy()]).grid(row=14, column=1, padx=5, pady=5)



        # Create the Referral section
        referral_frame = tk.LabelFrame(scrollable_frame, text="Referral", padx=10, pady=10)
        referral_frame.pack(fill="x", padx=10, pady=5)

        # Date (with DateEntry for calendar selection)
        ttk.Label(referral_frame, text="Date").grid(row=0, column=0, padx=5, pady=5)
        date_entry = DateEntry(referral_frame)
        date_entry.grid(row=0, column=1, padx=5, pady=5)

        agencies = get_all_agencies()

        ttk.Label(referral_frame, text="Referral Source").grid(row=1, column=0, sticky="w")
        referral_source = ttk.Combobox(referral_frame, values=list(agencies.keys()))
        referral_source.grid(row=1, column=1, padx=5, pady=5)

        persons = get_all_personnel()

        ttk.Label(referral_frame, text="Person").grid(row=2, column=0, padx=5, pady=5)
        person_entry = ttk.Combobox(referral_frame, values=list(persons.keys())) 
        person_entry.grid(row=2, column=1, padx=5, pady=5)

        ttk.Button(referral_frame, text="Add Referral Source", command=add_agency_popup).grid(row=1, column=2, padx=5, pady=5)
        ttk.Button(referral_frame, text="Add Person", command=add_personnel_popup).grid(row=2, column=2, padx=5, pady=5)


        #Create the VAS section
        vas_frame = tk.LabelFrame(scrollable_frame, text="Victim Advocacy Services", padx=10, pady=10)
        vas_frame.pack(fill="x", padx=10, pady=5)

        ttk.Label(vas_frame, text="VA Case Number").grid(row=0, column=0, padx=5, pady=5)
        va_casenum_entry = ttk.Entry(vas_frame) 
        va_casenum_entry.grid(row=0, column=1, padx=5, pady=5)

        agencies = get_all_agencies()

        ttk.Label(vas_frame, text="Agency").grid(row=1, column=0, padx=5, pady=5)
        agency_entry = ttk.Combobox(vas_frame, values=list(agencies.keys())) 
        agency_entry.grid(row=1, column=1, padx=5, pady=5)

        ttk.Button(vas_frame, text="Add Agency", command=add_agency_popup).grid(row=1, column=2, padx=5, pady=5)

        persons = get_all_personnel()

        ttk.Label(vas_frame, text="Person").grid(row=2, column=0, padx=5, pady=5)
        person_entry = ttk.Combobox(vas_frame, values=list(persons.keys())) 
        person_entry.grid(row=2, column=1, padx=5, pady=5) 

        ttk.Button(vas_frame, text="Add Person", command=add_personnel_popup).grid(row=2, column=2, padx=5, pady=5)

        ttk.Label(vas_frame, text="Date Services first offered to child/family").grid(row=3, column=0, padx=5, pady=5)
        date_services_offered = DateEntry(vas_frame)  
        date_services_offered.grid(row=3, column=1, padx=5, pady=5)

        services_accept = tk.BooleanVar(value=False)
        ttk.Label(vas_frame, text="Did the child/family accept VA services?").grid(row=4, column=0, padx=5, pady=5)
        services_accepted = ttk.Checkbutton(vas_frame, text="Yes", variable=services_accept)  
        services_accepted.grid(row=4, column=1, padx=5, pady=5, sticky="w")

        ttk.Label(vas_frame, text="Hope: (1)").grid(row=5, column=0, padx=5, pady=5)
        hope_entry = ttk.Combobox(vas_frame)  
        hope_entry.grid(row=5, column=1, padx=5, pady=5)

        tk.Label(vas_frame, text="VA Services Custom Field (2)").grid(row=6, column=0, padx=5, pady=5)
        custom_field2 = ttk.Combobox(vas_frame)  
        custom_field2.grid(row=6, column=1, padx=5, pady=5)

        tk.Label(vas_frame, text="VA Services Custom Field (3)").grid(row=7, column=0, padx=5, pady=5)
        custom_field3 = ttk.Combobox(vas_frame)  
        custom_field3.grid(row=7, column=1, padx=5, pady=5)

        tk.Label(vas_frame, text="VA Services Custom Field (4)").grid(row=8, column=0, padx=5, pady=5)
        custom_field4 = ttk.Combobox(vas_frame)  
        custom_field4.grid(row=8, column=1, padx=5, pady=5)

        tk.Label(vas_frame, text="VA Services Custom Field (5)").grid(row=9, column=0, padx=5, pady=5)
        custom_field5 = ttk.Combobox(vas_frame)  
        custom_field5.grid(row=9, column=1, padx=5, pady=5)

        tk.Label(vas_frame, text="Date Services were concluded").grid(row=10, column=0, padx=5, pady=5)
        services_conclusion = DateEntry(vas_frame)  
        services_conclusion.grid(row=10, column=1, padx=5, pady=5)

        mdt = tk.BooleanVar(value=False)
        ttk.Label(vas_frame, text="Ready for MDT Review").grid(row=11, column=0, padx=5, pady=5)
        mdt_ready = ttk.Checkbutton(vas_frame, text="Yes", variable=mdt)  
        mdt_ready.grid(row=11, column=1, padx=5, pady=5, sticky="w")

        #------------------------------

        # VAS Log Information
        def insert_new_session(date, start, end, status):
            sqlQuery = """insert into case_va_session_log(cac_id, case_id, case_va_session_id, start_time, end_time, va_provider_agency_id, session_date, session_status)
             VALUES(%s, %s, %s, %s, %s, %s, %s, %s);"""
            try:
                config = load_config()
                with psycopg2.connect(**config) as conn:
                    with conn.cursor() as cur:
                        cur.execute(sqlQuery, (3, 757172936, random.randint(1, 999999999), start, end, 51706749, date, status))
                        conn.commit
            except (psycopg2.DatabaseError, Exception) as error:
                print(f"{error}")
                exit()

        def generate_timestamps(start_date, interval_minutes):
            timestamps = []
            start_datetime = datetime.strptime(start_date, "%Y-%m-%d")
            end_datetime = start_datetime + timedelta(days=1)  
            current_datetime = start_datetime

            while current_datetime < end_datetime:
                timestamps.append(current_datetime.strftime("%Y-%m-%d %H:%M:%S"))
                current_datetime += timedelta(minutes=interval_minutes)
    
            return timestamps

        def add_new_session_popup():
            popup = tk.Toplevel(self)
            popup.title("New Session")
            popup.geometry("800x900")

            popup.grid_columnconfigure(0, weight=1)  
            popup.grid_columnconfigure(1, weight=1) 

            rowCounter = 0

            ttk.Label(popup, text="Fields marked with a (*) are required", foreground='red').grid(row=0, column=0, padx=5, pady=5, sticky='w')
            
            field_frame = ttk.Frame(popup)
            field_frame.grid(row=1, column=0, padx=5, pady=5, sticky='w')

            # Entry fields for case details
            ttk.Label(field_frame, text="Session Date *").grid(row=rowCounter, column=0, padx=5, pady=5)
            session_date_entry = DateEntry(field_frame, background='darkblue', foreground='white', borderwidth=2)
            session_date_entry.grid(row=rowCounter, column=1, padx=5, pady=5)
            rowCounter += 1

            times = generate_timestamps(str(session_date_entry.get_date()), 30)

            formattedTimes = []

            for time in times:
                formattedTimes.append(time.split(" ")[1])

            ttk.Label(field_frame, text="Start Time *").grid(row=rowCounter, column=0, padx=5, pady=5)
            start_time_entry = ttk.Combobox(field_frame, values=formattedTimes)
            start_time_entry.grid(row=rowCounter, column=1, padx=5, pady=5)
            rowCounter += 1

            ttk.Label(field_frame, text="End Time *").grid(row=rowCounter, column=0, padx=5, pady=5)
            end_start_entry = ttk.Combobox(field_frame, values=formattedTimes) 
            end_start_entry.grid(row=rowCounter, column=1, padx=5, pady=5)
            rowCounter += 1

            ttk.Label(field_frame, text="Prep").grid(row=rowCounter, column=0, padx=5, pady=5)
            prep_entry = ttk.Combobox(field_frame)
            prep_entry.grid(row=rowCounter, column=1, padx=5, pady=5)
            rowCounter += 1

            ttk.Label(field_frame, text="Session Status *").grid(row=rowCounter, column=0, padx=5, pady=5)
            session_status_entry = ttk.Combobox(field_frame, values=['1', '2', '3', '4'])
            session_status_entry.grid(row=rowCounter, column=1, padx=5, pady=5)
            rowCounter += 1

            ttk.Label(field_frame, text="Funding Source").grid(row=rowCounter, column=0, padx=5, pady=5)
            funding_source_entry = ttk.Combobox(field_frame)
            funding_source_entry.grid(row=rowCounter, column=1, padx=5, pady=5)
            rowCounter += 1

            ttk.Label(field_frame, text="Location").grid(row=rowCounter, column=0, padx=5, pady=5)
            location_entry = ttk.Combobox(field_frame)
            location_entry.grid(row=rowCounter, column=1, padx=5, pady=5)
            rowCounter += 1

            ttk.Label(field_frame, text="Provider Agency").grid(row=rowCounter, column=0, padx=5, pady=5)
            provider_agency_entry = ttk.Combobox(field_frame)
            provider_agency_entry.grid(row=rowCounter, column=1, padx=5, pady=5)
            rowCounter += 1

            ttk.Label(field_frame, text="Provider Employee").grid(row=rowCounter, column=0, padx=5, pady=5)
            provider_employee_entry = ttk.Combobox(field_frame)
            provider_employee_entry.grid(row=rowCounter, column=1, padx=5, pady=5)
            rowCounter += 1

            ttk.Label(field_frame, text="Attendees").grid(row=rowCounter, column=0, padx=5, pady=5)
            rowCounter += 1
            attendee1Check = tk.BooleanVar(value=False)
            attendee2Check = tk.BooleanVar(value=False)
            attendee3Check = tk.BooleanVar(value=False)
            attendee4Check = tk.BooleanVar(value=False)
            attendee1 = ttk.Checkbutton(field_frame, text="Billie Badguys", variable=attendee1Check).grid(row=rowCounter, column=1, sticky="w")
            attendee2 = ttk.Checkbutton(field_frame, text="Bobbie RRose", variable=attendee2Check).grid(row=rowCounter, column=2, sticky="w")
            rowCounter += 1
            attendee3 = ttk.Checkbutton(field_frame, text="Candi Rose", variable=attendee3Check).grid(row=rowCounter, column=1, sticky="w")
            attendee4 = ttk.Checkbutton(field_frame, text="Cindi Rose", variable=attendee4Check).grid(row=rowCounter, column=2, sticky="w")
            rowCounter += 1

            ttk.Label(field_frame, text="Services Provided").grid(row=rowCounter, column=0, padx=5, pady=5)
            service1Check = tk.BooleanVar(value=False)
            service2Check = tk.BooleanVar(value=False)
            service3Check = tk.BooleanVar(value=False)
            service4Check = tk.BooleanVar(value=False)
            service5Check = tk.BooleanVar(value=False)
            service6Check = tk.BooleanVar(value=False)
            service7Check = tk.BooleanVar(value=False)
            service8Check = tk.BooleanVar(value=False)
            service9Check = tk.BooleanVar(value=False)
            service10Check = tk.BooleanVar(value=False)
            service11Check = tk.BooleanVar(value=False)
            service12Check = tk.BooleanVar(value=False)
            service13Check = tk.BooleanVar(value=False)
            service14Check = tk.BooleanVar(value=False)
            service15Check = tk.BooleanVar(value=False)
            service16Check = tk.BooleanVar(value=False)
            service17Check = tk.BooleanVar(value=False)
            service18Check = tk.BooleanVar(value=False)
            service19Check = tk.BooleanVar(value=False)
            service20Check = tk.BooleanVar(value=False)
            service21Check = tk.BooleanVar(value=False)
            service22Check = tk.BooleanVar(value=False)
            service23Check = tk.BooleanVar(value=False)
            service24Check = tk.BooleanVar(value=False)
            service25Check = tk.BooleanVar(value=False)
            service26Check = tk.BooleanVar(value=False)
            service27Check = tk.BooleanVar(value=False)
            service28Check = tk.BooleanVar(value=False)
            service29Check = tk.BooleanVar(value=False)
            service30Check = tk.BooleanVar(value=False)
            rowCounter += 1
            service1 = ttk.Checkbutton(field_frame, text="Legal Services", variable=service1Check).grid(row=rowCounter, column=1, sticky="w")
            service2 = ttk.Checkbutton(field_frame, text="Transportation", variable=service2Check).grid(row=rowCounter, column=2, sticky="w")
            rowCounter += 1

            service3 = ttk.Checkbutton(field_frame, text="Victim Support", variable=service3Check).grid(row=12, column=1, sticky="w")
            service4 = ttk.Checkbutton(field_frame, text="1-2 Week Follow-up Call", variable=service4Check).grid(row=12, column=2, sticky="w")
            rowCounter += 1

            service5 = ttk.Checkbutton(field_frame, text="2. Personal Court Education", variable=service5Check).grid(row=13, column=1, sticky="w")
            service6 = ttk.Checkbutton(field_frame, text="24 -- hour crisis line cal", variable=service6Check).grid(row=13, column=2, sticky="w")
            rowCounter += 1

            service7 = ttk.Checkbutton(field_frame, text="3a. Info & Support - MDT response", variable=service7Check).grid(row=14, column=1, sticky="w")
            service8 = ttk.Checkbutton(field_frame, text="3b. Information & Support - Court", variable=service8Check).grid(row=14, column=2, sticky="w")
            rowCounter += 1

            service9 = ttk.Checkbutton(field_frame, text="3bi Personal advocacy", variable=service9Check).grid(row=15, column=1, sticky="w")
            service10 = ttk.Checkbutton(field_frame, text="6--8 Week Follow-up Call", variable=service10Check).grid(row=15, column=2, sticky="w")
            rowCounter += 1

            service11 = ttk.Checkbutton(field_frame, text="B2. Victim Advocacy/Accompaniment to Medical Forensic Exam", variable=service11Check).grid(row=16, column=1, sticky="w")
            service12 = ttk.Checkbutton(field_frame, text="Collected Survey", variable=service12Check).grid(row=16, column=2, sticky="w")
            rowCounter += 1

            service13 = ttk.Checkbutton(field_frame, text="Criminal Justice support/advocacy", variable=service13Check).grid(row=17, column=1, sticky="w")
            service14 = ttk.Checkbutton(field_frame, text="Compensation Claim Filing", variable=service14Check).grid(row=17, column=2, sticky="w")
            rowCounter += 1

            service15 = ttk.Checkbutton(field_frame, text="Emergency Crisis Intervention", variable=service15Check).grid(row=18, column=1, sticky="w")
            service16 = ttk.Checkbutton(field_frame, text="Crisis Counseling", variable=service16Check).grid(row=18, column=2, sticky="w")
            rowCounter += 1

            service17 = ttk.Checkbutton(field_frame, text="Gave Educational Information", variable=service17Check).grid(row=19, column=1, sticky="w")
            service18 = ttk.Checkbutton(field_frame, text="Follow-up", variable=service18Check).grid(row=19, column=2, sticky="w")
            rowCounter += 1

            service19 = ttk.Checkbutton(field_frame, text="Homeless support group", variable=service19Check).grid(row=20, column=1, sticky="w")
            service20 = ttk.Checkbutton(field_frame, text="Initial Meeting with Caregiver", variable=service20Check).grid(row=20, column=2, sticky="w")
            rowCounter += 1

            service21 = ttk.Checkbutton(field_frame, text="Initial Telephone Call", variable=service21Check).grid(row=21, column=1, sticky="w")
            service22 = ttk.Checkbutton(field_frame, text="Mailed Brochure", variable=service22Check).grid(row=21, column=2, sticky="w")
            rowCounter += 1

            service23 = ttk.Checkbutton(field_frame, text="Orientation to Center for FI", variable=service23Check).grid(row=22, column=1, sticky="w")
            service24 = ttk.Checkbutton(field_frame, text="Post Interview Crisis Counseling", variable=service24Check).grid(row=22, column=2, sticky="w")
            rowCounter += 1

            service25 = ttk.Checkbutton(field_frame, text="Pre-Interview Family Call", variable=service25Check).grid(row=23, column=1, sticky="w")
            service26 = ttk.Checkbutton(field_frame, text="Shelter/safehouse Referral", variable=service26Check).grid(row=23, column=2, sticky="w")
            rowCounter += 1

            service27 = ttk.Checkbutton(field_frame, text="Survey Distributed", variable=service27Check).grid(row=24, column=1, sticky="w")
            service28 = ttk.Checkbutton(field_frame, text="Survey Recieved", variable=service28Check).grid(row=24, column=2, sticky="w")
            rowCounter += 1

            service29 = ttk.Checkbutton(field_frame, text="Telephone Follow-up", variable=service29Check).grid(row=25, column=1, sticky="w")
            service30 = ttk.Checkbutton(field_frame, text="Unscheduled Call", variable=service30Check).grid(row=25, column=2, sticky="w")
            rowCounter += 1

            ttk.Label(field_frame, text="Comments").grid(row=rowCounter, column=0, padx=5, pady=5)
            session_comments_entry = ttk.Entry(field_frame)
            session_comments_entry.grid(row=rowCounter, column=1, padx=5, pady=5)
            rowCounter += 1

            ttk.Label(field_frame, text="VA Session Custom Field 1").grid(row=rowCounter, column=0, padx=5, pady=5)
            session_custom_one_entry = ttk.Entry(field_frame)
            session_custom_one_entry.grid(row=rowCounter, column=1, padx=5, pady=5)
            rowCounter += 1

            ttk.Label(field_frame, text="VA Session Custom Field 2").grid(row=rowCounter, column=0, padx=5, pady=5)
            session_custom_two_entry = ttk.Entry(field_frame)
            session_custom_two_entry.grid(row=rowCounter, column=1, padx=5, pady=5)
            rowCounter += 1

            ttk.Label(field_frame, text="VA Session Custom Field 3").grid(row=rowCounter, column=0, padx=5, pady=5)
            session_custom_three_entry = ttk.Entry(field_frame)
            session_custom_three_entry.grid(row=rowCounter, column=1, padx=5, pady=5)
            rowCounter += 1

            button_frame = ttk.Frame(popup)
            button_frame.grid(row=rowCounter, column=0, columnspan=3, pady=15)

            # Update and Cancel buttons
            ttk.Button(button_frame, text="Save", command=lambda: [insert_new_session(session_date_entry.get_date(), (str(session_date_entry.get_date()) + " " + start_time_entry.get()), 
                                                                               (str(session_date_entry.get_date()) + " " + end_start_entry.get()), session_status_entry.get()), popup.destroy()]).grid(row=0, column=0, padx=5, pady=5)
            ttk.Button(button_frame, text="Cancel", command=lambda: [popup.destroy()]).grid(row=0, column=1, padx=5, pady=5)

        def get_all_sessions():
            try:
                config = load_config()
                with psycopg2.connect(**config) as conn:
                    with conn.cursor() as cur:
                        cur.execute("select session_date, start_time, end_time, session_status from case_va_session_log;")
                        sessions = cur.fetchall()
                        return sessions
            except (psycopg2.DatabaseError, Exception) as error:
                print(f"{error}")
                exit()

        vas_log_frame = tk.LabelFrame(scrollable_frame, text="Victim Advocacy Services Log", padx=10, pady=10)
        vas_log_frame.pack(fill="x", padx=10, pady=5)

        sessions = get_all_sessions()

        ttk.Button(vas_log_frame, text="Add New Session Log", command=add_new_session_popup).grid(row=0, column=0, padx=5, pady=5)
        ttk.Button(vas_log_frame, text="Details").grid(row=0, column=1, padx=5, pady=5)
        ttk.Button(vas_log_frame, text="Newer Records").grid(row=0, column=2, padx=5, pady=5)
        ttk.Button(vas_log_frame, text="Older Records").grid(row=0, column=3, padx=5, pady=5)
        
        rowCounter = 2

        ttk.Label(vas_log_frame, text="Date").grid(row=1, column=1)
        ttk.Label(vas_log_frame, text="Start Time").grid(row=1, column=2)
        ttk.Label(vas_log_frame, text="End Time").grid(row=1, column=3)
        ttk.Label(vas_log_frame, text="Status").grid(row=1, column=4)

        for session in sessions:
            ttk.Label(vas_log_frame, text=session[0]).grid(row=rowCounter, column=1)
            ttk.Label(vas_log_frame, text=session[1]).grid(row=rowCounter, column=2)
            ttk.Label(vas_log_frame, text=session[2]).grid(row=rowCounter, column=3)
            ttk.Label(vas_log_frame, text=session[3]).grid(row=rowCounter, column=4)
            rowCounter += 1
        #------------------------------

        # Crime Compensation Application Section
        crime_comp_app_frame = tk.LabelFrame(scrollable_frame, text="Crime Compensation Application", padx=10, pady=10)
        crime_comp_app_frame.pack(fill="x", padx=10, pady=5)

        ttk.Label(crime_comp_app_frame, text="State Claim Representative").grid(row=0, column=0, padx=5, pady=5)
        state_claim_rep = ttk.Entry(crime_comp_app_frame)  
        state_claim_rep.grid(row=0, column=1, padx=5, pady=5)

        birth_cert = tk.BooleanVar(value=False)
        ttk.Label(crime_comp_app_frame, text="Have Birth Certificate").grid(row=1, column=0, padx=5, pady=5)
        has_birth_cert = ttk.Checkbutton(crime_comp_app_frame, variable=birth_cert)  
        has_birth_cert.grid(row=1, column=1, padx=5, pady=5, sticky="w")

        police_report = tk.BooleanVar(value=False)
        ttk.Label(crime_comp_app_frame, text="Have Police Report").grid(row=2, column=0, padx=5, pady=5)
        has_police_report = ttk.Checkbutton(crime_comp_app_frame, variable=police_report)  
        has_police_report.grid(row=2, column=1, padx=5, pady=5, sticky="w")

        ttk.Label(crime_comp_app_frame, text="Claim Number").grid(row=3, column=0, padx=5, pady=5)
        claim_number = ttk.Entry(crime_comp_app_frame)  
        claim_number.grid(row=3, column=1, padx=5, pady=5)

        ttk.Label(crime_comp_app_frame, text="Date Application Mailed").grid(row=4, column=0, padx=5, pady=5)
        date_app_mailed = DateEntry(crime_comp_app_frame)  
        date_app_mailed.grid(row=4, column=1, padx=5, pady=5)

        ttk.Label(crime_comp_app_frame, text="Status").grid(row=5, column=0, padx=5, pady=5)
        status_entry = ttk.Combobox(crime_comp_app_frame)  
        status_entry.grid(row=5, column=1, padx=5, pady=5)

        ttk.Label(crime_comp_app_frame, text="Application Assistance Provided (1)").grid(row=6, column=0, padx=5, pady=5)
        app_assistance_provided = ttk.Combobox(crime_comp_app_frame)  
        app_assistance_provided.grid(row=6, column=1, padx=5, pady=5)

        ttk.Label(crime_comp_app_frame, text="Crime Compensation Application Custom Field (2)").grid(row=7, column=0, padx=5, pady=5)
        cca_customfield2 = ttk.Entry(crime_comp_app_frame)  
        cca_customfield2.grid(row=7, column=1, padx=5, pady=5)

        ttk.Label(crime_comp_app_frame, text="Reason Claim Denied").grid(row=8, column=0, padx=5, pady=5)
        claim_denied_reason = ttk.Entry(crime_comp_app_frame)  
        claim_denied_reason.grid(row=8, column=1, padx=5, pady=5)

        #--------------------------------
        # -Screenings Given Section

        def insert_new_instrument(name):
            sqlQuery = """insert into case_mh_assessment_instrument (instrument_id, assessment_name)
                                    values(%s, %s);"""
            try:
                config = load_config()
                with psycopg2.connect(**config) as conn:
                    with conn.cursor() as cur:
                        cur.execute(sqlQuery, (random.randint(1, 999999), name))
                        conn.commit
            except (psycopg2.DatabaseError, Exception) as error:
                print(f"{error}")
                exit()

        def add_screening_instrument_popup():
            popup = tk.Toplevel(self)
            popup.title("Add New Screening Instrument")
            popup.geometry("350x200")

            popup.grid_columnconfigure(0, weight=0)  
            popup.grid_columnconfigure(1, weight=1)

            ttk.Label(popup, text="Fields marked with a (*) are required", foreground='red').grid(row=0, column=0, padx=5, pady=5, sticky='w')

            ttk.Label(popup, text="Screening Instrument Name *", foreground='black').grid(row=1, column=0, padx=5, pady=5, sticky='w')
            instrument_name_entry = ttk.Entry(popup)
            instrument_name_entry.grid(row=1, column=1, padx=5, pady=5, sticky='w')

            ttk.Label(popup, text="Source", foreground='black').grid(row=2, column=0, padx=5, pady=5, sticky='w')
            provider_agency_entry = ttk.Combobox(popup)
            provider_agency_entry.grid(row=2, column=1, padx=5, pady=5, sticky='w')

            ttk.Label(popup, text="# of Measures", foreground='black').grid(row=3, column=0, padx=5, pady=5, sticky='w')
            provider_personnel_entry = ttk.Combobox(popup) 
            provider_personnel_entry.grid(row=3, column=1, padx=5, pady=5, sticky='w')


            button_frame = ttk.Frame(popup)
            button_frame.grid(row=4, column=0, columnspan=2, pady=10)

            # Update and Cancel buttons
            ttk.Button(button_frame, text="Save", command=lambda: [insert_new_instrument(instrument_name_entry.get()), popup.destroy()]).grid(row=4, column=0, padx=5, pady=5)
            ttk.Button(button_frame, text="Cancel", command=lambda: [popup.destroy()]).grid(row=4, column=1, padx=5, pady=5)

        def insert_new_screening(date, personnel, instrument):
            sqlQuery = """insert into case_mh_assessment (cac_id, case_id, assessment_id, 
                                    mh_provider_agency_id, session_date, agency_id, provider_employee_id, 
                                    assessment_instrument_id)
                                    values(%s, %s, %s, %s, %s, %s, %s, %s);"""
            try:
                config = load_config()
                with psycopg2.connect(**config) as conn:
                    with conn.cursor() as cur:
                        cur.execute(sqlQuery, (1, 302621084, random.randint(1, 99999999), 64669736, date, 64669736, personnel, instrument))
                        conn.commit
            except (psycopg2.DatabaseError, Exception) as error:
                print(f"{error}")
                exit()

        def get_all_instruments():
            sqlQuery = """select * from case_mh_assessment_instrument;"""
            try:
                config = load_config()
                with psycopg2.connect(**config) as conn:
                    with conn.cursor() as cur:
                        cur.execute(sqlQuery)
                        instruments = cur.fetchall()
                        instrumentMap = {instrument[1]: instrument[0] for instrument in instruments}
                        return instrumentMap
            except (psycopg2.DatabaseError, Exception) as error:
                print(f"{error}")
                exit()        

        def add_new_screening_popup():
            popup = tk.Toplevel(self)
            popup.title("Add New Screening")
            popup.geometry("550x350")

            popup.grid_columnconfigure(0, weight=0)  
            popup.grid_columnconfigure(1, weight=1)

            instruments = get_all_instruments()
            agencies = get_all_agencies()
            personnel = get_all_personnel()
            
            field_frame = ttk.Frame(popup)
            field_frame.grid(row=1, column=0, padx=5, pady=5, sticky='w')

            ttk.Label(popup, text="Fields marked with a (*) are required", foreground='red').grid(row=0, column=0, padx=5, pady=5, sticky='w')

            ttk.Label(field_frame, text="Screening Instrument *", foreground='black').grid(row=0, column=0, padx=5, pady=5, sticky='w')

            screening_instrument_entry = ttk.Combobox(field_frame, values=list(instruments.keys()))
            screening_instrument_entry.grid(row=0, column=1, padx=5, pady=5, sticky='w')

            ttk.Label(field_frame, text="Scores of this Screening's Measures").grid(row=1, column=0, padx=5, pady=5, sticky='w')
            ttk.Label(field_frame).grid(row=1, column=1, padx=5, pady=5, sticky='w')

            ttk.Button(field_frame, text="Add Screening Instrument", command=add_screening_instrument_popup).grid(row=0, column=2, padx=5, pady=5, sticky='w')

            ttk.Label(field_frame, text="Screening Date *", foreground='black').grid(row=2, column=0, padx=5, pady=5, sticky='w')
            screening_date_entry = DateEntry(field_frame, background='darkblue', foreground='white', borderwidth=2)
            screening_date_entry.grid(row=2, column=1, padx=5, pady=5, sticky='w')

            ttk.Label(field_frame, text="Provider Agency", foreground='black').grid(row=3, column=0, padx=5, pady=5, sticky='w')
            provider_agency_entry = ttk.Combobox(field_frame, values=list(agencies.keys()))
            provider_agency_entry.grid(row=3, column=1, padx=5, pady=5, sticky='w')

            ttk.Label(field_frame, text="Provider Personnel *", foreground='black').grid(row=4, column=0, padx=5, pady=5, sticky='w')
            provider_personnel_entry = ttk.Combobox(field_frame, values=list(personnel.keys())) 
            provider_personnel_entry.grid(row=4, column=1, padx=5, pady=5, sticky='w')

            ttk.Label(field_frame, text="Functional Impairment").grid(row=5, column=0, padx=5, pady=5, sticky='w')
            functional_impairment_entry = ttk.Entry(field_frame)
            functional_impairment_entry.grid(row=5, column=1, padx=5, pady=5, sticky='w')

            ttk.Label(field_frame, text="Comments").grid(row=6, column=0, padx=5, pady=5, sticky='w')
            _screening_commets_entry = ttk.Entry(field_frame)
            _screening_commets_entry.grid(row=6, column=1, padx=5, pady=5, sticky='w')

            button_frame = ttk.Frame(popup)
            button_frame.grid(row=2, column=0, columnspan=3, pady=15)

            # Update and Cancel buttons
            ttk.Button(button_frame, text="Save", command=lambda: [insert_new_screening(screening_date_entry.get_date(), provider_personnel_entry.get()[0], screening_instrument_entry.get()[0]), popup.destroy()]).grid(row=0, column=0, padx=5, pady=5, sticky='w')
            ttk.Button(button_frame, text="Cancel", command=lambda: [popup.destroy()]).grid(row=0, column=1, padx=5, pady=5, sticky='w')

        def get_all_screenings():
            try:
                config = load_config()
                with psycopg2.connect(**config) as conn:
                    with conn.cursor() as cur:
                        cur.execute("""select case_mh_assessment_instrument.assessment_name, 
                                    case_mh_assessment.session_date, 
                                    employee.first_name,
                                    employee.last_name 
                                    from case_mh_assessment
                                    join case_mh_assessment_instrument on case_mh_assessment.assessment_instrument_id = case_mh_assessment_instrument.instrument_id
                                    join employee on case_mh_assessment.provider_employee_id = employee.employee_id;""")
                        screenings = cur.fetchall()
                        return screenings
            except (psycopg2.DatabaseError, Exception) as error:
                print(f"{error}")
                exit()

        screenings_frame = tk.LabelFrame(scrollable_frame, text="Screenings Given", padx=10, pady=10)
        screenings_frame.pack(fill="x", padx=10, pady=5)

        #Add New Screening button
        ttk.Button(screenings_frame, text="Add New Screening", command=add_new_screening_popup).grid(row=0, column=0, padx=5, pady=5)

        screenings = get_all_screenings()
        rowCounter = 2

        ttk.Label(screenings_frame, text="Action").grid(row=1, column=0, padx=5, pady=5)
        ttk.Label(screenings_frame, text="Screening Instrument Name").grid(row=1, column=2, padx=5, pady=5)
        ttk.Label(screenings_frame, text="Date").grid(row=1, column=3, padx=5, pady=5)
        ttk.Label(screenings_frame, text="Provider Personnel").grid(row=1, column=4, padx=5, pady=5)

        #ttk.Label(screenings_frame, text=screening[0]).grid(row=2, column=1, padx=5, pady=5) Actions

        for screening in screenings:
         ttk.Label(screenings_frame, text=screening[0]).grid(row=rowCounter, column=2, padx=5, pady=5)
         ttk.Label(screenings_frame, text=screening[1]).grid(row=rowCounter, column=3, padx=5, pady=5)
         ttk.Label(screenings_frame, text=screening[2] + " " + screening[3]).grid(row=rowCounter, column=4, padx=5, pady=5)
         rowCounter += 1

        #--------------------------------------

        def add_referral_popup():
            # Create a new Toplevel window
            popup = tk.Toplevel(self)
            popup.title("Add Referral")
            popup.geometry("400x300")

            ttk.Label(popup, text="Date").grid(row=1, column=0, padx=5, pady=5)
            referral_date_entry = DateEntry(popup, background='darkblue', foreground='white', borderwidth=2)
            referral_date_entry.grid(row=1, column=1, padx=5, pady=5)

            ttk.Label(popup, text="Referred To").grid(row=2, column=0, padx=5, pady=5)
            referred_to_combo = ttk.Entry(popup)
            referred_to_combo.grid(row=2, column=1, padx=5, pady=5)

            ttk.Label(popup, text="Comment").grid(row=3, column=0, padx=5, pady=5)
            comment_entry = ttk.Entry(popup)
            comment_entry.grid(row=3, column=1, padx=5, pady=5)

            # Update and Cancel buttons
            ttk.Button(popup, text="Update", command=popup.destroy).grid(row=4, column=0, padx=5, pady=5)
            ttk.Button(popup, text="Cancel", command=popup.destroy).grid(row=4, column=1, padx=5, pady=5)

        # Outside Referrals Section
        outside_referrals_frame = tk.LabelFrame(scrollable_frame, text="Outside Referrals", padx=10, pady=10)
        outside_referrals_frame.pack(fill="x", padx=10, pady=5)

        ttk.Label(outside_referrals_frame, text="Referred From").grid(row=1, column=1, padx=5, pady=5)
        referral_from_entry = ttk.Entry(outside_referrals_frame)
        referral_from_entry.grid(row=2, column=1, padx=5, pady=5)

        ttk.Label(outside_referrals_frame, text="Referral Date").grid(row=1, column=2, padx=5, pady=5)
        referral_date_entry = ttk.Entry(outside_referrals_frame)
        referral_date_entry.grid(row=2, column=2, padx=5, pady=5)

        ttk.Label(outside_referrals_frame, text="Referred To").grid(row=1, column=3, padx=5, pady=5)
        referral_to_entry = ttk.Entry(outside_referrals_frame)
        referral_to_entry.grid(row=2, column=3, padx=5, pady=5)

        ttk.Label(outside_referrals_frame, text="Comments").grid(row=1, column=4, padx=5, pady=5)
        comments_entry = ttk.Entry(outside_referrals_frame)
        comments_entry.grid(row=2, column=4, padx=5, pady=5)

        ttk.Button(outside_referrals_frame, text="Add New Referral", command=add_referral_popup).grid(row=0, column=0, padx=5, pady=5, sticky="w")

        #----------------------

        #Add contact modal
        def add_contact_popup():
            # Create a new Toplevel window
            popup = tk.Toplevel(self)
            popup.title("Add New Point of Contact")
            popup.geometry("400x300")

            #  labels and entry fields
            ttk.Label(popup, text="Agency").grid(row=0, column=0, padx=5, pady=5)
            agency_entry = ttk.Entry(popup)
            agency_entry.grid(row=0, column=1, padx=5, pady=5)

            ttk.Label(popup, text="Name").grid(row=1, column=0, padx=5, pady=5)
            name_entry = ttk.Entry(popup)
            name_entry.grid(row=1, column=1, padx=5, pady=5)

            ttk.Label(popup, text="Phone").grid(row=2, column=0, padx=5, pady=5)
            phone_entry = ttk.Entry(popup)
            phone_entry.grid(row=2, column=1, padx=5, pady=5)

            ttk.Label(popup, text="Email").grid(row=3, column=0, padx=5, pady=5)
            email_entry = ttk.Entry(popup)
            email_entry.grid(row=3, column=1, padx=5, pady=5)

            # update/cancel buttons
            ttk.Button(popup, text="Save", command=lambda: [popup.destroy()]).grid(row=4, column=0, padx=5, pady=5)
            ttk.Button(popup, text="Cancel", command=lambda: [popup.destroy()]).grid(row=4, column=1, padx=5, pady=5)
        # Additional Points of Contact Section
        additional_contact_frame = tk.LabelFrame(scrollable_frame, text="Additional Points of Contact", padx=10, pady=10)
        additional_contact_frame.pack(fill="x", padx=10, pady=5)

        # button to add a new point of contact
        ttk.Button(additional_contact_frame, text="+ Add New Point of Contact", command=add_contact_popup).grid(row=0, column=0, padx=5, pady=5, sticky="w")
        ttk.Label(additional_contact_frame, text="Action").grid(row=1, column=0, padx=5, pady=5)
        ttk.Label(additional_contact_frame, text="Agency").grid(row=1, column=1, padx=5, pady=5)
        ttk.Label(additional_contact_frame, text="Name").grid(row=1, column=2, padx=5, pady=5)
        ttk.Label(additional_contact_frame, text="Phone").grid(row=1, column=3, padx=5, pady=5)
        ttk.Label(additional_contact_frame, text="Email").grid(row=1, column=4, padx=5, pady=5)

        # Document Upload Section
        upload_frame = tk.LabelFrame(scrollable_frame, text="Document Upload", padx=10, pady=10)
        upload_frame.pack(fill="x", padx=10, pady=5)

        ttk.Label(upload_frame, text="File Name:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        file_name_var = tk.StringVar()  # Variable to hold the filename
        file_name_entry = ttk.Entry(upload_frame, textvariable=file_name_var, width=50, state="readonly")
        file_name_entry.grid(row=0, column=1, padx=5, pady=5)

        # Function to open file dialog and set the filename
        def select_file():
            file_path = tk.filedialog.askopenfilename(title="Select a file", filetypes=[("All files", "*.*")])
            if file_path:  # If a file is selected
                file_name_var.set(file_path.split("/")[-1])  # Set the filename in the entry

        # Button to trigger file selection
        ttk.Button(upload_frame, text="Select Files...", command=select_file).grid(row=0, column=2, padx=5, pady=5)

        # Add placeholder for upload status (could be enhanced later)
        upload_status_label = ttk.Label(upload_frame, text="Maximum allowed file size is 10 MB.")
        upload_status_label.grid(row=1, column=0, columnspan=3, padx=5, pady=5)