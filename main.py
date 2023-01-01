from sure3208SPI import *
from font import *  # import all fonts in the font file
import machine
import time

import network
from urequests import get
import uasyncio as asyncio
import json

# On board LED used for diagnostics. Pico W specific
led = machine.Pin("LED", machine.Pin.OUT)


def wifi_login():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.config(pm = 0xa11140) # power saving mode off
    wlan.connect('WIFISSID', 'PASSWORD')
    s.defaults()
    while not wlan.isconnected() and wlan.status() >= 0:
        s.fill(0)  # empty instance bytearray
        s.render("Connecting..")  # write text to the framebuffer
        s.update(1)
        #update(s.bytearray)  # send all data to the matrix collection
        time.sleep(0.5)
        s.fill(0)  # empty instance bytearray
        s.render("------------")  # write text to the framebuffer
        s.update(1)
       # update(s.bytearray)  # send all data to the matrix collection
        time.sleep(0.5)

    status = wlan.ifconfig()
    print('ip = ' + status[0])
    s.fill(0)  # empty instance bytearray
    s.render(status[0])  # write text to the framebuffer
    s.update(1)
    time.sleep(2)

async def serve_client(reader, writer):
    
    # HTML Page to deliver
    
    html = """<!DOCTYPE html><html><head>
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Pico W LED Matrix</title>
</head>
<body>
<h1>Pico LED Matrix Messeger</h1>
<br>
  Font:




</p>
  <form action="#" method="post" enctype="multipart/form-data">

<input type="radio" id="8x5" name="font" value="f8x5" checked = checked>
<label for="html">Simple 8x5</label><br>
<input type="radio" id="spectrum" name="font" value="spec">
<label for="html">Spectrum</label><br>
<input type="radio" id="digital" name="font" value="digi">
<label for="html">Digital</label><br>

    <br>

        Message:
        <br>
        <input type="text" name="message">
        
        <button type="submit" formmethod="GET">
          Upload 
        </button>
        <br>

    </form>
    <br>
     <br>
     <form action="#" method="post" enctype="multipart/form-data">
     <input type="range" min="1" max="16" value="10" name = "slider">

        <button type="submit" formmethod="GET">
          Set Brightness 
        </button>

     </form>
     
     </form>

     
      <form action="#" method="post" enctype="multipart/form-data">
      <input type="hidden" name="weather">
        <br>
        <button type="submit" formmethod="GET">
          Weather Report
        </button>

     </form>

     
         <form action="#" method="post" enctype="multipart/form-data">
      <input type="hidden" name="btc">
        <br>
        <button type="submit" formmethod="GET">
          BTC Price
        </button>

     </form>
     <br>
     
     <form action="#" method="post" enctype="multipart/form-data">
      <input type="hidden" name="clock">

        <button type="submit" formmethod="GET">
          Set to Clock
        </button>

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
    print(request)
    m_rec = ""
    try:
        if request.index("GET") != -1:
            mstart = request.index("GET")+5
            mend = request.index("HTTP")
            m_rec = request[mstart:mend]
            m_rec = m_rec.replace("+", " ")

        else:
            pass
            #print("No Message")

    except ValueError:
        pass
        #print("Not found!")

    response = html
    writer.write('HTTP/1.0 200 OK\r\nContent-type: text/html\r\n\r\n')
    writer.write(response)

    await writer.drain()
    await writer.wait_closed()
    #print("Client disconnected")

    print(m_rec)
    print(m_rec[7:11])
    print(m_rec[11:18])
    old_message = s.message
    old_scroll = s.scroll
    if m_rec[0] =="?":
        if m_rec[1:5]=="font":
            if m_rec[6:10]=="f8x5":
                s.font = font_8x5
            if m_rec[6:10]=="spec":
                s.font = font_spectrum
            if m_rec[6:10]=="digi":
                s.font = font_digital
        if m_rec[11:18]=="message":
            
            m_rec =  m_rec[19:]
            m_rec = parse_url(m_rec)
            print(m_rec)
            s.message = m_rec
            s.scroll = 0
            old_message = s.message
            old_scroll = s.scroll
        # set message and reset scroll value



        # override if it's a command word
        if m_rec[1:6] == "clock":
            s.message = ""
            s.scroll = 0
        
        if m_rec[1:8]=="weather":
            s.font = font_spectrum
            s.message = weather()
            s.scroll = 0
            s.delay =0
            s.countdown = 500
        
        if m_rec[1:4]=="btc":
            s.font = font_spectrum
            s.message = BTC()
            s.scroll = 0
            s.delay =0
            s.countdown = 500
            

            

        if m_rec[1:7]=="slider":
            s.message = old_message
            s.scroll = old_scroll
            bright = int(m_rec[8:])
            print(bright)
          
            s.brightness(bright)
            
                
        if s.message !="":      
            s.render(s.message)




def get_json_time():
    # get the time from the network
    r = get("https://worldtimeapi.org/api/timezone/Europe/London")
    t = r.json()
    return t

# set the internal RTC time for the pico
def set_machine_rtc():
    t = get_json_time()
   
   
    print(t["datetime"])
   
    current = t["datetime"]

       # Note! It seems the month and day are reversed, not correct in the official docs??
   
    
    day =int(current[8:10])
    month =int(current[5:7])
    year = int(current[:4])
    day_of_week = int(t["day_of_week"])
    day_of_year = int(t["day_of_year"])
    hours =int(current[11:13])
    mins =int(current[14:16])
    secs = int(current[17:19])
    
#     print(day)
#     print(month)
#     print(year)
#     print(hours)
#     print(mins)
#     print(secs)
#     print(day_of_week)
#     print(day_of_year)

    machine.RTC().datetime((year,month,day,1, hours,mins,secs,0))  # 1 is day of week, but RTC will fix it....
    
    #print(machine.RTC().datetime())
    
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


def BTC():
    BTC = ""
    
    try:
        
        r = get("https://api.coindesk.com/v1/bpi/currentprice.json")
        parsed = r.json()
        rate =str(parsed["bpi"]["GBP"]["rate"])
        btc_rate = rate.split('.', 1)[0]
        BTC = "BTC: £" + btc_rate
        
    except Exception as e:
        BTC = "Failed to get BTC"
    
    return BTC

def weather():
    weather = ""
    #print("Weather trying...")
    try:
        # get the weather - use your own API and location
        #                                                   API*******************************API
        #print("Weather get")
        r = get("http://api.weatherapi.com/v1/current.json?key=d4a8ae03607f4016942172600222107&q=YOURCITY%20UK")
        #print("Weather got")
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
        weather = "Temp: "+ temp +" C  "+ condition + "  Precip:" +precip+" mm  Wind: "+wind + " kph "+wind_dir+"  Cloud %: "+cloud+"  UV lvl: "+uv 
        #print(weather)
        # times to scroll before returning to the clock
        #s.weather = weather
       # s.countdown = 5*32*s.num_screens # 5 scrolls is enough to get the data once and a bit on 3 screens
    except Exception as e: 
        # It didn't work :(
        weather = "Weather Failed"
        
        if weather_now != "Weather Failed":
            weather = weather_now
        
        
        print(str(e))
       # s.countdown = 10 # short message
    return weather




def login_wifi():
    wifi_login()
    asyncio.create_task(asyncio.start_server(serve_client, "0.0.0.0", 80))
    print('Setting up webserver...')
    led.on()
    set_machine_rtc()






async def main():
    # Set up some variables
    
    while True:
        # check if we're still connected to the network....
        wlan = network.WLAN(network.STA_IF)
        while not wlan.isconnected():
            # if we're not, log back in
           login_wifi()

        # Set up the time to display
        current_time = time.localtime()
        if current_time[5] % 2 ==0:
            colon ="g"
        else:
            colon = " "
        display_time = str(current_time[3]) + colon + str(current_time[4]) + colon + str(current_time[5]) + " " + str(
            current_time[2]) + "/" + str(current_time[1])
    
      
        if s.message != "":
            
            s.delay =0
            if s.countdown>0:
               
                s.countdown = s.countdown-1
            
            if s.countdown==1:
                
                s.message = ""
                s.countdown =0
            #s.justify = 1
            #s.render(s.message)
           
        else:
            # write a clock out
            s.fill(0)
            s.scroll = 0
            s.justify =3
            if int(current_time[5]) % 2 ==0:
                colon =":"
            else:
                colon = " "
            clock_text = "  "+str(day[current_time[6]]) + "    " +str(lead_zero(str(current_time[3]),2))+colon+str(lead_zero(str(current_time[4]), 2))+colon+str(lead_zero(str(current_time[5]), 2)) + "   " + str(lead_zero(str(current_time[2]), 2))+ "/" + str(lead_zero(str(current_time[1]), 2))
            s.defaults()
            s.font = font_8x5

            #s.render(str(wlan.status())+ " " +str(wlan.isconnected())+ " " +clock_text)
            s.render(clock_text)
            if wlan.status() != 3:
                wlan.disconnect()
            # if we're not, log back in
                login_wifi()

        s.update(1)   # 1 = scroll only if long, 0 = no scroll, 2 = forced scroll
        
        await asyncio.sleep(0.01)


try:

    # Set up the day tuple
    day = ("Mon", "Tue", "Wed", "Thr", "Fri", "Sat", "Sun")
    
    # Initialise the sure 3208 LED matrix.
    # The list contains the physical GPIO pins that each matrix has a CS pin connection to, then general commands to initialise the devices with
  # From the Sure 3208 module, these are GPIO pins on the pico/ picoW
    WR_PIN = 18
    DATA_PIN = 19

    # init the matrix                     Matrix CS pins       CMDs for init
    s = sure3208(
        WR_PIN, DATA_PIN, font_8x5, [17,20,15], [sure3208.SYS_EN, sure3208.LED_On, sure3208.RC_Master_Mode, sure3208.PWM_DUTY_10]
    )


    led.on()
    print("Login")
    wifi_login()
    print("Login complete")
    led.off()

    asyncio.create_task(asyncio.start_server(serve_client, "0.0.0.0", 80))
    print('Setting up webserver...')
    led.on()
    
    set_machine_rtc()
    print('Set RTC')
    weather_now = weather()
    print(weather_now)
    s.countdown =0

    asyncio.run(main())

finally:
    asyncio.new_event_loop()

