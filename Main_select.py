from AutoFarm.Threads.StealthFarm_select import *
from AutoFarm.Threads.StealthSafeFarm_select import *
import customtkinter as tk


def script_gui():
    # visual
    tk.set_appearance_mode('dark')
    tk.set_default_color_theme('dark-blue')
    # definindo variavel
    root = tk.CTk()
    # remove opcao "maximizar" do windows
    root.resizable(0,0)
    # titulo da janela 
    root.title('[Discord: dz6k]')
    # dimensao
    root.geometry('450x430')

    frame = tk.CTkFrame(master=root)
    frame.pack(pady=20,padx=60,fill='both',expand=True)
    
    # titulo dentro da aplicacao
    label = tk.CTkLabel(master=frame, text='Mir4 Auto Farm',font=('unispace',35),text_color='#293fa3')
    label.pack(pady=1,padx=5)
    # modos
    button_stealth_farm = tk.CTkButton(master=frame,text='Normal', command=start)
    button_stealth_farm.pack(padx=12,pady=10)
    
    button_stealth_farm_ultimate = tk.CTkButton(master=frame,text='Normal With Ult', command=start_ultimate)
    button_stealth_farm_ultimate.pack(padx=12,pady=10)
    button_stealth_farm_ultimate = tk.CTkButton(master=frame,text='❌Stop Normal Script❌',hover_color='red', command=stop_threads)
    button_stealth_farm_ultimate.pack(padx=5,pady=5)
    label = tk.CTkLabel(master=frame, text='----------------',font=('unispace',15),text_color='#37a987')
    label.pack(pady=1,padx=1)
    
    button_safe = tk.CTkButton(master=frame,text='Safe Protection', command=start_safe)
    button_safe.pack(padx=12,pady=10)
    
    button_safe = tk.CTkButton(master=frame,text='Safe Protection With Ult', command=start_safe_ultimate)
    button_safe.pack(padx=12,pady=10)
    button_safe = tk.CTkButton(master=frame,text='❌Stop Safe Script❌',
                               hover_color='red', command=stop_safe)
    button_safe.pack(padx=12,pady=10)
    
    # explicacao
    texto = tk.CTkLabel(master=frame, text='!!! Press "CTRL+E" for stop script !!!',font=('unispace',13),text_color='#abd11f')
    texto.pack(padx=2,pady=1)

    root.mainloop()

if __name__ == '__main__':
    script_gui()