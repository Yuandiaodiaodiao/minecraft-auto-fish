from concurrent.futures import ThreadPoolExecutor, wait
import cv2
from argsolver import args
from logger import logger

threadPool = ThreadPoolExecutor(max_workers=1, thread_name_prefix="exec")
from pynput.keyboard import Listener
from keyboardsim import press_str,pressdown_str,pressup_str,mouseClick
import os
import time
import threading
import numpy as np
import matplotlib.pyplot as plt
from getscreennew import getpicture


import matplotlib.pyplot as plt

from utils import castimg


from findGan import findGan

def get_key_name(key):
    t = None
    try:
        t = key.char
    except:
        try:
            t = key.name
        except:
            return ""
    return t


def get_thread_id(thread):
    for id, t in threading._active.items():
        if t is thread:
            return id


def raise_exception(thread_id):
    import ctypes
    res = ctypes.pythonapi.PyThreadState_SetAsyncExc(thread_id,
                                                     ctypes.py_object(SystemExit))
    if res > 1:
        ctypes.pythonapi.PyThreadState_SetAsyncExc(thread_id, 0)
        print('Exception raise failure')




def stop():
    global threadPool
    for thread in threadPool._threads:
        id = get_thread_id(thread)
        raise_exception(id)

    threadPool.shutdown(wait=False)


def restart():
    global threadPool
    stop()
    threadPool = ThreadPoolExecutor(max_workers=1, thread_name_prefix="exec")




def presskey(key):
    global threadPool
    t = get_key_name(key)

    if t == args.record:
        def run():

            print('录制异常退出')

        threadPool.submit(run)



    elif t=='f7':
        def run():

            res = findGan()
            if not res:
                mouseClick()
                time.sleep(3)
            while True:

                res=findGan()
                if res:
                    print('找到鱼漂')
                else:
                    print('找不到')
                    mouseClick()
                    time.sleep(1)
                    mouseClick()
                    time.sleep(3)
        threadPool.submit(run)

    elif t == args.stop:
        # 停止当前的动作
        logger.info("stop")
        restart()

    elif t == args.allstop:
        # 停止进程
        stop()
        exit(0)
        raise Exception

if __name__ == '__main__':
    logger.info("start!")

    with Listener(on_press=presskey) as listener:
        listener.join()
