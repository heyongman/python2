# coding=utf-8
import requests
path = 'C:\\Users\\Administrator\\Downloads\\Compressed\\he.png'

response = requests.post(
    'https://api.remove.bg/v1.0/removebg',
    files={'image_file': open(path, 'rb')},
    data={'size': 'auto', 'bg_color': 'blue'},
    headers={'X-Api-Key': 'NAD3SixKAzQf3v62aEpKompv'},
)
if response.status_code == requests.codes.ok:
    with open('no-bg.png', 'wb') as out:
        out.write(response.content)
else:
    print("Error:", response.status_code, response.text)