from datetime import datetime
import requests
import base64
import socket
import os 

username=""
password=""
link_url=""

auth_data={'username':username,'password':password}
auth_response=requests.post(link_url+"request_token/",auth_data)
auth_data = auth_response.json()
token =auth_data['token']
print(str(datetime.now())+ " get token {0}".format(token))

dirname = '/' # need / at the last
for i in os.listdir(dirname):
  files = {'file': open(dirname + i, 'rb')}
  streaming_response=requests.post(link_url+"submit_file2/",headers={'Authorization': 'Token {}'.format(token)},files=files)

  print(streaming_response)
