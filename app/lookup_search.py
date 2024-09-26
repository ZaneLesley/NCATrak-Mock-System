import tkinter as tk
from tkinter import ttk
import pandas as pd

heading_font = ("Helvetica", 18, "bold")
bold_label_font = ("Helvetica", 12, "bold")
normal_text_font = ("Helvetica", 12)
entry_width = 30

padx = 10
pady = 5

# load patient data from CSV file
def load_patient_data(file_path):
    return pd.read_csv(file_path)

# to populate the details of the selected patient
def show_patient_details(patient_index):
    # Clear previous patient details
    for widget in details_frame.winfo_children():
        widget.destroy()

    patient = patient_data.iloc[patient_index]

    tk.Label(details_frame, text="First Name:", font=bold_label_font).grid(column=0, row=0, sticky="e", padx=padx, pady=pady)
    tk.Label(details_frame, text=patient['first_name'], font=normal_text_font).grid(column=1, row=0, sticky="w", padx=padx, pady=pady)

    tk.Label(details_frame, text="Last Name:", font=bold_label_font).grid(column=0, row=1, sticky="e", padx=padx, pady=pady)
    tk.Label(details_frame, text=patient['last_name'], font=normal_text_font).grid(column=1, row=1, sticky="w", padx=padx, pady=pady)

    tk.Label(details_frame, text="Middle Initial:", font=bold_label_font).grid(column=0, row=2, sticky="e", padx=padx, pady=pady)
    tk.Label(details_frame, text=patient['second_name'], font=normal_text_font).grid(column=1, row=2, sticky="w", padx=padx, pady=pady)

    tk.Label(details_frame, text="Nickname:", font=bold_label_font).grid(column=0, row=3, sticky="e", padx=padx, pady=pady)
    tk.Label(details_frame, text=patient['nickname'], font=normal_text_font).grid(column=1, row=3, sticky="w", padx=padx, pady=pady)

    tk.Label(details_frame, text="Date of Birth:", font=bold_label_font).grid(column=0, row=4, sticky="e", padx=padx, pady=pady)
    tk.Label(details_frame, text=patient['date_of_birth'], font=normal_text_font).grid(column=1, row=4, sticky="w", padx=padx, pady=pady)

    tk.Label(details_frame, text="Race:", font=bold_label_font).grid(column=0, row=5, sticky="e", padx=padx, pady=pady)
    tk.Label(details_frame, text=patient['race'], font=normal_text_font).grid(column=1, row=5, sticky="w", padx=padx, pady=pady)

    tk.Label(details_frame, text="Social Security Number:", font=bold_label_font).grid(column=0, row=6, sticky="e", padx=padx, pady=pady)
    tk.Label(details_frame, text=patient['ssn'], font=normal_text_font).grid(column=1, row=6, sticky="w", padx=padx, pady=pady)

    tk.Label(details_frame, text="Biological Gender:", font=bold_label_font).grid(column=0, row=7, sticky="e", padx=padx, pady=pady)
    tk.Label(details_frame, text=patient['bio_gender'], font=normal_text_font).grid(column=1, row=7, sticky="w", padx=padx, pady=pady)

    tk.Label(details_frame, text="Religion:", font=bold_label_font).grid(column=0, row=8, sticky="e", padx=padx, pady=pady)
    tk.Label(details_frame, text=patient['religion'], font=normal_text_font).grid(column=1, row=8, sticky="w", padx=padx, pady=pady)

    tk.Label(details_frame, text="Language:", font=bold_label_font).grid(column=0, row=9, sticky="e", padx=padx, pady=pady)
    tk.Label(details_frame, text=patient['language'], font=normal_text_font).grid(column=1, row=9, sticky="w", padx=padx, pady=pady)

    tk.Label(details_frame, text="VOCA Classifications:", font=bold_label_font).grid(column=0, row=10, sticky="e", padx=padx, pady=pady)
    tk.Label(details_frame, text=patient['voca_classifications'], font=normal_text_font).grid(column=1, row=10, sticky="w", padx=padx, pady=pady)

    tk.Label(details_frame, text="Comments:", font=bold_label_font).grid(column=0, row=11, sticky="e", padx=padx, pady=pady)
    tk.Label(details_frame, text=patient['comments'], font=normal_text_font).grid(column=1, row=11, sticky="w", padx=padx, pady=pady)

    tk.Label(details_frame, text="Prior Convictions:", font=bold_label_font).grid(column=0, row=12, sticky="e", padx=padx, pady=pady)
    tk.Label(details_frame, text="Yes" if patient['prior_convictions'] else "No", font=normal_text_font).grid(column=1, row=12, sticky="w", padx=padx, pady=pady)

    tk.Label(details_frame, text="Convicted of Crimes Against Children:", font=bold_label_font).grid(column=0, row=13, sticky="e", padx=padx, pady=pady)
    tk.Label(details_frame, text="Yes" if patient['convicted_against_children'] else "No", font=normal_text_font).grid(column=1, row=13, sticky="w", padx=padx, pady=pady)

    tk.Label(details_frame, text="Sexual Offender:", font=bold_label_font).grid(column=0, row=14, sticky="e", padx=padx, pady=pady)
    tk.Label(details_frame, text="Yes" if patient['sexual_offender'] else "No", font=normal_text_font).grid(column=1, row=14, sticky="w", padx=padx, pady=pady)

    tk.Label(details_frame, text="Sexual Predator:", font=bold_label_font).grid(column=0, row=15, sticky="e", padx=padx, pady=pady)
    tk.Label(details_frame, text="Yes" if patient['sexual_predator'] else "No", font=normal_text_font).grid(column=1, row=15, sticky="w", padx=padx, pady=pady)

#to filter patients based on search
def search_patients(event=None):
    global filtered_patients
    search_query = search_entry.get().lower()
    filtered_patients = patient_data[
        (patient_data['first_name'].str.lower().str.contains(search_query)) |
        (patient_data['last_name'].str.lower().str.contains(search_query))
    ]
    update_patient_list(filtered_patients)

#update the patient list based on search 
def update_patient_list(filtered_patients):
    patient_list.delete(0, tk.END)
    for idx, row in filtered_patients.iterrows():
        patient_list.insert(tk.END, f"{row['first_name']} {row['last_name']}")
    patient_list.bind("<Double-1>", on_patient_select_from_list)

# callback function when a patient is selected from the list
def on_patient_select_from_list(event):
    selected_index = patient_list.curselection()
    if selected_index:
        patient_index = selected_index[0]
        show_patient_details(filtered_patients.index[patient_index])

window = tk.Tk()
window.geometry("1200x800")
window.title("Patient Lookup")

# load patient data
file_path = 'data.csv'  # Update with your CSV file name
patient_data = load_patient_data(file_path)
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
