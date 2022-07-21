import machine
import time
import network
from urequests import get
import uasyncio as asyncio
import json

# On board LED used for diagnostics. Pico W specific
led = machine.Pin("LED", machine.Pin.OUT)

# From the Sure 3208 module, these are GPIO pins on the pico/ picoW
WR_PIN = 2
DATA_PIN = 3

# CMD codes for the matrix
SYS_DIS = 0b100_0000_0000_0
SYS_EN = 0b100_0000_0001_0
LED_Off = 0b100_0000_0010_0
LED_On = 0b100_0000_0011_0
BLINK_Off = 0b100_0000_1000_0
BLINK_On = 0b100_0000_1001_0
SLAVE_Mode = 0b100_0001_0000_0
RC_Master_Mode = 0b100_0001_1000_0
EXT_CLK_Mode = 0b100_0001_1100_0
COM_Option_1 = 0b100_0010_0000_0
COM_Option_2 = 0b100_0010_0100_0
COM_Option_3 = 0b100_0010_1000_0
COM_Option_4 = 0b100_0010_1100_0
PWM_DUTY_1 = 0b100_1010_0000_0
PWM_DUTY_2 = 0b100_1010_0001_0
PWM_DUTY_3 = 0b100_1010_0010_0
PWM_DUTY_4 = 0b100_1010_0011_0
PWM_DUTY_5 = 0b100_1010_0100_0
PWM_DUTY_6 = 0b100_1010_0101_0
PWM_DUTY_7 = 0b100_1010_0110_0
PWM_DUTY_8 = 0b100_1010_0111_0
PWM_DUTY_9 = 0b100_1010_1000_0
PWM_DUTY_10 = 0b100_1010_1001_0
PWM_DUTY_11 = 0b100_1010_1010_0
PWM_DUTY_12 = 0b100_1010_1011_0
PWM_DUTY_13 = 0b100_1010_1100_0
PWM_DUTY_14 = 0b100_1010_1101_0
PWM_DUTY_15 = 0b100_1010_1110_0
PWM_DUTY_16 = 0b100_1010_1111_0

