import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
from tkinter import filedialog
import psycopg2
import configparser
from faker import Faker
import Generaltab_interface
import people_interface
import MH_basic_interface
import MH_assessment
import va_tab_interface
import case_notes
import sv_ttk
import MH_treatmentPlan_interface
import os
from configparser import ConfigParser


class MHassessment(tk.Frame):
    
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        self.grid_rowconfigure(2, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Nav bar buttons
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
                             command=lambda: controller.show_frame(MHassessment))
        button4.grid(row=0, column=3, padx=5, pady=5)

        button5 = ttk.Button(self, text="Mental Health - Treatment Plan",
                             command=lambda: controller.show_frame(MH_treatmentPlan_interface.MH_treatment_plan_interface))
        button5.grid(row=0, column=4, padx=5, pady=5)

        button6 = ttk.Button(self, text="VA",
                             command=lambda: controller.show_frame(va_tab_interface.va_interface))
        button6.grid(row=0, column=5, padx=5, pady=5)

        button7 = ttk.Button(self, text="Case Notes",
                             command=lambda: controller.show_frame(case_notes.case_notes_interface))
        button7.grid(row=0, column=6, padx=5, pady=5)

        # Create a canvas and a scrollbar
        canvas = tk.Canvas(self)
        scrollbar = ttk.Scrollbar(self, orient="vertical", command=canvas.yview)
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
        
        
        # # Assessments Given Section 
        assessments_frame = tk.LabelFrame(scrollable_frame, text="Assessments Given", padx=10, pady=10)
        assessments_frame.pack(fill="x", padx=10, pady=5)

        # Button to add new assessment
        ttk.Button(assessments_frame, text="+ Add New Assessment", command=self.add_assessment_popup).grid(row=0, column=0, padx=5, pady=5, sticky="w")

        # Column headers
        ttk.Label(assessments_frame, text="Assessment Instrument Name").grid(row=1, column=0, padx=5, pady=5)
        ttk.Label(assessments_frame, text="Timing").grid(row=1, column=1, padx=5, pady=5)
        ttk.Label(assessments_frame, text="Session Date").grid(row=1, column=2, padx=5, pady=5)

        # Fetch and display existing assessments
        try:
            config = self.load_config()
            with psycopg2.connect(**config) as conn:
                with conn.cursor() as cur:
                    query = "SELECT assessment_instrument_id, timing_id, session_date FROM case_mh_assessment"
                    cur.execute(query)
                    assessments = cur.fetchall()

                    for index, assessment in enumerate(assessments, start=2):  # Start from row 2
                        instrument_name = self.get_assessment_instrument_name(assessment[0])
                        timing_name = self.get_timing_name(assessment[1])

                        ttk.Label(assessments_frame, text=instrument_name or "Unknown").grid(row=index, column=0, padx=5, pady=5)
                        ttk.Label(assessments_frame, text=timing_name).grid(row=index, column=1, padx=5, pady=5)
                        ttk.Label(assessments_frame, text=str(assessment[2])).grid(row=index, column=2, padx=5, pady=5)
        except Exception as error:
            print(f"Error fetching assessments: {error}")

        # Diagnosis Log Section
        diagnosis_frame = tk.LabelFrame(scrollable_frame, text="Diagnosis Log", padx=10, pady=10)
        diagnosis_frame.pack(fill="x", padx=10, pady=5)

        # Button to add a new diagnosis
        ttk.Button(diagnosis_frame, text="+ Add Diagnosis", command=self.add_diagnosis_popup).grid(row=0, column=0, padx=5, pady=5, sticky="w")

        # Column headers for the diagnosis log table
        ttk.Label(diagnosis_frame, text="MH Provider Agency").grid(row=1, column=0, padx=5, pady=5)
        ttk.Label(diagnosis_frame, text="Diagnosis Date").grid(row=1, column=1, padx=5, pady=5)

        # Fetch and display existing diagnosis records
        try:
            config = self.load_config()
            with psycopg2.connect(**config) as conn:
                with conn.cursor() as cur:
                    # Fetch diagnosis log details
                    query = "SELECT mh_provider_agency_id, diagnosis_date FROM case_mh_assessment_diagnosis"
                    cur.execute(query)
                    diagnoses = cur.fetchall()

                    for index, diagnosis in enumerate(diagnoses, start=2):  # Start from row 2
                        agency_name = self.get_agency_name_by_id(diagnosis[0])

                        ttk.Label(diagnosis_frame, text=agency_name).grid(row=index, column=0, padx=5, pady=5)
                        ttk.Label(diagnosis_frame, text=str(diagnosis[1])).grid(row=index, column=1, padx=5, pady=5)
                        
        except Exception as error:
            print(f"Error fetching diagnosis log: {error}")



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

    def load_config(self, filename=None, section='postgresql'):
        """Load database configuration from the ini file."""
        
        cwd = os.path.dirname(os.path.abspath(__file__))
        database_dir= os.path.join(cwd, "database")
        if filename is None:
                filename = os.path.join(database_dir, "database.ini")
        else:
                filename = os.path.join(database_dir, filename)
      
        parser = ConfigParser()
        parser.read(filename)
        config = {}
        if parser.has_section(section):
            params = parser.items(section)
            for param in params:
                config[param[0]] = param[1]
        else:
            raise Exception(f"Section {section} not found in {filename}")
        return config


    def add_assessment_popup(self):
        """Popup window for adding a new assessment."""
        popup = tk.Toplevel(self)
        popup.title("Add New Assessment")
        popup.geometry("600x600")

        # Assessment Instrument Dropdown
        ttk.Label(popup, text="Assessment Instrument").grid(row=0, column=0, padx=10, pady=5, sticky="w")
        assessment_instrument_var = tk.StringVar()
        assessment_instrument_dropdown = ttk.Combobox(popup, textvariable=assessment_instrument_var, values=self.get_assessment_instruments(), width=40)
        assessment_instrument_dropdown.grid(row=0, column=1, padx=10, pady=5)
        # Add button for custom instruments
        ttk.Button(popup, text="Add", command=self.add_custom_assessment_popup).grid(row=0, column=2, padx=5, pady=5)


        # Score Entry
        ttk.Label(popup, text="Score").grid(row=1, column=0, padx=10, pady=5, sticky="w")
        score_var = tk.StringVar()
        score_entry = ttk.Entry(popup, textvariable=score_var, width=40)
        score_entry.grid(row=1, column=1, padx=10, pady=5)

        # Session Date
        ttk.Label(popup, text="Session Date").grid(row=2, column=0, padx=10, pady=5, sticky="w")
        session_date_entry = DateEntry(popup, width=20)
        session_date_entry.grid(row=2, column=1, padx=10, pady=5)

        # Assessment Date
        ttk.Label(popup, text="Assessment Date").grid(row=3, column=0, padx=10, pady=5, sticky="w")
        assessment_date_entry = DateEntry(popup, width=20)
        assessment_date_entry.grid(row=3, column=1, padx=10, pady=5)
        
        # Provider Agency Dropdown
        ttk.Label(popup, text="Provider Agency").grid(row=4, column=0, padx=10, pady=5, sticky="w")
        provider_agency_var = tk.StringVar()
        provider_agency_dropdown = ttk.Combobox(popup, textvariable=provider_agency_var, values=self.get_provider_agencies(), width=40)
        provider_agency_dropdown.grid(row=4, column=1, padx=10, pady=5)

        # Provider Employee ID
        ttk.Label(popup, text="Provider Employee ID").grid(row=5, column=0, padx=10, pady=5, sticky="w")
        provider_employee_id_var = tk.StringVar()
        provider_employee_id_entry = ttk.Entry(popup, textvariable=provider_employee_id_var, width=40)
        provider_employee_id_entry.grid(row=5, column=1, padx=10, pady=5)

        # Case ID
        ttk.Label(popup, text="Case ID").grid(row=6, column=0, padx=10, pady=5, sticky="w")
        case_id_var = tk.StringVar()
        case_id_entry = ttk.Entry(popup, textvariable=case_id_var, width=40)
        case_id_entry.grid(row=6, column=1, padx=10, pady=5)

        # Timing Dropdown
        ttk.Label(popup, text="Timing").grid(row=7, column=0, padx=10, pady=5, sticky="w")
        timing_var = tk.StringVar()
        timing_mapping = {"Pre-Treatment": 1, "Mid-Treatment": 2, "Post-Treatment": 3}
        timing_dropdown = ttk.Combobox(popup, textvariable=timing_var, values=list(timing_mapping.keys()), width=40)
        timing_dropdown.grid(row=7, column=1, padx=10, pady=5)

        # Comments
        ttk.Label(popup, text="Comments").grid(row=8, column=0, padx=10, pady=5, sticky="w")
        comments_var = tk.StringVar()
        comments_entry = ttk.Entry(popup, textvariable=comments_var, width=40)
        comments_entry.grid(row=8, column=1, padx=10, pady=5)
        
        def save_assessment():
            # Fetch inputs
            instrument_name = assessment_instrument_var.get()
            assessment_instrument_id = self.get_assessment_instrument_id(instrument_name)
            score = score_var.get()
            session_date = session_date_entry.get_date()
            assessment_date = assessment_date_entry.get_date()
            provider_agency_name = provider_agency_var.get()
            agency_id = self.get_agency_id_by_name(provider_agency_name)
            cac_id = self.get_cac_id_by_agency(provider_agency_name)
            mh_provider_agency_id = agency_id
            provider_employee_id = provider_employee_id_var.get().strip()
            
            # Handle optional employee ID
            if provider_employee_id.isdigit():
                provider_employee_id = int(provider_employee_id)
            else:
                provider_employee_id = None

            case_id = int(case_id_var.get().strip())
            timing_id = timing_mapping.get(timing_var.get(), None)
            comments = comments_var.get().strip()

            # Generate unique IDs
            assessment_id = self.generate_unique_id("case_mh_assessment", "assessment_id")
            score_id = self.generate_unique_id("case_mh_assessment_measure_scores", "score_id")

            # Insert into database
            self.save_assessment(
                assessment_id, cac_id, case_id, agency_id, mh_provider_agency_id, assessment_instrument_id,
                provider_employee_id, timing_id, session_date, assessment_date, comments)
            
            self.save_score(score_id, cac_id, case_id, assessment_id, assessment_instrument_id, score)

            popup.destroy()
            
        ttk.Button(popup, text="Save", command=save_assessment).grid(row=9, column=0, padx=10, pady=10)
        ttk.Button(popup, text="Cancel", command=popup.destroy).grid(row=9, column=1, padx=10, pady=10)
        
    def add_custom_assessment_popup(self):
        """Popup window to add a new custom assessment instrument."""
        custom_popup = tk.Toplevel(self)
        custom_popup.title("Add Custom Assessment Instrument")
        custom_popup.geometry("400x200")

        # Label and entry for the new assessment instrument
        ttk.Label(custom_popup, text="Enter New Instrument:").grid(row=0, column=0, padx=10, pady=10, sticky="w")
        new_assessment_name_var = tk.StringVar()
        new_assessment_name_entry = ttk.Entry(custom_popup, textvariable=new_assessment_name_var, width=40)
        new_assessment_name_entry.grid(row=0, column=1, padx=10, pady=10, sticky="w")

        def save_new_assessment():
            """Save a new custom assessment instrument."""
            assessment_name = new_assessment_name_var.get().strip()
            if not assessment_name:
                messagebox.showerror("Input Error", "Assessment name cannot be empty.")
                return

            try:
                # Load the database configuration
                config = self.load_config()
                with psycopg2.connect(**config) as conn:
                    with conn.cursor() as cur:
                        # Get the latest instrument_id and increment it
                        cur.execute("SELECT MAX(instrument_id) FROM case_mh_assessment_instrument")
                        max_id = cur.fetchone()[0] or 0
                        new_instrument_id = max_id + 1

                        # Insert the new assessment instrument
                        query = """
                            INSERT INTO case_mh_assessment_instrument (instrument_id, assessment_name)
                            VALUES (%s, %s)
                        """
                        cur.execute(query, (new_instrument_id, assessment_name))
                        conn.commit()

                # Show success message and close the popup
                messagebox.showinfo("Success", "New assessment instrument added successfully.")
                custom_popup.destroy()

            except Exception as error:
                print(f"Error adding new assessment instrument: {error}")
                messagebox.showerror("Database Error", "Failed to add new assessment instrument.")


        # Buttons for Save and Cancel
        ttk.Button(custom_popup, text="Save", command=save_new_assessment).grid(row=1, column=0, padx=10, pady=10, sticky="w")
        ttk.Button(custom_popup, text="Cancel", command=custom_popup.destroy).grid(row=1, column=1, padx=10, pady=10, sticky="w")

    def get_assessment_instruments(self):
        """Fetch available assessment instruments."""
        try:
            config = self.load_config()
            with psycopg2.connect(**config) as conn:
                with conn.cursor() as cur:
                    cur.execute("SELECT assessment_name FROM case_mh_assessment_instrument")
                    return [row[0] for row in cur.fetchall()]
        except Exception as error:
            print(f"Error fetching assessment instruments: {error}")
            return []

    def get_assessment_instrument_id(self, assessment_name):
        """Fetch assessment instrument ID by name."""
        try:
            config = self.load_config()
            with psycopg2.connect(**config) as conn:
                with conn.cursor() as cur:
                    cur.execute("SELECT instrument_id FROM case_mh_assessment_instrument WHERE assessment_name = %s", (assessment_name,))
                    result = cur.fetchone()
                    return result[0] if result else None
        except Exception as error:
            print(f"Error fetching assessment instrument ID: {error}")
            return None
        
    def get_assessment_instrument_name(self, instrument_id):
        """Fetches the assessment instrument name for a given instrument ID."""
        try:
            config = self.load_config()
            with psycopg2.connect(**config) as conn:
                with conn.cursor() as cur:
                    cur.execute(
                        "SELECT assessment_name FROM case_mh_assessment_instrument WHERE instrument_id = %s", 
                        (instrument_id,)
                    )
                    result = cur.fetchone()
                    return result[0] if result else None
        except Exception as error:
            print(f"Error fetching assessment instrument name for ID {instrument_id}: {error}")
            return None

    def get_timing_name(self, timing_id):
        """Maps timing ID to its corresponding string value."""
        timing_map = {
            1: "pre-treatment",
            2: "mid-treatment",
            3: "post-treatment"
        }
        return timing_map.get(timing_id, "Unknown")

    def generate_unique_id(self, table_name, column_name):
        """Generate a unique ID for a given table and column."""
        fake = Faker()
        config = self.load_config()
        while True:
            unique_id = fake.unique.random_number(digits=9)
            try:
                with psycopg2.connect(**config) as conn:
                    with conn.cursor() as cur:
                        cur.execute(f"SELECT 1 FROM {table_name} WHERE {column_name} = %s", (unique_id,))
                        if not cur.fetchone():
                            return unique_id
            except Exception as error:
                print(f"Error generating unique ID: {error}")
                return None
            
    def get_provider_agencies(self):
        """Fetches available provider agencies for the dropdown."""
        try:
            config = self.load_config()
            with psycopg2.connect(**config) as conn:
                with conn.cursor() as cur:
                    cur.execute("SELECT agency_name FROM cac_agency")
                    return [str(row[0]) for row in cur.fetchall()]
        except Exception as error:
            print(f"Error fetching provider agencies: {error}")
            return []

    def get_cac_id_by_agency(self, agency_name):
        """Fetches the CAC ID for a given agency name."""
        try:
            # Load the database configuration
            config = self.load_config()
            with psycopg2.connect(**config) as conn:
                with conn.cursor() as cur:
                    # Execute the query to fetch the CAC ID
                    cur.execute("SELECT cac_id FROM cac_agency WHERE agency_name = %s", (agency_name,))
                    result = cur.fetchone()
                    print(f"Fetching CAC ID for agency '{agency_name}': {result[0] if result else 'None'}")
                    return result[0] if result else None
        except Exception as error:
            print(f"Error fetching CAC ID for agency '{agency_name}': {error}")
            return None

        
    def get_agency_id_by_name(self, agency_name):
        """Fetches the Agency ID for a given agency name."""
        try:
            # Load the database configuration
            config = self.load_config()
            with psycopg2.connect(**config) as conn:
                with conn.cursor() as cur:
                    # Execute the query to fetch the Agency ID
                    cur.execute("SELECT agency_id FROM cac_agency WHERE agency_name = %s", (agency_name,))
                    result = cur.fetchone()
                    print(f"Fetching Agency ID for agency '{agency_name}': {result[0] if result else 'None'}")
                    return result[0] if result else None
        except Exception as error:
            print(f"Error fetching Agency ID for agency '{agency_name}': {error}")
            return None
        
    def get_agency_name_by_id(self, agency_id):
        """Fetches the Agency Name for a given agency ID."""
        try:
            # Load the database configuration
            config = self.load_config()
            with psycopg2.connect(**config) as conn:
                with conn.cursor() as cur:
                    # Execute the query to fetch the Agency Name
                    cur.execute("SELECT agency_name FROM cac_agency WHERE agency_id = %s", (agency_id,))
                    result = cur.fetchone()
                    print(f"Fetching Agency Name for agency ID '{agency_id}': {result[0] if result else 'None'}")
                    return result[0] if result else "Unknown"
        except Exception as error:
            print(f"Error fetching Agency Name for agency ID '{agency_id}': {error}")
            return "Unknown"
        
    def refresh_logs(self):
        """Refreshes the logs for assessments and diagnosis."""
        for widget in self.assessments_frame.winfo_children():
            widget.destroy()
        for widget in self.diagnosis_frame.winfo_children():
            widget.destroy()

        # Re-add column headers
        ttk.Label(self.assessments_frame, text="Assessment Instrument Name").grid(row=1, column=0, padx=5, pady=5)
        ttk.Label(self.assessments_frame, text="Timing").grid(row=1, column=1, padx=5, pady=5)
        ttk.Label(self.assessments_frame, text="Session Date").grid(row=1, column=2, padx=5, pady=5)

        ttk.Label(self.diagnosis_frame, text="MH Provider Agency").grid(row=1, column=0, padx=5, pady=5)
        ttk.Label(self.diagnosis_frame, text="Diagnosis Date").grid(row=1, column=1, padx=5, pady=5)

        # Re-fetch data
        self.load_assessments()
        self.load_diagnoses()
    
    def load_assessments(self):
        """Fetch and display assessments in the log."""
        try:
            config = self.load_config()
            with psycopg2.connect(**config) as conn:
                with conn.cursor() as cur:
                    query = "SELECT assessment_instrument_id, timing_id, session_date FROM case_mh_assessment"
                    cur.execute(query)
                    assessments = cur.fetchall()

                    for index, assessment in enumerate(assessments, start=2):
                        instrument_name = self.get_assessment_instrument_name(assessment[0])
                        timing_name = self.get_timing_name(assessment[1])

                        ttk.Label(self.assessments_frame, text=instrument_name or "Unknown").grid(row=index*2-1, column=0, padx=5, pady=5)
                        ttk.Label(self.assessments_frame, text=timing_name).grid(row=index*2-1, column=1, padx=5, pady=5)
                        ttk.Label(self.assessments_frame, text=str(assessment[2])).grid(row=index*2-1, column=2, padx=5, pady=5)
        except Exception as error:
            print(f"Error fetching assessments: {error}")

    def load_diagnoses(self):
        """Fetch and display diagnoses in the log."""
        try:
            config = self.load_config()
            with psycopg2.connect(**config) as conn:
                with conn.cursor() as cur:
                    query = "SELECT mh_provider_agency_id, diagnosis_date FROM case_mh_assessment_diagnosis"
                    cur.execute(query)
                    diagnoses = cur.fetchall()

                    for index, diagnosis in enumerate(diagnoses, start=2):
                        agency_name = self.get_agency_name_by_id(diagnosis[0])

                        ttk.Label(self.diagnosis_frame, text=agency_name).grid(row=index*2-1, column=0, padx=5, pady=5)
                        ttk.Label(self.diagnosis_frame, text=str(diagnosis[1])).grid(row=index*2-1, column=1, padx=5, pady=5)

                        ttk.Separator(self.diagnosis_frame, orient="horizontal").grid(row=index*2, column=0, columnspan=2, sticky="ew", pady=5)
        except Exception as error:
            print(f"Error fetching diagnosis log: {error}")


    def save_assessment(self, assessment_id, cac_id, case_id, agency_id, mh_provider_agency_id, assessment_instrument_id,
                        provider_employee_id, timing_id, session_date, assessment_date, comments):
        """Insert a new record into case_mh_assessment."""
        try:
            # Load the database configuration
            config = self.load_config()
            with psycopg2.connect(**config) as conn:
                with conn.cursor() as cur:
                    query = """
                        INSERT INTO case_mh_assessment (assessment_id, cac_id, case_id, agency_id, mh_provider_agency_id, 
                            assessment_instrument_id, provider_employee_id, timing_id, session_date, assessment_date, comments)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    """
                    cur.execute(query, (
                        assessment_id, cac_id, case_id, agency_id, mh_provider_agency_id, assessment_instrument_id,
                        provider_employee_id, timing_id, session_date, assessment_date, comments
                    ))
                    conn.commit()
                    messagebox.showinfo("Success", "Assessment added successfully.")
        except Exception as error:
            print(f"Error saving assessment: {error}")
            messagebox.showerror("Error", "Failed to save the assessment.")



    def save_score(self, score_id, cac_id, case_id, assessment_id, instrument_id, scores):
        """Insert a new record into case_mh_assessment_measure_scores."""
        try:
            config = self.load_config()
            with psycopg2.connect(**config) as conn:
                with conn.cursor() as cur:
                    query = """
                        INSERT INTO case_mh_assessment_measure_scores (score_id, cac_id, case_id, assessment_id, instrument_id, mh_assessment_scores)
                        VALUES (%s, %s, %s, %s, %s, %s)
                    """
                    cur.execute(query, (score_id, cac_id, case_id, assessment_id, instrument_id, scores))
                    conn.commit()
                    messagebox.showinfo("Success", "Scores added successfully.")
        except Exception as error:
            print(f"Error saving scores: {error}")


    def add_diagnosis_popup(self):
        popup = tk.Toplevel(self)
        popup.title("Add Diagnosis")
        popup.geometry("400x400+100+100")

        # Add some padding at the top using an empty label or adjust the grid padding
        ttk.Label(popup).grid(row=0, column=0, padx=10, pady=10)  # Empty label for spacing

        # Provider Agency Dropdown
        ttk.Label(popup, text="Provider Agency").grid(row=1, column=0, padx=10, pady=5, sticky="w")
        provider_agency_var = tk.StringVar()
        provider_agency_entry = ttk.Combobox(popup, textvariable=provider_agency_var, 
                                            values=self.get_provider_agencies(), width=40)
        provider_agency_entry.grid(row=1, column=1, padx=10, pady=5)

        # Diagnosis Date
        ttk.Label(popup, text="Diagnosis Date").grid(row=2, column=0, padx=10, pady=5, sticky="w")
        diagnosis_date_entry = DateEntry(popup, width=18)
        diagnosis_date_entry.grid(row=2, column=1, padx=10, pady=5)

        # Case ID
        ttk.Label(popup, text="Case ID").grid(row=3, column=0, padx=10, pady=5, sticky="w")
        case_id_var = tk.StringVar()
        case_id_entry = ttk.Entry(popup, textvariable=case_id_var, width=40)
        case_id_entry.grid(row=3, column=1, padx=10, pady=5)

        # Personnel ID
        ttk.Label(popup, text="Provider Employee ID").grid(row=4, column=0, padx=10, pady=5, sticky="w")
        personnel_id_var = tk.StringVar()
        personnel_id_entry = ttk.Entry(popup, textvariable=personnel_id_var, width=40)
        personnel_id_entry.grid(row=4, column=1, padx=10, pady=5)

        # ICD 10 Group Dropdown
        ttk.Label(popup, text="ICD 10 Group").grid(row=5, column=0, padx=10, pady=5, sticky="w")
        icd10_group_entry = ttk.Combobox(popup, values=["ICD Group A", "ICD Group B", "ICD Group C"], width=40)
        icd10_group_entry.grid(row=5, column=1, padx=10, pady=5)

        def save_diagnosis():
                """Save diagnosis to the case_mh_assessment_diagnosis table."""
                provider_agency_name = provider_agency_var.get()
                diagnosis_date = diagnosis_date_entry.get_date()
                case_id = case_id_var.get().strip()

                if not provider_agency_name or not case_id:
                    messagebox.showerror("Error", "All fields must be filled out.")
                    return

                try:
                    # Get the mh_provider_agency_id for the selected provider
                    mh_provider_agency_id = self.get_agency_id_by_name(provider_agency_name)

                    # Insert into the database
                    config = self.load_config()
                    with psycopg2.connect(**config) as conn:
                        with conn.cursor() as cur:
                            query = """
                                INSERT INTO case_mh_assessment_diagnosis (case_id, diagnosis_date, mh_provider_agency_id)
                                VALUES (%s, %s, %s)
                            """
                            cur.execute(query, (case_id, diagnosis_date, mh_provider_agency_id))
                            conn.commit()

                    messagebox.showinfo("Success", "Diagnosis added successfully.")
                    popup.destroy()
                except Exception as error:
                    print(f"Error saving diagnosis: {error}")
                    messagebox.showerror("Error", "An error occurred while saving the diagnosis.")
        
        # Save and Cancel buttons
        ttk.Button(popup, text="Save", command=save_diagnosis).grid(row=6, column=0, padx=10, pady=10, sticky="w")
        ttk.Button(popup, text="Cancel", command=popup.destroy).grid(row=6, column=1, padx=10, pady=10, sticky="e")
