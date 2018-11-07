#!/home/vicio75/anaconda3/bin/python3
# -*- coding: utf-8 -*-
"""
Created on Sun Oct 14 16:35:29 2018

@author: vicio75
"""
import math
import tkinter as tk
from tkinter import  messagebox
#from PIL import ImageTk, Image

#Tkinter window
root = tk.Tk() #new window
root.geometry("1200x500+100+50")
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
for i in range(20):
    root.rowconfigure(i, minsize=rc)
wid = 10
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
    Fp = [rot,gamma_t,mi,ni,T,t]
    return Fp

def calculon():
    print(" ... in progress")
    #Fluid properties
    propfluid = fluid()
    t = propfluid[5] #temperature in Kelvin
    T = propfluid[4] #temperature in Celsius
    
    #Parameters reading
    Par =  [T, atm_.get(), SpeedEn_.get(), SpeedFan_.get(), D_.get()]
    Par = [float(p) for p in Par]
    patm = Par[1]
    Dduct = Par[4]
    staticP_ = float(staticP.get())
    staticFan_ = float(staticFan.get())
    staticBody_ = float(staticBody.get())

    #getting the total pressure values
    P_first =  [P_1_1.get(), P_2_1.get(),P_3_1.get(), P_4_1.get(),P_5_1.get(), P_6_1.get()]
    P_first = [float(p) for p in P_first]
    P_second = [P_1_2.get(), P_2_2.get(),P_3_2.get(), P_4_2.get(),P_5_2.get(), P_6_2.get()]
    P_second = [float(p) for p in P_second]

    P_first2 = [(p)**2 for p in P_first]
    P_second2 = [(p)**2 for p in P_second]
    
    ####Error Messages
    if Par[2] == 0:
        messagebox.showwarning("Warning","The Engine speed is 0!")
    if Par[3] == 0:
        messagebox.showwarning("Warning","The Fan speed is 0!")
    if Par[4] == 0:
        messagebox.showwarning("Warning","The intake tube diameter is 0!")

    for i,p in enumerate(P_first):
        if p == 0:
            messagebox.showwarning("Warning","First Pass - Total pressure #{} is 0!".format(str(i+1)))

    for i,p in enumerate(P_second):
        if p == 0:
            messagebox.showwarning("Warning","Second Pass - Total pressure #{} is 0!".format(str(i+1)))
    if staticP_ == 0:
        messagebox.showwarning("Warning","The static pressure is 0!")
    ##################

    #Estimations
    AVGH = (((sum(P_first2)+sum(P_second2))/12)**0.5)*10 *(t/293)*(1013/patm)*(10363/(10363+(staticP_*10)))
    Aduct = (0.25*math.pi*(Dduct/1000)**2)
    Vduct = 4.032*(AVGH)**0.5 
    Qduct = Aduct*Vduct
    #static pressure correction
    staticFan_ = staticFan_ * (t/293)*(1013/patm)
    staticBody_ = staticBody_ * (t/293)*(1013/patm)
    #Developed Power
    devPow = Qduct * abs(staticFan_*58.84*1000/600)/1000

    #Estimation label
    avgh = "{:2.2f}".format(AVGH) 
    avg = tk.Label(root,text = avgh, padx = 10, bg = "white", font=f_BO10)
    avg.grid(row = 8, column = 1)

    vduct = "{:2.3f}".format(Vduct)
    vlab = tk.Label(root,text = vduct, padx = 10, bg = "white", font=f_BO10)
    vlab.grid(row = 9, column = 1)

    qduct = "{:2.3f}".format(Qduct)
    qlab = tk.Label(root,text = qduct, padx = 10, bg = "white", font=f_BO10)
    qlab.grid(row = 10, column = 1)

    density = "{:2.5f}".format(propfluid[0]) 
    den = tk.Label(root,text=density,padx = 10, bg = "white",font=f_BO10)
    den.grid(row = 11, column = 1)

    fanc = "{:2.2f}".format(staticFan_) 
    fan = tk.Label(root,text = fanc, padx = 10, bg = "white", font=f_BO10)
    fan.grid(row = 8, column = 4)

    bodyc = "{:2.2f}".format(staticBody_) 
    body = tk.Label(root,text = bodyc, padx = 10, bg = "white", font=f_BO10)
    body.grid(row = 9, column = 4)

    devPowc = "{:2.2f}".format(devPow) 
    devl = tk.Label(root,text = devPowc, padx = 10, bg = "white", font=f_BO10)
    devl.grid(row = 10, column = 4)


