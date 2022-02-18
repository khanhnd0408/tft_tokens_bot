import cv2
import win32api
from time import sleep, time
import numpy as np
import pydirectinput

method = cv2.TM_SQDIFF_NORMED
BASE_THRESHOLD = 0.01
BASE_WAIT_TIME = 5
SCREEN_RESOLUTION = [0,0, win32api.GetSystemMetrics(0), win32api.GetSystemMetrics(1)]

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

def take_screenshot_v2(ROI):
    img = d.screenshot(ROI)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    return img

def take_screenshot(ROI):
    x,y,xx,yy = ROI
    convertROI = (x,y,xx-x,yy-y)
    img = pyautogui.screenshot(region=convertROI)
    img = np.asarray(img)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    return img

try:
    import d3dshot
    d = d3dshot.create(capture_output="numpy")
    SCREEN_CAPTURE = take_screenshot_v2
except:
    import pyautogui
    SCREEN_CAPTURE = take_screenshot

def sync_take_screenshot(unsync_screenshot_image, sync_signal):
    current = time()
    while sync_signal.value != 0:
        if time() - current < BASE_WAIT_TIME//2:
            continue
        unsync_screenshot_image[:] = SCREEN_CAPTURE(SCREEN_RESOLUTION).flatten()
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

def get_keyboard_event(sync_signal, key=0x51):
    start_state = win32api.GetKeyState(key)
    while sync_signal.value != 0:
        current_state = win32api.GetKeyState(key)
        if start_state != current_state and current_state >= 0:
            start_state = current_state
            sync_signal.value = 0

def to_numpy_array(flatten_array, crop=None):
    raw_screenshot = np.reshape(np.asarray(flatten_array, dtype=np.uint8), 
                               (SCREEN_RESOLUTION[3], SCREEN_RESOLUTION[2], 3))
    if crop is None:
        return raw_screenshot
    else:
        x, y , xx, yy = crop
        return raw_screenshot[y:yy, x:xx]