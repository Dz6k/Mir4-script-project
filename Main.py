from AutoFarm.Threads.StealthFarm import start,start_ultimate
from AutoFarm.Threads.StealthSafeFarm import start_safe, start__safe_ultimate
from AutoFarm.farm import start_simple, start_simple_ultimate
import customtkinter as tk
import webbrowser

def script_gui():
    # aviso
    tk.set_appearance_mode('dark')
    tk.set_default_color_theme('dark-blue')
    root = tk.CTk()
    root.resizable(0,0)
    root.title('[Discord: dz6k]')
    root.geometry('500x650')
    tk.set_widget_scaling(1.1)
    def youtube():
        webbrowser.open('')
    

    frame = tk.CTkFrame(master=root)
    frame.pack(pady=20,padx=60,fill='both',expand=True)
    label = tk.CTkLabel(master=frame, text='Mir4 Auto Farm',font=('unispace',35),text_color='#293fa3')
    label.pack(pady=12,padx=10)
    label = tk.CTkLabel(master=frame, text='Please! See the tutorial!',font=('unispace',15),text_color='#37a987')
    label.pack(pady=6,padx=5)
    
    button_tutorial = tk.CTkButton(master=frame,text='Tutorial', command=youtube)
    button_tutorial.pack(padx=9,pady=7)
    
    label = tk.CTkLabel(master=frame, text='Stealth Modes',font=('unispace',18),text_color='#37a987')
    label.pack(pady=6,padx=5)
    
    button_stealth_farm = tk.CTkButton(master=frame,text='Normal', command=start)
    button_stealth_farm.pack(padx=12,pady=10)
    
    button_stealth_farm_ultimate = tk.CTkButton(master=frame,text='Normal With Ult', command=start_ultimate)
    button_stealth_farm_ultimate.pack(padx=12,pady=10)
    
    button_safe = tk.CTkButton(master=frame,text='Safe Protection', command=start_safe)
    button_safe.pack(padx=12,pady=10)
    
    button_safe = tk.CTkButton(master=frame,text='Safe Protection With Ult', command=start__safe_ultimate)
    button_safe.pack(padx=12,pady=10)
    
    label = tk.CTkLabel(master=frame, text='Simple Modes(one UI)',font=('unispace',18),text_color='#37a987')
    label.pack(pady=6,padx=5)
    
    button_normal_farm = tk.CTkButton(master=frame,text='Simple', command=start_simple)
    button_normal_farm.pack(padx=12,pady=10)
    button_normal_farm = tk.CTkButton(master=frame,text='Simple With Ultmate', command=start_simple_ultimate)
    button_normal_farm.pack(padx=12,pady=10)
    
    texto = tk.CTkLabel(master=frame, text='!!! Press "CTRL+E" for stop script !!!',font=('unispace',13),text_color='#abd11f')
    texto.pack(padx=11,pady=9)

    root.mainloop()
    
if __name__ == '__main__':
    script_gui()