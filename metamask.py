from web3 import Web3, HTTPProvider
import bscscan
import aws

global web3

account1 = "0x1DaDE4ca7c68c03b39C34a6f4D26Bb4c8a2264fb"
account2 = "0x282FaE0F5Cd3568e60883AeB3993c558D95e8743"


def main():
    connectionWeb3()
    # transferBNB(account1,account2, 0)
    # transferBNB(account2,account1, 0)
    # bscscanObj = bscscan.bscScan()


def connectionWeb3():
    global web3
    bsc = "https://bsc-dataseed.binance.org/"
    web3 = Web3(HTTPProvider(bsc))


def transferBNB(fromAccount, toAccount, quantity):
    nonce = web3.eth.getTransactionCount(fromAccount)
    if web3.isConnected():
        tx = {
            'nonce': nonce,
            'to': toAccount,
            'value': web3.toWei(0.001, 'ether'),
            'gas': 21000,
            'gasPrice': web3.toWei('5', 'gwei')
        }
    signed_tx = web3.eth.account.signTransaction(tx, getPrivateKey(fromAccount))
    tx_hash = web3.eth.sendRawTransaction(signed_tx.rawTransaction)
    tx_hash_hex = web3.toHex(tx_hash)
    print("TxId: " + tx_hash_hex)
    return tx_hash_hex


def getPrivateKey(account):
    return aws.getSecretFromAWS(account)['private_key']


main()

# abi = test.getContractSourceCode("0xfdff7a8eda6a3739132867f989be4bf84e803c15")


# # print(conn.eth.get_block(12345))

# # # tkn = "0xB8c77482e45F1F44dE1745F52C74426C631bDD52"

# # # # Web.toChecksumAddress(from_account)

# def getBnbBalance(address):
#   balance = web3.eth.get_balance("0x1DaDE4ca7c68c03b39C34a6f4D26Bb4c8a2264fb")
#   return web3.fromWei(balance, 'ether')
