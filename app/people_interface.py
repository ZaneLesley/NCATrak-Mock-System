import tkinter as tk
from tkinter import ttk, messagebox
import psycopg2
from configparser import ConfigParser
import os
from datetime import datetime
from tkinter import ttk
import Generaltab_interface
import MH_basic_interface
import MH_assessment
import MH_treatmentPlan_interface
import va_tab_interface
import case_notes


# -------------------- Internal Mappings --------------------
# Define roles and relationships here
ROLE_MAPPING = {
    'Alleged Offender': 1,
    'Witness': 2,
    'Victim': 3,
    'Friend': 4,
    'Family Member': 5,
    # Add more roles as needed
}

RELATIONSHIP_MAPPING = {
    'Boyfriend': 1,
    'Girlfriend': 2,
    'Friend': 3,
    'Sibling': 4,
    'Parent': 5,
    'Colleague': 6,
    # Add more relationships as needed
}

# Reverse mappings for display purposes
ROLE_REVERSE_MAPPING = {v: k for k, v in ROLE_MAPPING.items()}
RELATIONSHIP_REVERSE_MAPPING = {v: k for k, v in RELATIONSHIP_MAPPING.items()}

class PeopleInterface(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)

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

        #  window in the canvas
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")

        # scrollbar to canvas
        canvas.configure(yscrollcommand=scrollbar.set)

        # row counter for grid management
        row_counter = 2

        # Use grid over pack for interface linking
        canvas.grid(row=row_counter, column=0, sticky="nsew")
        scrollbar.grid(row=row_counter, column=1, sticky="ns")
        row_counter += 1

        button1 = ttk.Button(self, text="General", 
                            command=lambda: controller.show_frame(Generaltab_interface.GeneraltabInterface))
        button1.grid(row=0, column=0, padx=5, pady=5)

        button2 = ttk.Button(self, text="People", 
                            command=lambda: controller.show_frame(people_interface))
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
        
        button7 = ttk.Button(self, text="Case Notes", 
                            command=lambda: controller.show_frame(case_notes.case_notes_interface))
        button7.grid(row=0, column=6, padx=5, pady=5)


        # -------------------- Save and Cancel Buttons --------------------
        buttons_frame = tk.Frame(self)
        buttons_frame.grid(row=0, column=0, padx=10, pady=5, sticky='w')

        save_button = ttk.Button(buttons_frame, text="Save", command=self.save_changes)
        save_button.pack(side='left', padx=5)

        cancel_button = ttk.Button(buttons_frame, text="Cancel", command=self.cancel_changes)
        cancel_button.pack(side='left', padx=5)

        # -------------------- Header --------------------
        header_label = ttk.Label(self, text="PEOPLE ASSOCIATED WITH CASE", font=('Helvetica', 16))
        header_label.grid(row=1, column=0, padx=10, pady=10, sticky='w')

        # -------------------- Search Fields --------------------
        search_frame = tk.Frame(self)
        search_frame.grid(row=2, column=0, padx=10, pady=5, sticky='w')

        search_label = ttk.Label(search_frame, text="Search:")
        search_label.pack(side='left', padx=(0, 5))

        self.search_entry = ttk.Entry(search_frame)
        self.search_entry.pack(side='left', padx=5)
        self.search_entry.bind('<KeyRelease>', self.on_search)

        # -------------------- Add Button --------------------
        add_button = ttk.Button(self, text="+ Add", command=self.add_person)
        add_button.grid(row=3, column=0, padx=10, pady=5, sticky='w')

        # -------------------- Main Table --------------------
        table_frame = tk.Frame(self)
        table_frame.grid(row=4, column=0, padx=10, pady=10, sticky='nsew')
        self.grid_rowconfigure(4, weight=1)

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
        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        self.tree.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')

        # Create a custom style for the buttons
        style = ttk.Style()
        style.configure('Action.TButton', padding=(0, 0), font=('TkDefaultFont', 10))

        # Dictionary to hold action buttons and checkboxes for each item
        self.action_widgets = {}

        # Load people into the table
        self.load_people()

        # Start the update loop for action buttons and checkboxes
        self.update_action_widgets()

        # -------------------- Additional Checkbox and Comments --------------------
        additional_frame = tk.Frame(self)
        additional_frame.grid(row=5, column=0, padx=10, pady=10, sticky='w')

        checkbox_var = tk.BooleanVar()
        checkbox = ttk.Checkbutton(additional_frame, text="Alleged Offender Name Unknown", variable=checkbox_var)
        checkbox.grid(row=0, column=0, pady=5, sticky='w')

        comments_label = ttk.Label(additional_frame, text="Alleged Offender Unknown Comments:")
        comments_label.grid(row=1, column=0, pady=(10, 0), sticky='w')

        comments_text = tk.Text(additional_frame, height=5, width=100)
        comments_text.grid(row=2, column=0, pady=5, sticky='w')

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
        try:
            cur = self.conn.cursor()
            query = "SELECT case_id FROM cac_case LIMIT 1;"
            cur.execute(query)
            result = cur.fetchone()
            cur.close()
            if result:
                return result[0]
            else:
                messagebox.showerror("Error", "No cases found in the database.")
                return None
        except Exception as e:
            messagebox.showerror("Error", f"Failed to retrieve case ID: {e}")
            return None

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
                cp.role_id, cp.relationship_id, cp.same_household, cp.custody
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
                role_id = row[4] if row[4] else None
                relationship_id = row[5] if row[5] else None
                role = ROLE_REVERSE_MAPPING.get(role_id, 'N/A') if role_id else 'N/A'
                relationship = RELATIONSHIP_REVERSE_MAPPING.get(relationship_id, 'N/A') if relationship_id else 'N/A'
                values = ('', name, age, dob, role, relationship, '', '')
                self.tree.insert("", "end", iid=person_id, values=values)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load people: {e}")

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
        EditPersonForm(self, person_id)

    def on_bio_press(self, item):
        person_id = item
        BioForm(self, person_id)

    def on_delete_press(self, item):
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
                role_id = row[4] if row[4] else None
                relationship_id = row[5] if row[5] else None
                role = ROLE_REVERSE_MAPPING.get(role_id, 'N/A') if role_id else 'N/A'
                relationship = RELATIONSHIP_REVERSE_MAPPING.get(relationship_id, 'N/A') if relationship_id else 'N/A'
                values = ('', name, age, dob, role, relationship, '', '')
                self.tree.insert("", "end", iid=person_id, values=values)

    # -------------------- Add Person Functionality --------------------
    def add_person(self):
        AddPersonForm(self)

    # -------------------- Save and Cancel Changes --------------------
    def save_changes(self):
        # Implement any actions needed when the 'Save' button is clicked
        messagebox.showinfo("Info", "Changes have been saved.")

    def cancel_changes(self):
        # Implement any actions needed when the 'Cancel' button is clicked
        # For example, reload data from the database
        self.load_people()
        messagebox.showinfo("Info", "Changes have been canceled.")

