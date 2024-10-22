import tkinter as tk
from tkinter import ttk
import Generaltab_interface
import people_interface
import MH_basic_interface
import MH_assessment
import MH_treatmentPlan_interface
import va_tab_interface

class tkinterApp(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        
        container = tk.Frame(self)
        container.pack(side = "top", fill = "both", expand=True)
        
        container.grid_rowconfigure(0, weight = 1)
        container.grid_columnconfigure(0, weight = 1)
        
        self.frames = {}

        frames_list = [
            Generaltab_interface.GeneraltabInterface, 
            people_interface.people_interface,
            MH_basic_interface.MHBasicInterface,
            MH_assessment.MHassessment,
            MH_treatmentPlan_interface.MH_treatment_plan_interface,
            va_tab_interface.va_interface
        ]
        
        for F in frames_list:
            frame = F(parent=container, controller=self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        
        # For Testing
        #print(self.frame)
        
        self.show_frame(MH_assessment.MHassessment)
            
    
    def show_frame(self, frame_class):
        frame = self.frames[frame_class] 
        frame.tkraise()

if __name__ == "__main__":
    app = tkinterApp()
    app.geometry("1600x800")
    app.mainloop()