import json
import requests
google_key = "AIzaSyDrZ-lEzCYDJRXJc6RxAjcyxK_JSfQpEIw"


class Route:
    def __init__(self):
        self.distance = None
        self.duration = None
        self.coords = []
        self.rating = 0
        self.slopes = []

    def google_init(self, route):
        self.coords = self.decode_polyline(route["overview_polyline"]["points"])
        route = route["legs"][0]
        self.distance = route["distance"]
        self.duration = route["duration"]
        self.add_elev()
        self.calc_slopes()
        return self

    def bing_init(self, route):
        self.distance = route["travelDistance"]
        self.duration = route["travelDurationTraffic"]
        self.coords = route["routePath"]["line"]["coordinates"]
        self.add_elev()
        self.calc_slopes()
        return self

    def add_elev(self):
        elev_req = []
        counter = 0
        index = 0
        elev_str = ""
        for coord in self.coords:
            if counter > 510:
                index += 1
                counter = 0
                elev_str = elev_str[:-1]
                elev_req.append(elev_str)
                elev_str = ""

            elev_str += str(coord[0]) + "," + str(coord[1]) + "|"
            counter += 1

        elev_str = elev_str[:-1]
        elev_req.append(elev_str)

        elevs = []

        for x in range(0, len(elev_req)):
            elev_url = "https://maps.googleapis.com/maps/api/elevation/json?locations=" + elev_req[x] + "&key=" + google_key
            elev_req = requests.get(elev_url)
            if elev_req.status_code == 200:
                elev_json = json.loads(elev_req.text)
                elev_data = elev_json['results']
                for data in elev_data:
                    elevs.append(data['elevation'])

        for x in range(0, len(elevs)):
            self.coords[x].append(elevs[x])

    def calc_slopes(self):
        for i in range(1, len(self.coords)):
            coord = self.coords[i]
            last_coord = self.coords[i-1]

            slope = ((((coord[0] - last_coord[0]) ** 2) + ((coord[1] - last_coord[1]) ** 2)) + ((coord[2] + last_coord[2]) ** 2)) ** 0.5

            self.slopes.append(slope)

        max_slope = self.slopes[0]
        for i in range(1, len(self.slopes)):
            self.rating += abs(self.slopes[i] - self.slopes[i-1])

            if self.slopes[i] > max_slope:
                max_slope = self.slopes[i]

        self.rating /= len(self.slopes)

        self.coords[0].append((self.slopes[0]/max_slope)*255)

        for i in range(1, len(self.coords)):
            self.coords[i].append((self.slopes[i-1] / max_slope) * 255)

    def decode_polyline(self, polyline_str):
        # Pass a Google Maps encoded polyline string; returns list of lat/lon pairs
        index, lat, lng = 0, 0, 0
        coordinates = []
        changes = {'latitude': 0, 'longitude': 0}

        # Coordinates have variable length when encoded, so just keep
        # track of whether we've hit the end of the string. In each
        # while loop iteration, a single coordinate is decoded.
        while index < len(polyline_str):
            # Gather lat/lon changes, store them in a dictionary to apply them later
            for unit in ['latitude', 'longitude']:
                shift, result = 0, 0

                while True:
                    byte = ord(polyline_str[index]) - 63
                    index += 1
                    result |= (byte & 0x1f) << shift
                    shift += 5
                    if not byte >= 0x20:
                        break

                if (result & 1):
                    changes[unit] = ~(result >> 1)
                else:
                    changes[unit] = (result >> 1)

            lat += changes['latitude']
            lng += changes['longitude']

            coordinate = [lat / 100000.0, lng / 100000.0]

            coordinates.append(coordinate)

        return coordinates