###############
### input part

#Labels
l00 = tk.Label(root,text="Parameters", font = f_BO12)
l00.grid(row=0,column=0,sticky="e") 
l01 = tk.Label(root,text="First Pass", font = f_BO12)
l01.grid(row=0,column=3,sticky="e") 
l02 = tk.Label(root,text="Second Pass", font = f_BO12)
l02.grid(row=0,column=7,sticky="e") 
l03 = tk.Label(root,text="Static Pressure", font = f_BO12)
l03.grid(row=0,column=10,sticky="e") 

#temperature selection    
l0 = tk.Label(root,text="Temperature", padx = 10,font=f_BO10)
l0.grid(row=1,column=0,sticky="e")
l0_1 = tk.Label(root,text="[°C]",padx = 10,font=f_BO10)
l0_1.grid(row=1,column=2,sticky="w")
T_ = tk.StringVar()
t1 = tk.Entry(root,textvariable= T_ , width=wid,justify="center",font=f_10)
t1.grid(row=1,column=1)
t1.insert("end", 20)

#Atmospheric pressure selection    
atm0 = tk.Label(root,text="ATM pressure", padx = 10,font=f_BO10)
atm0.grid(row=2,column=0,sticky="e")
atm0_1 = tk.Label(root,text="[mbars]",padx = 10,font=f_BO10)
atm0_1.grid(row=2,column=2,sticky="w")
atm_ = tk.StringVar()
atm1 = tk.Entry(root,textvariable= atm_ , width=wid,justify="center",font=f_10)
atm1.grid(row=2,column=1)
atm1.insert("end", 1016)

#Engine Speed selection    
SpeedEn0 = tk.Label(root,text="Engine speed", padx = 10,font=f_BO10)
SpeedEn0.grid(row=3,column=0,sticky="e")
SpeedEn0_1 = tk.Label(root,text="[rpm]",padx = 10,font=f_BO10)
SpeedEn0_1.grid(row=3,column=2,sticky="w")
SpeedEn_ = tk.StringVar()
SpeedEn1 = tk.Entry(root,textvariable= SpeedEn_ , width=wid,justify="center",font=f_10)
SpeedEn1.grid(row=3,column=1)
SpeedEn1.insert("end", 0)

#Fan Speed selection    
SpeedFan0 = tk.Label(root,text="Fan speed", padx = 10,font=f_BO10)
SpeedFan0.grid(row=4,column=0,sticky="e")
SpeedFan0_1 = tk.Label(root,text="[rpm]",padx = 10,font=f_BO10)
SpeedFan0_1.grid(row=4,column=2,sticky="w")
SpeedFan_ = tk.StringVar()
SpeedFan1 = tk.Entry(root,textvariable= SpeedFan_, width=wid,justify="center",font=f_10)
SpeedFan1.grid(row=4,column=1)
SpeedFan1.insert("end", 0)

#Inlet tube Diameter    
D0 = tk.Label(root,text="Inlet Diameter", padx = 10,font=f_BO10)
D0.grid(row=5,column=0,sticky="e")
D0_1 = tk.Label(root,text="[mm]",padx = 10,font=f_BO10)
D0_1.grid(row=5,column=2,sticky="w")
D_ = tk.StringVar()
D1 = tk.Entry(root,textvariable= D_, width=wid,justify="center",font=f_10)
D1.grid(row=5,column=1)
D1.insert("end", 0)

Row0 = 6 #last row used in the this previous part + 1
RowF = Row0 + 6
Rows = [i for i in range(Row0,RowF)] #list of rows 

s = 1
##Pressure first pass
for i in Rows:
    ttt  = "Total Pressure #{}".format(str(s))
    l = tk.Label(root,text= ttt, padx = 15,font=f_BO10)
    l.grid(row=s,column=3,sticky="e")
    l_1 = tk.Label(root,text="[cmH20]",padx = 10,font=f_BO10)
    l_1.grid(row=s,column=5,sticky="w")
    s += 1

s = 1
##Pressure second pass
for i in Rows:
    ttt  = "Total Pressure #{}".format(str(s))
    l = tk.Label(root,text= ttt, padx = 15  ,font=f_BO10)
    l.grid(row=s,column=7,sticky="e")
    l_1 = tk.Label(root,text="[cmH20]",padx = 10,font=f_BO10)
    l_1.grid(row=s,column=9,sticky="w")
    s += 1

