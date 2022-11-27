import time
from rpi_ws281x import PixelStrip, Color
import strandtestc as s
import random
import ledLIB as m


# LED strip configuration:
LED_COUNT = 70        # Number of LED pixels.
LED_PIN = 18          # GPIO pin connected to the pixels (18 uses PWM!).
# LED_PIN = 10        # GPIO pin connected to the pixels (10 uses SPI /dev/spidev0.0).
LED_FREQ_HZ = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA = 10          # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 255  # Set to 0 for darkest and 255 for brightest
LED_INVERT = False    # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53
strip = PixelStrip(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
# Intialize the library (must be called once before other functions).
strip.begin()
# Setter opp forkjelige verdier.
MAP, SIDES, data, testColor = m.setup(LED_COUNT,strip)

#Gamal funkjson som ikkje er viktig.
stripColor = []
for i in range(strip.numPixels()):
    stripColor.append(Color(0,0,0))
st = (strip, stripColor)    
for i in SIDES:
    stripColor = m.setSideColor(st, SIDES[i], testColor[i])

#Sørgjer for at led stripa er svart når vi starter
m.colorWipe(strip, Color(0,0,0))

#Main loop
while True:
    #Regnbue effekt
    while True:
        if not m.rainbow(strip, MAP, wait_ms=50): break # Skjer når knappen er
        #trykkt og gjer at vi går ut av denne loopen og går til neste
    toggle = True # er for å kjøre eine efekten ein gong og ikkje fleire i neste loop
    while True:
        if toggle:
            if m.colorWipeD(strip, MAP, Color(0,0,0)): break
            toggle = False
        if m.colorWipeD(strip, MAP, Color(255, 0, 0)): break
        if m.colorWipeD(strip, MAP, Color(0, 255, 0)): break
        if m.colorWipeD(strip, MAP, Color(0, 0, 255)): break
    #Alle under er vare fokjelige effekts
    while True:
        if m.rainbowSS(strip,MAP): break
    m.sRandom(strip)
    while True:
       if m.ssRandom(strip, wait_ms=250): break
    m.colorWipe(strip, Color(0,0,0))
    while True:
        if m.rainboww(strip,MAP): break
    m.colorWipe(strip, Color(0,0,0))
    while True:
        if m.testS(strip, MAP): break
    m.colorWipe(strip, Color(0,0,0))
    while True:
        if m.newRs(): break