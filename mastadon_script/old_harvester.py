import requests
import json
import couchdb
import mastadon_id
import argparse

parser = argparse.ArgumentParser(description="Search Mastadon with a given hashtag")
parser.add_argument('--tag', required=True, help="hashtag to search for")
parser.add_argument('--ip', required = True, help="IP address of CouchDB Host")
args = parser.parse_args()

url = f'https://mastodon.social/api/v1/timelines/tag/{args.tag}'
ACCESS_TOKEN = 'Dj5UsrDUfcd_vPoYHeYqR6GsnJAghZXC8pRIhsGWzbU'
headers = {'Authorization': f'Bearer {ACCESS_TOKEN}'}
params = {}
count_tots = 0
# Connect to the CouchDB Server
couch = couchdb.Server(f'http://admin:admin@{args.ip}:5984')
# Select the database to insert the data into
db = couch["mastadon"]
if(args.tag is not None):   
    db_spec = couch[str(args.tag)]

while count_tots < 2000:
    # get the oldest tut id (min id from couchdb)
    params["max_id"] = mastadon_id.retrieve_min_mastadonid(db_spec)
    response = requests.get(url, headers=headers, params=params)
    data = response.json()
    count_tots += len(data)
    if len(data) == 0:
        break
    for json_obj in data:
        if db_spec:
            db_spec.save(json_obj, batch='ok')
    for json_obj in data:
        json_obj["_id"] = json_obj["url"]
        db.save(json_obj, batch='ok')
