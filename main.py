import requests, json
from bs4 import BeautifulSoup
from lxml import etree
# from fake_useragent import UserAgent
import datetime, time
import secretsManager, dynamoDB

# TODO ADD initial investment sum in title

# APIKEY_BSC = "5EH88KDIGUYFY6QT5PAC4GZJPQ4TQJCXMD"


tokens = {
    "FLOV_": ["0xCA1E6F584E0d7EEc74F553E9a7B64a4DeD8A4b61",
              "https://coinmarketcap.com/dexscan/bsc/0x0b21b50aa725fc4977b4a215423d44a9d0db6d19", 299394000000, 100,
              300],
    "CNY__": ["0xdaB9cdB7753e206948ECd691166B33a93693eb75",
              "https://coinmarketcap.com/dexscan/bsc/0xa1178c9d5d66d761c1947f6df3f9279dbd4ad6b7", 226775.992903966, 50,
              500],
    "CDC__": ["0x06c629728e78906cd2b94e01c9025af6ae6f1dff",
              "https://coinmarketcap.com/dexscan/bsc/0x6b6807a2302d2663cfc3c70a54a609d16b49abb2", 71.5, 15, 150],
    "SBOWL": ["0x327bd7E823fe251EC960EeB937cF359149833caC",
              "https://coinmarketcap.com/dexscan/bsc/0x84e1602ab61272dc90643e24568e78af0fdf8940", 29103000, 25, 3000],
    "MRABB": ["0xe8b8F7D15473D6821D525aDBC981665A237d5916",
              "https://coinmarketcap.com/dexscan/bsc/0x40df4015656b41ea5b6c065e3ffa550a9f0219a1", 519437277087, 25, 75],
   "SPI": ["0x69b14e8d3cebfdd8196bfe530954a0c226e5008e",
              "https://coinmarketcap.com/dexscan/bsc/0x7f1b11a798273da438b4b132df1383d8387e73b4", 48384400000, 50,
              300],
   "4TH": ["0xD3E371dB6977eEeAa338bA86c90Df2Fb3b5993d6",
              "https://coinmarketcap.com/dexscan/bsc/0x7f46eacdfa01834c161aa71b66583e32eb90f7d6", 13769400, 25,
              250],

} #https://coinmarketcap.com/dexscan/bsc/0x7f1b11a798273da438b4b132df1383d8387e73b4

#0x037D70234EeA7D05e8cd6796D89Bc37A2Ac45DE9

def main():
    hora = getTime()

    prices = getPrices()

    total = getSumOfPrices(prices, hora)

    takeProfitAlert(prices, hora)

    dynamoDBClient = dynamoDB.dynamodb()
    dynamoDBClient.getItem("cryptoTrades", '0xfdff7a8eda6a3739132867f989be4bf84e803c15')
    print(dynamoDBClient.getAccountAddress(), dynamoDBClient.getBuyPrice(), dynamoDBClient.getBuyPrice(),
          dynamoDBClient.getBuyTax(), dynamoDBClient.getLastPrice(), dynamoDBClient.getSellTax(),
          dynamoDBClient.getTokensAmount())


# ---------------- testing
# contractVerified("0xfdff7a8eda6a3739132867f989be4bf84e803c15")
# bsc = bscScan()
# ca_not_verified = "0xb5be339fec4fe81d5a2d76dd66159509e2597bac"
# ca_NYT = "0xfdff7a8eda6a3739132867f989be4bf84e803c15"
# value = bsc.getAddressListOfTransactions("0xe222491bf744f180a3499b4590b5f05dcbd9268d")
# print(value)
# buyAlert(prices, hora)

# trailingStopAlert()


def getPrices():
    prices = {}

    for symbol in tokens:
        urlToken = tokens[symbol][1]
        try:
            price = getCoinMarketCapPrice(urlToken)
            prices[urlToken] = price

        except Exception as err:
            print(err)

    return prices


