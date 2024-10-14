import tkinter as tk
from MH_basic_interface import MH_Basic_Interface
from people_interface import People_Interface

class main(tk.Tk):
    
    def __init__(self, *args, **kwargs):
        root = tk.Tk()

        self.pages = {}
        for F in (People_Interface, MH_Basic_Interface):
            page_name = F.__name__
            page = F(root=root, controller=self)
            self.pages[page_name] = page

            # put all of the pages in the same location;
            # the one on the top of the stacking order
            # will be the one that is visible.
            # page.grid(row=0, column=0, sticky="nsew")

        self.show_frame("People_Interface")

    def show_frame(self, page_name):
        '''Show a frame for the given page name'''
        frame = self.pages[page_name]
        frame.tkraise()

if __name__ == "__main__":
    m = main()
    m.mainloop()