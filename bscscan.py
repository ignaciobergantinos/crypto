
class bscScan:

  def bscScan():
    CONTRACT = "0xfdff7a8eda6a3739132867f989be4bf84e803c15"
    URL = "https://api.bscscan.com/api?module=token&action=tokeninfo&contractaddress=" + CONTRACT + "&apikey=" + APIKEY_BSC

    response = requests.post(URL)
    print(response.content)
    #  

  def getAddressListOfTransactions(self, address): #max 10000 records
    URL = "https://api.bscscan.com/api?module=account&action=txlist&address=" + address + "&startblock=0&endblock=99999999&page=1&offset=10000&sort=desc&apikey=" + APIKEY_BSC
    response = requests.post(URL)
    transactions = json.loads((response.content.decode('utf-8')))
    for results in transactions:
      if results == 'result':
        # return transactions[results]
        for tx in transactions[results]:
          print(tx)
          print('----------------------')

# METHODIDS
# TRANSFER: 0xa9059cbb
# Approve: 0x095ea7b3
# renounceOWnerShip: 0x715018a6
# creation??: 0x60c06040
# lock: 0x07279357
# add liquidity: 0xf305d719

  def contractVerified(self, contract):
    URL = "https://api.bscscan.com/api?module=contract&action=getabi&address=" + contract + "&apikey" + APIKEY_BSC
    response = requests.post(URL)
    ca = json.loads(response.content.decode('utf-8'))

    for results in ca:
      if results == 'result':
        if ca[results] == "Contract source code not verified":
          print('Contract Not verified')
          return False
        return True

  def getAddresbalance(self, address):
    URL = "https://api.bscscan.com/api?module=account&action=balance&address=" + address + "&apikey=" + APIKEY_BSC
    response = requests.post(URL)
    balance = json.loads(response.content.decode('utf-8'))
    return float(balance['result']) / (10 ** 18)

  def getContractSourceCode(self, contract):
      URL = "https://api.bscscan.com/api?module=contract&action=getsourcecode&address=" + contract + "&apikey" + APIKEY_BSC
      response = requests.post(URL)
      code = json.loads(response.content.decode('utf-8'))
      for results in code:
        if results == 'result':
            return code[results]



