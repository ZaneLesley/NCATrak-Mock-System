import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import psycopg2
from configparser import ConfigParser
import os
from datetime import datetime
from tkcalendar import DateEntry
import math

# Assuming these modules are available. If not, you can comment out or adjust accordingly.
# import Generaltab_interface
# import MH_basic_interface
# import MH_assessment
# import MH_treatmentPlan_interface
# import va_tab_interface
# import case_notes

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

        # window in the canvas
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")

        # scrollbar to canvas
        canvas.configure(yscrollcommand=scrollbar.set)

        # Use grid over pack for interface linking
        canvas.grid(row=0, column=0, sticky="nsew")
        scrollbar.grid(row=0, column=1, sticky="ns")

        # Navigation Buttons (assuming 'controller' is provided)
        # Note: Adjusted to remove 'controller' since it's not defined
        # You can re-add 'controller' parameter if needed
        button_frame = ttk.Frame(scrollable_frame)
        button_frame.grid(row=0, column=0, columnspan=7, padx=5, pady=5, sticky='w')

        button1 = ttk.Button(button_frame, text="General",
                             command=lambda: self.show_frame(None))  # Replace None with actual frame
        button1.pack(side='left', padx=5)

        button2 = ttk.Button(button_frame, text="People",
                             command=lambda: self.show_frame(PeopleInterface))
        button2.pack(side='left', padx=5)

        button3 = ttk.Button(button_frame, text="Mental Health - Basic",
                             command=lambda: self.show_frame(None))  # Replace None with actual frame
        button3.pack(side='left', padx=5)

        button4 = ttk.Button(button_frame, text="Mental Health - Assessment",
                             command=lambda: self.show_frame(None))  # Replace None with actual frame
        button4.pack(side='left', padx=5)

        button5 = ttk.Button(button_frame, text="Mental Health - Treatment Plan",
                             command=lambda: self.show_frame(None))  # Replace None with actual frame
        button5.pack(side='left', padx=5)

        button6 = ttk.Button(button_frame, text="VA",
                             command=lambda: self.show_frame(None))  # Replace None with actual frame
        button6.pack(side='left', padx=5)

        button7 = ttk.Button(button_frame, text="Case Notes",
                             command=lambda: self.show_frame(None))  # Replace None with actual frame
        button7.pack(side='left', padx=5)

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

        # -------------------- Additional Checkbox and Comments --------------------
        additional_frame = tk.Frame(scrollable_frame)
        additional_frame.grid(row=6, column=0, padx=10, pady=10, sticky='w')

        self.checkbox_var = tk.BooleanVar()
        checkbox = ttk.Checkbutton(additional_frame, text="Alleged Offender Name Unknown", variable=self.checkbox_var)
        checkbox.grid(row=0, column=0, pady=5, sticky='w')

        comments_label = ttk.Label(additional_frame, text="Alleged Offender Unknown Comments:")
        comments_label.grid(row=1, column=0, pady=(10, 0), sticky='w')

        self.comments_text = tk.Text(additional_frame, height=5, width=100)
        self.comments_text.grid(row=2, column=0, pady=5, sticky='w')

        # -------------------- Document Upload Section --------------------
        # Document Upload section title
        upload_title_frame = ttk.Frame(scrollable_frame)
        upload_title_frame.grid(row=7, column=0, padx=10, pady=5, sticky='w')
        ttk.Label(upload_title_frame, text="Document Upload", font=('Arial', 16)).pack(side=tk.LEFT)

        # Treeview for document uploads
        upload_frame = ttk.Frame(scrollable_frame)
        upload_frame.grid(row=8, column=0, padx=10, pady=5, sticky='nsew')
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
        file_nav_frame.grid(row=9, column=0, padx=10, pady=10, sticky='w')
        ttk.Button(file_nav_frame, text="Select Files...", command=self.select_files).pack(side=tk.LEFT, padx=10)

    # -------------------- Navigation Function Placeholder --------------------
    def show_frame(self, frame_class):
        # Placeholder for navigation function
        pass

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
                cp.same_household, cp.custody
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
                role = 'N/A'
                relationship = 'N/A'
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
        PersonalProfileForm(self, person_id, mode='edit')

    def on_bio_press(self, item):
        person_id = item
        PersonalProfileForm(self, person_id, mode='bio')

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
                role = 'N/A'
                relationship = 'N/A'
                values = ('', name, age, dob, role, relationship, '', '')
                self.tree.insert("", "end", iid=person_id, values=values)

    # -------------------- Add Person Functionality --------------------
    def add_person(self):
        LookupPersonForm(self)

    # -------------------- Save and Cancel Changes --------------------
    def save_changes(self):
        # Save additional checkbox and comments
        try:
            cur = self.conn.cursor()
            # Update case table with 'alleged_offender_unknown' and 'comments'
            query = """
                UPDATE cac_case
                SET alleged_offender_unknown = %s,
                    alleged_offender_unknown_comments = %s
                WHERE case_id = %s;
            """
            alleged_offender_unknown = self.checkbox_var.get()
            comments = self.comments_text.get("1.0", tk.END).strip()
            cur.execute(query, (alleged_offender_unknown, comments, self.current_case_id))
            self.conn.commit()
            cur.close()
            messagebox.showinfo("Success", "Changes have been saved.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save changes: {e}")

    def cancel_changes(self):
        # Reload data from the database
        self.load_people()
        # Reset additional checkbox and comments
        self.load_additional_info()
        messagebox.showinfo("Info", "Changes have been canceled.")

    def load_additional_info(self):
        try:
            cur = self.conn.cursor()
            query = """
                SELECT alleged_offender_unknown, alleged_offender_unknown_comments
                FROM cac_case
                WHERE case_id = %s;
            """
            cur.execute(query, (self.current_case_id,))
            result = cur.fetchone()
            cur.close()
            if result:
                self.checkbox_var.set(result[0])
                self.comments_text.delete("1.0", tk.END)
                self.comments_text.insert(tk.END, result[1] if result[1] else '')
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load additional information: {e}")

    # -------------------- Document Upload Methods --------------------
    def select_files(self):
        file_paths = filedialog.askopenfilenames()
        if file_paths:
            for file_path in file_paths:
                file_name = os.path.basename(file_path)
                # For demonstration, we will insert dummy data into the treeview
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

