import tkinter as tk
from database.config import load_config
from database.connect import connect

heading_font = ("Helvetica", 18, "bold")
bold_label_font = ("Helvetica", 12, "bold")
normal_text_font = ("Helvetica", 12)
entry_width = 30

padx = 10
pady = 5

def load_first_100_patients():

    patient_data = []
    config = load_config()
    conn = connect(config)
    with conn.cursor() as cur:
        cur.execute("SELECT * FROM personal_profile ORDER BY last_name FETCH FIRST 100 ROWS ONLY") 
        row = cur.fetchone()
                
        while row is not None:
            patient_data.append(row)
            row = cur.fetchone()

        return patient_data
    
# to populate the details of the selected patient
def show_patient_details(patient):
    # Clear previous patient details
    for widget in details_frame.winfo_children():
        widget.destroy()

    tk.Label(details_frame, text="First Name:", font=bold_label_font).grid(column=0, row=0, sticky="e", padx=padx, pady=pady)
    tk.Label(details_frame, text=patient[0], font=normal_text_font).grid(column=1, row=0, sticky="w", padx=padx, pady=pady)

    tk.Label(details_frame, text="Last Name:", font=bold_label_font).grid(column=0, row=1, sticky="e", padx=padx, pady=pady)
    tk.Label(details_frame, text=patient[2], font=normal_text_font).grid(column=1, row=1, sticky="w", padx=padx, pady=pady)

    tk.Label(details_frame, text="Middle Initial:", font=bold_label_font).grid(column=0, row=2, sticky="e", padx=padx, pady=pady)
    tk.Label(details_frame, text=patient[1], font=normal_text_font).grid(column=1, row=2, sticky="w", padx=padx, pady=pady)

    tk.Label(details_frame, text="Nickname:", font=bold_label_font).grid(column=0, row=3, sticky="e", padx=padx, pady=pady)
    tk.Label(details_frame, text=patient[3], font=normal_text_font).grid(column=1, row=3, sticky="w", padx=padx, pady=pady)

    tk.Label(details_frame, text="Date of Birth:", font=bold_label_font).grid(column=0, row=4, sticky="e", padx=padx, pady=pady)
    tk.Label(details_frame, text=patient[4], font=normal_text_font).grid(column=1, row=4, sticky="w", padx=padx, pady=pady)

    tk.Label(details_frame, text="Race:", font=bold_label_font).grid(column=0, row=5, sticky="e", padx=padx, pady=pady)
    tk.Label(details_frame, text=patient[8], font=normal_text_font).grid(column=1, row=5, sticky="w", padx=padx, pady=pady)

    tk.Label(details_frame, text="Social Security Number:", font=bold_label_font).grid(column=0, row=6, sticky="e", padx=padx, pady=pady)
    tk.Label(details_frame, text=patient[5], font=normal_text_font).grid(column=1, row=6, sticky="w", padx=padx, pady=pady)

    tk.Label(details_frame, text="Biological Gender:", font=bold_label_font).grid(column=0, row=7, sticky="e", padx=padx, pady=pady)
    tk.Label(details_frame, text=patient[6], font=normal_text_font).grid(column=1, row=7, sticky="w", padx=padx, pady=pady)

    tk.Label(details_frame, text="Religion:", font=bold_label_font).grid(column=0, row=8, sticky="e", padx=padx, pady=pady)
    tk.Label(details_frame, text=patient[7], font=normal_text_font).grid(column=1, row=8, sticky="w", padx=padx, pady=pady)

    tk.Label(details_frame, text="Language:", font=bold_label_font).grid(column=0, row=9, sticky="e", padx=padx, pady=pady)
    tk.Label(details_frame, text=patient[9], font=normal_text_font).grid(column=1, row=9, sticky="w", padx=padx, pady=pady)

    tk.Label(details_frame, text="VOCA Classifications:", font=bold_label_font).grid(column=0, row=10, sticky="e", padx=padx, pady=pady)
    tk.Label(details_frame, text=patient[10], font=normal_text_font).grid(column=1, row=10, sticky="w", padx=padx, pady=pady)

    tk.Label(details_frame, text="Comments:", font=bold_label_font).grid(column=2, row=0, sticky="e", padx=padx, pady=pady)
    tk.Label(details_frame, text=patient[11], font=normal_text_font, wraplength=500).grid(column=3, row=0, sticky="w", padx=padx, pady=pady)

    tk.Label(details_frame, text="Prior Convictions:", font=bold_label_font).grid(column=2, row=1, sticky="e", padx=padx, pady=pady)
    tk.Label(details_frame, text="Yes" if patient[12] else "No", font=normal_text_font).grid(column=3, row=1, sticky="w", padx=padx, pady=pady)

    tk.Label(details_frame, text="Convicted of Crimes Against Children:", font=bold_label_font).grid(column=2, row=2, sticky="e", padx=padx, pady=pady)
    tk.Label(details_frame, text="Yes" if patient[13] else "No", font=normal_text_font).grid(column=3, row=2, sticky="w", padx=padx, pady=pady)

    tk.Label(details_frame, text="Sexual Offender:", font=bold_label_font).grid(column=2, row=3, sticky="e", padx=padx, pady=pady)
    tk.Label(details_frame, text="Yes" if patient[14] else "No", font=normal_text_font).grid(column=3, row=3, sticky="w", padx=padx, pady=pady)

    tk.Label(details_frame, text="Sexual Predator:", font=bold_label_font).grid(column=2, row=4, sticky="e", padx=padx, pady=pady)
    tk.Label(details_frame, text="Yes" if patient[15] else "No", font=normal_text_font).grid(column=3, row=4, sticky="w", padx=padx, pady=pady)

