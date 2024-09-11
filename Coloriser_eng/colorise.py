# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import math
import numpy as np
import matplotlib.pyplot as plt
from skimage.color import lch2lab, lab2rgb
import tkinter as tk
from tkinter import filedialog
from PIL import Image, UnidentifiedImageError
from ewnds import ErrorWindow1, ErrorWindow2, ErrorWindow3, ErrorWindow4,ErrorWindow5,ErrorWindow6

picture=np.zeros((1,1))
bw_picture=np.zeros((1,1))
new_picture=np.zeros((1,1))
points=[]
width=0
height=0



class ColorPoints():
    
    def __init__(self, H_dif):
        self.points=[]
        self.L_max=87
        self.L_min=0
        self.C_max=90
        self.L_start=43.5
        self.H_max=360
        self.H_dif=H_dif
        self.min_dist=0

    
    
    def make_mindist(self):
        radH_dif=math.radians(float(self.H_dif))
        self.min_dist=2*self.C_max*math.sin(radH_dif/2)
    
    def make_Hs(self,C):
        pr_H=math.degrees(2*math.asin(self.min_dist/(2*C)))
        Hs=list(np.arange(0,self.H_max,pr_H))
        if Hs[-1]+self.H_dif>360:
            del Hs[-1]
        return Hs
        
    def make_Ls(self):
        Ls=[self.L_start]
        L_quant=self.L_max//self.min_dist
        tech_list=list(range(int(math.ceil(L_quant/2))+1))
        del tech_list[0]
        for i in tech_list:
            Ls.extend([self.L_start+self.min_dist*i, self.L_start-self.min_dist*i])
        Ls=filter(lambda x: self.L_min<=x<=self.L_max, Ls)
        return Ls
        
    def make_Cs(self,L):
        pr_C = math.sqrt((self.C_max**2)*(1 - (L-self.L_start)** 2 / (self.L_start ** 2)))
        Cs=list(np.arange(pr_C,self.min_dist/2,-self.min_dist))
        Cs=filter(lambda x: x>=self.min_dist/2, Cs)
        return Cs
        
    def make_points(self):
        self.make_mindist()
        Ls=self.make_Ls()
        global points
        points=np.array([[i,j,math.radians(k)] for i in Ls for j in self.make_Cs(i) for k in self.make_Hs(j)])
        points=np.round(lab2rgb(lch2lab(points))*255).astype('uint8').tolist()
        points=tuple(map(tuple,points))
        
       
        
        
class Picture():
    
    def __init__(self, address):
        self.__pict = Image.open(address)  # Приватный атрибут для имени

    @property
    def pict(self):
        return self.__pict



class CheckColors():
    
    def __init__(self,angle_dif):
        try:
            self.angle_dif = math.radians(float(angle_dif))
        except:
            we6.make_win()
        
        
    def show_check(self):
        if self.angle_dif>0:
            fc1_LCH=np.array((50,100,0),dtype=np.float64)
            fc2_LCH=np.array((50,100,self.angle_dif),dtype=np.float64)
            fc1=lab2rgb(lch2lab(fc1_LCH)).tolist()
            fc2=lab2rgb(lch2lab(fc2_LCH)).tolist()
            fig, ax = plt.subplots()
            square1 = plt.Rectangle((0, 0), 0.45, 1, color=fc1)
            ax.add_patch(square1)
            square2 = plt.Rectangle((0.55, 0), 0.45, 1, color=fc2)
            ax.add_patch(square2)
            ax.set_xlim(0, 1)
            ax.set_ylim(0, 1)
            ax.axis('off')
            plt.show()
        else:
            we5.make_win()



class NewPicture():
    
    def __init__(self, bw_picture, new_picture, points):
        self.bw_picture=bw_picture
        self.new_picture=new_picture
        self.points=points
        
    
    
    def transform(self,value):
        return points[value]
    
        
    def colorise(self):
        global new_picture
        new_picture= bw_picture.convert('RGB')
        for i in range(width):
            for j in range(height):
                pixel_value = bw_picture.getpixel((i,j))
                new_picture.putpixel((i, j), points[pixel_value])



def forwardwin1(value):
    txtfrtextfield = value
    if txtfrtextfield:
        try:
            
            with open(txtfrtextfield):
               global picture
               picture=Picture(address=txtfrtextfield)
               global width
               global height
               width,height = picture.pict.size
               global new_picture
               new_picture=np.zeros((height, width), 'uint8')
               global bw_picture
               bw_picture = picture.pict.convert('L')
                
               w2.make_win()
               
        except FileNotFoundError:
            we2.make_win()
            
        except UnidentifiedImageError:
            we3.make_win()
            
    else:
        we4.make_win()
    

def forwardwin2(value):
    if value>0:
        try:
            global points
            points=ColorPoints(value)
            points.make_points()
            global new_picture
            new_picture=NewPicture(bw_picture, new_picture, points)
            new_picture.colorise()
            plt.imshow(new_picture)
            plt.axis('off')
            plt.show()
            w3.make_win()
        except (IndexError,ValueError):
            we1.make_win()
    else:
        we5.make_win()
        

