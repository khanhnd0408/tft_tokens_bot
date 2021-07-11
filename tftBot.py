from lib import *

def getTFT_Window(unsyncScreenshotImage, syncGameWindow, syncStatus):
    topImg = cv2.imread("tft_window_top.png")
    botImg = cv2.imread("tft_window_bottom.png")
    bot_h, bot_w, _ = botImg.shape
    
    current = time()
    while syncStatus.value != 0:
        if time() - current < 2 or syncStatus.value == 2:
            continue
        image = tonumpyarray(unsyncScreenshotImage[:])
        top_minVal, top_minLoc = matching(image, topImg)
        if top_minVal < BASE_THRESHOLD:
            bot_minVal, bot_minLoc = matching(image, botImg)
            if bot_minVal < BASE_THRESHOLD:
                syncGameWindow[:] = [top_minLoc[0], top_minLoc[1], bot_minLoc[0] + bot_w, bot_minLoc[1] + bot_h]
            else:
                syncGameWindow[:] = [top_minLoc[0], top_minLoc[1], win32api.GetSystemMetrics(0), win32api.GetSystemMetrics(1)]
        current = time()

def stage_WaitRoom(unsyncScreenshotImage, syncGameWindow, syncStatus, isDebug=False):
    findGameButton = cv2.imread("tim_tran_2.png")
    buttonH, buttonW, _ = findGameButton.shape
    current = time()
    while syncStatus.value != 0:
        if time() - current < BASE_WAIT_TIME:
            continue
        gameWindowRect = syncGameWindow[:]
        image = tonumpyarray(unsyncScreenshotImage[:], crop=gameWindowRect)
        minVal, minLoc = matching(image, findGameButton)
        if isDebug:
            debug(image, minVal, minLoc, keyTime=0)
        if minVal < BASE_THRESHOLD:
            xPos = minLoc[0] + buttonW//2 + gameWindowRect[0]
            yPos = minLoc[1] + buttonH//2 + gameWindowRect[1]
            direct_mouse_event("left", (xPos, yPos))
            direct_mouse_event("move", (300,500))
        current = time()

def stage_AcceptGame(unsyncScreenshotImage, syncGameWindow, syncStatus, isDebug=False):
    joinGameButton = cv2.imread("choi_luon_2.png")
    buttonH, buttonW, _ = joinGameButton.shape
    current = time()
    while syncStatus.value != 0:
        if time() - current < BASE_WAIT_TIME:
            continue
        gameWindowRect = syncGameWindow[:]
        image = tonumpyarray(unsyncScreenshotImage[:], crop=gameWindowRect)
        minVal, minLoc = matching(image, joinGameButton)
        if isDebug:
            debug(image, minVal, minLoc, keyTime=0)
        if minVal < BASE_THRESHOLD:
            xPos = minLoc[0] + buttonW//2 + gameWindowRect[0]
            yPos = minLoc[1] + buttonH//2 + gameWindowRect[1]
            direct_mouse_event("left", (xPos, yPos))
            direct_mouse_event("move", (300,500))
            syncStatus.value = 2
        current = time()

def stage_OutGame(unsyncScreenshotImage, syncStatus, isDebug=False):
    ffBackground = cv2.imread("ff_ready.png")
    acceptOutGame = cv2.imread("ff_accept.png")
    buttonH, buttonW, _ = acceptOutGame.shape
    current = time()
    while syncStatus.value != 0:
        if time() - current < BASE_WAIT_TIME:
            continue
        image = tonumpyarray(unsyncScreenshotImage[:])
        minVal, _ = matching(image, ffBackground)
        if isDebug:
            debug(image, minVal, minLoc, keyTime=0)
        if minVal < BASE_THRESHOLD:
            direct_key_event('enter')
            direct_key_event("/")
            direct_key_event("f")
            direct_key_event("f")
            direct_key_event('enter')
            sleep(2)
            image = tonumpyarray(unsyncScreenshotImage[:])
            minVal, minLoc = matching(image, acceptOutGame)
            if isDebug:
                debug(image, minVal, minLoc, keyTime=0)
            if minVal < BASE_THRESHOLD:
                xPos = minLoc[0] + buttonW//2 + SCREEN_RESOLUTION[0]
                yPos = minLoc[1] + buttonH//2 + SCREEN_RESOLUTION[1]
                direct_mouse_event("holdLeft", (xPos, yPos))
                direct_mouse_event("releaseLeft", (xPos, yPos))
                direct_mouse_event("move", (300,500))
        current = time()

def stage_Replay(unsyncScreenshotImage, syncGameWindow, syncStatus, isDebug=False):
    replayGameButton = cv2.imread("choi_lai_2.png")
    buttonH, buttonW, _ = replayGameButton.shape
    current = time()
    while syncStatus.value != 0:
        if time() - current < BASE_WAIT_TIME:
            continue
        gameWindowRect = syncGameWindow[:]
        image = tonumpyarray(unsyncScreenshotImage[:], crop=gameWindowRect)
        minVal, minLoc = matching(image, replayGameButton)
        if isDebug:
            debug(image, minVal, minLoc, keyTime=0)
        if minVal < BASE_THRESHOLD:
            xPos = minLoc[0] + buttonW//2 + gameWindowRect[0]
            yPos = minLoc[1] + buttonH//2 + gameWindowRect[1]
            direct_mouse_event("left", (xPos, yPos))
            direct_mouse_event("move", (300,500))
            syncStatus.value = 1
        current = time()