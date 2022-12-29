import aws, boto3, json


class dynamodb:
    def __init__(self):
        self.item = None
        self.client = boto3.client('dynamodb', region_name='us-east-1')

    def getItem(self, table, contractAddress):
        self.item = self.client.get_item(
            TableName=table,  # 'cryptoTrades',
            Key={
                'contractAddress': {
                    'S': contractAddress
                }
            }
        )

    def putItem(self, table, contractAddress, accountAddress, tokensAmount, buyPrice, buyTax, sellTax):
        self.client.put_item(
            TableName=table,
            Item={
                'contractAddress': {
                    'S': contractAddress,
                },
                "accountAddress": {
                    "S": accountAddress
                },
                "tokensAmount": {
                    "N": tokensAmount
                },
                "buyPrice": {
                    "N": buyPrice
                },
                "buyTax": {
                    "N": buyTax
                },
                "sellTax": {
                    "N": sellTax
                }
            }
        )

    def getBuyPrice(self):
        if self.item:
            return self.item["Item"]["buyPrice"]["N"]

    def getSellTax(self):
        if self.item:
            return self.item["Item"]["sellTax"]["N"]

    def getBuyTax(self):
        if self.item:
            return self.item["Item"]["buyTax"]["N"]

    def getAccountAddress(self):
        if self.item:
            return self.item["Item"]["accountAddress"]["S"]

    def getLastPrice(self):
        if self.item:
            return self.item["Item"]["lastPrice"]["N"]

    def getTokensAmount(self):
        if self.item:
            return self.item["Item"]["tokensAmount"]["N"]

#
#
# def localGetItem():
#     return {'Item': {'buyPrice': {'N': '0.002171'}, 'sellTax': {'N': '4.7'}, 'accountAddress': {'S': '0x1DaDE4ca7c68c03b39C34a6f4D26Bb4c8a2264fb'}, 'lastPrice': {'N': '0.00274097'}, 'tokensAmount': {'N': '190000'}, 'buyTax': {'N': '5'}, 'contractAddress': {'S': '0xfdff7a8eda6a3739132867f989be4bf84e803c15'}}, 'ResponseMetadata': {'RequestId': 'TJKQQSDC84SM42DV938ULB8AEFVV4KQNSO5AEMVJF66Q9ASUAAJG', 'HTTPStatusCode': 200, 'HTTPHeaders': {'server': 'Server', 'date': 'Thu, 29 Dec 2022 01:06:37 GMT', 'content-type': 'application/x-amz-json-1.0', 'content-length': '277', 'connection': 'keep-alive', 'x-amzn-requestid': 'TJKQQSDC84SM42DV938ULB8AEFVV4KQNSO5AEMVJF66Q9ASUAAJG', 'x-amz-crc32': '1402913086'}, 'RetryAttempts': 0}}
#
# #
# a = dynamodb()
# a.getItem('0xfdff7a8eda6a3739132867f989be4bf84e803c15')
