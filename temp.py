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

headers={
        'Content-Type': 'application/json',
        "subscription-key": '679bdfc8c0b5491bacb0eb9a3d96bb5a'
    }

response = requests.post(
    'https://api.nhs.uk/service-search/search-postcode-or-place?api-version=1&search=Birmingham',
    headers=headers,
    data=u'''
{
    "top": 25,
    "skip": 0,
    "count": true
}
    ''', )

print(response.text)