# Custom font. Numbers all the same width to easily justify numbver display together
# without pixel shifts moving from 01 to 02 etc
# Custom sprites allowed as well
font_8x5 = {
    " ": [0b00000000],
    "!": [0b11111010],
    '"': [0b11000000, 0b00000000, 0b11000000],
    "~": [0b00101000, 0b01111100, 0b00101000, 0b01111100, 0b00101000],
    "$": [0b00100100, 0b01010110, 0b11010100, 0b01001000],
    "%": [0b11000110, 0b11001000, 0b00010000, 0b00100110, 0b11000110],
    "&": [0b01101100, 0b10010010, 0b01101010, 0b00000100, 0b00001010],
    "'": [0b11000000],
    "(": [0b00111000, 0b01000100, 0b10000010],
    ")": [0b10000010, 0b01000100, 0b00111000],
    "*": [0b00010100, 0b00011000, 0b01110000, 0b00011000, 0b00010100],
    "+": [0b00010000, 0b00010000, 0b01111100, 0b00010000, 0b00010000],
    ",": [0b00001101, 0b00001110],
    "-": [0b00010000, 0b00010000, 0b00010000, 0b00010000],
    ".": [0b00000010],
    "/": [0b00000110, 0b00111000, 0b11000000],
    "0": [0b01111100, 0b10000010, 0b10000010, 0b01111100],
    "1": [0b01000010, 0b11111110, 0b00000010, 0b00000000],
    "2": [0b01000110, 0b10001010, 0b10010010, 0b01100010],
    "3": [0b01000100, 0b10000010, 0b10010010, 0b01101100],
    "4": [0b00011000, 0b00101000, 0b01001000, 0b11111110],
    "5": [0b11100100, 0b10100010, 0b10100010, 0b10011100],
    "6": [0b01111100, 0b10010010, 0b10010010, 0b01001100],
    "7": [0b10000110, 0b10001000, 0b10010000, 0b11100000],
    "8": [0b01101100, 0b10010010, 0b10010010, 0b01101100],
    "9": [0b01100100, 0b10010010, 0b10010010, 0b01111100],
    ":": [0b01000100],
    ";": [0b00000001, 0b00001010],
    "<": [0b00001000, 0b00010100, 0b00100010],
    "=": [0b00101000, 0b00101000, 0b00101000],
    ">": [0b00100010, 0b00010100, 0b00001000],
    "?": [0b01000000, 0b10011010, 0b10010000, 0b01100000],
    "@": [0b01111100, 0b10010010, 0b10101010, 0b10111010, 0b01110000],
    "A": [0b01111110, 0b10001000, 0b10001000, 0b01111110],
    "B": [0b11111110, 0b10010010, 0b10010010, 0b01101100],
    "C": [0b01111100, 0b10000010, 0b10000010, 0b01000100],
    "D": [0b11111110, 0b10000010, 0b10000010, 0b01111100],
    "E": [0b11111110, 0b10010010, 0b10010010, 0b10000010],
    "F": [0b11111110, 0b10010000, 0b10010000, 0b10000000],
    "G": [0b01111100, 0b10000010, 0b10010010, 0b01011110],
    "H": [0b11111110, 0b00010000, 0b00010000, 0b11111110],
    "I": [0b10000010, 0b11111110, 0b10000010],
    "J": [0b00001100, 0b00000010, 0b10000010, 0b11111100],
    "K": [0b11111110, 0b00010000, 0b00101000, 0b11000110],
    "L": [0b11111110, 0b00000010, 0b00000010, 0b00000010],
    "M": [0b11111110, 0b01000000, 0b00110000, 0b01000000, 0b11111110],
    "N": [0b11111110, 0b00100000, 0b00010000, 0b00001000, 0b11111110],
    "O": [0b01111100, 0b10000010, 0b10000010, 0b01111100],
    "P": [0b11111110, 0b10010000, 0b10010000, 0b01100000],
    "Q": [0b01111100, 0b10000010, 0b10000010, 0b01111101],
    "R": [0b11111110, 0b10010000, 0b10010000, 0b01101110],
    "S": [0b01100100, 0b10010010, 0b10010010, 0b01001100],
    "T": [0b10000000, 0b10000000, 0b11111110, 0b10000000, 0b10000000],
    "U": [0b11111100, 0b00000010, 0b00000010, 0b11111100],
    "V": [0b11110000, 0b00001100, 0b00000010, 0b00001100, 0b11110000],
    "W": [0b11111100, 0b00000010, 0b00011100, 0b00000010, 0b11111100],
    "X": [0b11000110, 0b00101000, 0b00010000, 0b00101000, 0b11000110],
    "Y": [0b11100000, 0b00010000, 0b00001110, 0b00010000, 0b11100000],
    "Z": [0b10000110, 0b10001010, 0b10010010, 0b11100010],
    "[": [0b11111110, 0b10000010],
    "\\": [0b10000000, 0b01100000, 0b00011000, 0b00000110],
    "]": [0b10000010, 0b11111110],
    "^": [0b01000000, 0b10000000, 0b01000000],
    "_": [0b00000010, 0b00000010, 0b00000010, 0b00000010],
    "¬": [0b00100000, 0b00100000, 0b00100010, 0b00100110, 0b00111110, 0b00100110, 0b00100110, 0b00000110, 0b00101110,
          0b00111110, 0b00110110, 0b01100000, 0b01100000, 0b00100000, 0b00100000, 0b00100000],
    "`": [0b00010000, 0b00110000, 0b00111000, 0b00110000, 0b00010000, 0b00010000, 0b00010000, 0b00010000, 0b00010000,
          0b00010000, 0b00010000, 0b00110000, 0b00111010, 0b00111110, 0b01111110, 0b01111110, 0b01101110, 0b00000110,
          0b00000010, 0b00000010, 0b00000010, 0b00000010]}


