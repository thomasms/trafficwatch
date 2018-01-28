import requests
import json
import datetime
import pytz

from traffic._apikey import API_KEY

base_api = "https://maps.googleapis.com/maps/api/directions"

# Lets go from the Savoy in London to Westminster Cathedral
# at rush hour (08:30) on a Monday
origin_address = "Savoy+Ct,+London+WC2R+0EZ"
destination_address = "Francis+St,+Westminster,+London+SW1P+1QW"
depature_datetime = datetime.datetime(2018, 1, 29, 8, 30, tzinfo=pytz.timezone('Europe/London'))

traffic_model = "pessimistic"

# wraps the api call given a datetimet
def get_optimal_route_time(dt):
    # google API depature time works from seconds since midnight 01/01/1970 UTC time
    depature_time_secs = int((dt-datetime.datetime(1970, 1, 1, 0, 0, tzinfo=pytz.timezone('UTC'))).total_seconds())
    departure_time = "{0}".format(depature_time_secs)

    api_url = "{0}/json?origin={1}&destination={2}&departure_time={3}&traffic_model={4}&key={5}".format(base_api,
                                                                                                        origin_address,
                                                                                                        destination_address,
                                                                                                        departure_time,
                                                                                                        traffic_model,
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

# Get the time
t = get_optimal_route_time(depature_datetime)
print("From: {0}".format(origin_address.replace('+', ' ')))
print("To: {0}".format(destination_address.replace('+', ' ')))
print("At: {0}:{1}".format(depature_datetime.hour, depature_datetime.minute))
print("Quickest route time is: {0} minutes.".format(t/60.))
