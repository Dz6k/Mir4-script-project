from AutoFarm.StealthFarm import start,start_ultimate
from AutoFarm.farm import start_simple
from time import sleep
import customtkinter as tk
import webbrowser

if __name__ == '__main__':
    tk.set_appearance_mode('dark')
    tk.set_default_color_theme('dark-blue')
    root = tk.CTk()
    root.title('Created By Dz6k <3')
    root.geometry('500x500')
    tk.set_widget_scaling(1.1)
    
    def youtube():
        webbrowser.open('https://www.youtube.com/watch?v=iM3kjbbKHQU')
    
    frame = tk.CTkFrame(master=root)
    frame.pack(pady=20,padx=60,fill='both',expand=True)
    
    label = tk.CTkLabel(master=frame, text='Mir4 Auto Farm',font=('cascadia',30),text_color='#4169E1')
    label.pack(pady=12,padx=10)
    label = tk.CTkLabel(master=frame, text='Please! See the tutorial!',font=('cascadia',20),text_color='#6699FF')
    label.pack(pady=6,padx=5)

    
    button_tutorial = tk.CTkButton(master=frame,text='Tutorial', command=youtube)
    button_tutorial.pack(padx=9,pady=7)
    
    label = tk.CTkLabel(master=frame, text='Select Mode!',font=('cascadia',20))
    label.pack(pady=6,padx=5)
    
    button_stealth_farm = tk.CTkButton(master=frame,text='Stealth Mode', command=start)
    button_stealth_farm.pack(padx=12,pady=10)
    
    button_stealth_farm_ultimate = tk.CTkButton(master=frame,text='Stealth Mode With Ultimate', command=start_ultimate)
    button_stealth_farm_ultimate.pack(padx=12,pady=10)
    
    button_normal_farm = tk.CTkButton(master=frame,text='Simple Mode', command=start_simple)
    button_normal_farm.pack(padx=12,pady=10)
    
    texto = tk.CTkLabel(master=frame, text='!!! Press "CTRL+E" for stop script !!!')
    texto.pack(padx=12,pady=10)
    
    texto2 = tk.CTkLabel(master=frame, text='Discord: dz6k',text_color='#008000',font=('cascadia', 25))
    texto2.pack(padx=12,pady=10)
    
    root.mainloop()
