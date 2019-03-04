#! /usr/bin/python3

# -*- coding: utf-8 -*-
"""
Created on Sun Oct 14 16:35:29 2018
#http://www.science.smith.edu/dftwiki/index.php/Color_Charts_for_TKinter
@author: vicio75
"""
import math
import tkinter as tk
from tkinter import filedialog
from tkinter import  messagebox
import datetime as tt
from tkinter import PhotoImage

##To solve import PIL
try:
    from PIL import Image, ImageTk
except ImportError:
    print("NO module found")
    import Image  #noshow
    print("Image has been imported")

# pylint: disable=locally-disabled, invalid-name
#Time
time_ = tt.datetime.now().strftime("%d/%m/%Y - %H:%M:%S")
#Tkinter window

root = tk.Tk() #new window # pylint: disable=locally-disabled, invalid-name
root.geometry("1210x500+50+50")
root.title("Pitot-static probe")
root.resizable(width=False, height=False)
root.configure(bg="grey77")

root.iconbitmap(r'fan.ico')

### Decorators
frame00 = tk.Frame(width=320, height=280, colormap="new", relief="sunken", bd=1)
frame00.place(x=25, y=3)
frame01 = tk.Frame(width=845, height=280, colormap="new", relief="sunken", bd=1)
frame01.place(x=350, y=3)
frame02 = tk.Frame(width=645, height=200, colormap="new", relief="sunken", bd=1)
frame02.place(x=25, y=288)

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

##rows and columns configuration
rc = 40
cc = 40
for i in range(40):
    root.rowconfigure(i, minsize=rc)
for i in range(40):
    root.columnconfigure(i, minsize=cc)
root.columnconfigure(0, minsize=160)#col0
root.columnconfigure(2, minsize=120)#col0
root.columnconfigure(3, minsize=80)#col0
root.columnconfigure(6, minsize=130)#col0
root.columnconfigure(9, minsize=160)#col0
wid = 10
widout = 80

#Constants
Rf = 287.058 # Universal Constant of Gases [J/(Kg K)]
pAtm = 101325 # [Pa] atmospheric pressure
g = 9.806   # [m/s2] gravitational accelaration
###

data = []

##Functions
def fluid():
    """Return the Fluid characteristics"""
    T = float(T_.get())
    t = T + 273.17 # Kelvin
    rot = pAtm/(Rf*t) #Density as function of temperature in Kelvin [Kg/mc]
    gamma_t = rot * g  #specific weight at t°C
    #Sutherland Equation
    ba = 1.458*10**(-6)
    sa = 110.4 #Kelvin
    mi_ = ba * (t**1.5)/(t+sa) #Dinamic Viscosity  Pa s = kg m^-1 s^-1
    ni = mi_ / rot         #Cinematic Viscosity  m2·s-1
    Fp = [rot, gamma_t, mi_, ni, T, t]
    return Fp

