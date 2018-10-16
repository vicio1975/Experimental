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
rc = 40
for i in range(10):
    root.rowconfigure(i, minsize=rc)

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

#Atmospheric pressure selection    
atm0 = tk.Label(root,text="ATM pressure", padx = 10,font=f_BO10)
atm0.grid(row=1,column=0,sticky="w")
atm0_1 = tk.Label(root,text="[mbars]",padx = 10,font=f_BO10)
atm0_1.grid(row=1,column=2)
atm_ = tk.StringVar()
atm1 = tk.Entry(root,textvariable= atm_ , width=6,justify="center",font=f_10)
atm1.grid(row=1,column=1)
atm1.insert("end", 0)

#Engine Speed selection    
SpeedEn0 = tk.Label(root,text="Engine speed", padx = 10,font=f_BO10)
SpeedEn0.grid(row=2,column=0,sticky="w")
SpeedEn0_1 = tk.Label(root,text="[rpm]",padx = 10,font=f_BO10)
SpeedEn0_1.grid(row=2,column=2)
SpeedEn_ = tk.StringVar()
SpeedEn1 = tk.Entry(root,textvariable= SpeedEn_ , width=6,justify="center",font=f_10)
SpeedEn1.grid(row=2,column=1)
SpeedEn1.insert("end", 0)

#Fan Speed selection    
SpeedFan0 = tk.Label(root,text="Fan speed", padx = 10,font=f_BO10)
SpeedFan0.grid(row=3,column=0,sticky="w")
SpeedFan0_1 = tk.Label(root,text="[rpm]",padx = 10,font=f_BO10)
SpeedFan0_1.grid(row=3,column=2)
SpeedFan_ = tk.StringVar()
SpeedFan1 = tk.Entry(root,textvariable= SpeedFan_, width=6,justify="center",font=f_10)
SpeedFan1.grid(row=3,column=1)
SpeedFan1.insert("end", 0)

#Inlet tube Diameter    
D0 = tk.Label(root,text="Inlet Diameter", padx = 10,font=f_BO10)
D0.grid(row=4,column=0,sticky="w")
D0_1 = tk.Label(root,text="[mm]",padx = 10,font=f_BO10)
D0_1.grid(row=4,column=2)
D_ = tk.StringVar()
D1 = tk.Entry(root,textvariable= SpeedFan_, width=6,justify="center",font=f_10)
D1.grid(row=4,column=1)
D1.insert("end", 0)


Row0 = 5 #last row used in the this previous part + 1
RowF = Row0 + 6
Rows = [i for i in range(Row0,RowF)] #list of rows 

s = 0
##Pressure settings
for i in Rows:
    ttt  = "Pressure #{}".format(str(s))
    l = tk.Label(root,text= ttt, padx = 10,font=f_BO10)
    l.grid(row=s,column=3,sticky="w")
    l_1 = tk.Label(root,text="[cmH20]",padx = 10,font=f_BO10)
    l_1.grid(row=s,column=6)
    s += 1
#value definition
P_1 = tk.StringVar()
p1 = tk.Entry(root,textvariable= P_1 , width=6,justify="center",font=f_10)
p1.grid(row=0,column=4)
p1.insert("end", 0)

P_2 = tk.StringVar()
p2 = tk.Entry(root,textvariable= P_2 , width=6,justify="center",font=f_10)
p2.grid(row=1,column=4)
p2.insert("end", 0)

P_3 = tk.StringVar()
p3 = tk.Entry(root,textvariable= P_3 , width=6,justify="center",font=f_10)
p3.grid(row=2,column=4)
p3.insert("end", 0)

P_4 = tk.StringVar()
p4 = tk.Entry(root,textvariable= P_4 , width=6,justify="center",font=f_10)
p4.grid(row=3,column=4)
p4.insert("end", 0)

P_5 = tk.StringVar()
p5 = tk.Entry(root,textvariable= P_5 , width=6,justify="center",font=f_10)
p5.grid(row=4,column=4)
p5.insert("end", 0)

P_6 = tk.StringVar()
p6 = tk.Entry(root,textvariable= P_6 , width=6,justify="center",font=f_10)
p6.grid(row=5,column=4)
p6.insert("end", 0)


root.mainloop() #looping the frame