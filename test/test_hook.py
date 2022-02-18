import pydirectinput
# import pywinauto

# app = pywinauto.application.Application().connect(title='League of Legends (TM) Client')
# Form1 = app.window(title='League of Legends (TM) Client')
# Form1.set_focus()

from time import sleep
sleep(2)

pydirectinput.press("enter")
pydirectinput.press("/")
pydirectinput.press("f")
pydirectinput.press("f")
pydirectinput.press("enter")

pydirectinput.mouseDown(896, 382)#, button=pydirectinput.RIGHT)
pydirectinput.mouseUp(896, 382)#, button=pydirectinput.RIGHT)


# Form1.TypeKeys("{PAUSE 2}")
# Form1.TypeKeys("{TAB 2}{PAUSE 2}{ENTER}")