import globals
import time

# Fill all LEDs with one color (usually for turning them off)
def fill(color):

    globals.np.fill(color)

# Thread that runs through animation data and updates np list
def redraw_thread():

    globals.frameTime = time.ticks_ms()
    while globals.redraw_active:

        for index, strip in enumerate(globals.strip_data):
            if strip["animation_name"] == "blink":
                blink(index, strip["animation_data"]["color"], strip["animation_data"]["speed"])

            if not strip["redrawn"] and not strip["stopRedraw"]:

                for led_index, color in enumerate(strip["LEDs"]):
                    int_color = (int(color[0]), int(color[1]), int(color[2]))
                    globals.np[int(index * globals.config["stripLength"] + led_index)] = int_color

                globals.strip_data[index]["redrawn"] = True

        globals.np.write()

        frameTime = time.ticks_diff(time.ticks_ms(), globals.frameTime)

        if frameTime <= 1000/globals.config["frameRate"]:
            time.sleep_ms(int(1000/globals.config["frameRate"]) - frameTime)

        globals.frameTime = time.ticks_ms()

# 
# ANIMATION FUNCTIONS
#

# Simple blink function
# Fades from given color to black and back
def blink(strip_number, color, time=1000, pulse=False):

    if globals.strip_data[strip_number]["redrawn"]:

        # When direction is true the animation goes from black to the original color
        if not "direction" in globals.strip_data[strip_number]["animation_data"]:
            globals.strip_data[strip_number]["animation_data"]["direction"] = False
        direction = globals.strip_data[strip_number]["animation_data"]["direction"]

        # We take maximum component of color and we find a number by which max component should be divided
        # n times (depending on framerate and animation time) to get 1.
        # In other words, max/(x^15) = 1 (15 is in case when frame rate is 30 and animation time is 1 sec, or 0.5 sec for each transition)
        # max/(x^15) = 1
        # x = max^(1/15)
        # We divide all components by this number to get smooth transition without changing base color
        if not "quotient" in globals.strip_data[strip_number]["animation_data"]:
            globals.strip_data[strip_number]["animation_data"]["quotient"] = max(color) ** (1. / (globals.config["frameRate"] * time / 2000 - 1))

        quotient = globals.strip_data[strip_number]["animation_data"]["quotient"]

        current_color = globals.strip_data[strip_number]["LEDs"][0]

        if current_color == (0, 0, 0):
            current_color = color

        if current_color[0] <= 1 and current_color[1] <= 1 and current_color[2] <= 1:
            direction = True

        if max(current_color) >= max(color):
            direction = False
            current_color = color

        if direction:
            new_color = (current_color[0]*quotient, current_color[1]*quotient, current_color[2]*quotient)
        else:
            new_color = (current_color[0]/quotient, current_color[1]/quotient, current_color[2]/quotient)

        globals.strip_data[strip_number]["animation_data"]["direction"] = direction

        globals.strip_data[strip_number]["LEDs"] = [new_color for _ in range(0, globals.config["stripLength"])]
        globals.strip_data[strip_number]["redrawn"] = False
