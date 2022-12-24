import requests, json 
from bs4 import BeautifulSoup
from lxml import etree
# from fake_useragent import UserAgent
import datetime, time

# TODO ADD initial investment sum in title

# APIKEY_BSC = "5EH88KDIGUYFY6QT5PAC4GZJPQ4TQJCXMD"



tokens = { 
  "NYT__": ["0xfdff7a8eda6a3739132867f989be4bf84e803c15", "https://coinmarketcap.com/dexscan/bsc/0x6dcb370b61b9ee192082a1c42fa994f767916754",  190000,  480,  2000], 
  "FLOKY": ["0x4a01d24aa894530f83fa3764c584fc75885762b4", "https://coinmarketcap.com/dexscan/bsc/0x331b77297fa9acfbf2d73aa7feb693a335efb994", 43899, 49, 250],
  "Sinu" : ["0x4d496efc21754481fe7a9f3f0f758785ade8e1d3", "https://coinmarketcap.com/dexscan/bsc/0x2cedc038aa6a8b481e8a20d323f83f2718beec1f",  235000000000,  50,  250], 
  "CHRIS" : ['0xc51a7658022bae406900536525877a6dec99c34c', "https://coinmarketcap.com/dexscan/bsc/0x824147f9da7185aeb7e8aa27b102dbef6ca9d690",  48611.243960888, 100 ,  250], 
  "MCT__" : ["0x15e596aecb199d94bbf7869b42273f9e8bcc9fa1", "https://coinmarketcap.com/dexscan/bsc/0xf26b58df2f3fe4dcf625908a592cfa6e1ea5a40a",  219331.4473140,  50,  250], 
  "SFLOK" : ["0x14940169e2db1595cdd3cacd30decc5bbb4d9f19", "https://coinmarketcap.com/dexscan/bsc/0x0fabba0a03879e1b5a114214fbbe1485dec5e4f9",  498360,  50,  150], 
  "CFLOC" : ["0xe5765e33e349b2dcf22a37b2b4e87c10ad43f165", "https://coinmarketcap.com/dexscan/bsc/0x066a9f7b67070cf409314afa648dbd8d66866c7b",  133380000,  50,  100], 
  "NYC__" : ["0x3307381db5ef1fe6c770116304e2c37024023f49", "https://coinmarketcap.com/dexscan/bsc/0xf0abba03cfb987f0d23f8c049c7bfbd96fcf7bba",  8166410,  10,  50], 
  "CMUSK" : ["0x716130205547C093354eAbAcA56294571B938B3B", "https://coinmarketcap.com/dexscan/bsc/0x134f781574722fbf4d7701afda808ed36028bffe",  37.613581481,  10,  50], 
  "MEC__" : ["0x4b264f0b2dcbe5a63fb8734d76a644236680ce2d", "https://coinmarketcap.com/dexscan/bsc/0xd227f7c2a5b152c3757d1324b31b8fe414fe77ca",  1840000,  41,  50], 
  "CFLOKI" : ["0x0f1e37df0d48bce3f47453bb665a0e14b704a020", "https://coinmarketcap.com/dexscan/bsc/0x74ff0e29e45f3dcceafa79263b622ffd4d30a9c3",  129567597406.52865,  8.57,  30], 
  "SShiba" : ["0x52b4f554766b028337e9047c8b916e520c3aa726", "https://coinmarketcap.com/dexscan/bsc/0xe2b78759d4779a6448b1995bb6848f4ee32e25f7",  632193,  50,  150], 
  "FLOV_" : ["0xCA1E6F584E0d7EEc74F553E9a7B64a4DeD8A4b61", "https://coinmarketcap.com/dexscan/bsc/0x0b21b50aa725fc4977b4a215423d44a9d0db6d19",  299394000000,  100 ,  300], 
  "CNY__" : ["0xdaB9cdB7753e206948ECd691166B33a93693eb75", "https://coinmarketcap.com/dexscan/bsc/0xa1178c9d5d66d761c1947f6df3f9279dbd4ad6b7",  226775.992903966,  50,  500], 
  "RABIT" : ["0x95a1199eba84ac5f19546519e287d43d2f0e1b41", "https://coinmarketcap.com/dexscan/bsc/0x04b56a5b3f45cfeafbfdcfc999c14be5434f2146",  24809,  49.5,  500], 
  "CDC__" : ["0x06c629728e78906cd2b94e01c9025af6ae6f1dff",  "https://coinmarketcap.com/dexscan/bsc/0x6b6807a2302d2663cfc3c70a54a609d16b49abb2",  71.5,  15,  150], 
  "SBOWL" : ["0x327bd7E823fe251EC960EeB937cF359149833caC", "https://coinmarketcap.com/dexscan/bsc/0x84e1602ab61272dc90643e24568e78af0fdf8940",  29103000,  25,  3000], 
  "MRABB" : ["0xe8b8F7D15473D6821D525aDBC981665A237d5916", "https://coinmarketcap.com/dexscan/bsc/0x40df4015656b41ea5b6c065e3ffa550a9f0219a1",  519437277087,  25, 75],
}

