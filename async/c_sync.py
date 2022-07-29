import requests
import time



def main():
    currency = requests.get('http://api.coincap.io/v2/assets').json()
    currency = [item['id'] for item in currency['data']]
    for item in currency:
        print(requests.get(f'http://api.coincap.io/v2/assets/{item}').json())

if __name__ == '__main__':
    start = time.time()
    main()
    print(time.time() - start)