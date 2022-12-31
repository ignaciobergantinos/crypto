import requests


def sendNotificationPhone(title, message, type):
    url = "https://wirepusher.com/send?id=PPkWmps6F&title=" + title + "&message=" + message + "&type=" + type
    response = requests.get(url)
    return response
