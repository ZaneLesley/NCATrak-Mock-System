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

# VA tab title
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

#------------------------------

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

services_accept = tk.BooleanVar(value=False)
ttk.Label(vas_frame, text="Did the child/family accept VA services?").grid(row=4, column=0, padx=5, pady=5)
services_accepted = ttk.Checkbutton(vas_frame, text="Yes", variable=services_accept)  
services_accepted.grid(row=4, column=1, padx=5, pady=5, sticky="w")

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

mdt = tk.BooleanVar(value=False)
ttk.Label(vas_frame, text="Ready for MDT Review").grid(row=11, column=0, padx=5, pady=5)
mdt_ready = ttk.Checkbutton(vas_frame, text="Yes", variable=mdt)  
mdt_ready.grid(row=11, column=1, padx=5, pady=5, sticky="w")

#------------------------------

# VAS Log Information

def add_new_session_popup():
    popup = tk.Toplevel(root)
    popup.title("New Session")
    popup.geometry("800x900")

    # Entry fields for case details
    ttk.Label(popup, text="Session Date").grid(row=0, column=0, padx=5, pady=5)
    session_date_entry = DateEntry(popup, width=12, background='darkblue', foreground='white', borderwidth=2)
    session_date_entry.grid(row=0, column=1, padx=5, pady=5)

    ttk.Label(popup, text="Start Time").grid(row=1, column=0, padx=5, pady=5)
    start_time_entry = ttk.Combobox(popup)
    start_time_entry.grid(row=1, column=1, padx=5, pady=5)

    ttk.Label(popup, text="End Time").grid(row=2, column=0, padx=5, pady=5)
    end_start_entry = ttk.Combobox(popup) 
    end_start_entry.grid(row=2, column=1, padx=5, pady=5)

    ttk.Label(popup, text="Prep").grid(row=3, column=0, padx=5, pady=5)
    prep_entry = ttk.Combobox(popup)
    prep_entry.grid(row=3, column=1, padx=5, pady=5)

    ttk.Label(popup, text="Session Status").grid(row=4, column=0, padx=5, pady=5)
    session_status_entry = ttk.Combobox(popup)
    session_status_entry.grid(row=4, column=1, padx=5, pady=5)

    ttk.Label(popup, text="Funding Source").grid(row=5, column=0, padx=5, pady=5)
    funding_source_entry = ttk.Combobox(popup)
    funding_source_entry.grid(row=5, column=1, padx=5, pady=5)

    ttk.Label(popup, text="Location").grid(row=6, column=0, padx=5, pady=5)
    location_entry = ttk.Combobox(popup)
    location_entry.grid(row=6, column=1, padx=5, pady=5)

    ttk.Label(popup, text="Provider Agency").grid(row=7, column=0, padx=5, pady=5)
    provider_agency_entry = ttk.Combobox(popup)
    provider_agency_entry.grid(row=7, column=1, padx=5, pady=5)

    ttk.Label(popup, text="Provider Employee").grid(row=8, column=0, padx=5, pady=5)
    provider_employee_entry = ttk.Combobox(popup)
    provider_employee_entry.grid(row=8, column=1, padx=5, pady=5)

    ttk.Label(popup, text="Attendees").grid(row=9, column=0, padx=5, pady=5)
    attendee1Check = tk.BooleanVar(value=False)
    attendee2Check = tk.BooleanVar(value=False)
    attendee3Check = tk.BooleanVar(value=False)
    attendee4Check = tk.BooleanVar(value=False)
    attendee1 = ttk.Checkbutton(popup, text="Billie Badguys", variable=attendee1Check).grid(row=9, column=1, sticky="w")
    attendee2 = ttk.Checkbutton(popup, text="Bobbie RRose", variable=attendee2Check).grid(row=9, column=2, sticky="w")
    attendee3 = ttk.Checkbutton(popup, text="Candi Rose", variable=attendee3Check).grid(row=10, column=1, sticky="w")
    attendee4 = ttk.Checkbutton(popup, text="Cindi Rose", variable=attendee4Check).grid(row=10, column=2, sticky="w")

    ttk.Label(popup, text="Services Provided").grid(row=11, column=0, padx=5, pady=5)
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
    service1 = ttk.Checkbutton(popup, text="Legal Services", variable=service1Check).grid(row=11, column=1, sticky="w")
    service2 = ttk.Checkbutton(popup, text="Transportation", variable=service2Check).grid(row=11, column=2, sticky="w")
    service3 = ttk.Checkbutton(popup, text="Victim Support", variable=service3Check).grid(row=12, column=1, sticky="w")
    service4 = ttk.Checkbutton(popup, text="1-2 Week Follow-up Call", variable=service4Check).grid(row=12, column=2, sticky="w")
    service5 = ttk.Checkbutton(popup, text="2. Personal Court Education", variable=service5Check).grid(row=13, column=1, sticky="w")
    service6 = ttk.Checkbutton(popup, text="24 -- hour crisis line cal", variable=service6Check).grid(row=13, column=2, sticky="w")
    service7 = ttk.Checkbutton(popup, text="3a. Info & Support - MDT response", variable=service7Check).grid(row=14, column=1, sticky="w")
    service8 = ttk.Checkbutton(popup, text="3b. Information & Support - Court", variable=service8Check).grid(row=14, column=2, sticky="w")
    service9 = ttk.Checkbutton(popup, text="3bi Personal advocacy", variable=service9Check).grid(row=15, column=1, sticky="w")
    service10 = ttk.Checkbutton(popup, text="6--8 Week Follow-up Call", variable=service10Check).grid(row=15, column=2, sticky="w")
    service11 = ttk.Checkbutton(popup, text="B2. Victim Advocacy/Accompaniment to Medical Forensic Exam", variable=service11Check).grid(row=16, column=1, sticky="w")
    service12 = ttk.Checkbutton(popup, text="Collected Survey", variable=service12Check).grid(row=16, column=2, sticky="w")
    service13 = ttk.Checkbutton(popup, text="Criminal Justice support/advocacy", variable=service13Check).grid(row=17, column=1, sticky="w")
    service14 = ttk.Checkbutton(popup, text="Compensation Claim Filing", variable=service14Check).grid(row=17, column=2, sticky="w")
    service15 = ttk.Checkbutton(popup, text="Emergency Crisis Intervention", variable=service15Check).grid(row=18, column=1, sticky="w")
    service16 = ttk.Checkbutton(popup, text="Crisis Counseling", variable=service16Check).grid(row=18, column=2, sticky="w")
    service17 = ttk.Checkbutton(popup, text="Gave Educational Information", variable=service17Check).grid(row=19, column=1, sticky="w")
    service18 = ttk.Checkbutton(popup, text="Follow-up", variable=service18Check).grid(row=19, column=2, sticky="w")
    service19 = ttk.Checkbutton(popup, text="Homeless support group", variable=service19Check).grid(row=20, column=1, sticky="w")
    service20 = ttk.Checkbutton(popup, text="Initial Meeting with Caregiver", variable=service20Check).grid(row=20, column=2, sticky="w")
    service21 = ttk.Checkbutton(popup, text="Initial Telephone Call", variable=service21Check).grid(row=21, column=1, sticky="w")
    service22 = ttk.Checkbutton(popup, text="Mailed Brochure", variable=service22Check).grid(row=21, column=2, sticky="w")
    service23 = ttk.Checkbutton(popup, text="Orientation to Center for FI", variable=service23Check).grid(row=22, column=1, sticky="w")
    service24 = ttk.Checkbutton(popup, text="Post Interview Crisis Counseling", variable=service24Check).grid(row=22, column=2, sticky="w")
    service25 = ttk.Checkbutton(popup, text="Pre-Interview Family Call", variable=service25Check).grid(row=23, column=1, sticky="w")
    service26 = ttk.Checkbutton(popup, text="Shelter/safehouse Referral", variable=service26Check).grid(row=23, column=2, sticky="w")
    service27 = ttk.Checkbutton(popup, text="Survey Distributed", variable=service27Check).grid(row=24, column=1, sticky="w")
    service28 = ttk.Checkbutton(popup, text="Survey Recieved", variable=service28Check).grid(row=24, column=2, sticky="w")
    service29 = ttk.Checkbutton(popup, text="Telephone Follow-up", variable=service29Check).grid(row=25, column=1, sticky="w")
    service30 = ttk.Checkbutton(popup, text="Unscheduled Call", variable=service30Check).grid(row=25, column=2, sticky="w")

    ttk.Label(popup, text="Comments").grid(row=26, column=0, padx=5, pady=5)
    session_comments_entry = ttk.Entry(popup)
    session_comments_entry.grid(row=26, column=1, padx=5, pady=5)

    ttk.Label(popup, text="VA Session Custom Field 1").grid(row=27, column=0, padx=5, pady=5)
    session_custom_one_entry = ttk.Entry(popup)
    session_custom_one_entry.grid(row=27, column=1, padx=5, pady=5)

    ttk.Label(popup, text="VA Session Custom Field 2").grid(row=28, column=0, padx=5, pady=5)
    session_custom_two_entry = ttk.Entry(popup)
    session_custom_two_entry.grid(row=28, column=1, padx=5, pady=5)

    ttk.Label(popup, text="VA Session Custom Field 3").grid(row=29, column=0, padx=5, pady=5)
    session_custom_three_entry = ttk.Entry(popup)
    session_custom_three_entry.grid(row=29, column=1, padx=5, pady=5)

    # Update and Cancel buttons
    ttk.Button(popup, text="Save", command=lambda: [popup.destroy()]).grid(row=31, column=0, padx=5, pady=5)
    ttk.Button(popup, text="Cancel", command=lambda: [popup.destroy()]).grid(row=31, column=1, padx=5, pady=5)


