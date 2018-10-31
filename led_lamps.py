import gc

import globals
import time

# Fill all LEDs with one color (usually for turning them off)
def fill(color):

    globals.np.fill(color)

# Thread that runs through animation data and updates np list
def redraw_thread():

    globals.frameTime = time.ticks_ms()
    np = globals.np
    config = globals.config

    enum = list(enumerate(globals.strip_data))

    while globals.redraw_active:

        for index, strip in enum:
            if strip["animation_name"] == "blink":
                blink(np, config, index, strip["animation_data"])

        np.write()

        gc.collect()
        print(gc.mem_free())

        frameTime = time.ticks_diff(time.ticks_ms(), globals.frameTime)

        if frameTime <= 1000/config["frameRate"]:
            time.sleep_ms(int(1000/config["frameRate"]) - frameTime)


        globals.frameTime = time.ticks_ms()

#
# ANIMATION FUNCTIONS
#

# Simple blink function
# Fades from given color to black and back
def blink(np, config, strip_number, animation_data, half=True, pulse=False):

    if not "quotient" in animation_data:
        # We take maximum component of color and we find a number by which max component should be divided
        # n times (depending on framerate and animation time) to get n/4.
        # In other words, max/(x^15) = max/4 (15 is in case when frame rate is 30 and animation time is 1 sec, or 0.5 sec for each transition)
        # x^15 = 4
        # x = 4^(1/15)
        # We divide all components by this number to get smooth transition without changing base color
        animation_time = animation_data["speed"]

        quotient = 4. ** (1000. / (config["frameRate"] * animation_time ))

        animation_data["quotient"] = quotient

        current_color = animation_data["color"]

        animation_data["frames"] = [current_color]

        frameCount = int(config["frameRate"] * animation_time / 2000)
        animation_data["frameCount"] = frameCount


        for i in range(0, frameCount):
            current_color = (current_color[0]/quotient, current_color[1]/quotient, current_color[2]/quotient)
            animation_data["frames"].append(
                (
                    config["gamma"][int(current_color[0])],
                    config["gamma"][int(current_color[1])],
                    config["gamma"][int(current_color[2])]
                )
            )





    # When direction is true the animation goes from black to the original color
    if not "direction" in animation_data:
        animation_data["direction"] = False
    direction = animation_data["direction"]

    if not "position" in animation_data:
        animation_data["position"] = 0
    position = animation_data["position"]

    if direction and position == 0:
        direction = False

    if (not direction) and position >= animation_data["frameCount"] - 1:
        direction = True

    animation_data["direction"] = direction

    color = animation_data["frames"][position]


    stripColor = [0] * 3
    stripColor[np.ORDER[0]] = color[0]
    stripColor[np.ORDER[1]] = color[1]
    stripColor[np.ORDER[2]] = color[2]
    stripColor = bytearray(stripColor * config["stripLength"])
    np.buf[strip_number * config["stripLength"] * np.bpp : (strip_number + 1) * config["stripLength"] * np.bpp] = stripColor

    position = position - 1 if direction else position + 1
    animation_data["position"] = position

    del stripColor

    gc.collect()
