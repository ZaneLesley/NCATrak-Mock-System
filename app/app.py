import os.path
import tkinter as tk
from tkinter import ttk
import database_lookup_search
import Generaltab_interface
import people_interface
import MH_basic_interface
import MH_assessment
import MH_treatmentPlan_interface
import va_tab_interface
import case_notes
from database.config import load_config
from database.connect import connect


class tkinterApp(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)


        
        container = tk.Frame(self)
        container.pack(side = "top", fill = "both", expand=True)
        
        container.grid_rowconfigure(0, weight = 1)
        container.grid_columnconfigure(0, weight = 1)
        
        self.frames = {}

        frames_list = [
            database_lookup_search.lookup_interface,
            Generaltab_interface.GeneraltabInterface, 
            people_interface.people_interface,
            MH_basic_interface.MHBasicInterface,
            MH_assessment.MHassessment,
            MH_treatmentPlan_interface.MH_treatment_plan_interface,
            va_tab_interface.va_interface,
            case_notes.case_notes_interface
        ]
        
        for F in frames_list:
            frame = F(parent=container, controller=self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")
            print(f"Completed loading for frame {frame}")

        self.show_frame(database_lookup_search.lookup_interface)
            
    def show_frame(self, frame_class):
        frame = self.frames[frame_class] 
        frame.tkraise()

    def refresh(self):
        self.destroy()
        self.__init__()
        self.geometry("1600x800")
        self.mainloop()

if __name__ == "__main__":
    cwd = os.path.abspath(os.path.dirname(__file__))
    case_id_txt = os.path.join(cwd, 'case_id.txt')

    config = load_config(filename="database.ini")
    conn = connect(config)
    try:
        with conn.cursor() as cur:
            if os.path.exists(case_id_txt):
                with open(case_id_txt, 'r') as f:
                    case_id = f.read().strip()

                # check if the case_id exists in the database
                cur.execute("SELECT COUNT(*) FROM cac_case WHERE case_id = %s", (case_id,))
                row = cur.fetchone()

                # isn't valid write a random one in.
                if row[0] == 0:
                    cur.execute("SELECT case_id FROM cac_case ORDER BY RANDOM() LIMIT 1")
                    random_case = cur.fetchone()[0]
                    with open(case_id_txt, 'w') as f:
                        f.write(str(random_case))
            else:
                # Get a random cac_cac
                cur.execute("SELECT case_id FROM cac_case ORDER BY RANDOM() LIMIT 1")
                random_case = cur.fetchone()[0]

                # Write the new case_id to the file
                with open(case_id_txt, 'w') as f:
                    f.write(str(random_case))
    except Exception as e:
        print(f"An error has occurred regarding the database and a case_id not being present in the database. Details: {e}\n")
        print("Please ensure there is least one case_id in the database (run the wizard with data generation of > 15")
    finally:
        conn.close()

    app = tkinterApp()
    app.geometry("1600x800")
    app.mainloop()