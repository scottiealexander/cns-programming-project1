import json # for the parameters file
import csv  # for the event data
from array import array
import numpy as np

from matplotlib import pyplot as plt
import matplotlib.colors as mcolors

# ---------------------------------------------------------------------------- #
def read_parameter_file(filepath):
    # this is the "pythonic" way to read from a file, by using the:
    # with ... as ...: construct we ensure that the file will automatically
    # get closed *no matter what* (even if an error occurs during reading)
    with open(filepath, "r") as f:
        return json.load(f)
# ---------------------------------------------------------------------------- #
def read_event_file(filepath):
    # intitalize an arrays to hold the event labels (integers) and the event
    # timestamps (floats)
    labels = array("i")
    timestamps = array("d")

    with open(filepath, "r", newline='') as f:
        # use a dict reader to access the columns according the the labels in
        # the first row
        reader = csv.DictReader(
            f,
            delimiter=",",
            quoting=csv.QUOTE_NONNUMERIC,
            quotechar='"'
        )

        for row in reader:
            labels.append(int(row["label"]))
            timestamps.append(float(row["timestamp"]))

    return np.array(labels), np.array(timestamps)
# ---------------------------------------------------------------------------- #
def read_data_file(filepath):
    # data files are *binary* so we *MUST* open as "rb" (read mode + binary mode)
    with open(filepath, "rb") as f:
        # skip the 8-byte header (a Int64 holding the number of elements in
        # the file)
        f.seek(8)
        return np.fromfile(f, dtype=np.float64)
# ---------------------------------------------------------------------------- #
def sample_times(data, fs):
    """
    sample_times(data, fs)

    returns a vector of the time (in seconds) corresponding to each sample
    in <data>

    Input:
        data - a numpy array (1D) of continuous voltage values
        fs   - the sampling rate of the data in Hz
    """
    n = len(data)
    return np.linspace(0, n / fs, n)
# ---------------------------------------------------------------------------- #
def plot_all(data, params, ts, events, labels):
    """
    plot_all(data, params, ts, events, labels)

    plot evenything!

    Input:
        data   - 1D numpy array of continuous voltage values
        params - a dictionary of experimental parameters for this data
                 as returned by read_parameter_file()
        ts     - 1D numpy array of spike timestamps (in seconds)
        events - 1D numpy array of event timestamps (in seconds)
        labels - 1D numpy array of event labels

    """

    t = sample_times(data, params["sample_rate"])

    plt.plot(t, data)

    # plot a black "." at the time of each spike at a y-value of 1.0 (which in
    # this data is the peak amplitude of each spike)
    plt.plot(ts, np.ones(len(ts)), "k.")

    # make a list of color names (should be longer than the number of labels)
    # so that the lines for each event type show up in the same color
    colors = [name for (name, _) in mcolors.BASE_COLORS.items()]

    # list of the unique event labels
    ulab = np.unique(labels)

    # precompute the y-values for our vertical line (data range +- 5%)
    mx = np.amax(data)
    mn = np.amin(data)
    pad = (mx - mn) * 0.05
    mx += pad
    mn -= pad

    # iterate over label,color pairs
    for (label, color) in zip(ulab, colors):

        # find all events of the current type <lab>
        k = np.flatnonzero(labels == label)
        n = len(k)

        # plot a vertical line at the time at which each event of type <label>
        # occured
        plt.plot(
            # x-data is just the time at which the events occured in the form:
            #  t1, t2, t3...
            #  t1, t2, t3...
            np.vstack((events[k], events[k])),

            # y-data is just the ymin,ymax values (~ -0.6, 1.2) in the form:
            #  mn,  mn,  mn...
            #  mx,  mx,  mx...
            np.vstack((np.full((n,), mn), np.full((n,), mx))),

            # set the color for the line
            color=color
        )

    plt.show()

# ---------------------------------------------------------------------------- #
if __name__ == "__main__":
    param_file = "./data/params.json"
    events_file = "./data/events.csv"
    data_file = "./data/continuous1.dat"
    ts_file = "./data/timestamps1.dat"

    params = read_parameter_file(param_file)

    labels, events = read_event_file(events_file)

    data = read_data_file(data_file)
    ts = read_data_file(ts_file)

    plot_all(data, params, ts, events, labels)
