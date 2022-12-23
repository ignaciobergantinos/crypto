import requests, json 
from bs4 import BeautifulSoup
from lxml import etree
# from fake_useragent import UserAgent
import datetime

# TODO ADD initial investment sum in title

tokens = { 
  "NYT__" : ["0xfdff7a8eda6a3739132867f989be4bf84e803c15","https://coinmarketcap.com/dexscan/bsc/0x6dcb370b61b9ee192082a1c42fa994f767916754", 190000, 480, 2000],
  # "FLOKY" : ["0x4a01d24aa894530f83fa3764c584fc75885762b4", "https://coinmarketcap.com/dexscan/bsc/0x331b77297fa9acfbf2d73aa7feb693a335efb994", 0,0, 2000],
  "Sinu" : ["0x4d496efc21754481fe7a9f3f0f758785ade8e1d3","https://coinmarketcap.com/dexscan/bsc/0x2cedc038aa6a8b481e8a20d323f83f2718beec1f", 235000000000, 50, 250],
  "CHRIS" : ['0xc51a7658022bae406900536525877a6dec99c34c',"https://coinmarketcap.com/dexscan/bsc/0x824147f9da7185aeb7e8aa27b102dbef6ca9d690", 48611.243960888,100 , 250],
  "MCT__" : ["0x15e596aecb199d94bbf7869b42273f9e8bcc9fa1","https://coinmarketcap.com/dexscan/bsc/0xf26b58df2f3fe4dcf625908a592cfa6e1ea5a40a", 219331.4473140, 50, 250],
  "SFLOK" : ["0x14940169e2db1595cdd3cacd30decc5bbb4d9f19","https://coinmarketcap.com/dexscan/bsc/0x0fabba0a03879e1b5a114214fbbe1485dec5e4f9", 498360, 50, 150],
  "CFLOC" : ["0xe5765e33e349b2dcf22a37b2b4e87c10ad43f165","https://coinmarketcap.com/dexscan/bsc/0x066a9f7b67070cf409314afa648dbd8d66866c7b", 31223300, 50, 100],
  "NYC__" : ["0x3307381db5ef1fe6c770116304e2c37024023f49","https://coinmarketcap.com/dexscan/bsc/0xf0abba03cfb987f0d23f8c049c7bfbd96fcf7bba", 8166410, 10, 50],
  "CMUSK" : ["0x716130205547C093354eAbAcA56294571B938B3B","https://coinmarketcap.com/dexscan/bsc/0x134f781574722fbf4d7701afda808ed36028bffe", 37.613581481, 10, 50],
  "MEC__" : ["0x4b264f0b2dcbe5a63fb8734d76a644236680ce2d","https://coinmarketcap.com/dexscan/bsc/0xd227f7c2a5b152c3757d1324b31b8fe414fe77ca", 1840000, 41, 50],
  "CFLOKI" : ["0x0f1e37df0d48bce3f47453bb665a0e14b704a020","https://coinmarketcap.com/dexscan/bsc/0x74ff0e29e45f3dcceafa79263b622ffd4d30a9c3", 129567597406.52865, 8.57, 30],

  "FLOV_" : ['0xCA1E6F584E0d7EEc74F553E9a7B64a4DeD8A4b61',"https://coinmarketcap.com/dexscan/bsc/0x0b21b50aa725fc4977b4a215423d44a9d0db6d19", 299394000000, 100 , 300],
  "CNY__" : ["0xdaB9cdB7753e206948ECd691166B33a93693eb75","https://coinmarketcap.com/dexscan/bsc/0xa1178c9d5d66d761c1947f6df3f9279dbd4ad6b7", 226775.992903966, 50, 500],
  "RABIT" : ["0x95a1199eba84ac5f19546519e287d43d2f0e1b41","https://coinmarketcap.com/dexscan/bsc/0x04b56a5b3f45cfeafbfdcfc999c14be5434f2146", 24809, 49.5, 500],
  "SBOWL" : ["0x327bd7E823fe251EC960EeB937cF359149833caC","https://coinmarketcap.com/dexscan/bsc/0x84e1602ab61272dc90643e24568e78af0fdf8940", 29103000, 25, 3000],
  "CDC__" : ['0x06c629728e78906cd2b94e01c9025af6ae6f1dff', "https://coinmarketcap.com/dexscan/bsc/0x6b6807a2302d2663cfc3c70a54a609d16b49abb2", 71.588843663873700398, 15, 150],
  "DBOWL" : ["0x6a43f8f4b12fcd3b3eb86b319f92eb17c955dda3","https://coinmarketcap.com/dexscan/bsc/0x2515f9c1f0f88dcccffc40ab9660ba8cdfe239d3", 180743.796937320358836921 , 5, 50],
  "TLAND" :  ['0x58c2cc04b2859916c5e5683545b349df3d7530b8', "https://coinmarketcap.com/dexscan/bsc/0x103d6f7d33fa24865db97b39be3b25443978983e", 19028.354888281089418229 , 5, 50],
  # ADD THIS ONE 0xf376c874eacdcaaeb2f4012e5e09cf99357d830f !!
  
}