# These last two have been taken for sprites - NCC 1701 and a Klingon battlecruiser. Don't judge me :)


# Class for the Sure 3208 led single colour matrix
class Sure3208:
    def __init__(self, wr_pin, data_pin, cs_pin=[], CMDS=[]):
        # CS pins are given as a list in the initialisation of the instance
        # CMDS are also given as a list that are applied to all the matrices on startup
        self.cs = cs_pin
        self.cmds = CMDS

        # setup GPIO pins for the devices...
        for f in range(len(self.cs)):
            self.cs[f] = machine.Pin(cs_pin[f], machine.Pin.OUT)
        self.wr = machine.Pin(wr_pin, machine.Pin.OUT)
        self.data = machine.Pin(data_pin, machine.Pin.OUT)

        # remember number of screens from CS list
        self.num_screens = len(self.cs)
        # Setup a bytearray to hold data for the screens
        self.bytearray = bytearray(len(self.cs) * 32)
        # message to display is held in the instance as is the scrolll shift value. Minus values shift to the left.
        self.message = ""
        self.justify = 1 # justify mode. 0 is none (left justify), 1 = centre (default) 2 = right !!!RIGHT NOT IMPLEMENTED YET!!!
        self.scroll = 0
        self.countdown =0 # to set if you want the data to be temporary
        self.weather = ""
        
        
        # Now apply all the startup CMD's to all the screens
        for f in range(len(self.cs)):
            for t in range(len(self.cmds)):
                self.send_data(self.cmds[t], f, 12)

            self.cs[f].on()

    def send_data(self, bits, screen, length):
        # send binary data to device bit by bit

        # Go through bits and put them in a list (the right way round)
        bit_list = [(bits >> shift_ind) & 1
                    for shift_ind in range(length)]
        bit_list.reverse()

        self.cs[screen].off()  # prepare the matrix for data

        for bit in bit_list:  # loop through the bits from the data

            if bit == 1:  # set the data pin to the bit data
                self.data.on()
            else:
                self.data.off()

            self.wr.off()  # cycle the WR pin to set the bit 
            self.wr.on()

        self.cs[screen].on()  # close the matrix for data

    def write_text(self, text, position):
        b = 0
        text = text.upper() # No lowercase in font, convert
        length = 0
        
        # write all characters to b
        for character in text:
            try:
                b = self.write_chr(b, font_8x5[character])
                length = length + 1 + len(font_8x5[character])

            except:
                print("CHR NOT FOUND")
                
        # make bytes_val the bytes to write to the matrix
        bytes_val = b.to_bytes(length, 'big')

        if len(bytes_val) < s.num_screens * 32:
            # it will fit, centre jusify
            if s.message != "" and s.justify ==1:
                s.scroll = int(((s.num_screens * 32) - len(bytes_val)) / 2)
                position = s.scroll

        # Chr byte position
        cb = position
        # go through the bytes in the message
        for byt in bytes_val:
            # if it's in range of the display, put it in the instance bytearray buffer
            # maybe we should go through the buffer instead? FOr long messages We will process bytes that aren't being displayed? Time penalty?
            if cb < len(self.bytearray) and cb > -1:
                self.bytearray[cb] = byt
            # increment byte position to write
            cb = cb + 1
        # If we're scrolling a message and it wraps completely, shift it to start again
        if (position * -1) > (len(bytes_val)):
            s.scroll = s.num_screens * 32

    def write_chr(self, by, c):
        # c is a list of binay data to add to by and returns it
        for font_bytes in c:
            by = by << 8
            by = by | int(font_bytes)
        by = by << 8  # This creates a single blank line between the characters
        return by

    def fill(self, value):
        # fill the matrix with a value - usually 0 to blank the display before writing
        for byt in range(len(self.bytearray)):
            self.bytearray[byt] = value

    def sideshift(self, value):
        # shift the instance bytyearray by the value number of places. Used for manual justification of the clock
        temp = bytearray(len(self.bytearray))
        
        for i in range(len(self.bytearray)):
            if (i + value) >= 0 and (i + value) < len(self.bytearray):
                temp[i + value] = self.bytearray[i]
                
        self.bytearray = temp


