import win32api
import winsound
import win32con
import cv2
import time
import json
import threading
import numpy as np
from PIL import ImageGrab


def beep_on():
    winsound.Beep(2000, 100)

def beep_off():
    winsound.Beep(1000, 100)

def get_tick(rpm):
    rps = rpm/60
    ms = 1000.0/rps
    s = round(ms/1000, 3)
    return s

def loadImages(weapons):
    images = {}
    for i in range(len(weapons)):
        images[i] = cv2.imread(weapons[i]["img"], cv2.IMREAD_GRAYSCALE)
        images[i] = images[i].astype(np.float32)
    return images

def detectCurrentWeapon(images):
    screen = ImageGrab.grab().convert("RGB")
    screen = np.array(screen)
    screen = screen[:, :, ::-1].copy()
    screen = screen.astype(np.float32)
    
    screenGray = cv2.cvtColor(screen, cv2.COLOR_BGR2GRAY)
    for i in range(len(images)):
        template = images[i]
        w, h = template.shape[::-1]

        res = cv2.matchTemplate(screenGray, images[i], cv2.TM_CCOEFF_NORMED)
        threshold = 0.95
        loc = np.where( res >= threshold)
        for pt in zip(*loc[::-1]):
            cv2.rectangle(screen, pt, (pt[0] + w, pt[1] + h), (0,0,255), 2)
        cv2.imwrite('res.png', screen)
        cv2.imwrite('ehmole.png', images[i])
        print(str(i))
        print(list(zip(*loc[::-1])))
        if list(zip(*loc[::-1])):
            return i
    return None

class threadWeaponDetect(threading.Thread):
    def __init__(self, images):
        threading.Thread.__init__(self)
        self.images = images
        self.index = None
        self.norecoil = False
        self.stop = False

    def run(self):
        while not self.stop:
            if self.norecoil:
                index = detectCurrentWeapon(self.images)
                self.index = index
            time.sleep(0.05)
        
    def sstop(self):
        self.stop = True


def main():
    try:
        with open('config.json', 'r') as file:
            config = json.load(file)
            weapons = config["weapons"]
            file.close
    except:
        print("Could not read config file!")
        return
    images = loadImages(weapons)
    wDetect = threadWeaponDetect(images)
    wDetect.setDaemon(True)
    wDetect.start()
    while True:
        if win32api.GetAsyncKeyState(win32con.VK_F8):
            wDetect.norecoil = not wDetect.norecoil
            if wDetect.norecoil:
                beep_on()
            else:
                beep_off()
            print("No Recoil = " + str(wDetect.norecoil))
        
        if win32api.GetAsyncKeyState(win32con.VK_END):
            wDetect.sstop()
            exit()

        shoti = 0
        while (wDetect.norecoil and win32api.GetKeyState(win32con.VK_LBUTTON) < 0 and wDetect.index != None):
            weapon = weapons[wDetect.index]
            wtick = get_tick(weapon["rpm"])
            pattern = weapon["pattern"]
            if shoti < len(pattern):
                currentshot = pattern[shoti]
                win32api.mouse_event(win32con.MOUSEEVENTF_MOVE, int(-currentshot[0]), int(-currentshot[1]), 0, 0)
                print("Shot {} fired with {}".format(shoti+1, weapon["name"]))
                time.sleep(wtick)
                shoti += 1

if __name__ == "__main__":
    main()