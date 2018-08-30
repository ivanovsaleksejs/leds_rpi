import globals
import time

def redraw_thread():
    while globals.redraw_active:
        start = time.ticks_ms()

        for index, strip in enumerate(globals.strip_data):
            if strip["animation_name"] == "blink":
                demo_blink(index, strip["animation_data"]["color"], strip["animation_data"]["speed"])

            if not strip["redrawn"] and not strip["stopRedraw"]:

                for led_index, color in enumerate(strip["LEDs"]):
                    int_color = (int(color[0]), int(color[1]), int(color[2]))
                    globals.np[int(index * globals.config["stripLength"] + led_index)] = int_color

                globals.strip_data[index]["redrawn"] = True

        globals.np.write()

        end = time.ticks_ms()

        if (end - start) < 1000/globals.config["frameRate"]:
            time.sleep_ms(int(1000/globals.config["frameRate"] - (end - start)))

def demo_blink(strip_number, color, time=1000, pulse=False):
    if globals.strip_data[strip_number]["redrawn"]:

        if not "direction" in globals.strip_data[strip_number]["animation_data"]:
            globals.strip_data[strip_number]["animation_data"]["direction"] = False
        direction = globals.strip_data[strip_number]["animation_data"]["direction"]

        if not "quotient" in globals.strip_data[strip_number]["animation_data"]:
            globals.strip_data[strip_number]["animation_data"]["quotient"] = max(color)**(1./(globals.config["frameRate"]*time/2000))
        quotient = globals.strip_data[strip_number]["animation_data"]["quotient"]

        current_color = globals.strip_data[strip_number]["LEDs"][0]
        if current_color == (0, 0, 0):
            current_color = color
        if current_color[0] < 1 and current_color[1] < 1 and current_color[2] < 1:
            direction = True
        if max(current_color) >= max(color):
            direction = False
            current_color = color
        globals.strip_data[strip_number]["animation_data"]["direction"] = direction

        if direction:
            new_color = (current_color[0]*quotient, current_color[1]*quotient, current_color[2]*quotient)
        else:
            new_color = (current_color[0]/quotient, current_color[1]/quotient, current_color[2]/quotient)

        globals.strip_data[strip_number]["LEDs"] = [new_color for _ in range(0, globals.config["stripLength"])]
        globals.strip_data[strip_number]["redrawn"] = False
