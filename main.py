import requests, json 
from bs4 import BeautifulSoup
from lxml import etree
# from fake_useragent import UserAgent
import datetime


tokens = { 
  "NYT__" : ["0xfdff7a8eda6a3739132867f989be4bf84e803c15","https://coinmarketcap.com/dexscan/bsc/0x6dcb370b61b9ee192082a1c42fa994f767916754", 190000, 480, 1000],
  "FLOKY" : ["0x4a01d24aa894530f83fa3764c584fc75885762b4", "https://coinmarketcap.com/dexscan/bsc/0x331b77297fa9acfbf2d73aa7feb693a335efb994", 825171.882619393,200, 1000],
  "CHRIS" : ['0xc51a7658022bae406900536525877a6dec99c34c',"https://coinmarketcap.com/dexscan/bsc/0x824147f9da7185aeb7e8aa27b102dbef6ca9d690", 48611.243960888,100 , 500],
  "MEC__" : ["0x4b264f0b2dcbe5a63fb8734d76a644236680ce2d","https://coinmarketcap.com/dexscan/bsc/0xd227f7c2a5b152c3757d1324b31b8fe414fe77ca", 1840000, 41, 300],
  "QATAR" : ['0x238f5cc8bd082895d1f832cef967e7bb7ba4f992',"https://coinmarketcap.com/dexscan/bsc/0xf1d85613b7cb69460e9cd8565f9793448ecbc83c", 35680.6657466065048718,5, 50],
  "SANTA" : ['0x3b58989f6b11e0a348e0b0fee1a8139e7cf2753e',"https://coinmarketcap.com/dexscan/bsc/0x35182c82717cfffd63bf53990721517794b7a314", 31207426106.657056026, 5, 50],
  "CDC__" : ['0x06c629728e78906cd2b94e01c9025af6ae6f1dff', "https://coinmarketcap.com/dexscan/bsc/0x6b6807a2302d2663cfc3c70a54a609d16b49abb2", 71.588843663873700398, 15, 150],
  "DBOWL" : ["0x6a43f8f4b12fcd3b3eb86b319f92eb17c955dda3","https://coinmarketcap.com/dexscan/bsc/0x2515f9c1f0f88dcccffc40ab9660ba8cdfe239d3", 180743.796937320358836921 , 5, 50],
  "TLAND" :  ['0x58c2cc04b2859916c5e5683545b349df3d7530b8', "https://coinmarketcap.com/dexscan/bsc/0x103d6f7d33fa24865db97b39be3b25443978983e", 19028.354888281089418229 , 5, 50],
  "CNY__" : ["0xdaB9cdB7753e206948ECd691166B33a93693eb75","https://coinmarketcap.com/dexscan/bsc/0xa1178c9d5d66d761c1947f6df3f9279dbd4ad6b7", 226775.992903966, 50, 50],
  "FLOKI" : ["0x0f1e37df0d48bce3f47453bb665a0e14b704a020","https://coinmarketcap.com/dexscan/bsc/0x74ff0e29e45f3dcceafa79263b622ffd4d30a9c3", 129567597406.52865, 8.57, 100],
}

def main():

  hora = getTime()

  prices = getPrices()
  
  total = getSumOfPrices(prices, hora)

  takeProfitAlert()
  trailingStopAlert()
 


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

  for symbol in tokens:
    contract = tokens[symbol][0]
    urlToken = tokens[symbol][1]
    tokensQuantity = tokens[symbol][2]
    initialInvestment = tokens[symbol][3]
    expectedReturn = tokens[symbol][3]

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

  totalMessage = "$" + str(round(total, 2)) + "\n"
  print("-------------")
  print("Total: $" + str(round(total, 2)))

  title = hora + " - " + totalMessage
  sendNotificationPhone(title, message, "nosound")

  return total


def takeProfitAlert():
  return true

def trailingStopAlert():
  return true

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



