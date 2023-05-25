import sys
import time

from pymata4 import pymata4

def servo(my_board, pin):

    # set the pin mode
    my_board.set_pin_mode_servo(pin)

    # set the servo to 0 degrees
    my_board.servo_write(pin, 0)
    time.sleep(1)
    # set the servo to 90 degrees
    my_board.servo_write(pin, 90)
    time.sleep(1)
    # set the servo to 180 degrees
    my_board.servo_write(pin, 180)
    print("1")


board = pymata4.Pymata4()

try:
    servo(board, 5)
except KeyboardInterrupt:
    board.shutdown()
    sys.exit(0)
