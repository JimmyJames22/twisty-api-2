import json
import requests

bing_key = "AsNyJ5NjEPrI5buVctUalKFK4T6G2xUJyFEv6V-KSViyteReZ9vpP-vMzjY5tyxM"
google_key = "AIzaSyDrZ-lEzCYDJRXJc6RxAjcyxK_JSfQpEIw"


class MapMaster:
    def __init__(self, url_params):
        if url_params.__contains__("origin"):
            self.origin = url_params["origin"][0]
        if url_params.__contains__("destination"):
            self.destination = url_params["destination"][0]
        if url_params.__contains__("mode"):  # can be "driving", "walking", or "transit"
            self.mode = url_params["mode"][0]
        else:
            self.mode = "driving"
        if url_params.__contains__("avoid"):
            self.avoid = json.loads(url_params["avoid"][0])

    def googleReq(self):
        url = "https://maps.googleapis.com/maps/api/directions/json?origin=%s&destination=%s&alternatives=true&key=%s" % (self.origin, self.destination, google_key)
        print(url)
        req = requests.get(url)
        if req.status_code == 200:
            google_json = json.loads(req.text)
            print(google_json['routes'])
