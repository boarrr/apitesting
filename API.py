import requests
import gtfs_realtime_pb2

url = "https://api.nationaltransport.ie/gtfsr/v2/Vehicles"


hdr = {
    'x-api-key': 'c582cb4619ce4e938cd74690feda0df0'
}

response = requests.get(url, headers=hdr)

if response.status_code == 200:
    data = response.content

    # Parse the data
    feed = gtfs_realtime_pb2.FeedMessage()
    feed.ParseFromString(data)

    i = 0

    # Process the feed data
    for entity in feed.entity:
        if i > 3:
            break
        print(entity)
        i += 1
 

# Failed to get data
else:
    print("Failed to fetch data:", response.status_code)

