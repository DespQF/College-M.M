import csv
import hashlib
import json
import os
import requests
import time
from datetime import datetime

# -files-#
input_file = 'DATA.json'
output_file = 'dom_click.csv'


# -API-And-Connection-#
class DomClickApi:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({"X-Service": "true",
                                     "Connection": "Keep-Alive",
                                     "User-Agent": "Android; 12; Google; google_pixel_5; 8.72.0; 8720006; ; NONAUTH"
                                     })

        # init (get cookies)
        self.get("https://api.domclick.ru/core/no-auth-zone/api/v1/ensure_session")
        self.get("https://ipoteka.domclick.ru/mobile/v1/feature_toggles")

    def get(self, url, **kwargs):
        self.__update_headers(url, **kwargs)
        result = self.session.get(url, **kwargs)
        # print(self.session.cookies.get_dict())
        return result

    def __update_headers(self, url, **kwargs):
        url = self.__get_prepared_url(url, **kwargs)
        sault = "ad65f331b02b90d868cbdd660d82aba0"
        timestamp = str(int(datetime.now().timestamp()))
        encoded = (sault + url + timestamp).encode("UTF-8")
        h = hashlib.md5(encoded).hexdigest()
        self.session.headers.update({"Timestamp": timestamp,
                                     "Hash": "v1:" + h,
                                     })

    def __get_prepared_url(self, url, **kwargs):
        p = requests.models.PreparedRequest()
        p.prepare(method="GET", url=url, **kwargs)
        return p.url


# -get-json-object and write to file-#
def pprint_json(json_str):
    try:

        json_object = json.loads(json_str)
        json_formatted_str = json.dumps(json_object, indent=2, ensure_ascii=False).encode('utf8')
        print("2", json_formatted_str.decode())
        with open("DATA.json", 'wb') as file:
            file.write(json_formatted_str)
        print("-----New DATA sucessfully writed-----")
    except:
        print("3", json_str)


# -creating csv-table-#
if not os.path.exists(output_file):
    with open(output_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(
            ['location', 'floor', 'floor_count', 'rooms_count', 'square_meter_price', 'price',
             'year_of_construction',
             'ipoteka_rate', 'area', 'discount', 'distance', 'monthly_payment'])


def extract_data_to_csv(input_file, output_file):
    # opening input JSON
    with open(input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Opening output CSV
    with open(output_file, 'a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        # Writing JSON-DATA
        for user in data['result']['items']:
            writer.writerow([
                user['address'].get('display_name', 'none'),
                user['object_info'].get('floor', 'none'),
                user['house'].get('floors', 'none'),
                user['object_info'].get('rooms', 'none'),
                user['price_info'].get('square_price', 'none'),
                user['price_info'].get('price', 'none'),
                user.get('flat_complex', {}).get('building', {}).get('end_build_year', 'none'),
                user.get('ipoteka_rate', 'none'),
                user['object_info'].get('area', 'none'),
                user['discount_status'].get('value', 'none'),
                (user.get('address', {}).get('subways', [])[0].get('distance', 'none')
                 if user.get('address', {}).get('subways', []) else 'none'),
                user.get('monthly_payment', 'none')
            ])
        print(f"The data has been successfully extracted and written to '{output_file}'")


print("Welcome to UPDATED Domclick Parser (added data write to the csv table, not to the terminal)")
print("Original By https://gitlab.com/airatb1508/domclick-parser?ysclid=m3g5su2agl154099168")
input("Press ENTER to start parsing")

# -total number of offers-#
offers_url = 'https://offers-service.domclick.ru/research/v5/offers/'
count_url = 'https://offers-service.domclick.ru/research/v5/offers/count/'

# -FILTERS-#(First-Check)
dca = DomClickApi()
res = dca.get(count_url, params={
    "address": "9930cc20-32c6-4f6f-a55e-cd67086c5171",
    "deal_type": "sale",
    "category": "living",
    "offer_type": ["flat"],
    # "rooms": ["1", "2"],
    # "area__gte": 50,
    # "floor__gte": 7,
})
# -The server response to the request-#
print("RES:", res)

# -General information-#
print("1", res.text)
pprint_json(res.text)
count_obj = json.loads(res.text)

# -The total number of offers available for parsing
total = count_obj["pagination"]["total"]

# -clearing old data from a previous offer-#
with open("DATA.json", 'w') as file:
    file.write('')
    print("-----Clearing old DATA-----")

time.sleep(5)
offset = 0
# -The cycle of writing to the table-#
while offset < total:
    # -FILTERS-#(Parsing-process)
    res = dca.get(offers_url, params={
        "address": "9930cc20-32c6-4f6f-a55e-cd67086c5171",
        "deal_type": "sale",
        "category": "living",
        "offer_type": ["flat"],
        # "rooms": ["1", "2"],
        # "area__gte": 50,
        # "floor__gte": 7,

        "sort": "qi",
        "sort_dir": "desc",
        "offset": offset,
        "limit": 1,
    })
    # -The server's response when parsing each page-#
    print("RES:", res)

    # -Calling the page recording function in json-#
    pprint_json(res.text)

    # -Calling the filtering function and writing data from DATA.json to CSV table
    extract_data_to_csv(input_file, output_file)

    # -The time interval between pages-#
    time.sleep(0.05)
    offset += 1

    # -pages counter-#
    offers_obj = json.loads(res.text)
    total = offers_obj["pagination"]["total"]
    print(f"{offset}/{total}")
    # -Delay for normal operation-#
    time.sleep(0.05)
