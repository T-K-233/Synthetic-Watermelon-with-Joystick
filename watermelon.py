"""
 * @file watermelon.py
 * @author -T.K.- (t_k_233@outlook.com)
 * @version 0.1
 * @date 2021-02-20
 *
 * Maps the gamepad actions to mouse movements to play Synthetic Watermelon.
 *
 * @copyright Copyright (c) 2021
 * 
"""

import msvcrt
import time

from pynput.mouse import Button, Controller
import joystickapi


print("Initializing gamepad...")

num = joystickapi.joyGetNumDevs()
ret, caps, startinfo = False, None, None

for stick_id in range(num):
    ret, caps = joystickapi.joyGetDevCaps(stick_id)
    if ret:
        print("gamepad detected: " + caps.szPname)
        ret, startinfo = joystickapi.joyGetPosEx(stick_id)
        break
else:
    print("no gamepad detected")


gamepad_detected = ret
button_pressed = 0

mouse = Controller()

while gamepad_detected:
    # detect ESC, exit if pressed
    if msvcrt.kbhit() and msvcrt.getch() == chr(27).encode():
        break

    ret, info = joystickapi.joyGetPosEx(stick_id)
    if ret:
        btns = [(1 << i) & info.dwButtons != 0 for i in range(caps.wNumButtons)]
        axis_XYZ = [info.dwXpos-startinfo.dwXpos, info.dwYpos-startinfo.dwYpos, info.dwZpos-startinfo.dwZpos]
        axis_RUV = [info.dwRpos-startinfo.dwRpos, info.dwUpos-startinfo.dwUpos, info.dwVpos-startinfo.dwVpos]

        '''
        # print all buttons and axes for debug
        if info.dwButtons:
            print("buttons: ", btns)
        if any([abs(v) > 10 for v in axisXYZ]):
            print("axis:", axisXYZ)
        if any([abs(v) > 10 for v in axisRUV]):
            print("roation axis:", axisRUV)
        '''
        
        if btns[0] and not button_pressed:
            # move the cursor to the center of the screen
            mouse.position = (525, pos[1])
            # press to grab the fruit
            mouse.press(Button.left)
            button_pressed = 1
            
        if not btns[0] and button_pressed:
            # release the fruit
            mouse.release(Button.left)
            button_pressed = 0

        # move the cursor
        if axis_XYZ[0] < -100:
            pos = mouse.position
            mouse.position = (pos[0] - 10, pos[1])
        elif axis_XYZ[0] > 100:
            pos = mouse.position
            mouse.position = (pos[0] + 10, pos[1])
    
    time.sleep(0.01)

