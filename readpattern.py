import win32api
import winsound
import win32con

def bipbop():
    winsound.Beep(2000, 100)

def main():
    preX = 0
    preY = 0
    dX = 0
    dY = 0
    readc = False
    file = open('pattern.txt', 'w')
    while not win32api.GetAsyncKeyState(win32con.VK_MULTIPLY):
        if win32api.GetAsyncKeyState(win32con.VK_F8):
            readc = not readc

        if win32api.GetAsyncKeyState(win32con.VK_LBUTTON) < 0 and readc:
            bipbop()
            pos = win32api.GetCursorPos()
            if not (preX and preY):
                preX = pos[0]
                preY = pos[1]
            else:
                dX = int((pos[0] - preX) / 2)
                dY = int((pos[1] - preY) / 2)
                preX = pos[0]
                preY = pos[1]

            dxdy = "[{},{}]".format(dX, dY)
            print(dxdy, "\n")
            file.write(dxdy + ",\n")
    print("Exiting...")

if __name__ == "__main__":
    main()