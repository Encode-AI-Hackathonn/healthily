import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()

user_postcode = 'B15 3TF'
user_postcode_url = user_postcode.replace(' ', '%20')

postcodes_response = requests.get(f'http://api.postcodes.io/postcodes/{user_postcode_url}')

if postcodes_response.status_code == 200:
    data = postcodes_response.json()
    la = data['result']['latitude']
    lg = data['result']['longitude']
    loc = [lg, la]
    print('Latitude: ' + str(la) + '\n' + 'Longitude: ' + str(lg))
    
else:
    print(postcodes_response.status_code)


org_types = ['Hospital', 'Pharmacy', 'Clinic']

api_key = os.getenv('NHS_PK')


headers = {
    'subscription-key': api_key
}

params = {
    'api-version' : '2',
    'search' : org_types[0],
    'searchFields' : 'OrganisationType',
    '$top' : '10',
    '$orderby' : f"geo.distance(Geocode, geography'POINT({lg} {la})') asc"
}

response_services = requests.get('https://api.nhs.uk/service-search', headers=headers, params=params)

if response_services.status_code == 200:
    data = response_services.json()
    with open('result.txt', 'w') as f:
        f.write(json.dumps(data, indent=4))
else:
    print(response_services.status_code)


for item in data['value']:
    print(item['OrganisationName'])