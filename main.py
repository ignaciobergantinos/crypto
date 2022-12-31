import customTime
import coinmarketcap


def main():
    hora = customTime.getTime()

    prices = coinmarketcap.getPrices()

    total = coinmarketcap.getSumOfPrices(prices, hora)

    coinmarketcap.takeProfitAlert(prices, hora)
