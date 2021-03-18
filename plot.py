#! /usr/bin/env python3

""" Plot some of the generated logs using matplotlib.
"""

import os
import csv
import glob
import argparse
from datetime import datetime
from matplotlib import pyplot as plt

def parse_args():
    """ Parse basic input arguments.

    Default is to have one plot per day (e.g. log).
    """
    parser = argparse.ArgumentParser(description='Plot some logs.')
    parser.add_argument("-l", "--log-directory", type=str,
        default=os.path.join(os.path.dirname(os.path.abspath(__file__)), "logs"),
        help="the directory containing logs to plot.")
    return parser.parse_args()

def load_log(filename):
    """ Load the contents of a single log file.
    """
    time = []
    code = []
    mesg = []
    with open(filename, "r") as csvfile:
        reader = csv.reader(csvfile)
        for t, c, m in reader:
            time.append(float(t))
            code.append(int(c))
            mesg.append(m)
    # return the length of data along with the data
    return len(time), zip(time, code, mesg)

def plot_single_log(data):
    """ Plot a single log file's information.

    Time is plotted as time-of-day.
    """
    # parse data
    time, code, mesg = zip(*data)

    # convert time to dateime
    x = [datetime.fromtimestamp(t) for t in time]

    # plot time vs. code
    day = datetime.fromtimestamp(time[0]).strftime("%Y-%m-%d")
    plt.figure(day)
    plt.title("Error Codes for {}".format(day))
    plt.plot(x, code, "o")
    plt.grid(True)
    plt.gcf().autofmt_xdate()

if __name__ == "__main__":
    args = parse_args()

    # get all log files in the logging directory
    files = glob.glob(os.path.join(args.log_directory, "*.log"))
    print("Found {} log files in {}".format(len(files), args.log_directory))

    # create and plot a new figure for each file
    for file_ in files:
        size, data = load_log(file_)
        # make sure to skip empty files
        if size != 0:
            plot_single_log(data)

    # show info
    plt.show()


