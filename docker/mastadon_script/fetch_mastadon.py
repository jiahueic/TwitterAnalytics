import requests
import json
import couchdb
url = 'https://mastodon.social/api/v1/timelines/tag/mentalhealth'
ACCESS_TOKEN = 'Dj5UsrDUfcd_vPoYHeYqR6GsnJAghZXC8pRIhsGWzbU'
headers = {'Authorization': f'Bearer {ACCESS_TOKEN}'}
params = {'local': 'true'}
count_tots = 0
# Connect to the CouchDB Server
couch = couchdb.Server('http://admin:YOURPASSWORD@172.26.129.91:5984')
# Select the database to insert the data into
db = couch["mastadon"]
while count_tots < 200:
    response = requests.get(url, headers=headers, params=params)
    data = response.json()
    print("response received")
    
    
    for json_obj in data:
        db.save(json_obj)
        print("json saved")
    try:
        params["max_id"] = data[len(data) - 1]['id']
    except:
        break


