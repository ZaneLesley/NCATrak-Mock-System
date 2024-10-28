import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkcalendar import DateEntry
import Generaltab_interface
import people_interface
import MH_assessment
import MH_treatmentPlan_interface
import va_tab_interface
import sv_ttk

class MHBasicInterface(tk.Frame):

    def __init__(self, parent, controller):

        tk.Frame.__init__(self, parent)

        self.grid_rowconfigure(2, weight=1)
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

        #  window in the canvas
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")

        # scrollbar to canvas
        canvas.configure(yscrollcommand=scrollbar.set)

        # Use grid over pack for interface linking
        canvas.grid(row=2, column=0, sticky="nsew")
        scrollbar.grid(row=2, column=1, sticky="ns")

        button1 = ttk.Button(self, text="General", 
                            command=lambda: controller.show_frame(Generaltab_interface.GeneraltabInterface))
        button1.grid(row=0, column=0, padx=5, pady=5)

        button2 = ttk.Button(self, text="People", 
                            command=lambda: controller.show_frame(people_interface.people_interface))
        button2.grid(row=0, column=1, padx=5, pady=5)

        button3 = ttk.Button(self, text="Mental Health - Basic", 
                            command=lambda: controller.show_frame(MHBasicInterface))
        button3.grid(row=0, column=2, padx=5, pady=5)

        button4 = ttk.Button(self, text="Mental Health - Assessment", 
                            command=lambda: controller.show_frame(MH_assessment.MHassessment))
        button4.grid(row=0, column=3, padx=5, pady=5)

        button5 = ttk.Button(self, text="Mental Health - Treatment Plan", 
                            command=lambda: controller.show_frame(MH_treatmentPlan_interface.MH_treatment_plan_interface))
        button5.grid(row=0, column=4, padx=5, pady=5)

        button6 = ttk.Button(self, text="VA", 
                            command=lambda: controller.show_frame(va_tab_interface.va_interface))
        button6.grid(row=0, column=5, padx=5, pady=5)

        # function for line numbering
        def create_line_numbered_label(frame, text, line_number):
            line_number_label = ttk.Label(frame, text=f"({line_number})")
            line_number_label.grid(row=line_number-1, column=0, sticky="w", padx=5)
            label = ttk.Label(frame, text=text)
            label.grid(row=line_number-1, column=1, sticky="w", padx=5)

        # MDT Review checkbox at the top
        ready_mdt_var = tk.BooleanVar(value=False)
        mdt_frame = tk.Frame(scrollable_frame)
        mdt_frame.pack(anchor="center", pady=10)
        ttk.Checkbutton(mdt_frame, text="Ready for MDT Review", variable=ready_mdt_var).pack()


        # function to create a new personnel popup
        def add_personnel_popup():
            popup = tk.Toplevel(self)
            popup.title("New Personnel")
            popup.geometry("400x400")

            # existing personnel 
            existing_personnel = [
                "Bob Dylan",
                "Freddie Mercury",
                "Mike Jackson",
                "Adele",
                "Elvis Presley"
            ]
            
            # existing personnel displayed
            ttk.Label(popup, text="Below is a list of existing personnel. If the desired person is on this list, do not add again.").grid(row=0, column=0, columnspan=2, pady=5)

            personnel_listbox = tk.Listbox(popup, height=5)
            for person in existing_personnel:
                personnel_listbox.insert(tk.END, person)
            personnel_listbox.grid(row=1, column=0, columnspan=2, padx=10, pady=5)

            # input fields for new personnel
            ttk.Label(popup, text="First Name *", foreground='red').grid(row=2, column=0, padx=5, pady=5)
            first_name_entry = ttk.Entry(popup)
            first_name_entry.grid(row=2, column=1, padx=5, pady=5)

            ttk.Label(popup, text="Last Name *", foreground='red').grid(row=3, column=0, padx=5, pady=5)
            last_name_entry = ttk.Entry(popup)
            last_name_entry.grid(row=3, column=1, padx=5, pady=5)

            ttk.Label(popup, text="Preface").grid(row=4, column=0, padx=5, pady=5)
            preface_entry = ttk.Entry(popup)
            preface_entry.grid(row=4, column=1, padx=5, pady=5)

            ttk.Label(popup, text="Credentials").grid(row=5, column=0, padx=5, pady=5)
            credentials_entry = ttk.Entry(popup)
            credentials_entry.grid(row=5, column=1, padx=5, pady=5)

            ttk.Label(popup, text="Job Title").grid(row=6, column=0, padx=5, pady=5)
            job_title_entry = ttk.Entry(popup)
            job_title_entry.grid(row=6, column=1, padx=5, pady=5)

            ttk.Label(popup, text="Email").grid(row=7, column=0, padx=5, pady=5)
            email_entry = ttk.Entry(popup)
            email_entry.grid(row=7, column=1, padx=5, pady=5)

            ttk.Label(popup, text="Phone").grid(row=8, column=0, padx=5, pady=5)
            phone_entry = ttk.Entry(popup)
            phone_entry.grid(row=8, column=1, padx=5, pady=5)

            # save/cancel buttons
            ttk.Button(popup, text="Save", command=lambda: [popup.destroy()]).grid(row=9, column=0, padx=5, pady=5)
            ttk.Button(popup, text="Cancel", command=lambda: [popup.destroy()]).grid(row=9, column=1, padx=5, pady=5)

        def add_referral_source_popup():
            popup = tk.Toplevel(self)
            popup.title("New Referral Source")
            popup.geometry("400x400")

            # existing referral sources
            existing_sources = [
                "Blue Shield Blue Cross",
                "United Healthcare"
            ]
            
            # existing referral sources display
            ttk.Label(popup, text="Below is a list of existing referral sources. If the desired source is on this list, select it.").grid(row=0, column=0, columnspan=2, pady=5)

            source_listbox = tk.Listbox(popup, height=5)
            for source in existing_sources:
                source_listbox.insert(tk.END, source)
            source_listbox.grid(row=1, column=0, columnspan=2, padx=10, pady=5)

            # input fields for new referral source
            ttk.Label(popup, text="Agency Name *", foreground='red').grid(row=2, column=0, padx=5, pady=5)
            agency_name_entry = ttk.Entry(popup)
            agency_name_entry.grid(row=2, column=1, padx=5, pady=5)

            ttk.Label(popup, text="Address Line 1").grid(row=3, column=0, padx=5, pady=5)
            address_line1_entry = ttk.Entry(popup)
            address_line1_entry.grid(row=3, column=1, padx=5, pady=5)

            ttk.Label(popup, text="Address Line 2").grid(row=4, column=0, padx=5, pady=5)
            address_line2_entry = ttk.Entry(popup)
            address_line2_entry.grid(row=4, column=1, padx=5, pady=5)

            ttk.Label(popup, text="City").grid(row=5, column=0, padx=5, pady=5)
            city_entry = ttk.Entry(popup)
            city_entry.grid(row=5, column=1, padx=5, pady=5)

            ttk.Label(popup, text="State").grid(row=6, column=0, padx=5, pady=5)
            state_combo = ttk.Combobox(popup, values=["- Please select a state -", "State 1", "State 2"])
            state_combo.grid(row=6, column=1, padx=5, pady=5)

            ttk.Label(popup, text="Zip Code").grid(row=7, column=0, padx=5, pady=5)
            zip_code_entry = ttk.Entry(popup)
            zip_code_entry.grid(row=7, column=1, padx=5, pady=5)

            ttk.Label(popup, text="Phone Number").grid(row=8, column=0, padx=5, pady=5)
            phone_number_entry = ttk.Entry(popup)
            phone_number_entry.grid(row=8, column=1, padx=5, pady=5)

            # save/cancel buttons
            ttk.Button(popup, text="Save", command=lambda: [popup.destroy()]).grid(row=9, column=0, padx=5, pady=5)
            ttk.Button(popup, text="Cancel", command=lambda: [popup.destroy()]).grid(row=9, column=1, padx=5, pady=5)

        #  incoming referral section
        incoming_frame = tk.LabelFrame(scrollable_frame, text="Incoming Referral", padx=10, pady=10)
        incoming_frame.pack(fill="x", padx=10, pady=5)

        # Date (uses dateEntry)
        ttk.Label(incoming_frame, text="Date").grid(row=0, column=0, padx=5, pady=5)
        date_entry = DateEntry(incoming_frame, width=12, background='darkblue', foreground='white', borderwidth=2)
        date_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(incoming_frame, text="Referral Source:").grid(row=1, column=0, sticky="w")
        referral_source = ttk.Combobox(incoming_frame, values=["Blue Shield Blue Cross", "United Healthcare"])
        referral_source.grid(row=1, column=1, padx=5, pady=5)

        #  "+ Add" button for referral source dropdown
        ttk.Button(incoming_frame, text="+ Add", command=add_referral_source_popup).grid(row=1, column=2, padx=5, pady=5)

        ttk.Label(incoming_frame, text="Person").grid(row=2, column=0, padx=5, pady=5)
        person_combo = ttk.Combobox(incoming_frame, values=["Bob Dylan", "Freddie Mercury"])  
        person_combo.grid(row=2, column=1, padx=5, pady=5)

        #  "+ Add" button next to personnel dropdown
        ttk.Button(incoming_frame, text="+ Add", command=add_personnel_popup).grid(row=2, column=2, padx=5, pady=5)

        # custom fields section
        custom_frame = tk.LabelFrame(scrollable_frame, text="Custom Fields", padx=10, pady=10)
        custom_frame.pack(fill="x", padx=10, pady=5)

        # custom fields content
        create_line_numbered_label(custom_frame, "Referred for Mental Health Services", 1)
        mh_services_var = tk.BooleanVar(value=False)
        no_mh_services_var = tk.BooleanVar(value=False)  
        ttk.Checkbutton(custom_frame, text="Yes", variable=mh_services_var).grid(row=0, column=2, sticky="w")
        ttk.Checkbutton(custom_frame, text="No", variable=no_mh_services_var).grid(row=0, column=3, sticky="w")

        create_line_numbered_label(custom_frame, "Status of Mental Health Referral", 2)
        status_accepted_var = tk.BooleanVar(value=False)
        status_declined_var = tk.BooleanVar(value=False)  
        ttk.Checkbutton(custom_frame, text="Accepted: Attending Therapy Sessions", variable=status_accepted_var).grid(row=1, column=2, sticky="w")
        ttk.Checkbutton(custom_frame, text="Declined: Already receiving therapy services", variable=status_declined_var).grid(row=1, column=3, sticky="w")

        create_line_numbered_label(custom_frame, "Seen For MH Services Elsewhere", 3)
        mh_services_elsewhere = ttk.Combobox(custom_frame, values=["", "Location 1", "Location 2"])
        mh_services_elsewhere.grid(row=2, column=2, columnspan=2, padx=5, pady=5, sticky="we")

        create_line_numbered_label(custom_frame, "Psyco/Social Notes", 4)
        psyc_notes_entry = ttk.Entry(custom_frame)
        psyc_notes_entry.grid(row=3, column=2, columnspan=2, padx=5, pady=5, sticky="we")

        create_line_numbered_label(custom_frame, "MH Extended Services Candidate", 5)
        # the options for the dropdown based of NCA-Trak
        options = ["If Needed"] + [str(i) for i in range(4, 34)] + ["If Space Allows"]
        mh_extended_services = ttk.Combobox(custom_frame, values=options)
        mh_extended_services.grid(row=4, column=2, columnspan=2, padx=5, pady=5, sticky="we")


        create_line_numbered_label(custom_frame, "MH - Services Custom", 6)
        custom_field_6 = ttk.Entry(custom_frame)
        custom_field_6.grid(row=5, column=2, columnspan=2, padx=5, pady=5, sticky="we")

        create_line_numbered_label(custom_frame, "MH - Services Custom", 7)
        custom_field_7 = ttk.Entry(custom_frame)
        custom_field_7.grid(row=6, column=2, columnspan=2, padx=5, pady=5, sticky="we")

        create_line_numbered_label(custom_frame, "Client Declined Services", 8)
        client_declined_var = tk.BooleanVar(value=False)
        no_client_declined_var = tk.BooleanVar(value=False)  
        ttk.Checkbutton(custom_frame, text="Yes", variable=client_declined_var).grid(row=7, column=2, sticky="w")
        ttk.Checkbutton(custom_frame, text="No", variable=no_client_declined_var).grid(row=7, column=3, sticky="w")

        create_line_numbered_label(custom_frame, "Why Client Declined Services", 9)
        client_declined_reason = ttk.Combobox(custom_frame, values=["Already receiving therapy services", "Family didn't think needed/not supportive"])
        client_declined_reason.grid(row=8, column=2, columnspan=2, padx=5, pady=5, sticky="we")

        # telehealth Services Section
        telehealth_frame = tk.LabelFrame(scrollable_frame, text="Telehealth Services", padx=10, pady=10)
        telehealth_frame.pack(fill="x", padx=10, pady=5)

        # number of miles saved
        ttk.Label(telehealth_frame, text="Number of Miles Saved Providing Telehealth Services Per Session:").grid(row=0, column=0, padx=5, pady=5)
        miles_saved_combo = ttk.Combobox(telehealth_frame, values=["0-10 miles", "10-20 miles", "20+ miles"])
        miles_saved_combo.grid(row=0, column=1, padx=5, pady=5)

        # barriers encountered
        ttk.Label(telehealth_frame, text="Barriers Encountered During Mental Health Services:").grid(row=1, column=0, padx=5, pady=5, sticky="w")

        # list to store the BooleanVar instances
        barrier_vars = []
        barriers = ["Center doesn't offer the services needed", "Concerned about what others think", "Cost of services", 
                    "Distance to clinic", "Lack of transportation", "No insurance", "Scheduling difficulty", 
                    "Waitlist too long", "Other"]
        for i, barrier in enumerate(barriers):
            var = tk.BooleanVar(value=False)  
            barrier_vars.append(var)  
            ttk.Checkbutton(telehealth_frame, text=barrier, variable=var).grid(row=i+2, column=0, sticky="w")


        def add_provider_popup():
            # Create a new Toplevel window
            popup = tk.Toplevel(self)
            popup.title("Add Provider")
            popup.geometry("600x400")

            #  labels and entry fields
            ttk.Label(popup, text="MH Provider Agency").grid(row=0, column=0, padx=5, pady=5)
            agency_entry = ttk.Combobox(popup, values=["ABS Linkage", "Other Agency Options"])
            agency_entry.grid(row=0, column=1, padx=5, pady=5)

            ttk.Label(popup, text="Mental Health Service Provider").grid(row=1, column=0, padx=5, pady=5)
            provider_entry = ttk.Combobox(popup, values=["Sarah Jones", "Other Providers"])
            provider_entry.grid(row=1, column=1, padx=5, pady=5)

            ttk.Label(popup, text="MH Case #").grid(row=2, column=0, padx=5, pady=5)
            case_number_entry = ttk.Entry(popup)
            case_number_entry.grid(row=2, column=1, padx=5, pady=5)

            ttk.Label(popup, text="Date Therapy Offered to Family").grid(row=3, column=0, padx=5, pady=5)
            therapy_date_entry = DateEntry(popup, width=12, background='darkblue', foreground='white', borderwidth=2)
            therapy_date_entry.grid(row=3, column=1, padx=5, pady=5)

            ttk.Label(popup, text="Reason Sessions Ended").grid(row=4, column=0, padx=5, pady=5)
            reason_combo = ttk.Combobox(popup, values=["Select...", "Reason 1", "Reason 2"])
            reason_combo.grid(row=4, column=1, padx=5, pady=5)

            # save/cancel buttons
            ttk.Button(popup, text="Save", command=popup.destroy).grid(row=5, column=0, padx=5, pady=5)
            ttk.Button(popup, text="Cancel", command=popup.destroy).grid(row=5, column=1, padx=5, pady=5)

        # Mental Health Provider Log Section
        provider_log_frame = tk.LabelFrame(scrollable_frame, text="Mental Health Provider Log", padx=10, pady=10)
        provider_log_frame.pack(fill="x", padx=10, pady=5)

        # provider and details buttons
        provider_log_buttons_frame = tk.Frame(provider_log_frame)
        provider_log_buttons_frame.grid(row=0, column=0, sticky="w")
        ttk.Button(provider_log_buttons_frame, text="+ Add Provider", command=add_provider_popup).pack(side="left", padx=5, pady=5)
        ttk.Button(provider_log_buttons_frame, text="Details").pack(side="left", padx=5, pady=5)

        # Create a frame for adding a new provider
        provider_frame = tk.Frame(provider_log_frame)

        # Labels and entries for the new provider details
        ttk.Label(provider_frame, text="Date Services Offered").grid(row=0, column=0, padx=5, pady=5)
        date_services_offered = DateEntry(provider_frame, width=12, background='darkblue', foreground='white', borderwidth=2)
        date_services_offered.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(provider_frame, text="Agency").grid(row=0, column=2, padx=5, pady=5)
        agency_entry = ttk.Combobox(provider_frame, values=["ABS Linkage", "Other Agency Options"])
        agency_entry.grid(row=0, column=3, padx=5, pady=5)

        ttk.Label(provider_frame, text="Therapist").grid(row=0, column=4, padx=5, pady=5)
        therapist_entry = ttk.Entry(provider_frame)
        therapist_entry.grid(row=0, column=5, padx=5, pady=5)


        ttk.Label(provider_frame, text="Referral Type").grid(row=0, column=6, padx=5, pady=5)
        referral_type_entry = ttk.Combobox(provider_frame, values=["In House", "External"])
        referral_type_entry.grid(row=0, column=7, padx=5, pady=5)

        ttk.Label(provider_frame, text="Case #").grid(row=0, column=8, padx=5, pady=5)
        case_number_entry = ttk.Entry(provider_frame)
        case_number_entry.grid(row=0, column=9, padx=5, pady=5)

        # save/cancel buttons
        ttk.Button(provider_frame, text="Save").grid(row=1, column=8, padx=5, pady=5)
        ttk.Button(provider_frame, text="Cancel").grid(row=1, column=9, padx=5, pady=5)


        def add_referral_popup():
            # Create a new Toplevel window
            popup = tk.Toplevel(self)
            popup.title("Add Referral")
            popup.geometry("400x300")

            #  labels and entry fields
            ttk.Label(popup, text="Date").grid(row=0, column=0, padx=5, pady=5)
            referral_date_entry = DateEntry(popup, width=12, background='darkblue', foreground='white', borderwidth=2)
            referral_date_entry.grid(row=0, column=1, padx=5, pady=5)

            ttk.Label(popup, text="Referred To").grid(row=1, column=0, padx=5, pady=5)
            referred_to_combo = ttk.Combobox(popup, values=["Provider 1", "Provider 2"])
            referred_to_combo.grid(row=1, column=1, padx=5, pady=5)

            ttk.Label(popup, text="Comment").grid(row=2, column=0, padx=5, pady=5)
            comment_entry = ttk.Entry(popup, width=50)
            comment_entry.grid(row=2, column=1, padx=5, pady=5)

            # update/cancel buttons
            ttk.Button(popup, text="Update", command=popup.destroy).grid(row=4, column=1, padx=5, pady=5)
            ttk.Button(popup, text="Cancel", command=popup.destroy).grid(row=4, column=2, padx=5, pady=5)

        # Outside Referrals Section
        outside_referrals_frame = tk.LabelFrame(scrollable_frame, text="Outside Referrals", padx=10, pady=10)
        outside_referrals_frame.pack(fill="x", padx=10, pady=5)

        ttk.Button(outside_referrals_frame, text="+ Add New Referral", command=add_referral_popup).grid(row=0, column=0, padx=5, pady=5, sticky="w")
        ttk.Label(outside_referrals_frame, text="Referral").grid(row=1, column=0, padx=5, pady=5)
        ttk.Label(outside_referrals_frame, text="Referred To").grid(row=1, column=1, padx=5, pady=5)
        ttk.Label(outside_referrals_frame, text="Comments").grid(row=1, column=2, padx=5, pady=5)


        # function to add new point of contact popup for addintonal point of contact section
        def add_contact_popup():
            # Create a new Toplevel window
            popup = tk.Toplevel(self)
            popup.title("Add New Point of Contact")
            popup.geometry("400x300")

            #  labels and entry fields
            ttk.Label(popup, text="Action").grid(row=0, column=0, padx=5, pady=5)
            action_entry = ttk.Entry(popup)
            action_entry.grid(row=0, column=1, padx=5, pady=5)

            ttk.Label(popup, text="Agency").grid(row=1, column=0, padx=5, pady=5)
            agency_entry = ttk.Entry(popup)
            agency_entry.grid(row=1, column=1, padx=5, pady=5)

            ttk.Label(popup, text="Name").grid(row=2, column=0, padx=5, pady=5)
            name_entry = ttk.Entry(popup)
            name_entry.grid(row=2, column=1, padx=5, pady=5)

            ttk.Label(popup, text="Phone").grid(row=3, column=0, padx=5, pady=5)
            phone_entry = ttk.Entry(popup)
            phone_entry.grid(row=3, column=1, padx=5, pady=5)

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

        # Contact Info Section
        contact_info_frame = tk.LabelFrame(scrollable_frame, text="Contact Info", padx=10, pady=10)
        contact_info_frame.pack(fill="x", padx=10, pady=5)

        ttk.Label(contact_info_frame, text="Client Contact Info").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        ttk.Label(contact_info_frame, text="Justin Bieber").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        ttk.Label(contact_info_frame, text="Austin, Texas").grid(row=2, column=0, padx=5, pady=5, sticky="w")
        ttk.Label(contact_info_frame, text="Date Therapy Completed").grid(row=3, column=0, padx=5, pady=5)
        date_therapy_completed = DateEntry(contact_info_frame, width=12, background='darkblue', foreground='white', borderwidth=2)
        date_therapy_completed.grid(row=3, column=1, padx=5, pady=5)

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