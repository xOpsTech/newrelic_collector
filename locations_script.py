import requests
import urllib.parse
#
# locations = {
#     'Washington, DC, USA': '38.9071923,-77.0368707',
#     'Columbus, OH, USA': '39.9611755, -82.99879419999999',
#     'San Francisco, CA, USA': '37.7749295, -122.4194155',
#
# }

NR_LOCATION_LIST = [
    {
        "name": "AWS_US_EAST_1",
        "label": "Washington, DC, USA"
    },
    {
        "name": "AWS_US_EAST_2",
        "label": "Columbus, OH, USA"
    },
    {
        "name": "AWS_US_WEST_1",
        "label": "San Francisco, CA, USA"
    },
    {
        "name": "AWS_US_WEST_2",
        "label": "Portland, OR, USA"
    },
    {
        "name": "AWS_CA_CENTRAL_1",
        "label": "Montreal, Québec, CA"
    },
    {
        "name": "AWS_EU_WEST_1",
        "label": "Dublin, IE"
    },
    {
        "name": "AWS_EU_CENTRAL_1",
        "label": "Frankfurt, DE"
    },
    {
        "name": "AWS_AP_NORTHEAST_1",
        "label": "Tokyo, JP"
    },
    {
        "name": "AWS_AP_NORTHEAST_2",
        "label": "Seoul, KR"
    },
    {
        "name": "AWS_AP_SOUTHEAST_1",
        "label": "Singapore, SG"
    },
    {
        "name": "AWS_AP_SOUTHEAST_2",
        "label": "Sydney, AU"
    },
    {
        "name": "AWS_AP_SOUTH_1",
        "label": "Mumbai, IN"
    },
    {
        "name": "AWS_SA_EAST_1",
        "label": "São Paulo, BR"
    },
    {
        "name": "LINODE_US_WEST_1",
        "label": "Fremont, CA, USA"
    },
    {
        "name": "LINODE_US_CENTRAL_1",
        "label": "Dallas, TX, USA"
    },
    {
        "name": "LINODE_US_SOUTH_1",
        "label": "Atlanta, GA, USA"
    },
    {
        "name": "LINODE_US_EAST_1",
        "label": "Newark, NJ, USA"
    },
    {
        "name": "LINODE_EU_WEST_1",
        "label": "London, England, UK"
    }
]

API_KEY = 'AIzaSyDvAO1ehevqMYizaj7dON_bwEtq6UDd_ec'
BASE_URL = 'https://maps.googleapis.com/maps/api/geocode/json?address='
KEY_URL = '&key=' + API_KEY

locations = dict()
for location_item in NR_LOCATION_LIST:
    location = location_item.get('label')
    encoded_location = urllib.parse.quote_plus(location)
    url = BASE_URL + encoded_location + KEY_URL
    response = requests.get(url)
    response_json = response.json()
    location_lat_long = response_json['results'][0]['geometry']['location']
    locations[location] = '%s,%s' % (location_lat_long['lat'], location_lat_long['lng'])

print(locations)

l = {'Washington, DC, USA': '38.9071923,-77.0368707', 'Columbus, OH, USA': '39.9611755,-82.99879419999999', 'San Francisco, CA, USA': '37.7749295,-122.4194155', 'Portland, OR, USA': '45.5230622,-122.6764815', 'Montreal, Québec, CA': '45.5016889,-73.567256', 'Dublin, IE': '53.3498053,-6.2603097', 'Frankfurt, DE': '50.1109221,8.6821267', 'Tokyo, JP': '35.6894875,139.6917064', 'Seoul, KR': '37.566535,126.9779692', 'Singapore, SG': '1.352083,103.819836', 'Sydney, AU': '-33.8688197,151.2092955', 'Mumbai, IN': '19.0759837,72.8776559', 'São Paulo, BR': '-23.5505199,-46.63330939999999', 'Fremont, CA, USA': '37.5482697,-121.9885719', 'Dallas, TX, USA': '32.7766642,-96.79698789999999', 'Atlanta, GA, USA': '33.7489954,-84.3879824', 'Newark, NJ, USA': '40.735657,-74.1723667', 'London, England, UK': '51.5073509,-0.1277583'}

