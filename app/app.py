import tkinter as tk
from tkinter import ttk
import Generaltab_interface
import MH_basic_interface
import people_interface

class tkinterApp(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        
        container = tk.Frame(self)
        container.pack(side = "top", fill = "both", expand=True)
        
        container.grid_rowconfigure(0, weight = 1)
        container.grid_columnconfigure(0, weight = 1)
        
        self.frames = {}
        
        for F in (Generaltab_interface.GeneraltabInterface, MH_basic_interface.MHBasicInterface, people_interface.people_interface):
            frame = F(parent=container, controller=self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        
        # For Testing
        #print(self.frame)
        
        self.show_frame(people_interface.people_interface)
            
    
    def show_frame(self, frame_class):
        frame = self.frames[frame_class] 
        frame.tkraise()

if __name__ == "__main__":
    app = tkinterApp()
    app.geometry("1600x800")
    app.mainloop()