import aws, boto3, json

def connectDynamodb():
    return boto3.client('dynamodb', region_name='us-east-1')

def getItem():
    DBclient = connectDynamodb()

    item = DBclient.get_item(
      TableName='cryptoTrades',
      Key={
        'id': {
          'contractAddress': '0xfdff7a8eda6a3739132867f989be4bf84e803c15'
        }
      }
    )
    print(item)


getItem()


# data = client.put_item(
#   TableName='table-for-saving-picking-time',
#   Item={
#     'id': {
#       'S': id,
#     },
#     "bodega": {
#       "S": bodega
#     },
#     "StartTimeDate": {
#       "S": startDate
#     },
#     "FinishTimeDate": {
#       "S": finishDate
#     },
#     "StartTimeHour": {
#       "S": startHour
#     },
#     "FinishTimeHour": {
#       "S": finishHour
#     }
#   }
# )
