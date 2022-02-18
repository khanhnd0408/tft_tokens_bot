import cv2
import pyautogui
import numpy as np
import d3dshot
d = d3dshot.create(capture_output="numpy")
import pydirectinput

def take_screenshot_v2(ROI):
    img = d.screenshot(ROI)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    return img

def take_screenshot(ROI):
    img = pyautogui.screenshot(region=ROI)
    img = np.asarray(img)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    return img

if __name__ == "__main__":
    bboxes = [
        (790,760,160,30),
        (855,635,220,80),
        (0,0,1920,1080),
        (710,520,240,70),
        (780,760,175,40)
    ]
    from time import sleep
    sleep(5)
    img = take_screenshot((0,0,1920,1080))
    # cv2.imshow("IMG", img)
    # key = cv2.waitKey(0)
    # if key == "s":
    cv2.imwrite("1.jpg", img)    
    # cv2.destroyAllWindows()

    pydirectinput.press('enter')
    pydirectinput.press("/")
    pydirectinput.press("f")
    pydirectinput.press("f")
    pydirectinput.press('enter')
