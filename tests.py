import awsSecrets

account1 = "0x1DaDE4ca7c68c03b39C34a6f4D26Bb4c8a2264fb"
account2 = "0x282FaE0F5Cd3568e60883AeB3993c558D95e8743"

def getPrivateKey(account):
  return awsSecrets.get_secrets(account)['private_key']



print(getPrivateKey(account2))