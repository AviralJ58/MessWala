
import requests
import json

url = 'https://app.nanonets.com/api/v2/OCR/Model/c6ae1aa4-0006-4a65-8001-f8492d3e20bf/LabelFile/?async=false'

data = {'file': open('Screenshot 2022-07-19 at 23-46-45 Online editor and converter - edit any document quick and easy.png', 'rb')}

response = requests.post(url, auth=requests.auth.HTTPBasicAuth('VMKD_k5J8_RNlzO9chHTYbnAjvuHbn63', ''), files=data)

pred=json.loads(response.text)

f=open('prediction.txt','w')

for content in pred['result'][0]['prediction'][0]['cells']:
    f.write(content['text']+'\n')
        