# Generic imports
import board
import digitalio
import time
# NeoPixel stuff
import neopixel
import colors
from adafruit_led_animation.animation.rainbow import Rainbow
# Keyboard stuff
import usb_hid
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keycode import Keycode
from keyboard_layout_win_sw import KeyboardLayout

#----- Set up on-board LED -----
led = digitalio.DigitalInOut(board.LED)
led.direction = digitalio.Direction.OUTPUT
def LED_toggle():
    led.value = not led.value

#----- Set up a keyboard device. -----
kbd = Keyboard(usb_hid.devices)
layout = KeyboardLayout(kbd)
btns = [digitalio.DigitalInOut(board.GP15),
        digitalio.DigitalInOut(board.GP14)]
num_btns = len(btns)
for x in range(num_btns):
    btns[x].direction = digitalio.Direction.INPUT
    btns[x].pull = digitalio.Pull.UP
PRESSED = False
RELEASED = True
btn_prev_values = [RELEASED] * num_btns

#----- Set up NeoPixel chain -----
pixel_pin = board.GP17
rgb_order = neopixel.GRB
pixels = neopixel.NeoPixel(pin=pixel_pin, n=num_btns, brightness=0.2, 
    auto_write=False, pixel_order=rgb_order)
mainColor = colors.RED

def np_all(color: colors):
    pixels.fill(color)
    pixels.show()

def np_one(num: int, color: colors):
    pixels[num] = color
    pixels.show()

def handle_btn_coloring(num: int, state: bool):
    if state != btn_prev_values[num]:
        if state == RELEASED:
            if animating: return
            else: 
                np_one(num, mainColor)
        else:
            np_one(num, colors.WHITE)
    else:
        if state == PRESSED & animating:
            np_one(num, colors.WHITE)
        elif not animating & state == RELEASED:
            np_one(num, mainColor)

#----- THE ACTUAL PROGRAM -----
np_all(mainColor)
runSpeed = 0.05
rainbow = Rainbow(pixels, speed=runSpeed, period=3)
animating = False

toggle = True

# Continuous code
while True:
    if animating:
        rainbow.animate()

    for x in range(num_btns):
        curr_state = btns[x].value
        handle_btn_coloring(x, curr_state)
        if curr_state != btn_prev_values[x]:
            if curr_state == RELEASED:
                print("Button " + str(x) + " released")
            else:
                print("Button " + str(x) + " pressed")

            # WHAT SHOULD THE FIRST BUTTON DO?
            if x == 0:
                if curr_state == PRESSED:
                    if animating: animating = False
                    else: animating = True

            # WHAT SHOULD THE SECOND BUTTON DO?
            elif x == 1:
                if curr_state == PRESSED:
                    if toggle: 
                        mainColor = colors.BLUE
                        toggle = False
                    else:
                        mainColor = colors.RED
                        toggle = True

            btn_prev_values[x] = curr_state
    time.sleep(runSpeed)