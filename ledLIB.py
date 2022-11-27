import os
import math
import json
from rpi_ws281x import PixelStrip, Color
import RPi.GPIO as GPIO
import random
import time
import strandtestc as s

#Setter opp fokjelige verier
button = 23
GPIO.setmode(GPIO.BCM) 
GPIO.setup(button, GPIO.IN, pull_up_down=GPIO.PUD_UP)
testColor = (Color(0, 0, 255), Color(0, 255, 0), Color(0, 255, 255), Color(255, 0, 0), Color(255, 0, 255), Color(255, 255, 0))

#Er ein funkjson som setter opp fokjelige verdier, ikkje alle er relevante 
#siden koden endrea seg seinare.
def setup(LED_COUNT, strip):
    path = os.path.dirname(os.path.realpath(__file__))
    SETTINGFILE = path+"/settings.json" # setting file er ikkje brukt i den endlige koden

    #lager MAP som er ein liste med verdier som kartleger stipa. Dette er fordi stripa starter på led 5 og slutter på 4. for å kartlege så kjører man bare MAP[i] så vist i er 0 så får vi verdien 5 tilbake.
    maptemplate = (list(range(5,70)),list(range(0,5)))
    MAP = []
    for i in maptemplate:
        for j in i:
            MAP.append(j)   

    #Kartleger kvar side så vi kan ha ein farge. dette er fordi ikkje samme antal
    #led er på kvar side i hexagonen
    SIDES = {
        0: [64,65,66,67,68,69,70,0,1,2,3,4],
        1: list(range(5,17)),
        2: list(range(17,29)),
        3: list(range(29,40)),
        4: list(range(40,52)),
        5: list(range(52,64)),
    }
    r = ''
    with open(SETTINGFILE, "r") as file:
        r = file.read()
    data = json.loads(r)
    #leser data fra json fila og gjer dei om til farge veridar.
    for i in data:
        for j in range(len(data[i])):
            a = data[i][j]
            data[i][j] = Color(a[0], a[1], a[2])

    testColor = (Color(0, 0, 255), Color(0, 255, 0), Color(0, 255, 255), Color(255, 0, 0), Color(255, 0, 255), Color(255, 255, 0))
    return MAP, SIDES, data, testColor

#ein funkjson som leser av pin 23 for å sjå om knappen har vore trykka, 
#dette skjer med å sjå på kass verdi forgje hadde i forhold til den nye.
def newRs(ledLIBrsL = ""):
    e = bool(GPIO.input(button))
    if not ledLIBrsL == e:
        ledLIBrsL = e
        return True
    return False 

#skriver ein farge til led stripa
def colorWipe(strip, color):
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, color)
    show(strip)

#seter ein farge på ein side
def setSideColor(strip, side, color):
    stripColor = strip[1]
    strip = strip[0]
    for i in side:
        strip.setPixelColor(i, color)
        #stripColor[i] = color
    strip.show()
    return stripColor

#gjer det samme som setSideColor men bare for ein arrary.
def setPIXELarr(strip, side, color):
    for i in side:
        strip.setPixelColor(i, color)

# Swttwe randome farge på ledstipa.
def sRandom(strip, wait_ms=20):
    for led in range(strip.numPixels()):
        r = random.randint(0,50)
        g = random.randint(0,150)
        b = random.randint(0,255)
        strip.setPixelColor(led, Color(r,g,b))
    if show(strip): return True
    time.sleep(wait_ms / 1000.0)
# ein anna random funksjon. 
#(disse var for testing for å få eit klu på korleis vi skulle kode ledstripa)
def ssRandom(strip, wait_ms=50):
    l = list(range(strip.numPixels()))
    r = random.randint(0,50)
    g = random.randint(0,150)
    b = random.randint(0,255)
    led = random.choice(l)
    strip.setPixelColor(led, Color(r,g,b))
    if show(strip): return True
    time.sleep(wait_ms / 1000.0)

#Større funksjon som gjer randome effekt til lystripa. 
#(gamal ikkje i bruk lenger også ein test)
def setRandom(strip, color=False, wait_ms=50, c=False):
    l = list(range(strip.numPixels()))
    if not color:
        for led in range(strip.numPixels()):
            r = random.randint(0,50)
            g = random.randint(0,150)
            b = random.randint(0,255)
            strip.setPixelColor(led, Color(r,g,b))
        strip.show()
        while True:
            r = random.randint(0,50)
            g = random.randint(0,150)
            b = random.randint(0,255)
            led = random.choice(l)
            strip.setPixelColor(led, Color(r,g,b))
            strip.show()
            time.sleep(wait_ms / 1000.0)
    elif c:
        while True:
            for led in range(strip.numPixels()):
                colo = random.choice(color)
                strip.setPixelColor(led, colo)
            strip.show()
            time.sleep(wait_ms / 1000.0)            
    else:
        for led in range(strip.numPixels()):
            colo = random.choice(color)
            strip.setPixelColor(led, colo)
        strip.show()
        while True:
            colo = random.choice(color)
            led = random.choice(l)
            strip.setPixelColor(led, colo)
            strip.show()
            time.sleep(wait_ms / 1000.0)

