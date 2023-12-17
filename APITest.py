import requests
import gtfs_realtime_pb2
import time
import pandas as pd
import datetime

# URL of your GTFS Realtime feed
url = "https://api.nationaltransport.ie/gtfsr/v2/gtfsr"

hdr = {
  # Request headers
  'Cache-Control': 'no-cache',
  'x-api-key': 'c582cb4619ce4e938cd74690feda0df0',
}


# Make the request
#response = requests.get(url, headers=hdr)


def vehicleCount():
  response = requests.get(url2, headers=hdr)

  if response.status_code == 200:
    data = response.content

    # Parse the data
    feed = gtfs_realtime_pb2.FeedMessage()
    feed.ParseFromString(data)

    vehicleCount = 0

    # Process the feed data
    for entity in feed.entity:
      if entity.HasField('id'):
        vehicleCount += 1

    return vehicleCount
  
  # Failed to get data      
  else:
    print("Failed to fetch data:", response.status_code)
    return None


def constCount():
  prevCount = 0

  try:
    while True:
      count = vehicleCount()

      if count != prevCount:
        print(count)
        prevCount = count

      time.sleep(30)
  except KeyboardInterrupt:
    print("Exiting...")
    exit(0)


def stopTest():
  stops = pd.read_csv("GTFS/stops.txt")
  routes = pd.read_csv("GTFS/routes.txt")

  all_routes = []

  oconnell_stops = stops[(stops['stop_name'].str.contains("O'Connell Street") )& (stops['stop_code'] < 5000)]

  response = requests.get(url, headers=hdr)

  if response.status_code == 200:
    data = response.content

    # Parse the data
    feed = gtfs_realtime_pb2.FeedMessage()
    feed.ParseFromString(data)

    for entity in feed.entity:
      if entity.HasField('trip_update'):
        for stop_time_update in entity.trip_update.stop_time_update:
          if stop_time_update.stop_id in oconnell_stops['stop_id'].values:
            all_routes.append(routes[routes['route_id'] == entity.trip_update.trip.route_id]['route_short_name'].values[0])
     
    print(set(all_routes))
  
  # Failed to get data        
  else:
    print("Failed to fetch data:", response.status_code)
    return None

  

stopTest()