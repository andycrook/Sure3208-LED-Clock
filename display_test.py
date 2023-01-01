from sure3208 import *
from font import *  # import all fonts in the font file
import time
from machine import Pin, SPI
import random
    
    
# 
# # On board LED used for diagnostics. Pico W specific
# led = machine.Pin("LED", machine.Pin.OUT)
# 
# # From the Sure 3208 module, these are GPIO pins on the pico/ picoW
SCK_PIN = 18
MOSI_PIN = 19
#                                         [17, 20, 15]
# # init the matrix                     Matrix CS pins       CMDs for init
s = sure3208(SCK_PIN, MOSI_PIN, font_8x5, [17,20,15], [sure3208.SYS_EN, sure3208.LED_On, sure3208.RC_Master_Mode,sure3208.PWM_DUTY_9])
# 
# #s.send_CMD(sure3208.PWM_DUTY_4)


print("class instantiated")


print("Value")















s.brightness(12)
s.justify = 1
s.scroll = 0
s.font = font_8x5
s.fill(0)
s.render("Pixel Drawing")
s.update(1)
time.sleep(2)

s.justify = 1
s.scroll = 0
s.font = font_8x5
s.fill(0)
s.render("Set, Unset, Invert")
s.update(1)
time.sleep(3)

for f in range(100):
    s.set_pixel(random.randrange(96),random.randrange(8),2)
    #time.sleep(0.1)
    s.update(1)
time.sleep(2)
s.fill(0)
s.new_buffer(0)
s.update(1)


s.justify = 1
s.scroll = 0
s.font = font_8x5
s.fill(0)
s.render("Rectangle Draw")
s.update(1)
time.sleep(2)
s.fill(0)
s.render(" ")
s.update(1)

for f in range(10):
    x = random.randrange(50)
    y = random.randrange(3)
    w = random.randrange(96-x)
    h = random.randrange(8-y-1)+1
    s.draw_rect(x,y,w,h,random.randrange(1),1) # x y width height fill value
    s.update(1)
    time.sleep(0.5)
    s.fill(0)
    s.new_buffer(0)
time.sleep(3)



#for f in range(200):
#s.update(1)
s.render("Matrix Rain")
s.update(1)
time.sleep(2)
s.invert()
s.update(1)
time.sleep(2)
s.bytes_buffer = s.bytearray
for f in range(100):
    # parameter1 = frequency of drop lines parameter 2 = frequency of drop line breaking (higher = less frequent)

    s.matrix_rain(16, 7)
    time.sleep(0.02)
    s.update(1)


s.defaults()

s.render("Vertical Shift Down")
s.update(1)
time.sleep(2)


for f in range(9):
    s.vertical = f * -1
    s.update(1)
time.sleep(1)
    
    
s.defaults()

s.render("Vertical Shift Up")
s.update(1)
time.sleep(2)


for f in range(8):
    s.vertical = f
    s.update(1)
s.vertical = 0
time.sleep(2)

s.defaults()
s.justify = 0  # center justify mode  0 = left, 1 = center, 2 = right 3 = none (set scroll manually for placement!)
s.render("Left Justify")
s.update(1)
time.sleep(3)

s.defaults()
s.justify = 1
s.render("Center Justify")
s.update(1)
time.sleep(3)

s.defaults()
s.justify = 2
s.render("Right Justify")
s.update(1)
time.sleep(3)

s.defaults()
s.justify = 3
s.scroll = 3
s.render("Manual")
s.update(1)
time.sleep(1)

s.defaults()
s.justify = 3
s.scroll = 25
s.render("Manual")
s.update(1)
time.sleep(1)

s.defaults()
s.justify = 3
s.scroll = 55
s.render("Manual")
s.update(1)
time.sleep(1)

s.defaults()
s.justify = 1
s.brightness(1)
s.render("BRIGHTNESS")
s.update(1)
for g in range(5):
    for f in range(1,16):
        s.brightness(f)
        time.sleep(0.05)
    for f in range(16,1,-1):
        s.brightness(f)
        time.sleep(0.05)


s.brightness(12)
s.defaults()
s.justify = 1
s.render("_ New @ : 17")
s.update(1)
time.sleep(3)


s.defaults()
s.justify = 3
s.scroll = 0
s.scroll_direction = 1
s.render("Long message scrolling to the left")
s.update(1)
time.sleep(1)

count = 200
while count > 1:
    s.update(1)
    count = count - 1
    
    
    
s.defaults()
s.justify = 3
s.scroll = 0
s.scroll_direction = 2
s.render("Long message scrolling to the left step 2")
s.update(1)
time.sleep(1)

count = 200
while count > 1:
    s.update(1)
    count = count - 1
    
s.defaults()
s.justify = 3
s.scroll = 0
s.delay = 0
s.scroll_direction = 2
s.render("Long message scrolling to the left fastest possible single step")
s.update(1)
time.sleep(1)

count = 200
while count > 1:
    s.update(1)
    count = count - 1    

    
s.defaults()
s.justify = 3
s.scroll = 0
s.scroll_direction = -1
s.render("Long message scrolling to the right")
s.update(1)
time.sleep(1)


count = 200
while count > 1:
    s.update(1)
    count = count - 1
    
    

s.defaults()
s.justify = 3
s.scroll = 0
s.scroll_direction = -2
s.render("Long message scrolling to the right step -2")
s.update(1)
time.sleep(1)


count = 200
while count > 1:
    s.update(1)
    count = count - 1


    
s.defaults()
s.justify = 3
s.scroll = 0
s.scroll_direction = 1
s.font = font_spectrum
s.render("Different fonts on the fly")
s.update(1)
time.sleep(1)

count = 200
while count > 1:
    s.update(1)
    count = count - 1
    
s.defaults()
s.justify = 1
s.scroll = 0
s.fill(0)

s.font = font_8x5
s.render("Font")
s.font = font_spectrum
s.render("Change",1)   # argument = 1 = append text to buffer
s.font = font_8x5
s.render("Per",1)
s.font = font_spectrum
s.render("Line",1)

s.update(1)
time.sleep(5)




s.defaults()
s.justify = 3
s.scroll = 0
s.font = font_8x5
s.scroll_direction = 1
s.render("SURE 3208 Micropython Driver")
s.font = font_spectrum
s.render(" by Andy Crook 2023 for Raspberry Pico W",1)
while 1:
    s.update(1)
    #time.sleep(1)
    
    