def calculon():
    """Execute the velocity estimation"""
    global Par, staticP_, staticFan_, staticBody_, P_first, P_second, AVGH,\
    Vduct, Qduct, devPow, conPow, remark

    #Fluid properties
    propfluid = fluid()
    t = float(propfluid[5]) #temperature in Kelvin
    #Parameters reading
    Par = [atm_.get(), SpeedEn_.get(), SpeedFan_.get(), D_.get(), Tor_.get()]
    Par = [float(p) for p in Par]

    staticP_ = float(staticP.get())
    staticFan_ = float(staticFan.get())
    staticBody_ = float(staticBody.get())
    #getting the total pressure values
    P_first = [P_1_1.get(), P_2_1.get(), P_3_1.get(), P_4_1.get(), P_5_1.get(), P_6_1.get()]
    P_first = [float(p) for p in P_first]
    P_second = [P_1_2.get(), P_2_2.get(), P_3_2.get(), P_4_2.get(), P_5_2.get(), P_6_2.get()]
    P_second = [float(p) for p in P_second]

    P_first2 = [(p)**2 for p in P_first]
    P_second2 = [(p)**2 for p in P_second]
    ####Error Messages
    if Par[1] == 0:
        messagebox.showwarning("Warning", "The Engine speed is 0!")
    if Par[2] == 0:
        messagebox.showwarning("Warning", "The Fan speed is 0!")
    if Par[3] == 0:
        messagebox.showwarning("Warning", "The intake tube diameter is 0!")
    if Par[4] == 0:
        messagebox.showwarning("Warning", "The torque is 0!")

    pp = []
    tt = ""
    for j, p in enumerate(P_first):
        if p == 0: tt += (str(j+1)+",")
    if 0 in P_first:
        tx0 = "First Pass - dynamic pressure #{} = 0!".format(tt[:-1])
        messagebox.showwarning("Warning", tx0)

    pp = []
    tt = ""
    for ii, p in enumerate(P_second):
        if p == 0: tt += (str(ii+1)+",")
    if 0 in P_second:
        tx1 = "Second Pass - dynamic pressure #{} = 0!".format(tt[:-1])
        messagebox.showwarning("Warning", tx1)

    if staticP_ == 0:
        messagebox.showwarning("Warning", "The static pressure is 0!")
    ##################

    ########>>>> Estimations <<<<##############
    AVGH = (((sum(P_first2)+sum(P_second2))/12)**0.5)*10 \
    * (t/293) * (1013/Par[0]) * (10363/(10363+staticP_*10)) #averaged value of the dynamic pressure
    Aduct = (0.25*math.pi*(Par[3]/1000)**2)
    Vduct = 4.032*(AVGH)**0.5 #averaged value of the velocity
    Qduct = Aduct*Vduct #volume flow rate
    #static pressure correction
    staticFan_ = staticFan_ * (t/293) * (1013/Par[0])
    staticBody_ = staticBody_ * (t/293) * (1013/Par[0])
    #Developed Power
    devPow = Qduct * abs(staticFan_*58.84*1000/600)/1000
    #Consumed Power
    conPow = Par[4]*(Par[2]*2*math.pi/60)/1000
    ###########################################

    #Estimation labels
    avg = tk.Label(root, text="{:2.2f}".format(AVGH), padx=10, bg="white", font=f_BO10)
    avg.grid(row=8, column=1)

    vlab = tk.Label(root, text="{:2.3f}".format(Vduct), padx=10, bg="white", font=f_BO10)
    vlab.grid(row=9, column=1)

    qlab = tk.Label(root, text="{:2.3f}".format(Qduct), padx=10, bg="white", font=f_BO10)
    qlab.grid(row=10, column=1)

    den = tk.Label(root, text="{:2.5f}".format(propfluid[0]), padx=10, bg="white", font=f_BO10)
    den.grid(row=11, column=1)

    fan = tk.Label(root, text="{:2.2f}".format(staticFan_), padx=10, bg="white", font=f_BO10)
    fan.grid(row=8, column=4)

    body = tk.Label(root, text="{:2.2f}".format(staticBody_), padx=10, bg="white", font=f_BO10)
    body.grid(row=9, column=4)

    devl = tk.Label(root, text="{:2.2f}".format(devPow), padx=10, bg="white", font=f_BO10)
    devl.grid(row=10, column=4)

    conl = tk.Label(root, text="{:2.2f}".format(conPow), padx=10, bg="white", font=f_BO10)
    conl.grid(row=11, column=4)

    remark = text.get("1.0", "end-1c")
    if remark == "Insert here some remarks":
        messagebox.showwarning("Warning", "No comments have been added!")

#Cleaning values
def ClEaN_1():
    """ Clean values first pass """
    messagebox.showwarning("Warning", "You are deleting the First Pass data!")
    for ll in [P_1_1, P_2_1, P_3_1, P_4_1, P_5_1, P_6_1]:
        ll.set(0)

def ClEaN_2():
    """ Clean values second pass """
    messagebox.showwarning("Warning", "You are deleting the Second Pass data!")
    for m in [P_1_2, P_2_2, P_3_2, P_4_2, P_5_2, P_6_2]:
        m.set(0)

