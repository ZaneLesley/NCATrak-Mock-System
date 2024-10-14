import tkinter as tk
from tkinter import ttk

class People_Interface:

    # Initialize the main window
    def __init__(self, root, controller):
        self.controller = controller
        root.title("People Associated with Case")
        root.geometry("1200x600")
        self.create_interface(root, controller)

    def create_interface(self, root, controller):

        # ----------------Save and Cancel Buttons---------------
        buttons_frame = tk.Frame(root)
        buttons_frame.pack(fill='x', padx=10, pady=5)

        save_button = ttk.Button(buttons_frame, text="Save")
        save_button.pack(side='left', padx=5)

        cancel_button = ttk.Button(buttons_frame, text="Cancel")
        cancel_button.pack(side='left', padx=5)

        # -------------------- Header --------------------

        header_label = ttk.Label(root, text="PEOPLE ASSOCIATED WITH CASE", font=('Helvetica', 16))
        header_label.pack(fill='x', padx=10, pady=10)

        # -------------------- Add Button --------------------

        add_button_frame = tk.Frame(root)
        add_button_frame.pack(fill='x', padx=10)

        add_button = ttk.Button(add_button_frame, text="+ Add")
        add_button.pack(side='left', padx=5)

        # -------------------- Main Table --------------------

        table_frame = tk.Frame(root)
        table_frame.pack(fill='both', expand=True, padx=10, pady=10)

        # Define columns
        columns = ("Action", "Name", "Age", "Date of Birth", "Role", "Relationship To Victim", "Same Household", "Custody")
        tree = ttk.Treeview(table_frame, columns=columns, show='headings')

        # Define headings
        for col in columns:
            tree.heading(col, text=col)

        # Define column widths (increased 'Action' column width)
        tree.column("Action", width=200, anchor='center')
        tree.column("Name", width=150)
        tree.column("Age", width=50, anchor='center')
        tree.column("Date of Birth", width=100, anchor='center')
        tree.column("Role", width=120)
        tree.column("Relationship To Victim", width=150)
        tree.column("Same Household", width=120, anchor='center')
        tree.column("Custody", width=100, anchor='center')

        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side='right', fill='y')
        tree.pack(fill='both', expand=True)

        # Function to handle "Edit" button press
        def on_edit_press(item):
            pass  # Functionality to be implemented later

        # Function to handle "Bio" button press
        def on_bio_press(item):
            pass  # Functionality to be implemented later

        # Create a custom style for the buttons
        style = ttk.Style()
        style.configure('Action.TButton', padding=(0, 0), font=('TkDefaultFont', 10))

        # Example of adding an entry
        #item = tree.insert("", "end", values=('', 'Jane Doe', '28', '1993-07-21', 'Witness', 'Friend', '', ''))


        # Dictionary to hold action buttons and checkboxes for each item
        action_widgets = {}

        def update_action_buttons():
            # For each visible item in the treeview, create buttons and checkboxes if they don't exist and place them
            for item in tree.get_children():
                # Get the bounding boxes of the relevant columns
                bbox_action = tree.bbox(item, column='Action')
                bbox_same_household = tree.bbox(item, column='Same Household')
                bbox_custody = tree.bbox(item, column='Custody')

                if not bbox_action or not bbox_same_household or not bbox_custody:
                    continue

                # Adjust x and y to be relative to root window
                x_action, y_action, width_action, height_action = bbox_action
                x_action += tree.winfo_rootx() - root.winfo_rootx()
                y_action += tree.winfo_rooty() - root.winfo_rooty()

                x_sh, y_sh, width_sh, height_sh = bbox_same_household
                x_sh += tree.winfo_rootx() - root.winfo_rootx()
                y_sh += tree.winfo_rooty() - root.winfo_rooty()

                x_custody, y_custody, width_custody, height_custody = bbox_custody
                x_custody += tree.winfo_rootx() - root.winfo_rootx()
                y_custody += tree.winfo_rooty() - root.winfo_rooty()

                if item not in action_widgets:
                    # Create the buttons
                    edit_button = ttk.Button(root, text='Edit', command=lambda i=item: on_edit_press(i), style='Action.TButton')
                    bio_button = ttk.Button(root, text='Bio', command=lambda i=item: on_bio_press(i), style='Action.TButton')

                    # Create the checkboxes
                    sh_var = tk.BooleanVar()
                    custody_var = tk.BooleanVar()

                    sh_checkbox = ttk.Checkbutton(root, variable=sh_var)
                    custody_checkbox = ttk.Checkbutton(root, variable=custody_var)

                    action_widgets[item] = {
                        'edit_button': edit_button,
                        'bio_button': bio_button,
                        'sh_checkbox': sh_checkbox,
                        'custody_checkbox': custody_checkbox,
                        'sh_var': sh_var,
                        'custody_var': custody_var
                    }
                else:
                    widgets = action_widgets[item]
                    edit_button = widgets['edit_button']
                    bio_button = widgets['bio_button']
                    sh_checkbox = widgets['sh_checkbox']
                    custody_checkbox = widgets['custody_checkbox']

                # Place the buttons
                total_button_width = 160  # Total width of both buttons and spacing
                button_height = height_action
                button_y = y_action
                start_x = x_action + (width_action - total_button_width) // 2

                edit_button.place(x=start_x, y=button_y, width=75, height=button_height)
                bio_button.place(x=start_x + 85, y=button_y, width=75, height=button_height)

                # Place the checkboxes
                checkbox_size = min(height_sh, 20)  # Set a max size for the checkbox
                checkbox_y_sh = y_sh + (height_sh - checkbox_size) // 2
                checkbox_y_custody = y_custody + (height_custody - checkbox_size) // 2

                sh_checkbox.place(x=x_sh + (width_sh - checkbox_size) // 2, y=checkbox_y_sh, width=checkbox_size, height=checkbox_size)
                custody_checkbox.place(x=x_custody + (width_custody - checkbox_size) // 2, y=checkbox_y_custody, width=checkbox_size, height=checkbox_size)

            # Remove widgets for items that no longer exist
            items_to_remove = []
            for item in action_widgets:
                if item not in tree.get_children():
                    widgets = action_widgets[item]
                    widgets['edit_button'].destroy()
                    widgets['bio_button'].destroy()
                    widgets['sh_checkbox'].destroy()
                    widgets['custody_checkbox'].destroy()
                    items_to_remove.append(item)
            for item in items_to_remove:
                del action_widgets[item]

            # Schedule the next update
            root.after(100, update_action_buttons)

        # Start the update loop
        update_action_buttons()

        # -------------------- Pagination Controls --------------------

        pagination_frame = tk.Frame(root)
        pagination_frame.pack(fill='x', padx=10, pady=5)

        first_button = ttk.Button(pagination_frame, text="\u23EE")  # Black left-pointing double triangle with vertical bar
        first_button.pack(side='left', padx=2)

        prev_button = ttk.Button(pagination_frame, text="\u25C0")   # Black left-pointing triangle
        prev_button.pack(side='left', padx=2)

        page_number = ttk.Entry(pagination_frame, width=5, justify='center')
        page_number.insert(0, "1")
        page_number.pack(side='left', padx=2)

        next_button = ttk.Button(pagination_frame, text="\u25B6")   # Black right-pointing triangle
        next_button.pack(side='left', padx=2)

        last_button = ttk.Button(pagination_frame, text="\u23ED")   # Black right-pointing double triangle with vertical bar
        last_button.pack(side='left', padx=2)

        items_per_page_var = tk.StringVar(value="20")
        items_per_page_dropdown = ttk.Combobox(pagination_frame, textvariable=items_per_page_var, values=["1", "5", "10", "15", "20"], width=5)
        items_per_page_dropdown.pack(side='left', padx=5)

        items_per_page_label = ttk.Label(pagination_frame, text="Items per page")
        items_per_page_label.pack(side='left', padx=5)

        # -------------------- Additional Checkbox and Comments --------------------

        additional_frame = tk.Frame(root)
        additional_frame.pack(fill='x', padx=10, pady=10)

        checkbox_var = tk.BooleanVar()
        checkbox = ttk.Checkbutton(additional_frame, text="Alleged Offender Name Unknown", variable=checkbox_var)
        checkbox.grid(row=0, column=0, pady=5, sticky='n')

        comments_label = ttk.Label(additional_frame, text="Alleged Offender Unknown Comments:")
        comments_label.grid(row=1, column=0, pady=(10, 0), sticky='n')

        comments_text = tk.Text(additional_frame, height=5, width=100)
        comments_text.grid(row=2, column=0, pady=5, sticky='n')

        # ------------------- Link to MH_basic_interface ----------------------------
        link_frame = tk.Frame(root)
        link_frame.pack(fill = 'x', padx=10, pady=10)

        link_button = ttk.Button(link_frame, text="Go to MH_Basic_Interface", command=lambda: controller.show_frame("MH_Basic_Interface"))   # Black right-pointing double triangle with vertical bar
        link_button.pack(side='left', padx=2)
