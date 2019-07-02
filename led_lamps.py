import globals
import time
import board
import digitalio
import neopixel
from neopixel_write import neopixel_write
import digitalio
import math
import random

from threading import Thread

def time_ms():

    return int(time.time()%1000*1000)

def sum_lengths(stripData, index):

    sum = 0

    for i in range(0, index):
        sum += stripData[i]["animation_data"]["zoneLength"] * stripData[i]["animation_data"]["stripLength"]

    return sum


# Thread that runs through animation data and updates np list
def redraw_thread(np, config, stripData):

    enum = list(enumerate(stripData))

    for index, strip in enum:
        strip["animation_data"]["offset"] = sum_lengths(stripData, index)

    pin = digitalio.DigitalInOut(board.D18)
    pin.direction = digitalio.Direction.OUTPUT

    msPerFrame = int(1000/config["frameRate"])

    while globals.redraw_active:
        frameStart = time_ms()

        for index, strip in enum:
            if strip["animation_name"] == "blink":
                blink(np, config, index, strip["animation_data"])
            if strip["animation_name"] == "blinkrng":
                blinkrng(np, config, index, strip["animation_data"])
            if strip["animation_name"] == "blink_solid":
                blink(np, config, index, strip["animation_data"], True, False, True)
            if strip["animation_name"] == "blinkrng_solid":
                blinkrng(np, config, index, strip["animation_data"], True, False, True)
            if strip["animation_name"] == "solid":
                solid(np, config, index, strip["animation_data"])

        # _thread.start_new_thread(neopixel_write, (machine.Pin(26), np.buf, 1))
        t = Thread(target=neopixel_write, args=(pin, np.buf))
        t.start()
        #np.show()
        #neopixel_write(pin, np.buf)

        frameTime = time_ms() - frameStart

        if frameTime < msPerFrame:
            time.sleep((msPerFrame - frameTime - 1)/1000)


#
# ANIMATION FUNCTIONS
#

#
# Solid color function
#
def solid(np, config, strip_number, animation_data):
    if not "drawn" in animation_data or not animation_data["drawn"]:
        animation_data["totalLength"] = animation_data["zoneLength"] * animation_data["stripLength"]
        current_color = animation_data["color"]
        color = [0] * 3
        color[np.order[0]] = config["gamma"][int(current_color[0])]
        color[np.order[1]] = config["gamma"][int(current_color[1])]
        color[np.order[2]] = config["gamma"][int(current_color[2])]
        while True:
            try:
                color = bytearray(color * animation_data["totalLength"])
                np.buf[animation_data["offset"] * np.bpp : (animation_data["offset"] + animation_data["totalLength"]) * np.bpp] = color
                animation_data["drawn"] = True
            except MemoryError:
                gc.collect()
                print("here")
                continue
            break
    if "flicker" in animation_data and animation_data["flicker"] and random.randint(0, 50) == random.randint(0, 50):
            l = random.randint(0, animation_data["zoneLength"] - 1)
            tl = animation_data["stripLength"] * l
            print (l, tl)
            color = bytearray((0,0,0) * animation_data["stripLength"])
            np.buf[(animation_data["offset"] + tl) * np.bpp : (animation_data["offset"] + tl + animation_data["stripLength"]) * np.bpp] = color
            animation_data["drawn"] = False

        

# Simple blink function
# Fades from given color to black and back
def blink(np, config, strip_number, animation_data, half=True, pulse=False, solid=False):

    if not "quotient" in animation_data or not animation_data["quotient"]:
        # We take maximum component of color and we find a number by which max component should be divided
        # n times (depending on framerate and animation time) to get n/4.
        # In other words, max/(x^15) = max/4 (15 is in case when frame rate is 30 and animation time is 1 sec, or 0.5 sec for each transition)
        # x^15 = 4
        # x = 4^(1/15)
        # We divide all components by this number to get smooth transition without changing base color
        animation_time = animation_data["speed"]
        animation_data["fullCycle"] = 0

        length = animation_data["zoneLength"] * animation_data["stripLength"]

        animation_data["totalLength"] = length

        # quotient = 8. ** (2000. / (config["frameRate"] * animation_time ))

        frameCount = int(config["frameRate"] * animation_time / 1000)
        animation_data["frameCount"] = frameCount

        current_color = animation_data["color"]
        color = [0] * 3
        color[np.order[0]] = config["gamma"][int(current_color[0])]
        color[np.order[1]] = config["gamma"][int(current_color[1])]
        color[np.order[2]] = config["gamma"][int(current_color[2])]
        color = bytearray(color) * length

        if solid:
            animation_data["frames"] = [color for _ in range (0, frameCount+1)]

        else:
            animation_data["frames"] = [color]

            startColor = max(animation_data["color"])

            stopColor = startColor*animation_data["quot"]


            for i in range(0, frameCount):
                quotient = 2 * startColor / (math.cos(i * math.pi / frameCount) * (startColor - stopColor) + startColor + stopColor)
                # current_color = (current_color[0]/quotient, current_color[1]/quotient, current_color[2]/quotient)
                color = [0] * 3
                color[np.order[0]] = config["gamma"][int(current_color[0] / quotient)]
                color[np.order[1]] = config["gamma"][int(current_color[1] / quotient)]
                color[np.order[2]] = config["gamma"][int(current_color[2] / quotient)]
                color = bytearray(color) * length

                animation_data["frames"].append(color)

        animation_data["quotient"] = True





    # When direction is true the animation goes from black to the original color
    if not "direction" in animation_data:
        animation_data["direction"] = False
    direction = animation_data["direction"]

    if not "position" in animation_data:
        animation_data["position"] = 0
    position = animation_data["position"]

    if direction and position == 0:
        direction = False
        animation_data["fullCycle"] += 1

        if solid:
            animation_data["fullCycle"] = 10

    if (not direction) and position >= animation_data["frameCount"] - 1:
        direction = True

    animation_data["direction"] = direction
    if "flicker" in animation_data and animation_data["flicker"] and random.randint(0, 100) == random.randint(0, 100):
        length = animation_data["zoneLength"] * animation_data["stripLength"]
        color = bytearray((0,0,0)) * length
    else:
        color = animation_data["frames"][position]
    np.buf[animation_data["offset"] * np.bpp : (animation_data["offset"] + animation_data["totalLength"]) * np.bpp] = color

    if direction:
        position -= 1
    else:
        position += 1

    animation_data["position"] = position

def blinkrng(np, config, strip_number, animation_data, half=True, pulse=False, solid=False):
    if not "fullCycle" in animation_data:
        animation_data["fullCycle"] = 0

    if animation_data["fullCycle"] >= 10:
        color = (0, 0, 0)
        while max(color) < 252:
            color = (random.randint(0,4) * 63, random.randint(0,4) * 63, random.randint(0,4) * 63)
        animation_data["speed"] = animation_data["speed"] if solid else random.randint(9, 36) * 200
        animation_data["color"] = color

        animation_data["quotient"] = False

    blink(np, config, strip_number, animation_data, half=half, pulse=pulse, solid=solid)
