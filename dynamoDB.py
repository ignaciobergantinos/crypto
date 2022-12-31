import boto3

def getBuyTax(item):
    if item:
        return item["buyTax"]["N"]


def getAccountAddress(item):
    if item:
        return item["accountAddress"]["S"]


def getLastPrice(item):
    if item:
        return item["lastPrice"]["N"]


def getTokensAmount(item):
    if item:
        return item["tokensAmount"]["N"]


def getBuyPrice(item):
    if item:
        return item["buyPrice"]["N"]


def getSellTax(item):
    if item:
        return item["sellTax"]["N"]


def getName(item):
    if item:
        return item["name"]["S"]


class dynamodb:
    def __init__(self):
        self.client = boto3.client('dynamodb', region_name='us-east-1')

    def getAllItems(self):
        return self.client.scan(TableName='cryptoTrades')

    def getItem(self, table, contractAddress):
        item = self.client.get_item(
            TableName=table,  # 'cryptoTrades',
            Key={
                'contractAddress': {
                    'S': contractAddress
                }
            }
        )
        return item
        # example: {'Item': {'buyPrice': {'N': '0.002171'}, 'sellTax': {'N': '4.7'}, 'accountAddress': {'S': '0x1DaDE4ca7c68c03b39C34a6f4D26Bb4c8a2264fb'}, 'lastPrice': {'N': '0.00274097'}, 'tokensAmount': {'N': '190000'}, 'buyTax': {'N': '5'}, 'contractAddress': {'S': '0xfdff7a8eda6a3739132867f989be4bf84e803c15'}}, 'ResponseMetadata': {'RequestId': 'ANIFTRV28LG56BK9N7EQV0E97BVV4KQNSO5AEMVJF66Q9ASUAAJG', 'HTTPStatusCode': 200, 'HTTPHeaders': {'server': 'Server', 'date': 'Thu, 29 Dec 2022 01:36:04 GMT', 'content-type': 'application/x-amz-json-1.0', 'content-length': '277', 'connection': 'keep-alive', 'x-amzn-requestid': 'ANIFTRV28LG56BK9N7EQV0E97BVV4KQNSO5AEMVJF66Q9ASUAAJG', 'x-amz-crc32': '1402913086'}, 'RetryAttempts': 0}}

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

# dynamoDBClient = dynamoDB.dynamodb()
# dynamoDBClient.getItem("cryptoTrades", '0xfdff7a8eda6a3739132867f989be4bf84e803c15')
# print(dynamoDBClient.getAccountAddress(), dynamoDBClient.getBuyPrice(), dynamoDBClient.getBuyPrice(),
#       dynamoDBClient.getBuyTax(), dynamoDBClient.getLastPrice(), dynamoDBClient.getSellTax(),
#       dynamoDBClient.getTokensAmount())