def saveEx(Par, staticP_, staticFan_, staticBody_, P_first, P_second, AVGH, \
           Vduct, Qduct, devPow, conPow, remark):
    """
    
    - Creating the data list and Saving data
    
    """
    header = ["Atm pressure(mbars)", "Engine Speed(rpm)", "Fan Speed(rpm)",
              "Inlet Diameter(mm)", "Static Pressure(cmH2O)",
              "Static Fan Pressure(cmH2O)", "Static Body Pressure(cmH2O)",
              "P1st(cmH2O)", "P2st(cmH2O)", "P3st(cmH2O)",
              "P4st(cmH2O)", "P5st(cmH2O)", "P6st(cmH2O)",
              "P1nd(cmH2O)", "P2nd(cmH2O)", "P3nd(cmH2O)",
              "P4nd(cmH2O)", "P5nd(cmH2O)", "P6nd(cmH2O)",
              "Avg Tot pressure (mmH2O)", "Velocity(m/s)",
              "Flow Rate(m^3/s)", "Fan Pressure(cmH2O)",
              "Body Pressure(cmH2O)", "Developed Power(kW)", "Consumed Power(kW)", "Remarks"]
    
    ##### data list creation
    for I in Par:
        data.append(I)
    data.append(staticP_)
    data.append(staticFan_)
    data.append(staticBody_)
    for J in P_first:
        data.append(J)
    for II in P_second:
        data.append(II)
    for JJ in [AVGH, Vduct, Qduct, staticFan_, staticBody_, devPow, conPow]:
        data.append(JJ)
    data.append(remark)
    data.append("\n")

    f = filedialog.asksaveasfile(mode="w", defaultextension=".csv")
    f.write(time_+"\n")
    if f is None:
        return
    for head in header:
        ss0 = head + ","
        f.write(ss0)
    f.write("\n")

    for item in data:
        if item == "\n":
            ss1 = "\n"
        elif isinstance(item, str):
            ss1 = item+","
        else:
            ss1 = str("{:2.5f}".format(item))+","
        f.write(ss1)
    f.close()
    
def close():
    """
    Close the UI
    """
    root.destroy()

###############
### inputs section
#Labels
l00 = tk.Label(root, text="Parameters", font=f_BO12)
l00.place(x=156, y=8)
l01 = tk.Label(root, text="Dynamic Pressure - Pass #1", font=f_BO12)
l01.place(x=365, y=8)
l02 = tk.Label(root, text="Dynamic Pressure - Pass #2", font=f_BO12)
l02.place(x=650, y=8)
l03 = tk.Label(root, text="Static Pressure", font=f_BO12, padx=10)
l03.place(x=988, y=8)

#Temperature selection
l0 = tk.Label(root, text="Temperature", font=f_BO10, padx=0)
l0.grid(row=1, column=0, sticky="e", ipadx=5)
T_ = tk.StringVar()
t1 = tk.Entry(root, textvariable=T_, width=wid, justify="center", font=f_10)
t1.grid(row=1, column=1, sticky="we")
t1.insert("end", 20)
l0_1 = tk.Label(root, text="[°C]", padx=5, font=f_BO10)
l0_1.grid(row=1, column=2, sticky="w")

#Atmospheric pressure selection
atm0 = tk.Label(root, text="ATM pressure", font=f_BO10)
atm0.grid(row=2, column=0, sticky="e", ipadx=5)
atm_ = tk.StringVar()
atm1 = tk.Entry(root, textvariable=atm_, width=wid, justify="center", font=f_10)
atm1.grid(row=2, column=1, sticky="we")
atm1.insert("end", 1016)
atm0_1 = tk.Label(root, text="[mbars]", padx=5, font=f_BO10)
atm0_1.grid(row=2, column=2, sticky="w")

#Engine Speed selection
SpeedEn0 = tk.Label(root, text="Engine speed", font=f_BO10)
SpeedEn0.grid(row=3, column=0, sticky="e", ipadx=5)
SpeedEn_ = tk.StringVar()
SpeedEn1 = tk.Entry(root, textvariable=SpeedEn_, width=wid, justify="center", font=f_10)
SpeedEn1.grid(row=3, column=1, sticky="we")
SpeedEn1.insert("end", 0)
SpeedEn0_1 = tk.Label(root, text="[rpm]", padx=5, font=f_BO10)
SpeedEn0_1.grid(row=3, column=2, sticky="w")

#Fan Speed selection
SpeedFan0 = tk.Label(root, text="Fan speed", font=f_BO10)
SpeedFan0.grid(row=4, column=0, sticky="e", ipadx=5)
SpeedFan_ = tk.StringVar()
SpeedFan1 = tk.Entry(root, textvariable=SpeedFan_, width=wid, justify="center", font=f_10)
SpeedFan1.grid(row=4, column=1, sticky="we")
SpeedFan1.insert("end", 0)
SpeedFan0_1 = tk.Label(root, text="[rpm]", padx=5, font=f_BO10)
SpeedFan0_1.grid(row=4, column=2, sticky="w")

