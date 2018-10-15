#!/home/vicio75/anaconda3/bin/python3
# -*- coding: utf-8 -*-
"""
Created on Sun Oct 14 16:35:29 2018

@author: vicio75
"""
#import numpy as num
import tkinter as tk
#from tkinter import  messagebox
#from PIL import ImageTk, Image

#Tkinter window
root = tk.Tk() #new window
root.geometry("700x470+100+50")
root.title("Experimental Test")
root.resizable(width=False, height=False)

#Fonts
f_8 = ("arial",8)
f_9 = ("arial",9)
f_10 = ("arial",10)
f_12 = ("arial",12)

f_IT8 = ("arial",8,"italic")
f_IT8 = ("arial",8,"italic")
f_IT9 = ("arial",9,"italic")
f_IT11 = ("arial",11,"italic")
f_BO7 = ("arial",7,"bold")
f_BO9 = ("arial",9,"bold")
f_BO10 = ("arial",10,"bold")
f_BO12 = ("arial",12,"bold")

##columnconfig
root.rowconfigure(0, minsize=40)
root.rowconfigure(1, minsize=40)
root.rowconfigure(2, minsize=40)
root.rowconfigure(3, minsize=40)
root.rowconfigure(4, minsize=40)

#Constants
Rf = 287.058 # Universal Constant of Gases [J/(Kg K)]
pAtm = 101325 # [Pa] atmospheric pressure
g = 9.806   # [m/s2] gravitational accelaration
###

###Functions
def fluid():
    T = float(T_.get())
    t = T + 273.17 # Kelvin
    
    rot = pAtm/(Rf*t) #Density as function of temperature in Kelvin [Kg/mc]
    gamma_t = rot * g  #specific weight at t°C
    #Sutherland Equation
    ba = 1.458*10**(-6) 
    sa = 110.4 #Kelvin
    mi = ba * (t**1.5)/(t+sa) #Dinamic Viscosity  Pa s = kg m^-1 s^-1
    ni = mi/rot         #Cinematic Viscosity  m2·s-1
    Fp = [rot,gamma_t,mi,ni]

#    L0 = Label(root)
#    L0.config(text="{:10.4e}".format(Fp[0]),font=f_BO10,bg="white",width=22)
#    L0.place(x=455,y=yR+32)   
#    L1 = Label(root)
#    L1.config(text="{:10.4e}".format(Fp[2]),font=f_BO10,bg="white",width=22)
#    L1.place(x=455,y=yR+91)   
#    L2 = Label(root)
#    L2.config(text="{:10.4e}".format(Fp[3]),font=f_BO10,bg="white",width=22)
#    L2.place(x=455,y=yR+152)
    return Fp

#input part
#temperature selection    
l0 = tk.Label(root,text="Temperature", padx = 10,font=f_BO10)
l0.grid(row=0,column=0,sticky="w")
l0_1 = tk.Label(root,text="[°C]",padx = 10,font=f_BO10)
l0_1.grid(row=0,column=2)
T_ = tk.StringVar()
t1 = tk.Entry(root,textvariable= T_ , width=6,justify="center",font=f_10)
t1.grid(row=0,column=1)
t1.insert("end", 20)

##Pressure settings
for i in [1,2,3,4]:
    ttt  = "Pressure #{}".format(str(i))
    l = tk.Label(root,text= ttt, padx = 10,font=f_BO10)
    l.grid(row=i,column=0,sticky="w")
    l_1 = tk.Label(root,text="[cmH20]",padx = 10,font=f_BO10)
    l_1.grid(row=i,column=2)

#value definition
P_1 = tk.StringVar()
p1 = tk.Entry(root,textvariable= P_1 , width=6,justify="center",font=f_10)
p1.grid(row=1,column=1)
p1.insert("end", 0)

P_2 = tk.StringVar()
p2 = tk.Entry(root,textvariable= P_2 , width=6,justify="center",font=f_10)
p2.grid(row=2,column=1)
p2.insert("end", 0)

P_3 = tk.StringVar()
p3 = tk.Entry(root,textvariable= P_3 , width=6,justify="center",font=f_10)
p3.grid(row=3,column=1)
p3.insert("end", 0)

P_4 = tk.StringVar()
p4 = tk.Entry(root,textvariable= P_4 , width=6,justify="center",font=f_10)
p4.grid(row=4,column=1)
p4.insert("end", 0)

root.mainloop() #looping the frame