import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkcalendar import DateEntry
import Generaltab_interface
import MH_basic_interface
import people_interface
import MH_assessment
import MH_treatmentPlan_interface
import va_tab_interface
import case_notes
from database.config import load_config
from database.connect import connect

heading_font = ("Helvetica", 18, "bold")
bold_label_font = ("Helvetica", 12, "bold")
normal_text_font = ("Helvetica", 12)
entry_width = 30

padx = 10
pady = 5

religions = [
    "Christianity",
    "Islam",
    "Judaism",
    "Hinduism",
    "Buddhism",
    "Sikhism",
    "Jainism",
    "Atheist/Agnostic",
    "Other"
]

languages = [
    "English",
    "Spanish",
    "French",
    "German",
    "Portuguese",
    "Russian",
    "Arabic",
    "Turkish",
    "Hindi",
    "Urdu",
    "Chinese",
    "Japanese",
    "Vietnamese",
    "Korean",
    "Other"
]

races = [
    "Asian",
    "American Indian",
    "Biracial",
    "Biracial - African-American/White",
    "Biracial - Hispanic/White",
    "Black/African-American",
    "White",
    "Hispanic",
    "Native Hawaiian/Other Pacific Islander",
    "Alaska Native",
    "Multiple Races",
    "Not Reported",
    "Not Tracked"
]

case_roles = [
    "Alleged Victim/Client",
    "Alleged Co-Victim",
    "Alleged Offender",
    "Caregiver",
    "Other"
]

relationships_to_victim = [
    "Self",
    "Mother",
    "Biological Mother",
    "Adoptive Mother",
    "Step-Mother",
    "Father's Girlfriend",
    "Father",
    "Biological Father",
    "Adoptive Father",
    "Step-Father",
    "Mother's Boyfriend",
    "Brother",
    "Sister",
    "Step-Brother",
    "Step-Sister",
    "Adoptive Brother",
    "Adoptive Sister",
    "Grandmother",
    "Grandfather",
    "Friend",
    "Other Known Person"
]

