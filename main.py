import requests, json
from bs4 import BeautifulSoup
import datetime, customTime
import secretsManager, dynamoDB
import notificationPhone
import customTime
import coinmarketcap
# APIKEY_BSC = "5EH88KDIGUYFY6QT5PAC4GZJPQ4TQJCXMD"



def main():
    hora = customTime.getTime()

    prices = coinmarketcap.getPrices()

    total = coinmarketcap.getSumOfPrices(prices, hora)

    coinmarketcap.takeProfitAlert(prices, hora)