#Inlet tube Diameter
D0 = tk.Label(root, text="Inlet Diameter", font=f_BO10)
D0.grid(row=5, column=0, sticky="e", ipadx=5)
D_ = tk.StringVar()
D1 = tk.Entry(root, textvariable=D_, width=wid, justify="center", font=f_10)
D1.grid(row=5, column=1, sticky="we")
D1.insert("end", 0)
D0_1 = tk.Label(root, text="[mm]", padx=5, font=f_BO10)
D0_1.grid(row=5, column=2, sticky="w")

#Impeller torque
Tor = tk.Label(root, text="Torque", font=f_BO10)
Tor.grid(row=6, column=0, sticky="e", ipadx=5)
Tor_ = tk.StringVar()
T1 = tk.Entry(root, textvariable=Tor_, width=wid, justify="center", font=f_10)
T1.grid(row=6, column=1, sticky="we")
T1.insert("end", 0)
T1_1 = tk.Label(root, text="[Nm]", padx=5, font=f_BO10)
T1_1.grid(row=6, column=2, sticky="w")

lastRow = 6
Row0 = lastRow + 1 #last row used in the this previous part + 1
RowF = Row0 + 6
Rows = [i for i in range(Row0, RowF)] #list of rows

s = 1
##Dynamic Pressure first pass
for i in Rows:
    ttt = "Value #{}".format(str(s))
    l = tk.Label(root, text=ttt, padx=0, font=f_BO10)
    l.grid(row=s, column=3, ipadx=0)
    l_1 = tk.Label(root, text="[cmH20]", padx=5, font=f_BO10)
    l_1.grid(row=s, column=5, sticky="w", ipadx=0)
    s += 1
s = 1
##Dynamic Pressure second pass
for i in Rows:
    ttt = "Value #{}".format(str(s))
    ll = tk.Label(root, text=ttt, padx=0, font=f_BO10)
    ll.grid(row=s, column=6, sticky="e", ipadx=10)
    l_2 = tk.Label(root, text="[cmH20]", padx=5, font=f_BO10)
    l_2.grid(row=s, column=8, sticky="w", ipadx=0)
    s += 1

#Values First Pass
P_1_1 = tk.StringVar()
p1_1 = tk.Entry(root, textvariable=P_1_1, width=wid, justify="center", font=f_10)
p1_1.grid(row=1, column=4)
p1_1.insert("end", 0)

P_2_1 = tk.StringVar()
p2_1 = tk.Entry(root, textvariable=P_2_1, width=wid, justify="center", font=f_10)
p2_1.grid(row=2, column=4)
p2_1.insert("end", 0)

P_3_1 = tk.StringVar()
p3_1 = tk.Entry(root, textvariable=P_3_1, width=wid, justify="center", font=f_10)
p3_1.grid(row=3, column=4)
p3_1.insert("end", 0)

P_4_1 = tk.StringVar()
p4_1 = tk.Entry(root, textvariable=P_4_1, width=wid, justify="center", font=f_10)
p4_1.grid(row=4, column=4)
p4_1.insert("end", 0)

P_5_1 = tk.StringVar()
p5_1 = tk.Entry(root, textvariable=P_5_1, width=wid, justify="center", font=f_10)
p5_1.grid(row=5, column=4)
p5_1.insert("end", 0)

P_6_1 = tk.StringVar()
p6_1 = tk.Entry(root, textvariable=P_6_1, width=wid, justify="center", font=f_10)
p6_1.grid(row=6, column=4) 
p6_1.insert("end", 0)

#Values Second Pass
P_1_2 = tk.StringVar()
p1_2 = tk.Entry(root, textvariable=P_1_2, width=wid, justify="center", font=f_10)
p1_2.grid(row=1, column=7)
p1_2.insert("end", 0)

P_2_2 = tk.StringVar()
p2_2 = tk.Entry(root, textvariable=P_2_2, width=wid, justify="center", font=f_10)
p2_2.grid(row=2, column=7)
p2_2.insert("end", 0)

P_3_2 = tk.StringVar()
p3_2 = tk.Entry(root, textvariable=P_3_2, width=wid, justify="center", font=f_10)
p3_2.grid(row=3, column=7)
p3_2.insert("end", 0)

P_4_2 = tk.StringVar()
p4_2 = tk.Entry(root, textvariable=P_4_2, width=wid, justify="center", font=f_10)
p4_2.grid(row=4, column=7)
p4_2.insert("end", 0)

