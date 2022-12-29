import json
import boto3
import base64
from botocore.exceptions import ClientError


def getSecretFromAWS(secret_id):
    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name='us-east-1'
    )

    try:
        get_secret_value_response = client.get_secret_value(SecretId=secret_id)
    except ClientError as e:
        print("Get AWS Secrets " + secret_id + "error -" + e.response['Error']['Code'])
        exit(0)
    else:
        if 'SecretString' in get_secret_value_response:
            return json.loads(get_secret_value_response['SecretString'])
        else:
            return base64.b64decode(get_secret_value_response['SecretBinary'])


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
