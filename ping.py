#!/usr/bin/env python3
""" Periodically ping Gitlab and log the amount of downtime.
"""

import os
import argparse
import time
import signal
import urllib.request
from threading import Event

# import packages for Exceptions
import http
import socket

# event to handle shutdown
exit = Event()

def parse_args():
    """ Parse basic input arguments.
    """
    parser = argparse.ArgumentParser(description='Periodically log the site code of a given website.')
    parser.add_argument("url", type=str, help="the URL of the website to monitor.")
    parser.add_argument("-b", "--baseline", type=str, default="https://google.com",
        help="a 'reliable' website used to differentiate local internet problems.")
    parser.add_argument("-l", "--log-directory", type=str,
        default=os.path.join(os.path.dirname(os.path.abspath(__file__)), "logs"),
        help="the directory to place logs.")
    parser.add_argument("-i", "--interval", type=float, default=5.0)
    return parser.parse_args()

def main(args):
    """ Continually ping until an exit signal is sent.
    """
    while not exit.is_set():
        # if we have local internet, log sitcore's code
        code = -1
        local_internet_ok = False
        try:
            local_internet_ok = urllib.request.urlopen(args.baseline, timeout=1).getcode() == 200
        except Exception as e:
            # No internet at all, presumable. pass
            print("Couldn't reach baseline URL {}: {} \nAssuming we don't have internet".format(
                args.baseline, e))
        else:
            try:
                code = urllib.request.urlopen(args.url, timeout=min(1,args.interval)).getcode()
            except http.client.RemoteDisconnected:
                # error #1, remote Disconnected
                code = 590
            except socket.timeout:
                # error #2, timeout
                code = 591
            except Exception as e:
                # miscellaneous errors get 599
                code = 599
                print("Using error code {} for miscellaneous error: \n{}: {}".format(code, type(e), e))
            with open(os.path.join(args.log_directory, "log.log"), "a") as f:
                f.write("\n{}, {}".format(time.time(), code))

        # sleep until next poll, or exit requested
        exit.wait(args.interval)

if __name__ == "__main__":
    args = parse_args()
    print("{}: Starting to ping {}, logging to {}".format(
        time.time(), args.url, args.log_directory))

    # set exit signals
    for sig in ('TERM', 'HUP', 'INT'):
        signal.signal(getattr(signal, 'SIG'+sig), lambda s,f: exit.set());

    # run until shut down
    main(args)

