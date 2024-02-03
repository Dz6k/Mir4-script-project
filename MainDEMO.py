from AutoFarm.FarmDEMO import farm
from time import sleep
import customtkinter as tk
import webbrowser

if __name__ == '__main__':
    tk.set_appearance_mode('dark')
    tk.set_default_color_theme('dark-blue')
    root = tk.CTk()
    root.title('Created By Dz6k <3 - DEMO VERSION')
    root.geometry('500x450')
    tk.set_widget_scaling(1.1)
    
    def youtube():
        webbrowser.open('https://www.youtube.com/watch?v=iM3kjbbKHQU')
    
    frame = tk.CTkFrame(master=root)
    frame.pack(pady=20,padx=60,fill='both',expand=True)
    
    label = tk.CTkLabel(master=frame, text='Mir4 Auto Farm',font=('cascadia',30))
    label.pack(pady=12,padx=10)
    label = tk.CTkLabel(master=frame, text='Please! See the tutorial!',font=('cascadia',20))
    label.pack(pady=6,padx=5)

    
    button_tutorial = tk.CTkButton(master=frame,text='Tutorial', command=youtube)
    button_tutorial.pack(padx=9,pady=7)
    
    label = tk.CTkLabel(master=frame, text='Select Mode!',font=('cascadia',20))
    label.pack(pady=6,padx=5)
    
    button_demo = tk.CTkButton(master=frame,text='Demo Mode', command=farm)
    button_demo.pack(padx=12,pady=10)
    
    
    texto = tk.CTkLabel(master=frame, text='DEMO VERSION :(')
    texto.pack(padx=12,pady=10)
    texto = tk.CTkLabel(master=frame, text='!!! Press "CTRL+E" for stop script !!!')
    texto.pack(padx=12,pady=10)

    texto = tk.CTkLabel(master=frame, text='buy the script Discord: dz6k',text_color='#008000',font=('cascadia', 20))
    texto.pack(padx=12,pady=10)
    
    root.mainloop()
