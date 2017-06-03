#
# neopixcel test programn 2017-06-03
# CC0:No rights reserved
# ハートの鼓動をイメージして色を変化させる
#

from machine import Pin
from neopixel import NeoPixel
from time import *
import urandom

urandom.seed(2017)
pin = Pin(4,Pin.OUT) # NeoPixel data port
np = NeoPixel(pin, 5) # use 5 NeoPixels

def test(pw, t, bia):
    for i in range(pw):
        np.fill([i, pw-i, bia])
        np.write()
        sleep(t)
    for i in range(pw):
        np.fill([pw-i, bia, i])
        np.write()
        sleep(t)
    for i in range(pw):
        np.fill([bia, i, pw-i])
        np.write()
        sleep(t)

while True:
    test(100,0.01,urandom.getrandbits(6))
