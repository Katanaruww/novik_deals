import traceback
import time
import json
import sqlite3
from random import randint

import requests


conn = sqlite3.connect('database.db', check_same_thread=False)
cursor = conn.cursor()
global rekv
i2p_proxy = {
            "http": "http://127.0.0.1:4444",
            "https": "https://127.0.0.1:4444"
}
print("гуд")
token = conn.execute("SELECT token FROM setting").fetchone()
while True:
    try:
        params = {'c': '20', 'st': '1'}
        respons = requests.post(f'http://obmen.i2p/api/{token[0]}/p2p_exchange_deals', proxies=i2p_proxy, data=params)
        if respons.status_code == 200:
            js = json.loads(respons.text)
            jsd = js["a"]
            if len(jsd) == 0:
                pass
            else:
                for i in range(len(jsd)):
                    if jsd[i]["status"] == 0:
                        id_num = jsd[i]['id']
                        try:
                            if jsd[i]['pm'] == 1:
                                row = conn.execute("SELECT card FROM cards WHERE payment_type = 'Сбербанк'").fetchall()
                                rekv = row[randint(0, len(row) - 1)]
                            if jsd[i]['pm'] == 2:
                                row = conn.execute("SELECT card FROM cards WHERE payment_type = 'Qiwi'").fetchall()
                                rekv = row[randint(0, len(row) - 1)]
                            if jsd[i]['pm'] == 3:
                                row = conn.execute("SELECT card FROM cards WHERE payment_type = 'Перевод на карту'").fetchall()
                                rekv = row[randint(0, len(row) - 1)]
                            if jsd[i]['pm'] == 4:
                                row = conn.execute("SELECT card FROM cards WHERE payment_type = 'Мобильная связь'").fetchall()
                                rekv = row[randint(0, len(row) - 1)]
                            if jsd[i]['pm'] == 5:
                                row = conn.execute("SELECT card FROM cards WHERE payment_type = 'Qiwi-счёт'").fetchall()
                                rekv = row[randint(0, len(row) - 1)]
                            if jsd[i]['pm'] == 6:
                                row = conn.execute("SELECT card FROM cards WHERE payment_type = 'Тинькофф'").fetchall()
                                rekv = row[randint(0, len(row) - 1)]
                            if jsd[i]['pm'] == 7:
                                row = conn.execute("SELECT card FROM cards WHERE payment_type = 'СБП'").fetchall()
                                rekv = row[randint(0, len(row) - 1)]
                        except Exception:
                            if jsd[i]['pm'] == 1:
                                row = conn.execute("SELECT card FROM cards WHERE payment_type = 'Сбербанк'").fetchall()
                                rekv = row[0]
                            if jsd[i]['pm'] == 2:
                                row = conn.execute("SELECT card FROM cards WHERE payment_type = 'Qiwi'").fetchall()
                                rekv = row[0]
                            if jsd[i]['pm'] == 3:
                                row = conn.execute(
                                    "SELECT card FROM cards WHERE payment_type = 'Перевод на карту'").fetchall()
                                rekv = row[0]
                            if jsd[i]['pm'] == 4:
                                row = conn.execute(
                                    "SELECT card FROM cards WHERE payment_type = 'Мобильная связь'").fetchall()
                                rekv = row[0]
                            if jsd[i]['pm'] == 5:
                                row = conn.execute("SELECT card FROM cards WHERE payment_type = 'Qiwi-счёт'").fetchall()
                                rekv = row[0]
                            if jsd[i]['pm'] == 6:
                                row = conn.execute("SELECT card FROM cards WHERE payment_type = 'Тинькофф'").fetchall()
                                rekv = row[0]
                            if jsd[i]['pm'] == 7:
                                row = conn.execute("SELECT card FROM cards WHERE payment_type = 'СБП'").fetchall()
                                rekv = row[0]

                        param = {"did": id_num, "number": rekv}
                        response = requests.post(f'http://obmen.i2p/api/{token[0]}/p2p_exchange_deal_accept',
                                                            proxies=i2p_proxy, data=param)
                        if response.status_code == 200:
                            print('Успешно!')
                        else:
                            print("увы(")
                        time.sleep(1)
                    else:
                        pass
    except Exception as r:
        print(r)
        print(traceback.print_exc())
        print("Хуй! Проверьте правильность токена")

