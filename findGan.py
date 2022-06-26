from concurrent.futures import ThreadPoolExecutor, wait
import cv2
from argsolver import args
from logger import logger

threadPool = ThreadPoolExecutor(max_workers=1, thread_name_prefix="exec")
from pynput.keyboard import Listener
from keyboardsim import press_str,pressdown_str,pressup_str
import os
import time
import threading
import numpy as np
import matplotlib.pyplot as plt
from getscreennew import window_capture


import matplotlib.pyplot as plt

from utils import castimg


def perpareimg(img,show=False):
    # img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img720p = cv2.resize(img, (1280, 720))
    # img=cv2.cvtColor(img,cv2.COLOR_BGRA2RGB)
    imggray = img720p
    if show:
        plt.subplot(221)
        plt.imshow(imggray)

    h, w = imggray.shape[0:2]
    argmap = [0.35, 0.7, 0.45, 0.55]
    img_code_matrix = castimg(imggray, argmap, h, w)
    if show:
        plt.subplot(222)
        plt.imshow(img_code_matrix)
        plt.show()
    return img_code_matrix

def findGan():
    t1=time.time()
    img = window_capture(0, 'fullscreen', FULLRES=[3840, 2160])
    t2=time.time()
    res = perpareimg(img, show=False)
    # print('shape=')
    # print(res.shape)
    t3=time.time()
    h, w = res.shape[0:2]
    count = 0
    posAll = [0, 0]
    colorRange = [
        [35, 45], [35, 45], [199, 208]
    ]

    def colorInRange(col, min, max):
        return col >= min and col <= max

    def findx(pix):
        for ci in range(3):
            if not colorInRange(pix[ci], colorRange[ci][0], colorRange[ci][1]):
                return False
        return True

    def posAdd(col1, col2):
        return [col1[0] + col2[0], col1[1] + col2[1]]

    for i in range(h):
        tempH = res[i]
        for j in range(w):
            pix = tempH[j]

            findRes = findx(pix)
            if findRes:
                # posAll = posAdd(posAll, [i, j])
                count += 1

    # res=res.reshape(h*w,3)
    # for x in res:
    #     findRes=findx(x)
    #     if findRes:
    #         count+=1
    # print('findEnd', count)
    t4=time.time()
    timeArray=[t2-t1,t3-t2,t4-t3]
    print(timeArray)
    if count==0:
        return False
    posAll[0] /= count
    posAll[1] /= count
    # print('pos=')
    # print(posAll)
    return True

if __name__=="__main__":
    findGan()