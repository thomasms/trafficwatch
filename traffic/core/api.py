import requests
import json
import datetime
import pytz

from traffic.secrets._apikey import API_KEY

BASE_API_URL = "https://maps.googleapis.com/maps/api/directions"

def getOptimalRouteTime(dt, origin, destination, model="pessimistic"):
    # google API depature time works from seconds since midnight 01/01/1970 UTC time
    depature_time_secs = int((dt-datetime.datetime(1970, 1, 1, 0, 0, tzinfo=pytz.timezone('UTC'))).total_seconds())
    departure_time = "{0}".format(depature_time_secs)

    api_url = "{0}/json?origin={1}&destination={2}&departure_time={3}&traffic_model={4}&key={5}".format(BASE_API_URL,
                                                                                                        origin,
                                                                                                        destination,
                                                                                                        departure_time,
                                                                                                        model,
                                                                                                        API_KEY
                                                                                                        )

    r = requests.get(api_url)
    data = r.json()

    # get the minimum time for all routes
    time_in_secs = float("inf")
    for r in data['routes']:
        route_time_in_secs = 0
        for l in r['legs']:
            route_time_in_secs += l['duration_in_traffic']['value']

        time_in_secs = min(route_time_in_secs, time_in_secs)

    return time_in_secs

