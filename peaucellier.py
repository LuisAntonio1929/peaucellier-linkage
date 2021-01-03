# -*- coding: utf-8 -*-
"""
Created on Tue Dec 15 16:43:01 2020

@author: USUARIO
"""

import math
from tkinter import Label,Button,DoubleVar,Tk,Entry,Scale,HORIZONTAL,Checkbutton,IntVar,Radiobutton
from tkinter import messagebox
import numpy as np
import matplotlib.animation as animation
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from matplotlib import colors
from matplotlib import pyplot as plt

def cos(x):
    return math.cos(x)
def sen(x):
    return math.sin(x)
def norm(a):
    return (a[0]**2+a[1]**2)**0.5

    
class Root(Tk):
    def __init__(self):
        super(Root,self).__init__()
        self.title('PEAUCELLIER LINKAGE')
        self.geometry('1280x720')
        self.resizable(0,0)
        self.columnconfigure(1, weight=1)
        self.rowconfigure(2, weight=1)
        self.measure_state = False
        self.protocol("WM_DELETE_WINDOW",self.salirfichero)
        self.a_value = DoubleVar()
        self.a_value.set(2)
        self.b_value = DoubleVar()
        self.b_value.set(5)
        self.c_value = DoubleVar()
        self.c_value.set(2)
        self.a0_value = DoubleVar()
        self.a0_value.set(0)
        self.b0_value = DoubleVar()
        self.b0_value.set(22.3316)
        self.c0_value = DoubleVar()
        self.c0_value.set(0)
        self.r_value = DoubleVar()
        self.r_xtr = [1.01,5]
        self.r_value.set(2)
        self.scale_factor = DoubleVar()
        self.scale_factor.set(1)
        self.j = 0
        self.xs=[]
        self.ys=[]
        self.alpha = []
        self.beta = []
        self.theta =[]
        self.time = []
        self.ratio = 60
        self.theta_max = DoubleVar() 
        self.theta_max.set(round(math.degrees(1.4455),4))
        self.x_max = DoubleVar()
        self.x_max.set(5.25)
        self.y_max = DoubleVar()
        self.y_max.set(4.6301)
        self.t_max = 1.4455
        self.widgets()
        
    def points_pos(self):
        a = self.a_value.get()
        b = self.b_value.get()
        c = self.c_value.get()
        r = self.r_value.get()
        t0 = self.c0_value.get()
        t_max = math.acos((b**2+c**2-r**2-a**2-2*b*c)/(2*r*a))
        ymax = (b+c)*(a*sen(t_max))/(b-c)
        xmax = ((b+c)**2-ymax**2)**0.5
        self.x_max.set(round(xmax,4))
        self.y_max.set(round(ymax,4))
        self.t_max = t_max
        if abs(t0)>t_max:
            sgn = t0/abs(t0)
            t0 = t_max*sgn*1
        A = [0,0]
        B = [r,0]
        C = [r + a*cos(t0),a*sen(t0)]
        AC = norm(C)
        alpha = math.atan(C[1]/C[0])
        beta = math.acos((b**2+AC**2-c**2)/(2*b*AC))  
        D = [b*cos(alpha+beta),b*sen(alpha+beta)]
        E = [b*cos(alpha-beta),b*sen(alpha-beta)]
        AF = (b**2-c**2)/AC
        F = [AF*cos(alpha),AF*sen(alpha)]
        
        r_min = max([a-b+c,b-c-a,c-b-a,a-b-c])
        r_max = b+c-a
        self.r_xtr=[r_min+0.01,r_max-0.01]
        self.points = np.around(np.array([A,B,C,D,E,F]),4)
        self.a0_value.set(round(math.degrees(alpha),4))
        self.b0_value.set(round(math.degrees(beta),4))
        self.c0_value.set(round(math.degrees(t0),4))
        self.theta_max.set(round(math.degrees(t_max),4))
        self.alpha.append(alpha)
        self.beta.append(beta)
        self.theta.append(t0)
        self.alpha = self.alpha[-self.ratio:]
        self.beta = self.beta[-self.ratio:]
        self.theta = self.theta[-self.ratio:]
        
    def salirfichero(self):
        valor=messagebox.askquestion('Salir','¿Desea cerrar la aplicacion?')
        if valor=='yes':        
            self.destroy()  

    def animate(self, i):   
        self.i = i
        try:
            a = self.a_value.get()
            b = self.b_value.get()
            c = self.c_value.get()
        except:
            a = 0
            b = 0
            c = 0
        
        p1 = np.linspace(-self.t_max,self.t_max,num=50)
        p_inv = np.flipud(p1)
        p2 = p_inv[1:-1]
        angle_list = np.concatenate((p1,p2), axis=0)
        if self.measure_state and a != 0 and b != 0 and c != 0:
            cont = self.i%98
            if self.selected.get() == 2:
                angle = math.sin(self.i/20)*(self.t_max)*0.9
            elif self.selected.get() == 3:
                if cont == 0:
                    self.j = self.j+1
                angle = angle_list[cont*(-1)**self.j]
            else:
                angle = math.sin(self.i/20)*(self.t_max)*0.9
            
            
            self.c0_value.set(angle)
            state = False
            try:
                self.points_pos()
                state=True
            except:
                state=False
            if state:
                
                self.r_scale.config(from_=self.r_xtr[0],to=self.r_xtr[1])
                self.ax.clear()
                self.ax2.clear()
                
                n = 1.1
                y = self.y_max.get()*n
                x = self.x_max.get()*n
                if 1.2*x < 2*y:
                    self.ax.set_ylim(-y,y)
                    self.ax.set_xlim(-y*0.2,y*1.8)
                else:
                    self.ax.set_ylim(-0.6*x,0.6*x)
                    self.ax.set_xlim(-x*0.2,x)
                    
                point = np.transpose(self.points)
                x_data = point[0,:]
                y_data = point[1,:]
                self.ax.plot(x_data,y_data,'o')
                
                text = ['A','B','C','D','E','F']
                for i in range(len(text)):
                    self.ax.text(x_data[i]+0.3,y_data[i]+0.3,text[i])
                
                angle_plot = ['α','β','θ']
                alpha = self.alpha[-1]
                alpha_array = np.linspace(0,alpha,num=20)
                beta = self.beta[-1]
                beta_array = np.linspace(alpha,alpha+beta,num=20)
                theta = self.theta[-1]
                theta_array = np.linspace(0,theta,num=20)
                AD = norm([x_data[3],y_data[3]])
                BC = norm([x_data[2]-x_data[1],y_data[2]-y_data[1]])
                self.ax.text(AD*0.3*math.cos(alpha*0.5),AD*0.3*math.sin(alpha*0.5),angle_plot[0])
                self.ax.plot(AD*0.3*np.cos(alpha_array),AD*0.3*np.sin(alpha_array),'b')
                self.ax.text(AD*0.5*math.cos(alpha+beta*0.5),AD*0.5*math.sin(alpha+beta*0.5),angle_plot[1])
                self.ax.plot(AD*0.5*np.cos(beta_array),AD*0.5*np.sin(beta_array),'r')
                self.ax.text(BC*0.5*math.cos(theta*0.5)+x_data[1]*1.1,BC*0.5*math.sin(theta*0.5),angle_plot[2])
                self.ax.plot(BC*0.5*np.cos(theta_array)+x_data[1],BC*0.5*np.sin(theta_array),'g')
                    
                data_lines = [[0,1,'k'],[0,3,'r'],[0,4,'r'],[1,2,'b'],[2,3,'g'],[2,4,'g'],[3,5,'g'],[4,5,'g'],[0,5,'--']]
                for i,j,k in data_lines:
                    self.ax.plot([x_data[i],x_data[j]],[y_data[i],y_data[j]],k)
                

                self.time.append(self.i/20)
                self.xs.append(x_data[5])
                self.ys.append(y_data[5])
                self.xs = self.xs[-self.ratio:]
                self.ys = self.ys[-self.ratio:]
                self.time = self.time[-self.ratio:]
                xs2 = np.array(self.xs)
                ys2 = np.array(self.ys)
                time = np.array(self.time)
                xs = np.array(self.xs[-15:])
                ys = np.array(self.ys[-15:])
                self.ax.plot(xs,ys,'c.',alpha=0.5)
                alpha = np.array(self.alpha)
                beta = np.array(self.beta)
                theta = np.array(self.theta)
                try:
                    scale = self.scale_factor.get()
                except: 
                    scale = 1
                if scale == 0:
                    scale = 1
                if len(self.xs)>3:
                    w_a = np.gradient(alpha)
                    a_a = np.gradient(w_a)
                    w_b = np.gradient(beta)
                    a_b = np.gradient(w_b)
                    w_t = np.gradient(theta)
                    a_t = np.gradient(w_t)
                    dx = np.gradient(xs2)
                    dy = np.gradient(ys2)
                    d2x = np.gradient(dx)
                    d2y = np.gradient(dy)
                    vF = norm([dx,dy])
                    aF = norm([d2x,d2y])
                    v = [xs[-1]-xs[-2],ys[-1]-ys[-2]]
                    self.ax.quiver(xs[-1],ys[-1],v[0],v[1],angles='xy', scale_units='xy', scale=0.08,color='blue')
                    a = [xs[-1]+xs[-3]-xs[-2]*2,ys[-1]+ys[-3]-ys[-2]*2]
                    self.ax.quiver(xs[-1],ys[-1],a[0],a[1],angles='xy', scale_units='xy', scale=0.008,color='red')
                    coef = list(map(lambda x:x.get(),self.var_data))
                    values = [alpha,beta,theta,w_a,a_a,w_b,a_b,w_t,a_t,vF,aF]
                    cn = colors.Normalize(0, 11)
                    for i in range(11):
                        if coef[i]==1:
                            if  self.selected.get() == 1:
                                lim = self.t_max
                                self.ax2.set_ylim(-lim*0.5/scale,lim*0.5/scale)
                                self.ax2.set_xlim(-lim,lim)
                                self.ax2.plot(self.theta,values[i],color=plt.cm.jet(cn(i)))
                            elif self.selected.get() == 2 or self.selected.get() == 3:
                                lim = self.t_max
                                self.ax2.set_ylim(-self.t_max/scale,self.t_max/scale)
                                self.ax2.set_xlim(time.min(),time.max())
                                self.ax2.plot(time,values[i]*scale,color=plt.cm.jet(cn(i)))
                    
                self.ax.grid(True)
                self.ax2.grid(True)
                self.i=self.i+1    
    
    
    def state(self):
        if (self.measure_button['text']=='START'):
            self.measure_button['text']='STOP'
            self.measure_state = True
        else:
            self.measure_button['text']='START'
            self.measure_state = False

        
    def widgets(self):
        
        title = Label(self, text ='PEAUCELLIER LINKAGE ANALISYS')
        title.place(x=300,y=10)
        title.config(justify='center',font=("Courier", 30)) 

        data_label = Label(self,text='Input data: ',font=("Times", 15, "italic"))
        data_label.place(x=75,y=75)
        a_label = Label(self,text='a: ',font=("Times", 15, "italic"))
        a_label.place(x=75,y=115)
        a_entry = Entry(self,textvariable=self.a_value)    
        a_entry.place(x=100,y=120)  
        a_color = Label(self,bg = 'blue',width=2)
        a_color.place(x=230,y=120)
        b_label = Label(self,text='b: ',font=("Times", 15, "italic"))
        b_label.place(x=75,y=145)
        b_entry = Entry(self,textvariable=self.b_value)    
        b_entry.place(x=100,y=150)  
        b_color = Label(self,bg = 'red',width=2)
        b_color.place(x=230,y=150)
        c_label = Label(self,text='c: ',font=("Times", 15, "italic"))
        c_label.place(x=75,y=175)
        c_entry = Entry(self,textvariable=self.c_value)    
        c_entry.place(x=100,y=180)  
        c_color = Label(self,bg = 'green',width=2)
        c_color.place(x=230,y=180)
        
        r_label = Label(self,text='r: ',font=("Times", 15, "italic"))
        r_label.place(x=270,y=135)
        self.r_scale = Scale(self,variable =self.r_value, from_=self.r_xtr[0], to=self.r_xtr[1], orient=HORIZONTAL,length = 200,resolution = 0.01)
        self.r_scale.place(x=315,y=125)
        
        data_label = Label(self,text='Output data: ',font=("Times", 15, "italic"))
        data_label.place(x=775,y=75)
        a0_label = Label(self,text='α: ',font=("Times", 15, "italic"))
        a0_label.place(x=775,y=115) 
        a1_label = Label(self,textvariable=self.a0_value,font=("Times", 15, "italic"))
        a1_label.place(x=800,y=115)
        b0_label = Label(self,text='β: ',font=("Times", 15, "italic"))
        b0_label.place(x=775,y=145) 
        b1_label = Label(self,textvariable=self.b0_value,font=("Times", 15, "italic"))
        b1_label.place(x=800,y=145)
        c0_label = Label(self,text='θ: ',font=("Times", 15, "italic"))
        c0_label.place(x=775,y=175)
        b1_label = Label(self,textvariable=self.c0_value,font=("Times", 15, "italic"))
        b1_label.place(x=800,y=175)
        m0_label = Label(self,text='θ_max: ',font=("Times", 15, "italic"))
        m0_label.place(x=975,y=115)
        m1_label = Label(self,textvariable=self.theta_max,font=("Times", 15, "italic"))
        m1_label.place(x=1050,y=115)
        y0_label = Label(self,text='y_max: ',font=("Times", 15, "italic"))
        y0_label.place(x=975,y=145)
        y1_label = Label(self,textvariable=self.y_max,font=("Times", 15, "italic"))
        y1_label.place(x=1050,y=145)
        x0_label = Label(self,text='x_max: ',font=("Times", 15, "italic"))
        x0_label.place(x=975,y=175)
        x1_label = Label(self,textvariable=self.x_max,font=("Times", 15, "italic"))
        x1_label.place(x=1050,y=175)
        scale_label = Label(self,text='scale factor:',font=("Times", 15, "italic"))
        scale_label.place(x=800,y=220)
        scale_entry =  Entry(self,textvariable=self.scale_factor)
        scale_entry.place(x=920,y=225)

        self.measure_button = Button(self, text='START',command = self.state)
        self.measure_button.place(x=50,y=250)                
        
        self.var_data = []
        self.var_text = ['α','β','θ','w_α','α_α','w_β','α_β','w_θ','α_θ','v','a']
        for i in range(len(self.var_text)):
            self.var_data.append(IntVar())
            Checkbutton(self, text=self.var_text[i], variable=self.var_data[-1]).place(x=570,y=80+i*20)
        
        self.selected = IntVar()
        Radiobutton(self,text='θ', value=1, variable=self.selected).place(x=650,y=80)
        Radiobutton(self,text='t ∿', value=2, variable=self.selected).place(x=650,y=100)
        Radiobutton(self,text='t ʌ', value=3, variable=self.selected).place(x=650,y=120)
        
        self.fig = Figure(figsize=(14, 4), dpi=100)
        self.canvas = FigureCanvasTkAgg(self.fig, master=self) 
        self.canvas.get_tk_widget().place(x=-100,y=300)
        gs = self.fig.add_gridspec(1, 3)
        self.ax = self.fig.add_subplot(gs[0,0])
        self.ax2 = self.fig.add_subplot(gs[0,1:])
        self.measure_state = True
        self.animate(0)
        self.measure_state = False      

root = Root()
ani = animation.FuncAnimation(root.fig, root.animate, interval=50)
root.mainloop()
