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

class MH_treatment_plan_interface(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        
        # Configure layout for navigation buttons and main canvas
        self.grid_rowconfigure(2, weight=1)
        self.grid_columnconfigure(0, weight=1)
        
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
                            command=lambda: controller.show_frame(MH_treatment_plan_interface))
        button5.grid(row=0, column=4, padx=5, pady=5)

        button6 = ttk.Button(self, text="VA", 
                            command=lambda: controller.show_frame(va_tab_interface.va_interface))
        button6.grid(row=0, column=5, padx=5, pady=5)
        
        button7 = ttk.Button(self, text="Case Notes", 
                            command=lambda: controller.show_frame(case_notes.case_notes_interface))
        button7.grid(row=0, column=6, padx=5, pady=5)

        # Setup scrollable canvas for the main content
        canvas = tk.Canvas(self)
        scrollbar = ttk.Scrollbar(self, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.grid(row=2, column=0, sticky="nsew")
        scrollbar.grid(row=2, column=1, sticky="ns")

        # Database connection
        self.conn = self.connect_to_db()

        # Function to open file dialog and set the filename
        def select_file():
            file_path = filedialog.askopenfilename(title="Select a file", filetypes=[("All files", "*.*")])
            if file_path:
                file_name_var.set(file_path.split("/")[-1])  # Set the filename in the entry

        # Treatment Plans Section
        treatment_frame = tk.LabelFrame(scrollable_frame, text="Treatment Plans", padx=10, pady=10)
        treatment_frame.pack(fill="x", padx=10, pady=5)
        ttk.Button(treatment_frame, text="+ Add New Treatment Plan", command=self.add_treatment_plan_popup).grid(row=0, column=0, padx=5, pady=5)

        # Document Upload Section
        upload_frame = tk.LabelFrame(scrollable_frame, text="Document Upload", padx=10, pady=10)
        upload_frame.pack(fill="x", padx=10, pady=5)
        ttk.Label(upload_frame, text="File Name:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        file_name_var = tk.StringVar()
        file_name_entry = ttk.Entry(upload_frame, textvariable=file_name_var, width=50, state="readonly")
        file_name_entry.grid(row=0, column=1, padx=5, pady=5)
        ttk.Button(upload_frame, text="Select Files...", command=select_file).grid(row=0, column=2, padx=5, pady=5)
        ttk.Label(upload_frame, text="Maximum allowed file size is 10 MB.").grid(row=1, column=0, columnspan=3, padx=5, pady=5)

    def connect_to_db(self):
        """Establishes a connection to the database."""
        try:
            config = configparser.ConfigParser()
            config.read('/Users/danieljacob/Desktop/Capstone_temp/NCATrak-Mock-System/app/database/database.ini')
            db_params = {
                'database': config['postgresql']['database'],
                'user': config['postgresql']['user'],
                'password': config['postgresql']['password'],
                'host': config['postgresql']['host'],
                # 'port': config['postgresql']['port']
            }
            return psycopg2.connect(**db_params)
        except Exception as error:
            print(f"Database connection error: {error}")
            messagebox.showerror("Database Error", "Could not connect to the database.")
            return None

    def get_treatment_models(self):
        """Fetches available treatment models for the dropdown."""
        try:
            with self.conn.cursor() as cur:
                cur.execute("SELECT id, model_name FROM case_mh_treatment_models")
                return [f"{row[0]} - {row[1]}" for row in cur.fetchall()]
        except Exception as error:
            print(f"Error fetching treatment models: {error}")
            return []

    def get_provider_agencies(self):
        """Fetches available provider agencies for the dropdown."""
        try:
            with self.conn.cursor() as cur:
                cur.execute("SELECT agency_name FROM cac_agency")
                return [str(row[0]) for row in cur.fetchall()]
        except Exception as error:
            print(f"Error fetching provider agencies: {error}")
            return []
    def save_treatment_plan(self, model_id, agency_id, cac_id, start_date, end_date, case_id, 
                        authorized_status_id, duration, duration_unit, planned_review_date):
        """Saves a new treatment plan into the database with a randomly generated unique ID."""
        fake = Faker()
        fake.seed_instance(0)  # Ensure consistent results if needed

        try:
            with self.conn.cursor() as cur:
                while True:
                    # Generate a random unique ID
                    random_id = fake.unique.random_number(digits=9)

                    # Check if the ID already exists in the database
                    cur.execute("SELECT 1 FROM case_mh_treatment_plans WHERE id = %s", (random_id,))
                    if cur.fetchone() is None:
                        # If the ID is unique, proceed to insert the new record
                        insert_query = """
                            INSERT INTO case_mh_treatment_plans 
                            (id, treatment_model_id, provider_agency_id, cac_id, planned_start_date, planned_end_date, 
                            case_id, authorized_status_id, duration, duration_unit, planned_review_date)
                            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                        """
                        cur.execute(insert_query, (
                            random_id, model_id, agency_id, cac_id, start_date, end_date, case_id, 
                            authorized_status_id, duration, duration_unit, planned_review_date
                        ))
                        self.conn.commit()
                        messagebox.showinfo("Success", "Treatment plan added successfully.")
                        break  # Exit the loop after successful insertion

        except Exception as error:
            print(f"Error saving treatment plan: {error}")
            messagebox.showerror("Error", "Failed to save the treatment plan.")
            self.conn.rollback()

    def add_treatment_model_popup(self):
        """Popup for adding a new treatment model."""
        popup = tk.Toplevel(self)
        popup.title("Add Treatment Model")
        popup.geometry("300x200")

        # Treatment Model Name Entry
        ttk.Label(popup, text="Treatment Model Name").grid(row=0, column=0, padx=10, pady=10, sticky="w")
        model_name_var = tk.StringVar()
        model_name_entry = ttk.Entry(popup, textvariable=model_name_var, width=30)
        model_name_entry.grid(row=0, column=1, padx=10, pady=10)

        def save_treatment_model():
            model_name = model_name_var.get().strip()

            if not model_name:
                messagebox.showerror("Error", "Model name cannot be empty.")
                return

            try:
                with self.conn.cursor() as cur:
                    # Get the latest ID and increment it
                    cur.execute("SELECT MAX(id) FROM case_mh_treatment_models")
                    max_id = cur.fetchone()[0]
                    new_id = (max_id + 1) if max_id else 1

                    # Insert the new treatment model
                    query = "INSERT INTO case_mh_treatment_models (id, model_name) VALUES (%s, %s)"
                    cur.execute(query, (new_id, model_name))
                    self.conn.commit()

                messagebox.showinfo("Success", "Treatment model added successfully.")
                popup.destroy()

            except Exception as error:
                print(f"Error saving treatment model: {error}")
                self.conn.rollback()
                messagebox.showerror("Error", "Failed to add treatment model.")

        # Save and Cancel Buttons
        ttk.Button(popup, text="Save", command=save_treatment_model).grid(row=2, column=0, padx=10, pady=10)
        ttk.Button(popup, text="Cancel", command=popup.destroy).grid(row=2, column=1, padx=10, pady=10)

            
    def add_treatment_plan_popup(self):
        """Popup window for adding a new treatment plan."""
        popup = tk.Toplevel(self)
        popup.title("New Treatment Plan")
        popup.geometry("400x450") 

        # Plan Date
        ttk.Label(popup, text="Plan Date").grid(row=0, column=0, padx=10, pady=5, sticky="w")
        plan_date_entry = DateEntry(popup, width=20)
        plan_date_entry.grid(row=0, column=1, padx=10, pady=5)

        # Treatment Model
        ttk.Label(popup, text="Treatment Model").grid(row=1, column=0, padx=10, pady=5, sticky="w")
        treatment_model_var = tk.StringVar()
        treatment_model_dropdown = ttk.Combobox(popup, textvariable=treatment_model_var, values=self.get_treatment_models(), width=40)
        treatment_model_dropdown.grid(row=1, column=1, padx=(10, 0), pady=5, sticky="w")
        
        ## add button for treatment model
        ttk.Button(popup, text="Add", command=self.add_treatment_model_popup).grid(row=1, column=2, padx=5, pady=5)


        # Provider Agency
        ttk.Label(popup, text="Provider Agency").grid(row=2, column=0, padx=10, pady=5, sticky="w")
        provider_agency_var = tk.StringVar()
        provider_agency_dropdown = ttk.Combobox(popup, textvariable=provider_agency_var, values=self.get_provider_agencies(), width=40)
        provider_agency_dropdown.grid(row=2, column=1, padx=(10, 0), pady=5, sticky="w")

        # Planned Start Date
        ttk.Label(popup, text="Planned Start Date").grid(row=4, column=0, padx=10, pady=5, sticky="w")
        start_date_entry = DateEntry(popup, width=20)
        start_date_entry.grid(row=4, column=1, padx=10, pady=5)

        # Planned End Date
        ttk.Label(popup, text="Planned End Date").grid(row=5, column=0, padx=10, pady=5, sticky="w")
        end_date_entry = DateEntry(popup, width=20)
        end_date_entry.grid(row=5, column=1, padx=10, pady=5)
        
        # Case ID
        ttk.Label(popup, text="Case ID").grid(row=6, column=0, padx=10, pady=5, sticky="w")
        case_id_entry = ttk.Entry(popup, width=40)
        case_id_entry.grid(row=6, column=1, padx=10, pady=5)
        
        # Authorized Status
        ttk.Label(popup, text="Authorized Status").grid(row=7, column=0, padx=10, pady=5, sticky="w")
        authorized_status_var = tk.StringVar()
        status_mapping = {
            "Approved": 1,
            "Authorized": 2,
            "Cancelled": 3,
            "Rejected": 4,
            "Denied": 5,
            "In Progress": 6,
            "Not Needed": 7
        }
        authorized_status_dropdown = ttk.Combobox(popup, textvariable=authorized_status_var, values=list(status_mapping.keys()), width=40)
        authorized_status_dropdown.grid(row=7, column=1, padx=10, pady=5)
        
        # Duration
        ttk.Label(popup, text="Duration").grid(row=8, column=0, padx=10, pady=5, sticky="w")
        duration_var = tk.StringVar()
        duration_entry = ttk.Entry(popup, textvariable=duration_var, width=40)
        duration_entry.grid(row=8, column=1, padx=10, pady=5)

        # Duration Unit
        ttk.Label(popup, text="Duration Unit").grid(row=9, column=0, padx=10, pady=5, sticky="w")
        duration_unit_var = tk.StringVar()
        duration_unit_dropdown = ttk.Combobox(popup, textvariable=duration_unit_var, values=["days", "weeks", "months"], width=40)
        duration_unit_dropdown.grid(row=9, column=1, padx=10, pady=5)

        # Planned Review Date
        ttk.Label(popup, text="Planned Review Date").grid(row=10, column=0, padx=10, pady=5, sticky="w")
        planned_review_date_entry = DateEntry(popup, width=20)
        planned_review_date_entry.grid(row=10, column=1, padx=10, pady=5)
 
        def save_action():
            model_id = int(treatment_model_var.get().split(" - ")[0])  # Extract ID from "ID - Name" format
            agency_name = provider_agency_var.get()
            agency_id = self.get_agency_id_by_name(agency_name)  # Fetch agency_id based on selected agency name
            cac_id = self.get_cac_id_by_agency(agency_name)  # Fetch cac_id based on selected agency name
            case_id = case_id_entry.get().strip()
            # authorized_status_id = int(authorized_status_var.get())
            selected_status = authorized_status_var.get()
            authorized_status_id = status_mapping.get(selected_status, None)  # Map text to corresponding integer
            
            if authorized_status_id is None:
                messagebox.showerror("Error", "Invalid authorized status selected.")
                return
            
            duration = int(duration_var.get().strip())
            duration_unit = duration_unit_var.get()
            planned_review_date = planned_review_date_entry.get_date()
            
            self.save_treatment_plan(
                model_id, agency_id, cac_id, start_date_entry.get_date(), end_date_entry.get_date(),
                case_id, authorized_status_id, duration, duration_unit, planned_review_date
            )
            popup.destroy()
        
        ttk.Button(popup, text="Update", command=save_action).grid(row=12, column=0, padx=5, pady=5)
        ttk.Button(popup, text="Cancel", command=popup.destroy).grid(row=12, column=1, padx=5, pady=5)
    
    def get_cac_id_by_agency(self, agency_name):
        """Fetches the CAC ID for a given agency name."""
        try:
            with self.conn.cursor() as cur:
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
            with self.conn.cursor() as cur:
                cur.execute("SELECT agency_id FROM cac_agency WHERE agency_name = %s", (agency_name,))
                result = cur.fetchone()
                print(f"Fetching Agency ID for agency '{agency_name}': {result[0] if result else 'None'}")
                return result[0] if result else None
        except Exception as error:
            print(f"Error fetching Agency ID for agency '{agency_name}': {error}")
            return None





