# NeoPixelをいくつか（1セグ４個くらい）つないで７セグにし、大会用のタイマーにする。
# 7セグのaからbcdefgと順番に信号線で一直列につなぐ。7セグ１桁のタイマー。
# 残10分から表示し、時間ぎれで点滅＋ブザー鳴らす。
# 2017-03-21 by penkich
# 
from machine import Pin,I2C,Timer
from neopixel import NeoPixel
import time

npix = 4 # 1セグを構成するNeoPixelの個数
t = 50 # 時間設定（分） 

pin = Pin(4,Pin.OUT) # NeoPixelの信号線を接続
np = NeoPixel(pin, 7 * npix)
buz = Pin(5,Pin.OUT) # 圧電ブザーを接続
buz.high() # 起動時に少し鳴らす
time.sleep(1)
buz.low()

def seg7(n,rgb):
    data = [0xfc,0x60,0xda,0xf2,0x66,0xb6,0xbe,0xe4,0xfe,0xe6,0xee]
    x = data[n] >> 1
    out = []
    for i in range(7): 
        if x % 2:
            out.append(rgb)
        else:
            out.append(blank)
        x = x >> 1
    out.reverse()
    tmp = []
    for x in out:
        tmp = tmp + x # １次配列に変換
    j = 0
    data_len = npix * 7 * 3 # 3=RGB
    for i in range(0,data_len,3):
        np[j] = [tmp[i],tmp[i+1],tmp[i+2]] # RGB３つ１組の配列に変換 
        j = j + 1
    np.write()

blank = [0,0,0]*npix
green = [0,100,0]*npix
blue = [0,20,80]*npix
bluegreen = [40,40,20]*npix
purple = [50,0,50]*npix
red = [150,0,0]*npix
yellow = [80,80,0]*npix

def led():
    global i
    i = i-1
    if i > 60*11:
        np[0] = [50,50,50]
        np.write()
        time.sleep(0.4)
        np[0] = [0,0,0]
        np.write()
        time.sleep(0.1)
    elif i >= 60*10:
        seg7(10,green)
    elif i >= 60*9:
        seg7(9,blue)
    elif i >= 60*8:
        seg7(8,green)
    elif i >= 60*7:
        seg7(7,blue)
    elif i >= 60*6:
        seg7(6,green)
    elif i >= 60*5:
        seg7(5,blue)
    elif i >= 60*4:
        seg7(4,bluegreen)
    elif i >= 60*3:
        seg7(3,green)
    elif i >= 60*2:
        seg7(2,yellow)
    elif i >= 60*1:
        seg7(1,purple)
    elif i > 0:
        seg7(0,red)
    else:
        seg7(0,red)
        buz.high() # 時間ぎれでブザー鳴る
        time.sleep(0.8)
        seg7(0,blank)
        buz.low()
        time.sleep(0.1)

i = t * 60
tim = Timer(-1)
tim.init(period=1000, mode=Timer.PERIODIC, callback=lambda t:led()) # １秒ごとに割り込み
