from web3 import Web3, HTTPProvider
import bscscan
import secretsManager
import json

account1 = "0x1DaDE4ca7c68c03b39C34a6f4D26Bb4c8a2264fb"
account2 = "0x282FaE0F5Cd3568e60883AeB3993c558D95e8743"


def connectionWeb3():
    bsc = "https://bsc-dataseed.binance.org/"
    web3 = Web3(HTTPProvider(bsc))
    return web3


def transferBNB(conn, fromAccount, toAccount, amountBNB):
    nonce = conn.eth.getTransactionCount(fromAccount)
    if conn.isConnected():
        tx = {
            'nonce': nonce,
            'to': toAccount,
            'value': conn.toWei(amountBNB, 'ether'),
            'gas': 21000,
            'gasPrice': conn.toWei('5', 'gwei')
        }
    signed_tx = conn.eth.account.signTransaction(tx, getPrivateKey(fromAccount))
    tx_hash = conn.eth.sendRawTransaction(signed_tx.rawTransaction)
    tx_hash_hex = conn.toHex(tx_hash)
    print("TxId: " + tx_hash_hex)
    return tx_hash_hex


def getPrivateKey(account):
    return secretsManager.getSecretFromAWS(account)['private_key']



class contractInteraction:

    def __init__(self, conn, contactAddress, abi):
        self.contract = conn.eth.contract(address=contactAddress, abi=abi)
        self.conn = conn

    def getTotalSupply(self):
        return self.contract.functions.totalSupply().call()


    def getName(self):
        return self.contract.functions.name().call()


    def getSymbol(self):
        return self.contract.functions.symbol().call()


    def getBalanceOf(self, address):
        return self.contract.functions.balanceOf(address).call()

    def convertToGweiFormat(self, value):
        return self.conn.fromWei(value, 'gwei')

    def transfer(self, fromAccount, toAccount, amount):
        nonce = self.conn.eth.getTransactionCount(fromAccount)
        token_tx = self.contract.functions.transfer(toAccount, amount).buildTransaction(
            {
                'chainId': 56,
                'gas': 80000,
                'gasPrice': self.conn.toWei('5', 'gwei'),
                'nonce': nonce
            }
        )
        signed_tx = self.conn.eth.account.signTransaction(token_tx, getPrivateKey(fromAccount))
        tx_hash = self.conn.eth.sendRawTransaction(signed_tx.rawTransaction)
        tx_hash_hex = self.conn.toHex(tx_hash)
        print("TxId: " + tx_hash_hex)
        return tx_hash_hex


def tests():
    contactAddress = "0x69b14e8D3CEBfDD8196Bfe530954A0C226E5008E"

    abi = json.loads(
        '[{"constant":true,"inputs":[],"name":"name","outputs":[{"name":"","type":"string"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"spender","type":"address"},{"name":"value","type":"uint256"}],"name":"approve","outputs":[{"name":"","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"totalSupply","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"sender","type":"address"},{"name":"recipient","type":"address"},{"name":"amount","type":"uint256"}],"name":"transferFrom","outputs":[{"name":"","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"decimals","outputs":[{"name":"","type":"uint8"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"spender","type":"address"},{"name":"addedValue","type":"uint256"}],"name":"increaseAllowance","outputs":[{"name":"","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"name":"value","type":"uint256"}],"name":"burn","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[{"name":"account","type":"address"}],"name":"balanceOf","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"symbol","outputs":[{"name":"","type":"string"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"spender","type":"address"},{"name":"subtractedValue","type":"uint256"}],"name":"decreaseAllowance","outputs":[{"name":"","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"name":"recipient","type":"address"},{"name":"amount","type":"uint256"}],"name":"transfer","outputs":[{"name":"","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[{"name":"owner","type":"address"},{"name":"spender","type":"address"}],"name":"allowance","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"inputs":[{"name":"name","type":"string"},{"name":"symbol","type":"string"},{"name":"decimals","type":"uint8"},{"name":"totalSupply","type":"uint256"},{"name":"feeReceiver","type":"address"},{"name":"tokenOwnerAddress","type":"address"}],"payable":true,"stateMutability":"payable","type":"constructor"},{"anonymous":false,"inputs":[{"indexed":true,"name":"from","type":"address"},{"indexed":true,"name":"to","type":"address"},{"indexed":false,"name":"value","type":"uint256"}],"name":"Transfer","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"name":"owner","type":"address"},{"indexed":true,"name":"spender","type":"address"},{"indexed":false,"name":"value","type":"uint256"}],"name":"Approval","type":"event"}]')
    conn = connectionWeb3()

    contract = contractInteraction(conn, contactAddress, abi )

    contract.transfer(account1, account2, 1000)

    # print(contract.getSymbol(), contract.getName(), contract.convertToGweiFormat(contract.getTotalSupply()), contract.convertToGweiFormat(contract.getBalanceOf(account1)))

tests()
# abi = test.getContractSourceCode("0xfdff7a8eda6a3739132867f989be4bf84e803c15")
# # print(conn.eth.get_block(12345))

# # # tkn = "0xB8c77482e45F1F44dE1745F52C74426C631bDD52"

# # # # Web.toChecksumAddress(from_account)

# def getBnbBalance(address):
#   balance = web3.eth.get_balance("0x1DaDE4ca7c68c03b39C34a6f4D26Bb4c8a2264fb")
#   return web3.fromWei(balance, 'ether')