def checkwin2(value):
        checkcolors=CheckColors(value)
        checkcolors.show_check()

def forwardwin3(value):
    new_picture.save(value)



class BackButton:
    def __init__(self, master, prwin):
        self.prwin = prwin
        self.button = tk.Button(master, text='Back', command=self.back)
        

    def back(self):
        self.prwin.make_win()
        self.withdraw()
        
    def pack (self,side,anchor,padx,pady):
        self.button.pack(side=side,anchor=anchor,padx=padx,pady=pady)
        


        

class Window(tk.Tk):
    
    def __init__(self,pastwin):
        super().__init__()
        self.textfield = tk.Entry(self)
        self.txtfrtextfield = ''
        self.button2 = BackButton(self,pastwin)
        self.button3 = tk.Button(self, text="Next", command=self.forward)
        self.button3.pack(side='right',anchor='s',padx=10,pady=10)
        self.withdraw()
        

    def make_win(self):
        self.title("Coloriser0.8")
        self.resizable(False, False)
        self.deiconify()
        self.mainloop()
        
    
    def forward(self):
        pass
    

class Window1(Window):
    def __init__(self,pastwin):
        super().__init__(None)
        self.geometry("500x130")
        self.textfield.config(width=40)
        self.label = tk.Label(self,text='Enter a file path')
        self.button1 = tk.Button(self, text="Browse", command=self.open_file_browser)
        self.button2 = tk.Button(self, text="Close", command=self.close)
        self.button3 = tk.Button(self, text="Next", command=self.forward)
        self.button1.pack(side="right")
        self.button2.pack(side='left',anchor='s',padx=10,pady=10)
        self.label.pack(side="top",anchor='s')
        self.textfield.pack(side='top',pady=35)
        
                


    def forward(self):
        forwardwin1(self.textfield.get())
        self.withdraw()



    def open_file_browser(self):
        file_path = tk.filedialog.askopenfilename(title="Choose the file")
        self.textfield.delete(0, tk.END)  # Очищаем текстовое поле
        self.textfield.insert(0, file_path)  # Вставляем путь к выбранному файлу
        
    
    
    #Функция закрытия окна    
    def close(self):
        self.destroy()
        w2.destroy()
        w3.destroy()
        we1.destroy()
        we2.destroy()
        we3.destroy()
        we4.destroy()
    

            
    

class Window2(Window):
    
    def __init__(self,pastwin):
        super().__init__(w1)
        self.geometry("700x200")
        self.textfield.config(width=10)
        self.label = tk.Label(self,text='Enter in the text field the difference \nbetween two angles, calculated in this application \nas the difference in angles H between the corresponding colors. After entering, \nclick the "Check" button. If you are at a loss, \nyou can experiment with different values.',justify='left')
        self.button1 = tk.Button(self, text="Check",command=self.check)
        self.button3 = tk.Button(self, text="Next", command=self.forward)
        self.label.pack(side='top')
        self.button1.pack(side='top',pady=10)
        self.textfield.pack(side='top')
        self.button2.pack(side='left', anchor="s",padx=10,pady=10)
        
        
    
    def forward(self):
        try:
            forwardwin2(float(self.textfield.get()))
        except ValueError:
            we6.make_win()
        self.withdraw()
        
        
    def check(self):
        checkwin2(self.textfield.get())
        
            
            

class Window3(Window):
    def __init__(self,pastwin):
        super().__init__(w2)
        self.geometry("500x130")
        self.textfield.config(width=40)
        self.label = tk.Label(self,text='Enter the address to save the file')
        self.button1 = tk.Button(self, text="Browse", command=self.open_file_browser)
        self.button3 = tk.Button(self, text="Next", command=self.forward)
        self.button1.pack(side="right")
        self.button2.pack(side='left',anchor='s',padx=10,pady=10)
        self.label.pack(side="top",anchor='s')
        self.textfield.pack(side='top',pady=35)
        

        
    

    def open_file_browser(self):
        file_path = tk.filedialog.asksaveasfilename(defaultextension=".jpg", filetypes=[("JPEG", "*.jpg"), ("All Files", "*.*")])
        self.textfield.delete(0, tk.END) 
        self.textfield.insert(0, file_path) 
        self.make_win()
        
        
    def forward(self):
        forwardwin3(self.textfield.get())
        self.withdraw()




class ErrorWindow(tk.Tk):
    def __init__(self,text):
        super().__init__()
        self.label = tk.Label(self, text=text)
        self.withdraw()
        self.button = tk.Button(self, text="OK", command=self.close_window, width=6)
        
    def close_window(self):
        self.withdraw()

    def make_win(self):
        self.title("Coloriser0.8")
        self.geometry("500x100")
        self.label.pack()
        self.button.pack()
        self.deiconify()
        self.mainloop()
        

       
            
w1=Window1(None)
w2=Window2(w1)
w3=Window3(w2)
we1=ErrorWindow1()
we2=ErrorWindow2()
we3=ErrorWindow3()
we4=ErrorWindow4()
we5=ErrorWindow5()
we6=ErrorWindow6()
w1.make_win()