vas_log_frame = tk.LabelFrame(scrollable_frame, text="Victim Advocacy Services Log", padx=10, pady=10)
vas_log_frame.pack(fill="x", padx=10, pady=5)

ttk.Button(vas_log_frame, text="Add New Session Log", command=add_new_session_popup).grid(row=0, column=0, padx=5, pady=5)
ttk.Button(vas_log_frame, text="Details").grid(row=0, column=1, padx=5, pady=5)
ttk.Button(vas_log_frame, text="Newer Records").grid(row=0, column=2, padx=5, pady=5)
ttk.Button(vas_log_frame, text="Older Records").grid(row=0, column=3, padx=5, pady=5)

ttk.Label(vas_log_frame, text="Date").grid(row=1, column=1)
session_date = ttk.Entry(vas_log_frame).grid(row=2, column=1)

ttk.Label(vas_log_frame, text="Start Time").grid(row=1, column=2)
start_time = ttk.Entry(vas_log_frame).grid(row=2, column=2)

ttk.Label(vas_log_frame, text="End Time").grid(row=1, column=3)
end_time = ttk.Entry(vas_log_frame).grid(row=2, column=3)

ttk.Label(vas_log_frame, text="Status").grid(row=1, column=4)
session_status = ttk.Entry(vas_log_frame).grid(row=2, column=4)
#------------------------------

