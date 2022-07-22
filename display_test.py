import machine
import time

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
        # message to display is held in the instance as is the scroll shift value. Minus values shift to the left.
        self.message = ""
        self.bytes_buffer = bytearray(1)
        self.justify = 1 # justify mode. 0 is none (left justify), 1 = centre (default) 2 = right !!!RIGHT NOT IMPLEMENTED YET!!!
        self.scroll = 0
        self.scroll_direction = -1  # -1 = left by 1
        self.delay = -1   # -1 is auto mode
        self.delay_auto = (4-(self.num_screens))*(0.02)
        
       
        # Now apply all the startup CMD's to all the screens
        for f in range(len(self.cs)):
            for t in range(len(self.cmds)):
                self.send_data(self.cmds[t], f, 12)

            self.cs[f].on()

    def send_data(self, bits, screen, length):
        # send binary data to device bit by bit

        # Go through bits and put them in a list (the right way round)
        bit_list = [(bits >> shift_index) & 1 for shift_index in range(length)]
        #bit_list.reverse()

        self.cs[screen].off()  # prepare the matrix for data

        for bit in bit_list[::-1]:  # loop through the bits from the data

            #value_when_true if condition else value_when_false
            self.data.on() if bit==1 else self.data.off()

#             if bit == 1:  # set the data pin to the bit data
#                 self.data.on()
#             else:
#                 self.data.off()

            self.wr.off()  # cycle the WR pin to set the bit
            self.wr.on()

        self.cs[screen].on()  # close the matrix for data

    def render(self, text):
        # were going to render the text to a full bytes buffer
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
               
               
        b=b >> 8 # to remove the last space put on after the last character
        length = length-1
        # make bytes_val the bytes to write to the matrix
        bytes_val = b.to_bytes(length, 'big')
        
        
        if len(bytes_val)> (self.num_screens*32):

            # it's going to scroll. Add spaces at the end
            a = bytearray(8)
            bytes_val = bytes_val + a
            
           
       
        self.bytes_buffer = bytes_val
       
       
        if len(bytes_val)> (self.num_screens*32):
            pass

        else:

            # it will fit. justify the text by creating a blank full screen
            # and adding the bytes to it so it can be scrolled with lots of
            # blank space
            new_b =bytearray(self.num_screens*32)
           
            if self.justify ==0:
                scroll = 0
                for byt in self.bytes_buffer:
                    new_b[scroll] = byt
                    scroll = scroll+1
            if self.justify ==1:
                scroll = int(((s.num_screens * 32) - len(bytes_val)) / 2)
                for byt in self.bytes_buffer:
                    new_b[scroll] = byt
                    scroll = scroll+1
           
            if self.justify ==2:
                scroll = int((s.num_screens * 32) - len(bytes_val)) 
                for byt in self.bytes_buffer:
                    new_b[scroll] = byt
                    scroll = scroll+1
                    
            if self.justify ==3:
                
                scroll = self.scroll
                
                for byt in self.bytes_buffer:
                    if scroll>(self.num_screens*32):
                        scroll =scroll-(self.num_screens*32)
                    
                    if scroll<len(self.bytearray):
                        new_b[scroll] = byt
                    scroll = scroll+1
                    
                    
                    
            bytes_val = new_b
       
        # store all bytes in the instance buffer
        self.bytes_buffer = bytes_val
       
       
       
       
       
    def update_matrix(self):
        screen = 0
        # Command code for writing. Address at 0 because we're going to sequentially write to the whole matrix
        CMD = 0b1010000000  
        bytes_written_index = 0

        for t in self.bytearray:  # loop through every byte in the framebuffer - 32 X number of matrices

            bit_expand = CMD << 8  # add 8 bit slots

            # Get the bits from the byte so that we can easily reverse it
            bit_list = [(t >> shift_index) & 1
                        for shift_index in range(8)]  
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
                if screen < self.num_screens:  # only send if the matrix is in range
                    self.send_data(CMD, screen,266)  # send the CMD and data to the screen - 266 bits in all for a full matrix
                CMD = 0b1010000000  # reset the CMD to the start
                screen = screen + 1  # increment the screen number

            else:
                bytes_written_index = bytes_written_index + 1  # add one to the index to keep adding data to the CMD
                
                
                
        # delay for screens...        
        if self.delay !=0:
            delay = self.delay/1000
            if self.delay == -1:
                delay = self.delay_auto
        
            time.sleep(delay)

   
       
       
       
       
    def update(self,scroll_mode):
        # draw self.bytes_buffer to self.bytesarray
        
        for b in range(len(self.bytearray)):
            self.bytearray[b] = self.bytes_buffer[b]
           
        # if we're scrolling, then rotate the buffer
           
        if scroll_mode == 1 and len(self.bytes_buffer)> len(self.bytearray):
            # scroll only if the message is bigger than the screen
            self.rotate(self.scroll)
            #print("Scroll!")
            self.scroll= self.scroll+ self.scroll_direction
            
            if abs(self.scroll) == len(self.bytes_buffer):
                self.scroll=0
            
            
            
        if scroll_mode == 2 :
            # force scroll
            self.rotate(self.scroll)
        # 1 = scroll only if long, 0 = no scroll, 2 = forced scroll
       
       
        self.update_matrix()
       
       

       

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

    def rotate(self, value):
        # rotate the instance bytes_buffer by the value number of places.
        temp=bytearray(len(self.bytes_buffer))
        
        for f in range(len(self.bytes_buffer)):
            if (f+value)>len(self.bytes_buffer):
                temp[(f+value)-len(self.bytes_buffer)] = self.bytes_buffer[f]
            if (f+value)<0:
                temp[(f+value)+len(self.bytes_buffer)] = self.bytes_buffer[f]
                
                
                
            if (f+value)>=0 and (f+value)<len(self.bytes_buffer):
                temp[f+value] = self.bytes_buffer[f]
       
       
        
       
        for i in range(len(self.bytearray)):
            
                self.bytearray[i] = temp[i]
               
        
       