class lookup_interface(tk.Frame):
    
    def __init__(self, parent, controller):
        
        self.controller = controller

        tk.Frame.__init__(self, parent)
        
        self.grid_rowconfigure(2, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Create a canvas and a scrollbar
        canvas = tk.Canvas(self)
        scrollbar = ttk.Scrollbar(self, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        # label = ttk.Label(self, text="back to main page", font = ("Verdana", 35))
        # label.grid(row = 0, column=0, padx = 5, pady = 5)

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

        # Create a window in the canvas
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")

        # Link scrollbar to the canvas
        canvas.configure(yscrollcommand=scrollbar.set)

        # Use grid over pack for interface linking
        canvas.grid(row=2, column=0, sticky="nsew")
        scrollbar.grid(row=2, column=1, sticky="ns")

        self.patient_data = self.load_first_100_patients()
        self.filtered_patients = self.patient_data  # Initialize filtered_patients

        # creates frame for search and patient list
        search_frame = tk.Frame(scrollable_frame)
        search_frame.grid(row=1, column=0, padx=20, pady=20)

        # create search entry
        tk.Label(search_frame, text="Search Patient:", font=bold_label_font).grid(row=1, column=0, padx=padx, pady=pady)
        self.search_entry = tk.Entry(search_frame, font=normal_text_font, width=entry_width)
        self.search_entry.grid(row=1, column=1, padx=padx, pady=pady)
        self.search_entry.bind("<KeyRelease>", self.search_patients)

        # creates a listbox to display search results
        self.patient_list = tk.Listbox(search_frame, width=entry_width * 2, height=10, font=normal_text_font)
        self.patient_list.grid(row=2, column=0, columnspan=2, padx=padx, pady=pady)

        # creates frame for patient details
        self.details_frame = tk.Frame(scrollable_frame)
        self.details_frame.grid(row=2, column=0, columnspan=3, padx=20, pady=20)
        canvas = tk.Canvas(self.details_frame)
        scrollbar = ttk.Scrollbar(self.details_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(self.details_frame)

    def get_religion(self, id):
        if id is not None:
            return religions[id]
        else:
            return ""
        
    def get_race(self, id):
        if id is not None:
            return races[id]
        else:
            return ""
        
    def get_language(self, id):
        if id is not None:
            return languages[id]
        else:
            return ""

    def get_relationship(self, id):
        if id is not None:
            return relationships_to_victim[id]
        else:
            return "Not Listed"

    def get_role(self, id):
        if id is not None:
            return case_roles[id]
        else:
            return "Not Listed"

    def load_first_100_patients(self):

        patient_data = []
        config = load_config(filename="database.ini")
        conn = connect(config)
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM person ORDER BY last_name FETCH FIRST 100 ROWS ONLY") 
            row = cur.fetchone()
                    
            while row is not None:
                patient_data.append(row)
                row = cur.fetchone()

            return patient_data
        
    # to populate the details of the selected patient
    def show_patient_details(self, patient):
        # Clear previous patient details
        for widget in self.details_frame.winfo_children():
            widget.destroy()

        tk.Label(self.details_frame, text="First Name:", font=bold_label_font).grid(column=0, row=0, sticky="e", padx=padx, pady=pady)
        tk.Label(self.details_frame, text=patient[2], font=normal_text_font).grid(column=1, row=0, sticky="w", padx=padx, pady=pady)

        tk.Label(self.details_frame, text="Last Name:", font=bold_label_font).grid(column=0, row=1, sticky="e", padx=padx, pady=pady)
        tk.Label(self.details_frame, text=patient[4], font=normal_text_font).grid(column=1, row=1, sticky="w", padx=padx, pady=pady)

        tk.Label(self.details_frame, text="Middle Name:", font=bold_label_font).grid(column=0, row=2, sticky="e", padx=padx, pady=pady)
        tk.Label(self.details_frame, text=patient[3], font=normal_text_font).grid(column=1, row=2, sticky="w", padx=padx, pady=pady)

        tk.Label(self.details_frame, text="Date of Birth:", font=bold_label_font).grid(column=0, row=4, sticky="e", padx=padx, pady=pady)
        tk.Label(self.details_frame, text=patient[6], font=normal_text_font).grid(column=1, row=4, sticky="w", padx=padx, pady=pady)

        tk.Label(self.details_frame, text="Race:", font=bold_label_font).grid(column=0, row=5, sticky="e", padx=padx, pady=pady)
        tk.Label(self.details_frame, text=self.get_race(patient[9]), font=normal_text_font).grid(column=1, row=5, sticky="w", padx=padx, pady=pady)

        tk.Label(self.details_frame, text="Gender:", font=bold_label_font).grid(column=0, row=6, sticky="e", padx=padx, pady=pady)
        tk.Label(self.details_frame, text=patient[7], font=normal_text_font).grid(column=1, row=6, sticky="w", padx=padx, pady=pady)

        tk.Label(self.details_frame, text="Religion:", font=bold_label_font).grid(column=0, row=7, sticky="e", padx=padx, pady=pady)
        tk.Label(self.details_frame, text=self.get_religion(patient[10]), font=normal_text_font).grid(column=1, row=7, sticky="w", padx=padx, pady=pady)

        tk.Label(self.details_frame, text="Language:", font=bold_label_font).grid(column=0, row=8, sticky="e", padx=padx, pady=pady)
        tk.Label(self.details_frame, text=self.get_language(patient[8]), font=normal_text_font).grid(column=1, row=8, sticky="w", padx=padx, pady=pady)

        tk.Label(self.details_frame, text="Prior Convictions:", font=bold_label_font).grid(column=2, row=0, sticky="e", padx=padx, pady=pady)
        tk.Label(self.details_frame, text="Yes" if patient[11] else "No", font=normal_text_font).grid(column=3, row=0, sticky="w", padx=padx, pady=pady)

        tk.Label(self.details_frame, text="Convicted of Crimes Against Children:", font=bold_label_font).grid(column=2, row=1, sticky="e", padx=padx, pady=pady)
        tk.Label(self.details_frame, text="Yes" if patient[12] else "No", font=normal_text_font).grid(column=3, row=1, sticky="w", padx=padx, pady=pady)

        tk.Label(self.details_frame, text="Sexual Offender:", font=bold_label_font).grid(column=2, row=2, sticky="e", padx=padx, pady=pady)
        tk.Label(self.details_frame, text="Yes" if patient[13] else "No", font=normal_text_font).grid(column=3, row=2, sticky="w", padx=padx, pady=pady)

        tk.Label(self.details_frame, text="Sexual Predator:", font=bold_label_font).grid(column=2, row=3, sticky="e", padx=padx, pady=pady)
        tk.Label(self.details_frame, text="Yes" if patient[14] else "No", font=normal_text_font).grid(column=3, row=3, sticky="w", padx=padx, pady=pady)

        # creates a listbox to display search results for cases
        tk.Label(self.details_frame, text="Case ID\tRelationship to Victim\tRole\tAge\tSame Household?\tCustody?", font=bold_label_font).grid(column=0, row=10, sticky="e", padx=padx, pady=pady)
        cases_list = tk.Listbox(self.details_frame, width=entry_width * 4, height=10, font=normal_text_font)
        cases_list.grid(row=11, column=0, columnspan=5, padx=padx, pady=pady)

        # to search cases based on specific person
        def search_cases_by_patient(person_id, event=None):
            global filtered_cases
            config = load_config(filename="database.ini")
            conn = connect(config)

            search_query = self.search_entry.get().lower()
            filtered_cases = []

            with conn.cursor() as cur:
                cur.execute(f"SELECT * FROM case_person WHERE person_id={person_id} FETCH FIRST 100 ROWS ONLY".format(search_query))
                row = cur.fetchone()

                while row is not None:
                    filtered_cases.append(row)
                    row = cur.fetchone()

            update_cases_list(filtered_cases)

        #update the patient list based on search 
        def update_cases_list(filtered_cases):
            cases_list.delete(0, tk.END)
            for case in filtered_cases:
                cases_list.insert(tk.END, f"{case[1]}   {self.get_relationship(case[17])}   {self.get_role(case[18])}   {case[3]}   {case[19]}   {case[13]}")
            cases_list.bind("<Double-1>", on_case_select_from_list)

        # callback function when a patient is selected from the list
        def on_case_select_from_list(event):
            selected_index = cases_list.curselection()
            if selected_index:
                case_index = selected_index
                case_id = filtered_cases[case_index[0]][1]
                case_id_file = open("app/case_id.txt", "w")
                case_id_file.write(str(case_id))

        search_cases_by_patient(patient[1])

    # to filter patients based on search
    def search_patients(self, event=None):
        global filtered_patients
        config = load_config(filename="database.ini")
        conn = connect(config)

        search_query = self.search_entry.get().lower()
        filtered_patients = []

        with conn.cursor() as cur:
            cur.execute("SELECT * FROM person WHERE CONCAT(first_name, \' \', middle_name, \' \', last_name)~*\'{0}\' OR CONCAT(first_name, \' \', last_name)~*\'{0}\' ORDER BY last_name FETCH FIRST 100 ROWS ONLY".format(search_query))
            row = cur.fetchone()

            while row is not None:
                filtered_patients.append(row)
                row = cur.fetchone()

        self.update_patient_list(filtered_patients)

    #update the patient list based on search 
    def update_patient_list(self, filtered_patients):
        self.patient_list.delete(0, tk.END)
        for patient in filtered_patients:
            self.patient_list.insert(tk.END, f"{patient[2]} {patient[3]} {patient[4]}")
        self.patient_list.bind("<Double-1>", self.on_patient_select_from_list)

    # callback function when a patient is selected from the list
    def on_patient_select_from_list(self, event):
        selected_index = self.patient_list.curselection()
        if selected_index:
            patient_index = selected_index[0]
            self.show_patient_details(filtered_patients[patient_index])

    # -------------------- Navigation Functions --------------------
    def show_lookup_page(self):
        self.controller.show_frame(lookup_interface)

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
        self.controller.show_frame(va_tab_interface.va_interface)

    def show_case_notes(self):
        self.controller.show_frame(case_notes.case_notes_interface)