# Crime Compensation Application Section
crime_comp_app_frame = tk.LabelFrame(scrollable_frame, text="Crime Compensation Application", padx=10, pady=10)
crime_comp_app_frame.pack(fill="x", padx=10, pady=5)

ttk.Label(crime_comp_app_frame, text="State Claim Representative").grid(row=0, column=0, padx=5, pady=5)
state_claim_rep = ttk.Entry(crime_comp_app_frame)  
state_claim_rep.grid(row=0, column=1, padx=5, pady=5)

birth_cert = tk.BooleanVar(value=False)
ttk.Label(crime_comp_app_frame, text="Have Birth Certificate").grid(row=1, column=0, padx=5, pady=5)
has_birth_cert = ttk.Checkbutton(crime_comp_app_frame, variable=birth_cert)  
has_birth_cert.grid(row=1, column=1, padx=5, pady=5, sticky="w")

police_report = tk.BooleanVar(value=False)
ttk.Label(crime_comp_app_frame, text="Have Police Report").grid(row=2, column=0, padx=5, pady=5)
has_police_report = ttk.Checkbutton(crime_comp_app_frame, variable=police_report)  
has_police_report.grid(row=2, column=1, padx=5, pady=5, sticky="w")

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
# -Screenings Given Section
def edit_screening_instrument_popup():
    popup = tk.Toplevel(root)
    popup.title("Edit Screening Instrument")
    popup.geometry("800x500")

    ttk.Label(popup, text="Action", foreground='black').grid(row=1, column=0, padx=5, pady=5)

    ttk.Label(popup, text="Screening Instrument Name", foreground='black').grid(row=1, column=2, padx=5, pady=5)
    screening_date_entry = DateEntry(popup, width=12, background='darkblue', foreground='white', borderwidth=2)
    screening_date_entry.grid(row=2, column=2, padx=5, pady=5)

    ttk.Label(popup, text="Source", foreground='black').grid(row=1, column=3, padx=5, pady=5)
    provider_agency_entry = ttk.Combobox(popup)
    provider_agency_entry.grid(row=2, column=3, padx=5, pady=5)

    ttk.Label(popup, text="# of Measures", foreground='black').grid(row=1, column=4, padx=5, pady=5)
    provider_personnel_entry = ttk.Combobox(popup) 
    provider_personnel_entry.grid(row=2, column=4, padx=5, pady=5)

    # Update and Cancel buttons
    ttk.Button(popup, text="Edit", command=lambda: [popup.destroy()]).grid(row=2, column=0, padx=5, pady=5)
    ttk.Button(popup, text="Delete", command=lambda: [popup.destroy()]).grid(row=2, column=1, padx=5, pady=5)