#Gamal test funkjson.
def sideWheel(strip, side, color, SIDES, wait_ms=50):
    while len(color) < len(SIDES):
        color.append(Color(0,0,0))
    for i in range(len(SIDES)):
        setSideColor(strip, SIDES[i], color[i])
    lis = []
    for i, val in side.items():
        lis.append(val[-1])
        #strip.setPixelColor(i, color)
        #strip.show()
        #time.sleep(wait_ms / 1000.0)
    while True:
        for i in range(len(lis)):
            strip.setPixelColor(lis[i], color[i])
            if lis[i] < 72:
                lis[i] += 1
            else:
                lis[i] = 0
        strip.show()
        time.sleep(wait_ms / 1000.0)

#Står for å vise effekta samtidig som han leser av knappen
def show(strip):
    strip.show()
    return newRs()

#ein funkjson som er brukt for å flytte på nokon røde pixel i ein regnbue effekt
def clock3led(strip, color, MAP,t, arr=[1,2,3]):
    ar = []
    for i in range(len(arr)):
        ar.append(MAP[arr[i]])
    for i in range(len(arr)):
        arr[i] += t
        if arr[i] >= strip.numPixels():
            arr[i] = 0
    setPIXELarr(strip, arr, color)

# rainbow effekt med nokon pixler som beveger seg
def rainbow(strip, map, wait_ms=20, iterations=1):
    timee = 0
    for j in range(256 * iterations):
        for i in range(strip.numPixels()):
            strip.setPixelColor(map[i], s.wheel((i + j) & 255))
        #skjeker om det har gåt eit sekund. vist den har så flytter den pixlane 1
        #steg og setter tida til null igjen.
        if timee >= 1:
            clock3led(strip, Color(255,0,0), map,1)
            timee = 0
        else:
            clock3led(strip, Color(255,0,0), map,0)
        if show(strip): return False
        time.sleep(wait_ms / 1000.0)
        timee += wait_ms / 1000.0
    return True

#ein anna fungkjon som endrer fargen på ledstripa
def colorWipeD(strip, MAP, color, wait_ms=50):
    """Wipe color across display a pixel at a time."""
    for i in range(strip.numPixels()):
        strip.setPixelColor(MAP[i], color)
        if show(strip): return True
        time.sleep(wait_ms / 1000.0)

# regnbue effek
def rainbowS(strip, wait_ms=20, iterations=1):
    """Draw rainbow that fades across all pixels at once."""
    for j in range(256 * iterations):
        for i in range(int(strip.numPixels()/2)+1):
            strip.setPixelColor(i, s.wheel((i + j) & 255))
            strip.setPixelColor((strip.numPixels()-i), s.wheel(( + j) & 255))
        
        strip.show()
        time.sleep(wait_ms / 1000.0)

# Rengbue effekt som er splitta i miden. så han er spegla på midten
def rainbowSS(strip, MAP, wait_ms=50, iterations=1):
    for j in range(256):
        for i in range(int(strip.numPixels()/2)):
            strip.setPixelColor(MAP[i], s.wheel((i+j) & 255))
            strip.setPixelColor(MAP[strip.numPixels()-i-1], s.wheel((i+j) & 255))
        if show(strip): return True
        time.sleep(wait_ms / 1000.0)

#ein kul effekt som går gjennom dei forkjelige fargane i wheel funkjsonen.
def testS(strip, MAP):
    w = 0
    z = 0
    max = strip.numPixels()
    while True:
        if w > 0:
            strip.setPixelColor(MAP[w-1], Color(0,0,0))
        if w == 0: 
            strip.setPixelColor(max, Color(0,0,0))
        strip.setPixelColor(w, s.wheel(z))
        if show(strip): return True
        time.sleep(20 / 1000.0)
        if z < 255:
            z +=1
        else:
            z = 0
        if w < max:
            w +=1
        else:
            w = 0

#ein til regnbue effekt
def rainboww(strip, map, wait_ms=20, iterations=1):
    for j in range(256 * iterations):
        for i in range(strip.numPixels()):
            strip.setPixelColor(map[i], s.wheel((i + j) & 255))
        if show(strip): return True
        time.sleep(wait_ms / 1000.0)

#EIn effekt som aldri blei skikleg ferdig. er to ting som går att og 
#fram på led stripa og når dei trefer kverandre snur dei retning
def chASS(strip,wait_ms=50, c1=[-1,Color(255,0,0),[1,2,3]],c2=[1,Color(0,0,255),[10,11,12]]):

    if c1[0] > 0:
        strip.setPixelColor(c1[2][0], Color(0,0,0))
        strip.setPixelColor(c2[2][2], Color(0,0,0))
    else:
        strip.setPixelColor(c1[2][2], Color(0,0,0))
        strip.setPixelColor(c2[2][0], Color(0,0,0))
    for i in range(len(c1[2])):
        if c1[2][i] + c1[0] < 0:
            c1[2][i] = strip.numPixels()
        elif c1[2][i] + c1[0] > strip.numPixels():
            c1[2][i] = 0
        else:
            c1[2][i] += c1[0]
    for i in range(len(c2[2])):
        if c2[2][i] + c2[0] < 0:
            c2[2][i] = strip.numPixels()
        elif c2[2][i] + c2[0] > strip.numPixels():
            c2[2][i] = 0
        else:
            c2[2][i] += c2[0]

    if c1[2][0] in c2[2] or c1[2][2] in c2[2]:
        c1[0] = -c1[0]
        c2[0] = -c2[0]
    else:
        setPIXELarr(strip, c1[2], c1[1])
        setPIXELarr(strip, c2[2], c2[1])
        show(strip)