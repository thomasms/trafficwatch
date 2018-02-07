import requests
import json
import datetime
import pytz
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

from traffic._apikey import API_KEY

base_api = "https://maps.googleapis.com/maps/api/directions"

origin_address = "Savoy+Ct,+London+WC2R+0EZ"
destination_address = "Francis+St,+Westminster,+London+SW1P+1QW"

traffic_model = "pessimistic"

# wraps the api call given a datetimet
def get_optimal_route_time(dt, reverse=False):
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
    if reverse:
        api_url = "{0}/json?origin={1}&destination={2}&departure_time={3}&traffic_model={4}&key={5}".format(base_api,
                                                                                                            destination_address,
                                                                                                            origin_address,
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
hours = np.arange(0, 24, 1)
mins = np.arange(0, 60, 10)

dt = []
times = []
timesrev = []
for h in hours:
    for m in mins:
        dt.append(datetime.datetime(2018, 2, 8, h, m, tzinfo=pytz.timezone('Europe/London')))
        times.append(get_optimal_route_time(dt[-1], reverse=False)/60.)
        timesrev.append(get_optimal_route_time(dt[-1], reverse=True)/60.)
        print(dt[-1], times[-1])

fig, ax = plt.subplots(1)
ax.plot(dt, times, label='home to work', color='black')
ax.plot(dt, timesrev, label='work to home', color='red')
ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
ax.set_title('My journey to work')
ax.legend(loc='upper left')
ax.set_xlabel('leave time (HH:MM)')
ax.set_ylabel('travel time (minutes)')
plt.gcf().autofmt_xdate()
plt.savefig('traffic.eps', format='eps', dpi=1000)
plt.show()

#depature_datetime = datetime.datetime.now()
#t = get_optimal_route_time(depature_datetime)
#print("From: {0}".format(origin_address.replace('+', ' ')))
#print("To: {0}".format(destination_address.replace('+', ' ')))
#print("At: {0}:{1}".format(depature_datetime.hour, depature_datetime.minute))
#print("Quickest route time is: {0} minutes.".format(t/60.))