# -------------------- AddPersonForm Class --------------------
class AddPersonForm(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.title("Add Person")
        self.conn = master.conn
        self.case_id = master.current_case_id
        self.cac_id = master.cac_id
        self.master = master
        self.fields = {}

        # Define field names
        field_names = ['First Name', 'Last Name', 'Date of Birth (YYYY-MM-DD)', 'Gender (M/F)', 'Role', 'Relationship To Victim']
        for idx, field in enumerate(field_names):
            label = ttk.Label(self, text=field)
            label.grid(row=idx, column=0, padx=10, pady=5, sticky='e')
            if field in ['Role', 'Relationship To Victim']:
                if field == 'Role':
                    combobox = ttk.Combobox(self, values=list(ROLE_MAPPING.keys()), state='readonly')
                else:
                    combobox = ttk.Combobox(self, values=list(RELATIONSHIP_MAPPING.keys()), state='readonly')
                combobox.grid(row=idx, column=1, padx=10, pady=5, sticky='w')
                self.fields[field] = combobox
            else:
                entry = ttk.Entry(self)
                entry.grid(row=idx, column=1, padx=10, pady=5, sticky='w')
                self.fields[field] = entry

        # Save and Cancel Buttons
        buttons_frame = tk.Frame(self)
        buttons_frame.grid(row=len(field_names), column=0, columnspan=2, padx=10, pady=10, sticky='w')

        save_button = ttk.Button(buttons_frame, text="Save", command=self.save_person)
        save_button.pack(side='left', padx=5)

        cancel_button = ttk.Button(buttons_frame, text="Cancel", command=self.destroy)
        cancel_button.pack(side='left', padx=5)

    def save_person(self):
        try:
            # Validate required fields
            required_fields = ['First Name', 'Last Name', 'Date of Birth (YYYY-MM-DD)', 'Role', 'Relationship To Victim']
            for field in required_fields:
                if not self.fields[field].get().strip():
                    messagebox.showwarning("Validation Error", f"{field} is required.")
                    return

            # Validate date format
            dob = self.fields['Date of Birth (YYYY-MM-DD)'].get()
            try:
                datetime.strptime(dob, '%Y-%m-%d')
            except ValueError:
                messagebox.showwarning("Validation Error", "Date of Birth must be in YYYY-MM-DD format.")
                return

            role_name = self.fields['Role'].get().strip()
            relationship_name = self.fields['Relationship To Victim'].get().strip()

            # Map role and relationship names to IDs
            role_id = ROLE_MAPPING.get(role_name)
            relationship_id = RELATIONSHIP_MAPPING.get(relationship_name)

            if role_id is None:
                messagebox.showwarning("Validation Error", f"Invalid Role: {role_name}")
                return

            if relationship_id is None:
                messagebox.showwarning("Validation Error", f"Invalid Relationship To Victim: {relationship_name}")
                return

            cur = self.conn.cursor()
            # Insert into person table
            insert_person_query = """
                INSERT INTO person (person_id, cac_id, first_name, last_name, date_of_birth, gender)
                VALUES (%s, %s, %s, %s, %s, %s)
            """
            person_id = self.generate_person_id()
            if person_id is None:
                return  # ID generation failed

            person_data = (
                person_id, self.cac_id, self.fields['First Name'].get(), self.fields['Last Name'].get(),
                dob, self.fields['Gender (M/F)'].get().upper()
            )
            cur.execute(insert_person_query, person_data)

            # Insert into case_person table
            insert_case_person_query = """
                INSERT INTO case_person (person_id, case_id, cac_id, role_id, relationship_id)
                VALUES (%s, %s, %s, %s, %s)
            """
            case_person_data = (
                person_id, self.case_id, self.cac_id, role_id, relationship_id
            )
            cur.execute(insert_case_person_query, case_person_data)
            self.conn.commit()
            cur.close()
            messagebox.showinfo("Success", "Person added successfully.")
            self.destroy()
            self.master.load_people()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to add person: {e}")

    def generate_person_id(self):
        # Generate a unique person_id
        try:
            cur = self.conn.cursor()
            cur.execute("SELECT MAX(person_id) FROM person;")
            max_id = cur.fetchone()[0]
            cur.close()
            if max_id:
                return max_id + 1
            else:
                return 1
        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate person ID: {e}")
            return None

# -------------------- EditPersonForm Class --------------------
class EditPersonForm(AddPersonForm):
    def __init__(self, master, person_id):
        super().__init__(master)
        self.title("Edit Person")
        self.person_id = person_id
        self.load_person_data()

    def load_person_data(self):
        try:
            cur = self.conn.cursor()
            # Fetch person data
            person_query = "SELECT first_name, last_name, date_of_birth, gender FROM person WHERE person_id = %s"
            cur.execute(person_query, (self.person_id,))
            person = cur.fetchone()
            if not person:
                messagebox.showerror("Error", "Person not found.")
                self.destroy()
                return

            # Fetch case_person data
            case_person_query = """
                SELECT role_id, relationship_id FROM case_person 
                WHERE person_id = %s AND case_id = %s
            """
            cur.execute(case_person_query, (self.person_id, self.case_id))
            case_person = cur.fetchone()
            if not case_person:
                messagebox.showerror("Error", "Case-Person association not found.")
                cur.close()
                self.destroy()
                return
            cur.close()

            # Populate fields
            self.fields['First Name'].insert(0, person[0] if person[0] else '')
            self.fields['Last Name'].insert(0, person[1] if person[1] else '')
            self.fields['Date of Birth (YYYY-MM-DD)'].insert(0, person[2].strftime('%Y-%m-%d') if person[2] else '')
            self.fields['Gender (M/F)'].insert(0, person[3] if person[3] else '')

            # Map role_id and relationship_id back to names
            role_id = case_person[0]
            relationship_id = case_person[1]

            role_name = ROLE_REVERSE_MAPPING.get(role_id, 'N/A') if role_id else ''
            relationship_name = RELATIONSHIP_REVERSE_MAPPING.get(relationship_id, 'N/A') if relationship_id else ''

            self.fields['Role'].set(role_name)
            self.fields['Relationship To Victim'].set(relationship_name)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load person data: {e}")
            self.destroy()

    def save_person(self):
        try:
            # Validate required fields
            required_fields = ['First Name', 'Last Name', 'Date of Birth (YYYY-MM-DD)', 'Role', 'Relationship To Victim']
            for field in required_fields:
                if not self.fields[field].get().strip():
                    messagebox.showwarning("Validation Error", f"{field} is required.")
                    return

            # Validate date format
            dob = self.fields['Date of Birth (YYYY-MM-DD)'].get()
            try:
                datetime.strptime(dob, '%Y-%m-%d')
            except ValueError:
                messagebox.showwarning("Validation Error", "Date of Birth must be in YYYY-MM-DD format.")
                return

            role_name = self.fields['Role'].get().strip()
            relationship_name = self.fields['Relationship To Victim'].get().strip()

            # Map role and relationship names to IDs
            role_id = ROLE_MAPPING.get(role_name)
            relationship_id = RELATIONSHIP_MAPPING.get(relationship_name)

            if role_id is None:
                messagebox.showwarning("Validation Error", f"Invalid Role: {role_name}")
                return

            if relationship_id is None:
                messagebox.showwarning("Validation Error", f"Invalid Relationship To Victim: {relationship_name}")
                return

            cur = self.conn.cursor()
            # Update person table
            update_person_query = """
                UPDATE person SET first_name = %s, last_name = %s, date_of_birth = %s, gender = %s
                WHERE person_id = %s
            """
            person_data = (
                self.fields['First Name'].get(), self.fields['Last Name'].get(), dob,
                self.fields['Gender (M/F)'].get().upper(), self.person_id
            )
            cur.execute(update_person_query, person_data)

            # Update case_person table
            update_case_person_query = """
                UPDATE case_person SET role_id = %s, relationship_id = %s
                WHERE person_id = %s AND case_id = %s
            """
            case_person_data = (
                role_id, relationship_id, self.person_id, self.case_id
            )
            cur.execute(update_case_person_query, case_person_data)
            self.conn.commit()
            cur.close()
            messagebox.showinfo("Success", "Person updated successfully.")
            self.destroy()
            self.master.load_people()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to update person: {e}")

# -------------------- BioForm Class --------------------
class BioForm(EditPersonForm):
    def __init__(self, master, person_id):
        super().__init__(master, person_id)
        self.title("Bio")
        # Additional fields or customizations for the Bio form can be added here

# -------------------- Main Execution --------------------
if __name__ == '__main__':
    root = tk.Tk()
    root.title("People Interface")
    root.geometry("1000x600")  # Set a reasonable default window size
    app = PeopleInterface(root)
    app.pack(fill='both', expand=True)
    root.mainloop()
