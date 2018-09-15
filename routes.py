import globals

# Sets animation for lamp using parameters provided with GEt request
def setAnimation(path, params):

    lamp = int(params["lamp"])
    color = tuple(map(lambda x: int(x), params["color"].replace('%2C', ',').split(',')))
    duration = int(params["duration"])

    globals.strip_data[lamp]["reset"] = True
    globals.strip_data[lamp]["animation_name"] = path[0]
    globals.strip_data[lamp]["animation_data"] = {"direction": False, "speed": duration, "color": color}
    globals.strip_data[lamp]["LEDs"] = [color for _ in range(0, globals.config["stripLength"])]
    return ""

# Returns public config data
def getConfig(path, params):

    return globals.dumpconf(globals.config)

# Routes mapping to functions
routes = {
    "animation": setAnimation,
    "config": getConfig
}
