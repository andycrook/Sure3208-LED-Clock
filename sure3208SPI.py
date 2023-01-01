import machine
import time
import random

# Class for the Sure 3208 led single colour matrix
class sure3208:
    
    # CMD codes for the matrix
    SYS_DIS = 0b100_0000_0000_0_0000
    SYS_EN = 0b100_0000_0001_0_0000
    LED_Off = 0b100_0000_0010_0_0000
    LED_On = 0b100_0000_0011_0_0000
    BLINK_Off = 0b100_0000_1000_0_0000
    BLINK_On = 0b100_0000_1001_0_0000
    SLAVE_Mode = 0b100_0001_0000_0_0000
    RC_Master_Mode = 0b100_0001_1000_0_0000
    EXT_CLK_Mode = 0b100_0001_1100_0_0000
    COM_Option_1 = 0b100_0010_0000_0_0000
    COM_Option_2 = 0b100_0010_0100_0_0000
    COM_Option_3 = 0b100_0010_1000_0_0000
    COM_Option_4 = 0b100_0010_1100_0_0000
    PWM_DUTY_1 = 0b100_1010_0000_0_0000
    PWM_DUTY_2 = 0b100_1010_0001_0_0000
    PWM_DUTY_3 = 0b100_1010_0010_0_0000
    PWM_DUTY_4 = 0b100_1010_0011_0_0000
    PWM_DUTY_5 = 0b100_1010_0100_0_0000
    PWM_DUTY_6 = 0b100_1010_0101_0_0000
    PWM_DUTY_7 = 0b100_1010_0110_0_0000
    PWM_DUTY_8 = 0b100_1010_0111_0_0000
    PWM_DUTY_9 = 0b100_1010_1000_0_0000
    PWM_DUTY_10 = 0b100_1010_1001_0_0000
    PWM_DUTY_11 = 0b100_1010_1010_0_0000
    PWM_DUTY_12 = 0b100_1010_1011_0_0000
    PWM_DUTY_13 = 0b100_1010_1100_0_0000
    PWM_DUTY_14 = 0b100_1010_1101_0_0000
    PWM_DUTY_15 = 0b100_1010_1110_0_0000
    PWM_DUTY_16 = 0b100_1010_1111_0_0000
    
    
    
    def __init__(self, sck_pin, mosi_pin, font, cs_pin=[], CMDS=[]):
        # CS pins are given as a list in the initialisation of the instance
        # CMDS are also given as a list that are applied to all the matrices on startup
        self.cs = cs_pin
        self.cmds = CMDS

        # setup GPIO pins for the devices...
        for f in range(len(self.cs)):
            self.cs[f] = machine.Pin(cs_pin[f], machine.Pin.OUT)
        self.sck = machine.Pin(sck_pin, machine.Pin.OUT)
        self.mosi = machine.Pin(mosi_pin, machine.Pin.OUT)

        # remember number of screens from CS list
        self.num_screens = len(self.cs)
        # Setup a bytearray to hold data for the screens
        self.bytearray = bytearray(len(self.cs) * 32)
        self.length = len(self.cs) * 32 # so we don't have to calculate it
        self.render_position = 0
        
        
        # message to display is held in the instance as is the scroll shift value. Minus values shift to the left.
        self.message = ""
        self.bytes_buffer = bytearray(self.length)
        self.font = font
       
        print("SPI Done")
        for f in range(len(self.cs)):
            for t in range(len(self.cmds)):
                self.send_CMD(self.cmds[t]>>4) # remove last 4 bits for 12 bit bit banging
            self.cs[f].on()
                  
        print("Screens ready")
        
        
        self.spi=machine.SPI(0,baudrate=50000000, polarity=0, phase=0, bits=8, sck=machine.Pin(sck_pin), mosi=machine.Pin(mosi_pin))  # no miso, we don't need to read
        self.defaults()
        
        
    def cmd_write(self, data,cs_pin):

            self.spi_write(data, cs_pin, 2)
            self.pulse()
            
            
    def pulse(self):
        self.sck.off()
        self.sck.on()
        
        
    def spi_write(self, data, cs_pin, length):

