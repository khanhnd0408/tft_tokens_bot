import cv2
import win32api, win32con
from time import sleep, time
import numpy as np
import pydirectinput

method = cv2.TM_SQDIFF_NORMED
mouseLeftDo = [win32con.MOUSEEVENTF_LEFTDOWN, win32con.MOUSEEVENTF_LEFTUP]
mouseRightDo =  [win32con.MOUSEEVENTF_RIGHTDOWN, win32con.MOUSEEVENTF_RIGHTUP]
BASE_THRESHOLD = 0.01
BASE_WAIT_TIME = 5
SCREEN_RESOLUTION = [0,0, win32api.GetSystemMetrics(0), win32api.GetSystemMetrics(1)]

def click(pos, targetEvent):
    try:
        win32api.SetCursorPos((pos[0],pos[1]))
        win32api.mouse_event(targetEvent[0],pos[0],pos[1],0,0)
        win32api.mouse_event(targetEvent[1],pos[0],pos[1],0,0)
        moveMouse((1,1))
    except Exception as E:
        print("Click error: ", E)
        print(pos)

def moveMouse(pos):
    try:
        win32api.SetCursorPos((pos[0],pos[1]))
    except Exception as E:
        print("Mouse error: ", E)

def direct_mouse_event(event, pos):
    posX, posY = pos
    if event == "left":
        pydirectinput.click(posX, posY)
    elif event == "right":
        pydirectinput.click(posX, posY, button=pydirectinput.RIGHT)
    elif event == "move":
        pydirectinput.moveTo(posX, posY)
    elif event == "doubleLeft":
        pydirectinput.doubleClick(posX, posY)
    elif event == "doubleRight":
        pydirectinput.doubleClick(posX, posY, button=pydirectinput.RIGHT)
    elif event == "holdLeft":
        pydirectinput.mouseDown(posX, posY)
    elif event == "releaseLeft":
        pydirectinput.mouseUp(posX, posY)
    elif event == "holdRight":
        pydirectinput.mouseDown(posX, posY, button=pydirectinput.RIGHT)
    elif event == "releaseRight":
        pydirectinput.mouseUp(posX, posY, button=pydirectinput.RIGHT)
    
def direct_key_event(key):
    pydirectinput.press(key)

def takeScreenShot_v2(ROI):
    img = d.screenshot(ROI)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    return img

def takeScreenShot(ROI):
    x,y,xx,yy = ROI
    convertROI = (x,y,xx-x,yy-y)
    img = pyautogui.screenshot(region=convertROI)
    img = np.asarray(img)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    return img

try:
    import d3dshot
    d = d3dshot.create(capture_output="numpy")
    SCREEN_CAPTURE = takeScreenShot_v2
except:
    import pyautogui
    SCREEN_CAPTURE = takeScreenShot

def sync_TakeScreenShot(unsyncScreenshotImage, syncSignal):
    current = time()
    while syncSignal.value != 0:
        if time() - current < BASE_WAIT_TIME//2:
            continue
        unsyncScreenshotImage[:] = SCREEN_CAPTURE(SCREEN_RESOLUTION).flatten()
        current = time()

def matching(reference, cropped):
    result = cv2.matchTemplate(cropped, reference, method)
    mn,_,mnLoc,_ = cv2.minMaxLoc(result)
    return mn, mnLoc

def debug(img, conf, loc, keyTime=0):
    cv2.imshow("img", img)
    print("conf:", conf)
    print("loc:", loc)
    cv2.waitKey(keyTime)

def getKeyboardEvent(syncSignal, key=0x51):
    trangThaiBanDau = win32api.GetKeyState(key)
    while syncSignal.value != 0:
        trangThai = win32api.GetKeyState(key)
        if trangThaiBanDau != trangThai and trangThai >= 0:
            trangThaiBanDau = trangThai
            syncSignal.value = 0

def tonumpyarray(flatten_array, crop=None):
    rawScreenshot = np.reshape(np.asarray(flatten_array, dtype=np.uint8), 
                               (SCREEN_RESOLUTION[3], SCREEN_RESOLUTION[2], 3))
    if crop is None:
        return rawScreenshot
    else:
        x,y,xx,yy = crop
        return rawScreenshot[y:yy, x:xx]