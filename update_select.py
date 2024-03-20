import tkinter as tk
from tkinter import ttk
from threading import Thread
import requests
from tkinter import messagebox


def executar_download():
    def auto_update(progress_bar):
        def download():
            url_update = requests.get(
                'https://raw.githubusercontent.com/Dz6k/Mir4-script-project/main/version_manual.txt')
            with open('version_manual.txt', 'r+') as arquivo:
                try:
                    response = requests.get(
                        'https://raw.githubusercontent.com/Dz6k/Mir4-script-project/main/dist/manual.exe', stream=True)
                    total_size = int(response.headers.get('content-length', 0))

                    current_size = 0
                    with open('manual.exe', 'wb') as f:
                        for chunk in response.iter_content(chunk_size=1024):
                            if chunk:
                                current_size += len(chunk)
                                progress = (current_size / total_size) * 100
                                progress_bar['value'] = progress
                                progress_bar.update()
                                f.write(chunk)

                    arquivo.write(url_update.text)

                    if progress_bar['value'] == 100:
                        messagebox.showinfo(
                            "Download Finished", "Download has been finalized")

                except Exception as e:
                    print('Error:', e)


        download_thread = Thread(target=download)
        download_thread.start()

    janela = tk.Tk()
    janela.title("Update")
    janela.resizable(False, False)

    def fechar_janela():
        janela.quit()
        janela.destroy()

    janela.protocol("WM_DELETE_WINDOW", fechar_janela)

    largura_janela = 300
    altura_janela = 150
    largura_tela = janela.winfo_screenwidth()
    altura_tela = janela.winfo_screenheight()
    posicao_x = (largura_tela - largura_janela) // 2
    posicao_y = (altura_tela - altura_janela) // 2

    janela.geometry(
        f"{largura_janela}x{altura_janela}+{posicao_x}+{posicao_y}")

    frame = tk.Frame(janela)
    frame.pack(expand=True)

    progresso = ttk.Progressbar(
        frame, orient="horizontal", length=200, mode="determinate")
    progresso.pack(pady=10)

    btn_iniciar = tk.Button(frame, text="Start Download",
                            command=lambda: auto_update(progresso))
    btn_iniciar.pack(pady=10)

    janela.mainloop()


if __name__ == "__main__":
    executar_download()
