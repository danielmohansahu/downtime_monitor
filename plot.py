#! /usr/bin/env python3

""" Plot some of the generated logs using matplotlib.
"""

import os
import csv
import glob
import argparse
from datetime import datetime
from matplotlib import dates
from matplotlib import pyplot as plt

def parse_args():
    """ Parse basic input arguments.

    Default is to just plot the latest log.
    """
    parser = argparse.ArgumentParser(description='Plot some logs.')
    parser.add_argument("-l", "--log-directory", type=str,
        default=os.path.join(os.path.dirname(os.path.abspath(__file__)), "logs"),
        help="the directory containing logs to plot.")
    parser.add_argument("-a", "--all", action="store_true", help="Plot all logs. Default is to just plot the latest.")
    parser.add_argument("-f", "--filter", type=int, default=0, help="Plot a moving average over +/- N points. Default is 0, e.g. raw.")
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

def plot_single_log(data, filter_window):
    """ Plot a single log file's information.

    Time is plotted as time-of-day.
    """
    # parse data
    time, code, mesg = zip(*data)

    # convert time to dateime
    x = [datetime.fromtimestamp(t) for t in time]

    # convert codes into boolean "up or down"
    y = [1 if c == 200 else 0 for c in code]

    # get filtered version (basic moving average)
    x_filt = x[filter_window:-1-filter_window]
    y_filt = [1 if any(y[i-filter_window:i+1+filter_window]) else 0 for i,v in enumerate(y[filter_window:-1-filter_window])]

    # plot time vs. code
    day = datetime.fromtimestamp(time[0]).strftime("%Y-%m-%d")
    fig = plt.figure(day)
    plt.title("Error Codes for {}".format(day))
    plt.grid(True)

    # plot raw data and a filtered version
    plt.plot(x_filt, y_filt, "-r")

    # format x data labels
    fig.axes[-1].xaxis.set_major_formatter(dates.DateFormatter('%H:%M'))
    plt.gcf().autofmt_xdate()
    plt.xlabel("time")

    # format y data labels
    labels = ["no", "yes"]
    fig.axes[-1].set_yticks(range(len(labels)))
    fig.axes[-1].set_yticklabels(labels)
    plt.ylabel("Up?")

if __name__ == "__main__":
    args = parse_args()

    # get all log files in the logging directory
    all_files = glob.glob(os.path.join(args.log_directory, "*.log*"))
    print("Found {} log files in {}".format(len(all_files), args.log_directory))

    # check if we're plotting everything or just latest
    if args.all:
        files = all_files
        print("Plotting all data.")
    else:
        all_files.sort()
        files = all_files[:1]
        print("Plotting latest file: {}".format(files))

    # create and plot a new figure for each file
    for file_ in files:
        size, data = load_log(file_)
        # make sure to skip empty files
        if size != 0:
            plot_single_log(data, args.filter)
        else:
            print("Skipping empty file {}".format(file_))

    # show info
    plt.show()