P_5_2 = tk.StringVar()
p5_2 = tk.Entry(root, textvariable=P_5_2, width=wid, justify="center", font=f_10)
p5_2.grid(row=5, column=7)
p5_2.insert("end", 0)

P_6_2 = tk.StringVar()
p6_2 = tk.Entry(root, textvariable=P_6_2, width=wid, justify="center", font=f_10)
p6_2.grid(row=6, column=7)
p6_2.insert("end", 0)

#Duct Pressure
s1 = "Duct Pressure"
s1 = tk.Label(root, text=s1, padx=0, font=f_BO10)
s1.grid(row=1, column=9, sticky="e", ipadx=10)
s1_1 = tk.Label(root, text="[cmH20]", padx=5, font=f_BO10)
s1_1.grid(row=1, column=11, sticky="w", ipadx=0)

staticP = tk.StringVar()
stp = tk.Entry(root, textvariable=staticP, width=wid, justify="center", font=f_10)
stp.grid(row=1, column=10)
stp.insert("end", 0)

#Fan pressure
s2 = "Fan Pressure"
s2 = tk.Label(root, text=s2, padx=0, font=f_BO10)
s2.grid(row=2, column=9, sticky="e", ipadx=10)
s2_1 = tk.Label(root, text="[cmH20]", padx=5, font=f_BO10)
s2_1.grid(row=2, column=11, sticky="w", ipadx=0)

staticFan = tk.StringVar()
stf = tk.Entry(root, textvariable=staticFan, width=wid, justify="center", font=f_10)
stf.grid(row=2, column=10)
stf.insert("end", 0)

#Body pressure
s3 = "Body Pressure"
s3 = tk.Label(root, text=s3, padx=0, font=f_BO10)
s3.grid(row=3, column=9, sticky="e", ipadx=10)
s3_1 = tk.Label(root, text="[cmH20]", padx=5, font=f_BO10)
s3_1.grid(row=3, column=11, sticky="w", ipadx=0)

staticBody = tk.StringVar()
stb = tk.Entry(root, textvariable=staticBody, width=wid, justify="center", font=f_10)
stb.grid(row=3, column=10)
stb.insert("end", 0)

#################Text Remark
text = tk.Text(root, state='normal', width=32, height=6, wrap='none')
text.insert("end", '   Insert here some remarks')
text.place(x=910, y=172)

########################################################### END input section ###

######################
###### Outputs Section
l03 = tk.Label(root, text="Output values", font=f_BO12)
l03.place(x=165, y=295)

r1 = "Dynamic pressure"
r1 = tk.Label(root, text=r1, padx=0, font=f_BO10)
r1.grid(row=8, column=0, sticky="e", ipadx=5)
r1_1 = tk.Label(root, text="[mmH20]", padx=5, font=f_BO10)
r1_1.grid(row=8, column=2, sticky="w")
frame1 = tk.Frame(width=widout, height=25, bg="white", colormap="new", relief=tk.SUNKEN, bd=1)
frame1.grid(row=8, column=1, sticky="we")

r2 = "Duct Velocity"
r2 = tk.Label(root, text=r2, padx=0, font=f_BO10)
r2.grid(row=9, column=0, sticky="e", ipadx=5)
r2_1 = tk.Label(root, text="[m/s]", padx=5, font=f_BO10)
r2_1.grid(row=9, column=2, sticky="w")
frame2 = tk.Frame(width=widout, height=25, bg="white", colormap="new", relief=tk.SUNKEN, bd=1)
frame2.grid(row=9, column=1, sticky="we")

r3 = "Flow rate"
r3 = tk.Label(root, text=r3, padx=0, font=f_BO10)
r3.grid(row=10, column=0, sticky="e", ipadx=5)
r3_1 = tk.Label(root, text="[m\u00b3/s]", padx=5, font=f_BO10)
r3_1.grid(row=10, column=2, sticky="w")
frame3 = tk.Frame(width=widout, height=25, bg="white", colormap="new", relief=tk.SUNKEN, bd=1)
frame3.grid(row=10, column=1, sticky="we")

r4 = "Density"
r4 = tk.Label(root, text=r4, padx=0, font=f_BO10)
r4.grid(row=11, column=0, sticky="e", ipadx=5)
r4_1 = tk.Label(root, text="[kg/m\u00b3]", padx=5, font=f_BO10)
r4_1.grid(row=11, column=2, sticky="w")
frame4 = tk.Frame(width=widout, height=25, bg="white", colormap="new", relief=tk.SUNKEN, bd=1)
frame4.grid(row=11, column=1, sticky="we")