def update(b):
    screen = 0
    # Command code for writing. Address at 0 because we're going to sequentially write to the whole matrix
    CMD = 0b1010000000  
    bytes_written_index = 0

    for t in b:  # loop through every byte in the framebuffer - 32 X number of matrices

        bit_expand = CMD << 8  # add 8 bit slots

        # Get the bits from the byte so that we can easily reverse it
        bit_list = [(t >> shift_ind) & 1
                    for shift_ind in range(8)]  
        bit_list.reverse()  
        # reverse to big endian for the sure 3208 matrix. Comment out this line if your text appears upside down!

        # get the bits and reconstruct it into an 8 bit byte
        a = 0
        for bit in bit_list:
            a = (a << 1) | bit

        # add the 8 bit byte to the command code
        CMD = bit_expand | a

        if bytes_written_index == 31:  # we have written 0 - 31 bytes, so the matrix is full. Send the data to the screen
            bytes_written_index = 0  # reset the bytes index to 0
            if screen < s.num_screens:  # only send if the matrix is in range
                s.send_data(CMD, screen,266)  # send the CMD and data to the screen - 266 bits in all for a full matrix
            CMD = 0b1010000000  # reset the CMD to the start
            screen = screen + 1  # increment the screen number

        else:
            bytes_written_index = bytes_written_index + 1  # add one to the index to keep adding data to the CMD


def wifi_login():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect('SSID', 'PASSWORD')
    while not wlan.isconnected() and wlan.status() >= 0:
        s.fill(0)  # empty instance bytearray
        s.write_text("Connecting..", 0)  # write text to the framebuffer
        update(s.bytearray)  # send all data to the matrix collection
        time.sleep(0.5)
        s.fill(0)  # empty instance bytearray
        s.write_text("------------", 0)  # write text to the framebuffer
        update(s.bytearray)  # send all data to the matrix collection
        time.sleep(0.5)

    status = wlan.ifconfig()
    print('ip = ' + status[0])


