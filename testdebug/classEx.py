# -*- coding: utf-8 -*-
"""
Created on Tue Dec 18 14:13:14 2018

@author: bmusammartanov
"""


import tkinter as tk

class Demo1:
    def __init__(self, master):
        self.master = master
        self.frame = tk.Frame(self.master)
        self.button1 = tk.Button(self.frame, text = 'New Window', width = 25, command = self.new_window)
        self.button1.pack()
        self.frame.pack()
    def new_window(self):
        self.newWindow = tk.Toplevel(self.master)
        self.app = Demo2(self.newWindow)

class Demo2:
    def __init__(self, master):
        self.master = master
        self.frame = tk.Frame(self.master)
        self.quitButton = tk.Button(self.frame, text = 'Quit', width = 25, command = self.close_windows)
        self.quitButton.pack()
        self.frame.pack()
    def close_windows(self):
        self.master.destroy()

def main(): 
    root = tk.Tk()
    Demo1(root)
    root.mainloop()

if __name__ == '__main__':
    main()


#class Navbar(tk.Frame): ...
#class Toolbar(tk.Frame): ...
#class Statusbar(tk.Frame): ...
#class Main(tk.Frame): ...
#
#class MainApplication(tk.Frame):
#    def __init__(self, parent, *args, **kwargs):
#        tk.Frame.__init__(self, parent, *args, **kwargs)
#        self.statusbar = Statusbar(self, ...)
#        self.toolbar = Toolbar(self, ...)
#        self.navbar = Navbar(self, ...)
#        self.main = Main(self, ...)
#
#        self.statusbar.pack(side="bottom", fill="x")
#        self.toolbar.pack(side="top", fill="x")
#        self.navbar.pack(side="left", fill="y")
#        self.main.pack(side="right", fill="both", expand=True)
#        
#if __name__ == "__main__":
#    root = tk.Tk()
#    MainApplication(root).pack(side="top", fill="both", expand=True)
#    root.mainloop()