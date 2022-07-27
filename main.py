from sure3208 import *
from font import *  # import all fonts in the font file


# On board LED used for diagnostics. Pico W specific
led = machine.Pin("LED", machine.Pin.OUT)

# From the Sure 3208 module, these are GPIO pins on the pico/ picoW
WR_PIN = 2
DATA_PIN = 3

# init the matrix                     Matrix CS pins       CMDs for init
s = sure3208(
    WR_PIN, DATA_PIN, font_8x5, [4, 5, 6], [sure3208.SYS_EN, sure3208.LED_On, sure3208.RC_Master_Mode, sure3208.PWM_DUTY_10]
)

#s.send_CMD(sure3208.PWM_DUTY_4)


s.defaults()
s.render("Matrix Rain")
s.update(1)
time.sleep(2)
s.bytes_buffer = s.bytearray
for f in range(300):
    # parameter1 = frequency of drop lines parameter 2 = frequency of drop line breaking (higher = less frequent)

    s.matrix_rain(16, 7)
    s.update(1)
s.defaults()
s.render("Vertical Shift")
s.update(1)
time.sleep(2)


for f in range(8):
    s.vertical = f * -1
    s.update(1)
s.defaults()
s.render("Vertical Shift")
s.update(1)
time.sleep(2)


for f in range(8):
    s.vertical = f
    s.update(1)
s.vertical = 0


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
s.scroll = 15
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



s.defaults()
s.justify = 1
s.render("_ New @ : 17")
s.update(1)
time.sleep(3)


s.defaults()
s.justify = 3
s.scroll = 0
s.scroll_direction = -1
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
s.scroll_direction = 1
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
s.delay = 0
s.scroll_direction = -1
s.render("Fastest possible scrolling with delay = 0")
s.update(1)
time.sleep(1)

count = 200
while count > 1:
    s.update(1)
    count = count - 1
s.defaults()
s.justify = 1
s.render("Custom sprites")
s.update(1)
time.sleep(2)

s.defaults()
s.justify = 3
s.scroll = 0
s.scroll_direction = 1
s.render("¬ ......  .   ¬  . ... .  ¬   . . . . .  .. ")
time.sleep(1)
count = 100
while count > 1:
    # s.render("¬")
    s.update(1)
    count = count - 1
s.defaults()
s.justify = 3
s.scroll = 0
s.scroll_direction = -1
s.render("` ......  .   `  . ... .  `   . . . . .  .. ")
time.sleep(1)
count = 100
while count > 1:
    # s.render("¬")
    s.update(1)
    count = count - 1
s.defaults()
s.justify = 1
s.scroll = 0
s.scroll_direction = -1
s.render("Sure 3208 Micropython driver for Raspberry PI Pico W by Andy Crook")

while 1:
    s.update(1)  # 1 = scroll only if long, 0 = no scroll, 2 = forced scroll
