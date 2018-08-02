from datetime import datetime
import requests
import base64

username=""
password=""
link_url="http://140.112.107.41/"

auth_data={'username':username,'password':password}
auth_response=requests.post(link_url+"request_token/",auth_data)
auth_data = auth_response.json()
token =auth_data['token']

submit_data = {"SHA256": ""}
response = requests.post(link_url+"get_hooklog/",
                         headers={'Authorization': 'Token {}'.format(token)},
                         data=submit_data)

import json
d = json.loads(response.text)

# write file
for i in d['hooklog']:
    fn = i['filename']
    data = i['hooklog']
    with open('test/' + fn, 'wb') as f:
        f.write(base64.b64decode(data))