#       
#         print("SPI DATA: PIN - "+str(cs_pin) + "  LENGTH: " + str(length))
#         data_str = "{0:b}".format(data)
#         data_str = str(data_str)
#         new_data = ""
#         count=-2
#         for c in data_str:
#             new_data = new_data+c
#             count+=1
#             if count==8:
#                 count=0
#                 new_data = new_data+" "
#         print(new_data)
        #length = length*2
        
        self.cs[cs_pin].off()
        self.spi.write(data.to_bytes(length, 'big'))   
        self.cs[cs_pin].on()
        
        self.pulse()
      
    def send_data(self, bits, screen, length):
        # send binary data to device bit by bit

        # Go through bits and put them in a list (the right way round)
        bit_list = [(bits >> shift_index) & 1 for shift_index in range(length)]
        bit_list.reverse()
        #print("BITLIST")
        #print(bit_list)
        self.cs[screen].off()  # prepare the matrix for data

        for bit in bit_list:  # loop through the bits from the data in reverse
            # set the data pin for the bit
            self.mosi.on() if bit == 1 else self.mosi.off()
            # cycle the WR pin to set the bit in teh matrix
            self.sck.off()
            self.sck.on()
        self.cs[screen].on()  # close the matrix for data
            
    def send_CMD(self,bits):
        for f in range(self.num_screens):
            self.send_data(bits, f, 12)
            
    def set_bright(self,data):
        for f in range(self.num_screens):
            self.cmd_write(data,f)
            
    def brightness(self,value):
        if value == 1:
            self.set_bright(self.PWM_DUTY_1)
        if value == 2:
            self.set_bright(self.PWM_DUTY_2)
        if value == 3:
            self.set_bright(self.PWM_DUTY_3)
        if value == 4:
            self.set_bright(self.PWM_DUTY_4)
        if value == 5:
            self.set_bright(self.PWM_DUTY_5)
        if value == 6:
            self.set_bright(self.PWM_DUTY_6)
        if value == 7:
            self.set_bright(self.PWM_DUTY_7)
        if value == 8:
            self.set_bright(self.PWM_DUTY_8)
        if value == 9:
            self.set_bright(self.PWM_DUTY_9)
        if value == 10:
            self.set_bright(self.PWM_DUTY_10)
        if value == 11:
            self.set_bright(self.PWM_DUTY_11)
        if value == 12:
            self.set_bright(self.PWM_DUTY_12)
        if value == 13:
            self.set_bright(self.PWM_DUTY_13)
        if value == 14:
            self.set_bright(self.PWM_DUTY_14)
        if value == 15:
            self.set_bright(self.PWM_DUTY_15)
        if value == 16:
            self.set_bright(self.PWM_DUTY_16)

    def render(self, text, *app):
        # were going to render the text to a full bytes buffer
        b = 0
        if len(app)>0:
            append = 1
        else:
            append=0
        #print(len(app))
        #print(append)

        length = 0
        
        # write all characters to b
        for character in text:
            try:
                b = self.write_chr(b, self.font[character])
                length = length + 1 + len(self.font[character])
            except:
                # is there an upper case variant? Check.... default should be upper for a font...
                try:
                    b = self.write_chr(b, self.font[character.upper()])
                    length = length + 1 + len(self.font[character.upper()])
                except:

                    print("CHR NOT FOUND")
        b = b >> 8  # to remove the last space put on after the last character
        length = length - 1
        # make bytes_val the bytes to write to the matrix
        bytes_val = b.to_bytes(length, "big")

        
            
        if append==0:
            
            if len(bytes_val) > (self.length):

            # it's going to scroll. Add spaces at the end
                a = bytearray(8)
                
                bytes_val = bytes_val + a

            self.bytes_buffer = bytes_val
        else:
            #print("APPENDING")
            self.bytes_buffer = self.bytes_buffer+ bytearray(len(bytes_val))
            st_data = -1
            en_data = -1
            
            for f in range(len(self.bytes_buffer)):
                if self.bytes_buffer[len(self.bytes_buffer)-f-1]!=0:
                    # found first non blank
                    if en_data == -1:
                        en_data = len(self.bytes_buffer)-f+1
            for f in range(len(self.bytes_buffer)):
                if self.bytes_buffer[f]!=0:
                    # found first non blank
                    if st_data == -1:
                        st_data = f
            
            bytes_val = self.bytes_buffer[st_data:en_data] + bytes_val
            
            #print(self.bytes_buffer)
            #print (bytes_val)
            #bytes_val = self.bytes_buffer[:]+ bytes_val[:]
            
            #print (bytes_val)
            
            
            if len(bytes_val) > (self.length):

            # it's going to scroll. Add spaces at the end
                a = bytearray(8)
                bytes_val = bytes_val + a
                
            self.bytes_buffer = bytes_val
        
        if len(bytes_val) > (self.length):
            pass
        else:

            # it will fit. justify the text by creating a blank full screen
            # and adding the bytes to it so it can be scrolled with lots of
            # blank space
            new_b = bytearray(self.length)

            if self.justify == 0:
                scroll = 0
                for byt in self.bytes_buffer:
                    new_b[scroll] = byt
                    scroll = scroll + 1
            if self.justify == 1:
                scroll = int(((self.length) - len(bytes_val)) / 2)
                for byt in self.bytes_buffer:
                    new_b[scroll] = byt
                    scroll = scroll + 1
            if self.justify == 2:
                scroll = int((self.length) - len(bytes_val))
                for byt in self.bytes_buffer:
                    new_b[scroll] = byt
                    scroll = scroll + 1
            if self.justify == 3:

                scroll = self.scroll

                for byt in self.bytes_buffer:
                    # shift scroll to be within ranbge of screen
                    while scroll > (self.length):
                        scroll = scroll - (self.length)
                    while scroll < 0:
                        scroll = scroll - (self.length)
                    # check if it's in bounds
                    if scroll > -1 and scroll < len(self.bytearray):
                        new_b[scroll] = byt
                    scroll = scroll + 1
            bytes_val = new_b
        # store all bytes in the instance buffer
        self.bytes_buffer = bytes_val

    def delay_matrix(self):
        # delay for screens...
        if self.delay != 0:
            delay = self.delay / 1000
            if self.delay == -1:
                delay = self.delay_auto
            time.sleep(delay)


    def update_matrix(self):
        screen = 0
        # Command code for writing. Address at 0 because we're going to sequentially write to the whole matrix
        self.delay_matrix()

        CMD =  0b101_0000_000
        
        bytes_written_index = 0
        aa=0
        for t in self.bytearray:
            # loop through every byte in the framebuffer - 32 X number of matrices

            bit_expand = CMD << 8  # add 8 bit slots

            # Get the bits from the byte so that we can easily reverse it
            bit_list = [(t >> shift_index) & 1 for shift_index in range(8)]
            bit_list.reverse()
            
            if aa==0:
                aa=1
                first_byte = bit_list
                #first_byte.reverse()
            # reverse to big endian for the sure 3208 matrix. Comment out this line if your text appears upside down!

            # get the bits and reconstruct it into an 8 bit byte
            a = 0
            for bit in bit_list:
                a = (a << 1) | bit
            # add the 8 bit byte to the command code
            CMD = bit_expand | a

            if (
                bytes_written_index == 31
            ):  # we have written 0 - 31 bytes, so the matrix is full. Send the data to the screen
                bytes_written_index = 0  # reset the bytes index to 0
                if screen < self.num_screens:  # only send if the matrix is in range
                    
                    # when writing a full frame, SPI overwrites the first nibble. Reconstruct
                    CMD = CMD <<6
                    nibble=0
                    n = 32
                    #print(first_byte)
                    for gg in range(4):
                        if first_byte[gg]==1:
                            nibble = nibble + n
                        n=n/2
                    
                    #print(nibble)
                    aa=0
                    CMD = CMD | int(nibble)
                    #CMD = CMD <<6
                    #print(screen)
                    #print(CMD.to_bytes(34, 'big'))
                    #print(CMD)
                    #print("{0:b}".format(CMD))
                    self.spi_write(CMD, screen, 34)  # send the CMD and data to the screen - 266 bits in all for a full matrix
                CMD = 0b101_0000_000  # reset the CMD to the start
                screen = screen + 1  # increment the screen number
            else:
                bytes_written_index = (
                    bytes_written_index + 1
                )  # add one to the index to keep adding data to the CMD
            # delay for screens...
        
            
            
            


    def update(self, scroll_mode):
        # draw self.bytes_buffer to self.bytesarray

        
        self.bytearray[:] = self.bytes_buffer[:self.length]
            
            
            
        if self.vertical != 0:

            self.vertical_shift(self.vertical)
        # if we're scrolling, then rotate the buffer
        # 1 = scroll only if long, 0 = no scroll, 2 = forced scroll
        if scroll_mode == 1 and len(self.bytes_buffer) > self.length:
            # scroll only if the message is bigger than the screen
            self.rotate(self.scroll)
            # print("Scroll!")
            self.scroll = self.scroll + self.scroll_direction
            
            if self.scroll> len(self.bytes_buffer) :
                self.scroll = self.scroll - len(self.bytes_buffer)
            if self.scroll<(len(self.bytes_buffer)*-1):
                self.scroll = self.scroll + len(self.bytes_buffer) 
            
            if abs(self.scroll) == len(self.bytes_buffer):
                self.scroll = 0
        if scroll_mode == 2:
            # force scroll
            self.rotate(self.scroll)
        self.update_matrix()

    def vertical_shift(self, value):
        self.delay_matrix() # extra delay
        if value < 0:
            value = value * -1
            for byte in range(self.length):
                self.bytearray[byte] = (self.bytearray[byte] >> value) & 255
        else:
            for byte in range(self.length):
                self.bytearray[byte] = (self.bytearray[byte] << value) & 255
        

    def matrix_rain(self, value1, value2):
        self.vertical_shift(-1)

        for byte in range(self.length):
            if random.randrange(value1) == 1 or self.bytearray[byte] >= 64:
                self.bytearray[byte] = self.bytearray[byte] | 128
                if random.randrange(value2) == 1 and self.bytearray[byte] > 127:
                    self.bytearray[byte] = self.bytearray[byte] - 128
        
    
    def defaults(self):
        # set some basic defaults for the matrix so we can call it easily
        self.fill(0)
        self.justify = 1  # justify mode. 0 is none (left justify), 1 = centre (default) 2 = right !!!RIGHT NOT IMPLEMENTED YET!!!
        self.scroll = 0
        self.scroll_direction = 1  # -1 = left by 1
        self.delay = -1  # -1 is auto mode
        self.delay_auto = (4 - (self.num_screens)) * (0.02)
        self.vertical = 0
        #self.brightness(10)
        self.countdown = 0
        
    def write_chr(self, by, c):
        # c is a list of binay data to add to by and returns it
        for font_bytes in c:
            by = by << 8
            by = by | int(font_bytes)
        by = by << 8  # This creates a single blank line between the characters
        return by

    def fill(self, value):
        # fill the matrix with a value - usually 0 to blank the display before writing
        for byt in range(self.length):
            self.bytearray[byt] = value
            #self.bytes_buffer[byt] = value
            
    def new_buffer(self, value):
        # fill the matrix with a value - usually 0 to blank the display before writing
        
        self.bytes_buffer = bytearray(self.length)
        for byt in range(len(self.bytes_buffer)):
            self.bytes_buffer[byt] = value 
            
    def set_pixel(self,x,y,value):
        # 0 = set a pixel to off, 1 to on, and 2 to invert
        inv_y = 8-(y+1)
        if value==1:
            self.bytes_buffer[x] = self.bytes_buffer[x] | (2** inv_y)
        elif value ==0:
            self.bytes_buffer[x] = ~self.bytes_buffer[x]
            self.bytes_buffer[x] = self.bytes_buffer[x] | (2** inv_y)
            self.bytes_buffer[x] = ~self.bytes_buffer[x]
        elif value ==2:
            self.bytes_buffer[x] = self.bytes_buffer[x] ^ (2** inv_y)
            
    def invert(self):
        for b in range(len(self.bytes_buffer)):
            self.bytes_buffer[b] = ~self.bytes_buffer[b]
            
    def draw_rect(self,x,y,width,height,fill,value):
        if fill ==1:
            for xx in range(x, x+width):
                for yy in range(y,y+height):
                    self.set_pixel(xx,yy,value)
        else:
            for xx in range(x, x+width):
                self.set_pixel(xx,y,value)
                self.set_pixel(xx,y+height-1,value)
                
            for yy in range(y+1,y+height-1):
                self.set_pixel(x,yy,value)
                self.set_pixel(x+width-1,yy,value)

    def rotate(self,value):
        if value>0:
            temp = self.bytes_buffer[value:] + self.bytes_buffer[:value]
            self.bytearray[:] = temp[: self.length]
        if value<0:

            inv_val = value*-1
            temp = self.bytes_buffer[len(self.bytes_buffer)-inv_val:] + self.bytes_buffer[:len(self.bytes_buffer)-inv_val]
            self.bytearray[:] = temp[: self.length]
 