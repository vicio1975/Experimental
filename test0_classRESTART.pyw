# -*- coding: utf-8 -*-
"""
Created on Wed Dec 19 14:23:54 2018

@author: bmusammartanov
"""
import math
import tkinter as tk
from tkinter import filedialog
from tkinter import  messagebox
import datetime as tt
from PIL import Image, ImageTk

class fonts():
    #Fonts
    f_ver = ("arial", 7)
    f_8 = ("arial", 8)
    f_9 = ("arial", 9)
    f_10 = ("arial", 10)
    f_12 = ("arial", 12)
    f_IT6 = ("arial", 6, "italic")
    f_IT8 = ("arial", 8, "italic")
    f_IT9 = ("arial", 9, "italic")
    f_IT11 = ("arial", 11, "italic")
    f_BO7 = ("arial", 7, "bold")
    f_BO9 = ("arial", 9, "bold")
    f_BO10 = ("arial", 10, "bold")
    f_BO12 = ("arial", 12, "bold")

class Control:
    def __init__(self):
        self.root = tk.Tk()
        self.view = View(self.root)
        self.image = View.im(self.root)


    def run(self):
        self.root.title("Experimental Tard")
        self.root.deiconify()
        self.root.mainloop() 

class View():
    
    def __init__(self, master):
        master.geometry("1150x500+100+50")
        master.title("Experimental Test")
        master.resizable(width=False, height=False)

    def im(master):
        ### Bucher
        fs = fonts().f_ver
        vv = "2.0"
        img = ImageTk.PhotoImage(Image.open("buc_muni_co.png"), master=master)
        lb_im = tk.Label(master, image=img)
        lb_im.image = img
        lb_im.place(x=985, y=433)
        vers = tk.Label(master, text="Ver.{}".format(vv), font=fs)
        vers.place(x=1100, y=480)

        
class Calc:
      #Physics Constants
    Rf = 287.058 # Universal Constant of Gases [J/(Kg K)]
    pAtm = 101325 # [Pa] atmospheric pressure
    g = 9.806   # [m/s2] gravitational accelaration
    
    
    def fluid(self,temp):
        """Return the Fluid characteristics"""
        self.T = float(temp)
        self.t = self.T + 273.17 # Kelvin
        self.rot = self.pAtm/(self.Rf*self.t) #Density as function of temperature in Kelvin [Kg/mc]
        self.gamma_t = self.rot * self.g  #specific weight at t°C
        #Sutherland Equation
        self.ba = 1.458*10**(-6)
        self.sa = 110.4 #Kelvin
        self.mi_ = self.ba * (self.t**1.5)/(self.t + self.sa) #Dinamic Viscosity  Pa s = kg m^-1 s^-1
        self.ni = self.mi_ / self.rot         #Cinematic Viscosity  m2·s-1
        self.Fp = [self.rot, self.gamma_t, self.mi_, self.ni, self.T, self.t]
        
if __name__ == '__main__':
    c = Control()
    c.run()
#t = input("Set a temperature = ")
#F = Calc()
#F.fluid(t)
#print(F.Fp)