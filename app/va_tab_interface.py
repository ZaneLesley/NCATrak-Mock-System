import tkinter as tk
from tkinter import ttk
from tkinter import filedialog, messagebox
from tkcalendar import DateEntry
import database_lookup_search
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
import case_notes


class va_interface(tk.Frame):

    def __init__(self, parent, controller):

        def get_default_case():
            try:
                config = load_config()
                with psycopg2.connect(**config) as conn:
                    with conn.cursor() as cur:
                        cur.execute("select * from cac_case limit 1;")
                        case = cur.fetchone()
                        return case
            except (psycopg2.DatabaseError, Exception) as error:
                print(f"{error}")
                exit()


        def get_case(id):
            try:
                config = load_config()
                with psycopg2.connect(**config) as conn:
                    with conn.cursor() as cur:
                        cur.execute("select * from cac_case where case_id = %s;", (id,))
                        case = cur.fetchone()
                        return case
            except (psycopg2.DatabaseError, Exception) as error:
                print(f"{error}")
                exit()

        tk.Frame.__init__(self, parent)

        self.controller = controller

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
    
        with open("case_id.txt", "r") as file:
            case = get_case(file.read())

        if case is None:
            case = get_default_case()

        cacId = case[0]
        caseId = case[1]
        caseNumber = case[2]
        caseReceivedDate = case[3]
        caseClosedDate = case[4]
        caseClosedReasonId = case[5]
        caseCreatedDate = case[6]
        leadEmployeeId = case[7]
        vaAgencyId = case[19]
        vaCaseNumber = case[20]
        claimDeniedReason = case[21]
        claimNumber = case[22]
        claimStatusId = case[23]
        hasBirthCert = case[24]
        hasPoliceReport = case[25]
        mdtReady = case[26]
        vaNa = case[27]
        referralAgencyId = case[28]
        referralDate = case[29]
        servicesAccepted = case[30]
        servicesOfferedDate = case[31]
        servicesEndDate = case[32]

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
            ("Mental Health - Case Notes", self.show_case_notes),
            ("VA", self.show_va_tab),
        ]

        for btn_text, btn_command in nav_buttons:
            button = ttk.Button(button_frame, text=btn_text, command=btn_command)
            button.pack(side='left', padx=5)

        # Reload button - fully reloads the application
        refresh_button = ttk.Button(button_frame, text="Reload", command=controller.refresh)
        refresh_button.pack(side='right', padx=5)

        # Display current case ID
        current_case_id_file = open("case_id.txt", "r")
        current_case_id = int(current_case_id_file.readline())
        current_case_id_file.close()
        case_id_font = ("Helvetica", 10)
        tk.Label(button_frame, text=f"Case ID: {current_case_id}", font=case_id_font).pack(side='right', padx=30)

        # VA tab title
        va_frame = tk.Frame(scrollable_frame)
        va_frame.grid(row=1, column=0, sticky='w', pady=10, padx=10)
        ttk.Label(va_frame, text="VA").pack()

        def get_all_states():
            try:
                config = load_config()
                with psycopg2.connect(**config) as conn:
                    with conn.cursor() as cur:
                        cur.execute("select * from state_table;")
                        states = cur.fetchall()
                        stateMap = {state[1]: state[0] for state in states}
                        return stateMap
            except (psycopg2.DatabaseError, Exception) as error:
                print(f"{error}")
                exit()

        def get_all_agencies():
            try:
                config = load_config()
                with psycopg2.connect(**config) as conn:
                    with conn.cursor() as cur:
                        cur.execute("select * from cac_agency order by agency_name;")
                        agencies = cur.fetchall()
                        agencyMap = {agency[0]: agency[2] for agency in agencies}
                        agencyMapReversed = {agency[2]: agency[0] for agency in agencies}
                        return agencyMap, agencyMapReversed
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
                        messagebox.showinfo("Save", "Agency has been saved successfully!")
            except (psycopg2.DatabaseError, Exception) as error:
                print(f"{error}")
                exit()

        def add_agency_popup():
            popup = tk.Toplevel(self)
            popup.title("New Agency")
            popup.geometry("550x550")

            agencies, aReverse = get_all_agencies()

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
            for agency_name in agencies.values():
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
                    widget = widget_type(field_frame, values=list(states.values()))
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
                        cur.execute("select employee_id, first_name, last_name from employee order by last_name;")
                        personnel = cur.fetchall()
                        personMap = {person[0]: (person[1] + " " + person[2]) for person in personnel}
                        personMapReverse = { (person[1] + " " + person[2]): person[0] for person in personnel}
                        return personMap, personMapReverse
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
                        messagebox.showinfo("Save", "Person has been saved successfully!")
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
            persons, pReverse = get_all_personnel()

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
            for person in persons.values():
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
        referral_frame.grid(row=2, column=0, sticky='w', padx=10, pady=5)

        # Date (with DateEntry for calendar selection)
        ttk.Label(referral_frame, text="Date").grid(row=0, column=0, padx=5, pady=5)
        date_entry = DateEntry(referral_frame)
        date_entry.grid(row=0, column=1, padx=5, pady=5)
        if referralDate is not None:
            date_entry.set_date(referralDate)

        agencies, aReverse = get_all_agencies()

        ttk.Label(referral_frame, text="Referral Source").grid(row=1, column=0, sticky="w")
        referral_source = ttk.Combobox(referral_frame, values=list(agencies.values()), state='readonly')
        referral_source.grid(row=1, column=1, padx=5, pady=5)
        if agencies.get(referralAgencyId) is not None:
            referral_source.set(agencies[referralAgencyId])

        persons, pReverse = get_all_personnel()

        ttk.Label(referral_frame, text="Person").grid(row=2, column=0, padx=5, pady=5)
        person_entry = ttk.Combobox(referral_frame, values=list(persons.values())) 
        person_entry.grid(row=2, column=1, padx=5, pady=5)
        if persons.get(leadEmployeeId) is not None:
            person_entry.set(persons[leadEmployeeId])
        
        ttk.Button(referral_frame, text="Add Referral Source", command=add_agency_popup).grid(row=1, column=2, padx=5, pady=5)
        ttk.Button(referral_frame, text="Add Person", command=add_personnel_popup).grid(row=2, column=2, padx=5, pady=5)


        #Create the VAS section
        vas_frame = tk.LabelFrame(scrollable_frame, text="Victim Advocacy Services", padx=10, pady=10)
        vas_frame.grid(row=3, column=0, sticky='w', padx=10, pady=5)

        ttk.Label(vas_frame, text="VA Case Number").grid(row=0, column=0, padx=5, pady=5)
        va_casenum_entry = ttk.Entry(vas_frame) 
        va_casenum_entry.grid(row=0, column=1, padx=5, pady=5)
        if vaCaseNumber is not None:
            va_casenum_entry.delete(0)
            va_casenum_entry.insert(0, vaCaseNumber)

        agencies, aReverse = get_all_agencies()

        ttk.Label(vas_frame, text="Agency").grid(row=1, column=0, padx=5, pady=5)
        agency_entry = ttk.Combobox(vas_frame, values=list(agencies.values())) 
        agency_entry.grid(row=1, column=1, padx=5, pady=5)
        if agencies.get(vaAgencyId) is not None:
            agency_entry.set(agencies[vaAgencyId])

        ttk.Button(vas_frame, text="Add Agency", command=add_agency_popup).grid(row=1, column=2, padx=5, pady=5)

        persons, pReverse = get_all_personnel()

        ttk.Label(vas_frame, text="Person").grid(row=2, column=0, padx=5, pady=5)
        person_entry = ttk.Combobox(vas_frame, values=list(persons.values())) 
        person_entry.grid(row=2, column=1, padx=5, pady=5) 
        if persons.get(leadEmployeeId) is not None:
            person_entry.set(persons[leadEmployeeId])

        ttk.Button(vas_frame, text="Add Person", command=add_personnel_popup).grid(row=2, column=2, padx=5, pady=5)

        ttk.Label(vas_frame, text="Date Services first offered to child/family").grid(row=3, column=0, padx=5, pady=5)
        date_services_offered = DateEntry(vas_frame)  
        date_services_offered.grid(row=3, column=1, padx=5, pady=5)
        if servicesOfferedDate is not None:
            date_services_offered.set_date(servicesOfferedDate)

        services_accept = tk.BooleanVar(value=False)
        ttk.Label(vas_frame, text="Did the child/family accept VA services?").grid(row=4, column=0, padx=5, pady=5)
        services_accepted = ttk.Checkbutton(vas_frame, text="Yes", variable=services_accept)  
        services_accepted.grid(row=4, column=1, padx=5, pady=5, sticky="w")
        if servicesAccepted is not None:
            services_accept.set(servicesAccepted)

        ttk.Label(vas_frame, text="Hope: (1)").grid(row=5, column=0, padx=5, pady=5)
        hope_entry = ttk.Combobox(vas_frame, values=["VA PL 1 - Service One", "VA PL 1 - Service Two", "VA PL 1 - Service Three"])  
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

        tk.Label(vas_frame, text="VA Services Custom Field Chp (6)").grid(row=10, column=0, padx=5, pady=5)
        custom_field6 = ttk.Combobox(vas_frame, values=["VOCA", "Yes", "No"])  
        custom_field6.grid(row=10, column=1, padx=5, pady=5)

        tk.Label(vas_frame, text="VA Services Custom Field Chp (7)").grid(row=11, column=0, padx=5, pady=5)
        custom_field7 = ttk.Combobox(vas_frame, values=["Yes", "No", "FBI"])  
        custom_field7.grid(row=11, column=1, padx=5, pady=5)

        tk.Label(vas_frame, text="Date Services were concluded").grid(row=12, column=0, padx=5, pady=5)
        services_conclusion = DateEntry(vas_frame)  
        services_conclusion.grid(row=12, column=1, padx=5, pady=5)
        if servicesEndDate is not None:
            services_conclusion.set_date(servicesEndDate)

        mdt = tk.BooleanVar(value=False)
        ttk.Label(vas_frame, text="Ready for MDT Review").grid(row=13, column=0, padx=5, pady=5)
        mdt_ready = ttk.Checkbutton(vas_frame, text="Yes", variable=mdt)  
        mdt_ready.grid(row=13, column=1, padx=5, pady=5, sticky="w")
        if mdtReady is not None:
            mdt.set(mdtReady)

        #------------------------------

        # VAS Log Information
        def insert_new_session(date, start, end, status, attendees, atReverse, vaProvider, services, servicesId):
            sqlQuery1 = """insert into case_va_session_log(cac_id, case_id, case_va_session_id, start_time, end_time, va_provider_agency_id, session_date, session_status)
                    VALUES(%s, %s, %s, %s, %s, %s, %s, %s);"""
            sqlQuery2 = """insert into case_va_session_attendee(case_id, case_va_session_attendee_id, case_va_session_id, person_id)
                    VALUES(%s, %s, %s, %s);"""
            sqlQuery3 = """insert into case_va_session_service(cac_id, case_va_session_id, case_va_session_service_id, service_type_id)
                    VALUES(%s, %s, %s, %s);"""
            newSessionId = random.randint(1, 999999999)
            try:
                config = load_config()
                with psycopg2.connect(**config) as conn:
                    with conn.cursor() as cur:
                        cur.execute(sqlQuery1, (cacId, caseId, newSessionId, start, end, vaProvider, date, status))
                        for name, check in attendees.items():
                            if check.get():
                                newAttendeeId = random.randint(1, 999999999)
                                personId = atReverse[name]
                                cur.execute(sqlQuery2, (caseId, newAttendeeId, newSessionId, personId))
                        for name, check in services.items():
                            if check.get():
                                newServiceId = random.randint(1, 999999999)
                                cur.execute(sqlQuery3, (cacId, newSessionId, newServiceId, servicesId[name]))
                        conn.commit
                        messagebox.showinfo("Save", "Session has been saved successfully!")
            except (psycopg2.DatabaseError, Exception) as error:
                print(f"{error}")
                exit()

        def update_session(date, start, end, status, attendees, atReverse, vaProvider, services, servicesId, sessionId):
            sqlQuery1 = """update case_va_session_log set start_time = %s, end_time = %s, va_provider_agency_id = %s, session_date = %s, session_status = %s
                    where case_va_session_id = %s;"""
            sqlQuery2 = """delete from case_va_session_attendee where case_va_session_id = %s;
                    insert into case_va_session_attendee(case_id, case_va_session_attendee_id, case_va_session_id, person_id)
                    VALUES(%s, %s, %s, %s);"""
            sqlQuery3 = """delete from case_va_session_service where case_va_session_id = %s;
                    insert into case_va_session_service(cac_id, case_va_session_id, case_va_session_service_id, service_type_id)
                    VALUES(%s, %s, %s, %s);"""
            try:
                config = load_config()
                with psycopg2.connect(**config) as conn:
                    with conn.cursor() as cur:
                        cur.execute(sqlQuery1, (start, end, vaProvider, date, status, sessionId))
                        for name, check in attendees.items():
                            if check.get():
                                newAttendeeId = random.randint(1, 999999999)
                                personId = atReverse[name]
                                cur.execute(sqlQuery2, (sessionId, caseId, newAttendeeId, sessionId, personId))
                        for name, check in services.items():
                            if check.get():
                                newServiceId = random.randint(1, 999999999)
                                serviceType = servicesId[name]
                                cur.execute(sqlQuery3, (sessionId, cacId, sessionId, newServiceId, serviceType))
                        conn.commit
                        messagebox.showinfo("Save", "Session has been updated successfully!")
            except (psycopg2.DatabaseError, Exception) as error:
                print(f"{error}")
                exit()

        def delete_session(sessionId):
            response = messagebox.askyesno(
                title="Confirm Deletion",
                message=f"Are you sure you want to delete the session with ID {sessionId}?"
            )

            if response:
                sqlQuery1 = """delete from case_va_session_log where case_va_session_id = %s;"""
                sqlQuery2 = """delete from case_va_session_attendee where case_va_session_id = %s;"""
                sqlQuery3 = """delete from case_va_session_service where case_va_session_id = %s;"""
                try:
                    config = load_config()
                    with psycopg2.connect(**config) as conn:
                        with conn.cursor() as cur:
                            cur.execute(sqlQuery3, (sessionId,))
                            cur.execute(sqlQuery2, (sessionId,))
                            cur.execute(sqlQuery1, (sessionId,))
                            conn.commit
                            messagebox.showinfo("Save", "Session has been deleted successfully!")
                except (psycopg2.DatabaseError, Exception) as error:
                    print(f"{error}")
                    exit()

        def get_persons():
            sqlQuery = """select person_id, first_name, last_name from person order by last_name desc;"""
            try:
                config = load_config()
                with psycopg2.connect(**config) as conn:
                    with conn.cursor() as cur:
                        cur.execute(sqlQuery)
                        persons = cur.fetchall()
                        pMap = {person[0]: person[1] + " " + person[2] for person in persons}
                        pMapReverse =  {person[1] + " " + person[2]: person[0] for person in persons}
                        return pMap, pMapReverse
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
            popup.geometry("800x950")

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

            sessionStatuses = {
                1: "Cancelled",
                2: "To Be Scheduled",
                3: "Scheduled",
                4: "Attended",
                5: "No Show",
                6: "Cancelled & Rescheduled",
                7: "Client Cancelled",
                8: "Clinician Rescheduled",
                9: "Declined"
            }
            sessionReverse = {
                "Cancelled": 1,
                "To Be Scheduled": 2,
                "Scheduled": 3,
                "Attended": 4,
                "No Show": 5,
                "Cancelled & Rescheduled": 6,
                "Client Cancelled": 7,
                "Clinician Rescheduled": 8,
                "Declined": 9
            }

            ttk.Label(field_frame, text="Session Status *").grid(row=rowCounter, column=0, padx=5, pady=5)
            session_status_entry = ttk.Combobox(field_frame, values=list(sessionStatuses.values()))
            session_status_entry.grid(row=rowCounter, column=1, padx=5, pady=5)
            rowCounter += 1

            ttk.Label(field_frame, text="Funding Source").grid(row=rowCounter, column=0, padx=5, pady=5)
            funding_source_entry = ttk.Combobox(field_frame, values=["Source 1", "Source 2", ])
            funding_source_entry.grid(row=rowCounter, column=1, padx=5, pady=5)
            rowCounter += 1

            ttk.Label(field_frame, text="Location").grid(row=rowCounter, column=0, padx=5, pady=5)
            location_entry = ttk.Combobox(field_frame, values=["Location 1", "Location 2", "Location 3"])
            location_entry.grid(row=rowCounter, column=1, padx=5, pady=5)
            rowCounter += 1

            providers, providerReverse = get_all_agencies()

            ttk.Label(field_frame, text="Provider Agency *").grid(row=rowCounter, column=0, padx=5, pady=5)
            provider_agency_entry = ttk.Combobox(field_frame, values=list(providers.values()))
            provider_agency_entry.grid(row=rowCounter, column=1, padx=5, pady=5)
            rowCounter += 1

            employees, eReverse = get_all_personnel()

            ttk.Label(field_frame, text="Provider Employee").grid(row=rowCounter, column=0, padx=5, pady=5)
            provider_employee_entry = ttk.Combobox(field_frame, values=list(employees.values()))
            provider_employee_entry.grid(row=rowCounter, column=1, padx=5, pady=5)
            rowCounter += 1

            ttk.Label(field_frame, text="Attendees *").grid(row=rowCounter, column=0, padx=5, pady=5)
            rowCounter += 1

            attendees, atReverse = get_persons()

            attendee1Check = tk.BooleanVar(value=False)
            attendee2Check = tk.BooleanVar(value=False)
            attendee3Check = tk.BooleanVar(value=False)
            attendee4Check = tk.BooleanVar(value=False)
            attendee1 = ttk.Checkbutton(field_frame, text=list(attendees.values())[0], variable=attendee1Check).grid(row=rowCounter, column=1, sticky="w")
            attendee2 = ttk.Checkbutton(field_frame, text=list(attendees.values())[1], variable=attendee2Check).grid(row=rowCounter, column=2, sticky="w")
            rowCounter += 1
            attendee3 = ttk.Checkbutton(field_frame, text=list(attendees.values())[2], variable=attendee3Check).grid(row=rowCounter, column=1, sticky="w")
            attendee4 = ttk.Checkbutton(field_frame, text=list(attendees.values())[3], variable=attendee4Check).grid(row=rowCounter, column=2, sticky="w")
            rowCounter += 1

            attendees = {
                list(attendees.values())[0]: attendee1Check, 
                list(attendees.values())[1]: attendee2Check, 
                list(attendees.values())[2]: attendee3Check, 
                list(attendees.values())[3]: attendee4Check
            }

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

            service1 = ttk.Checkbutton(field_frame, text="Legal Services", variable=service1Check)
            service1.grid(row=rowCounter, column=1, sticky="w")
            service2 = ttk.Checkbutton(field_frame, text="Transportation", variable=service2Check)
            service2.grid(row=rowCounter, column=2, sticky="w")
            rowCounter += 1

            service3 = ttk.Checkbutton(field_frame, text="Victim Support", variable=service3Check)
            service3.grid(row=rowCounter, column=1, sticky="w")
            service4 = ttk.Checkbutton(field_frame, text="1-2 Week Follow-up Call", variable=service4Check)
            service4.grid(row=rowCounter, column=2, sticky="w")
            rowCounter += 1

            service5 = ttk.Checkbutton(field_frame, text="2. Personal Court Education", variable=service5Check)
            service5.grid(row=rowCounter, column=1, sticky="w")
            service6 = ttk.Checkbutton(field_frame, text="24 -- hour crisis line cal", variable=service6Check)
            service6.grid(row=rowCounter, column=2, sticky="w")
            rowCounter += 1

            service7 = ttk.Checkbutton(field_frame, text="3a. Info & Support - MDT response", variable=service7Check)
            service7.grid(row=rowCounter, column=1, sticky="w")
            service8 = ttk.Checkbutton(field_frame, text="3b. Information & Support - Court", variable=service8Check)
            service8.grid(row=rowCounter, column=2, sticky="w")
            rowCounter += 1

            service9 = ttk.Checkbutton(field_frame, text="3bi Personal advocacy", variable=service9Check)
            service9.grid(row=rowCounter, column=1, sticky="w")
            service10 = ttk.Checkbutton(field_frame, text="6--8 Week Follow-up Call", variable=service10Check)
            service10.grid(row=rowCounter, column=2, sticky="w")
            rowCounter += 1

            service11 = ttk.Checkbutton(field_frame, text="B2. Victim Advocacy/Accompaniment to Medical Forensic Exam", variable=service11Check)
            service11.grid(row=rowCounter, column=1, sticky="w")
            service12 = ttk.Checkbutton(field_frame, text="Collected Survey", variable=service12Check)
            service12.grid(row=rowCounter, column=2, sticky="w")
            rowCounter += 1

            service13 = ttk.Checkbutton(field_frame, text="Criminal Justice support/advocacy", variable=service13Check)
            service13.grid(row=rowCounter, column=1, sticky="w")
            service14 = ttk.Checkbutton(field_frame, text="Compensation Claim Filing", variable=service14Check)
            service14.grid(row=rowCounter, column=2, sticky="w")
            rowCounter += 1

            service15 = ttk.Checkbutton(field_frame, text="Emergency Crisis Intervention", variable=service15Check)
            service15.grid(row=rowCounter, column=1, sticky="w")
            service16 = ttk.Checkbutton(field_frame, text="Crisis Counseling", variable=service16Check)
            service16.grid(row=rowCounter, column=2, sticky="w")
            rowCounter += 1

            service17 = ttk.Checkbutton(field_frame, text="Gave Educational Information", variable=service17Check)
            service17.grid(row=rowCounter, column=1, sticky="w")
            service18 = ttk.Checkbutton(field_frame, text="Follow-up", variable=service18Check)
            service18.grid(row=rowCounter, column=2, sticky="w")
            rowCounter += 1

            service19 = ttk.Checkbutton(field_frame, text="Homeless support group", variable=service19Check)
            service19.grid(row=rowCounter, column=1, sticky="w")
            service20 = ttk.Checkbutton(field_frame, text="Initial Meeting with Caregiver", variable=service20Check)
            service20.grid(row=rowCounter, column=2, sticky="w")
            rowCounter += 1

            service21 = ttk.Checkbutton(field_frame, text="Initial Telephone Call", variable=service21Check)
            service21.grid(row=rowCounter, column=1, sticky="w")
            service22 = ttk.Checkbutton(field_frame, text="Mailed Brochure", variable=service22Check)
            service22.grid(row=rowCounter, column=2, sticky="w")
            rowCounter += 1

            service23 = ttk.Checkbutton(field_frame, text="Orientation to Center for FI", variable=service23Check)
            service23.grid(row=rowCounter, column=1, sticky="w")
            service24 = ttk.Checkbutton(field_frame, text="Post Interview Crisis Counseling", variable=service24Check)
            service24.grid(row=rowCounter, column=2, sticky="w")
            rowCounter += 1

            service25 = ttk.Checkbutton(field_frame, text="Pre-Interview Family Call", variable=service25Check)
            service25.grid(row=rowCounter, column=1, sticky="w")
            service26 = ttk.Checkbutton(field_frame, text="Shelter/safehouse Referral", variable=service26Check)
            service26.grid(row=rowCounter, column=2, sticky="w")
            rowCounter += 1

            service27 = ttk.Checkbutton(field_frame, text="Survey Distributed", variable=service27Check)
            service27.grid(row=rowCounter, column=1, sticky="w")
            service28 = ttk.Checkbutton(field_frame, text="Survey Recieved", variable=service28Check)
            service28.grid(row=rowCounter, column=2, sticky="w")
            rowCounter += 1

            service29 = ttk.Checkbutton(field_frame, text="Telephone Follow-up", variable=service29Check)
            service29.grid(row=rowCounter, column=1, sticky="w")
            service30 = ttk.Checkbutton(field_frame, text="Unscheduled Call", variable=service30Check)
            service30.grid(row=rowCounter, column=2, sticky="w")
            rowCounter += 1

            services = {
                service1.cget("text"): service1Check,
                service2.cget("text"): service2Check,
                service3.cget("text"): service3Check,
                service4.cget("text"): service4Check,
                service5.cget("text"): service5Check,
                service6.cget("text"): service6Check,
                service7.cget("text"): service7Check,
                service8.cget("text"): service8Check,
                service9.cget("text"): service9Check,
                service10.cget("text"): service10Check,
                service11.cget("text"): service11Check,
                service12.cget("text"): service12Check,
                service13.cget("text"): service13Check,
                service14.cget("text"): service14Check,
                service15.cget("text"): service15Check,
                service16.cget("text"): service16Check,
                service17.cget("text"): service17Check,
                service18.cget("text"): service18Check,
                service19.cget("text"): service19Check,
                service20.cget("text"): service20Check,
                service21.cget("text"): service21Check,
                service22.cget("text"): service22Check,
                service23.cget("text"): service23Check,
                service24.cget("text"): service24Check,
                service25.cget("text"): service25Check,
                service26.cget("text"): service26Check,
                service27.cget("text"): service27Check,
                service28.cget("text"): service28Check,
                service29.cget("text"): service29Check,
                service30.cget("text"): service30Check
            }

            servicesId = {
                service1.cget("text"): 1,
                service2.cget("text"): 2,
                service3.cget("text"): 3,
                service4.cget("text"): 4,
                service5.cget("text"): 5,
                service6.cget("text"): 6,
                service7.cget("text"): 7,
                service8.cget("text"): 8,
                service9.cget("text"): 9,
                service10.cget("text"): 10,
                service11.cget("text"): 11,
                service12.cget("text"): 12,
                service13.cget("text"): 13,
                service14.cget("text"): 14,
                service15.cget("text"): 15,
                service16.cget("text"): 16,
                service17.cget("text"): 17,
                service18.cget("text"): 18,
                service19.cget("text"): 19,
                service20.cget("text"): 20,
                service21.cget("text"): 21,
                service22.cget("text"): 22,
                service23.cget("text"): 23,
                service24.cget("text"): 24,
                service25.cget("text"): 25,
                service26.cget("text"): 26,
                service27.cget("text"): 27,
                service28.cget("text"): 28,
                service29.cget("text"): 29,
                service30.cget("text"): 30
            }

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
                                                                               (str(session_date_entry.get_date()) + " " + end_start_entry.get()), sessionReverse[session_status_entry.get()], attendees, atReverse, providerReverse[provider_agency_entry.get()], services, servicesId), popup.destroy()]).grid(row=0, column=0, padx=5, pady=5)
            ttk.Button(button_frame, text="Cancel", command=lambda: [popup.destroy()]).grid(row=0, column=1, padx=5, pady=5)

        def get_all_sessions(caseid):
            try:
                config = load_config()
                with psycopg2.connect(**config) as conn:
                    with conn.cursor() as cur:
                        cur.execute("""
                            SELECT case_va_session_id, session_date, start_time, end_time, session_status
                            FROM case_va_session_log
                            WHERE case_id = %s
                            ORDER BY session_date DESC;
                        """, (caseid,))
                        sessions = cur.fetchall()
                        return sessions
            except (psycopg2.DatabaseError, Exception) as error:
                print(f"{error}")
                exit()

        def get_session(id):
            try:
                config = load_config()
                with psycopg2.connect(**config) as conn:
                    with conn.cursor() as cur:
                        cur.execute("""select * from case_va_session_log
                                    where case_va_session_id = %s;""", (id,))
                        session = cur.fetchone()
                        return session
            except (psycopg2.DatabaseError, Exception) as error:
                print(f"{error}")
                exit()

        def get_attendees(id):
            try:
                config = load_config()
                with psycopg2.connect(**config) as conn:
                    with conn.cursor() as cur:
                        cur.execute("""select * from case_va_session_attendee
                                    where case_va_session_id = %s;""", (id,))
                        attendees = cur.fetchall()
                        return attendees
            except (psycopg2.DatabaseError, Exception) as error:
                print(f"{error}")
                exit()

        def get_services(id):
            try:
                config = load_config()
                with psycopg2.connect(**config) as conn:
                    with conn.cursor() as cur:
                        cur.execute("""select * from case_va_session_service
                                    where case_va_session_id = %s order by service_type_id desc;""", (id,))
                        services = cur.fetchall()
                        return services
            except (psycopg2.DatabaseError, Exception) as error:
                print(f"{error}")
                exit()

        vas_log_frame = tk.LabelFrame(scrollable_frame, text="Victim Advocacy Services Log", padx=10, pady=10)
        vas_log_frame.grid(row=4, column=0, sticky='w', padx=10, pady=5)

        sessions = get_all_sessions(caseId)

        ttk.Button(vas_log_frame, text="Add New Session Log", command=add_new_session_popup).grid(row=0, column=0, padx=5, pady=5)
    
        rowCounter = 2

        ttk.Label(vas_log_frame, text="Actions").grid(row=1, column=0, padx=5, pady=5)
        ttk.Label(vas_log_frame, text="Date").grid(row=1, column=2, padx=5, pady=5)
        ttk.Label(vas_log_frame, text="Start Time").grid(row=1, column=3, padx=5, pady=5)
        ttk.Label(vas_log_frame, text="End Time").grid(row=1, column=4, padx=5, pady=5)
        ttk.Label(vas_log_frame, text="Status").grid(row=1, column=5, padx=5, pady=5)

        sessionStatuses = {
                1: "Attended",
                2: "Cancelled",
                3: "No Show",
                4: "Canceled and rescheduled",
                5: "To be scheduled",
                6: "Scheduled"
            }

        for session in sessions:
            start_time = str(session[2]).split(' ')[1]
            end_time = str(session[3]).split(' ')[1]

            ttk.Button(vas_log_frame, text="Edit", command=lambda: edit_session(session[0])).grid(row=rowCounter, column=0, padx=5, pady=5)
            ttk.Button(vas_log_frame, text="Delete", command=lambda: delete_session(session[0])).grid(row=rowCounter, column=1, padx=5, pady=5)
            ttk.Label(vas_log_frame, text=session[1]).grid(row=rowCounter, column=2, padx=5, pady=5)
            ttk.Label(vas_log_frame, text=start_time).grid(row=rowCounter, column=3, padx=5, pady=5)
            ttk.Label(vas_log_frame, text=end_time).grid(row=rowCounter, column=4, padx=5, pady=5)
            ttk.Label(vas_log_frame, text=sessionStatuses[session[4]]).grid(row=rowCounter, column=5, padx=5, pady=5)
            rowCounter += 1

        def edit_session(sessionId):
            popup = tk.Toplevel(self)
            popup.title("Edit Session")
            popup.geometry("800x950")

            popup.grid_columnconfigure(0, weight=1)  
            popup.grid_columnconfigure(1, weight=1) 

            session = get_session(sessionId)
            newAttendees = get_attendees(sessionId)
            services = get_services(sessionId)

            rowCounter = 0

            ttk.Label(popup, text="Fields marked with a (*) are required", foreground='red').grid(row=0, column=0, padx=5, pady=5, sticky='w')
            
            field_frame = ttk.Frame(popup)
            field_frame.grid(row=1, column=0, padx=5, pady=5, sticky='w')

            # Entry fields for case details
            ttk.Label(field_frame, text="Session Date *").grid(row=rowCounter, column=0, padx=5, pady=5)
            session_date_entry = DateEntry(field_frame, background='darkblue', foreground='white', borderwidth=2)
            session_date_entry.grid(row=rowCounter, column=1, padx=5, pady=5)
            if session[6] is not None:
                session_date_entry.set_date(session[6])
            rowCounter += 1

            times = generate_timestamps(str(session_date_entry.get_date()), 30)

            formattedTimes = []

            for time in times:
                formattedTimes.append(time.split(" ")[1])

            ttk.Label(field_frame, text="Start Time *").grid(row=rowCounter, column=0, padx=5, pady=5)
            start_time_entry = ttk.Combobox(field_frame, values=formattedTimes)
            start_time_entry.grid(row=rowCounter, column=1, padx=5, pady=5)
            if session[3] is not None:
                start_time_entry.set(str(session[3]).split(" ")[1])
            rowCounter += 1

            ttk.Label(field_frame, text="End Time *").grid(row=rowCounter, column=0, padx=5, pady=5)
            end_start_entry = ttk.Combobox(field_frame, values=formattedTimes) 
            end_start_entry.grid(row=rowCounter, column=1, padx=5, pady=5)
            if session[4] is not None:
                end_start_entry.set(str(session[4]).split(" ")[1])
            rowCounter += 1

            ttk.Label(field_frame, text="Prep").grid(row=rowCounter, column=0, padx=5, pady=5)
            prep_entry = ttk.Combobox(field_frame)
            prep_entry.grid(row=rowCounter, column=1, padx=5, pady=5)
            rowCounter += 1

            sessionStatuses = {
                1: "Cancelled",
                2: "To Be Scheduled",
                3: "Scheduled",
                4: "Attended",
                5: "No Show",
                6: "Cancelled & Rescheduled",
                7: "Client Cancelled",
                8: "Clinician Rescheduled",
                9: "Declined"
            }
            sessionReverse = {
                "Cancelled": 1,
                "To Be Scheduled": 2,
                "Scheduled": 3,
                "Attended": 4,
                "No Show": 5,
                "Cancelled & Rescheduled": 6,
                "Client Cancelled": 7,
                "Clinician Rescheduled": 8,
                "Declined": 9
            }

            ttk.Label(field_frame, text="Session Status *").grid(row=rowCounter, column=0, padx=5, pady=5)
            session_status_entry = ttk.Combobox(field_frame, values=list(sessionStatuses.values()))
            session_status_entry.grid(row=rowCounter, column=1, padx=5, pady=5)
            if session[7] is not None:
                session_status_entry.set(sessionStatuses[session[7]])
            rowCounter += 1

            ttk.Label(field_frame, text="Funding Source").grid(row=rowCounter, column=0, padx=5, pady=5)
            funding_source_entry = ttk.Combobox(field_frame, values=["Source 1", "Source 2", ])
            funding_source_entry.grid(row=rowCounter, column=1, padx=5, pady=5)
            rowCounter += 1

            ttk.Label(field_frame, text="Location").grid(row=rowCounter, column=0, padx=5, pady=5)
            location_entry = ttk.Combobox(field_frame, values=["Location 1", "Location 2", "Location 3"])
            location_entry.grid(row=rowCounter, column=1, padx=5, pady=5)
            rowCounter += 1

            providers, providerReverse = get_all_agencies()

            ttk.Label(field_frame, text="Provider Agency *").grid(row=rowCounter, column=0, padx=5, pady=5)
            provider_agency_entry = ttk.Combobox(field_frame, values=list(providers.values()))
            provider_agency_entry.grid(row=rowCounter, column=1, padx=5, pady=5)
            if session[5] is not None:
                provider_agency_entry.set(providers[session[5]])
            rowCounter += 1

            employees, eReverse = get_all_personnel()

            ttk.Label(field_frame, text="Provider Employee").grid(row=rowCounter, column=0, padx=5, pady=5)
            provider_employee_entry = ttk.Combobox(field_frame, values=list(employees.values()))
            provider_employee_entry.grid(row=rowCounter, column=1, padx=5, pady=5)
            rowCounter += 1

            ttk.Label(field_frame, text="Attendees *").grid(row=rowCounter, column=0, padx=5, pady=5)
            rowCounter += 1

            attendees, atReverse = get_persons()

            attendee1Check = tk.BooleanVar(value=False)
            attendee2Check = tk.BooleanVar(value=False)
            attendee3Check = tk.BooleanVar(value=False)
            attendee4Check = tk.BooleanVar(value=False)

            checks = {
                list(attendees.keys())[0]: attendee1Check,
                list(attendees.keys())[1]: attendee2Check,
                list(attendees.keys())[2]: attendee3Check,
                list(attendees.keys())[3]: attendee4Check
            }

            for a in newAttendees:
                if a[3] in checks:
                    checks[a[3]].set(True)


            attendee1 = ttk.Checkbutton(field_frame, text=list(attendees.values())[0], variable=attendee1Check).grid(row=rowCounter, column=1, sticky="w")
            attendee2 = ttk.Checkbutton(field_frame, text=list(attendees.values())[1], variable=attendee2Check).grid(row=rowCounter, column=2, sticky="w")
            rowCounter += 1
            attendee3 = ttk.Checkbutton(field_frame, text=list(attendees.values())[2], variable=attendee3Check).grid(row=rowCounter, column=1, sticky="w")
            attendee4 = ttk.Checkbutton(field_frame, text=list(attendees.values())[3], variable=attendee4Check).grid(row=rowCounter, column=2, sticky="w")
            rowCounter += 1

            attendeesValues = {
                list(attendees.values())[0]: attendee1Check,
                list(attendees.values())[1]: attendee2Check,
                list(attendees.values())[2]: attendee3Check,
                list(attendees.values())[3]: attendee4Check
            }

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

            servicesCheck = {
                1: service1Check,
                2: service2Check,
                3: service3Check,
                4: service4Check,
                5: service5Check,
                6: service6Check,
                7: service7Check,
                8: service8Check,
                9: service9Check,
                10: service10Check,
                11: service11Check,
                12: service12Check,
                13: service13Check,
                14: service14Check,
                15: service15Check,
                16: service16Check,
                17: service17Check,
                18: service18Check,
                19: service19Check,
                20: service20Check,
                21: service21Check,
                22: service22Check,
                23: service23Check,
                24: service24Check,
                25: service25Check,
                26: service26Check,
                27: service27Check,
                28: service28Check,
                29: service29Check,
                30: service30Check
            }

            for s in services:
                if s[3] in servicesCheck:
                    servicesCheck[s[3]].set(True)

            service1 = ttk.Checkbutton(field_frame, text="Legal Services", variable=service1Check)
            service1.grid(row=rowCounter, column=1, sticky="w")
            service2 = ttk.Checkbutton(field_frame, text="Transportation", variable=service2Check)
            service2.grid(row=rowCounter, column=2, sticky="w")
            rowCounter += 1

            service3 = ttk.Checkbutton(field_frame, text="Victim Support", variable=service3Check)
            service3.grid(row=rowCounter, column=1, sticky="w")
            service4 = ttk.Checkbutton(field_frame, text="1-2 Week Follow-up Call", variable=service4Check)
            service4.grid(row=rowCounter, column=2, sticky="w")
            rowCounter += 1

            service5 = ttk.Checkbutton(field_frame, text="2. Personal Court Education", variable=service5Check)
            service5.grid(row=rowCounter, column=1, sticky="w")
            service6 = ttk.Checkbutton(field_frame, text="24 -- hour crisis line cal", variable=service6Check)
            service6.grid(row=rowCounter, column=2, sticky="w")
            rowCounter += 1

            service7 = ttk.Checkbutton(field_frame, text="3a. Info & Support - MDT response", variable=service7Check)
            service7.grid(row=rowCounter, column=1, sticky="w")
            service8 = ttk.Checkbutton(field_frame, text="3b. Information & Support - Court", variable=service8Check)
            service8.grid(row=rowCounter, column=2, sticky="w")
            rowCounter += 1

            service9 = ttk.Checkbutton(field_frame, text="3bi Personal advocacy", variable=service9Check)
            service9.grid(row=rowCounter, column=1, sticky="w")
            service10 = ttk.Checkbutton(field_frame, text="6--8 Week Follow-up Call", variable=service10Check)
            service10.grid(row=rowCounter, column=2, sticky="w")
            rowCounter += 1

            service11 = ttk.Checkbutton(field_frame, text="B2. Victim Advocacy/Accompaniment to Medical Forensic Exam", variable=service11Check)
            service11.grid(row=rowCounter, column=1, sticky="w")
            service12 = ttk.Checkbutton(field_frame, text="Collected Survey", variable=service12Check)
            service12.grid(row=rowCounter, column=2, sticky="w")
            rowCounter += 1

            service13 = ttk.Checkbutton(field_frame, text="Criminal Justice support/advocacy", variable=service13Check)
            service13.grid(row=rowCounter, column=1, sticky="w")
            service14 = ttk.Checkbutton(field_frame, text="Compensation Claim Filing", variable=service14Check)
            service14.grid(row=rowCounter, column=2, sticky="w")
            rowCounter += 1

            service15 = ttk.Checkbutton(field_frame, text="Emergency Crisis Intervention", variable=service15Check)
            service15.grid(row=rowCounter, column=1, sticky="w")
            service16 = ttk.Checkbutton(field_frame, text="Crisis Counseling", variable=service16Check)
            service16.grid(row=rowCounter, column=2, sticky="w")
            rowCounter += 1

            service17 = ttk.Checkbutton(field_frame, text="Gave Educational Information", variable=service17Check)
            service17.grid(row=rowCounter, column=1, sticky="w")
            service18 = ttk.Checkbutton(field_frame, text="Follow-up", variable=service18Check)
            service18.grid(row=rowCounter, column=2, sticky="w")
            rowCounter += 1

            service19 = ttk.Checkbutton(field_frame, text="Homeless support group", variable=service19Check)
            service19.grid(row=rowCounter, column=1, sticky="w")
            service20 = ttk.Checkbutton(field_frame, text="Initial Meeting with Caregiver", variable=service20Check)
            service20.grid(row=rowCounter, column=2, sticky="w")
            rowCounter += 1

            service21 = ttk.Checkbutton(field_frame, text="Initial Telephone Call", variable=service21Check)
            service21.grid(row=rowCounter, column=1, sticky="w")
            service22 = ttk.Checkbutton(field_frame, text="Mailed Brochure", variable=service22Check)
            service22.grid(row=rowCounter, column=2, sticky="w")
            rowCounter += 1

            service23 = ttk.Checkbutton(field_frame, text="Orientation to Center for FI", variable=service23Check)
            service23.grid(row=rowCounter, column=1, sticky="w")
            service24 = ttk.Checkbutton(field_frame, text="Post Interview Crisis Counseling", variable=service24Check)
            service24.grid(row=rowCounter, column=2, sticky="w")
            rowCounter += 1

            service25 = ttk.Checkbutton(field_frame, text="Pre-Interview Family Call", variable=service25Check)
            service25.grid(row=rowCounter, column=1, sticky="w")
            service26 = ttk.Checkbutton(field_frame, text="Shelter/safehouse Referral", variable=service26Check)
            service26.grid(row=rowCounter, column=2, sticky="w")
            rowCounter += 1

            service27 = ttk.Checkbutton(field_frame, text="Survey Distributed", variable=service27Check)
            service27.grid(row=rowCounter, column=1, sticky="w")
            service28 = ttk.Checkbutton(field_frame, text="Survey Recieved", variable=service28Check)
            service28.grid(row=rowCounter, column=2, sticky="w")
            rowCounter += 1

            service29 = ttk.Checkbutton(field_frame, text="Telephone Follow-up", variable=service29Check)
            service29.grid(row=rowCounter, column=1, sticky="w")
            service30 = ttk.Checkbutton(field_frame, text="Unscheduled Call", variable=service30Check)
            service30.grid(row=rowCounter, column=2, sticky="w")
            rowCounter += 1

            services = {
                service1.cget("text"): service1Check,
                service2.cget("text"): service2Check,
                service3.cget("text"): service3Check,
                service4.cget("text"): service4Check,
                service5.cget("text"): service5Check,
                service6.cget("text"): service6Check,
                service7.cget("text"): service7Check,
                service8.cget("text"): service8Check,
                service9.cget("text"): service9Check,
                service10.cget("text"): service10Check,
                service11.cget("text"): service11Check,
                service12.cget("text"): service12Check,
                service13.cget("text"): service13Check,
                service14.cget("text"): service14Check,
                service15.cget("text"): service15Check,
                service16.cget("text"): service16Check,
                service17.cget("text"): service17Check,
                service18.cget("text"): service18Check,
                service19.cget("text"): service19Check,
                service20.cget("text"): service20Check,
                service21.cget("text"): service21Check,
                service22.cget("text"): service22Check,
                service23.cget("text"): service23Check,
                service24.cget("text"): service24Check,
                service25.cget("text"): service25Check,
                service26.cget("text"): service26Check,
                service27.cget("text"): service27Check,
                service28.cget("text"): service28Check,
                service29.cget("text"): service29Check,
                service30.cget("text"): service30Check
            }

            servicesId = {
                service1.cget("text"): 1,
                service2.cget("text"): 2,
                service3.cget("text"): 3,
                service4.cget("text"): 4,
                service5.cget("text"): 5,
                service6.cget("text"): 6,
                service7.cget("text"): 7,
                service8.cget("text"): 8,
                service9.cget("text"): 9,
                service10.cget("text"): 10,
                service11.cget("text"): 11,
                service12.cget("text"): 12,
                service13.cget("text"): 13,
                service14.cget("text"): 14,
                service15.cget("text"): 15,
                service16.cget("text"): 16,
                service17.cget("text"): 17,
                service18.cget("text"): 18,
                service19.cget("text"): 19,
                service20.cget("text"): 20,
                service21.cget("text"): 21,
                service22.cget("text"): 22,
                service23.cget("text"): 23,
                service24.cget("text"): 24,
                service25.cget("text"): 25,
                service26.cget("text"): 26,
                service27.cget("text"): 27,
                service28.cget("text"): 28,
                service29.cget("text"): 29,
                service30.cget("text"): 30
            }

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
            ttk.Button(button_frame, text="Save", command=lambda: [update_session(session_date_entry.get_date(), (str(session_date_entry.get_date()) + " " + start_time_entry.get()), 
                                                                               (str(session_date_entry.get_date()) + " " + end_start_entry.get()), sessionReverse[session_status_entry.get()], attendeesValues, atReverse, providerReverse[provider_agency_entry.get()], services, servicesId, sessionId), popup.destroy()]).grid(row=0, column=0, padx=5, pady=5)
            ttk.Button(button_frame, text="Cancel", command=lambda: [popup.destroy()]).grid(row=0, column=1, padx=5, pady=5)
        #------------------------------

        # Crime Compensation Application Section
        crime_comp_app_frame = tk.LabelFrame(scrollable_frame, text="Crime Compensation Application", padx=10, pady=10)
        crime_comp_app_frame.grid(row=5, column=0, sticky='w', padx=10, pady=5)

        reps, repReverse = get_all_personnel()

        ttk.Label(crime_comp_app_frame, text="State Claim Representative").grid(row=0, column=0, padx=5, pady=5)
        state_claim_rep = ttk.Combobox(crime_comp_app_frame, values=list(reps.values()))  
        state_claim_rep.grid(row=0, column=1, padx=5, pady=5)

        birth_cert = tk.BooleanVar(value=False)
        ttk.Label(crime_comp_app_frame, text="Have Birth Certificate").grid(row=1, column=0, padx=5, pady=5)
        has_birth_cert = ttk.Checkbutton(crime_comp_app_frame, variable=birth_cert)  
        has_birth_cert.grid(row=1, column=1, padx=5, pady=5, sticky="w")
        if hasBirthCert is not None:
            birth_cert.set(hasBirthCert) 

        police_report = tk.BooleanVar(value=False)
        ttk.Label(crime_comp_app_frame, text="Have Police Report").grid(row=2, column=0, padx=5, pady=5)
        has_police_report = ttk.Checkbutton(crime_comp_app_frame, variable=police_report)  
        has_police_report.grid(row=2, column=1, padx=5, pady=5, sticky="w")
        if hasPoliceReport is not None:
            police_report.set(hasPoliceReport) 

        ttk.Label(crime_comp_app_frame, text="Claim Number").grid(row=3, column=0, padx=5, pady=5)
        claim_number = ttk.Entry(crime_comp_app_frame)  
        claim_number.grid(row=3, column=1, padx=5, pady=5)
        if claimNumber is not None:
            claim_number.delete(0)
            claim_number.insert(0, claimNumber)

        ttk.Label(crime_comp_app_frame, text="Date Application Mailed").grid(row=4, column=0, padx=5, pady=5)
        date_app_mailed = DateEntry(crime_comp_app_frame)  
        date_app_mailed.grid(row=4, column=1, padx=5, pady=5)

        statuses = {
            1: "Approved",
            2: "Denied",
            3: "Recieved",
            4: "Submitted"
        }
        sReverse = {
            "Approved": 1,
            "Denied": 2,
            "Recieved": 3,
            "Submitted": 4
        }
        ttk.Label(crime_comp_app_frame, text="Status").grid(row=5, column=0, padx=5, pady=5)
        status_entry = ttk.Combobox(crime_comp_app_frame, values=list(statuses.values()))  
        status_entry.grid(row=5, column=1, padx=5, pady=5)
        if claimStatusId is not None:
            status_entry.set(statuses[claimStatusId])

        ttk.Label(crime_comp_app_frame, text="Application Assistance Provided (1)").grid(row=6, column=0, padx=5, pady=5)
        app_assistance_provided = ttk.Combobox(crime_comp_app_frame, values=["Yes", "No"])  
        app_assistance_provided.grid(row=6, column=1, padx=5, pady=5)

        ttk.Label(crime_comp_app_frame, text="Crime Compensation Application Custom Field (2)").grid(row=7, column=0, padx=5, pady=5)
        cca_customfield2 = ttk.Entry(crime_comp_app_frame)  
        cca_customfield2.grid(row=7, column=1, padx=5, pady=5)

        ttk.Label(crime_comp_app_frame, text="Reason Claim Denied").grid(row=8, column=0, padx=5, pady=5)
        claim_denied_reason = ttk.Entry(crime_comp_app_frame)  
        claim_denied_reason.grid(row=8, column=1, padx=5, pady=5)
        if claimDeniedReason is not None:
            claim_denied_reason.delete(0)
            claim_denied_reason.insert(0, claimDeniedReason)

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
                        messagebox.showinfo("Save", "Instrument has been saved successfully!")
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

        def insert_new_screening(date, personnel, instrument, agency):
            sqlQuery = """insert into case_mh_assessment (cac_id, case_id, assessment_id, 
                                    mh_provider_agency_id, session_date, agency_id, provider_employee_id, 
                                    assessment_instrument_id)
                                    values(%s, %s, %s, %s, %s, %s, %s, %s);"""
            newAssessmentId = random.randint(1, 99999999)
            try:
                config = load_config()
                with psycopg2.connect(**config) as conn:
                    with conn.cursor() as cur:
                        cur.execute(sqlQuery, (cacId, caseId, newAssessmentId, agency, date, agency, personnel, instrument))
                        conn.commit
                        messagebox.showinfo("Save", "Screening has been saved successfully!")
            except (psycopg2.DatabaseError, Exception) as error:
                print(f"{error}")
                exit()
        
        def update_screening(id, date, personnel, instrument, agency):
            sqlQuery = """update case_mh_assessment set mh_provider_agency_id = %s, session_date = %s, agency_id = %s, provider_employee_id = %s,
            assessment_instrument_id = %s
            where assessment_id = %s;"""
            try:
                config = load_config()
                with psycopg2.connect(**config) as conn:
                    with conn.cursor() as cur:
                        cur.execute(sqlQuery, (agency, date, agency, personnel, instrument, id))
                        conn.commit
                        messagebox.showinfo("Save", "Screening has been updated successfully!")
            except (psycopg2.DatabaseError, Exception) as error:
                print(f"{error}")
                exit()

        def delete_screening(id):
            response = messagebox.askyesno(
                title="Confirm Deletion",
                message=f"Are you sure you want to delete the assessment with ID {id}?"
            )

            if response:
                sqlQuery = """delete from case_mh_assessment where assessment_id = %s;"""
                try:
                    config = load_config()
                    with psycopg2.connect(**config) as conn:
                        with conn.cursor() as cur:
                            cur.execute(sqlQuery, (id,))
                            conn.commit
                            messagebox.showinfo("Save", "Screening has been deleted successfully!")
                except (psycopg2.DatabaseError, Exception) as error:
                    print(f"{error}")
                    exit()

        def get_screening(id):
            try:
                config = load_config()
                with psycopg2.connect(**config) as conn:
                    with conn.cursor() as cur:
                        cur.execute("""select case_mh_assessment_instrument.assessment_name, 
                                    case_mh_assessment.session_date, 
                                    employee.first_name,
                                    employee.last_name,
                                    case_mh_assessment.mh_provider_agency_id
                                    from case_mh_assessment
                                    join case_mh_assessment_instrument on case_mh_assessment.assessment_instrument_id = case_mh_assessment_instrument.instrument_id
                                    join employee on case_mh_assessment.provider_employee_id = employee.employee_id
                                    where case_mh_assessment.assessment_id = %s""", (id,))
                        screenings = cur.fetchone()
                        return screenings
            except (psycopg2.DatabaseError, Exception) as error:
                print(f"{error}")
                exit()

        def get_all_instruments():
            sqlQuery = """select * from case_mh_assessment_instrument order by assessment_name;"""
            try:
                config = load_config()
                with psycopg2.connect(**config) as conn:
                    with conn.cursor() as cur:
                        cur.execute(sqlQuery)
                        instruments = cur.fetchall()
                        reverseInstrumentMap = {instrument[1]: instrument[0] for instrument in instruments}
                        instrumentMap = {instrument[0]: instrument[1] for instrument in instruments}
                        return instrumentMap, reverseInstrumentMap
            except (psycopg2.DatabaseError, Exception) as error:
                print(f"{error}")
                exit()   

        def edit_screening(assessmentId):
            popup = tk.Toplevel(self)
            popup.title("Edit Screening")
            popup.geometry("550x350")

            popup.grid_columnconfigure(0, weight=0)  
            popup.grid_columnconfigure(1, weight=1)

            instruments, iReverse = get_all_instruments()
            agencies, aReverse = get_all_agencies()
            personnel, pReverse = get_all_personnel()
            screening = get_screening(assessmentId)
            
            field_frame = ttk.Frame(popup)
            field_frame.grid(row=1, column=0, padx=5, pady=5, sticky='w')

            ttk.Label(popup, text="Fields marked with a (*) are required", foreground='red').grid(row=0, column=0, padx=5, pady=5, sticky='w')

            ttk.Label(field_frame, text="Screening Instrument *", foreground='black').grid(row=0, column=0, padx=5, pady=5, sticky='w')

            screening_instrument_entry = ttk.Combobox(field_frame, values=list(instruments.values()))
            screening_instrument_entry.grid(row=0, column=1, padx=5, pady=5, sticky='w')
            if screening[0] is not None:
                screening_instrument_entry.set(screening[0])

            ttk.Label(field_frame, text="Scores of this Screening's Measures").grid(row=1, column=0, padx=5, pady=5, sticky='w')
            ttk.Label(field_frame).grid(row=1, column=1, padx=5, pady=5, sticky='w')

            ttk.Button(field_frame, text="Add Screening Instrument", command=add_screening_instrument_popup).grid(row=0, column=2, padx=5, pady=5, sticky='w')

            ttk.Label(field_frame, text="Screening Date *", foreground='black').grid(row=2, column=0, padx=5, pady=5, sticky='w')
            screening_date_entry = DateEntry(field_frame, background='darkblue', foreground='white', borderwidth=2)
            screening_date_entry.grid(row=2, column=1, padx=5, pady=5, sticky='w')
            if screening[1] is not None:
                screening_date_entry.set_date(screening[1])

            ttk.Label(field_frame, text="Provider Agency", foreground='black').grid(row=3, column=0, padx=5, pady=5, sticky='w')
            provider_agency_entry = ttk.Combobox(field_frame, values=list(agencies.values()))
            provider_agency_entry.grid(row=3, column=1, padx=5, pady=5, sticky='w')
            if screening[4] is not None:
                provider_agency_entry.set(agencies[screening[4]])

            ttk.Label(field_frame, text="Provider Personnel *", foreground='black').grid(row=4, column=0, padx=5, pady=5, sticky='w')
            provider_personnel_entry = ttk.Combobox(field_frame, values=list(personnel.values())) 
            provider_personnel_entry.grid(row=4, column=1, padx=5, pady=5, sticky='w')
            if screening[2] is not None and screening[3] is not None:
                provider_personnel_entry.set(screening[2] + " " + screening[3])

            ttk.Label(field_frame, text="Functional Impairment").grid(row=5, column=0, padx=5, pady=5, sticky='w')
            functional_impairment_entry = ttk.Entry(field_frame)
            functional_impairment_entry.grid(row=5, column=1, padx=5, pady=5, sticky='w')

            ttk.Label(field_frame, text="Comments").grid(row=6, column=0, padx=5, pady=5, sticky='w')
            _screening_commets_entry = ttk.Entry(field_frame)
            _screening_commets_entry.grid(row=6, column=1, padx=5, pady=5, sticky='w')

            button_frame = ttk.Frame(popup)
            button_frame.grid(row=2, column=0, columnspan=3, pady=15)

            # Update and Cancel buttons
            ttk.Button(button_frame, text="Update", command=lambda: [update_screening(assessmentId, screening_date_entry.get_date(), pReverse[provider_personnel_entry.get()], iReverse[screening_instrument_entry.get()], aReverse[provider_agency_entry.get()]), popup.destroy()]).grid(row=0, column=0, padx=5, pady=5, sticky='w')
            ttk.Button(button_frame, text="Cancel", command=lambda: [popup.destroy()]).grid(row=0, column=1, padx=5, pady=5, sticky='w')


        def add_new_screening_popup():
            popup = tk.Toplevel(self)
            popup.title("Add New Screening")
            popup.geometry("550x350")

            popup.grid_columnconfigure(0, weight=0)  
            popup.grid_columnconfigure(1, weight=1)

            instruments, iReverse = get_all_instruments()
            agencies, aReverse = get_all_agencies()
            personnel, pReverse = get_all_personnel()
            
            field_frame = ttk.Frame(popup)
            field_frame.grid(row=1, column=0, padx=5, pady=5, sticky='w')

            ttk.Label(popup, text="Fields marked with a (*) are required", foreground='red').grid(row=0, column=0, padx=5, pady=5, sticky='w')

            ttk.Label(field_frame, text="Screening Instrument *", foreground='black').grid(row=0, column=0, padx=5, pady=5, sticky='w')

            screening_instrument_entry = ttk.Combobox(field_frame, values=list(instruments.values()))
            screening_instrument_entry.grid(row=0, column=1, padx=5, pady=5, sticky='w')

            ttk.Label(field_frame, text="Scores of this Screening's Measures").grid(row=1, column=0, padx=5, pady=5, sticky='w')
            ttk.Label(field_frame).grid(row=1, column=1, padx=5, pady=5, sticky='w')

            ttk.Button(field_frame, text="Add Screening Instrument", command=add_screening_instrument_popup).grid(row=0, column=2, padx=5, pady=5, sticky='w')

            ttk.Label(field_frame, text="Screening Date *", foreground='black').grid(row=2, column=0, padx=5, pady=5, sticky='w')
            screening_date_entry = DateEntry(field_frame, background='darkblue', foreground='white', borderwidth=2)
            screening_date_entry.grid(row=2, column=1, padx=5, pady=5, sticky='w')

            ttk.Label(field_frame, text="Provider Agency *", foreground='black').grid(row=3, column=0, padx=5, pady=5, sticky='w')
            provider_agency_entry = ttk.Combobox(field_frame, values=list(agencies.values()))
            provider_agency_entry.grid(row=3, column=1, padx=5, pady=5, sticky='w')

            ttk.Label(field_frame, text="Provider Personnel *", foreground='black').grid(row=4, column=0, padx=5, pady=5, sticky='w')
            provider_personnel_entry = ttk.Combobox(field_frame, values=list(personnel.values())) 
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
            ttk.Button(button_frame, text="Save", command=lambda: [insert_new_screening(screening_date_entry.get_date(), pReverse[provider_personnel_entry.get()], iReverse[screening_instrument_entry.get()], aReverse[provider_agency_entry.get()]), popup.destroy()]).grid(row=0, column=0, padx=5, pady=5, sticky='w')
            ttk.Button(button_frame, text="Cancel", command=lambda: [popup.destroy()]).grid(row=0, column=1, padx=5, pady=5, sticky='w')

        def get_all_screenings():
            try:
                config = load_config()
                with psycopg2.connect(**config) as conn:
                    with conn.cursor() as cur:
                        cur.execute("""select case_mh_assessment_instrument.assessment_name, 
                                    case_mh_assessment.session_date, 
                                    employee.first_name,
                                    employee.last_name,
                                    case_mh_assessment.assessment_id,
                                    case_mh_assessment.mh_provider_agency_id
                                    from case_mh_assessment
                                    join case_mh_assessment_instrument on case_mh_assessment.assessment_instrument_id = case_mh_assessment_instrument.instrument_id
                                    join employee on case_mh_assessment.provider_employee_id = employee.employee_id 
                                    order by case_mh_assessment.session_date desc;""")
                        screenings = cur.fetchall()
                        return screenings
            except (psycopg2.DatabaseError, Exception) as error:
                print(f"{error}")
                exit()

        screenings_frame = tk.LabelFrame(scrollable_frame, text="Screenings Given", padx=10, pady=10)
        screenings_frame.grid(row=6, column=0, sticky='w', padx=10, pady=5)

        #Add New Screening button
        ttk.Button(screenings_frame, text="Add New Screening", command=add_new_screening_popup).grid(row=0, column=0, padx=5, pady=5)

        screenings = get_all_screenings()
        rowCounter = 2

        ttk.Label(screenings_frame, text="Actions").grid(row=1, column=0, padx=5, pady=5)
        ttk.Label(screenings_frame, text="Screening Instrument Name").grid(row=1, column=2, padx=5, pady=5)
        ttk.Label(screenings_frame, text="Date").grid(row=1, column=3, padx=5, pady=5)
        ttk.Label(screenings_frame, text="Provider Personnel").grid(row=1, column=4, padx=5, pady=5)

        #ttk.Label(screenings_frame, text=screening[0]).grid(row=2, column=1, padx=5, pady=5) Actions

        for screening in screenings:
         ttk.Button(screenings_frame, text="Edit", command=lambda:[edit_screening(screening[4])]).grid(row=rowCounter, column=0, padx=5, pady=5)
         ttk.Button(screenings_frame, text="Delete", command=lambda:[delete_screening(screening[4])]).grid(row=rowCounter, column=1, padx=5, pady=5)
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
            ttk.Button(popup, text="Update", command=lambda: popup.destroy).grid(row=4, column=0, padx=5, pady=5)
            ttk.Button(popup, text="Cancel", command=lambda: popup.destroy).grid(row=4, column=1, padx=5, pady=5)

        # Outside Referrals Section
        outside_referrals_frame = tk.LabelFrame(scrollable_frame, text="Outside Referrals", padx=10, pady=10)
        outside_referrals_frame.grid(row=7, column=0, sticky='w', padx=10, pady=5)

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
        additional_contact_frame.grid(row=8, column=0, sticky='w', padx=10, pady=5)

        # button to add a new point of contact
        ttk.Button(additional_contact_frame, text="+ Add New Point of Contact", command=add_contact_popup).grid(row=0, column=0, padx=5, pady=5, sticky="w")
        ttk.Label(additional_contact_frame, text="Action").grid(row=1, column=0, padx=5, pady=5)
        ttk.Label(additional_contact_frame, text="Agency").grid(row=1, column=1, padx=5, pady=5)
        ttk.Label(additional_contact_frame, text="Name").grid(row=1, column=2, padx=5, pady=5)
        ttk.Label(additional_contact_frame, text="Phone").grid(row=1, column=3, padx=5, pady=5)
        ttk.Label(additional_contact_frame, text="Email").grid(row=1, column=4, padx=5, pady=5)

        # Document Upload Section
        upload_frame = tk.LabelFrame(scrollable_frame, text="Document Upload", padx=10, pady=10)
        upload_frame.grid(row=9, column=0, sticky='w', padx=10, pady=5)

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

        def submit_all_fields(date, rAgencyId, lEmployeeId, vaCN, vaAId, serviceODate, sAccept, serviceEnd, mdtV, birthCert, policeR, cNum, cStatus, cReason):
            referralDate = date 
            referralAgencyId = rAgencyId 
            leadEmployeeId = lEmployeeId
            vaCaseNumber = vaCN 
            vaAgencyId = vaAId 
            servicesOfferedDate = serviceODate 
            servicesAccepted =sAccept
            servicesEndDate = serviceEnd 
            mdtReady = mdtV 
            hasBirthCert = birthCert
            hasPoliceReport = policeR 
            claimNumber = cNum 
            claimStatusId = cStatus
            claimDeniedReason =  cReason 

            sqlQuery = """
            UPDATE cac_case
            SET
            case_number = %s,
            cac_received_date = %s,
            case_closed_date = %s,
            closed_reason_id = %s,
            created_date = %s,
            mh_lead_employee_id = %s,
            va_agency_id = %s,
            va_case_number = %s,
            va_claim_denied_reason = %s,
            va_claim_number = %s,
            va_claim_status_id = %s,
            va_have_birth_cert = %s,
            va_has_police_report = %s,
            va_mdt_ready = %s,
            va_na = %s,
            va_referral_agency_id = %s,
            va_referral_date = %s,
            va_services_accepted = %s,
            va_services_offered_date = %s,
            va_services_end_date = %s
            WHERE case_id = %s
            """ 
            data_tuple = (
                caseNumber, caseReceivedDate, caseClosedDate, caseClosedReasonId, 
                caseCreatedDate, leadEmployeeId, vaAgencyId, vaCaseNumber, claimDeniedReason, claimNumber, claimStatusId, hasBirthCert, 
                hasPoliceReport, mdtReady, vaNa, referralAgencyId, referralDate, servicesAccepted, servicesOfferedDate, 
                servicesEndDate, caseId
            )
            try:
                config = load_config()
                with psycopg2.connect(**config) as conn:
                    with conn.cursor() as cur:
                        cur.execute(sqlQuery, (data_tuple))
                        conn.commit
                        messagebox.showinfo("Save", "VA information has been saved successfully!")
            except (psycopg2.DatabaseError, Exception) as error:
                print(f"{error}")
                exit()

        save_button = ttk.Button(widget_frame, text='SAVE', command= lambda: submit_all_fields(str(date_entry.get_date()), aReverse[referral_source.get()], pReverse[person_entry.get()], va_casenum_entry.get(), aReverse[agency_entry.get()], 
                                                                                          str(date_services_offered.get_date()), services_accept.get(), str(services_conclusion.get_date()), mdt.get(), birth_cert.get(),
                                                                                            police_report.get(), claim_number.get(), sReverse[status_entry.get()], claim_denied_reason.get()))
        cancel_button = ttk.Button(widget_frame, text='CANCEL')

        save_button.grid(row=1, column=0, sticky="w", padx=5)
        cancel_button.grid(row=1, column=1, sticky="w", padx=5)
        cancel_button.grid(row=1, column=1, sticky="w", padx=5)

    # -------------------- Navigation Functions --------------------
    def show_lookup_page(self):
        self.controller.show_frame(database_lookup_search.lookup_interface)

    def show_general_tab(self):
        self.controller.show_frame(Generaltab_interface.GeneraltabInterface)

    def show_people_tab(self):
        self.controller.show_frame(people_interface.people_interface)

    def show_mh_basic(self):
        self.controller.show_frame(MH_basic_interface.MHBasicInterface)

    def show_mh_assessment(self):
        self.controller.show_frame(MH_assessment.MHassessment)

    def show_mh_treatment_plan(self):
        self.controller.show_frame(MH_treatmentPlan_interface.MH_treatment_plan_interface)

    def show_va_tab(self):
        self.controller.show_frame(va_interface)

    def show_case_notes(self):
        self.controller.show_frame(case_notes.case_notes_interface)