r5 = "Fan Pressure"
r5 = tk.Label(root, text=r5, padx=0, font=f_BO10)
r5.place(x=352, y=330)
r5_1 = tk.Label(root, text="[cmH20]", padx=5, font=f_BO10)
r5_1.grid(row=8, column=5, sticky="w")
frame5 = tk.Frame(width=widout, height=25, bg="white", colormap="new", relief=tk.SUNKEN, bd=1)
frame5.grid(row=8, column=4, sticky="we")

r6 = "Body Pressure"
r6 = tk.Label(root, text=r6, padx=0, font=f_BO10)
r6.place(x=345, y=368)
r6_1 = tk.Label(root, text="[cmH20]", padx=5, font=f_BO10)
r6_1.grid(row=9, column=5, sticky="w")
frame6 = tk.Frame(width=widout, height=25, bg="white", colormap="new", relief=tk.SUNKEN, bd=1)
frame6.grid(row=9, column=4, sticky="we")

r7 = "Developed Power"
r7 = tk.Label(root, text=r7, padx=0, font=f_BO10)
r7.place(x=322, y=408)
r7_1 = tk.Label(root, text="[kW]", padx=5, font=f_BO10)
r7_1.grid(row=10, column=5, sticky="w")
frame7 = tk.Frame(width=widout, height=25, bg="white", colormap="new", relief=tk.SUNKEN, bd=1)
frame7.grid(row=10, column=4, sticky="we")

r8 = "Consumed Power"
r8 = tk.Label(root, text=r8, padx=0, font=f_BO10)
r8.place(x=322, y=448)
r8_1 = tk.Label(root, text="[kW]", padx=5, font=f_BO10)
r8_1.grid(row=11, column=5, sticky="w")
frame8 = tk.Frame(width=widout, height=25, bg="white", colormap="new", relief=tk.SUNKEN, bd=1)
frame8.grid(row=11, column=4, sticky="we")

###################
#####   Buttons
photo_cal = ImageTk.PhotoImage(file="imgs/calculate.png")
b0 = tk.Button(root,image=photo_cal, text="Calculate", command=calculon, font=f_BO10)
b0.config(height=140, width=151)
b0["bg"] = "grey77"
b0["border"] = "0"
b0.place(x=675, y=320)

photo_canc1 = ImageTk.PhotoImage(file="imgs/clean1.png")
#cltx1 = "Clean"+"\nPass#1"
cl1 = tk.Button(root, image=photo_canc1, command=ClEaN_1, font=f_BO10)
cl1.config(height=140, width=136)
cl1["bg"] = "grey77"
cl1["border"] = "0"
cl1.place(x=831, y=320)

photo_canc2 = ImageTk.PhotoImage(file="imgs/clean2.png")
#cltx2 = "Clean"+"\nPass#2"
cl1 = tk.Button(root, image=photo_canc2, command=ClEaN_2, font=f_BO10)
cl1.config(height=140, width=136)
cl1["bg"] = "grey77"
cl1["border"] = "0"
cl1.place(x=973, y=320)

photo_save = ImageTk.PhotoImage(file="imgs/save.png")
b1 = tk.Button(root, image=photo_save, command=lambda: saveEx(Par, staticP_,\
staticFan_, staticBody_, P_first, P_second, AVGH, Vduct, Qduct, devPow, conPow, remark),\
font=f_BO10)
b1.config(height=67, width=67)
b1["bg"] = "grey77"
b1["border"] = "0"
b1.place(x=1120, y=320)

photo_exit = ImageTk.PhotoImage(file="imgs/exit_.png")
ex = tk.Button(root, image=photo_exit, command=close, font=f_BO10)
ex.config(height=67, width=67)
ex["bg"] = "grey77"
ex["border"] = "0"
ex.place(x=1120, y=393)

#####################
### Logo
#photo = "imgs/buc_muni_co.png"
#render = ImageTk.PhotoImage(file = photo) #render img
#lb_im = tk.Label(root, image=render)
#lb_im.image = render #keep a reference
#lb_im.place(x=1080, y=433)

vv = "2.0"
vers = tk.Label(root, text="Ver.{}".format(vv), font=f_ver)
vers.place(x=1145, y=480)
vers.configure(bg="grey77")
root.mainloop() #looping the frame
