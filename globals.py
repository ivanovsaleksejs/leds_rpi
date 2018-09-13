import json
import neopixel
import machine
import esp

# Returns public config
def dumpconf(config):

    return json.dumps(config)

# Disables esp debug
def no_debug():

    esp.osdebug(None)

# Load config file. Put secrets in separate variable
configFile = open('config.json', 'r')
config = json.loads(configFile.read().replace('\n', ''))
secrets = config["private"]
config = config["public"]
configFile.close()

# Init neopixel
np = neopixel.NeoPixel(machine.Pin(26), config["stripCount"] * config["stripLength"], timing=1)

# Init strip data
strip_data = [
    {
        "stopRedraw": False,
        "redrawn": False,
        "reset": True,
        "animation_name": "",
        "animation_data": {},
        "LEDs": [(0, 0, 0) for _ in range (0, config["stripLength"])]
    } for _ in range (0, config["stripCount"])
]

# While this variable is true redraw thread runs. Thread terminates once it is false
redraw_active = True

# Variable used to adjust delay of each frame
frameTime = 0
