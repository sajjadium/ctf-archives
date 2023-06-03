import requests as r
import base64
import hashlib
import os


class serverHandler:
    requestObject = ''
    urllocation = ''

    def __init__(self):
        self.urllocation = f'http://{os.environ["BACKEND_HOST"]}:1717/index.php'
        self.requestObject = 'TzoxMToiTUQ1REJFbmdpbmUiOjI6e3M6MjE6IgBNRDVEQkVuZ2luZQBvYmpBcnJheSI7YToxOntzOjM6Im9iaiI7cjoxO31zOjIzOiIATUQ1REJFbmdpbmUASGFzaFN0cmluZyI7czozMjoiMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAiO30='

    def sendRequest(self, key, word, jwt_token, utils):
        value = base64.b64decode(self.requestObject.encode()).decode()
        value = value.replace('00000000000000000000000000000000', hashlib.md5(word.encode()).hexdigest())
        myDict = {key: base64.b64encode(value.encode()).decode()}
        encoded_jwt = utils.jwtSignerMethod(myDict, jwt_token)
        cookies = {'decodeMyJwt': encoded_jwt}
        response = r.get(self.urllocation, cookies=cookies).text
        return [response if 'FOUND' in response else 'Your password is secure, no matches in our dbs', encoded_jwt]
