from tft_bot import *
from multiprocessing import get_context

def run():
    ctx = get_context('spawn')
    sync_signal = ctx.Value('d', 1)
    sync_game_window = ctx.Array('i', SCREEN_RESOLUTION)
    unsync_screenshot_image = ctx.RawArray('i', SCREEN_RESOLUTION[2]*SCREEN_RESOLUTION[3]*3)
    
    
    processes = []
    processes.append(ctx.Process(target=get_tft_window, args=(unsync_screenshot_image, sync_game_window, sync_signal, )))
    processes.append(ctx.Process(target=stage_wait_room, args=(unsync_screenshot_image, sync_game_window, sync_signal, )))
    processes.append(ctx.Process(target=stage_accept_game, args=(unsync_screenshot_image, sync_game_window, sync_signal, )))
    processes.append(ctx.Process(target=stage_out_game, args=(unsync_screenshot_image, sync_signal, )))
    processes.append(ctx.Process(target=stage_replay, args=(unsync_screenshot_image, sync_game_window, sync_signal, )))
    processes.append(ctx.Process(target=get_keyboard_event, args=(sync_signal, )))
    processes.append(ctx.Process(target=sync_take_screenshot, args=(unsync_screenshot_image, sync_signal, )))

    for process in processes:
        process.start()
    for process in processes:
        process.join()


if __name__ == "__main__":
    run()