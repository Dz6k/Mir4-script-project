import pyautogui
contei = "sim"
contador = 0
while contei == "sim":
    try:
        death_x, death_y = pyautogui.locateCenterOnScreen('morto.png',confidence=0.5)
        pyautogui.click(death_x,death_y)
        contei = "nao"
    except:
        contador += 1
        print('\bta vivo ainda.', contador)