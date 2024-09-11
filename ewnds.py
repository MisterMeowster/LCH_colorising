# -*- coding: utf-8 -*-
"""
Created on Fri Sep  6 22:52:21 2024

@author: Cotan
"""

import tkinter as tk



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
        self.label.pack(padx=10, pady=10)
        self.button.pack(padx=10, pady=10)
        self.deiconify()
        self.mainloop()
        

#Окно ошибки
class ErrorWindow1(ErrorWindow):
    
    def __init__(self):
        super().__init__(text='''Для некоторых градаций яркости не хватает набора цветовых 
        оттенков. Уменьшите значение H''')
        
        


class ErrorWindow2(ErrorWindow):
    
    def __init__(self):
        super().__init__(text = 'Файла по указанному адресу не найдено. Попробуйте еще раз')
        
        



class ErrorWindow3(ErrorWindow):
    
    def __init__(self):
        super().__init__(text = 'Неправильное расширение выбранного файла')
        
        
        
class ErrorWindow4(ErrorWindow):
    
    def __init__(self):
        super().__init__(text = 'Пустой адрес')
        
class ErrorWindow5(ErrorWindow):
    
    def __init__(self):
        super().__init__(text = 'Значение H должно быть больше 0')
        

class ErrorWindow6(ErrorWindow):
    
    def __init__(self):
        super().__init__(text = 'Неверное значение H')