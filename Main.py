import requests
import customtkinter as tk
import random
from AutoFarm.Threads.StealthFarm_select import *
from AutoFarm.Threads.StealthFarm import *
import threading
import webbrowser

CURRENT_VERSION = 'v3.0.170824'


def download_bot():
    webbrowser.open('https://github.com/Dz6k/Mir4-script-project/releases')

def script_gui():
    # visual
    tk.set_appearance_mode('dark')
    tk.set_default_color_theme('dark-blue')
    # definindo variavel
    root = tk.CTk()
    # remove opcao "maximizar" do windows
    root.resizable(0,0)
    # titulo da janela 
    dicionario = [
        '[ Discord: dz6k ]',
        'Obrigado por me escolher s2',
        'Totalmente gratis',
        'Auto Farm',
        'By ----> Dz6k',
        'Dz6k love you <3',
        'I need coffe',
        'Bom dia flor do dia',
        '@OnlyDz6k',
        'Ainw Nobru Apelaum'
    ]

    def alterar_titulo():
        while True:
            for i in dicionario:
                root.title(f'{i}')
                # root.title(f'{random.choice(dicionario)}')
                sleep(1.5)

    def pegadinha():
        desligar.destroy()
        threading.Thread(target=lambda: alterar_titulo(), daemon=True).start()

    root.title('[ Discord: dz6k ]')

    frame = tk.CTkFrame(master=root)
    frame.pack(pady=10, padx=10, fill='both', expand=True)
    
    # titulo dentro da aplicacao
    label = tk.CTkLabel(master=frame, text=f'Mir4 Auto Farm',
                        font=('unispace', 35), text_color='#293fa3')
    label.pack(pady=1, padx=5)
    # modos
    button_stealth_farm = tk.CTkButton(
        master=frame, text='Manual Selection', command=start_manual)
    button_stealth_farm.pack(padx=12, pady=5)

    button_stealth_farm_ultimate = tk.CTkButton(
        master=frame, text='Manual With Ultimate', command=start_ultimate_manual)
    button_stealth_farm_ultimate.pack(padx=12, pady=5)

    button_stop = tk.CTkButton(
        master=frame, text='❌ Stop Script ❌', hover_color='red', command=stop_threads_manual)
    button_stop.pack(padx=5, pady=5)

    # gambiarra, se funciona, nao tem pq alterar kkkkkkkk
    texto = tk.CTkLabel(master=frame, text=' ')
    texto.pack(padx=2, pady=1)
    
    # area do modo automatico
    button_automatic = tk.CTkButton(frame,
                                    text='Automatic Initialize',
                                    command=run_auto).pack(padx=12, pady=5)

    button_automatic_ultimate = tk.CTkButton(frame,
                                             text='Automatic With Ultimate',
                                             command=run_ultimate).pack(padx=12, pady=5)

    stop_automatic = tk.CTkButton(frame,
                                  text='❌ Stop Script ❌',
                                  hover_color='red',
                                  command=stop_threads_auto).pack(padx=5, pady=5)
    
    desligar = tk.CTkButton(
        master=frame, text='Don\'t click!', hover_color='red', command=pegadinha)
    desligar.pack(padx=5, pady=5)

    aviso = tk.CTkLabel(master=frame, text='-> Press "CTRL+E" for stop script <-',
                        font=('unispace', 13), text_color='#abd11f')
    aviso.pack(padx=2, pady=1)
    
    # explicacao
    if CURRENT_VERSION != VERSAO:
        root.geometry('340x500')
        aviso.destroy()
        linha = tk.CTkLabel(master=frame, text=' ', font=(
            'unispace', 13), text_color='#abd11f')
        linha.pack(padx=2, pady=0)
        texto = tk.CTkLabel(
            master=frame, text=f'New Update: {VERSAO}', text_color='#abd11f')
        texto.pack(padx=2, pady=1)
        texto = tk.CTkLabel(
            master=frame, text=f'Your Version: {CURRENT_VERSION}', text_color='#abd11f')
        texto.pack(padx=2, pady=1)
        download_button = tk.CTkButton(
            master=frame, text='Download Last Version', fg_color='green', command=download_bot)
        download_button.pack(padx=12, pady=10)

    root.mainloop()

if __name__ == '__main__':
    VERSAO = requests.get(
        'https://raw.githubusercontent.com/Dz6k/Mir4-script-project/main/version.txt').text
    script_gui()
