# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import math
import numpy as np
import tkinter as tk
from tkinter import filedialog
import matplotlib.pyplot as plt
from skimage.color import lch2lab, lab2rgb
from PIL import Image

picture=np.zeros((1,1))
bw_picture=np.zeros((1,1))
new_picture=np.zeros((1,1))
points=[]

#Объект окна ввода пути до изображения
class Window1(tk.Tk):
    def __init__(self):
        super().__init__()
        #Создаем все объекты для графического интерфейса
        self.text = 'Введите путь до файла и нажмите "Enter"'
        self.selected_file_entry = tk.Entry(self)
        self.selected_file_out = ''
        self.text_label = tk.Label(text=self.text)
        self.button1 = tk.Button(self, text="Обзор...", command=self.open_file_browser)
        self.button2 = tk.Button(self, text="Закрыть", command=self.back)
        self.button3 = tk.Button(self, text="Сохранить путь", command=self.forward)
        self.withdraw()
        

    def make_win(self):
        #Размещаем созданные в __init__ объекты для графического интерфейса
        self.title("Coloriser0.8")

        # Устанавливаем размер окна в пикселях (ширина x высота)
        self.geometry("400x150")
        
        # Запрет изменения размеров окна
        self.resizable(False, False)

        self.text_label.grid(row=0, column=0, padx=10, pady=10)

        self.selected_file_entry.config(width=40)
        self.selected_file_entry.grid(row=1, column=0, padx=10, pady=10,sticky="w")

        self.button1.grid(row=1, column=1, padx=10, pady=10, sticky="e")
        self.button2.grid(row=2, column=0, padx=10, pady=10, sticky="w")
        self.button3.grid(row=2, column=1, padx=10, pady=10)
        
        self.deiconify()
        
        self.mainloop()
        


    def open_file_browser(self):
        file_path = tk.filedialog.askopenfilename(title="Выберите файл")
        self.selected_file_entry.delete(0, tk.END)  # Очищаем текстовое поле
        self.selected_file_entry.insert(0, file_path)  # Вставляем путь к выбранному файлу

    # Функция, "далее"
    def forward(self):
        
        self.selected_file_out = self.selected_file_entry.get()
        if self.selected_file_out and self.selected_file_out.endswith(('.jpg','.png')):
            try:
                with open(self.selected_file_out):
                   global picture
                   picture=Picture(address=self.selected_file_out)
                   width,height = picture.pict.size
                   global new_picture
                   new_picture=np.zeros((height, width), 'uint8')
                   global bw_picture
                   bw_picture = picture.pict.convert('L')
                    
                   w2.make_win()
                   w1.withsraw()
                   
            except FileNotFoundError:
                we2.make_win()
                self.withdraw()
        else:
            we3.make_win()
            self.withdraw()
        



    #Функция закрытия окна    
    def back(self):
        self.destroy()
        w2.destroy()
        w3.destroy()
        we.destroy()
        we2.destroy()
    

            
    

#Окно ввода разницы H 
class Window2(tk.Tk):
    
    def __init__(self):
        super().__init__()
        #Создаем все объекты для графического интерфейса
        self.text = 'Введите в текстовое поле справа разницу между двумя углами, вычисляемую в этом приложении в виде разницы углов H между соотвующими цветами. После ввода нажмите кнопку "Проверить". Если затрудняетесь, можете поэкспериментировать с разными значениями.'
        #Создаем фреймы
        self.frame1 = tk.Frame(self, width=200, height=200)
        self.frame2 = tk.Frame(self, width=100, height=100)
        self.frame3 = tk.Frame(self, width=200, height=200)
        self.frame4 = tk.Frame(self, width=200, height=200)
        #Создаем кнопки и прочее
        self.button1 = tk.Button(self.frame2, text="Проверить",command=self.check)
        self.button2 = tk.Button(self.frame3, text="Назад", command=self.back)
        self.button3 = tk.Button(self.frame4, text="Сохранить значение", command=self.forward)
        
        self.text_label = tk.Label(self.frame1, text=self.text, wraplength=200,justify="left")

        
        self.text_entry = tk.Entry(self.frame2)
        
        self.withdraw()
            
        
    def make_win(self):
        #Размещаем созданные в __init__ объекты для графического интерфейса
        # Создаем основное окно
        self.title("Coloriser0.8")
        
        # Устанавливаем размер окна в пикселях (ширина x высота)
        self.geometry("350x200")
        
        # Запрет изменения размеров окна
        self.resizable(False, False)

        # Размещаем фреймы в окне
        self.frame1.grid(row=0, column=0)
        self.frame2.grid(row=0, column=1)
        self.frame3.grid(row=1, column=0)
        self.frame4.grid(row=1, column=1)

        # Добавляем текст в первый фрейм
        self.text_label.pack()

        # Размещаем текстовое поле во втором фрейме
        self.text_entry.pack()
        
        #Размещаем кнопки
        self.button1.pack(side=tk.BOTTOM)
        self.button2.pack(side=tk.LEFT, pady=10)
        self.button3.pack(side=tk.LEFT, pady=10)
        
        self.deiconify()

        # Запускаем главный цикл приложения
        self.mainloop()
        
    
    def forward(self):
        self.user_input = float(self.text_entry.get())
        global points
        points=ColorPoints(self.user_input)
        points.make_points()
        global new_picture
        new_picture=NewPicture(bw_picture, new_picture, points)
        new_picture.colorise()
        plt.imshow(new_picture)
        plt.axis('off')
        plt.show()
        w3.make_win()
        self.withdraw()
        
        
    def check(self):
        angle_dif = float(self.text_entry.get())
        angle_dif_rad=math.radians(angle_dif)
        fc1_LCH=np.array((50,100,0),dtype=np.float64)
        fc2_LCH=np.array((50,100,angle_dif_rad),dtype=np.float64)
        fc1_lab=lch2lab(fc1_LCH)
        fc1=lab2rgb(fc1_lab)
        fc2_lab=lch2lab(fc2_LCH)
        fc2=lab2rgb(fc2_lab)
        fc1=fc1.tolist()
        fc2=fc2.tolist()
        
        # Создаем фигуру и оси
        fig, ax = plt.subplots()
        # Создаем первый квадрат
        square1 = plt.Rectangle((0, 0), 0.45, 1, color=fc1)
        ax.add_patch(square1)
        # Создаем второй квадрат
        square2 = plt.Rectangle((0.55, 0), 0.45, 1, color=fc2)
        ax.add_patch(square2)

        # Устанавливаем пределы осей
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)

        # Убираем оси
        ax.axis('off')

        # Показать график
        plt.show()
        
        
    #Функция закрытия окна    
    def back(self):
        w1.make_win()
        self.withdraw()
            
            

