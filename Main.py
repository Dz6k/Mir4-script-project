import customtkinter
from ctkdlib.custom_widgets import *
import pywinstyles
import keyboard, ctypes,win32gui, win32con
from time import sleep
from hPyT import *
from pywinauto import Application
from AutoFarm.Threads.StealthFarm import *
from plyer import notification
from win10toast import ToastNotifier
import platform
import webbrowser
import requests
import os   
import threading
import re

customtkinter.set_appearance_mode("System")
customtkinter.set_default_color_theme("blue")



class App(customtkinter.CTk):

    CURRENT_VERSION = 'v4.0.101024'
    HEIGHT = 400
    WIDTH = 270
    VERSAO = requests.get(
        'https://raw.githubusercontent.com/Dz6k/Mir4-script-project/main/version.txt').text
    WINDOWS_VERSION = float('.'.join(platform.version().split('.')[:2]))
    PATH = os.path.join(os.path.dirname(os.path.realpath(__file__)), "assets")
    
    def __init__(self):
        super().__init__()
        self.title("Auto Farm")
        self.geometry(f"{App.WIDTH}x{App.HEIGHT}")
        self.resizable(False, False)
        self.wm_iconbitmap(r"assets\IconGroup1.ico")
        self.attributes('-topmost', True)
        self.menuon = True
        self.menu()
        self.hide_window()
        self.worker = {}
        self.manual_worker = {}
        self.instancias_lista = []

        all_stuffs.hide(self)
        rainbow_border.start(self)
        self.Gif1 = CTkGif(self, width=500, height=500, fg_color="transparent",
                           path=r"assets\background.gif")
        self.Gif1.place(x=0, y=0)
        
        # manual selection widgets
        self.button_manual_selection = customtkinter.CTkButton(self,bg_color='#000001', text="Manual Selection",
                                                               command=self.gui_manual)
        self.button_manual_selection.place(x=64, y=25)
        pywinstyles.set_opacity(self.button_manual_selection, color='#000001')

        self.button_stop_script_manual_selection = customtkinter.CTkButton(self,bg_color='#000001', text="Stop Script",
                                                                           state="disabled", hover_color="#ff0000", command=self.force_stop_manual)
        self.button_stop_script_manual_selection.place(x=64, y=65)
        pywinstyles.set_opacity(self.button_stop_script_manual_selection, color='#000001')
        
        # automatic initialize widget
        self.button_automatic_initialize = customtkinter.CTkButton(self,bg_color='#000001', text="Automatic Initialize", command=lambda: threading.Thread(target=self.start_automatic).start())
        self.button_automatic_initialize.place(x=64, y=150)
        pywinstyles.set_opacity(self.button_automatic_initialize, color='#000001')

        self.button_stop_script_automatic_selection = customtkinter.CTkButton(self,bg_color='#000001', 
                                                                              text="Stop Script", state="disabled",
                                                                              hover_color="#f5010a", command=self.force_stop_auto)
        self.button_stop_script_automatic_selection.place(x=64, y=190)
        pywinstyles.set_opacity(self.button_stop_script_automatic_selection, color='#000001')
        
        # ultimate widget
        self.switch_ultimate = customtkinter.CTkSwitch(self,bg_color='#000001',font=customtkinter.CTkFont(slant='italic', size=15), state="disabled", text="Ultimate", command=self.ultimate)
        self.switch_ultimate.place(x=82, y=239)
        pywinstyles.set_opacity(self.switch_ultimate, color='#000001')
        
        self.off = customtkinter.CTkButton(self,bg_color='#000001', text="Stop and Close", hover_color="#f5010a",
                                           command=lambda:  self.force_stop_and_kill())
        self.off.place(x=64, y=360)
        pywinstyles.set_opacity(self.off, color='#000001')
        self.update_script()
        
    def ultimate_setter(self, instancias, identificador):
        if identificador in instancias:
            instancias[identificador].ultimate = True

    def ultimate_setter_off(self, instancias, identificador):
        if identificador in instancias:
            instancias[identificador].ultimate = False
            
    def call_ultimate_setter_off(self):
        for i in self.instancias_lista: 
            self.ultimate_setter_off(self.manual_worker, int(i))  
        for i in self.worker:
            self.ultimate_setter_off(self.worker, int(i)) 
             
    def call_ultimate_setter(self):
        for i in self.instancias_lista: 
            self.ultimate_setter(self.manual_worker, int(i))  
        for i in self.worker:
            self.ultimate_setter(self.worker, int(i))  
            
    def ultimate(self):
        if self.switch_ultimate.get() == 1:
            try:
                for i in self.worker:
                    self.call_ultimate_setter()
            except: ...
            try:
                for i in self.manual_worker:
                    self.call_ultimate_setter()
            except: ...
        else:
            try:
                for i in self.worker:
                    self.call_ultimate_setter_off()
            except: ...
            try:
                for i in self.manual_worker:
                    self.call_ultimate_setter_off()
            except: ...
        
    def update_script(self):
        if App.CURRENT_VERSION != App.VERSAO:
            self.geometry(f"{App.WIDTH}x{App.HEIGHT+100}")
            texto = customtkinter.CTkLabel(self,bg_color="#000001", text=f'New Update: {App.VERSAO}', text_color='#abd11f')
            texto.place(x=64, y=400)
            pywinstyles.set_opacity(texto, color="#000001")
            texto_minha_versao = customtkinter.CTkLabel(self,bg_color="#000001", text=f'Your Version: {App.CURRENT_VERSION}', text_color='#abd11f')
            texto_minha_versao.place(x=64, y=425)
            pywinstyles.set_opacity(texto_minha_versao, color="#000001")
            download_button = customtkinter.CTkButton(self, text='Download Last Version', fg_color='green', command=self.download_bot)
            download_button.place(x=64, y=450)
            pywinstyles.set_opacity(download_button, color="#000001")
    
    def start_automatic(self):
        self.switch_ultimate.configure(state='normal')
        self.button_stop_script_automatic_selection.configure(state='normal')
        for indice in range(0, 30):
            try:
                app = Application().connect(title=f'Mir4G[{indice}]')
                app_text = app.window().texts()

                worker = Stealthfarm()
                worker.game = app_text
                self.worker[indice] = worker
                
                farm = threading.Thread(
                    target=worker.run)
                farm.start()
            except Exception as e:
                continue
        if App.WINDOWS_VERSION < 10.0:
            notification.notify(
                title="Auto Farm Notification",
                message=f"Script started on mir4 instances: {len(self.worker)}"
            )   
        elif App.WINDOWS_VERSION >= 10.0:
            toaster = ToastNotifier()
            toaster.show_toast(
                title="Auto Farm Notification",
                msg=f"Script started on mir4 instances: {len(self.worker)}"
            )
        return self.worker
    
    def force_stop_auto(self):
        self.switch_ultimate.configure(state='disabled')
        self.button_stop_script_automatic_selection.configure(state='disabled')
        for i in self.worker: 
            self.stop_script_per_mir4_index_manual(self.worker, int(i))
                    
    def force_stop_manual(self):
        self.switch_ultimate.configure(state='disabled')
        self.option_menu.destroy()
        self.botao_fechar_instancia_individual.destroy()
        for i in self.manual_worker: 
            self.stop_script_per_mir4_index_manual(self.manual_worker, int(i))
        self.instancias_lista.clear()
        self.button_stop_script_manual_selection.configure(state='disabled')
        
    def force_stop_and_kill(self):
        try:
            self.force_stop_auto()
        except: ...
        try:
            self.force_stop_manual()
        except: ...
        
        self.destroy()
            
    def hide_window(self):
        hwnd = win32gui.FindWindow(None, 'Auto Farm')
        
        if hwnd:
            style = win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE)
            win32gui.SetWindowLong(hwnd, win32con.GWL_EXSTYLE, style | win32con.WS_EX_TOOLWINDOW & ~win32con.WS_EX_APPWINDOW)
            
            win32gui.ShowWindow(hwnd, win32con.SW_HIDE)   
                
    def gui_manual(self):
        root_x = self.winfo_x()
        root_y = self.winfo_y()
        root_width = self.winfo_width()
        nova_janela_x = root_x + root_width 
        nova_janela_y = root_y 
        self.nova_janela = customtkinter.CTkToplevel(self)
        self.nova_janela.attributes('-topmost', True)
        self.nova_janela.geometry(f"400x300+{nova_janela_x}+{nova_janela_y}")
        self.nova_janela.title("Ultimate Manual")

        # mir4 windows instance
        self.label_instancias = customtkinter.CTkLabel(self.nova_janela, text="Number of Window:")
        self.label_instancias.pack(pady=10)
        self.entry_instancias = customtkinter.CTkEntry(self.nova_janela, width=200)
        self.entry_instancias.pack(pady=10)

        # delay to swap target 
        self.label_time = customtkinter.CTkLabel(self.nova_janela, text="Escolha o tempo (segundos) para troca de alvo:")
        self.label_time.pack(pady=10)
        self.entry_time = customtkinter.CTkEntry(self.nova_janela, width=200)
        self.entry_time.pack(pady=10)

        # start callback function script 
        self.button_start = customtkinter.CTkButton(self.nova_janela, text="Iniciar", command=self.call_manual)
        self.button_start.pack(pady=20)
        
    def stop_script_per_mir4_index_manual(self, instancias, identificador):
        if identificador in instancias:
            instancias[identificador].stop = True
            
    def parar_instancia_lista(self):
        valor = self.option_menu.get()
        if valor in self.instancias_lista: 
            self.instancias_lista.remove(valor)  
            if len(self.instancias_lista) == 0:
                self.option_menu.destroy()
                self.button_stop_script_manual_selection.configure(state='disabled')
                self.botao_fechar_instancia_individual.destroy()
                self.instancias_lista.clear()
                
            else:
                self.option_menu.configure(values=self.instancias_lista)  
                self.option_menu.set(self.instancias_lista[0])
            self.stop_script_per_mir4_index_manual(self.manual_worker, int(valor))
          
    def call_manual(self):
        instancias = self.entry_instancias.get()
        escolher_time = self.entry_time.get()
        novas_instancias = [(x) for x in re.split('[, ]+', instancias.strip()) if x]

        if novas_instancias:
            if hasattr(self, 'option_menu'):
                self.option_menu.destroy()

            self.instancias_lista.extend(novas_instancias)

            self.option_menu = customtkinter.CTkOptionMenu(self, width=100,values=self.instancias_lista)
            self.option_menu.place(x=30, y=300)
            
            self.botao_fechar_instancia_individual = customtkinter.CTkButton(self, text='Parar instancia', width=100,command=self.parar_instancia_lista)
            self.botao_fechar_instancia_individual.place(x=140, y=300)

            self.button_automatic_initialize.configure(state='disabled')   
            self.button_stop_script_manual_selection.configure(state='normal')
            self.switch_ultimate.configure(state='normal')

            threading.Thread(target=self.start_manual, args=(instancias, escolher_time,)).start()
            
    def start_manual(self, instancias, escolher_time):
        try:
            self.nova_janela.destroy()
            if instancias:
                self.instancias = [int(x) for x in re.split('[, ]+', instancias.strip()) if x]

            if len(escolher_time) > 0:
                self.possibilities = int(escolher_time)
            else:
                self.possibilities = [round(random.uniform(1, 3), 3) for _ in range(10)]

            if self.instancias:
                for indice in self.instancias:
                    try:
                        app = Application().connect(title=f'Mir4G[{indice}]') 
                        app_text = app.window().texts() 
                        worker_MANUAL = Stealthfarm()
                        worker_MANUAL.game = app_text
                        self.manual_worker[indice] = worker_MANUAL
                        
                        farm = threading.Thread(
                            target=worker_MANUAL.run)
                        farm.start()
                        
                    except:
                        ...
                        
                instancias_formatadas = ', '.join(map(str, self.instancias))
                
                if App.WINDOWS_VERSION < 10.0:
                    notification.notify(
                        title="Auto Farm Notification",
                        message=f"Script started on mir4 instances: {instancias_formatadas}"
                    )   
                elif App.WINDOWS_VERSION >= 10.0:
                    toaster = ToastNotifier()
                    toaster.show_toast(
                        title="Auto Farm Notification",
                        msg=f"Script started on mir4 instances: {instancias_formatadas}"
                    )

            return self.manual_worker
        except: ...
        
    def download_bot(self):
        webbrowser.open('https://github.com/Dz6k/Mir4-script-project/releases')      
             
    def menu(self):
        if keyboard.is_pressed('insert'):
            if self.menuon:
                self.menuon = False
                self.withdraw() 
            else:
                self.menuon = True
                self.deiconify()
                ctypes.windll.user32.ClipCursor(None)
                self.focus_force()  

            sleep(0.1) 
        self.after(40, self.menu)
        
        
if __name__ == "__main__":
    app = App()
    
    app.mainloop()
