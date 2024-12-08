# people_interface.py

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import psycopg2
from configparser import ConfigParser
import os
from datetime import datetime
from tkcalendar import DateEntry
import math

# Import other interfaces for navigation
import Generaltab_interface
import MH_basic_interface
import MH_assessment
import MH_treatmentPlan_interface
import va_tab_interface
import case_notes
import database_lookup_search

class PeopleInterface(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller  # Store the controller reference

        # Database connection
        self.conn = self.get_connection()
        if self.conn is None:
            return  # Exit if connection failed

        self.current_case_id = self.get_current_case_id()
        if self.current_case_id is None:
            return  # Exit if no case ID found

        self.cac_id = self.get_cac_id()
        if self.cac_id is None:
            return  # Exit if no CAC ID found

        self.grid_rowconfigure(0, weight=1)
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

        # Window in the canvas
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")

        # Scrollbar to canvas
        canvas.configure(yscrollcommand=scrollbar.set)

        # Use grid over pack for interface linking
        canvas.grid(row=0, column=0, sticky="nsew")
        scrollbar.grid(row=0, column=1, sticky="ns")

        # Navigation Buttons
        button_frame = ttk.Frame(scrollable_frame)
        button_frame.grid(row=0, column=0, columnspan=7, padx=5, pady=5, sticky='w')

        # Create a list of tuples with button text and corresponding function placeholders
        nav_buttons = [
            ("Lookup", self.show_lookup_tab),
            ("General", self.show_general_tab),
            ("People", self.show_people_tab),
            ("Mental Health - Basic", self.show_mh_basic),
            ("Mental Health - Assessment", self.show_mh_assessment),
            ("Mental Health - Treatment Plan", self.show_mh_treatment_plan),
            ("Mental Health - Case Notes", self.show_case_notes),
            ("VA", self.show_va_tab),
        ]

        for btn_text, btn_command in nav_buttons:
            button = ttk.Button(button_frame, text=btn_text, command=btn_command)
            button.pack(side='left', padx=5)

        # Reload button - fully reloads the application
        refresh_button = ttk.Button(button_frame, text="Reload", command=controller.refresh)
        refresh_button.pack(side='right', padx=5)

        # Display current case ID
        current_case_id_file = open("case_id.txt", "r")
        current_case_id = int(current_case_id_file.readline())
        current_case_id_file.close()
        case_id_font = ("Helvetica", 10)
        tk.Label(button_frame, text=f"Case ID: {current_case_id}", font=case_id_font).pack(side='right', padx=30)

        # -------------------- Save and Cancel Buttons --------------------
        save_cancel_frame = tk.Frame(scrollable_frame)
        save_cancel_frame.grid(row=1, column=0, padx=10, pady=5, sticky='w')

        save_button = ttk.Button(save_cancel_frame, text="Save", command=self.save_changes)
        save_button.pack(side='left', padx=5)

        cancel_button = ttk.Button(save_cancel_frame, text="Cancel", command=self.cancel_changes)
        cancel_button.pack(side='left', padx=5)

        # -------------------- Header --------------------
        header_label = ttk.Label(scrollable_frame, text="PEOPLE ASSOCIATED WITH CASE", font=('Helvetica', 16))
        header_label.grid(row=2, column=0, padx=10, pady=10, sticky='w')

        # -------------------- Search Fields --------------------
        search_frame = tk.Frame(scrollable_frame)
        search_frame.grid(row=3, column=0, padx=10, pady=5, sticky='w')

        search_label = ttk.Label(search_frame, text="Search:")
        search_label.pack(side='left', padx=(0, 5))

        self.search_entry = ttk.Entry(search_frame)
        self.search_entry.pack(side='left', padx=5)
        self.search_entry.bind('<KeyRelease>', self.on_search)

        # -------------------- Add Button --------------------
        add_button = ttk.Button(scrollable_frame, text="+ Add", command=self.add_person)
        add_button.grid(row=4, column=0, padx=10, pady=5, sticky='w')

        # -------------------- Main Table --------------------
        table_frame = tk.Frame(scrollable_frame)
        table_frame.grid(row=5, column=0, padx=10, pady=10, sticky='nsew')
        scrollable_frame.grid_rowconfigure(5, weight=1)
        scrollable_frame.grid_columnconfigure(0, weight=1)

        # Define columns
        columns = ("Action", "Name", "Age", "Date of Birth", "Role", "Relationship To Victim", "Same Household", "Custody")
        self.tree = ttk.Treeview(table_frame, columns=columns, show='headings')

        # Define headings
        for col in columns:
            self.tree.heading(col, text=col)

        # Define column widths
        self.tree.column("Action", width=240, anchor='center')
        self.tree.column("Name", width=150)
        self.tree.column("Age", width=50, anchor='center')
        self.tree.column("Date of Birth", width=100, anchor='center')
        self.tree.column("Role", width=120)
        self.tree.column("Relationship To Victim", width=150)
        self.tree.column("Same Household", width=120, anchor='center')
        self.tree.column("Custody", width=100, anchor='center')

        # Create a scrollbar
        table_scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=table_scrollbar.set)
        self.tree.pack(side='left', fill='both', expand=True)
        table_scrollbar.pack(side='right', fill='y')

        # Create a custom style for the buttons
        style = ttk.Style()
        style.configure('Action.TButton', padding=(0, 0), font=('TkDefaultFont', 10))

        # Dictionary to hold action widgets and checkboxes for each item
        self.action_widgets = {}

        # Load people into the table
        self.load_people()

        # Start the update loop for action widgets and checkboxes
        self.update_action_widgets()

        # -------------------- Document Upload Section --------------------
        # Document Upload section title
        upload_title_frame = ttk.Frame(scrollable_frame)
        upload_title_frame.grid(row=6, column=0, padx=10, pady=5, sticky='w')
        ttk.Label(upload_title_frame, text="Document Upload", font=('Arial', 16)).pack(side=tk.LEFT)

        # Treeview for document uploads
        upload_frame = ttk.Frame(scrollable_frame)
        upload_frame.grid(row=7, column=0, padx=10, pady=5, sticky='nsew')
        self.upload_tree = ttk.Treeview(upload_frame, columns=("File Name", "Upload Date", "User", "Page", "Size"), show="headings")
        for col in self.upload_tree['columns']:
            self.upload_tree.heading(col, text=col)
            self.upload_tree.column(col, anchor="center", width=100)
        self.upload_tree.pack(expand=True, fill='both', padx=10, pady=10)

        # No data placeholder
        self.upload_tree.insert('', 'end', values=("No documents to display", "", "", "", ""))

        # Pagination controls for uploads
        pagination_frame = ttk.Frame(upload_frame)
        pagination_frame.pack(fill='x', padx=10, pady=5)

        self.upload_first_page_button = ttk.Button(pagination_frame, text="<<", command=self.upload_first_page)
        self.upload_first_page_button.pack(side=tk.LEFT, padx=5)

        self.upload_prev_page_button = ttk.Button(pagination_frame, text="<", command=self.upload_previous_page)
        self.upload_prev_page_button.pack(side=tk.LEFT, padx=5)

        self.upload_page_number_var = tk.IntVar(value=1)
        self.upload_page_number_label = ttk.Label(pagination_frame, textvariable=self.upload_page_number_var)
        self.upload_page_number_label.pack(side=tk.LEFT, padx=5)

        self.upload_next_page_button = ttk.Button(pagination_frame, text=">", command=self.upload_next_page)
        self.upload_next_page_button.pack(side=tk.LEFT, padx=5)

        self.upload_last_page_button = ttk.Button(pagination_frame, text=">>", command=self.upload_last_page)
        self.upload_last_page_button.pack(side=tk.LEFT, padx=5)

        # Items per page dropdown
        items_per_page_options = [5, 10, 15, 'All']
        self.upload_items_per_page_var = tk.StringVar(value='5')
        self.upload_items_per_page_dropdown = ttk.Combobox(pagination_frame, textvariable=self.upload_items_per_page_var, values=items_per_page_options, width=5)
        self.upload_items_per_page_dropdown.pack(side=tk.LEFT, padx=5)

        ttk.Label(pagination_frame, text="items per page").pack(side=tk.LEFT, padx=5)

        # File selection button
        file_nav_frame = ttk.Frame(scrollable_frame)
        file_nav_frame.grid(row=8, column=0, padx=10, pady=10, sticky='w')
        ttk.Button(file_nav_frame, text="Select Files...", command=self.select_files).pack(side=tk.LEFT, padx=10)
        #self.controller.show_frame(people_interface)



    # -------------------- Navigation Functions --------------------
    def show_lookup_tab(self):
        self.controller.show_frame(database_lookup_search.lookup_interface)

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

    # -------------------- Database Connection and Functions --------------------
    def get_connection(self):
        # Read database configuration from database.ini
        try:
            config_file = os.path.join(os.path.dirname(__file__), 'database', 'database.ini')
            parser = ConfigParser()
            parser.read(config_file)
            db_config = {}
            if parser.has_section('postgresql'):
                params = parser.items('postgresql')
                for param in params:
                    db_config[param[0]] = param[1]
            else:
                messagebox.showerror("Error", "Database configuration file not found.")
                return None
            conn = psycopg2.connect(**db_config)
            return conn
        except Exception as e:
            messagebox.showerror("Error", f"Failed to connect to the database: {e}")
            return None

    def get_current_case_id(self):
        case_id_file = open("case_id.txt", "r")
        case_id = int(case_id_file.readline())
        case_id_file.close()
        return case_id

    def get_cac_id(self):
        try:
            cur = self.conn.cursor()
            query = "SELECT cac_id FROM cac_case WHERE case_id = %s;"
            cur.execute(query, (self.current_case_id,))
            result = cur.fetchone()
            cur.close()
            if result:
                return result[0]
            else:
                messagebox.showerror("Error", "CAC ID not found for the current case.")
                return None
        except Exception as e:
            messagebox.showerror("Error", f"Failed to retrieve CAC ID: {e}")
            return None

    def load_people(self):
        # Clear existing items
        for item in self.tree.get_children():
            self.tree.delete(item)
        try:
            cur = self.conn.cursor()
            query = """
                SELECT p.person_id, p.first_name || ' ' || p.last_name AS name, 
                DATE_PART('year', AGE(p.date_of_birth)) AS age, p.date_of_birth, 
                cp.same_household, cp.custody,
                cp.role_id, cp.relationship_id
                FROM person p
                JOIN case_person cp ON p.person_id = cp.person_id
                WHERE cp.case_id = %s;
            """
            cur.execute(query, (self.current_case_id,))
            rows = cur.fetchall()
            cur.close()
            # Store data for search functionality
            self.all_people = rows
            # Insert data into treeview
            for row in rows:
                person_id = row[0]
                name = row[1] if row[1] else 'N/A'
                age = int(row[2]) if row[2] else 'N/A'
                dob = row[3].strftime('%Y-%m-%d') if row[3] else 'N/A'
                same_household = row[4]
                custody = row[5]
                role = self.get_role_name(row[6])
                relationship = self.get_relationship_name(row[7])
                values = ('', name, age, dob, role, relationship, '', '')
                self.tree.insert("", "end", iid=person_id, values=values)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load people: {e}")

    def get_role_name(self, role_id):
        role_mapping = {
            0: 'Alleged Victim/Client',
            1: 'Alleged Co-Victim',
            2: 'Alleged Offender',
            3: 'Caregiver',
            4: 'Other'
        }
        return role_mapping.get(role_id, 'N/A')

    def get_relationship_name(self, relationship_id):
        relationship_mapping = {
            0: 'Self',
            1: 'Mother',
            2: 'Biological Mother',
            3: 'Adoptive Mother',
            4: 'Step-Mother',
            5: 'Father\'s Girlfriend',
            6: 'Father',
            7: 'Biological Father',
            8: 'Adoptive Father',
            9: 'Step-Father',
            10: 'Mother\'s Boyfriend',
            11: 'Brother',
            12: 'Sister',
            13: 'Step-Brother',
            14: 'Step-Sister',
            15: 'Step-Brother',
            16: 'Step-Sister',
            17: 'Grandmother',
            18: 'Grandfather',
            19: 'Friend',
            20: 'Other Known Person'
        }
        return relationship_mapping.get(relationship_id, 'N/A')

    # -------------------- Action Buttons and Checkboxes --------------------
    def update_action_widgets(self):
        # For each visible item in the treeview, create buttons and checkboxes if they don't exist and place them
        for item in self.tree.get_children():
            # Get the bounding boxes of the relevant columns
            bbox_action = self.tree.bbox(item, column='Action')
            bbox_same_household = self.tree.bbox(item, column='Same Household')
            bbox_custody = self.tree.bbox(item, column='Custody')

            if not bbox_action or not bbox_same_household or not bbox_custody:
                continue

            # Adjust x and y to be relative to treeview widget
            x_action, y_action, width_action, height_action = bbox_action
            x_sh, y_sh, width_sh, height_sh = bbox_same_household
            x_custody, y_custody, width_custody, height_custody = bbox_custody

            if item not in self.action_widgets:
                # Create the buttons
                edit_button = ttk.Button(self.tree, text='Edit', command=lambda i=item: self.on_edit_press(i), style='Action.TButton')
                bio_button = ttk.Button(self.tree, text='Bio', command=lambda i=item: self.on_bio_press(i), style='Action.TButton')
                delete_button = ttk.Button(self.tree, text='Delete', command=lambda i=item: self.on_delete_press(i), style='Action.TButton')

                # Create the checkboxes
                sh_var = tk.BooleanVar(value=self.get_boolean_value(item, 'Same Household'))
                custody_var = tk.BooleanVar(value=self.get_boolean_value(item, 'Custody'))

                sh_checkbox = ttk.Checkbutton(self.tree, variable=sh_var, command=lambda i=item, var=sh_var: self.update_same_household(i, var))
                custody_checkbox = ttk.Checkbutton(self.tree, variable=custody_var, command=lambda i=item, var=custody_var: self.update_custody(i, var))

                role_id =  self.get_person_role_id(item)
                if role_id is not None and role_id[0] == 0:
                    sh_checkbox.config(state='disabled')
                    custody_checkbox.config(state='disabled')

                self.action_widgets[item] = {
                    'edit_button': edit_button,
                    'bio_button': bio_button,
                    'delete_button': delete_button,
                    'sh_checkbox': sh_checkbox,
                    'custody_checkbox': custody_checkbox,
                }
            else:
                widgets = self.action_widgets[item]
                edit_button = widgets['edit_button']
                bio_button = widgets['bio_button']
                delete_button = widgets['delete_button']
                sh_checkbox = widgets['sh_checkbox']
                custody_checkbox = widgets['custody_checkbox']

            # Place the buttons
            edit_button.place(x=x_action + 10, y=y_action, width=60, height=height_action)
            bio_button.place(x=x_action + 80, y=y_action, width=60, height=height_action)
            delete_button.place(x=x_action + 150, y=y_action, width=60, height=height_action)

            # Place the checkboxes
            sh_checkbox.place(x=x_sh + width_sh // 2 - 10, y=y_sh + 2)
            custody_checkbox.place(x=x_custody + width_custody // 2 - 10, y=y_custody + 2)

        # Remove widgets for items that no longer exist
        items_to_remove = []
        for item in self.action_widgets:
            if item not in self.tree.get_children():
                widgets = self.action_widgets[item]
                widgets['edit_button'].destroy()
                widgets['bio_button'].destroy()
                widgets['delete_button'].destroy()
                widgets['sh_checkbox'].destroy()
                widgets['custody_checkbox'].destroy()
                items_to_remove.append(item)
        for item in items_to_remove:
            del self.action_widgets[item]

        # Schedule the next update
        self.after(100, self.update_action_widgets)

    def get_boolean_value(self, item, column_name):
        try:
            cur = self.conn.cursor()
            if column_name == 'Same Household':
                query = "SELECT same_household FROM case_person WHERE person_id = %s AND case_id = %s;"
            elif column_name == 'Custody':
                query = "SELECT custody FROM case_person WHERE person_id = %s AND case_id = %s;"
            else:
                return False
            cur.execute(query, (item, self.current_case_id))
            result = cur.fetchone()
            cur.close()
            return result[0] if result and result[0] is not None else False
        except Exception as e:
            print(f"Error fetching boolean value for {column_name}: {e}")
            return False

    def on_edit_press(self, item):
        person_id = item
        PersonalProfileForm(self, person_id, mode='edit')

    def on_bio_press(self, item):
        person_id = item
        PersonalProfileForm(self, person_id, mode='bio')
    
    def get_person_role_id(self, item):
        try:
            cur = self.conn.cursor()
            # Get person role from database
            person_query = "SELECT role_id FROM case_person WHERE person_id = %s AND case_id = %s;"
            cur.execute(person_query, (item, self.current_case_id))
            id = cur.fetchone()
            cur.close()
            return id
        except Exception as e:
            messagebox.showerror("Error", f"Failed to get person role id: {e}")

    def on_delete_press(self, item):
        #Check if person has role "Alleged Victim/Client"
        id = self.get_person_role_id(item)
        if id is not None and id[0] == 0:
            messagebox.showerror("Error", "Cannot delete person with role: Alleged Victim/Client")
            return

        # Confirm deletion
        response = messagebox.askyesno("Confirm Deletion", "Are you sure you want to delete this person from the case?")
        if response:
            try:
                cur = self.conn.cursor()
                # Delete from case_person table
                delete_query = "DELETE FROM case_person WHERE person_id = %s AND case_id = %s;"
                cur.execute(delete_query, (item, self.current_case_id))
                self.conn.commit()
                cur.close()
                # Remove from treeview
                self.tree.delete(item)
                messagebox.showinfo("Success", "Person deleted from the case.")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to delete person: {e}")

    def update_same_household(self, item, var):
        # Update the 'same_household' field in the database
        value = var.get()
        try:
            cur = self.conn.cursor()
            query = "UPDATE case_person SET same_household = %s WHERE person_id = %s AND case_id = %s;"
            cur.execute(query, (value, item, self.current_case_id))
            self.conn.commit()
            cur.close()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to update Same Household: {e}")

    def update_custody(self, item, var):
        # Update the 'custody' field in the database
        value = var.get()
        try:
            cur = self.conn.cursor()
            query = "UPDATE case_person SET custody = %s WHERE person_id = %s AND case_id = %s;"
            cur.execute(query, (value, item, self.current_case_id))
            self.conn.commit()
            cur.close()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to update Custody: {e}")

    # -------------------- Search Functionality --------------------
    def on_search(self, event):
        search_text = self.search_entry.get().lower()
        # Clear existing items
        for item in self.tree.get_children():
            self.tree.delete(item)
        # Filter the data
        for row in self.all_people:
            person_id = row[0]
            name = row[1] if row[1] else 'N/A'
            if search_text in name.lower():
                age = int(row[2]) if row[2] else 'N/A'
                dob = row[3].strftime('%Y-%m-%d') if row[3] else 'N/A'
                same_household = row[4]
                custody = row[5]
                role = self.get_role_name(row[6])
                relationship = self.get_relationship_name(row[7])
                values = ('', name, age, dob, role, relationship, '', '')
                self.tree.insert("", "end", iid=person_id, values=values)

    # -------------------- Add Person Functionality --------------------
    def add_person(self):
        LookupPersonForm(self)

    # -------------------- Save and Cancel Changes --------------------
    def save_changes(self):
        messagebox.showinfo("Info", "Changes have been saved.")
        # Implement any additional save functionality here.

    def cancel_changes(self):
        # Reload data from the database
        self.load_people()
        messagebox.showinfo("Info", "Changes have been canceled.")

    # -------------------- Document Upload Methods --------------------
    def select_files(self):
        file_paths = filedialog.askopenfilenames()
        if file_paths:
            for file_path in file_paths:
                file_name = os.path.basename(file_path)
                # For demonstration, we will insert dummy data into the upload treeview
                self.upload_tree.insert('', 'end', values=(file_name, 'Today', 'User', '1', '1MB'))

    def upload_first_page(self):
        messagebox.showinfo("Pagination", "First page clicked (Uploads).")

    def upload_previous_page(self):
        messagebox.showinfo("Pagination", "Previous page clicked (Uploads).")

    def upload_next_page(self):
        messagebox.showinfo("Pagination", "Next page clicked (Uploads).")

    def upload_last_page(self):
        messagebox.showinfo("Pagination", "Last page clicked (Uploads).")

# -------------------- LookupPersonForm Class --------------------
class LookupPersonForm(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.title("Lookup Person")
        self.conn = master.conn
        self.cac_id = master.cac_id
        self.case_id = master.current_case_id
        self.master = master

        # Last Name Entry and Buttons on the same row
        top_frame = ttk.Frame(self)
        top_frame.pack(side='top', fill='x', padx=10, pady=10)

        ttk.Label(top_frame, text="Last Name:").pack(side='left', padx=(0,5))
        self.last_name_var = tk.StringVar()
        self.last_name_entry = ttk.Entry(top_frame, textvariable=self.last_name_var)
        self.last_name_entry.pack(side='left', padx=5)
        self.last_name_entry.insert(0, "e.g. Smith")
        self.last_name_entry.bind("<FocusIn>", self.clear_placeholder)

        # Buttons
        search_button = ttk.Button(top_frame, text="SEARCH", command=self.search_person)
        search_button.pack(side='left', padx=5)

        no_match_button = ttk.Button(top_frame, text="NO MATCH FOUND", command=self.no_match_found)
        no_match_button.pack(side='left', padx=5)

        close_button = ttk.Button(top_frame, text="CLOSE", command=self.destroy)
        close_button.pack(side='left', padx=5)

        # Results Treeview
        self.tree = ttk.Treeview(self, columns=("Last Name", "First Name", "Middle Name", "Alias"), show='headings')
        self.tree.heading("Last Name", text="Last Name")
        self.tree.heading("First Name", text="First Name")
        self.tree.heading("Middle Name", text="Middle Name")
        self.tree.heading("Alias", text="Alias")
        self.tree.pack(expand=True, fill='both', padx=10, pady=10)

        # Pagination Controls
        pagination_frame = ttk.Frame(self)
        pagination_frame.pack(fill='x', padx=10, pady=5)

        self.first_page_button = ttk.Button(pagination_frame, text="<<", command=self.first_page)
        self.first_page_button.pack(side=tk.LEFT, padx=5)

        self.prev_page_button = ttk.Button(pagination_frame, text="<", command=self.previous_page)
        self.prev_page_button.pack(side=tk.LEFT, padx=5)

        self.page_number_var = tk.IntVar(value=1)
        self.page_number_label = ttk.Label(pagination_frame, textvariable=self.page_number_var)
        self.page_number_label.pack(side=tk.LEFT, padx=5)

        self.next_page_button = ttk.Button(pagination_frame, text=">", command=self.next_page)
        self.next_page_button.pack(side=tk.LEFT, padx=5)

        self.last_page_button = ttk.Button(pagination_frame, text=">>", command=self.last_page)
        self.last_page_button.pack(side=tk.LEFT, padx=5)

        # Items per page dropdown
        items_per_page_options = [5, 10, 15, 'All']
        self.items_per_page_var = tk.StringVar(value='5')
        self.items_per_page_dropdown = ttk.Combobox(pagination_frame, textvariable=self.items_per_page_var, values=items_per_page_options, width=5)
        self.items_per_page_dropdown.pack(side=tk.LEFT, padx=5)

        ttk.Label(pagination_frame, text="items per page").pack(side=tk.LEFT, padx=5)

        # Bind double-click to select person
        self.tree.bind("<Double-1>", self.on_select_person)

        # Pagination variables
        self.current_page = 1
        self.items_per_page = 5
        self.total_pages = 1
        self.search_results = []

    def clear_placeholder(self, event):
        if self.last_name_entry.get() == "e.g. Smith":
            self.last_name_entry.delete(0, tk.END)

    def search_person(self):
        last_name = self.last_name_var.get().strip()
        if not last_name or last_name == "e.g. Smith":
            messagebox.showwarning("Input Error", "Please enter a last name to search.")
            return
        try:
            cur = self.conn.cursor()
            query = """
                SELECT person_id, last_name, first_name, middle_name, '' AS alias
                FROM person
                WHERE last_name ILIKE %s;
            """
            cur.execute(query, (f"%{last_name}%",))
            self.search_results = cur.fetchall()
            cur.close()

            self.current_page = 1
            self.items_per_page = int(self.items_per_page_var.get()) if self.items_per_page_var.get() != 'All' else 'All'
            self.update_pagination()
            self.display_results()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to search person: {e}")

    def display_results(self):
        # Clear previous results
        for item in self.tree.get_children():
            self.tree.delete(item)
        # Get current page items
        start_index = (self.current_page - 1) * self.items_per_page if self.items_per_page != 'All' else 0
        end_index = start_index + self.items_per_page if self.items_per_page != 'All' else len(self.search_results)
        current_items = self.search_results[start_index:end_index]
        # Insert new results
        for row in current_items:
            person_id = row[0]
            last_name = row[1]
            first_name = row[2]
            middle_name = row[3]
            alias = row[4]
            self.tree.insert("", "end", iid=person_id, values=(last_name, first_name, middle_name, alias))

    def update_pagination(self):
        if self.items_per_page == 'All':
            self.total_pages = 1
        else:
            total_items = len(self.search_results)
            self.total_pages = math.ceil(total_items / self.items_per_page)
        self.page_number_var.set(self.current_page)

    def first_page(self):
        if self.current_page != 1:
            self.current_page = 1
            self.display_results()
            self.page_number_var.set(self.current_page)

    def previous_page(self):
        if self.current_page > 1:
            self.current_page -= 1
            self.display_results()
            self.page_number_var.set(self.current_page)

    def next_page(self):
        if self.current_page < self.total_pages:
            self.current_page += 1
            self.display_results()
            self.page_number_var.set(self.current_page)

    def last_page(self):
        if self.current_page != self.total_pages:
            self.current_page = self.total_pages
            self.display_results()
            self.page_number_var.set(self.current_page)

    def no_match_found(self):
        self.destroy()
        PersonalProfileForm(self.master, mode='add')

    def on_select_person(self, event):
        selected_item = self.tree.selection()
        if selected_item:
            person_id = selected_item[0]
            # Add person to case_person
            try:
                cur = self.conn.cursor()
                # Check if person is already associated with the case
                check_query = """
                    SELECT COUNT(*) FROM case_person WHERE person_id = %s AND case_id = %s;
                """
                cur.execute(check_query, (person_id, self.case_id))
                count = cur.fetchone()[0]
                if count > 0:
                    messagebox.showinfo("Info", "Person is already associated with this case.")
                    cur.close()
                    return
                # Insert into case_person
                insert_query = """
                    INSERT INTO case_person (person_id, case_id, cac_id)
                    VALUES (%s, %s, %s)
                """
                cur.execute(insert_query, (person_id, self.case_id, self.cac_id))
                self.conn.commit()
                cur.close()
                messagebox.showinfo("Success", "Person added to the case.")
                self.destroy()
                self.master.load_people()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to add person to case: {e}")

# -------------------- PersonalProfileForm Class ----------
import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
from datetime import datetime
import math

class PersonalProfileForm(tk.Toplevel):
    def __init__(self, master, person_id=None, mode='add'):
        super().__init__(master)
        self.title("PERSONAL PROFILE")
        self.conn = master.conn
        self.cac_id = master.cac_id
        self.case_id = master.current_case_id
        self.master = master
        self.person_id = person_id
        self.mode = mode  # 'add', 'edit', 'bio'

        # Scrollable Frame Setup
        self.canvas = tk.Canvas(self)
        self.scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = ttk.Frame(self.canvas)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(
                scrollregion=self.canvas.bbox("all")
            )
        )

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

        # Store Radiobutton references for disabling
        self.radio_buttons_bio_sex = []
        self.radio_buttons_ethnicity = []

        # Define Mappings for Race, Religion, Language, Role, Relationship, Ethnicity, Education Level, Marital Status, Income Level
        self.race_mapping = {
            'Asian': 0,
            'American Indian': 1,
            'Biracial': 2,
            'Biracial - African-American/White': 3,
            'Biracial - Hispanic/White': 4,
            'Black/African-American': 5,
            'White': 6,
            'Hispanic': 7,
            'Native Hawaiian/Other Pacific Islander': 8,
            'Alaska Native': 9,
            'Multiple Races': 10,
            'Not Reported': 11,
            'Not Tracked': 12,
            'Other': 13
        }

        self.religion_mapping = {
            'Christianity': 0,
            'Islam': 1,
            'Judaism': 2,
            'Hinduism': 3,
            'Buddhism': 4,
            'Sikhism': 5,
            'Jainism': 6,
            'Atheist/Agnostic': 7,
            'Other': 8
        }

        self.language_mapping = {
            'English': 0,
            'Spanish': 1,
            'French': 2,
            'German': 3,
            'Portuguese': 4,
            'Russian': 5,
            'Arabic': 6,
            'Turkish': 7,
            'Hindi': 8,
            'Urdu': 9,
            'Chinese': 10,
            'Japanese': 11,
            'Vietnamese': 12,
            'Korean': 13,
            'Other': 14
        }

        self.role_mapping = {
            'Alleged Victim/Client': 0,
            'Alleged Co-Victim': 1,
            'Alleged Offender': 2,
            'Caregiver': 3,
            'Other': 4
        }

        self.relationship_mapping = {
            'Self': 0,
            'Mother': 1,
            'Biological Mother': 2,
            'Adoptive Mother': 3,
            'Step-Mother': 4,
            'Father\'s Girlfriend': 5,
            'Father': 6,
            'Biological Father': 7,
            'Adoptive Father': 8,
            'Step-Father': 9,
            'Mother\'s Boyfriend': 10,
            'Brother': 11,
            'Sister': 12,
            'Step-Brother': 13,
            'Step-Sister': 14,
            'Adoptive Brother': 15,
            'Adoptive Sister': 16,
            'Grandmother': 17,
            'Grandfather': 18,
            'Friend': 19,
            'Other Known Person': 20
        }

        self.ethnicity_mapping = {
            'Non-Hispanic': 1,
            'Hispanic': 2
        }

        self.education_level_mapping = {
            'None': 0,
            'Preschool': 1,
            'Elementary School': 2,
            'Middle School': 3,
            'High School': 4,
            'High School Graduate - GED': 5,
            'Some College': 6,
            'Associate\'s Degree': 7,
            'Bachelor\'s Degree': 8,
            'Master\'s Degree': 9,
            'PhD': 10,
            'Unknown': 11
        }

        self.marital_status_mapping = {
            'Single': 0,
            'Married': 1,
            'Divorced': 2,
            'Widowed': 3,
            'Unknown': 4
        }

        self.income_level_mapping = {
            'less than $15,000': 0,
            'between $15,000 and $25,000': 1,
            'between $25,000 and $50,000': 2,
            'between $50,000 and $75,000': 3,
            'greater than $75,000': 4
        }

        # Initialize in-memory storage for Runaway Incidents
        self.runaway_incidents = []

        self.create_widgets()

        if self.mode in ['edit', 'bio']:
            self.load_person_data()
            if self.mode == 'bio':
                self.disable_fields()

    def create_widgets(self):
        self.fields = {}

        # Header
        header_label = ttk.Label(self.scrollable_frame, text="PERSONAL PROFILE", font=("Helvetica", 16, "bold"))
        header_label.grid(row=0, column=0, columnspan=4, pady=(10, 20), sticky='w')

        # Section 1: Basic Information
        basic_info_frame = ttk.LabelFrame(self.scrollable_frame, text="Basic Information")
        basic_info_frame.grid(row=1, column=0, columnspan=4, padx=10, pady=10, sticky='ew')

        # Define Basic Information Fields
        basic_fields = [
            ('First Name', 'First Name:', True),
            ('Middle Name', 'Middle Name:', False),
            ('Last Name', 'Last Name:', True),
            ('Suffix', 'Suffix:', False),
            ('Nick Name', 'Nick Name:', False),  # Not in database
            ('SSN', 'SSN:', False),              # Not in database
            ('Date of Birth', 'Date of Birth:', False),
            ('Unknown Date of Birth', 'Unknown Date of Birth:', False),
            ('Date of Death', 'Date of Death:', False),  # Not in database
            ('Biological Sex', 'Biological Sex:', True),
            ('Self Identified Gender', 'Self Identified Gender:', True),
            ('Ethnicity', 'Ethnicity:', False),
            ('Bio Custom Field 7', 'Bio Custom Field 7:', False),
            ('Bio Custom Field 8', 'Bio Custom Field 8:', False),
            ('Bio Custom Field 9', 'Bio Custom Field 9:', False)
        ]

        row_idx = 0
        for field_key, field_label, required in basic_fields:
            # Required field labels in red
            label = ttk.Label(basic_info_frame, text=field_label, foreground="red" if required else "black")
            label.grid(row=row_idx, column=0, sticky='e', padx=5, pady=5)

            if field_key == 'Biological Sex':
                self.fields[field_key] = tk.StringVar()
                options = ['Male', 'Female', 'Intersex', 'Unknown', 'Decline to Answer']
                for col, option in enumerate(options):
                    rb = ttk.Radiobutton(
                        basic_info_frame,
                        text=option,
                        variable=self.fields[field_key],
                        value=option
                    )
                    rb.grid(row=row_idx, column=1 + col, sticky='w', padx=5, pady=2)
                    self.radio_buttons_bio_sex.append(rb)
                row_idx += 1
            elif field_key == 'Self Identified Gender':
                self.fields[field_key] = {}
                options = [
                    'Female', 'Male', 'Transgender Female', 'Other', 'Transgender Male',
                    'Non-Binary', 'Not Reported', 'Another Gender Identity', 'Not Tracked',
                    'Unknown', 'Decline to Answer', 'Gender Queer'
                ]
                # Arrange checkboxes in two columns with six options each
                num_columns = 2
                for opt_idx, option in enumerate(options):
                    var = tk.BooleanVar()
                    cb = ttk.Checkbutton(
                        basic_info_frame,
                        text=option,
                        variable=var
                    )
                    row_offset = row_idx + (opt_idx // num_columns)
                    col_offset = 1 + (opt_idx % num_columns)
                    cb.grid(row=row_offset, column=col_offset, sticky='w', padx=5, pady=2)
                    self.fields[field_key][option] = var
                row_idx = row_offset + 1
            elif field_key in ['Date of Birth', 'Date of Death']:
                self.fields[field_key] = DateEntry(
                    basic_info_frame,
                    width=12,
                    background='darkblue',
                    foreground='white',
                    borderwidth=2,
                    date_pattern='yyyy-mm-dd'
                )
                self.fields[field_key].grid(row=row_idx, column=1, sticky='w', padx=5, pady=5)
                row_idx += 1
            elif field_key == 'Unknown Date of Birth':
                # It's a checkbox
                self.fields[field_key] = tk.BooleanVar()
                cb = ttk.Checkbutton(
                    basic_info_frame,
                    variable=self.fields[field_key]
                )
                cb.grid(row=row_idx, column=1, sticky='w', padx=5, pady=5)
                row_idx += 1
            elif field_key == 'Ethnicity':
                # Options: Non-Hispanic, Hispanic
                self.fields[field_key] = tk.StringVar()
                options = ['Non-Hispanic', 'Hispanic']
                for col, option in enumerate(options):
                    rb = ttk.Radiobutton(
                        basic_info_frame,
                        text=option,
                        variable=self.fields[field_key],
                        value=option
                    )
                    rb.grid(row=row_idx, column=1 + col, sticky='w', padx=5, pady=2)
                    self.radio_buttons_ethnicity.append(rb)
                row_idx += 1
            else:
                self.fields[field_key] = ttk.Entry(basic_info_frame)
                self.fields[field_key].grid(row=row_idx, column=1, sticky='w', padx=5, pady=5)
                row_idx += 1

        # Section 2: Demographics
        demographics_frame = ttk.LabelFrame(self.scrollable_frame, text="Demographics")
        demographics_frame.grid(row=2, column=0, columnspan=4, padx=10, pady=10, sticky='ew')

        demographics_fields = [
            ('Race', 'Race:', True),
            ('Religion', 'Religion:', False),
            ('Language', 'Language:', False)
        ]

        for idx, (field_key, field_label, required) in enumerate(demographics_fields):
            label = ttk.Label(demographics_frame, text=field_label, foreground="red" if required else "black")
            label.grid(row=idx, column=0, sticky='e', padx=5, pady=5)

            if field_key == 'Race':
                # Predefined options with mapping to integer IDs
                self.fields[field_key] = tk.StringVar()
                options = ["Asian", "American Indian", "Biracial", "Biracial - African-American/White", "Biracial - Hispanic/White",
                           "Black/African-American", "White", "Hispanic", "Native Hawaiian/Other Pacific Islander", "Alaska Native",
                           "Multiple Races", "Not Reported", "Not Tracked", "Other"]
                self.fields[field_key].set('Select Race')  # Default value
                race_combobox = ttk.Combobox(
                    demographics_frame,
                    textvariable=self.fields[field_key],
                    state="readonly"
                )
                race_combobox['values'] = options
                race_combobox.grid(row=idx, column=1, sticky='w', padx=5, pady=5)
            elif field_key == 'Religion':
                # Predefined options with mapping to integer IDs
                self.fields[field_key] = tk.StringVar()
                options = religions = ["Christianity", "Islam", "Judaism", "Hinduism", "Buddhism", "Sikhism", "Jainism", 
                                       "Atheist/Agnostic", "Other"]
                self.fields[field_key].set('Select Religion')  # Default value
                religion_combobox = ttk.Combobox(
                    demographics_frame,
                    textvariable=self.fields[field_key],
                    state="readonly"
                )
                religion_combobox['values'] = options
                religion_combobox.grid(row=idx, column=1, sticky='w', padx=5, pady=5)
            elif field_key == 'Language':
                # Predefined options with mapping to integer IDs
                self.fields[field_key] = tk.StringVar()
                options = ["English", "Spanish", "French", "German", "Portuguese", "Russian", "Arabic", "Turkish", "Hindi", "Urdu", 
                           "Chinese", "Japanese", "Vietnamese", "Korean", "Other"]
                self.fields[field_key].set('Select Language')  # Default value
                language_combobox = ttk.Combobox(
                    demographics_frame,
                    textvariable=self.fields[field_key],
                    state="readonly"
                )
                language_combobox['values'] = options
                language_combobox.grid(row=idx, column=1, sticky='w', padx=5, pady=5)
            else:
                self.fields[field_key] = ttk.Combobox(
                    demographics_frame,
                    state="readonly"
                )
                # Placeholder options; replace with actual data as needed
                self.fields[field_key]['values'] = ['Option 1', 'Option 2', 'Option 3']
                self.fields[field_key].grid(row=idx, column=1, sticky='w', padx=5, pady=5)

        # Section 3: Classifications and Populations
        classifications_frame = ttk.LabelFrame(self.scrollable_frame, text="Classifications and Populations")
        classifications_frame.grid(row=3, column=0, columnspan=4, padx=10, pady=10, sticky='ew')

        # VOCA Classification Checkboxes
        voca_classifications = [
            'Autism', 'Adult with Substantial Impairment', 'Behavioral Issues',
            "Asperberger's Autism Spectrum", 'Blind', 'Deaf', 'Homeless',
            'LGBTQ Community', 'MMR', 'Physically Handicapped', 'Veteran'
        ]
        ttk.Label(classifications_frame, text="VOCA Classification:").grid(row=0, column=0, sticky='nw', padx=5, pady=5)
        self.fields['VOCA Classification'] = {}
        for idx, option in enumerate(voca_classifications):
            var = tk.BooleanVar()
            cb = ttk.Checkbutton(
                classifications_frame,
                text=option,
                variable=var
            )
            cb.grid(row=idx+1, column=0, sticky='w', padx=20, pady=2)
            self.fields['VOCA Classification'][option] = var

        # Special Populations Checkboxes
        special_populations = [
            'Deaf/Hard of Hearing', 'Unstably Housed/Unhoused', 'Immigrants/Refugee or Asylum Seeking',
            'LGBTQIA+', 'Military-Dependent', 'Cognitive, Physical, or Mental Disability',
            'Limited English Proficiency', 'Vision Impaired', 'Indigenous/Tribal community', 'Other'
        ]
        ttk.Label(classifications_frame, text="Special Populations:").grid(row=0, column=1, sticky='nw', padx=5, pady=5)
        self.fields['Special Populations'] = {}
        for idx, option in enumerate(special_populations):
            var = tk.BooleanVar()
            cb = ttk.Checkbutton(
                classifications_frame,
                text=option,
                variable=var
            )
            cb.grid(row=idx+1, column=1, sticky='w', padx=20, pady=2)
            self.fields['Special Populations'][option] = var

        # Risk Factors Checkboxes
        risk_factors = [
            'Gifts/Bribes from non-caregivers', 'High Risk Sexual Behavior',
            'Other', 'Risky Online Behavior', 'Runaway', 'Street Language', 'Substance Abuse'
        ]
        ttk.Label(classifications_frame, text="Risk Factors:").grid(row=0, column=2, sticky='nw', padx=5, pady=5)
        self.fields['Risk Factors'] = {}
        for idx, option in enumerate(risk_factors):
            var = tk.BooleanVar()
            cb = ttk.Checkbutton(
                classifications_frame,
                text=option,
                variable=var
            )
            cb.grid(row=idx+1, column=2, sticky='w', padx=20, pady=2)
            self.fields['Risk Factors'][option] = var

        # Section 4: Legal and Behavioral Issues
        legal_behavior_frame = ttk.LabelFrame(self.scrollable_frame, text="Legal and Behavioral Issues")
        legal_behavior_frame.grid(row=4, column=0, columnspan=4, padx=10, pady=10, sticky='ew')

        # CSEC Checkboxes
        csec_options = ['Child Pornography', 'Other', 'Sex Tourism', 'Sex Trafficking']
        ttk.Label(legal_behavior_frame, text="CSEC:").grid(row=0, column=0, sticky='nw', padx=5, pady=5)
        self.fields['CSEC'] = {}
        for idx, option in enumerate(csec_options):
            var = tk.BooleanVar()
            cb = ttk.Checkbutton(
                legal_behavior_frame,
                text=option,
                variable=var
            )
            # Arrange in a single row
            cb.grid(row=0, column=1 + idx, sticky='w', padx=5, pady=2)
            self.fields['CSEC'][option] = var

        # Child Pornography Involvement Checkboxes
        cpp_involvement = ['Distribution', 'Manufacturing', 'Other', 'Possession', 'Trading']
        ttk.Label(legal_behavior_frame, text="Child Pornography Involvement:").grid(row=1, column=0, sticky='nw', padx=5, pady=5)
        self.fields['Child Pornography Involvement'] = {}
        for idx, option in enumerate(cpp_involvement):
            var = tk.BooleanVar()
            cb = ttk.Checkbutton(
                legal_behavior_frame,
                text=option,
                variable=var
            )
            # Arrange in a single row
            cb.grid(row=1, column=1 + idx, sticky='w', padx=5, pady=2)
            self.fields['Child Pornography Involvement'][option] = var

        # CSEC Involvement Checkboxes
        csec_involvement = ['USA', 'Canada', 'El Salvador', 'Mexico', 'Nicaragua', 'Uzbekistan', 'Foster Care', 'Awol History']
        ttk.Label(legal_behavior_frame, text="CSEC Involvement:").grid(row=2, column=0, sticky='nw', padx=5, pady=5)
        self.fields['CSEC Involvement'] = {}
        for idx, option in enumerate(csec_involvement):
            var = tk.BooleanVar()
            cb = ttk.Checkbutton(
                legal_behavior_frame,
                text=option,
                variable=var
            )
            # Arrange in two rows for better alignment (4 per row)
            row = 2 + (idx // 4)
            col = 1 + (idx % 4)
            cb.grid(row=row, column=col, sticky='w', padx=5, pady=2)
            self.fields['CSEC Involvement'][option] = var

        # Section 5: Additional Details
        additional_details_frame = ttk.LabelFrame(self.scrollable_frame, text="Additional Details")
        additional_details_frame.grid(row=5, column=0, columnspan=4, padx=10, pady=10, sticky='ew')

        additional_fields = [
            ('Special Needs Special Text', 'Special Needs Special Text:', False),
            ('Comments', 'Comments:', False),
            ('Prior Convictions', 'Prior Convictions:', False),
            ('Convicted Of Crime Against Children', 'Convicted Of Crime Against Children:', False),
            ('Sexual Offender', 'Sexual Offender:', False),
            ('Sexual Predator', 'Sexual Predator:', False),
            ('Do they like cookies?', 'Do they like cookies?:', False),
            ('Developmental Age', 'Developmental Age:', False),
            ('Date Added', 'Date Added:', False),
            ('Custom Field (4)', 'Custom Field (4):', False),
            ('Custom Field (5)', 'Custom Field (5):', False)
        ]

        for idx, (field_key, field_label, required) in enumerate(additional_fields):
            label = ttk.Label(additional_details_frame, text=field_label, foreground="red" if required else "black")
            label.grid(row=idx, column=0, sticky='e', padx=5, pady=5)

            if field_key in ['Prior Convictions', 'Convicted Of Crime Against Children',
                            'Sexual Offender', 'Sexual Predator', 'Do they like cookies?']:
                self.fields[field_key] = tk.BooleanVar()
                cb = ttk.Checkbutton(
                    additional_details_frame,
                    variable=self.fields[field_key]
                )
                cb.grid(row=idx, column=1, sticky='w', padx=5, pady=5)
            elif field_key == 'Date Added':
                self.fields[field_key] = DateEntry(
                    additional_details_frame,
                    width=12,
                    background='darkblue',
                    foreground='white',
                    borderwidth=2,
                    date_pattern='yyyy-mm-dd'
                )
                self.fields[field_key].grid(row=idx, column=1, sticky='w', padx=5, pady=5)
            elif field_key == 'Comments':
                self.fields[field_key] = tk.Text(additional_details_frame, width=40, height=5)
                self.fields[field_key].grid(row=idx, column=1, sticky='w', padx=5, pady=5)
            else:
                self.fields[field_key] = ttk.Entry(additional_details_frame)
                self.fields[field_key].grid(row=idx, column=1, sticky='w', padx=5, pady=5)

        # Section 6: Runaway Incidents
        runaway_frame = ttk.LabelFrame(self.scrollable_frame, text="Runaway Incidents")
        runaway_frame.grid(row=6, column=0, columnspan=4, padx=10, pady=10, sticky='ew')

        # Treeview for Runaway Incidents
        columns = ('Start Date', 'Length of Time', 'Location', 'Actions')
        self.runaway_incidents_tree = ttk.Treeview(
            runaway_frame,
            columns=columns,
            show='headings',
            height=5
        )
        for col in columns:
            self.runaway_incidents_tree.heading(col, text=col)
            if col == 'Actions':
                self.runaway_incidents_tree.column(col, width=200, anchor='center')
            else:
                self.runaway_incidents_tree.column(col, width=150)
        self.runaway_incidents_tree.pack(side='top', fill='x')

        # Buttons
        add_record_button = ttk.Button(runaway_frame, text="+ Add new record", command=self.add_runaway_incident)
        add_record_button.pack(side='top', padx=5, pady=5, anchor='w')

        # Load existing runaway incidents (from in-memory list)
        self.load_runaway_incidents()

        # Section 7: Case Specific Information
        case_specific_frame = ttk.LabelFrame(self.scrollable_frame, text="Case Specific Information")
        case_specific_frame.grid(row=7, column=0, columnspan=4, padx=10, pady=10, sticky='ew')

        case_specific_fields = [
            ('Relationship to Alleged Victim/Client', 'Relationship to Alleged Victim/Client:', True),
            ('Role', 'Role:', True),
            ('Victim Status', 'Victim Status:', False),
            ('Age at Time of Referral', 'Age at Time of Referral:', False),
            ('In Same Household as Alleged Victim/Client', 'In Same Household as Alleged Victim/Client:', False),
            ('Has Custody of Alleged Victim/Client', 'Has Custody of Alleged Victim/Client:', False),
            ('Address Line 1', 'Address Line 1:', False),
            ('Address Line 2', 'Address Line 2:', False),
            ('City', 'City:', False),
            ('State', 'State:', False),
            ('Zip', 'Zip:', False),
            ('County', 'County:', False),
            ('Region', 'Region:', False),
            ('Resides Out of Country', 'Resides Out of Country:', False),
            ('Home Phone', 'Home Phone:', False),
            ('Work Phone', 'Work Phone:', False),
            ('Cell Phone', 'Cell Phone:', False),
            ('Email Address', 'Email Address:', False),
            ('School Or Employer', 'School Or Employer:', False),
            ('Education Level', 'Education Level:', False),
            ('Marital Status', 'Marital Status:', False),
            ('Income Level of Household', 'Income Level of Household:', False),
            ('Does this youth have Youth Problematic Sexual Behaviors?', 'Does this youth have Youth Problematic Sexual Behaviors?', False),
            ('Military Connection', 'Military Connection:', False),
            ('Military Type', 'Military Type:', False),
            ('If National Guard or Reserves, are you currently active/on Title 10 status?', 'If National Guard or Reserves, are you currently active/on Title 10 status?', False),
            ('Military Dependent Relationship', 'Military Dependent Relationship:', False),
            ('Military Connection Name', 'Military Connection Name:', False),
            ('Custom Field (1)', 'Custom Field (1):', False),
            ('CSF Eligible (2)', 'CSF Eligible (2):', False),
            ('Does family need transportation assistance? (3)', 'Does family need transportation assistance? (3):', False),
            ('Community (5)', 'Community (5):', False),
            ('Case Person Custom Field 6', 'Case Person Custom Field 6:', False),
            ('Case Person Custom Field 7', 'Case Person Custom Field 7:', False),
            ('Case Person Custom Field 8', 'Case Person Custom Field 8:', False),
            ('Case Person Custom Field 9', 'Case Person Custom Field 9:', False)
        ]

        row_idx = 0
        for field_key, field_label, required in case_specific_fields:
            label = ttk.Label(case_specific_frame, text=field_label, foreground="red" if required else "black")
            label.grid(row=row_idx, column=0, sticky='e', padx=5, pady=5)

            if field_key == 'Relationship to Alleged Victim/Client':
                # Predefined options with mapping to integer IDs
                self.fields[field_key] = tk.StringVar()
                options = list(self.relationship_mapping.keys())
                self.fields[field_key].set('Select Relationship')  # Default value
                self.relationship_combobox = ttk.Combobox(
                    case_specific_frame,
                    textvariable=self.fields[field_key],
                    state="readonly"
                )
                self.relationship_combobox['values'] = options
                self.relationship_combobox.grid(row=row_idx, column=1, sticky='w', padx=5, pady=5)
                row_idx += 1
            elif field_key == 'Role':
                # Predefined options with mapping to integer IDs
                self.fields[field_key] = tk.StringVar()
                options = list(self.role_mapping.keys())
                self.fields[field_key].set('Select Role')  # Default value
                self.role_combobox = ttk.Combobox(
                    case_specific_frame,
                    textvariable=self.fields[field_key],
                    state="readonly"
                )
                self.role_combobox['values'] = options
                self.role_combobox.grid(row=row_idx, column=1, sticky='w', padx=5, pady=5)
                row_idx += 1
            elif field_key == 'Victim Status':
                self.fields[field_key] = ttk.Combobox(case_specific_frame, state="readonly")
                self.fields[field_key]['values'] = ['Status 1', 'Status 2', 'Status 3']  # Replace with actual statuses
                self.fields[field_key].grid(row=row_idx, column=1, sticky='w', padx=5, pady=5)
                row_idx += 1
            elif field_key == 'Age at Time of Referral':
                frame_age = ttk.Frame(case_specific_frame)
                frame_age.grid(row=row_idx, column=1, sticky='w', padx=5, pady=5)
                self.fields['Age at Time of Referral'] = ttk.Entry(frame_age, width=5)
                self.fields['Age at Time of Referral'].pack(side='left')
                self.fields['Age Unit'] = ttk.Combobox(frame_age, state="readonly", width=10)
                age_units = [('Years', 'YR'), ('Months', 'MO'), ('Days', 'DA')]
                self.age_unit_mapping = {unit[0]: unit[1] for unit in age_units}
                age_unit_names = [unit[0] for unit in age_units]
                self.fields['Age Unit']['values'] = age_unit_names
                self.fields['Age Unit'].pack(side='left', padx=(5, 0))
                self.fields['Age Unit'].set('Years')
                row_idx += 1
            elif field_key in ['In Same Household as Alleged Victim/Client', 'Has Custody of Alleged Victim/Client',
                               'Resides Out of Country', 'Does this youth have Youth Problematic Sexual Behaviors?',
                               'CSF Eligible (2)', 'Does family need transportation assistance? (3)']:
                self.fields[field_key] = tk.BooleanVar()
                cb = ttk.Checkbutton(
                    case_specific_frame,
                    variable=self.fields[field_key]
                )
                cb.grid(row=row_idx, column=1, sticky='w', padx=5, pady=5)
                row_idx += 1
            elif field_key == 'State':
                states = [
                    ('Alabama', 'AL'),
                    ('Alaska', 'AK'),
                    ('Arizona', 'AZ'),
                    ('Arkansas', 'AR'),
                    ('California', 'CA'),
                    ('Colorado', 'CO'),
                    ('Connecticut', 'CT'),
                    ('Delaware', 'DE'),
                    ('District of Columbia', 'DC'),
                    ('Florida', 'FL'),
                    ('Georgia', 'GA'),
                    ('Hawaii', 'HI'),
                    ('Idaho', 'ID'),
                    ('Illinois', 'IL'),
                    ('Indiana', 'IN'),
                    ('Iowa', 'IA'),
                    ('Kansas', 'KS'),
                    ('Kentucky', 'KY'),
                    ('Louisiana', 'LA'),
                    ('Maine', 'ME'),
                    ('Maryland', 'MD'),
                    ('Massachusetts', 'MA'),
                    ('Michigan', 'MI'),
                    ('Minnesota', 'MN'),
                    ('Mississippi', 'MS'),
                    ('Missouri', 'MO'),
                    ('Montana', 'MT'),
                    ('Nebraska', 'NE'),
                    ('Nevada', 'NV'),
                    ('New Hampshire', 'NH'),
                    ('New Jersey', 'NJ'),
                    ('New Mexico', 'NM'),
                    ('New York', 'NY'),
                    ('North Carolina', 'NC'),
                    ('North Dakota', 'ND'),
                    ('Ohio', 'OH'),
                    ('Oklahoma', 'OK'),
                    ('Oregon', 'OR'),
                    ('Pennsylvania', 'PA'),
                    ('Rhode Island', 'RI'),
                    ('South Carolina', 'SC'),
                    ('South Dakota', 'SD'),
                    ('Tennessee', 'TN'),
                    ('Texas', 'TX'),
                    ('Utah', 'UT'),
                    ('Vermont', 'VT'),
                    ('Virginia', 'VA'),
                    ('Washington', 'WA'),
                    ('West Virginia', 'WV'),
                    ('Wisconsin', 'WI'),
                    ('Wyoming', 'WY'),
                ]
                self.state_abbr_mapping = {state[0]: state[1] for state in states}
                state_names = [state[0] for state in states]
                self.fields[field_key] = ttk.Combobox(case_specific_frame, state="readonly")
                self.fields[field_key]['values'] = state_names
                self.fields[field_key].grid(row=row_idx, column=1, sticky='w', padx=5, pady=5)
                row_idx += 1
            elif field_key == 'Education Level':
                self.fields[field_key] = tk.StringVar()
                options = list(self.education_level_mapping.keys())
                self.fields[field_key].set('Select Education Level')
                education_combobox = ttk.Combobox(
                    case_specific_frame,
                    textvariable=self.fields[field_key],
                    state="readonly"
                )
                education_combobox['values'] = options
                education_combobox.grid(row=row_idx, column=1, sticky='w', padx=5, pady=5)
                row_idx += 1
            elif field_key == 'Marital Status':
                self.fields[field_key] = tk.StringVar()
                options = list(self.marital_status_mapping.keys())
                self.fields[field_key].set('Select Marital Status')
                marital_combobox = ttk.Combobox(
                    case_specific_frame,
                    textvariable=self.fields[field_key],
                    state="readonly"
                )
                marital_combobox['values'] = options
                marital_combobox.grid(row=row_idx, column=1, sticky='w', padx=5, pady=5)
                row_idx += 1
            elif field_key == 'Income Level of Household':
                self.fields[field_key] = tk.StringVar()
                options = list(self.income_level_mapping.keys())
                self.fields[field_key].set('Select Income Level')
                income_combobox = ttk.Combobox(
                    case_specific_frame,
                    textvariable=self.fields[field_key],
                    state="readonly"
                )
                income_combobox['values'] = options
                income_combobox.grid(row=row_idx, column=1, sticky='w', padx=5, pady=5)
                row_idx += 1
            elif field_key == 'Community (5)':
                self.fields[field_key] = tk.StringVar()
                options = ['West Hills', 'Cedar Bluff Apartments', 'Hardin Valley', 'Glenview']
                self.fields[field_key].set('Select Community')
                community_combobox = ttk.Combobox(
                    case_specific_frame,
                    textvariable=self.fields[field_key],
                    state="readonly"
                )
                community_combobox['values'] = options
                community_combobox.grid(row=row_idx, column=1, sticky='w', padx=5, pady=5)
                row_idx += 1
            else:
                self.fields[field_key] = ttk.Entry(case_specific_frame)
                self.fields[field_key].grid(row=row_idx, column=1, sticky='w', padx=5, pady=5)
                row_idx += 1

        # Control Buttons
        button_frame = ttk.Frame(self.scrollable_frame)
        button_frame.grid(row=8, column=0, columnspan=4, pady=20)

        if self.mode in ['add', 'edit']:
            save_button = ttk.Button(
                button_frame,
                text="SAVE",
                command=self.save_person
            )
            save_button.pack(side='left', padx=10)

        cancel_button = ttk.Button(
            button_frame,
            text="CANCEL",
            command=self.destroy
        )
        cancel_button.pack(side='left', padx=10)

    # -------------------- Runaway Incidents Methods --------------------
    def load_runaway_incidents(self):
        # Clear existing items
        for item in self.runaway_incidents_tree.get_children():
            self.runaway_incidents_tree.delete(item)
        # Load incidents from in-memory list
        for idx, incident in enumerate(self.runaway_incidents):
            self.runaway_incidents_tree.insert("", "end", iid=str(idx), values=(
                incident['Start Date'],
                incident['Length of Time'],
                incident['Location'],
                ''
            ))
        # Add action buttons to each row
        self.runaway_incidents_tree.update_idletasks()
        for idx in range(len(self.runaway_incidents)):
            self.add_actions_to_row(str(idx))

    def add_actions_to_row(self, iid):
        # Create action frame
        action_frame = ttk.Frame(self.runaway_incidents_tree)
        edit_btn = ttk.Button(action_frame, text="Edit", command=lambda: self.edit_runaway_incident(iid))
        delete_btn = ttk.Button(action_frame, text="Delete", command=lambda: self.delete_runaway_incident(iid))
        edit_btn.pack(side='left', padx=2)
        delete_btn.pack(side='left', padx=2)
        self.runaway_incidents_tree.item(iid, tags=('has_actions',))
        self.runaway_incidents_tree.tag_configure('has_actions', background='white')
        self.place_widget_in_treeview_cell(action_frame, iid, 'Actions')

    def add_runaway_incident(self):
        # Insert an empty row with input fields
        idx = len(self.runaway_incidents)
        iid = f'new_{idx}'
        self.runaway_incidents_tree.insert("", "end", iid=iid, values=('', '', '', ''))

        # Replace cells with input widgets
        self.edit_runaway_incident(iid, new=True)

    def edit_runaway_incident(self, iid, new=False):
        # Get current values
        if new:
            start_date = '11/21/2024'
            length_of_time = '0.00'
            location = ''
        else:
            values = self.runaway_incidents_tree.item(iid, 'values')
            start_date = values[0]
            length_of_time = values[1]
            location = values[2]

        # Create input widgets
        date_entry = DateEntry(self.runaway_incidents_tree, date_pattern='MM/dd/yyyy')
        try:
            date_entry.set_date(datetime.strptime(start_date, '%m/%d/%Y'))
        except ValueError:
            date_entry.set_date(datetime.now())
        length_entry = ttk.Spinbox(self.runaway_incidents_tree, from_=0, to=1000, increment=0.1, format="%.2f")
        length_entry.set(length_of_time)
        location_entry = ttk.Entry(self.runaway_incidents_tree)
        location_entry.insert(0, location)

        # Place input widgets
        self.place_widget_in_treeview_cell(date_entry, iid, 'Start Date')
        self.place_widget_in_treeview_cell(length_entry, iid, 'Length of Time')
        self.place_widget_in_treeview_cell(location_entry, iid, 'Location')

        # Replace Actions cell with Update and Cancel buttons
        action_frame = ttk.Frame(self.runaway_incidents_tree)
        update_btn = ttk.Button(action_frame, text="Update", command=lambda: self.save_runaway_incident(iid, date_entry, length_entry, location_entry, new))
        cancel_btn = ttk.Button(action_frame, text="Cancel", command=lambda: self.cancel_runaway_edit(iid, new))
        update_btn.pack(side='left', padx=2)
        cancel_btn.pack(side='left', padx=2)
        self.place_widget_in_treeview_cell(action_frame, iid, 'Actions')

    def place_widget_in_treeview_cell(self, widget, item, column):
        self.runaway_incidents_tree.update_idletasks()
        bbox = self.runaway_incidents_tree.bbox(item, column=column)
        if not bbox:
            self.runaway_incidents_tree.see(item)
            bbox = self.runaway_incidents_tree.bbox(item, column)
        if not bbox:
            return
        x, y, width, height = bbox
        widget.place(in_=self.runaway_incidents_tree, x=x, y=y, width=width, height=height)

    def save_runaway_incident(self, iid, date_entry, length_entry, location_entry, new):
        start_date = date_entry.get()
        length_of_time = length_entry.get()
        location = location_entry.get().strip()

        if not location:
            messagebox.showwarning("Validation Error", "Location is required.")
            return

        # Save to in-memory list
        incident = {
            'Start Date': start_date,
            'Length of Time': length_of_time,
            'Location': location
        }
        if new:
            self.runaway_incidents.append(incident)
        else:
            if iid.startswith('new_'):
                idx = int(iid.split('_')[1])
            else:
                idx = int(iid)
            self.runaway_incidents[idx] = incident

        # Reload the treeview
        self.load_runaway_incidents()

    def cancel_runaway_edit(self, iid, new):
        if new:
            self.runaway_incidents_tree.delete(iid)
        else:
            self.load_runaway_incidents()

    def delete_runaway_incident(self, iid):
        confirm = messagebox.askyesno("Confirm Deletion", "Are you sure you want to delete the selected runaway incident?")
        if confirm:
            if iid.startswith('new_'):
                idx = int(iid.split('_')[1])
            else:
                idx = int(iid)
            del self.runaway_incidents[idx]
            self.load_runaway_incidents()

    # -------------------- Load Person Data --------------------
    def load_person_data(self):
        try:
            cur = self.conn.cursor()
            # Fetch person data
            person_query = """
                SELECT first_name, middle_name, last_name, suffix, date_of_birth, gender,
                       religion_id, language_id, prior_convictions,
                       convicted_against_children, sex_offender, sex_predator, race_id
                FROM person WHERE person_id = %s
            """
            cur.execute(person_query, (self.person_id,))
            person = cur.fetchone()
            if not person:
                messagebox.showerror("Error", "Person not found.")
                self.destroy()
                return

            # Define the order of fields fetched from person table
            person_field_keys = [
                'First Name', 'Middle Name', 'Last Name', 'Suffix', 'Date of Birth', 'Biological Sex',
                'Religion', 'Language', 'Prior Convictions',
                'Convicted Of Crime Against Children', 'Sexual Offender', 'Sexual Predator', 'Race'
            ]

            for idx, key in enumerate(person_field_keys):
                value = person[idx]
                if key == 'Date of Birth':
                    if value:
                        self.fields[key].set_date(value)
                elif key == 'Biological Sex':
                    # Map single character to full-text option if necessary
                    mapping = {'M': 'Male', 'F': 'Female', 'I': 'Intersex', 'U': 'Unknown', 'D': 'Decline to Answer'}
                    full_text = mapping.get(value, '') 
                    self.fields[key].set(full_text)
                elif key == 'Religion':
                    # Map religion_id to religion name
                    reverse_religion_mapping = {v: k for k, v in self.religion_mapping.items()}
                    religion_name = reverse_religion_mapping.get(value, '') 
                    self.fields[key].set(religion_name)
                elif key == 'Language':
                    # Map language_id to language name
                    reverse_language_mapping = {v: k for k, v in self.language_mapping.items()}
                    language_name = reverse_language_mapping.get(value, '') 
                    self.fields[key].set(language_name)
                elif key in ['Prior Convictions', 'Convicted Of Crime Against Children', 'Sexual Offender', 'Sexual Predator']:
                    self.fields[key].set(bool(value))
                elif key == 'Race':
                    # Map race_id to race name
                    reverse_race_mapping = {v: k for k, v in self.race_mapping.items()}
                    race_name = reverse_race_mapping.get(value, '')
                    self.fields[key].set(race_name)
                else:
                    if isinstance(self.fields[key], ttk.Entry):
                        self.fields[key].delete(0, tk.END)
                        self.fields[key].insert(0, value if value else '')

            # Fetch case_person data
            case_person_query = """
                SELECT relationship_id, role_id, age, age_unit, address_line_1, address_line_2,
                       city, state_abbr, zip, cell_phone_number, home_phone_number,
                       work_phone_number, custody, education_level_id, income_level_id,
                       marital_status_id, same_household, school_or_employer, victim_status_id
            FROM case_person
            WHERE person_id = %s AND case_id = %s
            """
            cur.execute(case_person_query, (self.person_id, self.case_id))
            case_person = cur.fetchone()
            if case_person:
                # Define the order of fields fetched from case_person table
                case_person_field_keys = [
                    'Relationship to Alleged Victim/Client', 'Role', 'Age at Time of Referral', 'Age Unit',
                    'Address Line 1', 'Address Line 2', 'City', 'State', 'Zip',
                    'Cell Phone Number', 'Home Phone Number', 'Work Phone Number',
                    'Custody', 'Education Level ID', 'Income Level ID',
                    'Marital Status ID', 'Same Household', 'School or Employer', 'Victim Status ID'
                ]

                role_id = case_person[1]

                # Handle 'Relationship to Alleged Victim/Client'
                relationship_id = case_person[0]
                reverse_relationship_mapping = {v: k for k, v in self.relationship_mapping.items()}
                relationship_name = reverse_relationship_mapping.get(relationship_id, '') 
                self.fields['Relationship to Alleged Victim/Client'].set(relationship_name if relationship_name else 'Select Relationship')
                if role_id is not None and role_id == 0:
                    self.relationship_combobox.state(['disabled'])

                # Handle 'Role'
                reverse_role_mapping = {v: k for k, v in self.role_mapping.items()}
                role_name = reverse_role_mapping.get(role_id, '') 
                self.fields['Role'].set(role_name if role_name else 'Select Role')
                if role_id is not None and role_id == 0:
                    self.role_combobox.state(['disabled'])

                # Handle 'Age at Time of Referral' and 'Age Unit'
                age = case_person[2]
                age_unit_code = case_person[3]
                if age:
                    self.fields['Age at Time of Referral'].delete(0, tk.END)
                    self.fields['Age at Time of Referral'].insert(0, str(age))
                    # Map age_unit_code back to full name
                    reverse_age_unit_mapping = {v: k for k, v in self.age_unit_mapping.items()}
                    age_unit_name = reverse_age_unit_mapping.get(age_unit_code, 'Years')
                    self.fields['Age Unit'].set(age_unit_name)
                else:
                    self.fields['Age at Time of Referral'].delete(0, tk.END)
                    self.fields['Age Unit'].set('Years')

                # Handle address fields
                address_fields = ['Address Line 1', 'Address Line 2', 'City', 'State', 'Zip']
                for idx_field, key in enumerate(address_fields, start=4):
                    value = case_person[idx_field]
                    if key == 'State':
                        # Map state abbreviation back to state name
                        reverse_state_mapping = {v: k for k, v in self.state_abbr_mapping.items()}
                        state_name = reverse_state_mapping.get(value, '')
                        self.fields[key].set(state_name)
                    else:
                        if isinstance(self.fields[key], ttk.Entry):
                            self.fields[key].delete(0, tk.END)
                            self.fields[key].insert(0, value if value else '')

                # Handle 'In Same Household as Alleged Victim/Client'
                same_household = case_person[16]
                self.fields['In Same Household as Alleged Victim/Client'].set(bool(same_household))

                # Other fields can be handled similarly if needed

            # Handle 'Self Identified Gender' - Since it's not stored in the database, leave it blank
            for gender, var in self.fields['Self Identified Gender'].items():
                var.set(False)

            # Close cursor
            cur.close()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load person data: {e}")
            self.destroy()

    # -------------------- Disable Fields in Bio Mode --------------------
    def disable_fields(self):
        for key, field in self.fields.items():
            try:
                if key == 'Biological Sex':
                    # Disable all Radiobuttons
                    for rb in self.radio_buttons_bio_sex:
                        rb.configure(state='disabled')
                elif key == 'Self Identified Gender':
                    # Disable all Checkbuttons
                    for var in field.values():
                        var.set(False)
                elif isinstance(field, ttk.Entry):
                    field.configure(state='disabled')
                elif isinstance(field, DateEntry):
                    field.configure(state='disabled')
                elif isinstance(field, tk.BooleanVar):
                    # Disable associated Checkbutton if possible
                    pass  # Requires storing references
                elif isinstance(field, dict):
                    # For checkboxes in dictionaries
                    for sub_key, var in field.items():
                        # Disable the Checkbutton associated with var
                        pass  # Requires storing references
            except Exception as e:
                print(f"Error disabling field '{key}': {e}")

    # -------------------- Save Person Data --------------------
    def save_person(self):
        try:
            # Collect data from fields
            data = {}
            for key, field in self.fields.items():
                if key == 'Self Identified Gender':
                    # Collect selected genders
                    selected_genders = [gender for gender, var in field.items() if var.get()]
                    data[key] = ', '.join(selected_genders)
                elif key in ['CSEC Involvement', 'Child Pornography Involvement', 'VOCA Classification', 'Special Populations', 'Risk Factors', 'CSEC']:
                    # Collect selected options
                    selected_options = [option for option, var in field.items() if var.get()]
                    data[key] = ', '.join(selected_options)
                elif isinstance(field, tk.BooleanVar):
                    data[key] = field.get()
                elif isinstance(field, tk.StringVar):
                    data[key] = field.get()
                elif isinstance(field, ttk.Entry):
                    data[key] = field.get().strip()
                elif isinstance(field, DateEntry):
                    data[key] = field.get_date()
                elif isinstance(field, tk.Text):
                    data[key] = field.get("1.0", tk.END).strip()
                else:
                    data[key] = None  # Handle other field types if necessary

            # Ensure required fields are filled
            required_fields = ['First Name', 'Last Name', 'Biological Sex', 'Race', 'Relationship to Alleged Victim/Client', 'Role']
            for field in required_fields:
                if not data.get(field):
                    messagebox.showwarning("Validation Error", f"{field} is required.")
                    return

            # Ensure Age Unit is selected if 'Age at Time of Referral' is filled
            age_at_referral = data.get('Age at Time of Referral')
            age_unit_name = data.get('Age Unit')
            if age_at_referral:
                if not age_unit_name:
                    messagebox.showwarning("Validation Error", "Age Unit is required when Age at Time of Referral is provided.")
                    return
                age_unit_code = self.age_unit_mapping.get(age_unit_name, None)
                if age_unit_code is None:
                    messagebox.showwarning("Validation Error", "Invalid Age Unit selected.")
                    return
            else:
                data['Age Unit'] = ''
                age_unit_code = None

            # Map State to state_abbr
            state_name = data.get('State')
            state_abbr = self.state_abbr_mapping.get(state_name, None)
            if state_abbr is None and state_name != '':
                messagebox.showwarning("Validation Error", "Invalid State selected.")
                return

            cur = self.conn.cursor()

            if self.mode == 'add':
                # Generate a unique person_id
                cur.execute("SELECT MAX(person_id) FROM person;")
                max_id = cur.fetchone()[0]
                person_id = max_id + 1 if max_id else 1

                # Map Biological Sex to single character
                bio_sex_mapping = {
                    'Male': 'M',
                    'Female': 'F',
                    'Intersex': 'I',
                    'Unknown': 'U',
                    'Decline to Answer': 'D'
                }
                bio_sex_value = bio_sex_mapping.get(data.get('Biological Sex'), None)

                # Map Race to race_id
                race_id = None
                race_name = data.get('Race')
                if race_name in self.race_mapping:
                    race_id = self.race_mapping[race_name]
                else:
                    messagebox.showwarning("Validation Error", "Invalid Race selected.")
                    return

                # Map Religion to religion_id
                religion_id = None
                religion_name = data.get('Religion')
                if religion_name in self.religion_mapping:
                    religion_id = self.religion_mapping[religion_name]
                else: religion_id = None

                # Map Language to language_id
                language_id = None
                language_name = data.get('Language')
                if language_name in self.language_mapping:
                    language_id = self.language_mapping[language_name]
                else: language_id = None

                # Map Role to role_id
                role_id = None
                role_name = data.get('Role')
                if role_name in self.role_mapping:
                    role_id = self.role_mapping[role_name]
                elif role_name == 'Select Role':
                    role_id = None
                else:
                    messagebox.showwarning("Validation Error", "Invalid Role selected.")
                    return

                # Map Relationship to relationship_id
                relationship_id = None
                relationship_name = data.get('Relationship to Alleged Victim/Client')
                if relationship_name in self.relationship_mapping:
                    relationship_id = self.relationship_mapping[relationship_name]
                elif relationship_name == 'Select Relationship':
                    relationship_id = None
                else:
                    messagebox.showwarning("Validation Error", "Invalid Relationship selected.")
                    return

                # Insert into person table (only database fields)
                insert_person_query = """
                    INSERT INTO person (
                        person_id, cac_id, first_name, middle_name, last_name, suffix,
                        date_of_birth, gender, religion_id, language_id,
                        prior_convictions, convicted_against_children,
                        sex_offender, sex_predator, race_id
                    ) VALUES (
                        %s, %s, %s, %s, %s, %s,
                        %s, %s, %s, %s,
                        %s, %s,
                        %s, %s, %s
                    )
                """
                person_data = (
                    person_id,
                    self.cac_id,
                    data.get('First Name'),
                    data.get('Middle Name'),
                    data.get('Last Name'),
                    data.get('Suffix'),
                    data.get('Date of Birth'),
                    bio_sex_value,
                    religion_id,
                    language_id,
                    data.get('Prior Convictions'),
                    data.get('Convicted Of Crime Against Children'),
                    data.get('Sexual Offender'),
                    data.get('Sexual Predator'),
                    race_id
                )
                cur.execute(insert_person_query, person_data)

                # Insert into case_person table
                insert_case_person_query = """
                    INSERT INTO case_person (
                        person_id, case_id, cac_id, relationship_id, role_id,
                        age, age_unit, address_line_1, address_line_2,
                        city, state_abbr, zip, same_household, school_or_employer, victim_status_id
                    ) VALUES (
                        %s, %s, %s, %s, %s,
                        %s, %s, %s, %s,
                        %s, %s, %s, %s, %s, %s
                    )
                """
                case_person_data = (
                    person_id,
                    self.case_id,
                    self.cac_id,
                    relationship_id,
                    role_id,
                    int(data.get('Age at Time of Referral')) if data.get('Age at Time of Referral') else None,
                    age_unit_code,
                    data.get('Address Line 1'),
                    data.get('Address Line 2'),
                    data.get('City'),
                    state_abbr,
                    data.get('Zip'),
                    data.get('In Same Household as Alleged Victim/Client'),
                    data.get('School or Employer')
                )
                cur.execute(insert_case_person_query, case_person_data)

            elif self.mode == 'edit':
                # Map Biological Sex to single character
                bio_sex_mapping = {
                    'Male': 'M',
                    'Female': 'F',
                    'Intersex': 'I',
                    'Unknown': 'U',
                    'Decline to Answer': 'D'
                }
                bio_sex_value = bio_sex_mapping.get(data.get('Biological Sex'), None)

                # Map Race to race_id
                race_id = None
                race_name = data.get('Race')
                if race_name in self.race_mapping:
                    race_id = self.race_mapping[race_name]
                else:
                    messagebox.showwarning("Validation Error", "Invalid Race selected.")
                    return

                # Map Religion to religion_id
                religion_id = None
                religion_name = data.get('Religion')
                if religion_name in self.religion_mapping:
                    religion_id = self.religion_mapping[religion_name]
                else: religion_id = None
                

                # Map Language to language_id
                language_id = None
                language_name = data.get('Language')
                if language_name in self.language_mapping:
                    language_id = self.language_mapping[language_name]
                else: language_id = None

                # Map Role to role_id
                role_id = None
                role_name = data.get('Role')
                if role_name in self.role_mapping:
                    role_id = self.role_mapping[role_name]
                elif role_name == 'Select Role':
                    role_id = None
                else:
                    messagebox.showwarning("Validation Error", "Invalid Role selected.")
                    return

                # Map Relationship to relationship_id
                relationship_id = None
                relationship_name = data.get('Relationship to Alleged Victim/Client')
                if relationship_name in self.relationship_mapping:
                    relationship_id = self.relationship_mapping[relationship_name]
                elif relationship_name == 'Select Relationship':
                    relationship_id = None
                else:
                    messagebox.showwarning("Validation Error", "Invalid Relationship selected.")
                    return

                # Update person table (only database fields)
                update_person_query = """
                    UPDATE person SET
                        first_name = %s,
                        middle_name = %s,
                        last_name = %s,
                        suffix = %s,
                        date_of_birth = %s,
                        gender = %s,
                        religion_id = %s,
                        language_id = %s,
                        prior_convictions = %s,
                        convicted_against_children = %s,
                        sex_offender = %s,
                        sex_predator = %s,
                        race_id = %s
                    WHERE person_id = %s
                """
                person_data = (
                    data.get('First Name'),
                    data.get('Middle Name'),
                    data.get('Last Name'),
                    data.get('Suffix'),
                    data.get('Date of Birth'),
                    bio_sex_value,
                    religion_id,
                    language_id,
                    data.get('Prior Convictions'),
                    data.get('Convicted Of Crime Against Children'),
                    data.get('Sexual Offender'),
                    data.get('Sexual Predator'),
                    race_id,
                    self.person_id
                )
                cur.execute(update_person_query, person_data)

                # Update case_person table
                update_case_person_query = """
                    UPDATE case_person SET
                        relationship_id = %s,
                        role_id = %s,
                        age = %s,
                        age_unit = %s,
                        address_line_1 = %s,
                        address_line_2 = %s,
                        city = %s,
                        state_abbr = %s,
                        zip = %s,
                        same_household = %s,
                        school_or_employer = %s
                    WHERE person_id = %s AND case_id = %s
                """
                case_person_data = (
                    relationship_id,
                    role_id,
                    int(data.get('Age at Time of Referral')) if data.get('Age at Time of Referral') else None,
                    age_unit_code,
                    data.get('Address Line 1'),
                    data.get('Address Line 2'),
                    data.get('City'),
                    state_abbr,
                    data.get('Zip'),
                    data.get('In Same Household as Alleged Victim/Client'),
                    data.get('School or Employer'),
                    self.person_id,
                    self.case_id
                )
                cur.execute(update_case_person_query, case_person_data)

            else:
                # Unsupported mode
                messagebox.showerror("Error", "Unsupported mode for saving.")
                cur.close()
                return

            self.conn.commit()
            cur.close()
            messagebox.showinfo("Success", "Person information saved successfully.")
            self.destroy()
            self.master.load_people()
        except Exception as e:
            self.conn.rollback()
            messagebox.showerror("Error", f"Failed to save person information: {e}")


# -------------------- Alias for Compatibility with app.py --------------------
people_interface = PeopleInterface