class Window3(tk.Tk):
    def __init__(self):
        super().__init__()
        self.button1 = tk.Button(self, text="Отмена", command=self.back)
        self.button2 = tk.Button(self, text="Сохранить изображение", command=self.forward)
        self.withdraw()
        
        
    def make_win(self):
        self.title("Coloriser0.8")

        # Устанавливаем размер окна в пикселях (ширина x высота)
        self.geometry("250x70")
        
        # Запрет изменения размеров окна
        self.resizable(False, False)

        self.button1.grid(row=2, column=0, padx=10, pady=10, sticky="w")

        self.button2.grid(row=2, column=1, padx=10, pady=10, sticky="w")
        
        self.deiconify()

        self.mainloop()
        
    

    # Функция открытия окна диалога
    def forward(self):
        self.pathtosave = tk.filedialog.asksaveasfilename(defaultextension=".jpg", filetypes=[("JPEG", "*.jpg"), ("All Files", "*.*")])
        new_picture.save(self.pathtosave)
        self.withdraw()

    #Функция закрытия окна    
    def back(self):
        w2.make_win()
        self.withdraw()
    

#Окно ошибки
class ErrorWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.text = '''ВНИМАНИЕ!!! Для некоторых градаций яркости не хватает набора цветовых 
        оттенков. Для более точного результата уменьшите значение H'''
        self.withdraw()
        
    def close_window(self):
        self.destroy()
        self.withdraw()

    def make_win(self):
        self.title("Coloriser0.8")

        text_label = tk.Label(self, text=self.text)
        text_label.pack(padx=10, pady=10)

        button = tk.Button(self, text="OK", command=self.close_window, width=6)
        button.pack(padx=10, pady=10)
        
        self.deiconify()

        self.mainloop()


class ErrorWindow2(tk.Tk):
    
    def __init__(self):
        super().__init__()
        self.text = 'Файла по указанному адресу не найдено. Попробуйте еще раз'
        self.withdraw()
            
    def close_window(self):
        self.destroy()
        self.withdraw()

    def make_win(self):
        self.title("Coloriser0.8")

        text_label = tk.Label(self, text=self.text)
        text_label.pack(padx=10, pady=10)

        button = tk.Button(self, text="OK", command=self.close_window, width=6)
        button.pack(padx=10, pady=10)
             
        self.deiconify()

        self.mainloop()
        



class ErrorWindow3(tk.Tk):
    
    def __init__(self):
        super().__init__()
        self.text = 'Неправильное расширение выбранного файла'
        self.withdraw()
            
    def close_window(self):
        self.destroy()
        self.withdraw()

    def make_win(self):
        self.title("Coloriser0.8")

        text_label = tk.Label(self, text=self.text)
        text_label.pack(padx=10, pady=10)

        button = tk.Button(self, text="OK", command=self.close_window, width=6)
        button.pack(padx=10, pady=10)
             
        self.deiconify()

        self.mainloop()



class ColorPoints():
    
    def __init__(self, H_dif):
        self.points=[]
        self.L_max=87
        self.L_min=0
        self.C_max=90
        self.L_start=43.5
        self.C_start=90
        self.H_start=0
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




class NewPicture():
    
    def __init__(self, bw_picture, new_picture, points):
        self.bw_picture=bw_picture
        self.new_picture=new_picture
        self.points=points
        
    
    
    def transform(self,value):
        return points[value]
    
        
    def colorise(self):
        global new_picture
        width,height = picture.pict.size
        new_picture= bw_picture.convert('RGB')
        for i in range(width):
            for j in range(height):
                pixel_value = bw_picture.getpixel((i,j))
                new_picture.putpixel((i, j), points[pixel_value])
       
            
w1=Window1()
w2=Window2()
w3=Window3()
we=ErrorWindow()
we2=ErrorWindow2()
we3=ErrorWindow3()
w1.make_win()