#value definition First Pass
P_1_1 = tk.StringVar()
p1_1 = tk.Entry(root,textvariable= P_1_1 , width=wid,justify="center",font=f_10)
p1_1.grid(row=1,column=4,sticky="w")
p1_1.insert("end", 0)

P_2_1 = tk.StringVar()
p2_1 = tk.Entry(root,textvariable= P_2_1 , width=wid,justify="center",font=f_10)
p2_1.grid(row=2,column=4,sticky="w")
p2_1.insert("end", 0)

P_3_1 = tk.StringVar()
p3_1 = tk.Entry(root,textvariable= P_3_1 , width=wid,justify="center",font=f_10)
p3_1.grid(row=3,column=4,sticky="w")
p3_1.insert("end", 0)

P_4_1 = tk.StringVar()
p4_1 = tk.Entry(root,textvariable= P_4_1 , width=wid,justify="center",font=f_10)
p4_1.grid(row=4,column=4,sticky="w")
p4_1.insert("end", 0)

P_5_1 = tk.StringVar()
p5_1 = tk.Entry(root,textvariable= P_5_1 , width=wid,justify="center",font=f_10)
p5_1.grid(row=5,column=4,sticky="w")
p5_1.insert("end", 0)

P_6_1 = tk.StringVar()
p6_1 = tk.Entry(root,textvariable= P_6_1 , width=wid,justify="center",font=f_10)
p6_1.grid(row=6,column=4,sticky="w")
p6_1.insert("end", 0)

#value definition Second Pass
P_1_2 = tk.StringVar()
p1_2 = tk.Entry(root,textvariable= P_1_2 , width=wid,justify="center",font=f_10)
p1_2.grid(row=1,column=8,sticky="w")
p1_2.insert("end", 0)

P_2_2 = tk.StringVar()
p2_2 = tk.Entry(root,textvariable= P_2_2 , width=wid,justify="center",font=f_10)
p2_2.grid(row=2,column=8,sticky="w")
p2_2.insert("end", 0)

P_3_2 = tk.StringVar()
p3_2 = tk.Entry(root,textvariable= P_3_2 , width=wid,justify="center",font=f_10)
p3_2.grid(row=3,column=8,sticky="w")
p3_2.insert("end", 0)

P_4_2 = tk.StringVar()
p4_2 = tk.Entry(root,textvariable= P_4_2 , width=wid,justify="center",font=f_10)
p4_2.grid(row=4,column=8,sticky="w")
p4_2.insert("end", 0)

P_5_2 = tk.StringVar()
p5_2 = tk.Entry(root,textvariable= P_5_2 , width=wid,justify="center",font=f_10)
p5_2.grid(row=5,column=8,sticky="w")
p5_2.insert("end", 0)

P_6_2 = tk.StringVar()
p6_2 = tk.Entry(root,textvariable= P_6_2 , width=wid,justify="center",font=f_10)
p6_2.grid(row=6,column=8,sticky="w")
p6_2.insert("end", 0)

#Static Pressure
s1  = "Duct Pressure"
s1 = tk.Label(root,text= s1, padx = 15  ,font=f_BO10)
s1.grid(row=1,column=10,sticky="e")
s1_1 = tk.Label(root,text="[cmH20]",padx = 10,font=f_BO10)
s1_1.grid(row=1,column=12,sticky="w")
    
staticP = tk.StringVar()
stp = tk.Entry(root,textvariable= staticP, width=wid,justify="center",font=f_10)
stp.grid(row=1,column=11,sticky="w")
stp.insert("end", 0)

#Fan pressure
s2  = "Fan Pressure"
s2 = tk.Label(root,text= s2, padx = 15  ,font=f_BO10)
s2.grid(row=2,column=10,sticky="e")
s2_1 = tk.Label(root,text="[cmH20]",padx = 10,font=f_BO10)
s2_1.grid(row=2,column=12,sticky="w")
    
staticFan = tk.StringVar()
stf = tk.Entry(root,textvariable = staticFan, width=wid,justify="center",font=f_10)
stf.grid(row=2,column=11,sticky="w")
stf.insert("end", 0)

#body pressure
s3 = "Body Pressure"
s3 = tk.Label(root,text= s3, padx = 15  ,font=f_BO10)
s3.grid(row=3,column=10,sticky="e")
s3_1 = tk.Label(root,text="[cmH20]",padx = 10,font=f_BO10)
s3_1.grid(row=3,column=12,sticky="w")
    