#to filter patients based on search
def search_patients(event=None):
    global filtered_patients
    config = load_config()
    conn = connect(config)

    search_query = search_entry.get().lower()
    filtered_patients = []

    with conn.cursor() as cur:
        cur.execute("SELECT * FROM personal_profile WHERE CONCAT(first_name, \' \', middle_initial, \' \', last_name)~*\'{0}\' OR CONCAT(first_name, \' \', last_name)~*\'{0}\' ORDER BY last_name FETCH FIRST 100 ROWS ONLY".format(search_query))
        row = cur.fetchone()

        while row is not None:
            filtered_patients.append(row)
            row = cur.fetchone()

    update_patient_list(filtered_patients)

#update the patient list based on search 
def update_patient_list(filtered_patients):
    patient_list.delete(0, tk.END)
    for patient in filtered_patients:
        patient_list.insert(tk.END, f"{patient[0]} {patient[1]}. {patient[2]}")
    patient_list.bind("<Double-1>", on_patient_select_from_list)

# callback function when a patient is selected from the list
def on_patient_select_from_list(event):
    selected_index = patient_list.curselection()
    if selected_index:
        patient_index = selected_index[0]
        show_patient_details(filtered_patients[patient_index])

window = tk.Tk()
window.geometry("1600x900")
window.title("Patient Lookup")

# load patient data
file_path = 'data.csv'  # Update with your CSV file name


patient_data = load_first_100_patients()
filtered_patients = patient_data  # Initialize filtered_patients

# creates frame for search and patient list
search_frame = tk.Frame(window)
search_frame.grid(row=0, column=0, padx=20, pady=20)

# create search entry
tk.Label(search_frame, text="Search Patient:", font=bold_label_font).grid(row=0, column=0, padx=padx, pady=pady)
search_entry = tk.Entry(search_frame, font=normal_text_font, width=entry_width)
search_entry.grid(row=0, column=1, padx=padx, pady=pady)
search_entry.bind("<KeyRelease>", search_patients)

# creates a listbox to display search results
patient_list = tk.Listbox(search_frame, width=entry_width * 2, height=10, font=normal_text_font)
patient_list.grid(row=1, column=0, columnspan=2, padx=padx, pady=pady)

#creates frame for patient details
details_frame = tk.Frame(window)
details_frame.grid(row=1, column=0, columnspan=3, padx=20, pady=20)

window.mainloop()
