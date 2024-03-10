# import requests

# url = "https://portal.your.md/v4/search/symptoms?text=nausea"

# headers = {
#     "accept": "application/json",
#     "authorization": "Bearer eyJraWQiOiI0Y2RmY2Q0OS1kM2QyLTRlZGMtYThlZi02MDY5ZjRmZWYwNmMiLCJhbGciOiJSUzI1NiJ9.eyJzdWIiOiJ5bWRNb3JzZV9FU2tzcFhxWkpUSjhDaXNrVDEyT2drQWJVZEZteDdqV0g2WE5EZzZFN2dTdyIsImF1ZCI6IlVuaXZlcnNpdHlvZkJpcm1pbmdoYW0iLCJlbWFpbF92ZXJpZmllZCI6ZmFsc2UsImRldmljZV9pZCI6InBhcnRuZXJfVW5pdmVyc2l0eW9mQmlybWluZ2hhbV8xYzg5ZTQ0ZDgxZTkzZGFiYzU3ODI2NjU3MWJiM2U0NDJkMGM1NDA4NWJjMmNkNzI0ZjM4NTRlZmFlM2EwYzVmIiwibmFtZSI6IkdpdWxpbyIsImRlbGV0ZV9hdCI6MTcxMDE0MzAyMiwicGlkIjoiRlhJNWp1NTFGMWg4M1NZQmxWNDZObHNGWmxqT1J0QlgiLCJlbWFpbCI6ImdpdWxpby5iZWxsaW5pMDFAZ21haWwuY29tIiwiaXNzIjoieW1kLWludGVybmFsLXNlcnZpY2UtcHJvZCIsImp0aSI6IjNjMmRjMTkwLWVlOWMtNDJkZS1hNWFiLTk4MDMzMjU4MTM1MiIsImlhdCI6MTcwOTk3MDIyMiwiZXhwIjoxNzA5OTcyMDIyfQ.B0TDlFGgSqJqGap9-DnRVElxogb1Y3_IELMi38gL3Zlas5Xa1dkgBhceLUh_MEtJXMQi9QkljCYOX5RkhQFILrVd0SYjPunqULNYVd0F2uxRLH9eC9UQ8BgdaTwGQHlRLuy7FKw35llcqzQ58dBtA4HjBnuWEhc_sSIga5eZjKH993NZq7cf28_sPIBRfKT69cm-MmJo-4XpKe2XeChiiMc16gYOIbgGr9OmWNNH60nVKqF8M5AeBEneWKemQjdfOo2Tli5Owl2ojDc8BZ9L4Bkt5lHTEsBBSLUuPJr1vAFnkNiIKFjsoC53QIKN71jSPtdylFoNldxx9OuaHzg0Dg",
#     "x-api-key": "MkKh1sRuai8UkOLrCoUpIaCum4BdbmzN5VEcsacY"
# }

# response = requests.get(url, headers=headers)

# print(response.text)

import requests
from os import getenv, environ
from dotenv import find_dotenv, load_dotenv, set_key
import haversine as hs
from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route('/nhs',methods = ['POST'])
def nhs():
    assert request.method == 'POST'
    cause = request.json['cause']
    user_postcode = request.json['code']

    suggested_structures = search_service(cause, user_postcode)

    return jsonify(
        suggested_structures
    )

def get_code(user_postcode):
    
    user_postcode_url = user_postcode.replace(' ', '%20')

    postcodes_response = requests.get(f'http://api.postcodes.io/postcodes/{user_postcode_url}')

    if postcodes_response.status_code == 200:
        data = postcodes_response.json()
        la = data['result']['latitude']
        lg = data['result']['longitude']
        loc = [lg, la]
        return lg, la
        
    else:
        print(postcodes_response.status_code)


def get_NHS_header():
        return {
        'Content-Type': 'application/json',
        "subscription-key": f"{getenv('NHS_PK')}"
    }

def search_service(cause, user_postcode):

    lgt, ltn = get_code(user_postcode)

    nhs_url = 'https://api.nhs.uk/service-search'

    parameters = {
        'api-version' : 2,
        'search' : cause,
        '$orderby' : f"geo.distance(Geocode, geography'POINT({lgt} {ltn})')",
        '$top' : 5
    }

    request = requests.get(
        nhs_url,
        headers=get_NHS_header(),
        params=parameters)
    
    suggested_structures = []
    request_json = request.json()
    print(request_json)
    for org in request_json['value']:
        organization = {'Services' : []}
        organization['OrganisationName'] = org['OrganisationName']
        organization["Address"] = " ".join([org['Address1'],org['Address2'],org['Address3'],org['City']])
        organization['Distance'] = str(round(hs.haversine(org['Geocode']['coordinates'], (lgt,ltn)), 2))+'km'
        for service in org['Services']:
            if cause.lower() in service['ServiceName'].lower():
                if service['ServiceName'] not in organization['Services']:
                    organization['Services'].append(service['ServiceName'])
                suggested_structures.append(organization)
                break

    return suggested_structures

if __name__ == "__main__":
    app.run(debug = True, host="0.0.0.0", port=7777)
    # print(search_service('covid', 'B15 3TF'))