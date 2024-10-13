import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkcalendar import DateEntry

# Initialize the main window
root = tk.Tk()
root.title("General")
root.geometry("1000x800")

# Create a canvas and a scrollbar
canvas = tk.Canvas(root)
scrollbar = ttk.Scrollbar(root, orient="vertical", command=canvas.yview)
scrollable_frame = ttk.Frame(canvas)


widget_frame = ttk.Frame(root)
widget_frame.pack(side='top')

save_button = ttk.Button(widget_frame, text='SAVE')
cancel_button = ttk.Button(widget_frame, text='CANCEL')

save_button.grid(row=1, column=0, sticky="w", padx=5)
cancel_button.grid(row=1, column=1, sticky="w", padx=5)

# Configure the canvas and scrollbar
scrollable_frame.bind(
    "<Configure>",
    lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
)

# Create a window in the canvas
canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")

# Link scrollbar to the canvas
canvas.configure(yscrollcommand=scrollbar.set)

# Pack the canvas and scrollbar
canvas.pack(side="left", fill="both", expand=True)
scrollbar.pack(side="right", fill="y")

# General tab title
va_frame = tk.Frame(scrollable_frame)
va_frame.pack(anchor="center", pady=10, padx=10)
ttk.Label(va_frame, text="VA").pack()

def add_new_session_popup():
    popup = tk.Toplevel(root)
    popup.title("Add New Session")
    popup.geometry("600x500")

def add_agency_popup():
    popup = tk.Toplevel(root)
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


# Function to create edit case details
def add_editbutton_popup():
    popup = tk.Toplevel(root)
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
    popup = tk.Toplevel(root)
    popup.title("Edit")
    popup.geometry("300x200")

    ttk.Label(popup, text="CAC Case Number", foreground='black').grid(row=2, column=0, padx=5, pady=5)
    case_number_entry = ttk.Entry(popup)
    case_number_entry.grid(row=2, column=1, padx=5, pady=5)

    # Update and Cancel buttons
    ttk.Button(popup, text="Update", command=lambda: [popup.destroy()]).grid(row=9, column=0, padx=5, pady=5)
    ttk.Button(popup, text="Cancel", command=lambda: [popup.destroy()]).grid(row=9, column=1, padx=5, pady=5)

def add_information_record_popup():
    popup = tk.Toplevel(root)
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

def add_personnel_popup():
    popup = tk.Toplevel(root)
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



# Create the Referral section
referral_frame = tk.LabelFrame(scrollable_frame, text="Referral", padx=10, pady=10)
referral_frame.pack(fill="x", padx=10, pady=5)

# Date (with DateEntry for calendar selection)
ttk.Label(referral_frame, text="Date").grid(row=0, column=0, padx=5, pady=5)
date_entry = DateEntry(referral_frame)
date_entry.grid(row=0, column=1, padx=5, pady=5)

ttk.Label(referral_frame, text="Referral Source").grid(row=1, column=0, sticky="w")
referral_source = ttk.Combobox(referral_frame, values=["DCS - Anderson Co.", "DCS - Hamilton Co."])
referral_source.grid(row=1, column=1, padx=5, pady=5)

ttk.Label(referral_frame, text="Person").grid(row=2, column=0, padx=5, pady=5)
person_entry = ttk.Combobox(referral_frame, values=["Person 1", "Person 2"]) 
person_entry.grid(row=2, column=1, padx=5, pady=5)

ttk.Button(referral_frame, text="Add Referral Source", command=add_agency_popup).grid(row=1, column=2, padx=5, pady=5)
ttk.Button(referral_frame, text="Add Person", command=add_personnel_popup).grid(row=2, column=2, padx=5, pady=5)


#Create the VAS section
vas_frame = tk.LabelFrame(scrollable_frame, text="Victim Advocacy Services", padx=10, pady=10)
vas_frame.pack(fill="x", padx=10, pady=5)

ttk.Label(vas_frame, text="VA Case Number").grid(row=0, column=0, padx=5, pady=5)
va_casenum_entry = ttk.Entry(vas_frame) 
va_casenum_entry.grid(row=0, column=1, padx=5, pady=5)

