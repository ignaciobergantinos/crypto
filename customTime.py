import datetime
from zoneinfo import ZoneInfo

def getTime():
    now = datetime.datetime.now(ZoneInfo("America/Buenos_Aires"))
    minutes = str(now.minute)
    if len(str(now.minute)) == 1:
        minutes = "0" + str(now.minute)

    return str(now.hour) + ":" + minutes