# -------------------- PersonalProfileForm Class --------------------
import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry

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

        # Define Mappings for Race, Religion, Language, Role, and Relationship
        self.race_mapping = {
            'White': 1,
            'Black or African American': 2,
            'Asian': 3,
            'American Indian or Alaska Native': 4,
            'Native Hawaiian or Other Pacific Islander': 5,
            'Other': 6
        }

        self.religion_mapping = {
            'Christianity': 1,
            'Islam': 2,
            'Judaism': 3,
            'Hinduism': 4,
            'Buddhism': 5,
            'Other': 6
        }

        self.language_mapping = {
            'English': 1,
            'Spanish': 2,
            'French': 3,
            'Mandarin': 4,
            'Other': 5
        }

        self.role_mapping = {
            'Victim': 1,
            'Perpetrator': 2,
            'Witness': 3,
            'Other': 4
        }

        self.relationship_mapping = {
            'Parent': 1,
            'Sibling': 2,
            'Guardian': 3,
            'Other': 4
        }

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
            ('Self Identified Gender', 'Self Identified Gender:', True)
        ]

        for idx, (field_key, field_label, required) in enumerate(basic_fields):
            # Required field labels in red
            label = ttk.Label(basic_info_frame, text=field_label, foreground="red" if required else "black")
            label.grid(row=idx, column=0, sticky='e', padx=5, pady=5)

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
                    rb.grid(row=idx, column=1 + col, sticky='w', padx=5, pady=2)
                    self.radio_buttons_bio_sex.append(rb)
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
                    row_offset = opt_idx // num_columns
                    col_offset = opt_idx % num_columns
                    cb.grid(row=idx + row_offset, column=1 + col_offset, sticky='w', padx=5, pady=2)
                    self.fields[field_key][option] = var
            elif field_key in ['Date of Birth', 'Date of Death']:
                self.fields[field_key] = DateEntry(
                    basic_info_frame,
                    width=12,
                    background='darkblue',
                    foreground='white',
                    borderwidth=2,
                    date_pattern='yyyy-mm-dd'
                )
                self.fields[field_key].grid(row=idx, column=1, sticky='w', padx=5, pady=5)
            elif field_key == 'Unknown Date of Birth':
                # It's a checkbox
                self.fields[field_key] = tk.BooleanVar()
                cb = ttk.Checkbutton(
                    basic_info_frame,
                    variable=self.fields[field_key]
                )
                cb.grid(row=idx, column=1, sticky='w', padx=5, pady=5)
            else:
                self.fields[field_key] = ttk.Entry(basic_info_frame)
                self.fields[field_key].grid(row=idx, column=1, sticky='w', padx=5, pady=5)

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
                options = [
                    'White', 'Black or African American', 'Asian',
                    'American Indian or Alaska Native', 'Native Hawaiian or Other Pacific Islander', 'Other'
                ]
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
                options = [
                    'Christianity', 'Islam', 'Judaism',
                    'Hinduism', 'Buddhism', 'Other'
                ]
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
                options = [
                    'English', 'Spanish', 'French',
                    'Mandarin', 'Other'
                ]
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
            row = 2
            col = 1 + (idx % 4) + (idx // 4) * 1
            cb.grid(row=2, column=1 + (idx % 4), sticky='w', padx=5, pady=2)
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
            ('Date Added', 'Date Added:', False)
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

        # Section 6: Geographic and Custom Fields
        geo_custom_frame = ttk.LabelFrame(self.scrollable_frame, text="Geographic and Custom Fields")
        geo_custom_frame.grid(row=6, column=0, columnspan=4, padx=10, pady=10, sticky='ew')

        geo_custom_fields = [
            ('CSEC Involvement', 'CSEC Involvement:', False),
            ('Custom Field', 'Custom Field:', False),
            ('Ethnicity', 'Ethnicity:', False),
            ('Bio Custom Field 7', 'Bio Custom Field 7:', False),
            ('Bio Custom Field 8', 'Bio Custom Field 8:', False),
            ('Bio Custom Field 9', 'Bio Custom Field 9:', False),
            ('Runaway Incidents', 'Runaway Incidents:', False),
            # Add other fields as necessary
        ]

        for idx, (field_key, field_label, required) in enumerate(geo_custom_fields):
            label = ttk.Label(geo_custom_frame, text=field_label, foreground="red" if required else "black")
            label.grid(row=idx, column=0, sticky='ne', padx=5, pady=5)

            if field_key == 'CSEC Involvement':
                options = ['USA', 'Canada', 'El Salvador', 'Mexico', 'Nicaragua', 'Uzbekistan', 'Foster Care', 'Awol History']
                self.fields[field_key] = {}
                for opt_idx, option in enumerate(options):
                    var = tk.BooleanVar()
                    cb = ttk.Checkbutton(
                        geo_custom_frame,
                        text=option,
                        variable=var
                    )
                    # Arrange in two rows (4 in first row, 4 in second row)
                    row = idx
                    col = 1 + (opt_idx % 4)
                    cb.grid(row=idx, column=1 + (opt_idx % 4), sticky='w', padx=5, pady=2)
                    self.fields[field_key][option] = var
            elif field_key == 'Ethnicity':
                self.fields[field_key] = tk.StringVar()
                options = ['Non-Hispanic', 'Hispanic']
                for opt_idx, option in enumerate(options):
                    rb = ttk.Radiobutton(
                        geo_custom_frame,
                        text=option,
                        variable=self.fields[field_key],
                        value=option
                    )
                    rb.grid(row=idx, column=1 + opt_idx, sticky='w', padx=2, pady=2)
                    self.radio_buttons_ethnicity.append(rb)
            elif field_key.startswith('Bio Custom Field'):
                self.fields[field_key] = ttk.Entry(geo_custom_frame)
                self.fields[field_key].grid(row=idx, column=1, sticky='w', padx=5, pady=5)
            elif field_key == 'Runaway Incidents':
                # Implement a table for Runaway Incidents
                self.runaway_incidents_tree = ttk.Treeview(
                    geo_custom_frame,
                    columns=('Action', 'Start Date', 'Length of Time', 'Location'),
                    show='headings',
                    height=4
                )
                self.runaway_incidents_tree.heading('Action', text='Action')
                self.runaway_incidents_tree.heading('Start Date', text='Start Date')
                self.runaway_incidents_tree.heading('Length of Time', text='Length of Time')
                self.runaway_incidents_tree.heading('Location', text='Location')
                self.runaway_incidents_tree.column('Action', width=100)
                self.runaway_incidents_tree.column('Start Date', width=100)
                self.runaway_incidents_tree.column('Length of Time', width=120)
                self.runaway_incidents_tree.column('Location', width=150)
                self.runaway_incidents_tree.grid(row=idx, column=1, sticky='w', padx=5, pady=5)

                add_record_button = ttk.Button(geo_custom_frame, text="+ Add new record", command=self.add_runaway_incident)
                add_record_button.grid(row=idx, column=2, sticky='w', padx=5, pady=5)
            else:
                self.fields[field_key] = ttk.Entry(geo_custom_frame)
                self.fields[field_key].grid(row=idx, column=1, sticky='w', padx=5, pady=5)

        # Section 7: Case Specific Information
        case_specific_frame = ttk.LabelFrame(self.scrollable_frame, text="Case Specific Information")
        case_specific_frame.grid(row=7, column=0, columnspan=4, padx=10, pady=10, sticky='ew')

        case_specific_fields = [
            ('Relationship to Alleged Victim/Client', 'Relationship to Alleged Victim/Client:', True),
            ('Role', 'Role:', True),
            ('Victim Status', 'Victim Status:', False),
            ('Age at Time of Referral', 'Age at Time of Referral:', False),  # Exclude from save since column doesn't exist
            ('In Same Household as Alleged Victim/Client', 'In Same Household as Alleged Victim/Client:', False),
            ('Has Custody of Alleged Victim/Client', 'Has Custody of Alleged Victim/Client:', False),
            ('Address Line 1', 'Address Line 1:', False),
            ('Address Line 2', 'Address Line 2:', False),
            ('City', 'City:', False),
            ('State', 'State:', False),
            ('Zip', 'Zip:', False),
            ('County', 'County:', False),
            ('Region', 'Region:', False)
        ]

        for idx, (field_key, field_label, required) in enumerate(case_specific_fields):
            label = ttk.Label(case_specific_frame, text=field_label, foreground="red" if required else "black")
            label.grid(row=idx, column=0, sticky='e', padx=5, pady=5)

            if field_key == 'Relationship to Alleged Victim/Client':
                # Predefined options with mapping to integer IDs
                self.fields[field_key] = tk.StringVar()
                options = list(self.relationship_mapping.keys())
                self.fields[field_key].set('Select Relationship')  # Default value
                relationship_combobox = ttk.Combobox(
                    case_specific_frame,
                    textvariable=self.fields[field_key],
                    state="readonly"
                )
                relationship_combobox['values'] = options
                relationship_combobox.grid(row=idx, column=1, sticky='w', padx=5, pady=5)
            elif field_key == 'Role':
                # Predefined options with mapping to integer IDs
                self.fields[field_key] = tk.StringVar()
                options = list(self.role_mapping.keys())
                self.fields[field_key].set('Select Role')  # Default value
                role_combobox = ttk.Combobox(
                    case_specific_frame,
                    textvariable=self.fields[field_key],
                    state="readonly"
                )
                role_combobox['values'] = options
                role_combobox.grid(row=idx, column=1, sticky='w', padx=5, pady=5)
            elif field_key == 'Victim Status':
                self.fields[field_key] = ttk.Combobox(case_specific_frame, state="readonly")
                self.fields[field_key]['values'] = ['Status 1', 'Status 2', 'Status 3']  # Replace with actual statuses
                self.fields[field_key].grid(row=idx, column=1, sticky='w', padx=5, pady=5)
            elif field_key == 'Age at Time of Referral':
                frame_age = ttk.Frame(case_specific_frame)
                frame_age.grid(row=idx, column=1, sticky='w', padx=5, pady=5)
                self.fields['Age at Time of Referral'] = ttk.Entry(frame_age, width=5)
                self.fields['Age at Time of Referral'].pack(side='left')
                self.fields['Age Unit'] = ttk.Combobox(frame_age, state="readonly", width=10)
                self.fields['Age Unit']['values'] = ['Years', 'Months', 'Days']  # Add other units if needed
                self.fields['Age Unit'].pack(side='left', padx=(5,0))
                # Set default value to 'Years'
                self.fields['Age Unit'].set('Years')
            elif field_key in ['In Same Household as Alleged Victim/Client', 'Has Custody of Alleged Victim/Client']:
                self.fields[field_key] = tk.BooleanVar()
                cb = ttk.Checkbutton(
                    case_specific_frame,
                    variable=self.fields[field_key]
                )
                cb.grid(row=idx, column=1, sticky='w', padx=5, pady=5)
            elif field_key == 'State':
                self.fields[field_key] = ttk.Combobox(case_specific_frame, state="readonly")
                self.fields[field_key]['values'] = ['District of Columbia', 'State 1', 'State 2']  # Replace with actual states
                self.fields[field_key].grid(row=idx, column=1, sticky='w', padx=5, pady=5)
            else:
                self.fields[field_key] = ttk.Entry(case_specific_frame)
                self.fields[field_key].grid(row=idx, column=1, sticky='w', padx=5, pady=5)

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

    def add_runaway_incident(self):
        # Placeholder for adding a new runaway incident record
        # You can implement a separate form or popup to collect incident details
        pass

    def load_person_data(self):
        try:
            cur = self.conn.cursor()
            # Fetch person data
            person_query = """
                SELECT first_name, middle_name, last_name, suffix, date_of_birth, gender,
                       religion_id, language_id, prior_convictions,
                       convicted_against_children, sex_offender, sex_predator
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
                'Convicted Of Crime Against Children', 'Sexual Offender', 'Sexual Predator'
            ]

            for idx, key in enumerate(person_field_keys):
                value = person[idx]
                if key == 'Date of Birth':
                    if value:
                        self.fields[key].set_date(value)
                elif key == 'Biological Sex':
                    # Map single character to full-text option if necessary
                    mapping = {'M': 'Male', 'F': 'Female', 'I': 'Intersex', 'U': 'Unknown', 'D': 'Decline to Answer'}
                    full_text = mapping.get(value, '') if value else ''
                    self.fields[key].set(full_text)
                elif key == 'Religion':
                    # Map religion_id to religion name
                    reverse_religion_mapping = {v: k for k, v in self.religion_mapping.items()}
                    religion_name = reverse_religion_mapping.get(value, '') if value else ''
                    self.fields[key].set(religion_name)
                elif key == 'Language':
                    # Map language_id to language name
                    reverse_language_mapping = {v: k for k, v in self.language_mapping.items()}
                    language_name = reverse_language_mapping.get(value, '') if value else ''
                    self.fields[key].set(language_name)
                elif key in ['Prior Convictions', 'Convicted Of Crime Against Children', 'Sexual Offender', 'Sexual Predator']:
                    self.fields[key].set(bool(value))
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

                # Handle 'Relationship to Alleged Victim/Client'
                relationship_id = case_person[0]
                reverse_relationship_mapping = {v: k for k, v in self.relationship_mapping.items()}
                relationship_name = reverse_relationship_mapping.get(relationship_id, '') if relationship_id else ''
                self.fields['Relationship to Alleged Victim/Client'].set(relationship_name if relationship_name else 'Select Relationship')

                # Handle 'Role'
                role_id = case_person[1]
                reverse_role_mapping = {v: k for k, v in self.role_mapping.items()}
                role_name = reverse_role_mapping.get(role_id, '') if role_id else ''
                self.fields['Role'].set(role_name if role_name else 'Select Role')

                # Handle 'Age at Time of Referral' and 'Age Unit'
                age = case_person[2]
                age_unit = case_person[3]
                if age:
                    self.fields['Age at Time of Referral'].delete(0, tk.END)
                    self.fields['Age at Time of Referral'].insert(0, str(age))
                    self.fields['Age Unit'].set(age_unit if age_unit else 'Years')
                else:
                    self.fields['Age at Time of Referral'].delete(0, tk.END)
                    self.fields['Age Unit'].set('Years')

                # Handle address fields
                address_fields = ['Address Line 1', 'Address Line 2', 'City', 'State', 'Zip']
                for idx, key in enumerate(address_fields, start=4):
                    value = case_person[idx]
                    if key == 'State':
                        self.fields[key].set(value if value else '')
                    else:
                        if isinstance(self.fields[key], ttk.Entry):
                            self.fields[key].delete(0, tk.END)
                            self.fields[key].insert(0, value if value else '')

                # Other fields like phone numbers, custody, etc., can be handled similarly if present

            # Handle 'Self Identified Gender' - Since it's not stored in the database, leave it blank
            for gender, var in self.fields['Self Identified Gender'].items():
                var.set(False)

            # Close cursor
            cur.close()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load person data: {e}")
            self.destroy()

    def disable_fields(self):
        for key, field in self.fields.items():
            try:
                if key == 'Biological Sex':
                    # Disable all Radiobuttons
                    for rb in self.radio_buttons_bio_sex:
                        rb.configure(state='disabled')
                elif key == 'Ethnicity':
                    # Disable all Radiobuttons
                    for rb in self.radio_buttons_ethnicity:
                        rb.configure(state='disabled')
                elif key == 'Self Identified Gender':
                    # Disable all Checkbuttons
                    # Iterate through the children and disable checkbuttons
                    for child in self.scrollable_frame.winfo_children():
                        if isinstance(child, ttk.LabelFrame) and child.cget("text") == "Basic Information":
                            for subchild in child.winfo_children():
                                if isinstance(subchild, ttk.Checkbutton):
                                    subchild.configure(state='disabled')
                elif isinstance(field, ttk.Entry):
                    field.configure(state='disabled')
                elif isinstance(field, DateEntry):
                    field.configure(state='disabled')
                elif isinstance(field, tk.BooleanVar):
                    # Disable associated Checkbutton if possible
                    pass  # Requires storing references
                elif isinstance(field, dict):
                    # For CSEC Involvement, etc.
                    for sub_key, var in field.items():
                        # Disable the Checkbutton associated with var
                        pass  # Requires storing references
            except Exception as e:
                print(f"Error disabling field '{key}': {e}")

    def save_person(self):
        try:
            # Collect data from fields
            data = {}
            for key, field in self.fields.items():
                if key == 'Self Identified Gender':
                    # Collect selected genders
                    selected_genders = [gender for gender, var in field.items() if var.get()]
                    data[key] = ', '.join(selected_genders)
                elif key in ['CSEC Involvement', 'Child Pornography Involvement']:
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
                    # For other types, skip
                    pass

            # Validate required fields
            required_fields = [
                'First Name', 'Last Name', 'Biological Sex',
                'Self Identified Gender', 'Race',
                'Relationship to Alleged Victim/Client', 'Role'
                # 'Age at Time of Referral' is excluded since the column doesn't exist
            ]
            missing_fields = [field for field in required_fields if not data.get(field)]
            if missing_fields:
                messagebox.showwarning("Validation Error", f"The following required fields are missing: {', '.join(missing_fields)}")
                return

            # Additional validation: Ensure Age Unit is selected if 'Age at Time of Referral' is filled
            age_at_referral = self.fields.get('Age at Time of Referral').get().strip()
            age_unit = self.fields.get('Age Unit')
            if age_at_referral:
                if age_unit and not age_unit.get():
                    messagebox.showwarning("Validation Error", "Age Unit is required when Age at Time of Referral is provided.")
                    return
                else:
                    data['Age Unit'] = age_unit.get() if age_unit else ''
            else:
                data['Age Unit'] = ''

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
                elif religion_name == 'Select Religion':
                    religion_id = None
                else:
                    messagebox.showwarning("Validation Error", "Invalid Religion selected.")
                    return

                # Map Language to language_id
                language_id = None
                language_name = data.get('Language')
                if language_name in self.language_mapping:
                    language_id = self.language_mapping[language_name]
                elif language_name == 'Select Language':
                    language_id = None
                else:
                    messagebox.showwarning("Validation Error", "Invalid Language selected.")
                    return

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
                        sex_offender, sex_predator
                    ) VALUES (
                        %s, %s, %s, %s, %s, %s,
                        %s, %s, %s, %s,
                        %s, %s,
                        %s, %s
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
                    data.get('Sexual Predator')
                )
                cur.execute(insert_person_query, person_data)

                # Insert into case_person table
                insert_case_person_query = """
                    INSERT INTO case_person (
                        person_id, case_id, cac_id, relationship_id, role_id,
                        age, age_unit, address_line_1, address_line_2,
                        city, state_abbr, zip, same_household, school_or_employer
                    ) VALUES (
                        %s, %s, %s, %s, %s,
                        %s, %s, %s, %s,
                        %s, %s, %s, %s, %s
                    )
                """
                case_person_data = (
                    person_id,
                    self.case_id,
                    self.cac_id,
                    relationship_id,
                    role_id,
                    int(data.get('Age at Time of Referral')) if data.get('Age at Time of Referral') else None,
                    data.get('Age Unit'),
                    data.get('Address Line 1'),
                    data.get('Address Line 2'),
                    data.get('City'),
                    self.fields['State'].get(),
                    data.get('Zip'),
                    data.get('Same Household as Alleged Victim/Client'),
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
                elif religion_name == 'Select Religion':
                    religion_id = None
                else:
                    messagebox.showwarning("Validation Error", "Invalid Religion selected.")
                    return

                # Map Language to language_id
                language_id = None
                language_name = data.get('Language')
                if language_name in self.language_mapping:
                    language_id = self.language_mapping[language_name]
                elif language_name == 'Select Language':
                    language_id = None
                else:
                    messagebox.showwarning("Validation Error", "Invalid Language selected.")
                    return

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
                        sex_predator = %s
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
                    data.get('Age Unit'),
                    data.get('Address Line 1'),
                    data.get('Address Line 2'),
                    data.get('City'),
                    self.fields['State'].get(),
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



# -------------------- Main Execution --------------------
if __name__ == '__main__':
    root = tk.Tk()
    root.title("People Interface")
    root.geometry("1000x600")  # Set a reasonable default window size
    app = PeopleInterface(root)
    app.pack(fill='both', expand=True)
    root.mainloop()
