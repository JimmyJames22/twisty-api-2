import json
import requests
from flask import Response
from route import Route
bing_key = "AsNyJ5NjEPrI5buVctUalKFK4T6G2xUJyFEv6V-KSViyteReZ9vpP-vMzjY5tyxM"
google_key = "AIzaSyDrZ-lEzCYDJRXJc6RxAjcyxK_JSfQpEIw"


class MapMaster:
    def __init__(self, params):
        self.client_id = params['client_id']
        self.origin = params["origin"]
        self.destination = params["destination"]
        self.mode = params["mode"]
        if params['avoid'] is None:
            self.avoid = None
        else:
            self.avoid = json.loads(params["avoid"])
        self.routes = []

        self.google_origin = self.origin.replace(" ", "+")
        self.google_dest = self.destination.replace(" ", "+")
        self.bing_origin = self.origin.replace(" ", "%")
        self.bing_destination = self.destination.replace(" ", "%")

        self.google_url_params = '&origin=' + self.google_origin + '&destination=' + self.google_dest
        self.bing_url_params = "&wp.0=" + self.bing_origin + "&wp.1=" + self.bing_destination

    def get_route(self):
        self.form_reqs()
        self.make_routes()
        resp = Response(json.dumps(str(self.routes)), 200)
        return resp

    def form_reqs(self):
        if self.mode is not None:
            google_mode_string = '&mode=' + self.mode
            self.google_url_params += google_mode_string

        if self.avoid is not None:
            google_avoid_string = '&avoid='
            for x in range(0, len(self.avoid)):
                if x == len(self.avoid)-1:
                    google_avoid_string += self.avoid[x]
                else:
                    google_avoid_string += self.avoid[x] + '|'

            self.google_url_params += google_avoid_string

    def make_routes(self):
        google_url = "https://maps.googleapis.com/maps/api/directions/json?alternatives=true&key=%s%s" % (google_key, self.google_url_params)
        google_req = requests.get(google_url)
        if google_req.status_code == 200:
            google_json = json.loads(google_req.text)
            google_data = google_json['routes']
            for data in google_data:
                route = Route()
                route_parsed = route.google_init(data)
                self.routes.append(route_parsed)


        bing_url = "http://dev.virtualearth.net/REST/v1/Routes?routePathOutput=Points&distanceUnit=mi&maxSolns=3&key=%s%s" % (bing_key, self.bing_url_params)
        bing_req = requests.get(bing_url)
        if bing_req.status_code == 200:
            bing_json = json.loads(bing_req.text)
            bing_data = bing_json['resourceSets'][0]['resources']
            for data in bing_data:
                route = Route()
                route_parsed = route.bing_init(data)
                self.routes.append(route_parsed)

    def add_elev(self):
        for route in self.routes:
            print(route.coords)
            print(route.rating)
