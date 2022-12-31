import requests, json
from bs4 import BeautifulSoup
import customTime
import secretsManager, dynamoDB
import notificationPhone



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
   "SpacePi": ["0x69b14e8d3cebfdd8196bfe530954a0c226e5008e",
              "https://coinmarketcap.com/dexscan/bsc/0x7f1b11a798273da438b4b132df1383d8387e73b4", 48384400000, 50,
              300],
   "4TH__": ["0xD3E371dB6977eEeAa338bA86c90Df2Fb3b5993d6",
              "https://coinmarketcap.com/dexscan/bsc/0x7f46eacdfa01834c161aa71b66583e32eb90f7d6", 13769400, 25,
              250],
    "cupid": ["0x8E13db5c015f7790446B38701487087981bd2589",
              "https://coinmarketcap.com/dexscan/bsc/0x678d922f7b4c833308ac7f34f510380802cc22b6", 62610.3, 25,
              250],

}




def getEarnings(money, initialInvestment):
    dif = round(money - initialInvestment, 2)
    return "$" + str(dif)


def getPercentage(earnings, initialInvestment):
    return "P" + str(round(earnings / initialInvestment * 100 - 100, 2))


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
    notificationPhone.sendNotificationPhone(title, message, "nosound")

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
            notificationPhone.sendNotificationPhone(title, message, "takeProfit")


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
