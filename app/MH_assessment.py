import tkinter as tk
from tkinter import ttk
from tkcalendar import DateEntry
from tkinter import filedialog
import Generaltab_interface
import people_interface
import MH_basic_interface
import MH_treatmentPlan_interface
import va_tab_interface
import sv_ttk

class MHassessment(tk.Frame):

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
                            command=lambda: controller.show_frame(MHassessment))
        button4.grid(row=0, column=3, padx=5, pady=5)

        button5 = ttk.Button(self, text="Mental Health - Treatment Plan", 
                            command=lambda: controller.show_frame(MH_treatmentPlan_interface.MH_treatment_plan_interface))
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

        # Function to open the score entry popup and store the score
        def enter_score_popup(score_var):
            score_popup = tk.Toplevel(self)
            score_popup.title("Enter Score")
            score_popup.geometry("300x200")

            # Label and entry for score input
            ttk.Label(score_popup, text="Enter Assessment Score:").grid(row=0, column=0, padx=10, pady=10, sticky="w")
            score_entry = ttk.Entry(score_popup, width=10)
            score_entry.grid(row=0, column=1, padx=10, pady=10, sticky="w")

            def save_score():
                entered_score = score_entry.get()
                score_var.set(entered_score)
                score_popup.destroy()

            # Save and Cancel buttons
            ttk.Button(score_popup, text="Save", command=save_score).grid(row=1, column=0, padx=10, pady=10)
            ttk.Button(score_popup, text="Cancel", command=score_popup.destroy).grid(row=1, column=1, padx=10, pady=10)


        def add_custom_assessment_popup():
            # Create a new Toplevel window for custom assessment input
            custom_popup = tk.Toplevel(self)
            custom_popup.title("Add Custom Assessment Instrument")
            custom_popup.geometry("300x200+150+150")  # Adjusted size and positioning

            # Label and entry for the custom assessment instrument
            ttk.Label(custom_popup, text="Enter New Assessment Instrument:").grid(row=0, column=0, padx=10, pady=10, sticky="w")
            custom_assessment_entry = ttk.Entry(custom_popup, width=30)
            custom_assessment_entry.grid(row=1, column=0, padx=10, pady=5, sticky="w")

            # Function to save the custom assessment instrument
            def save_custom_assessment():
                new_assessment = custom_assessment_entry.get()
                if new_assessment:
                    # For now just print 
                    print(f"New Assessment Instrument Added: {new_assessment}")
                    custom_popup.destroy()  # Close the popup after saving

            ttk.Button(custom_popup, text="Save", command=save_custom_assessment).grid(row=2, column=0, padx=5, pady=5, sticky="w")
            ttk.Button(custom_popup, text="Cancel", command=custom_popup.destroy).grid(row=2, column=1, padx=5, pady=5, sticky="w")


        def add_assessment_popup():
            # Create a new Toplevel window
            popup = tk.Toplevel(self)
            popup.title("Add New Assessment")
            popup.geometry("600x400+100+100")  # Adjusted to add extra space from the top and left

            # Add some padding at the top using empty labels or adjust the grid padding
            ttk.Label(popup).grid(row=0, column=0, padx=10, pady=10)  # Empty label to add padding at the top

            # Variable to store and display the score
            score_var = tk.StringVar()

            # Assessment Instrument dropdown
            ttk.Label(popup, text="Assessment Instrument").grid(row=1, column=0, padx=10, pady=5, sticky="w")
            assessment_instrument_combo = ttk.Combobox(popup, values=["Instrument 1", "Instrument 2", "Instrument 3"], width=35, state="readonly")
            assessment_instrument_combo.grid(row=1, column=1, padx=10, pady=5, sticky="w")

            # Add link for custom assessment instrument
            ttk.Button(popup, text="Add", command=add_custom_assessment_popup).grid(row=1, column=2, padx=10, pady=5)

            # Bind selection event to open the score entry popup
            assessment_instrument_combo.bind("<<ComboboxSelected>>", lambda event: enter_score_popup(score_var))

            # Display the score once entered
            ttk.Label(popup, text="Score").grid(row=2, column=0, padx=10, pady=5, sticky="w")
            score_display = ttk.Label(popup, textvariable=score_var, width=10)  # Display the entered score
            score_display.grid(row=2, column=1, padx=10, pady=5, sticky="w")

            # Other content of the form follows the same layout...

            # Session Date
            ttk.Label(popup, text="Session Date").grid(row=3, column=0, padx=10, pady=5, sticky="w")
            session_date_entry = DateEntry(popup, width=20)
            session_date_entry.grid(row=3, column=1, padx=10, pady=5, sticky="w")

            # Assessment Date
            ttk.Label(popup, text="Assessment Date").grid(row=4, column=0, padx=10, pady=5, sticky="w")
            assessment_date_entry = DateEntry(popup, width=20)
            assessment_date_entry.grid(row=4, column=1, padx=10, pady=5, sticky="w")

            # Save and Cancel buttons
            ttk.Button(popup, text="Update", command=popup.destroy).grid(row=9, column=0, padx=5, pady=5)
            ttk.Button(popup, text="Cancel", command=popup.destroy).grid(row=9, column=1, padx=5, pady=5)


        # Assessments Given Section
        assessments_frame = tk.LabelFrame(scrollable_frame, text="Assessments Given", padx=10, pady=10)
        assessments_frame.pack(fill="x", padx=10, pady=5)  

        # Button to add new assessment
        ttk.Button(assessments_frame, text="+ Add New Assessment", command=add_assessment_popup).grid(row=0, column=0, padx=5, pady=5, sticky="w")

        # Column headers
        ttk.Label(assessments_frame, text="Assessment Instrument Name").grid(row=1, column=0, padx=5, pady=5)
        ttk.Label(assessments_frame, text="Timing").grid(row=1, column=1, padx=5, pady=5)
        ttk.Label(assessments_frame, text="Date").grid(row=1, column=2, padx=5, pady=5)
        ttk.Label(assessments_frame, text="Provider Person").grid(row=1, column=3, padx=5, pady=5)


        def add_diagnosis_popup():
            popup = tk.Toplevel(self)
            popup.title("Edit Diagnosis")
            popup.geometry("400x300+100+100") 

            # Add some padding at the top using an empty label or adjust the grid padding
            ttk.Label(popup).grid(row=0, column=0, padx=10, pady=10)  # Empty label to add padding at the top

            # Provider Agency Dropdown
            ttk.Label(popup, text="Provider Agency").grid(row=1, column=0, padx=10, pady=5, sticky="w")
            provider_agency_entry = ttk.Combobox(popup, values=["ABS Linkage Agreement Agency", "Agency B", "Agency C"], width=40)
            provider_agency_entry.grid(row=1, column=1, padx=10, pady=5)
            provider_agency_entry.current(0)  # Set default value

            # Provider Personnel Dropdown
            ttk.Label(popup, text="Provider Personnel").grid(row=2, column=0, padx=10, pady=5, sticky="w")
            provider_personnel_entry = ttk.Combobox(popup, values=["Sarah Jones", "John Doe", "Jane Smith"], width=40)
            provider_personnel_entry.grid(row=2, column=1, padx=10, pady=5)
            provider_personnel_entry.current(0)  # Set default value

            # Continue the rest of the form the same way...

            # Diagnosis Date
            ttk.Label(popup, text="Diagnosis Date").grid(row=3, column=0, padx=10, pady=5, sticky="w")
            diagnosis_date_entry = DateEntry(popup, width=18)
            diagnosis_date_entry.grid(row=3, column=1, padx=10, pady=5, sticky="w")

            # ICD 10 Group Dropdown
            ttk.Label(popup, text="ICD 10 Group").grid(row=4, column=0, padx=10, pady=5, sticky="w")
            icd10_group_entry = ttk.Combobox(popup, values=["ICD Group A", "ICD Group B", "ICD Group C"], width=40)
            icd10_group_entry.grid(row=4, column=1, padx=10, pady=5, sticky="w")

            # Save and Cancel buttons
            ttk.Button(popup, text="Update", command=popup.destroy).grid(row=6, column=0, padx=10, pady=10, sticky="w")
            ttk.Button(popup, text="Cancel", command=popup.destroy).grid(row=6, column=1, padx=10, pady=10, sticky="e")


        # Diagnosis Log Section
        diagnosis_frame = tk.LabelFrame(scrollable_frame, text="Diagnosis Log", padx=10, pady=10)
        diagnosis_frame.pack(fill="x", padx=10, pady=5)

        # Button to add a new diagnosis
        ttk.Button(diagnosis_frame, text="+ Add Diagnosis", command=add_diagnosis_popup).grid(row=0, column=0, padx=5, pady=5, sticky="w")

        # Column headers for the diagnosis log table
        ttk.Label(diagnosis_frame, text="Agency").grid(row=1, column=0, padx=5, pady=5)
        ttk.Label(diagnosis_frame, text="Therapist").grid(row=1, column=1, padx=5, pady=5)
        ttk.Label(diagnosis_frame, text="Diagnosis Date").grid(row=1, column=2, padx=5, pady=5)
        ttk.Label(diagnosis_frame, text="Diagnosis").grid(row=1, column=3, padx=5, pady=5)

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