staticBody = tk.StringVar()
stb = tk.Entry(root,textvariable = staticBody, width=wid,justify="center",font=f_10)
stb.grid(row=3,column=11,sticky="w")
stb.insert("end", 0)
########################################################### END input section ###

######################
###### Results Part
l03 = tk.Label(root,text="Corrected values", font = f_BO12)
l03.grid(row=7,column=0) 

r1  = "Avg Total pressure "
r1 = tk.Label(root,text= r1, padx = 15  ,font=f_BO10)
r1.grid(row=8,column=0,sticky="e")
r1_1 = tk.Label(root,text="[mmH20]",padx = 10,font=f_BO10)
r1_1.grid(row=8,column=2,sticky="w")

frame1 = tk.Frame(width=80,height=25, bg="white", colormap="new",relief=tk.SUNKEN ,bd=2)
frame1.grid(row=8,column=1)

r2  = "Duct Velocity"
r2 = tk.Label(root,text= r2, padx = 15  ,font=f_BO10)
r2.grid(row=9,column=0,sticky="e")
r2_1 = tk.Label(root,text="[m/s]",padx = 10,font=f_BO10)
r2_1.grid(row=9,column=2,sticky="w")

frame2 = tk.Frame(width=80,height=25, bg="white", colormap="new",relief=tk.SUNKEN ,bd=2)
frame2.grid(row=9,column=1)

r3  = "Flow rate"
r3 = tk.Label(root,text = r3, padx = 15  ,font=f_BO10)
r3.grid(row=10,column=0,sticky="e")
r3_1 = tk.Label(root,text="[m\u00b3/s]",padx = 10,font=f_BO10)
r3_1.grid(row=10,column=2,sticky="w")

frame3 = tk.Frame(width=80,height=25, bg="white",colormap="new",relief=tk.SUNKEN ,bd=2)
frame3.grid(row=10,column=1)

r4  = "Density"
r4 = tk.Label(root,text = r4, padx = 15  ,font=f_BO10)
r4.grid(row=11,column=0,sticky="e")
r4_1 = tk.Label(root,text="[kg/m\u00b3]",padx = 10,font=f_BO10)
r4_1.grid(row=11,column=2,sticky="w")

frame4 = tk.Frame(width=80,height=25, bg="white",colormap="new",relief=tk.SUNKEN ,bd=2)
frame4.grid(row=11,column=1)

r5  = "Fan Pressure"
r5 = tk.Label(root,text= r5, padx = 15  ,font=f_BO10)
r5.grid(row=8,column=3,sticky="e")
r5_1 = tk.Label(root,text="[cmH20]",padx = 10,font=f_BO10)
r5_1.grid(row=8,column=5,sticky="w")

frame5 = tk.Frame(width=80,height=25, bg="white",colormap="new",relief=tk.SUNKEN ,bd=2)
frame5.grid(row=8,column=4)

r6  = "Body Pressure"
r6 = tk.Label(root,text= r6, padx = 15  ,font=f_BO10)
r6.grid(row=9,column=3,sticky="e")
r6_1 = tk.Label(root,text="[cmH20]",padx = 10,font=f_BO10)
r6_1.grid(row=9,column=5,sticky="w")

frame6 = tk.Frame(width=80,height=25, bg="white",colormap="new",relief=tk.SUNKEN ,bd=2)
frame6.grid(row=9,column=4)

r7  = "Developed Power"
r7 = tk.Label(root,text= r7, padx = 15  ,font=f_BO10)
r7.grid(row=10,column=3,sticky="e")
r7_1 = tk.Label(root,text="[kW]",padx = 10,font=f_BO10)
r7_1.grid(row=10,column=5,sticky="w")

frame7 = tk.Frame(width=80,height=25, bg="white",colormap="new",relief=tk.SUNKEN ,bd=2)
frame7.grid(row=10,column=4)


###################
#####   Buttons
b0 = tk.Button(root,text="Calculate",command=calculon,font=f_BO12) #command=calc,
b0.config( height = 2, width = 8)
b0.place(x=975,y=300)

ln = tk.Button(root,text="Exit",command=root.destroy,font=f_BO12)
ln.config( height = 2, width = 8)
ln.place(x=975,y=360)
#####################

root.mainloop() #looping the frame