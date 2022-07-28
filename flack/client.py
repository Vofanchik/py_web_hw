import requests
from pprint import pprint

r = requests.post('http://127.0.0.1:5000/adv/',

                  json={
                      'email':'dhhh@ff.com',
                      'password': 'Geek@4'
                  }
                 )
pprint(r.text)