ttk.Label(vas_frame, text="Agency").grid(row=1, column=0, padx=5, pady=5)
agency_entry = ttk.Combobox(vas_frame, values=["Person 1", "Person 2"]) 
agency_entry.grid(row=1, column=1, padx=5, pady=5)

ttk.Button(vas_frame, text="Add Agency", command=add_agency_popup).grid(row=1, column=2, padx=5, pady=5)

ttk.Label(vas_frame, text="Person").grid(row=2, column=0, padx=5, pady=5)
person_entry = ttk.Combobox(vas_frame, values=["Person 1", "Person 2"]) 
person_entry.grid(row=2, column=1, padx=5, pady=5) 

ttk.Button(vas_frame, text="Add Person", command=add_personnel_popup).grid(row=2, column=2, padx=5, pady=5)

ttk.Label(vas_frame, text="Date Services first offered to child/family").grid(row=3, column=0, padx=5, pady=5)
date_services_offered = DateEntry(vas_frame)  
date_services_offered.grid(row=3, column=1, padx=5, pady=5)

ttk.Label(vas_frame, text="Did the child/family accept VA services?").grid(row=4, column=0, padx=5, pady=5)
services_accepted = ttk.Checkbutton(vas_frame, text="Yes", variable=False)  
services_accepted.grid(row=4, column=1, padx=5, pady=5)

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

ttk.Label(vas_frame, text="Ready for MDT Review").grid(row=11, column=0, padx=5, pady=5)
mdt_ready = ttk.Checkbutton(vas_frame, text="Yes", variable=False)  
mdt_ready.grid(row=11, column=1, padx=5, pady=5)

#------------------------------

# VAS Log Information
vas_log_frame = tk.LabelFrame(scrollable_frame, text="Victim Advocacy Services Log", padx=10, pady=10)
vas_log_frame.pack(fill="x", padx=10, pady=5)

ttk.Button(vas_log_frame, text="Add New Session Log", command=add_new_session_popup).grid(row=0, column=0, padx=5, pady=5)  
ttk.Button(vas_log_frame, text="Details").grid(row=0, column=1, padx=5, pady=5)  

ttk.Label(vas_log_frame, text="Date").grid(row=1, column=4, padx=5, pady=5)

ttk.Label(vas_log_frame, text="Start Time").grid(row=1, column=5, padx=5, pady=5)

ttk.Label(vas_log_frame, text="End Time").grid(row=1, column=6, padx=5, pady=5)

ttk.Label(vas_log_frame, text="Status").grid(row=1, column=7, padx=5, pady=5)

ttk.Button(vas_log_frame, text="Newer Records").grid(row=0, column=8, padx=5, pady=5)  
ttk.Button(vas_log_frame, text="Older Records").grid(row=0, column=9, padx=5, pady=5)  


#------------------------------

# Crime Compensation Application Section
crime_comp_app_frame = tk.LabelFrame(scrollable_frame, text="Crime Compensation Application", padx=10, pady=10)
crime_comp_app_frame.pack(fill="x", padx=10, pady=5)

ttk.Label(crime_comp_app_frame, text="State Claim Representative").grid(row=0, column=0, padx=5, pady=5)
state_claim_rep = ttk.Entry(crime_comp_app_frame)  
state_claim_rep.grid(row=0, column=1, padx=5, pady=5)

ttk.Label(crime_comp_app_frame, text="Have Birth Certificate").grid(row=1, column=0, padx=5, pady=5)
has_birth_cert = ttk.Checkbutton(crime_comp_app_frame, variable=False)  
has_birth_cert.grid(row=1, column=1, padx=5, pady=5)

ttk.Label(crime_comp_app_frame, text="Have Police Report").grid(row=2, column=0, padx=5, pady=5)
has_police_report = ttk.Checkbutton(crime_comp_app_frame, variable=False)  
has_police_report.grid(row=2, column=1, padx=5, pady=5)

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
# -Release of Information Section

def add_referral_popup():
    # Create a new Toplevel window
    popup = tk.Toplevel(root)
    popup.title("Add Referral")
    popup.geometry("400x300")

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

# Function to add new ICD Code record
def add_code_record_popup():
    # Create a new Toplevel window
    popup = tk.Toplevel(root)
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


#Add contact modal
def add_contact_popup():
    # Create a new Toplevel window
    popup = tk.Toplevel(root)
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


root.mainloop()