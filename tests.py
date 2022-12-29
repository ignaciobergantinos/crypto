import aws

dynamoDBClient = aws.dynamodb()
dynamoDBClient.getItem("cryptoTrades", '0xfdff7a8eda6a3739132867f989be4bf84e803c15')
print(dynamoDBClient.getAccountAddress(), dynamoDBClient.getBuyPrice(), dynamoDBClient.getBuyPrice(), dynamoDBClient.getBuyTax(), dynamoDBClient.getLastPrice(), dynamoDBClient.getSellTax(),
      dynamoDBClient.getTokensAmount())

