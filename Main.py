import customtkinter as ctk
import requests
import sys
import pyautogui
from AutoFarm.Threads.StealthFarm import *
from AutoFarm.Threads.StealthSafeFarm import *
from AutoFarm.farm import *
from tkinter import *
import webbrowser

# interface
def script_gui():
    # visual
    ctk.set_appearance_mode('dark')
    ctk.set_default_color_theme('dark-blue')
    # definindo variavel
    root = ctk.CTk()
    # remove opcao "maximizar" do windows
    root.resizable(0,0)
    # titulo da janela 
    root.title('[Discord: dz6k]')
    # dimensao
    root.geometry('310x635')
    # aumentar escala dos widgets
    # ctk.set_widget_scaling(1.1)

    def youtube():
        webbrowser.open('https://youtu.be/I0722Mpk-fM')
    
    frame = ctk.CTkFrame(root)
    frame.pack(pady=10, padx=20, fill='both', expand=True)
    
    # titulo dentro da aplicacao
    label = ctk.CTkLabel(frame,
                        text='Mir4 Auto Farm',
                        font=('unispace',35),
                        text_color='#293fa3').pack(pady=1,padx=5)

    
    # texto tutorial
    label = ctk.CTkLabel(frame,
                        text='Please! See the tutorial!',
                        font=('unispace',15),
                        text_color='#37a987').pack(pady=1,padx=5)

    
    # botao tutorial
    button_tutorial = ctk.CTkButton(frame,
                                   text='Tutorial',
                                   command=youtube).pack(padx=9,pady=1)

    
    # texto selecao de modos
    label = ctk.CTkLabel(frame,
                        text='Stealth Modes',
                        font=('unispace',18),
                        text_color='#37a987').pack(pady=6,padx=5)

    # modos
    button_stealth_farm = ctk.CTkButton(frame,
                                       text='Normal',
                                       command=start).pack(padx=12,pady=10)

    
    button_stealth_farm_ultimate = ctk.CTkButton(frame,
                                                text='Normal With Ult',
                                                command=start_ultimate).pack(padx=12,pady=10)

    button_stealth_farm_ultimate = ctk.CTkButton(frame,
                                                text='❌Stop Normal Script❌',
                                                hover_color='red',
                                                command=stop_threads).pack(padx=5,pady=5)
    label = ctk.CTkLabel(frame,
                        text='----------------',
                        font=('unispace',15),
                        text_color='#37a987').pack(pady=1,padx=1)

    
    button_safe = ctk.CTkButton(frame,
                               text='Safe Protection',
                               command=start_safe).pack(padx=12,pady=10)

    button_safe = ctk.CTkButton(frame,
                               text='Safe Protection With Ult',
                               command=start_safe_ultimate).pack(padx=12,pady=10)

    button_safe = ctk.CTkButton(frame,
                               text='❌Stop Safe Script❌',
                               hover_color='red',
                               command=stop_safe).pack(padx=12,pady=10)
    
    # selecao modo simples
    label = ctk.CTkLabel(frame,
                        text='Simple Modes(one UI)',
                        font=('unispace',18),
                        text_color='#37a987').pack(pady=6,padx=5)

    
    # modos simples
    button_normal_farm = ctk.CTkButton(frame,
                                      text='Simple',
                                      command=start_simple).pack(padx=12,pady=10)

    button_normal_farm = ctk.CTkButton(frame,
                                      text='Simple With Ultmate',
                                      command=start_simple_ultimate).pack(padx=12,pady=10)
    
    # explicacao
    texto = ctk.CTkLabel(frame,
                        text='!!! Press "CTRL+E" for stop script !!!',
                        font=('unispace',13),
                        text_color='#abd11f')
    texto.pack(padx=2,pady=1)

    root.mainloop()


if __name__ == '__main__':
    with open('version.txt', 'r') as arquivo:

        VERSION = arquivo.readline()
        url_update = requests.get(
            'https://raw.githubusercontent.com/Dz6k/Mir4-script-project/main/version.txt')

        if VERSION != url_update.text:
            pyautogui.alert(
                title='Alert', text=f'Your version: {VERSION}\nNew version: {url_update.text}\nDownload before start script')

            sys.exit(0)
        script_gui()
