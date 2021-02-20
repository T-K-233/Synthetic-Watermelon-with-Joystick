from pynput.mouse import Button, Controller

mouse = Controller()

while True:
    print ("Current position: " + str(mouse.position))