def add_new_screening_popup():
    popup = tk.Toplevel(root)
    popup.title("Add New Screening")
    popup.geometry("900x500")

    ttk.Label(popup, text="* Instrument, Agency, and Personnel Fields are Required").grid(row=0, column=0, padx=5, pady=5)

    ttk.Label(popup, text="Scores of this Screening's Measures").grid(row=0, column=4, padx=5, pady=5)
    ttk.Entry(popup).grid(row=1, column=4, padx=5, pady=5)

    ttk.Label(popup, text="Screening Instrument", foreground='black').grid(row=1, column=0, padx=5, pady=5)
    screening_instrument_entry = ttk.Combobox(popup)
    screening_instrument_entry.grid(row=1, column=1, padx=5, pady=5)

    ttk.Button(popup, text="Add Screening Instrument", command=edit_screening_instrument_popup).grid(row=1, column=2, padx=5, pady=5)

    ttk.Label(popup, text="Screening Date", foreground='black').grid(row=2, column=0, padx=5, pady=5)
    screening_date_entry = DateEntry(popup, width=12, background='darkblue', foreground='white', borderwidth=2)
    screening_date_entry.grid(row=2, column=1, padx=5, pady=5)

    ttk.Label(popup, text="Provider Agency", foreground='black').grid(row=3, column=0, padx=5, pady=5)
    provider_agency_entry = ttk.Combobox(popup)
    provider_agency_entry.grid(row=3, column=1, padx=5, pady=5)

    ttk.Label(popup, text="Provider Personnel", foreground='black').grid(row=4, column=0, padx=5, pady=5)
    provider_personnel_entry = ttk.Combobox(popup) 
    provider_personnel_entry.grid(row=4, column=1, padx=5, pady=5)

    ttk.Label(popup, text="Functional Impairment").grid(row=5, column=0, padx=5, pady=5)
    functional_impairment_entry = ttk.Entry(popup)
    functional_impairment_entry.grid(row=5, column=1, padx=5, pady=5)

    ttk.Label(popup, text="Comments").grid(row=6, column=0, padx=5, pady=5)
    _screening_commets_entry = ttk.Entry(popup)
    _screening_commets_entry.grid(row=6, column=1, padx=5, pady=5)

    # Update and Cancel buttons
    ttk.Button(popup, text="Update", command=lambda: [popup.destroy()]).grid(row=14, column=0, padx=5, pady=5)
    ttk.Button(popup, text="Cancel", command=lambda: [popup.destroy()]).grid(row=14, column=1, padx=5, pady=5)


screenings_frame = tk.LabelFrame(scrollable_frame, text="Screenings Given", padx=10, pady=10)
screenings_frame.pack(fill="x", padx=10, pady=5)

#Add New Screening button
ttk.Button(screenings_frame, text="Add New Screening", command=add_new_screening_popup).grid(row=0, column=0, padx=5, pady=5)

ttk.Label(screenings_frame, text="Action").grid(row=1, column=0, padx=5, pady=5)
date_requested = ttk.Label(screenings_frame)  
date_requested.grid(row=2, column=1, padx=5, pady=5)


ttk.Label(screenings_frame, text="Screening Instrument Name").grid(row=1, column=2, padx=5, pady=5)
requested_by = ttk.Combobox(screenings_frame, values=["Person 1", "Person 2"])  
requested_by.grid(row=2, column=2, padx=5, pady=5)

ttk.Label(screenings_frame, text="Date").grid(row=1, column=3, padx=5, pady=5)
by_subpeona = ttk.Combobox(screenings_frame, values=["Person 1", "Person 2"])  
by_subpeona.grid(row=2, column=3, padx=5, pady=5)


ttk.Label(screenings_frame, text="Provider Personnel").grid(row=1, column=4, padx=5, pady=5)
authorized_by = ttk.Combobox(screenings_frame, values=["Person 1", "Person 2"])  
authorized_by.grid(row=2, column=4, padx=5, pady=5)

#--------------------------------------

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