def main():

  hora = getTime()

  prices = getPrices()
  
  total = getSumOfPrices(prices, hora)

  takeProfitAlert(prices, hora) 

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
        print(symbol + ": $" + str(round(money,2)))
        earnings = getEarnings(money, initialInvestment)
        percentage = getPercentage(money, initialInvestment)
        message += symbol + ": $" + str(round(price * tokensQuantity, 2)) + " | " + earnings + " | " + percentage + "\n"
        total += money



    except Exception as err:
      print(err)



  totalMessage = "$" + str(round(total, 2)) +" | $" + str(round(totalInitialInvestment,2)) + "\n"
  print("-------------")
  print("Total: $" + str(round(total, 2)))

  title = hora + " - " + totalMessage
  additionalMessage = "FLOKINY PRICE: " + str(getCoinMarketCapPrice(urlToken)) + "\n" + "\n"
  sendNotificationPhone(title, additionalMessage + message, "nosound")

  return total

def takeProfitAlert(prices, hora):
  for symbol in tokens:
    contract = tokens[symbol][0]
    urlToken = tokens[symbol][1]
    tokensQuantity = tokens[symbol][2]
    initialInvestment = tokens[symbol][3]
    expectedReturn = tokens[symbol][4]

    price = prices[urlToken]
    money = round(price * tokensQuantity,2)


    title = hora + " - " + symbol + " - $" + str(money)

    message = "TAKE PROFIT!!!" + "\n" + "Initial investment: $" + str(initialInvestment) + "\n" + "Expected return: $" + str(expectedReturn)

    if (money > expectedReturn):
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

#     if (price > buyPrice && tokensQuantity > 0):
#       sendNotificationPhone(title, message, "BuySignal!")

def trailingStopAlert():
  #if price drop x%. (local storage?.. probably)
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
  url = "https://wirepusher.com/send?id=PPkWmps6F&title="+ title + "&message=" + message + "&type=" + type
  requests.get(url)

def getCoinMarketCapPrice(url):

  # userAgent = UserAgent()
  # headers = {"User-Agent":userAgent.random}
  webpage = requests.get(url)
  soup = BeautifulSoup(webpage.content, "html.parser")
  metadata = soup.find("script", type="application/ld+json")
  metadataJSON = json.loads(str(metadata).replace("</script>","").replace("<script type=\"application/ld+json\">", ""))
  price = float(metadataJSON['offers']['price'].replace("{","").replace("}","").replace(" ",""))
  return price 

def getEarnings(money, initialInvestment):
  dif = round(money - initialInvestment,2)
  return "$" + str(dif) 
  

def getPercentage(earnings, initialInvestment):
  return "%" + str(round(earnings / initialInvestment * 100, 2))

main()



