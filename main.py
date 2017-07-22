from urllib.parse import urlencode
import requests

TOKEN = "AQAAAAAfAZ9wAARnnc39HxAUcER7jBAqGoCprvo"
AUTH_URL = "https://oauth.yandex.ru/authorize"
ID = "2ca84fdbafe04e798398a233869176cf"
URL = "https://puckyou.github.io/"

def get_link():
    auth_data  = {
        "response_type": "token",
        "client_id": ID
    }
    print("?".join((AUTH_URL, urlencode(auth_data))))

class Ym():
    API_MAN_URL = "https://api-metrika.yandex.ru/management/v1/"
    API_STAT_URL = "https://api-metrika.yandex.ru/stat/v1/"
    token = "None"
    def __init__(self, token):
        self.token = token

    def get_headers(self):
        return {
            "Authorization": "OAuth {}".format(self.token),
            "Content - Type": "application/json"

         }

    def get_counters(self):
        headers = self.get_headers()
        r = requests.get(self.API_MAN_URL + "counters", headers=headers)
        return [counter["id"] for counter in r.json()["counters"]]

class Counter(Ym):
    def __init__(self, token):
        super().__init__(token)


    def get_visitors(self):
        headers = self.get_headers()
        counters = self.get_counters()
        params = {
            "ids": counters,
            "metrics": "ym:s:visits,ym:s:pageviews,ym:s:users"
        }
        r = requests.get(self.API_STAT_URL + "data", headers=headers,params=params)
        return r.json()["data"][0]["metrics"]

    def print_metrics(self):
        print("Посетители:{}\nПросмотры:{}\nПользователи:{}".format(self.get_visitors()[0], self.get_visitors()[1],\
                                                                    self.get_visitors()[2]))


Yam = Counter(TOKEN)
Yam.print_metrics()