def main():

  hora = getTime()

  prices = getPrices()

  total = getSumOfPrices(prices, hora)

  takeProfitAlert(prices, hora) 


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
  sendNotificationPhone(title,  message, "nosound")

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

#     if (price > buyPrice and tokensQuantity > 0):
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
  response = requests.get(url)
  print(response.content)

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
  return "P" + str(round(earnings / initialInvestment * 100 - 100, 2))


# class bscScan:

#   # def bscScan():
#   #   CONTRACT = "0xfdff7a8eda6a3739132867f989be4bf84e803c15"
#   #   URL = "https://api.bscscan.com/api?module=token&action=tokeninfo&contractaddress=" + CONTRACT + "&apikey=" + APIKEY_BSC

#   #   response = requests.post(URL)
#   #   print(response.content)
#   #   #  

#   def getAddressListOfTransactions(self, address): #max 10000 records
#     URL = "https://api.bscscan.com/api?module=account&action=txlist&address=" + address + "&startblock=0&endblock=99999999&page=1&offset=10000&sort=desc&apikey=" + APIKEY_BSC
#     response = requests.post(URL)
#     transactions = json.loads((response.content.decode('utf-8')))
#     for results in transactions:
#       if results == 'result':
#         # return transactions[results]
#         for tx in transactions[results]:
#           print(tx)
#           print('----------------------')

#METHODIDS
# TRANSFER: 0xa9059cbb
# Approve: 0x095ea7b3
# renounceOWnerShip: 0x715018a6
# creation??: 0x60c06040
# lock: 0x07279357
# add liquidity: 0xf305d719

  # def contractVerified(self, contract):
  #   URL = "https://api.bscscan.com/api?module=contract&action=getabi&address=" + contract + "&apikey" + APIKEY_BSC
  #   response = requests.post(URL)
  #   ca = json.loads(response.content.decode('utf-8'))

  #   for results in ca:
  #     if results == 'result':
  #       if ca[results] == "Contract source code not verified":
  #         print('Contract Not verified')
  #         return False
  #       return True

  # def getAddresbalance(self, address):
  #   URL = "https://api.bscscan.com/api?module=account&action=balance&address=" + address + "&apikey=" + APIKEY_BSC
  #   response = requests.post(URL)
  #   balance = json.loads(response.content.decode('utf-8'))
  #   return float(balance['result']) / (10 ** 18)

  # def getContractSourceCode(self, contract):
  #     URL = "https://api.bscscan.com/api?module=contract&action=getsourcecode&address=" + contract + "&apikey" + APIKEY_BSC
  #     response = requests.post(URL)
  #     code = json.loads(response.content.decode('utf-8'))
  #     for results in code:
  #       if results == 'result':
  #           return code[results]


main()
text = "NYT__: $606.19 | $126.19 | %126.29 FLOKY: $44.56 | $-4.44 | %90.94 Sinu: $48.3 | $-1.7 | %96.6 CHRIS: $36.03 | $-63.97 | %36.03 MCT__: $55.76 | $5.76 | %111.53 SFLOK: $46.18 | $-3.82 | %92.37 CFLOC: $36.08 | $-13.92 | %72.15 NYC__: $5.52 | $-4.48 | %55.24 CMUSK: $9.71 | $-0.29 | %97.08 MEC__: $11.61 | $-29.39 | %28.32 CFLOKI: $10.51 | $1.94 | %122.69 SShiba: $47.41 | $-2.59 | %94.82 FLOV_: $114.6 | $14.6 | %114.6 CNY__: $46.9 | $-3.1 | %93.8 RABIT: $71.19 | $21.69 | %143.82 CDC__: $10.97 | $-4.03 | %73.13 SBOWL: $22.01 | $-2.99 | %88.04 MRABB: $23.36 | $-1.64 | %93.44"


