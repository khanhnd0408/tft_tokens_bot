from tftBot import *
from multiprocessing import get_context

def run():
    ctx = get_context('spawn')
    syncSignal = ctx.Value('d', 1)
    syncGameWindow = ctx.Array('i', SCREEN_RESOLUTION)
    unsyncScreenshotImage = ctx.RawArray('i', SCREEN_RESOLUTION[2]*SCREEN_RESOLUTION[3]*3)
    
    
    processes = []
    processes.append(ctx.Process(target=getTFT_Window, args=(unsyncScreenshotImage, syncGameWindow, syncSignal, )))
    processes.append(ctx.Process(target=stage_WaitRoom, args=(unsyncScreenshotImage, syncGameWindow, syncSignal, )))
    processes.append(ctx.Process(target=stage_AcceptGame, args=(unsyncScreenshotImage, syncGameWindow, syncSignal, )))
    processes.append(ctx.Process(target=stage_OutGame, args=(unsyncScreenshotImage, syncSignal, )))
    processes.append(ctx.Process(target=stage_Replay, args=(unsyncScreenshotImage, syncGameWindow, syncSignal, )))
    processes.append(ctx.Process(target=getKeyboardEvent, args=(syncSignal, )))
    processes.append(ctx.Process(target=sync_TakeScreenShot, args=(unsyncScreenshotImage, syncSignal, )))

    for process in processes:
        process.start()
    for process in processes:
        process.join()


if __name__ == "__main__":
    run()