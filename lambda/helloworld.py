import json


def handler(event: dict, context) -> dict:
    return {
        'statusCode': 200,
        'body': json.dumps('Hello World')
    }