s = Sure3208(WR_PIN, DATA_PIN, [4,5,6], [SYS_EN, LED_On, RC_Master_Mode, PWM_DUTY_10])


s.fill(0)
s.justify =0 # center justify mode  0 = left, 1 = center, 2 = right 3 = none (set scroll manually for placement!)
s.render("Left Justify")
s.update(1)
time.sleep(3)

s.fill(0)
s.justify =1
s.render("Center Justify")
s.update(1)
time.sleep(3)

s.fill(0)
s.justify =2
s.render("Right Justify")
s.update(1)
time.sleep(3)

s.fill(0)
s.justify =3
s.scroll=3
s.render("Manual")
s.update(1)
time.sleep(1)

s.fill(0)
s.justify =3
s.scroll=25
s.render("Manual")
s.update(1)
time.sleep(1)

s.fill(0)
s.justify =3
s.scroll=15
s.render("Manual")
s.update(1)
time.sleep(1)

s.fill(0)
s.justify =3
s.scroll =0
s.scroll_direction = -1
s.render("long message scrolling to the left")
s.update(1)
time.sleep(1)

count =200
while count>1:
    s.update(1)
    count = count -1
    
s.fill(0)
s.justify =3
s.scroll =0
s.scroll_direction = 1
s.render("long message scrolling to the right")
s.update(1)
time.sleep(1)

count =200
while count>1:
    s.update(1)
    count = count -1
    
    
s.fill(0)
s.justify =1
s.render("Custom sprites")
s.update(1)
time.sleep(2)

s.fill(0)
s.justify =3
s.scroll = 0
s.scroll_direction = 1
s.render("¬ ......  .   ¬  . ... .  ¬   . . . . .  .. ")
time.sleep(1)
count =100
while count>1:
    #s.render("¬")
    s.update(1)
    count = count -1
    
s.fill(0)
s.justify =3
s.scroll = 0
s.scroll_direction = -1
s.render("` ......  .   `  . ... .  `   . . . . .  .. ")
time.sleep(1)
count =100
while count>1:
    #s.render("¬")
    s.update(1)
    count = count -1
    
s.fill(0)
s.justify =1
s.scroll =0
s.scroll_direction = -1
s.render("sure 3208 micropython driver for raspberry pi pico w by andy crook")
  
while 1:
    s.update(1) # 1 = scroll only if long, 0 = no scroll, 2 = forced scroll
