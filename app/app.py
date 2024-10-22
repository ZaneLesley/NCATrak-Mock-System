import tkinter as tk
from tkinter import ttk
import Generaltab_interface
import MH_basic_interface

class tkinterApp(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        
        container = tk.Frame(self)
        container.pack(side = "top", fill = "both", expand=True)
        
        container.grid_rowconfigure(0, weight = 1)
        container.grid_columnconfigure(0, weight = 1)
        
        self.frames = {}
        
        frame = Generaltab_interface.GeneraltabInterface(parent=container, controller=self)
        self.frames[Generaltab_interface.GeneraltabInterface] = frame

        frame = MH_basic_interface.MHBasicInterface(parent=container, controller=self)
        self.frames[MH_basic_interface.MHBasicInterface] = frame
        
        frame.grid(row=0, column=0, sticky="nsew")
        
        self.show_frame(Generaltab_interface.GeneraltabInterface)
            
    
    def show_frame(self, frame_class):
        frame = self.frames[frame_class]
        frame.tkraise()

if __name__ == "__main__":
    app = tkinterApp()
    app.geometry("1600x800")
    app.mainloop()