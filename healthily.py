import requests

url = "https://portal.your.md/v4/chat"

payload = { 
    "message": "hello!", 
    "conversation_id": "0"
}

headers = {
    "accept": "*/*",
    "content-type": "application/json",
    "Authorization": "Bearer eyJraWQiOiI0Y2RmY2Q0OS1kM2QyLTRlZGMtYThlZi02MDY5ZjRmZWYwNmMiLCJhbGciOiJSUzI1NiJ9.eyJzdWIiOiJ5bWRNb3JzZV9GYm1XWlJLSFZpcE5Jc282bnV2WWQ5dHRSVnY3Nkc5UmphdzFEc0Npc2ZiV28iLCJhdWQiOiJVbml2ZXJzaXR5b2ZCaXJtaW5naGFtIiwiZW1haWxfdmVyaWZpZWQiOnRydWUsImRldmljZV9pZCI6InBhcnRuZXJfVW5pdmVyc2l0eW9mQmlybWluZ2hhbV9hZmQ0MTI1NjgwZjUyYzc5YzMwNmQ4NWQwMjk1MTZiMTQxODJmMmI3MDEzMWI4OTQ2NzJjNGExMTIwZmM0ZjNlIiwibmFtZSI6InN0cmluZyIsImRlbGV0ZV9hdCI6MCwicGlkIjoiamN6QlRZdGJJOWpiUVpoN3VMckN5cTZtYkdlemQxRGkiLCJlbWFpbCI6InN0cmluZyIsImlzcyI6InltZC1pbnRlcm5hbC1zZXJ2aWNlLXByb2QiLCJqdGkiOiIyMTQ4YjFhNC01YmJiLTQxMjMtOGVmYS04M2E4ODc5ZDAyNTkiLCJpYXQiOjE3MDk5Mjg2MzEsImV4cCI6MTcwOTkzMDQzMX0.fMJikeoPkUTKnAjH8iCXOiBjMmVPEHXKPllxVN8mjfs5t7F6A4xx8s0UX8llbtG4RnCyJrFdMbJ5nkdI4LXWDTrASE4aTPLCS7wBCBBhYp2oCgVOqjpN077RdaTLXTstg8aCPZbTz_YgkQujb3kBq2xFeHndIkJlrbxc--9hGj3Qbud9QRx9HK0dhOt8492Esd-rWFMzP8odFN5qLceqSOqMTFWrW4vRle5eD6XF1CGU5vZlsNBKvXwQgRV7w6y-jdtgxKjeYtuQXJB5TId0MKLTUBBysl8ojkTpbEE5MFB-mi_WvFud_ZZ0GLhKcxsURIJf_9yv5MX4G-qJK4VVww",
    "x-api-key": "WOu7AITn55a6jj53R00Jk7OI7xR9fbzt5I1XfOoW"
}

response = requests.post(url, headers=headers, json=payload)

print(response.text)