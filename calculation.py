import requests
api_key = 'AIzaSyBgMTRBvh9AE3_WRD_z-htK-rlgRAtDadI'


class Calculation:

    def calculate_distance(origin, destination):
        """calculates distance between two points using google distance api"""
        origin_formatted = origin.replace(' ', '+') if origin else ''
        destination_formatted = destination.replace(' ', '+') if destination else ''
        try:
            url = f'https://maps.googleapis.com/maps/api/distancematrix/json?origins={origin_formatted}&destinations={destination_formatted}&key={api_key}'
        except:
            return ["unknown", 999999999]
        response = requests.get(url)
        data = response.json()
        if data['status'] == "INVALID_REQUEST":
            return "Unavailable"
        if not data['rows']:
            return ['Unknown', 999999999]
        distance_text = data['rows'][0]['elements'][0]['distance']['text']
        distance_value = data['rows'][0]['elements'][0]['distance']['value']
        return [distance_text, distance_value]