async def serve_client(reader, writer):
    
    # HTML Page to deliver
    
    html = """<!DOCTYPE html><html><head>
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Pico W LED Matrix</title>
</head>
<body>
<h1>Pico LED Matrix Messeger</h1>
<p>Commands:<br><br>
clock = switch to clock mode<br>
brightnessX = set brightness (X = 1-16)<br>
¬ or ` = Starship :)
<br><br>


</p>
  <form action="#" method="post" 
          enctype="multipart/form-data">
        Message:
        <input type="text" name="message">
        <br>
        <br>
        <button type="submit" formmethod="GET">
          Upload 
        </button>
        <br>

    </form>

</body></html>"""

    #print("Client connected")
    request_line = await reader.readline()
    #print("Request:", request_line)
    # We are not interested in HTTP request headers, skip them
    while await reader.readline() != b"\r\n":
        pass
    # print(request.post('http://httpbin.org/post', json={"text": "value"}))

    request = str(request_line)
    #print(request)
    m_rec = ""
    try:
        if request.index("message") != -1:
            mstart = request.index("message")
            mend = request.index("HTTP")
            m_rec = request[mstart + 8:(mend - mstart) + 7]
            m_rec = m_rec.replace("+", " ")

        else:
            pass
            #print("No Message")

    except ValueError:
        pass
        #print("Not found!")

    if m_rec != "":
        
        old_message = s.message
        old_scroll = s.scroll
        # set message and reset scroll value

        m_rec = parse_url(m_rec)
        print(m_rec)
        s.message = m_rec
        s.scroll = 0

        # override if it's a command word
        if m_rec.lower() == "clock":
            s.message = ""
            s.scroll = 0
        
        if m_rec.lower() == "weather":
            s.message = weather()
            s.scroll = 0

        if m_rec[:10].lower() == "brightness":
            s.message = old_message
            s.scroll = old_scroll
            bright = int(m_rec[10:])
            print(bright)
            if bright == 1:
                cmd_PWM = PWM_DUTY_1
            if bright == 2:
                cmd_PWM = PWM_DUTY_2
            if bright == 3:
                cmd_PWM = PWM_DUTY_3
            if bright == 4:
                cmd_PWM = PWM_DUTY_4
            if bright == 5:
                cmd_PWM = PWM_DUTY_5
            if bright == 6:
                cmd_PWM = PWM_DUTY_6
            if bright == 7:
                cmd_PWM = PWM_DUTY_7
            if bright == 8:
                cmd_PWM = PWM_DUTY_8
            if bright == 9:
                cmd_PWM = PWM_DUTY_9
            if bright == 10:
                cmd_PWM = PWM_DUTY_10
            if bright == 11:
                cmd_PWM = PWM_DUTY_11
            if bright == 12:
                cmd_PWM = PWM_DUTY_12
            if bright == 13:
                cmd_PWM = PWM_DUTY_13
            if bright == 14:
                cmd_PWM = PWM_DUTY_14
            if bright == 15:
                cmd_PWM = PWM_DUTY_15
            if bright == 16:
                cmd_PWM = PWM_DUTY_16
            for f in range(s.num_screens):
                s.send_data(cmd_PWM, f, 12)

    response = html
    writer.write('HTTP/1.0 200 OK\r\nContent-type: text/html\r\n\r\n')
    writer.write(response)

    await writer.drain()
    await writer.wait_closed()
    #print("Client disconnected")


def get_json_time():
    # get the time from the network
    r = get("http://date.jsontest.com")
    t = r.json()
    return t

# set the internal RTC time for the pico
def set_machine_rtc():
    t = get_json_time()
    time_now = t["time"]
    date_now = t["date"]
    dst = 0

    # NEEDS FIXING. DST is from last sunday in march to last sunday in october
    if int(date_now[:2]) > 3 and int(date_now[:2]) < 10:
        dst = 1
    # Note! It seems the month and day are reversed, not correct in the official docs??
    ampm = time_now[9:11]
    ampmconv = 0
    
    # add 12 hours if it's PM. Add in PM/AM to the screen?
    if ampm == "PM":
        ampmconv = 12
        
    # Set the pico datetime from the JSON output
    machine.RTC().datetime((int(date_now[6:10]), int(date_now[:2]), int(date_now[3:5]), 4,
                            int(time_now[:2]) + dst + ampmconv, int(time_now[3:5]), int(time_now[6:8]), 0))

# add leading zeros to a string and return it
def lead_zero(text, num):
    if len(text) < num:
        text = "0" * (num - len(text)) + text
    return text


def parse_url(url):
    # I can't find a urllib module. This will do. Incomplete at the moment
    replace_url = {"%20": " ", "%21": "!", "%22": '"', "%23": "#", "%24": "$", "%25": "%", "%26": "&", "%27": "'",
                   "%28": "(", "%29": ")", "%2A": "*", "%2B": "+", "%2C": ",", "%2D": "-", "%2E": ".", "%2F": "/",
                   "%3A": ":", "%3B": ";", "%3C": "<", "%3D": "=", "%3E": ">", "%3F": "?", "%40": "@", "%AC": "¬",
                   "%60": "`"}
    temp = url
    # Search throgh dictionary for url code and replace for proper character
    for key, value in replace_url.items():
        temp = temp.replace(key, value)

    return temp


