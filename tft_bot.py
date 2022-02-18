from lib import *

def get_tft_window(unsync_screenshot_image, sync_game_window, sync_status):
    top_img = cv2.imread("resources/tft_window_top.png")
    bot_img = cv2.imread("resources/tft_window_bottom.png")
    bot_h, bot_w, _ = bot_img.shape
    
    current = time()
    while sync_status.value != 0:
        if time() - current < 2 or sync_status.value == 2:
            continue
        image = to_numpy_array(unsync_screenshot_image[:])
        top_min_val, top_min_loc = matching(image, top_img)
        if top_min_val < BASE_THRESHOLD:
            bot_min_val, bot_min_loc = matching(image, bot_img)
            if bot_min_val < BASE_THRESHOLD:
                sync_game_window[:] = [top_min_loc[0], top_min_loc[1], bot_min_loc[0] + bot_w, bot_min_loc[1] + bot_h]
            else:
                sync_game_window[:] = [top_min_loc[0], top_min_loc[1], win32api.GetSystemMetrics(0), win32api.GetSystemMetrics(1)]
        current = time()

def stage_wait_room(unsync_screenshot_image, sync_game_window, sync_status, isDebug=False):
    find_game_button = cv2.imread("resources/tim_tran_2.png")
    button_h, button_w, _ = find_game_button.shape
    current = time()
    while sync_status.value != 0:
        if time() - current < BASE_WAIT_TIME:
            continue
        game_window_rect = sync_game_window[:]
        image = to_numpy_array(unsync_screenshot_image[:], crop=game_window_rect)
        min_val, min_loc = matching(image, find_game_button)
        if isDebug:
            debug(image, min_val, min_loc, keyTime=0)
        if min_val < BASE_THRESHOLD:
            x_pos = min_loc[0] + button_w//2 + game_window_rect[0]
            y_pos = min_loc[1] + button_h//2 + game_window_rect[1]
            direct_mouse_event("left", (x_pos, y_pos))
            direct_mouse_event("move", (300,500))
        current = time()

def stage_accept_game(unsync_screenshot_image, sync_game_window, sync_status, isDebug=False):
    join_game_button = cv2.imread("resources/choi_luon_2.png")
    button_h, button_w, _ = join_game_button.shape
    current = time()
    while sync_status.value != 0:
        if time() - current < BASE_WAIT_TIME:
            continue
        game_window_rect = sync_game_window[:]
        image = to_numpy_array(unsync_screenshot_image[:], crop=game_window_rect)
        min_val, min_loc = matching(image, join_game_button)
        if isDebug:
            debug(image, min_val, min_loc, keyTime=0)
        if min_val < BASE_THRESHOLD:
            x_pos = min_loc[0] + button_w//2 + game_window_rect[0]
            y_pos = min_loc[1] + button_h//2 + game_window_rect[1]
            direct_mouse_event("left", (x_pos, y_pos))
            direct_mouse_event("move", (300,500))
            sync_status.value = 2
        current = time()

def stage_out_game(unsync_screenshot_image, sync_status, isDebug=False):
    ff_background = cv2.imread("resources/resources/ff_ready.png")
    accept_out_game = cv2.imread("resources/resources/ff_accept.png")
    button_h, button_w, _ = accept_out_game.shape
    current = time()
    while sync_status.value != 0:
        if time() - current < BASE_WAIT_TIME:
            continue
        image = to_numpy_array(unsync_screenshot_image[:])
        min_val, _ = matching(image, ff_background)
        if isDebug:
            debug(image, min_val, min_loc, keyTime=0)
        if min_val < BASE_THRESHOLD:
            direct_key_event('enter')
            direct_key_event("/")
            direct_key_event("f")
            direct_key_event("f")
            direct_key_event('enter')
            sleep(2)
            image = to_numpy_array(unsync_screenshot_image[:])
            min_val, min_loc = matching(image, accept_out_game)
            if isDebug:
                debug(image, min_val, min_loc, keyTime=0)
            if min_val < BASE_THRESHOLD:
                x_pos = min_loc[0] + button_w//2 + SCREEN_RESOLUTION[0]
                y_pos = min_loc[1] + button_h//2 + SCREEN_RESOLUTION[1]
                direct_mouse_event("holdLeft", (x_pos, y_pos))
                direct_mouse_event("releaseLeft", (x_pos, y_pos))
                direct_mouse_event("move", (300,500))
        current = time()

def stage_replay(unsync_screenshot_image, sync_game_window, sync_status, isDebug=False):
    replay_game_button = cv2.imread("resources/choi_lai_2.png")
    button_h, button_w, _ = replay_game_button.shape
    current = time()
    while sync_status.value != 0:
        if time() - current < BASE_WAIT_TIME:
            continue
        game_window_rect = sync_game_window[:]
        image = to_numpy_array(unsync_screenshot_image[:], crop=game_window_rect)
        min_val, min_loc = matching(image, replay_game_button)
        if isDebug:
            debug(image, min_val, min_loc, keyTime=0)
        if min_val < BASE_THRESHOLD:
            x_pos = min_loc[0] + button_w//2 + game_window_rect[0]
            y_pos = min_loc[1] + button_h//2 + game_window_rect[1]
            direct_mouse_event("left", (x_pos, y_pos))
            direct_mouse_event("move", (300,500))
            sync_status.value = 1
        current = time()