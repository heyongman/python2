import requests

user_info = {'name': 'letian', 'value': ['letian1', 'letian2']}
r = requests.post("http://127.0.0.1:5000/register", data=user_info)
print r