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
