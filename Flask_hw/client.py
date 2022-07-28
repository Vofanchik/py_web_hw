import requests
from pprint import pprint

r = requests.get('http://127.0.0.1:5000/advertisment/'#,

                  # json={
                  #     'title':'garaj',
                  #     'description': 'prodam',
                  #     'author': 'petuh'
                  # }
                 )

# r = requests.delete('http://127.0.0.1:5000/advertisment/1')
pprint(r.text)