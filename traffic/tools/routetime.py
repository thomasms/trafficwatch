#!/usr/bin/env python3

import sys
import datetime
import pytz

from traffic.core.api import getOptimalRouteTime


def main():
    origin_address = "Savoy+Ct,+London+WC2R+0EZ"
    destination_address = "Francis+St,+Westminster,+London+SW1P+1QW"
    traffic_model = "pessimistic"

    startTime = datetime.datetime(2020, 2, 3, 9, 0, tzinfo=pytz.timezone('Europe/London'))
    try:
        time = getOptimalRouteTime(startTime, origin_address, destination_address, model=traffic_model)/60.
        print("Quickest route time is: {} minutes.".format(time/60.))
    except OSError as err:
        print("OS error: {0}".format(err))
    except ValueError as err:
        print(err)
    except:
        print("Unexpected error:", sys.exc_info()[0])

if __name__ == "__main__":
    main()

