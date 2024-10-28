import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkcalendar import DateEntry
import MH_basic_interface
import people_interface
import MH_assessment
import MH_treatmentPlan_interface
import va_tab_interface

class GeneraltabInterface(tk.Frame):
    
    def __init__(self, parent, controller):
        
        tk.Frame.__init__(self, parent)
        
        self.grid_rowconfigure(2, weight=1)
        self.grid_columnconfigure(0, weight=1)
        
        # label = ttk.Label(self, text="back to main page", font = ("Verdana", 35))
        # label.grid(row = 0, column=0, padx = 5, pady = 5)

        button1 = ttk.Button(self, text="General", 
                            command=lambda: controller.show_frame(GeneraltabInterface))
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

        widget_frame = ttk.Frame(self)
        widget_frame.grid(row=1, column=0, pady=20)

        save_button = ttk.Button(widget_frame, text='SAVE')
        cancel_button = ttk.Button(widget_frame, text='CANCEL')
        delete_button = ttk.Button(widget_frame, text='DELETE CASE')

        save_button.grid(row=1, column=0, sticky="w", padx=5)
        cancel_button.grid(row=1, column=1, sticky="w", padx=5)
        delete_button.grid(row=1, column=2, sticky="w", padx=5)

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

        # General tab title
        general_frame = tk.Frame(scrollable_frame)
        general_frame.pack(anchor="center", pady=10)
        ttk.Label(general_frame, text="Case Tracking").pack()


        # Function to create edit case details
        def add_editbutton_popup():
            popup = tk.Toplevel(self)
            popup.title("Edit")
            popup.geometry("500x400")

            # Entry fields for case details
            ttk.Label(popup, text="Service", foreground='black').grid(row=1, column=0, padx=5, pady=5)
            service_name = ttk.Label(popup, text="LI")
            service_name.grid(row=1, column=1, padx=5, pady=5)

            ttk.Label(popup, text="Referral Date", foreground='black').grid(row=2, column=0, padx=5, pady=5)
            referral_date_entry = DateEntry(popup, width=12, background='darkblue', foreground='white', borderwidth=2)
            referral_date_entry.grid(row=2, column=1, padx=5, pady=5)

            ttk.Label(popup, text="Referred By", foreground='black').grid(row=3, column=0, padx=5, pady=5)
            referral_group_entry = ttk.Combobox(popup)
            referral_group_entry.grid(row=3, column=1, padx=5, pady=5)
            referral_worker_entry = ttk.Combobox(popup)
            referral_worker_entry.grid(row=3, column=2, padx=5, pady=5)

            ttk.Label(popup, text="Providing Agency").grid(row=4, column=0, padx=5, pady=5)
            providing_agency_entry = ttk.Combobox(popup)
            providing_agency_entry.grid(row=4, column=1, padx=5, pady=5)

            ttk.Label(popup, text="Primary Contact").grid(row=5, column=0, padx=5, pady=5)
            primary_contact_entry = ttk.Combobox(popup)
            primary_contact_entry.grid(row=5, column=1, padx=5, pady=5)

            ttk.Label(popup, text="Status").grid(row=6, column=0, padx=5, pady=5)
            status_entry = ttk.Label(popup, text="Referred")
            status_entry.grid(row=6, column=1, padx=5, pady=5)

            ttk.Label(popup, text="Status Date").grid(row=7, column=0, padx=5, pady=5)
            status_date_entry = ttk.Label(popup, text="08/25/2021")
            status_date_entry.grid(row=7, column=1, padx=5, pady=5)

            # Update and Cancel buttons
            ttk.Button(popup, text="Update", command=lambda: [popup.destroy()]).grid(row=9, column=0, padx=5, pady=5)
            ttk.Button(popup, text="Cancel", command=lambda: [popup.destroy()]).grid(row=9, column=1, padx=5, pady=5)

        def add_allegation_record_popup():
            popup = tk.Toplevel(self)
            popup.title("Edit")
            popup.geometry("300x200")

            ttk.Label(popup, text="CAC Case Number", foreground='black').grid(row=2, column=0, padx=5, pady=5)
            case_number_entry = ttk.Entry(popup)
            case_number_entry.grid(row=2, column=1, padx=5, pady=5)

            # Update and Cancel buttons
            ttk.Button(popup, text="Update", command=lambda: [popup.destroy()]).grid(row=9, column=0, padx=5, pady=5)
            ttk.Button(popup, text="Cancel", command=lambda: [popup.destroy()]).grid(row=9, column=1, padx=5, pady=5)

        def add_information_record_popup():
            popup = tk.Toplevel(self)
            popup.title("")
            popup.geometry("600x500")

            twelve = tk.BooleanVar(value=False)

            # Entry fields for case details
            ttk.Label(popup, text="Requested Date", foreground='black').grid(row=2, column=0, padx=5, pady=5)
            requested_date_entry = DateEntry(popup, width=12, background='darkblue', foreground='white', borderwidth=2)
            requested_date_entry.grid(row=2, column=1, padx=5, pady=5)

            ttk.Label(popup, text="Requested By", foreground='black').grid(row=3, column=0, padx=5, pady=5)
            requested_by_entry = ttk.Entry(popup)
            requested_by_entry.grid(row=3, column=1, padx=5, pady=5)

            ttk.Label(popup, text="Is this a request by subpoena?", foreground='black').grid(row=4, column=0, padx=5, pady=5)
            check_box = ttk.Checkbutton(popup, text="Yes", variable=twelve) 
            check_box.grid(row=4, column=1, padx=5, pady=5)

            ttk.Label(popup, text="Who authorized release?").grid(row=5, column=0, padx=5, pady=5)
            who_authorized_entry = ttk.Entry(popup)
            who_authorized_entry.grid(row=5, column=1, padx=5, pady=5)

            ttk.Label(popup, text="Who released the records?").grid(row=6, column=0, padx=5, pady=5)
            who_released_entry = ttk.Entry(popup)
            who_released_entry.grid(row=6, column=1, padx=5, pady=5)

            ttk.Label(popup, text="What records were released?").grid(row=7, column=0, padx=5, pady=5)
            what_records_entry = ttk.Entry(popup)
            what_records_entry.grid(row=7, column=1, padx=5, pady=5)

            ttk.Label(popup, text="Date Released").grid(row=8, column=0, padx=5, pady=5)
            date_released_entry = ttk.Entry(popup)
            date_released_entry.grid(row=8, column=1, padx=5, pady=5)

            ttk.Label(popup, text="Date to be returned (if applicable)").grid(row=9, column=0, padx=5, pady=5)
            tobe_returned_date_entry = ttk.Entry(popup)
            tobe_returned_date_entry.grid(row=9, column=1, padx=5, pady=5)

            ttk.Label(popup, text="Date Returned").grid(row=10, column=0, padx=5, pady=5)
            returned_date_entry = ttk.Entry(popup)
            returned_date_entry.grid(row=10, column=1, padx=5, pady=5)

            ttk.Label(popup, text="Testing field 1").grid(row=11, column=0, padx=5, pady=5)
            testing_field1_entry = ttk.Entry(popup)
            testing_field1_entry.grid(row=11, column=1, padx=5, pady=5)

            ttk.Label(popup, text="Testing field 2").grid(row=12, column=0, padx=5, pady=5)
            testing_field2_entry = ttk.Entry(popup)
            testing_field2_entry.grid(row=12, column=1, padx=5, pady=5)

            ttk.Label(popup, text="Name and Address").grid(row=13, column=0, padx=5, pady=5)
            name_address_entry = ttk.Entry(popup)
            name_address_entry.grid(row=13, column=1, padx=5, pady=5)

            # Update and Cancel buttons
            ttk.Button(popup, text="Save", command=lambda: [popup.destroy()]).grid(row=14, column=0, padx=5, pady=5)
            ttk.Button(popup, text="Cancel", command=lambda: [popup.destroy()]).grid(row=14, column=1, padx=5, pady=5)



        # Create the cases section
        cases_frame = tk.LabelFrame(scrollable_frame, text="Cases", padx=10, pady=10)
        cases_frame.pack(fill="x", padx=10, pady=5)

        # Date (with DateEntry for calendar selection)
        ttk.Label(cases_frame, text="Service").grid(row=0, column=1, padx=5, pady=5)
        service_field = ttk.Entry(cases_frame)
        service_field.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(cases_frame, text="Referral Date").grid(row=0, column=2, sticky="w")
        referral_date = ttk.Combobox(cases_frame, values=["DCS - Anderson Co.", "DCS - Hamilton Co."])
        referral_date.grid(row=1, column=2, padx=5, pady=5)

        ttk.Label(cases_frame, text="Referred By").grid(row=0, column=3, padx=5, pady=5)
        referred_by_field = ttk.Combobox(cases_frame, values=["Person 1", "Person 2"])  # Add person options
        referred_by_field.grid(row=1, column=3, padx=5, pady=5)

        ttk.Label(cases_frame, text="Providing Agency").grid(row=0, column=4, padx=5, pady=5)
        providing_agency = ttk.Combobox(cases_frame, values=["Person 1", "Person 2"])  # Add person options
        providing_agency.grid(row=1, column=4, padx=5, pady=5)

        ttk.Label(cases_frame, text="Primary Contact").grid(row=0, column=5, padx=5, pady=5)
        primary_contact = ttk.Combobox(cases_frame, values=["Person 1", "Person 2"])  # Add person options
        primary_contact.grid(row=1, column=5, padx=5, pady=5)

        ttk.Label(cases_frame, text="Status").grid(row=0, column=6, padx=5, pady=5)
        status_field = ttk.Combobox(cases_frame, values=["Person 1", "Person 2"])  # Add person options
        status_field.grid(row=1, column=6, padx=5, pady=5)

        ttk.Label(cases_frame, text="Status Date").grid(row=0, column=7, padx=5, pady=5)
        status_date = ttk.Combobox(cases_frame, values=["Person 1", "Person 2"])  # Add person options
        status_date.grid(row=1, column=7, padx=5, pady=5)

        # Add the "Edit" button next to the personnel dropdown
        ttk.Button(cases_frame, text="Edit", command=add_editbutton_popup).grid(row=1, column=0, padx=5, pady=5)

        #------------------------------

        def add_agency_popup():
            popup = tk.Toplevel(self)
            popup.title("New Agency")
            popup.geometry("600x500")

            existing_agency = [
                "CAC of Anytown",
                "Child Guidance",
                "FBI",
                "Mercy Hospital",
                "Police Department"
            ]

            ttk.Label(popup, text="Below is a list of existing agencies.", foreground='black').grid(row=1, column=0, padx=5, pady=5)
            ttk.Label(popup, text="If the desired agency is on this list then click 'Use Agency'.", foreground='black').grid(row=2, column=0, padx=5, pady=5)
            ttk.Label(popup, text="If the agency is not on the list enter the agency name below and click 'Save'.", foreground='black').grid(row=3, column=0, padx=5, pady=5)
            agency_listbox = tk.Listbox(popup, height=5)
            for person in existing_agency:
                agency_listbox.insert(tk.END, person)
            agency_listbox.grid(row=4, column=0, columnspan=2, padx=10, pady=5)

            # Entry fields for case agency
            ttk.Label(popup, text="Agency Name", foreground='black').grid(row=5, column=0, padx=5, pady=5)
            agency_name_entry = ttk.Entry(popup, foreground='white')
            agency_name_entry.grid(row=5, column=1, padx=5, pady=5)

            ttk.Label(popup, text="Address Line 1", foreground='black').grid(row=6, column=0, padx=5, pady=5)
            address_line1_entry = ttk.Entry(popup)
            address_line1_entry.grid(row=6, column=1, padx=5, pady=5)

            ttk.Label(popup, text="Address Line 2", foreground='black').grid(row=7, column=0, padx=5, pady=5)
            address_line2_entry = ttk.Entry(popup)
            address_line2_entry.grid(row=7, column=1, padx=5, pady=5)

            ttk.Label(popup, text="City").grid(row=8, column=0, padx=5, pady=5)
            city_entry = ttk.Entry(popup)
            city_entry.grid(row=8, column=1, padx=5, pady=5)

            ttk.Label(popup, text="State").grid(row=9, column=0, padx=5, pady=5)
            state_entry = ttk.Combobox(popup)
            state_entry.grid(row=9, column=1, padx=5, pady=5)

            ttk.Label(popup, text="Zip Code").grid(row=10, column=0, padx=5, pady=5)
            zipcode_entry = ttk.Entry(popup)
            zipcode_entry.grid(row=10, column=1, padx=5, pady=5)

            ttk.Label(popup, text="Phone Number").grid(row=11, column=0, padx=5, pady=5)
            phone_entry = ttk.Entry(popup)
            phone_entry.grid(row=11, column=1, padx=5, pady=5)

            # Update and Cancel buttons
            ttk.Button(popup, text="Save", command=lambda: [popup.destroy()]).grid(row=14, column=0, padx=5, pady=5)
            ttk.Button(popup, text="Cancel", command=lambda: [popup.destroy()]).grid(row=14, column=1, padx=5, pady=5)

        def add_personnel_popup():
            popup = tk.Toplevel(self)
            popup.title("New Personnel")
            popup.geometry("800x600")

            # existing personnel 
            existing_personnel = [
                "Bob Dylan",
                "Freddie Mercury",
                "Mike Jackson",
                "Adele",
                "Elvis Presley"
            ]

            ttk.Label(popup, text="Below is a list of existing personnel.", foreground='black').grid(row=1, column=0, padx=5, pady=5)
            ttk.Label(popup, text="If the desired person is on this list, do not add again.", foreground='black').grid(row=2, column=0, padx=5, pady=5)
            ttk.Label(popup, text="Instead click Cancel to return to the previous screen and select them from the person pick list.", foreground='black').grid(row=3, column=0, padx=5, pady=5)
            personnel_listbox = tk.Listbox(popup, height=5)
            for person in existing_personnel:
                personnel_listbox.insert(tk.END, person)
            personnel_listbox.grid(row=4, column=0, columnspan=2, padx=10, pady=5)

            # Entry fields for case agency
            ttk.Label(popup, text="First Name", foreground='black').grid(row=5, column=0, padx=5, pady=5)
            first_name = ttk.Entry(popup, foreground='white')
            first_name.grid(row=5, column=1, padx=5, pady=5)

            ttk.Label(popup, text="Last Name", foreground='black').grid(row=6, column=0, padx=5, pady=5)
            last_name = ttk.Entry(popup)
            last_name.grid(row=6, column=1, padx=5, pady=5)

            ttk.Label(popup, text="Preface", foreground='black').grid(row=7, column=0, padx=5, pady=5)
            preface_entry = ttk.Entry(popup)
            preface_entry.grid(row=7, column=1, padx=5, pady=5)

            ttk.Label(popup, text="Credentials").grid(row=8, column=0, padx=5, pady=5)
            credentials_entry = ttk.Entry(popup)
            credentials_entry.grid(row=8, column=1, padx=5, pady=5)

            ttk.Label(popup, text="Job Title").grid(row=9, column=0, padx=5, pady=5)
            job_title_entry = ttk.Entry(popup)
            job_title_entry.grid(row=9, column=1, padx=5, pady=5)

            ttk.Label(popup, text="Email").grid(row=10, column=0, padx=5, pady=5)
            email_entry = ttk.Entry(popup)
            email_entry.grid(row=10, column=1, padx=5, pady=5)

            ttk.Label(popup, text="Phone").grid(row=11, column=0, padx=5, pady=5)
            phone_entry = ttk.Entry(popup)
            phone_entry.grid(row=11, column=1, padx=5, pady=5)

            # Update and Cancel buttons
            ttk.Button(popup, text="Save", command=lambda: [popup.destroy()]).grid(row=14, column=0, padx=5, pady=5)
            ttk.Button(popup, text="Cancel", command=lambda: [popup.destroy()]).grid(row=14, column=1, padx=5, pady=5)


        # Case Information
        case_information_frame = tk.LabelFrame(scrollable_frame, text="Case Information", padx=10, pady=10)
        case_information_frame.pack(fill="x", padx=10, pady=5)

        ttk.Label(case_information_frame, text="Date Received by CAC").grid(row=0, column=0, padx=5, pady=5)
        date_entry = DateEntry(case_information_frame, width=12, background='darkblue', foreground='white', borderwidth=2)
        date_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(case_information_frame, text="Main Agency Involved").grid(row=1, column=0, padx=5, pady=5)
        main_agency = ttk.Combobox(case_information_frame, values=["DCS - Anderson Co.", "DCS - Hamilton Co."])
        main_agency.grid(row=1, column=1, padx=5, pady=5)
        add_agency = ttk.Button(case_information_frame, text="+ Add", command=add_agency_popup)
        add_agency.grid(row=1, column=2, padx=5, pady=5)

        ttk.Label(case_information_frame, text="Main Personnel Involved").grid(row=2, column=0, padx=5, pady=5)
        main_personnel = ttk.Combobox(case_information_frame, values=["Person 1", "Person 2"])  
        main_personnel.grid(row=2, column=1, padx=5, pady=5)
        add_personnel = ttk.Button(case_information_frame, text="+ Add", command=add_personnel_popup)  
        add_personnel.grid(row=2, column=2, padx=5, pady=5)

        ttk.Label(case_information_frame, text="Case Closed Reason").grid(row=3, column=0, padx=5, pady=5)
        close_reason = ttk.Combobox(case_information_frame, values=["Person 1", "Person 2"]) 
        close_reason.grid(row=3, column=1, padx=5, pady=5)

        ttk.Label(case_information_frame, text="Case Close Date").grid(row=4, column=0, padx=5, pady=5)
        close_date = DateEntry(case_information_frame, width=12, background='darkblue', foreground='white', borderwidth=2) 
        close_date.grid(row=4, column=1, padx=5, pady=5)

        ttk.Label(case_information_frame, text="Survey Complete (1)").grid(row=5, column=0, padx=5, pady=5)
        survey_complete = ttk.Combobox(case_information_frame, values=["Person 1", "Person 2"])  
        survey_complete.grid(row=5, column=1, padx=5, pady=5)

        ttk.Label(case_information_frame, text="Follow Up Survey Complete (2)").grid(row=6, column=0, padx=5, pady=5)
        followup_survey = DateEntry(case_information_frame, width=12, background='darkblue', foreground='white', borderwidth=2) 
        followup_survey.grid(row=6, column=1, padx=5, pady=5)

        ttk.Label(case_information_frame, text="CAC Case # (3)").grid(row=7, column=0, padx=5, pady=5)
        cac_casenum = ttk.Entry(case_information_frame)  
        cac_casenum.grid(row=7, column=1, padx=5, pady=5)

        one = tk.BooleanVar(value=False)
        two = tk.BooleanVar(value=False)
        three = tk.BooleanVar(value=False)
        four = tk.BooleanVar(value=False)
        five = tk.BooleanVar(value=False)
        six = tk.BooleanVar(value=False)
        seven = tk.BooleanVar(value=False)
        eight = tk.BooleanVar(value=False)
        nine = tk.BooleanVar(value=False)
        ten = tk.BooleanVar(value=False)
        eleven = tk.BooleanVar(value=False)

        ttk.Label(case_information_frame, text="Did child go through the education program? (4)").grid(row=8, column=0, padx=2, pady=5)
        Yes = ttk.Checkbutton(case_information_frame, text="Yes", variable=one) 
        Yes.grid(row=8, column=1, padx=5, pady=5)
        No = ttk.Checkbutton(case_information_frame, text="No", variable=two)
        No.grid(row=8, column=2, padx=5, pady=5)
        Not_Interested = ttk.Checkbutton(case_information_frame, text="Not Interested", variable=three) 
        Not_Interested.grid(row=8, column=3, padx=5, pady=5)
        Maybe = ttk.Checkbutton(case_information_frame, text="Maybe", variable=four) 
        Maybe.grid(row=9, column=1, padx=5, pady=5)
        sure = ttk.Checkbutton(case_information_frame, text="Not sure", variable=five)
        sure.grid(row=9, column=2, padx=5, pady=5)
        Interested = ttk.Checkbutton(case_information_frame, text="Interested", variable=six) 
        Interested.grid(row=9, column=3, padx=5, pady=5)
        Denied = ttk.Checkbutton(case_information_frame, text="Denied", variable=seven)
        Denied.grid(row=10, column=1, padx=5, pady=5)

        ttk.Label(case_information_frame, text="Test 5").grid(row=11, column=0, padx=5, pady=5)
        test5 = ttk.Combobox(case_information_frame, values=["Person 1", "Person 2"])  
        test5.grid(row=11, column=1, padx=5, pady=5)

        ttk.Label(case_information_frame, text="General - Custom Field 6").grid(row=12, column=0, padx=5, pady=5)
        custom_field6 = ttk.Entry(case_information_frame)  
        custom_field6.grid(row=12, column=1, padx=5, pady=5)

        ttk.Label(case_information_frame, text="General - Custom Field 7").grid(row=13, column=0, padx=5, pady=5)
        custom_field7 = ttk.Entry(case_information_frame)  
        custom_field7.grid(row=13, column=1, padx=5, pady=5)

        ttk.Label(case_information_frame, text="General - Custom Field 8").grid(row=14, column=0, padx=5, pady=5)
        custom_field8 = ttk.Entry(case_information_frame)  
        custom_field8.grid(row=14, column=1, padx=5, pady=5)

        ttk.Label(case_information_frame, text="Chapter Test Field (9)").grid(row=15, column=0, padx=5, pady=5)
        testing = ttk.Checkbutton(case_information_frame, text="Testing", variable=nine) 
        testing.grid(row=15, column=1, padx=5, pady=5)
        no_testing = ttk.Checkbutton(case_information_frame, text="No Testing", variable=ten)
        no_testing.grid(row=16, column=1, padx=5, pady=5)
        new_client = ttk.Checkbutton(case_information_frame, text="New Client", variable=eleven) 
        new_client.grid(row=17, column=1, padx=5, pady=5)

        #------------------------------

        # Linked Cases Services Section
        linked_cases_frame = tk.LabelFrame(scrollable_frame, text="Cases Linked to this Allegation", padx=10, pady=10)
        linked_cases_frame.pack(fill="x", padx=10, pady=5)

        # CAC Case Number
        ttk.Label(linked_cases_frame, text="CAC Case Number").grid(row=1, column=6, padx=5, pady=5)
        case_number = ttk.Combobox(linked_cases_frame, values=["Person 1", "Person 2"])  # Add person options
        case_number.grid(row=2, column=6, padx=5, pady=5)

        # Alleged Victim
        ttk.Label(linked_cases_frame, text="Alleged Victim").grid(row=1, column=7, padx=5, pady=5)
        alleged_victim = ttk.Combobox(linked_cases_frame, values=["Person 1", "Person 2"])  # Add person options
        alleged_victim.grid(row=2, column=7, padx=5, pady=5)

        # Add the "Edit" button 
        ttk.Button(linked_cases_frame, text="Delete", command=add_editbutton_popup).grid(row=2, column=0, padx=5, pady=5)

        # Add the "Add new record" button 
        ttk.Button(linked_cases_frame, text="Add new record", command=add_allegation_record_popup).grid(row=0, column=0, padx=5, pady=5)

        # -Court Activities Section
        court_activities_frame = tk.LabelFrame(scrollable_frame, text="Court Activities", padx=10, pady=10)
        court_activities_frame.pack(fill="x", padx=10, pady=5)

        # Court Type
        ttk.Label(court_activities_frame, text="Court Type").grid(row=0, column=0, padx=5, pady=5)
        court_type = ttk.Combobox(court_activities_frame, values=["Person 1", "Person 2"])  # Add person options
        court_type.grid(row=1, column=0, padx=5, pady=5)

        # Court Date
        ttk.Label(court_activities_frame, text="Court Date").grid(row=0, column=1, padx=5, pady=5)
        court_date = ttk.Combobox(court_activities_frame, values=["Person 1", "Person 2"])  # Add person options
        court_date.grid(row=1, column=1, padx=5, pady=5)

        #--------------------------------
        # -Release of Information Section
        information_release_frame = tk.LabelFrame(scrollable_frame, text="Release of Information", padx=10, pady=10)
        information_release_frame.pack(fill="x", padx=10, pady=5)


        ttk.Label(information_release_frame, text="Date Requested").grid(row=1, column=1, padx=5, pady=5)
        date_requested = ttk.Combobox(information_release_frame, values=["Person 1", "Person 2"])  # Add person options
        date_requested.grid(row=2, column=1, padx=5, pady=5)


        ttk.Label(information_release_frame, text="Requested By").grid(row=1, column=2, padx=5, pady=5)
        requested_by = ttk.Combobox(information_release_frame, values=["Person 1", "Person 2"])  # Add person options
        requested_by.grid(row=2, column=2, padx=5, pady=5)

        ttk.Label(information_release_frame, text="By Subpoena").grid(row=1, column=3, padx=5, pady=5)
        by_subpeona = ttk.Combobox(information_release_frame, values=["Person 1", "Person 2"])  # Add person options
        by_subpeona.grid(row=2, column=3, padx=5, pady=5)


        ttk.Label(information_release_frame, text="Authorized By").grid(row=1, column=4, padx=5, pady=5)
        authorized_by = ttk.Combobox(information_release_frame, values=["Person 1", "Person 2"])  # Add person options
        authorized_by.grid(row=2, column=4, padx=5, pady=5)

        ttk.Label(information_release_frame, text="Released By").grid(row=1, column=5, padx=5, pady=5)
        released_by = ttk.Combobox(information_release_frame, values=["Person 1", "Person 2"])  # Add person options
        released_by.grid(row=2, column=5, padx=5, pady=5)


        ttk.Label(information_release_frame, text="Records").grid(row=1, column=6, padx=5, pady=5)
        records = ttk.Combobox(information_release_frame, values=["Person 1", "Person 2"])  # Add person options
        records.grid(row=2, column=6, padx=5, pady=5)

        ttk.Label(information_release_frame, text="Date Released").grid(row=1, column=7, padx=5, pady=5)
        date_released = ttk.Combobox(information_release_frame, values=["Person 1", "Person 2"])  # Add person options
        date_released.grid(row=2, column=7, padx=5, pady=5)


        ttk.Label(information_release_frame, text="Date to be Returned").grid(row=1, column=8, padx=5, pady=5)
        tobe_returned = ttk.Combobox(information_release_frame, values=["Person 1", "Person 2"])  # Add person options
        tobe_returned.grid(row=2, column=8, padx=5, pady=5)

        ttk.Label(information_release_frame, text="Date Returned").grid(row=1, column=9, padx=5, pady=5)
        date_returned = ttk.Combobox(information_release_frame, values=["Person 1", "Person 2"])  # Add person options
        date_returned.grid(row=2, column=9, padx=5, pady=5)

        # Add the "Add new record" button 
        ttk.Button(information_release_frame, text="Add new record", command=add_information_record_popup).grid(row=0, column=0, padx=5, pady=5)

        def add_referral_popup():
            # Create a new Toplevel window
            popup = tk.Toplevel(self)
            popup.title("Add Referral")
            popup.geometry("400x300")

            # Create labels and entry fields
            ttk.Label(popup, text="Referred From").grid(row=0, column=0, padx=5, pady=5)
            comment_entry = ttk.Entry(popup)
            comment_entry.grid(row=0, column=1, padx=5, pady=5)

            ttk.Label(popup, text="Date").grid(row=1, column=0, padx=5, pady=5)
            referral_date_entry = DateEntry(popup, width=12, background='darkblue', foreground='white', borderwidth=2)
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
        # Insurance Information

        insurance_information_frame = tk.LabelFrame(scrollable_frame, text="Insurance Information", padx=10, pady=10)
        insurance_information_frame.pack(fill="x", padx=10, pady=5)

        ttk.Label(insurance_information_frame, text="Primary Insurance").grid(row=0, column=1, padx=5, pady=5)
        ttk.Label(insurance_information_frame, text="Secondary Insurance").grid(row=0, column=2, padx=5, pady=5)

        ttk.Label(insurance_information_frame, text="Company").grid(row=1, column=0, padx=5, pady=5)
        company1 = ttk.Entry(insurance_information_frame, foreground='white')
        company1.grid(row=1, column=1, padx=5, pady=5)
        company2 = ttk.Entry(insurance_information_frame,foreground='white')
        company2.grid(row=1, column=2, padx=5, pady=5)

        ttk.Label(insurance_information_frame, text="Subscriber").grid(row=2, column=0, padx=5, pady=5)
        subscriber1 = ttk.Entry(insurance_information_frame)
        subscriber1.grid(row=2, column=1, padx=5, pady=5)
        subscriber2 = ttk.Entry(insurance_information_frame,foreground='white')
        subscriber2.grid(row=2, column=2, padx=5, pady=5)

        ttk.Label(insurance_information_frame, text="Policy Number").grid(row=3, column=0, padx=5, pady=5)
        policy1 = ttk.Entry(insurance_information_frame)  
        policy1.grid(row=3, column=1, padx=5, pady=5)
        policy2 = ttk.Entry(insurance_information_frame,foreground='white')
        policy2.grid(row=3, column=2, padx=5, pady=5)

        ttk.Label(insurance_information_frame, text="Group").grid(row=4, column=0, padx=5, pady=5)
        group1 = ttk.Entry(insurance_information_frame)  
        group1.grid(row=4, column=1, padx=5, pady=5)
        group2 = ttk.Entry(insurance_information_frame, foreground='white')
        group2.grid(row=4, column=2, padx=5, pady=5)

        ttk.Label(insurance_information_frame, text="Has Client received referral").grid(row=5, column=0, padx=5, pady=5)
        client_referral = ttk.Checkbutton(insurance_information_frame, variable=eight) 
        client_referral.grid(row=5, column=1, padx=5, pady=5)

        ttk.Label(insurance_information_frame, text="Primary Clinic").grid(row=6, column=0, padx=5, pady=5)
        primary_clinic = ttk.Entry(insurance_information_frame)  
        primary_clinic.grid(row=6, column=1, padx=5, pady=5)

        ttk.Label(insurance_information_frame, text="Primary Provider").grid(row=7, column=0, padx=5, pady=5)
        primary_prov = ttk.Entry(insurance_information_frame)  
        primary_prov.grid(row=7, column=1, padx=5, pady=5)

        ttk.Label(insurance_information_frame, text="Primary Provider Phone").grid(row=8, column=0, padx=5, pady=5)
        phone_num = ttk.Entry(insurance_information_frame) 
        phone_num.grid(row=8, column=1, padx=5, pady=5)

        # Function to add new ICD Code record
        def add_code_record_popup():
            # Create a new Toplevel window
            popup = tk.Toplevel(self)
            popup.title("Edit")
            popup.geometry("400x300")

            # Create labels and entry fields
            ttk.Label(popup, text="Group").grid(row=0, column=0, padx=5, pady=5)
            group_entry = ttk.Entry(popup)
            group_entry.grid(row=0, column=1, padx=5, pady=5)

            ttk.Label(popup, text="Code").grid(row=1, column=0, padx=5, pady=5)
            code_entry = ttk.Entry(popup)
            code_entry.grid(row=1, column=1, padx=5, pady=5)

            # Update and Cancel buttons
            ttk.Button(popup, text="Update", command=lambda: [popup.destroy()]).grid(row=3, column=0, padx=5, pady=5)
            ttk.Button(popup, text="Cancel", command=lambda: [popup.destroy()]).grid(row=3, column=1, padx=5, pady=5)

        # Additional Points of Contact Section
        codes_frame = tk.LabelFrame(scrollable_frame, text="ICD Codes", padx=10, pady=10)
        codes_frame.pack(fill="x", padx=10, pady=5)

        # Button to add a new point of contact
        ttk.Button(codes_frame, text="Add new record", command=add_code_record_popup).grid(row=0, column=0, padx=5, pady=5, sticky="w")
        ttk.Label(codes_frame, text="Group").grid(row=2, column=1, padx=5, pady=5)
        group_entry = ttk.Entry(codes_frame)
        group_entry.grid(row=3, column=1, padx=5, pady=5)

        ttk.Label(codes_frame, text="Code").grid(row=2, column=2, padx=5, pady=5)
        code_entry = ttk.Entry(codes_frame)
        code_entry.grid(row=3, column=2, padx=5, pady=5)

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