def weather():
    weather = ""
    
    try:
        # get the weather - use your own API and location
        #                                                   API*******************************API   
        r = get("http://api.weatherapi.com/v1/current.json?key=*******************************&q=LOCATION%20COUNTRY")

        parsed = r.json()
        #print (parsed)

        # Get some data from the JSON
        temp = str(parsed["current"]["temp_c"])
        condition = str(parsed["current"]["condition"]["text"])
        wind = str(parsed["current"]["wind_kph"])
        wind_dir = str(parsed["current"]["wind_dir"])
        cloud = str(parsed["current"]["cloud"])
        uv = str(parsed["current"]["uv"])
        precip = str(parsed["current"]["precip_mm"])
        
        # build the weather string
        weather = temp +" C  "+ condition + "  Precip:" +precip+" mm  Wind: "+wind + " kph "+wind_dir+"  Cloud %: "+cloud+"  UV lvl: "+uv 
        
        # times to scroll before returning to the clock
        s.weather = weather
        s.countdown = 5*32*s.num_screens # 5 scrolls is enough to get the data once and a bit on 3 screens
    except:
        # It didn't work :(
        weather = "Weather Failed"
        s.countdown = 10 # short message
    return weather



# main asynchronous function
async def main():
    # Set up some variables

  
    shifttoggle = 1

    while True:
        # check if we're still connected to the network....
        wlan = network.WLAN(network.STA_IF)
        while not wlan.isconnected():
            # if we're not, log back in
            wifi_login()
            asyncio.create_task(asyncio.start_server(serve_client, "0.0.0.0", 80))
            print('Setting up webserver...')
            led.on()
            set_machine_rtc()

        # Set up the time to display
        current_time = time.localtime()
        display_time = str(current_time[3]) + ":" + str(current_time[4]) + ":" + str(current_time[5]) + " " + str(
            current_time[2]) + "/" + str(current_time[1])
    
        # empty the instance byte buffer
        s.fill(0)
        if s.countdown>0:
            s.countdown = s.countdown-1
            
            if s.countdown==0:
                s.message = ""
        # It's a message to display
        if s.message != "":
            s.write_text(s.message, s.scroll)
            # take away from the scroll. This is overridden if the message fits and it's justified
            s.scroll = s.scroll - 1

        else:
            # write a clock out
            s.write_text(day[current_time[6]], 0)

            s.write_text(lead_zero(str(current_time[3]), 2), 4 + 17)
            s.write_text(":", 15 + 17)
            s.write_text(lead_zero(str(current_time[4]), 2), 18 + 17)
            s.write_text(":", 29 + 17)
            s.write_text(lead_zero(str(current_time[5]), 2), 32 + 17)

            s.write_text(lead_zero(str(current_time[2]), 2), 65)
            s.write_text("/", 76)
            s.write_text(lead_zero(str(current_time[1]), 2), 81)
            # shift it by 3 pixels to centre the display
            s.sideshift(3)
            # wait a bit.....
            time.sleep(0.05)

        update(s.bytearray)  # send all data to the matrix collection
        
        await asyncio.sleep(0.25)


try:

    # Set up the day tuple
    day = ("Mon", "Tue", "Wed", "Thr", "Fri", "Sat", "Sun")
    
    # Initialise the sure 3208 LED matrix.
    # The list contains the physical GPIO pins that each matrix has a CS pin connection to, then general commands to initialise the devices with
    s = Sure3208(WR_PIN, DATA_PIN, [4, 5, 6], [SYS_EN, LED_On, RC_Master_Mode, PWM_DUTY_10])

    led.on()
    print("Login")
    wifi_login()
    print("Login complete")
    led.off()

    asyncio.create_task(asyncio.start_server(serve_client, "0.0.0.0", 80))
    print('Setting up webserver...')
    led.on()
    
    set_machine_rtc()
    s.weather = weather()
    print(s.weather)
    asyncio.run(main())

finally:
    asyncio.new_event_loop()



