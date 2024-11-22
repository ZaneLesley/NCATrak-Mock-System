# case_notes.py

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from tkcalendar import DateEntry, Calendar
import datetime
import calendar
import psycopg2
from configparser import ConfigParser
import os
import traceback

# Import other interfaces for navigation
import Generaltab_interface
import people_interface
import MH_basic_interface
import MH_assessment
import MH_treatmentPlan_interface
import va_tab_interface

class AddSessionForm(tk.Toplevel):
    def __init__(self, master, controller):
        super().__init__(master)
        self.title("Add New Session Log")
        self.geometry("1200x800")  # Adjust size to fit all fields

        # Store reference to master and controller
        self.master = master
        self.controller = controller
        self.conn = self.controller.conn
        self.cur = self.conn.cursor()
        self.case_id = self.controller.current_case_id
        self.cac_id = self.controller.cac_id

        # Scrollable Frame Setup
        self.canvas = tk.Canvas(self)
        self.scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.scrollbar.pack(side="right", fill="y")

        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollable_frame = ttk.Frame(self.canvas)

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(
                scrollregion=self.canvas.bbox("all")
            )
        )

        self.create_widgets()

    def create_widgets(self):
        # Variables to hold widget values
        self.date_var = tk.StringVar()
        self.start_time_var = tk.StringVar()
        self.end_time_var = tk.StringVar()
        self.status_var = tk.StringVar()
        self.provider_agency_var = tk.StringVar()
        self.provider_personnel_var = tk.StringVar()
        self.location_var = tk.StringVar()
        self.onsite_var = tk.BooleanVar()
        self.type_var = tk.StringVar()
        self.funding_source_var = tk.StringVar()
        self.intervention_var = tk.StringVar()
        self.lock_case_notes_var = tk.BooleanVar()
        self.recurring_var = tk.BooleanVar()
        self.recurrence_frequency_var = tk.StringVar()
        self.recurrence_duration_number_var = tk.IntVar()
        self.recurrence_duration_unit_var = tk.StringVar()

        # Mental Health Session Custom Fields
        self.custom_field_vars = [tk.StringVar() for _ in range(3)]
        self.custom_field_sizes = [1, 1, 1]  # For dynamic resizing, default size is 1

        # Notes
        self.notes_size = 1  # For dynamic resizing

        # Client Mood Checkboxes
        self.client_mood_vars = {}
        mood_options = ["Euthymic", "Depressed", "Anxious", "Angry", "Euphoric", "Other"]
        for mood in mood_options:
            self.client_mood_vars[mood] = tk.BooleanVar()

        # Client Affect Checkboxes
        self.client_affect_vars = {}
        affect_options = ["Stable", "Labile", "Flat", "Blunted", "Exaggerated",
                          "Appropriate", "Inappropriate", "Irritable", "Apathetic",
                          "Pleasant", "Other"]
        for affect in affect_options:
            self.client_affect_vars[affect] = tk.BooleanVar()

        # Suicidal Ideation
        self.suicidal_ideation_var = tk.StringVar()
        suicidal_options = ["Not Suicidal", "Suicidal Ideation", "Suicidal Ideation and Plan"]

        # Homicidal Ideation
        self.homicidal_ideation_var = tk.StringVar()
        homicidal_options = ["No Homicidal Ideation", "Homicidal Ideation"]

        # Attendees
        self.attendees_vars = {}
        attendees_options = self.controller.get_attendees()  # Get attendees from the controller
        for attendee in attendees_options:
            self.attendees_vars[attendee] = tk.BooleanVar()

        # Treatment Plan Progress
        self.treatment_plan_progress_var = tk.StringVar()
        treatment_progress_options = ["None", "Minimal", "Moderate", "Significant", "Met/Exceeded"]

        # Hardcoded options for dropdown menus
        self.status_options = self.controller.status_options
        self.status_mapping = self.controller.status_mapping
        self.status_reverse_mapping = self.controller.status_reverse_mapping

        self.type_options = self.controller.type_options
        self.type_mapping = self.controller.type_mapping
        self.type_reverse_mapping = self.controller.type_reverse_mapping

        # Provider Agency and Personnel options
        self.provider_agency_options = self.controller.get_provider_agency_options()
        self.provider_personnel_options = self.controller.get_provider_personnel_options()

        # Location options
        self.location_options = ["Location 1", "Location 2", "Location 3"]

        # Funding Source options
        self.funding_source_options = ["Source 1", "Source 2", "Source 3"]

        # Intervention options
        self.intervention_options = ["Intervention 1", "Intervention 2", "Intervention 3"]

        # Layout Configuration
        self.scrollable_frame.columnconfigure(0, weight=1)
        self.scrollable_frame.columnconfigure(1, weight=1)
        self.scrollable_frame.columnconfigure(2, weight=1)
        self.scrollable_frame.columnconfigure(3, weight=1)

        # Left Column Widgets
        row = 0
        ttk.Label(self.scrollable_frame, text="Date").grid(row=row, column=0, sticky='e', padx=5, pady=5)
        # Use DateEntry widget from tkcalendar
        date_entry = DateEntry(self.scrollable_frame, textvariable=self.date_var, date_pattern='yyyy-mm-dd')
        date_entry.grid(row=row, column=1, sticky='w', padx=5, pady=5)

        row += 1
        ttk.Label(self.scrollable_frame, text="Start Time").grid(row=row, column=0, sticky='e', padx=5, pady=5)
        start_entry = ttk.Combobox(self.scrollable_frame, textvariable=self.start_time_var,
                                   values=self.generate_time_options())
        start_entry.grid(row=row, column=1, sticky='w', padx=5, pady=5)

        row += 1
        ttk.Label(self.scrollable_frame, text="End Time").grid(row=row, column=0, sticky='e', padx=5, pady=5)
        end_entry = ttk.Combobox(self.scrollable_frame, textvariable=self.end_time_var,
                                 values=self.generate_time_options())
        end_entry.grid(row=row, column=1, sticky='w', padx=5, pady=5)

        row += 1
        ttk.Label(self.scrollable_frame, text="Status").grid(row=row, column=0, sticky='e', padx=5, pady=5)
        status_entry = ttk.Combobox(self.scrollable_frame, textvariable=self.status_var,
                                    values=self.status_options)
        status_entry.grid(row=row, column=1, sticky='w', padx=5, pady=5)

        row += 1
        ttk.Checkbutton(self.scrollable_frame, text="Recurring", variable=self.recurring_var).grid(row=row, column=1,
                                                                                                   sticky='w',
                                                                                                   padx=5, pady=5)

        row += 1
        ttk.Label(self.scrollable_frame, text="Recurrence Frequency").grid(row=row, column=0, sticky='e', padx=5,
                                                                           pady=5)
        recurrence_frequency_entry = ttk.Combobox(self.scrollable_frame, textvariable=self.recurrence_frequency_var,
                                                  values=["Weekly", "Bi-Weekly", "Monthly"])
        recurrence_frequency_entry.grid(row=row, column=1, sticky='w', padx=5, pady=5)

        row += 1
        ttk.Label(self.scrollable_frame, text="Recurrence Duration").grid(row=row, column=0, sticky='e', padx=5,
                                                                          pady=5)
        duration_frame = ttk.Frame(self.scrollable_frame)
        duration_frame.grid(row=row, column=1, sticky='w', padx=5, pady=5)
        ttk.Spinbox(duration_frame, from_=0, to=100, textvariable=self.recurrence_duration_number_var,
                    width=5).pack(side='left')
        ttk.Combobox(duration_frame, textvariable=self.recurrence_duration_unit_var,
                     values=["", "Months"], width=10).pack(side='left')

        # Right Column Widgets
        row = 0
        ttk.Label(self.scrollable_frame, text="Provider Agency").grid(row=row, column=2, sticky='e', padx=5, pady=5)
        provider_agency_entry = ttk.Combobox(self.scrollable_frame, textvariable=self.provider_agency_var,
                                             values=self.provider_agency_options)
        provider_agency_entry.grid(row=row, column=3, sticky='w', padx=5, pady=5)

        row += 1
        ttk.Label(self.scrollable_frame, text="Provider Personnel").grid(row=row, column=2, sticky='e', padx=5, pady=5)
        provider_personnel_entry = ttk.Combobox(self.scrollable_frame, textvariable=self.provider_personnel_var,
                                                values=self.provider_personnel_options)
        provider_personnel_entry.grid(row=row, column=3, sticky='w', padx=5, pady=5)

        row += 1
        ttk.Label(self.scrollable_frame, text="Location").grid(row=row, column=2, sticky='e', padx=5, pady=5)
        location_entry = ttk.Combobox(self.scrollable_frame, textvariable=self.location_var,
                                      values=self.location_options)
        location_entry.grid(row=row, column=3, sticky='w', padx=5, pady=5)

        row += 1
        ttk.Checkbutton(self.scrollable_frame, text="Onsite", variable=self.onsite_var).grid(row=row, column=3,
                                                                                             sticky='w', padx=5,
                                                                                             pady=5)

        row += 1
        ttk.Label(self.scrollable_frame, text="Type").grid(row=row, column=2, sticky='e', padx=5, pady=5)
        type_entry = ttk.Combobox(self.scrollable_frame, textvariable=self.type_var,
                                  values=self.type_options)
        type_entry.grid(row=row, column=3, sticky='w', padx=5, pady=5)

        row += 1
        ttk.Label(self.scrollable_frame, text="Funding Source").grid(row=row, column=2, sticky='e', padx=5, pady=5)
        funding_source_entry = ttk.Combobox(self.scrollable_frame, textvariable=self.funding_source_var,
                                            values=self.funding_source_options)
        funding_source_entry.grid(row=row, column=3, sticky='w', padx=5, pady=5)

        row += 1
        ttk.Label(self.scrollable_frame, text="Intervention").grid(row=row, column=2, sticky='e', padx=5, pady=5)
        intervention_entry = ttk.Combobox(self.scrollable_frame, textvariable=self.intervention_var,
                                          values=self.intervention_options)
        intervention_entry.grid(row=row, column=3, sticky='w', padx=5, pady=5)

        row += 1
        ttk.Checkbutton(self.scrollable_frame, text="Lock Case Notes", variable=self.lock_case_notes_var).grid(row=row,
                                                                                                               column=3,
                                                                                                               sticky='w',
                                                                                                               padx=5,
                                                                                                               pady=5)

        # Mental Health Session Custom Fields
        row += 1
        ttk.Label(self.scrollable_frame, text="Mental Health Session Custom Field 1").grid(row=row, column=0,
                                                                                          sticky='e', padx=5,
                                                                                          pady=5)
        custom_field_1_frame = ttk.Frame(self.scrollable_frame)
        custom_field_1_frame.grid(row=row, column=1, sticky='w', padx=5, pady=5)
        custom_field_1_entry = tk.Text(custom_field_1_frame, width=40, height=3)
        custom_field_1_entry.pack(side='left')
        ttk.Button(custom_field_1_frame, text="+",
                   command=lambda: self.resize_text(custom_field_1_entry, 1)).pack(side='left')
        ttk.Button(custom_field_1_frame, text="-",
                   command=lambda: self.resize_text(custom_field_1_entry, -1)).pack(side='left')

        row += 1
        ttk.Label(self.scrollable_frame, text="Mental Health Session Custom Field 2").grid(row=row, column=0,
                                                                                          sticky='e', padx=5,
                                                                                          pady=5)
        custom_field_2_entry = ttk.Entry(self.scrollable_frame, textvariable=self.custom_field_vars[1])
        custom_field_2_entry.grid(row=row, column=1, sticky='w', padx=5, pady=5)

        row += 1
        ttk.Label(self.scrollable_frame, text="Mental Health Session Custom Field 3").grid(row=row, column=0,
                                                                                          sticky='e', padx=5,
                                                                                          pady=5)
        custom_field_3_entry = ttk.Entry(self.scrollable_frame, textvariable=self.custom_field_vars[2])
        custom_field_3_entry.grid(row=row, column=1, sticky='w', padx=5, pady=5)

        # Notes
        row += 1
        ttk.Label(self.scrollable_frame, text="Notes").grid(row=row, column=0, sticky='e', padx=5, pady=5)
        notes_frame = ttk.Frame(self.scrollable_frame)
        notes_frame.grid(row=row, column=1, columnspan=3, sticky='w', padx=5, pady=5)
        self.notes_text = tk.Text(notes_frame, width=80, height=5)
        self.notes_text.pack(side='left')
        ttk.Button(notes_frame, text="+", command=lambda: self.resize_text(self.notes_text, 1)).pack(side='left')
        ttk.Button(notes_frame, text="-", command=lambda: self.resize_text(self.notes_text, -1)).pack(side='left')

        # Spacer
        row += 1
        ttk.Separator(self.scrollable_frame, orient='horizontal').grid(row=row, column=0, columnspan=4, sticky='ew',
                                                                       pady=10)

        # Bottom Section - Checkboxes and Radio Buttons
        row += 1
        # Client Mood
        mood_frame = ttk.LabelFrame(self.scrollable_frame, text="Client Mood")
        mood_frame.grid(row=row, column=0, padx=5, pady=5, sticky='nw')
        for mood in mood_options:
            ttk.Checkbutton(mood_frame, text=mood, variable=self.client_mood_vars[mood]).pack(anchor='w')

        # Client Affect
        affect_frame = ttk.LabelFrame(self.scrollable_frame, text="Client Affect")
        affect_frame.grid(row=row, column=1, padx=5, pady=5, sticky='nw')
        for affect in affect_options:
            ttk.Checkbutton(affect_frame, text=affect, variable=self.client_affect_vars[affect]).pack(anchor='w')

        # Attendees
        attendees_frame = ttk.LabelFrame(self.scrollable_frame, text="Attendees")
        attendees_frame.grid(row=row, column=2, padx=5, pady=5, sticky='nw')
        for attendee in self.attendees_vars:
            ttk.Checkbutton(attendees_frame, text=attendee, variable=self.attendees_vars[attendee]).pack(anchor='w')

        row += 1
        # Suicidal Ideation
        suicidal_frame = ttk.LabelFrame(self.scrollable_frame, text="Suicidal Ideation")
        suicidal_frame.grid(row=row, column=0, padx=5, pady=5, sticky='nw')
        for option in suicidal_options:
            ttk.Radiobutton(suicidal_frame, text=option, variable=self.suicidal_ideation_var,
                            value=option).pack(anchor='w')

        # Homicidal Ideation
        homicidal_frame = ttk.LabelFrame(self.scrollable_frame, text="Homicidal Ideation")
        homicidal_frame.grid(row=row, column=1, padx=5, pady=5, sticky='nw')
        for option in homicidal_options:
            ttk.Radiobutton(homicidal_frame, text=option, variable=self.homicidal_ideation_var,
                            value=option).pack(anchor='w')

        # Treatment Plan Progress
        treatment_frame = ttk.LabelFrame(self.scrollable_frame, text="Treatment Plan Progress")
        treatment_frame.grid(row=row, column=2, padx=5, pady=5, sticky='nw')
        for option in treatment_progress_options:
            ttk.Radiobutton(treatment_frame, text=option, variable=self.treatment_plan_progress_var,
                            value=option).pack(anchor='w')

        # Save and Cancel Buttons at the Bottom Right
        row += 1
        button_frame = ttk.Frame(self.scrollable_frame)
        button_frame.grid(row=row, column=2, columnspan=2, pady=20, sticky='e')
        ttk.Button(button_frame, text="Save", command=self.save_session).pack(side='left', padx=10)
        ttk.Button(button_frame, text="Cancel", command=self.cancel).pack(side='left', padx=10)

    def resize_text(self, text_widget, delta):
        current_height = int(text_widget.cget("height"))
        new_height = max(1, current_height + delta)
        text_widget.config(height=new_height)

    def generate_time_options(self):
        times = []
        for hour in range(24):
            for minute in (0, 30):
                time_str = f"{hour % 12 if hour % 12 else 12}:{minute:02d} {'AM' if hour < 12 else 'PM'}"
                times.append(time_str)
        return times

    def save_session(self):
        # Collect data from the form
        session_date = self.date_var.get()
        start_time = self.start_time_var.get()
        end_time = self.end_time_var.get()
        status_name = self.status_var.get()
        session_type_name = self.type_var.get()
        notes = self.notes_text.get("1.0", tk.END).strip()

        # Map names to IDs
        status_id = self.status_mapping.get(status_name)
        session_type_id = self.type_mapping.get(session_type_name)

        # Ensure required fields are filled
        if not session_date or not status_id or not session_type_id:
            messagebox.showerror("Error", "Please fill in all required fields.")
            return

        try:
            # Generate a unique 'case_mh_session_id'
            self.cur.execute("SELECT MAX(case_mh_session_id) FROM case_mh_session_log_enc")
            max_id = self.cur.fetchone()[0]
            if max_id is None:
                case_mh_session_id = 1
            else:
                case_mh_session_id = max_id + 1

            # Insert new session
            query = """
                INSERT INTO case_mh_session_log_enc (
                    cac_id,
                    case_id,
                    case_mh_session_id,
                    session_date,
                    start_time,
                    end_time,
                    session_status_id,
                    session_type_id,
                    comments
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            data = (
                self.cac_id,
                self.case_id,
                case_mh_session_id,
                session_date,
                start_time,
                end_time,
                status_id,
                session_type_id,
                notes
            )
            self.cur.execute(query, data)
            self.conn.commit()
            messagebox.showinfo("Save", "Session has been saved successfully!")

            # Refresh the session tree in the main interface
            self.controller.load_session_logs()
            self.destroy()
        except Exception as e:
            self.conn.rollback()
            traceback_str = traceback.format_exc()
            print(f"Error in save_session:\n{traceback_str}")
            messagebox.showerror("Error", f"Failed to save session: {e}")

    def cancel(self):
        self.destroy()

class case_notes_interface(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        self.controller = controller

        # Add navigation buttons at the top
        nav_frame = ttk.Frame(self)
        nav_frame.grid(row=0, column=0, padx=10, pady=10, sticky='w')

        # Add buttons to navigate to other interfaces
        ttk.Button(nav_frame, text="General Tab", command=lambda: controller.show_frame(Generaltab_interface.GeneraltabInterface)).pack(side='left', padx=5)
        ttk.Button(nav_frame, text="People", command=lambda: controller.show_frame(people_interface.people_interface)).pack(side='left', padx=5)
        ttk.Button(nav_frame, text="MH Basic", command=lambda: controller.show_frame(MH_basic_interface.MHBasicInterface)).pack(side='left', padx=5)
        ttk.Button(nav_frame, text="MH Assessment", command=lambda: controller.show_frame(MH_assessment.MHassessment)).pack(side='left', padx=5)
        ttk.Button(nav_frame, text="MH Treatment Plan", command=lambda: controller.show_frame(MH_treatmentPlan_interface.MH_treatment_plan_interface)).pack(side='left', padx=5)
        ttk.Button(nav_frame, text="VA Tab", command=lambda: controller.show_frame(va_tab_interface.va_interface)).pack(side='left', padx=5)
        # Add more buttons as needed

        self.grid_rowconfigure(2, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Establish database connection
        self.conn = self.get_connection()
        if not self.conn:
            return
        self.conn.autocommit = False  # Manage transactions manually
        self.cur = self.conn.cursor()

        # Get current case_id and cac_id
        self.current_case_id = self.get_current_case_id()
        self.cac_id = self.get_cac_id()

        # Hardcoded options for mappings
        self.status_options = [
            "Attended", "Canceled", "Canceled & Rescheduled", "Client Canceled",
            "Clinician Canceled", "Declined", "No-show", "Scheduled", "To be scheduled"
        ]
        self.status_mapping = {name: idx for idx, name in enumerate(self.status_options, start=1)}
        self.status_reverse_mapping = {idx: name for name, idx in self.status_mapping.items()}

        self.type_options = [
            "Individual Session with Dog", "Individual Talk", "Group/Support",
            "Session with Interpreter present", "Family", "Psycho/Social Group"
        ]
        self.type_mapping = {name: idx for idx, name in enumerate(self.type_options, start=1)}
        self.type_reverse_mapping = {idx: name for name, idx in self.type_mapping.items()}

        # Setup notebook for tabs
        self.notebook = ttk.Notebook(self)
        self.notebook.grid(row=1, column=0, padx=10, pady=10)

        # Session Log / Appointments tab
        self.session_log_tab = ttk.Frame(self.notebook, padding=10)
        self.notebook.add(self.session_log_tab, text='Session Log / Appointments')
        self.setup_session_log_tab()

    # -------------------- Database Connection and Functions --------------------
    def get_connection(self):
        # Read database configuration from database.ini
        try:
            config_file = os.path.join(os.path.dirname(__file__), 'database', 'database.ini')
            parser = ConfigParser()
            parser.read(config_file)
            db_config = {}
            if parser.has_section('postgresql'):
                params = parser.items('postgresql')
                for param in params:
                    db_config[param[0]] = param[1]
                conn = psycopg2.connect(**db_config)
                print("Database connection established.")
                return conn
            else:
                messagebox.showerror("Error", "Database configuration file not found.")
                return None
        except Exception as e:
            messagebox.showerror("Error", f"Failed to connect to the database: {e}")
            return None

    def get_current_case_id(self):
        try:
            cur = self.conn.cursor()
            query = "SELECT case_id FROM cac_case LIMIT 1;"
            cur.execute(query)
            result = cur.fetchone()
            cur.close()
            if result:
                return result[0]
            else:
                messagebox.showerror("Error", "No cases found in the database.")
                return None
        except Exception as e:
            messagebox.showerror("Error", f"Failed to retrieve case ID: {e}")
            return None

    def get_cac_id(self):
        try:
            cur = self.conn.cursor()
            query = "SELECT cac_id FROM cac_case WHERE case_id = %s;"
            cur.execute(query, (self.current_case_id,))
            result = cur.fetchone()
            cur.close()
            if result:
                return result[0]
            else:
                messagebox.showerror("Error", "CAC ID not found for the current case.")
                return None
        except Exception as e:
            messagebox.showerror("Error", f"Failed to retrieve CAC ID: {e}")
            return None

    def get_attendees(self):
        # Fetch attendees from the database
        attendees = []
        try:
            self.cur.execute("""
                SELECT first_name || ' ' || last_name
                FROM person p
                JOIN case_person cp ON p.person_id = cp.person_id
                WHERE cp.case_id = %s;
            """, (self.current_case_id,))
            rows = self.cur.fetchall()
            attendees = [row[0] for row in rows]
            print(f"Attendees loaded: {attendees}")
        except Exception as e:
            self.conn.rollback()
            traceback_str = traceback.format_exc()
            print(f"Error in get_attendees:\n{traceback_str}")
            messagebox.showerror("Error", f"Failed to load attendees: {e}")
        return attendees

    def get_provider_agency_options(self):
        # Fetch provider agency options from the database
        agencies = []
        try:
            self.cur.execute("SELECT agency_name FROM cac_agency WHERE cac_id = %s;", (self.cac_id,))
            rows = self.cur.fetchall()
            agencies = [row[0] for row in rows]
            if not agencies:
                agencies = ["Agency 1", "Agency 2", "Agency 3"]
            return agencies
        except Exception as e:
            self.conn.rollback()
            print(f"Error fetching provider agencies: {e}")
            return ["Agency 1", "Agency 2", "Agency 3"]

    def get_provider_personnel_options(self):
        # Fetch provider personnel options from the database
        personnel = []
        try:
            self.cur.execute("SELECT first_name || ' ' || last_name FROM employee WHERE cac_id = %s;", (self.cac_id,))
            rows = self.cur.fetchall()
            personnel = [row[0] for row in rows]
            if not personnel:
                personnel = ["Sarah Jones", "Personnel 2", "Personnel 3"]
            return personnel
        except Exception as e:
            self.conn.rollback()
            print(f"Error fetching provider personnel: {e}")
            return ["Sarah Jones", "Personnel 2", "Personnel 3"]

    def open_add_session_form(self):
        try:
            add_session_window = AddSessionForm(self, self)
        except Exception as e:
            traceback_str = traceback.format_exc()
            print(f"Error in open_add_session_form:\n{traceback_str}")
            messagebox.showerror("Error", f"Failed to open Add Session Form: {e}")

    def setup_session_log_tab(self):
        # Tabs for Agenda and Calendar
        self.agenda_calendar_tabs = ttk.Notebook(self.session_log_tab)
        self.agenda_tab = ttk.Frame(self.agenda_calendar_tabs)
        self.calendar_tab = ttk.Frame(self.agenda_calendar_tabs)
        self.agenda_calendar_tabs.add(self.agenda_tab, text="Agenda")
        self.agenda_calendar_tabs.add(self.calendar_tab, text="Calendar")
        self.agenda_calendar_tabs.pack(expand=True, fill='both', padx=10, pady=10)

        # Setup session management and document upload sections in Agenda tab
        self.setup_session_management()
        self.setup_document_upload()

        # Setup calendar tab
        self.setup_calendar_tab()

    def setup_session_management(self):
        # Session management buttons
        button_frame = ttk.Frame(self.agenda_tab)
        button_frame.pack(fill='x', pady=10)

        ttk.Button(button_frame, text="+ Add New Session Log", command=self.open_add_session_form).pack(side=tk.LEFT, padx=10)

        # Navigation buttons placed above the session table
        nav_frame_top = ttk.Frame(self.agenda_tab)
        nav_frame_top.pack(fill='x', pady=5)

        self.newer_button = ttk.Button(nav_frame_top, text="Newer Records", command=self.load_newer_records)
        self.newer_button.pack(side=tk.RIGHT, padx=5)

        self.older_button = ttk.Button(nav_frame_top, text="Older Records", command=self.load_older_records)
        self.older_button.pack(side=tk.RIGHT, padx=5)

        # Treeview for sessions
        self.session_tree = ttk.Treeview(self.agenda_tab, columns=("Date", "Start Time", "End Time", "Type", "Status"), show="headings")
        for col in self.session_tree['columns']:
            self.session_tree.heading(col, text=col)
            self.session_tree.column(col, anchor="center", width=100)
        self.session_tree.pack(expand=True, fill='both', padx=10, pady=10)

        # Load sessions from the database
        self.load_session_logs()

        # Pagination controls
        pagination_frame = ttk.Frame(self.agenda_tab)
        pagination_frame.pack(fill='x', padx=10, pady=5)

        self.first_page_button = ttk.Button(pagination_frame, text="<<", command=self.first_page)
        self.first_page_button.pack(side=tk.LEFT, padx=5)

        self.prev_page_button = ttk.Button(pagination_frame, text="<", command=self.previous_page)
        self.prev_page_button.pack(side=tk.LEFT, padx=5)

        self.page_number_var = tk.IntVar(value=1)
        self.page_number_label = ttk.Label(pagination_frame, textvariable=self.page_number_var)
        self.page_number_label.pack(side=tk.LEFT, padx=5)

        self.next_page_button = ttk.Button(pagination_frame, text=">", command=self.next_page)
        self.next_page_button.pack(side=tk.LEFT, padx=5)

        self.last_page_button = ttk.Button(pagination_frame, text=">>", command=self.last_page)
        self.last_page_button.pack(side=tk.LEFT, padx=5)

        # Items per page dropdown
        items_per_page_options = [5, 10, 15, 'All']
        self.items_per_page_var = tk.StringVar(value='5')
        self.items_per_page_dropdown = ttk.Combobox(pagination_frame, textvariable=self.items_per_page_var, values=items_per_page_options, width=5)
        self.items_per_page_dropdown.pack(side=tk.LEFT, padx=5)

        ttk.Label(pagination_frame, text="items per page").pack(side=tk.LEFT, padx=5)

    def load_session_logs(self):
        # Clear the Treeview
        for item in self.session_tree.get_children():
            self.session_tree.delete(item)

        try:
            # Fetch session logs from the database
            query = """
                SELECT session_date, start_time, end_time, session_type_id, session_status_id, case_mh_session_id
                FROM case_mh_session_log_enc
                WHERE case_id = %s
                ORDER BY session_date DESC;
            """
            self.cur.execute(query, (self.current_case_id,))
            rows = self.cur.fetchall()

            if rows:
                for row in rows:
                    # Map IDs to names
                    session_type_name = self.type_reverse_mapping.get(row[3], "Unknown")
                    status_name = self.status_reverse_mapping.get(row[4], "Unknown")
                    # Insert data into the Treeview
                    self.session_tree.insert('', 'end', values=(row[0], row[1], row[2], session_type_name, status_name), iid=row[5])
            else:
                self.session_tree.insert('', 'end', values=("No sessions to display", "", "", "", ""))
        except Exception as e:
            self.conn.rollback()
            traceback_str = traceback.format_exc()
            print(f"Error in load_session_logs:\n{traceback_str}")
            messagebox.showerror("Error", f"Failed to load sessions: {e}")
            # Display a message that there are no sessions to display
            self.session_tree.insert('', 'end', values=("No sessions to display", "", "", "", ""))

    def setup_document_upload(self):
        # Document Upload section title
        upload_title_frame = ttk.Frame(self.agenda_tab, padding="10")
        upload_title_frame.pack(fill='x', expand=False, pady=5)
        ttk.Label(upload_title_frame, text="Document Upload", font=('Arial', 16)).pack(side=tk.LEFT)

        # Treeview for document uploads
        upload_frame = ttk.Frame(self.agenda_tab, padding="10")
        upload_frame.pack(fill='x', expand=False, pady=10)
        self.upload_tree = ttk.Treeview(upload_frame, columns=("File Name", "Upload Date", "User", "Page", "Size"), show="headings")
        for col in self.upload_tree['columns']:
            self.upload_tree.heading(col, text=col)
            self.upload_tree.column(col, anchor="center", width=100)
        self.upload_tree.pack(expand=True, fill='both', padx=10, pady=10)

        # No data placeholder
        self.upload_tree.insert('', 'end', values=("No documents to display", "", "", "", ""))

        # Pagination controls
        pagination_frame = ttk.Frame(upload_frame)
        pagination_frame.pack(fill='x', padx=10, pady=5)

        self.upload_first_page_button = ttk.Button(pagination_frame, text="<<", command=self.upload_first_page)
        self.upload_first_page_button.pack(side=tk.LEFT, padx=5)

        self.upload_prev_page_button = ttk.Button(pagination_frame, text="<", command=self.upload_previous_page)
        self.upload_prev_page_button.pack(side=tk.LEFT, padx=5)

        self.upload_page_number_var = tk.IntVar(value=1)
        self.upload_page_number_label = ttk.Label(pagination_frame, textvariable=self.upload_page_number_var)
        self.upload_page_number_label.pack(side=tk.LEFT, padx=5)

        self.upload_next_page_button = ttk.Button(pagination_frame, text=">", command=self.upload_next_page)
        self.upload_next_page_button.pack(side=tk.LEFT, padx=5)

        self.upload_last_page_button = ttk.Button(pagination_frame, text=">>", command=self.upload_last_page)
        self.upload_last_page_button.pack(side=tk.LEFT, padx=5)

        # Items per page dropdown
        items_per_page_options = [5, 10, 15, 'All']
        self.upload_items_per_page_var = tk.StringVar(value='5')
        self.upload_items_per_page_dropdown = ttk.Combobox(pagination_frame, textvariable=self.upload_items_per_page_var, values=items_per_page_options, width=5)
        self.upload_items_per_page_dropdown.pack(side=tk.LEFT, padx=5)

        ttk.Label(pagination_frame, text="items per page").pack(side=tk.LEFT, padx=5)

        # File selection button
        file_nav_frame = ttk.Frame(upload_frame)
        file_nav_frame.pack(fill='x', pady=10)
        ttk.Button(file_nav_frame, text="Select Files...", command=self.select_files).pack(side=tk.LEFT, padx=10)

    def setup_calendar_tab(self):
        # Controls above the calendar
        controls_frame = ttk.Frame(self.calendar_tab)
        controls_frame.pack(fill='x', padx=10, pady=10)

        # 'Today' button
        today_button = ttk.Button(controls_frame, text="Today", command=self.go_to_today)
        today_button.pack(side=tk.LEFT)

        # Left arrow button
        prev_month_button = ttk.Button(controls_frame, text="<", command=self.prev_month)
        prev_month_button.pack(side=tk.LEFT, padx=5)

        # Right arrow button
        next_month_button = ttk.Button(controls_frame, text=">", command=self.next_month)
        next_month_button.pack(side=tk.LEFT, padx=5)

        # Display of current month and year
        self.current_date = datetime.date.today()
        self.month_year_var = tk.StringVar()
        self.update_month_year_label()
        month_year_label = ttk.Label(controls_frame, textvariable=self.month_year_var)
        month_year_label.pack(side=tk.LEFT, padx=10)

        # Calendar widget
        self.calendar_widget = Calendar(self.calendar_tab, selectmode='day',
                                        year=self.current_date.year, month=self.current_date.month,
                                        day=self.current_date.day)
        self.calendar_widget.pack(expand=True, fill='both', padx=10, pady=10)

        # Load sessions and mark them on the calendar
        self.populate_calendar()

    def populate_calendar(self):
        try:
            # Fetch session dates from the database
            query = "SELECT session_date, case_mh_session_id FROM case_mh_session_log_enc WHERE case_id = %s;"
            self.cur.execute(query, (self.current_case_id,))
            sessions = self.cur.fetchall()
            for session_date, session_id in sessions:
                self.calendar_widget.calevent_create(session_date, 'Session', 'session')
        except Exception as e:
            self.conn.rollback()
            traceback_str = traceback.format_exc()
            print(f"Error in populate_calendar:\n{traceback_str}")
            messagebox.showerror("Error", f"Failed to load sessions for calendar: {e}")

        # Bind date selection
        self.calendar_widget.bind("<<CalendarSelected>>", self.on_calendar_date_select)

    def on_calendar_date_select(self, event):
        selected_date = self.calendar_widget.selection_get()
        try:
            query = """
                SELECT session_date, start_time, end_time, session_type_id, session_status_id
                FROM case_mh_session_log_enc
                WHERE session_date = %s AND case_id = %s;
            """
            self.cur.execute(query, (selected_date, self.current_case_id))
            sessions = self.cur.fetchall()

            if sessions:
                # Display sessions for the selected date
                session_info = ""
                for session in sessions:
                    session_type_name = self.type_reverse_mapping.get(session[3], "Unknown")
                    status_name = self.status_reverse_mapping.get(session[4], "Unknown")
                    session_info += f"Time: {session[1]} - {session[2]}, Type: {session_type_name}, Status: {status_name}\n"

                messagebox.showinfo("Sessions on " + selected_date.strftime('%Y-%m-%d'), session_info)
            else:
                messagebox.showinfo("No Sessions", "No sessions scheduled on this date.")
        except Exception as e:
            self.conn.rollback()
            traceback_str = traceback.format_exc()
            print(f"Error in on_calendar_date_select:\n{traceback_str}")
            messagebox.showerror("Error", f"Failed to retrieve sessions: {e}")

    def go_to_today(self):
        self.current_date = datetime.date.today()
        self.calendar_widget.selection_set(self.current_date)
        self.calendar_widget.see(self.current_date)
        self.update_month_year_label()
        # No need to reload events unless necessary

    def prev_month(self):
        first_day = self.current_date.replace(day=1)
        prev_month_last_day = first_day - datetime.timedelta(days=1)
        self.current_date = prev_month_last_day.replace(day=1)
        self.calendar_widget.see(self.current_date)
        self.update_month_year_label()

    def next_month(self):
        days_in_month = calendar.monthrange(self.current_date.year, self.current_date.month)[1]
        next_month_first_day = self.current_date.replace(day=days_in_month) + datetime.timedelta(days=1)
        self.current_date = next_month_first_day
        self.calendar_widget.see(self.current_date)
        self.update_month_year_label()

    def update_month_year_label(self):
        month_name = self.current_date.strftime("%B")
        year = self.current_date.year
        self.month_year_var.set(f"{month_name} {year}")

    def load_newer_records(self):
        messagebox.showinfo("www.ncatrak.org", "There are no sessions newer than what is currently on the screen.")

    def load_older_records(self):
        messagebox.showinfo("www.ncatrak.org", "There are no sessions older than what is currently on the screen.")

    def select_files(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            file_name = os.path.basename(file_path)
            self.upload_tree.insert('', 'end', values=(file_name, 'Today', 'User', '1', '1MB'))

    def view_details(self):
        messagebox.showinfo("Details", "Functionality not implemented yet.")

    # Pagination methods for sessions
    def first_page(self):
        messagebox.showinfo("Pagination", "First page clicked.")

    def previous_page(self):
        messagebox.showinfo("Pagination", "Previous page clicked.")

    def next_page(self):
        messagebox.showinfo("Pagination", "Next page clicked.")

    def last_page(self):
        messagebox.showinfo("Pagination", "Last page clicked.")

    # Pagination methods for uploads
    def upload_first_page(self):
        messagebox.showinfo("Pagination", "First page clicked (Uploads).")

    def upload_previous_page(self):
        messagebox.showinfo("Pagination", "Previous page clicked (Uploads).")

    def upload_next_page(self):
        messagebox.showinfo("Pagination", "Next page clicked (Uploads).")

    def upload_last_page(self):
        messagebox.showinfo("Pagination", "Last page clicked (Uploads).")

    def on_closing(self):
        if hasattr(self, 'cur') and self.cur:
            self.cur.close()
        if hasattr(self, 'conn') and self.conn:
            self.conn.close()
        self.destroy()

