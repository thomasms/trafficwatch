#!/usr/bin/env python3
import sys
sys.path.append('..')

import pytz
import datetime
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

from traffic.core.api import getOptimalRouteTime


def main():
    origin_address = "Savoy+Ct,+London+WC2R+0EZ"
    destination_address = "Francis+St,+Westminster,+London+SW1P+1QW"
    traffic_model = "pessimistic"
    year = 2018
    month = 2
    day = 15
    hour_step = 1
    min_step = 10

    try:
        # Get the time
        hours = np.arange(0, 24, hour_step)
        mins = np.arange(0, 60, min_step)

        dt = []
        times = []
        timesrev = []
        for h in hours:
            for m in mins:
                dt.append(datetime.datetime(year, month, day, h, m, tzinfo=pytz.timezone('Europe/London')))
                times.append(getOptimalRouteTime(dt[-1], origin_address, destination_address, model=traffic_model)/60.)
                timesrev.append(getOptimalRouteTime(dt[-1], destination_address, origin_address, model=traffic_model)/60.)
                print(dt[-1], times[-1])

        fig, ax = plt.subplots(1)
        ax.plot(dt, times, label='origin to dest', color='black')
        ax.plot(dt, timesrev, label='dest to origin', color='red')
        # rush hour peak
        ax.axvline(x=datetime.datetime(year, month, day, 7, 30, tzinfo=pytz.timezone('Europe/London')), linestyle='--', color='orange')
        ax.axvline(x=datetime.datetime(year, month, day, 9, 00, tzinfo=pytz.timezone('Europe/London')), linestyle='--', color='orange')
        ax.axvline(x=datetime.datetime(year, month, day, 16, 30, tzinfo=pytz.timezone('Europe/London')), linestyle='--', color='orange')
        ax.axvline(x=datetime.datetime(year, month, day, 18, 00, tzinfo=pytz.timezone('Europe/London')), linestyle='--', color='orange')
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
        ax.set_title('My journey to work')
        ax.legend(loc='upper left')
        ax.set_xlabel('leave time (HH:MM)')
        ax.set_ylabel('travel time (minutes)')
        plt.gcf().autofmt_xdate()
        plt.savefig('traffic.eps', format='eps', dpi=1000)
        plt.show()

    except OSError as err:
        print("OS error: {0}".format(err))
    except ValueError as err:
        print(err)
    except:
        print("Unexpected error:", sys.exc_info()[0])

    #depature_datetime = datetime.datetime.now()
    #t = get_optimal_route_time(depature_datetime)
    #print("From: {0}".format(origin_address.replace('+', ' ')))
    #print("To: {0}".format(destination_address.replace('+', ' ')))
    #print("At: {0}:{1}".format(depature_datetime.hour, depature_datetime.minute))
    #print("Quickest route time is: {0} minutes.".format(t/60.))

if __name__ == "__main__":
    main()

