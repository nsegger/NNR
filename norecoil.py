import win32api
import winsound
import win32con
import time
import json


def beep_on():
    winsound.Beep(2000, 100)

def beep_off():
    winsound.Beep(1000, 100)

def get_tick(rpm):
    rps = rpm/60
    mstick = 1000.0/rps
    stick = round(mstick/1000, 3)
    return stick

def main():
    norecoil = False
    try:
        with open('config.json', 'r') as file:
            config = json.load(file)
            weapons = config["weapons"]
    except:
        print("Could not read config file!")
        return
    while True:
        if win32api.GetAsyncKeyState(win32con.VK_F8):
            norecoil = not norecoil
            if norecoil:
                beep_on()
            else:
                beep_off()
            print("No Recoil = " + str(norecoil))
        
        shoti = 0
        while (norecoil and win32api.GetKeyState(win32con.VK_LBUTTON) < 0):
            weapon = weapons[0]     #r99
            wtick = get_tick(weapon["rpm"])
            print(wtick)
            pattern = weapon["pattern"]
            if shoti < len(pattern):
                currentshot = pattern[shoti]
                win32api.mouse_event(win32con.MOUSEEVENTF_MOVE, int(-currentshot[0]), int(-currentshot[1]), 0, 0)
                print("Shot {} fired with {}".format(shoti+1, weapon["name"]))
                time.sleep(wtick)
                shoti += 1

if __name__ == "__main__":
    main()