import requests, json 
from bs4 import BeautifulSoup
from lxml import etree
# from fake_useragent import UserAgent
import datetime


tokens = { 
  "NYT" : ["0xfdff7a8eda6a3739132867f989be4bf84e803c15","https://coinmarketcap.com/dexscan/bsc/0x6dcb370b61b9ee192082a1c42fa994f767916754", 190000],
  "Qatargrow" : ['0x238f5cc8bd082895d1f832cef967e7bb7ba4f992',"https://coinmarketcap.com/dexscan/bsc/0xf1d85613b7cb69460e9cd8565f9793448ecbc83c", 35680.6657466065048718],
  "Christmas" : ['0xc51a7658022bae406900536525877a6dec99c34c',"https://coinmarketcap.com/dexscan/bsc/0x824147f9da7185aeb7e8aa27b102dbef6ca9d690", 48611.243960888],
  "SMSANTA" : ['0x3b58989f6b11e0a348e0b0fee1a8139e7cf2753e',"https://coinmarketcap.com/dexscan/bsc/0x35182c82717cfffd63bf53990721517794b7a314", 31207426106.657056026],
  "MEC" : ["0x4b264f0b2dcbe5a63fb8734d76a644236680ce2d","https://coinmarketcap.com/dexscan/bsc/0xd227f7c2a5b152c3757d1324b31b8fe414fe77ca", 1840000],
  "FLOKY" : ["0x4a01d24aa894530f83fa3764c584fc75885762b4", "https://coinmarketcap.com/dexscan/bsc/0x331b77297fa9acfbf2d73aa7feb693a335efb994", 825171.882619393],
  "CDC" : ['0x06c629728e78906cd2b94e01c9025af6ae6f1dff', "https://coinmarketcap.com/dexscan/bsc/0x6b6807a2302d2663cfc3c70a54a609d16b49abb2", 71.588843663873700398],
  "DSBOWL" : ["0x6a43f8f4b12fcd3b3eb86b319f92eb17c955dda3","https://coinmarketcap.com/dexscan/bsc/0x2515f9c1f0f88dcccffc40ab9660ba8cdfe239d3", 180743.796937320358836921],
  "TOMORROWLAND" :  ['0x58c2cc04b2859916c5e5683545b349df3d7530b8', "https://coinmarketcap.com/dexscan/bsc/0x103d6f7d33fa24865db97b39be3b25443978983e", 19028.354888281089418229],
  "CHINESE_NEW_YEAR" : ["0xdaB9cdB7753e206948ECd691166B33a93693eb75","https://coinmarketcap.com/dexscan/bsc/0xa1178c9d5d66d761c1947f6df3f9279dbd4ad6b7", 226775.992903966],
  "BRAZIL_KING" : ["0xbc7c6e3f8ba62070e3e157e2928d988d59ba752b","https://coinmarketcap.com/dexscan/bsc/0x5ff0f97b605a4678b11024b8cba5a69bdeaaf70d", 37649.117497544942407324],
}

def main():

  hora = getTime()
  message =  getSum()
  sendNotificationPhone(hora, message, "nosound")

def getSum():
  total = 0
  message = ""

  for symbol in tokens:
    contract = tokens[symbol][0]
    urlToken = tokens[symbol][1]
    tokensQuantity = tokens[symbol][2]
    try: 
        price = getCoinMarketCapPrice(urlToken)
        print(symbol + ": " + str(price))
        money = price * tokensQuantity
        message += symbol + ": $" + str(round(price * tokensQuantity, 2)) + "\n"
        total += money
    except Exception as err:
      print(err)

  message += "Total: $" + str(round(total, 2)) + "\n"
  print("Total: $" + str(round(total, 2)))

  return message

def getTime():
  now = datetime.datetime.now()
  hora = str(now.hour) + ":" + str(now.minute)
  return hora

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


main()



