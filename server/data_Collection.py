
from datetime import datetime

# Json format:
{
    "sensor": # name of sensor here: string
    "type": # status_update, warning, error: string
    "message": # status message here: string
    "timestamp": datetime.now() # int
}

def build_json(sensor, type, message, timestamp):
    json_obj = {"sensor": sensor, "type": type, "message": message, "timestamp": timestamp}
    if (type(sensor)== str and type(type)== str and type(message)==str and type(timestamp)== int):
        return json_obj
        raise Exception("You're fucking dumb format things correctly.")