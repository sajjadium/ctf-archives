lambda crypto

import os
import json
import zlib

def lambda_handler(event, context):
    try:
        payload=bytes.fromhex(event["queryStringParameters"]["payload"])
        flag = os.environ["flag"].encode()
        message = b"Your payload is: %b\nThe flag is: %b" % (payload, flag)
        compressed_length = len(zlib.compress(message,9))
    except ValueError as e:
        return {'statusCode': 500, "error": str(e)}

    return {
        'statusCode': 200,
        'body': json.dumps({"sniffed": compressed_length})
    }

It's a little more crypto than web, but I know the exploit from a web defcon talk ages ago. This is a common web exploit for network sniffers.

-ProfNinja
https://55nlig2es7hyrhvzcxzboyp4xe0nzjrc.lambda-url.us-east-1.on.aws/?payload=00
