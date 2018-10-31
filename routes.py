import globals

# Sets animation for lamp using parameters provided with GEt request
def setAnimation(path, params, stripData):
    print(params)

    lamp = int(params["lamp"])
    color = tuple(map(lambda x: int(x), params["color"].replace('%2C', ',').split(',')))
    duration = int(params["duration"])

    stripData[lamp]["reset"] = True
    stripData[lamp]["animation_name"] = path[0]
    stripData[lamp]["animation_data"] = {"direction": False, "speed": duration, "color": color}
    return ""

# Returns public config data
def getConfig(path, params):

    return globals.dumpconf()

# Routes mapping to functions
routes = {
    "animation": setAnimation,
    "config": getConfig
}
