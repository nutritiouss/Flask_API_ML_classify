import time
import threading
import random
import requests
import json
from requests.adapters import HTTPAdapter
import logging
import pandas as pd

logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S'
)

url = "http://flask:5000/reg/"
#url = "http://localhost:5000/reg/"
df = pd.read_csv('test_data.csv')

headers = {
  'Content-Type': 'application/json',
  'x-api-key': '123321'
}
adapter = HTTPAdapter(max_retries=1)
session = requests.Session()
session.mount(url, adapter)


def run():
    while True:
        try:
            time.sleep(1)
            #берем рандомную строку из примера
            random_row = random.randint(0, 99)
            d = df.iloc[random_row].to_dict()
            d = json.dumps(d)
            response = session.request("POST", url, headers=headers, data=d, timeout=(2, 5))
            logger.info(response.text)

        except requests.RequestException:
            print("cannot connect", url)
            time.sleep(1)


if __name__ == "__main__":
    for _ in range(4):
        thread = threading.Thread(target=run)
        thread.daemon = True
        thread.start()

    while True:
        time.sleep(1)



