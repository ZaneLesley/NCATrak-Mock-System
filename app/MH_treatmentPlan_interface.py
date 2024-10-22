import tkinter as tk
from tkinter import ttk
from tkcalendar import DateEntry
from tkinter import filedialog
import Generaltab_interface
import people_interface
import MH_basic_interface
import MH_assessment
import va_tab_interface
import sv_ttk

class MH_treatment_plan_interface(tk.Frame):

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
                            command=lambda: controller.show_frame(MH_treatment_plan_interface))
        button5.grid(row=0, column=4, padx=5, pady=5)

        button6 = ttk.Button(self, text="VA", 
                            command=lambda: controller.show_frame(va_tab_interface.va_interface))
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

        # Create a window in the canvas
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")

        # Link scrollbar to the canvas
        canvas.configure(yscrollcommand=scrollbar.set)

        # Use grid over pack for interface linking
        canvas.grid(row=2, column=0, sticky="nsew")
        scrollbar.grid(row=2, column=1, sticky="ns")

        # functoin to add a new treatment model
        def add_new_treatment_model():
            model_popup = tk.Toplevel(self)
            model_popup.title("Add New Treatment Model")
            model_popup.geometry("400x300") 

            # outputs existing models and descriptions
            ttk.Label(model_popup, text="Existing Treatment Models:").grid(row=0, column=0, columnspan=2, padx=10, pady=5, sticky="w")
            models_description = [
                ("Model A", "Description of Model A..."),
                ("Model B", "Description of Model B..."),
                ("Model C", "Description of Model C...")
            ]

            # displays existing models and descriptions
            for i, (model, desc) in enumerate(models_description, start=1):
                ttk.Label(model_popup, text=f"{model}: {desc}").grid(row=i, column=0, columnspan=2, padx=10, pady=2, sticky="w")

            # input new model
            ttk.Label(model_popup, text="New Treatment Model:").grid(row=i+1, column=0, padx=10, pady=5, sticky="w")
            new_model_entry = ttk.Entry(model_popup, width=30)
            new_model_entry.grid(row=i+1, column=1, padx=10, pady=5)

            # input intervention for new model
            ttk.Label(model_popup, text="Intervention:").grid(row=i+2, column=0, padx=10, pady=5, sticky="w")
            new_intervention_entry = ttk.Entry(model_popup, width=30)
            new_intervention_entry.grid(row=i+2, column=1, padx=10, pady=5)

            ttk.Button(model_popup, text="Save", command=model_popup.destroy).grid(row=i+3, column=0, padx=10, pady=10)
            ttk.Button(model_popup, text="Cancel", command=model_popup.destroy).grid(row=i+3, column=1, padx=10, pady=10)


        # Function to add new treatment plan 
        def add_treatment_plan_popup():
            # Create a new Toplevel window
            popup = tk.Toplevel(self)
            popup.title("New Treatment Plan")
            popup.geometry("400x400") 
            
            # plan date
            ttk.Label(popup, text="Plan Date").grid(row=0, column=0, padx=10, pady=5, sticky="w")
            plan_date_entry = DateEntry(popup, width=20)
            plan_date_entry.grid(row=0, column=1, padx=10, pady=5)

            # treatment model 
            ttk.Label(popup, text="Treatment Model").grid(row=1, column=0, padx=10, pady=5, sticky="w")
            treatment_model_entry = ttk.Combobox(popup, values=["Model A", "Model B", "Model C"], width=40)
            treatment_model_entry.grid(row=1, column=1, padx=(10, 0), pady=5, sticky="w")

            # add button next to treatmend model
            ttk.Button(popup, text="+ Add", command=add_new_treatment_model).grid(row=1, column=2, padx=(5, 10), pady=5, sticky="w")

            # provider agency
            ttk.Label(popup, text="Provider Agency").grid(row=2, column=0, padx=10, pady=5, sticky="w")
            provider_agency_entry = ttk.Combobox(popup, values=["Agency X", "Agency Y", "Agency Z"], width=40)
            provider_agency_entry.grid(row=2, column=1, columnspan=2, padx=(10, 0), pady=5, sticky="w")

            # therapist
            ttk.Label(popup, text="Therapist").grid(row=3, column=0, padx=10, pady=5, sticky="w")
            therapist_entry = ttk.Combobox(popup, values=["Therapist 1", "Therapist 2", "Therapist 3"], width=40)
            therapist_entry.grid(row=3, column=1, columnspan=2, padx=(10, 0), pady=5, sticky="w")

            # expected length of services
            ttk.Label(popup, text="Expected Length of Services").grid(row=4, column=0, padx=10, pady=5, sticky="w")

            # Spinbox for number input
            length_entry = ttk.Spinbox(popup, from_=0, to=100, increment=1, width=10)
            length_entry.grid(row=4, column=1, padx=(10, 5), pady=5, sticky="w")

            # Combobox for time unit (Days, Weeks, Months)
            time_unit_entry = ttk.Combobox(popup, values=["Days", "Weeks", "Months"], width=10)
            time_unit_entry.grid(row=4, column=2, padx=(0, 10), pady=5, sticky="w")


            # planned Start Date
            ttk.Label(popup, text="Planned Start").grid(row=5, column=0, padx=10, pady=5, sticky="w")
            start_date_entry = DateEntry(popup, width=20)
            start_date_entry.grid(row=5, column=1, padx=10, pady=5)

            # planned End Date
            ttk.Label(popup, text="Planned End").grid(row=6, column=0, padx=10, pady=5, sticky="w")
            end_date_entry = DateEntry(popup, width=20)
            end_date_entry.grid(row=6, column=1, padx=10, pady=5)

            # plan Review Date
            ttk.Label(popup, text="Plan Review Date").grid(row=7, column=0, padx=10, pady=5, sticky="w")
            review_date_entry = DateEntry(popup, width=20)
            review_date_entry.grid(row=7, column=1, padx=10, pady=5)

            # authorization status 
            ttk.Label(popup, text="Authorization Status").grid(row=8, column=0, padx=10, pady=5, sticky="w")
            auth_status_entry = ttk.Combobox(popup, values=["Approved", "Authorized", "Cancelled", "Rejected", "Denied", "In Progress", "Not Needed"], width=47)
            auth_status_entry.grid(row=8, column=1, padx=10, pady=5)

            # session notes 
            ttk.Label(popup, text="Session Notes").grid(row=9, column=0, padx=10, pady=5, sticky="w")
            session_notes_entry = tk.Text(popup, height=4, width=50)
            session_notes_entry.grid(row=9, column=1, padx=10, pady=5)

            # treatment plan Goals/Progress 
            ttk.Label(popup, text="Treatment Plan Goals/Progress").grid(row=10, column=0, padx=10, pady=5, sticky="w")
            goals_entry = tk.Text(popup, height=4, width=50)
            goals_entry.grid(row=10, column=1, padx=10, pady=5)

            # privacy forms distributed
            ttk.Label(popup, text="Privacy Forms Distributed").grid(row=11, column=0, padx=10, pady=5, sticky="w")
            privacy_frame = tk.Frame(popup)
            privacy_frame.grid(row=11, column=1, padx=10, pady=5, sticky="w")
            ttk.Checkbutton(privacy_frame, text="HIPAA").pack(anchor='w')
            ttk.Checkbutton(privacy_frame, text="Agency Disclosure").pack(anchor='w')
            ttk.Checkbutton(privacy_frame, text="MDT Procedural").pack(anchor='w')
            ttk.Checkbutton(privacy_frame, text="Right to Privacy").pack(anchor='w')
            ttk.Checkbutton(privacy_frame, text="Chaperones").pack(anchor='w')

            # consents obtained
            ttk.Label(popup, text="Consents Obtained").grid(row=12, column=0, padx=10, pady=5, sticky="w")
            consent_frame = tk.Frame(popup)
            consent_frame.grid(row=12, column=1, padx=10, pady=5, sticky="w")
            ttk.Checkbutton(consent_frame, text="Parent").pack(anchor='w')
            ttk.Checkbutton(consent_frame, text="Guardian").pack(anchor='w')
            ttk.Checkbutton(consent_frame, text="G. Ad Litem").pack(anchor='w')
            ttk.Checkbutton(consent_frame, text="CPS").pack(anchor='w')
            ttk.Checkbutton(consent_frame, text="District Attorney").pack(anchor='w')

            ttk.Button(popup, text="Update", command=popup.destroy).grid(row=13, column=0, padx=10, pady=10)
            ttk.Button(popup, text="Cancel", command=popup.destroy).grid(row=13, column=1, padx=10, pady=10)

        # treatment plans section that will print out current ones
        treatment_frame = tk.LabelFrame(scrollable_frame, text="Treatment Plans", padx=10, pady=10)
        treatment_frame.pack(fill="x", padx=10, pady=5)

        # nutton to add a new treatment plan which calls the function above
        ttk.Button(treatment_frame, text="+ Add New Treatment Plan", command=add_treatment_plan_popup).grid(row=0, column=0, padx=5, pady=5)

        ttk.Label(treatment_frame, text="Action").grid(row=1, column=0, padx=5, pady=5)
        ttk.Label(treatment_frame, text="Plan Date").grid(row=1, column=1, padx=5, pady=5)
        ttk.Label(treatment_frame, text="Treatment Model").grid(row=1, column=2, padx=5, pady=5)
        ttk.Label(treatment_frame, text="Provider Agency").grid(row=1, column=3, padx=5, pady=5)
        ttk.Label(treatment_frame, text="Therapist").grid(row=1, column=4, padx=5, pady=5)


        # # document upload section
        # upload_frame = tk.LabelFrame(scrollable_frame, text="Document Upload", padx=10, pady=10)
        # upload_frame.pack(fill="x", padx=10, pady=5)

        # ttk.Label(upload_frame, text="File Name:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        # file_name_var = tk.StringVar()  # Variable to hold the filename
        # file_name_entry = ttk.Entry(upload_frame, textvariable=file_name_var, width=50, state="readonly")
        # file_name_entry.grid(row=0, column=1, padx=5, pady=5)

        # # Function to open file dialog and set the filename
        # def select_file():
        #     file_path = tk.filedialog.askopenfilename(title="Select a file", filetypes=[("All files", "*.*")])
        #     if file_path:  # If a file is selected
        #         file_name_var.set(file_path.split("/")[-1])  # Set the filename in the entry

        # # Button to trigger file selection
        # ttk.Button(upload_frame, text="Select Files...", command=select_file).grid(row=0, column=2, padx=5, pady=5)

        # # add placeholder for upload status 
        # upload_status_label = ttk.Label(upload_frame, text="Maximum allowed file size is 10 MB.")
        # upload_status_label.grid(row=1, column=0, columnspan=3, padx=5, pady=5)
        # Document Upload Section (this goes in the main interface, under the Treatment Plans section)
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