def getSumOfPrices(prices, hora):
    total = 0
    message = ""
    totalInitialInvestment = 0

    for symbol in tokens:
        contract = tokens[symbol][0]
        urlToken = tokens[symbol][1]
        tokensQuantity = tokens[symbol][2]
        initialInvestment = tokens[symbol][3]
        expectedReturn = tokens[symbol][4]
        totalInitialInvestment += initialInvestment

        try:
            price = prices[urlToken]
            money = price * tokensQuantity
            print(symbol + ": $" + str(round(money, 2)))
            earnings = getEarnings(money, initialInvestment)
            percentage = getPercentage(money, initialInvestment)
            message += symbol + ": $" + str(
                round(price * tokensQuantity, 2)) + " | " + earnings + " | " + percentage + "\n"
            total += money



        except Exception as err:
            print(err)

    totalMessage = "$" + str(round(total, 2)) + " | $" + str(round(totalInitialInvestment, 2)) + "\n"
    print("-------------")
    print("Total: $" + str(round(total, 2)))

    title = hora + " - " + totalMessage 
    sendNotificationPhone(title, message, "nosound")

    return total


def takeProfitAlert(prices, hora):
    for symbol in tokens:
        contract = tokens[symbol][0]
        urlToken = tokens[symbol][1]
        tokensQuantity = tokens[symbol][2]
        initialInvestment = tokens[symbol][3]
        expectedReturn = tokens[symbol][4]

        price = prices[urlToken]
        money = round(price * tokensQuantity, 2)

        title = hora + " - " + symbol + " - $" + str(money)

        message = "TAKE PROFIT!!!" + "\n" + "Initial investment: $" + str(
            initialInvestment) + "\n" + "Expected return: $" + str(expectedReturn)

        if money > expectedReturn:
            sendNotificationPhone(title, message, "takeProfit")


# def buyAlert(prices, hora):
#   for symbol in tokens:
#     contract = tokens[symbol][0]
#     urlToken = tokens[symbol][1]
#     tokensQuantity = tokens[symbol][2]
#     buyPrice = tokens[symbol][5]
#     price = prices[urlToken]
#     money = round(price * tokensQuantity,2)


#     title = hora + " - " + symbol + " - $" + str(money)

#     message = "BUY!!!!!!" + "\n" + "Contract:" + contract + "\n" 

#     if (price > buyPrice and tokensQuantity > 0):
#       sendNotificationPhone(title, message, "BuySignal!")

def trailingStopAlert():
    # if price drop x%. (local storage?.. probably)
    return True


def getTime():
    now = datetime.datetime.now()
    minutes = str(now.minute)
    if (len(str(now.minute)) == 1):
        minutes = "0" + str(now.minute)

    if 1 >= (now.hour) <= 3:
        return str(now.hour + 21) + ":" + minutes
    else:
        return str(now.hour - 3) + ":" + minutes


def sendNotificationPhone(title, message, type):
    url = "https://wirepusher.com/send?id=PPkWmps6F&title=" + title + "&message=" + message + "&type=" + type
    response = requests.get(url)


def getCoinMarketCapPrice(url):
    # userAgent = UserAgent()
    # headers = {"User-Agent":userAgent.random}
    webpage = requests.get(url)
    soup = BeautifulSoup(webpage.content, "html.parser")
    metadata = soup.find("script", type="application/ld+json")
    metadataJSON = json.loads(
        str(metadata).replace("</script>", "").replace("<script type=\"application/ld+json\">", ""))
    price = float(metadataJSON['offers']['price'].replace("{", "").replace("}", "").replace(" ", ""))
    return price


def getEarnings(money, initialInvestment):
    dif = round(money - initialInvestment, 2)
    return "$" + str(dif)


def getPercentage(earnings, initialInvestment):
    return "P" + str(round(earnings / initialInvestment * 100 - 100, 2))


main()
