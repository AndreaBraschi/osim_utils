import os
import c3d
from numpy import sort, concatenate, array, expand_dims, zeros, linspace, arange

from numpy import float64
from numpy import ndarray
from pandas import DataFrame
from typing import List

def readStoFile(file_path: str) -> DataFrame:
    """
        This function reads a .sto or .mot file using native Python functions and converts it into a pandas DataFrame.

        Args:
            file_path: str = path to .sto or .mot file

            """

    try:
        os.path.exists(file_path)
    except FileNotFoundError:
        print('file does not exists')

    file_id = open(file_path, 'r')
    # read header
    next_line = file_id.readline()
    header = [next_line]
    nc = 0
    nr = 0

    # loop through lines until 'endheader' is found
    while 'endheader' not in next_line:
        if 'nColumns' in next_line:
            nc = int(next_line[next_line.index('=') + 1:len(next_line)])
        elif 'nRows' in next_line:
            nr = int(next_line[next_line.index('=') + 1:len(next_line)])

        next_line = file_id.readline()
        header.append(next_line)

    # process column labels
    next_line = file_id.readline()
    if next_line.isspace() is True:
        next_line = file_id.readline()

    labels = next_line.split()

    # get data
    data = []
    d = [0] * nr
    for i in range(0, nr):
        d[i] = [float(x) for x in file_id.readline().split()]
        data.append(d[i])

    file_id.close()

    df = DataFrame(data=data, columns=labels)

    return df

def readTrc(file_path):
    """ function that reads .trc files and stores the data as a DataFrame"""

    file_id = open(file_path, 'r')
    # read header
    next_line = file_id.readline()
    header = [next_line]
    nc = 0
    nr = 0
    while 'Frame#\t' not in next_line:
        if 'NumFrames\t' in next_line:
            next_line = file_id.readline()
            nr = int(next_line.split('\t')[2])
            nc = int(next_line.split('\t')[3])

        next_line = file_id.readline()
        header.append(next_line)

    labels = next_line.split()
    new_labels = []
    for label in labels:
        if label == 'Frame#' or label == 'Time':
            new_labels.append(label)
        else:
            new_labels.append(label + '.X')
            new_labels.append(label + '.Y')
            new_labels.append(label + '.Z')

    next_line = file_id.readline()

    # get data
    data = []
    d = [0] * nr
    for i in range(0, nr):
        d[i] = [float(x) for x in file_id.readline().split()]
        data.append(d[i][1:])

    file_id.close()

    df = DataFrame(data=data, columns=new_labels[1:])
    return df

def readC3D(c3d_path: str) -> DataFrame:
    with open(c3d_path, 'rb') as handle:
        reader = c3d.Reader(handle)
        items_header = str(reader.header).split('\n')
        items_header_list = [item.strip().split(': ') for item in items_header]
        header_c3d = dict(items_header_list)


        init_frame = int(header_c3d['first_frame'])
        end_frame = int(header_c3d['last_frame'])

        marker_labels = []
        for label in reader.point_labels:
            marker_labels.append(label.strip())
        final_list = []
        idx = []

        for i, marker_ in enumerate(marker_labels):
            final_list.append(marker_ + '.X')
            final_list.append(marker_ + '.Y')
            final_list.append(marker_ + '.Z')
            idx.append(i)

        index_data_markers = sort(
            concatenate(
                [array(idx) * 3, array(idx) * 3 + 1, array(idx) * 3 + 2]
            ))

        # pre-allocate how many entries the final array will have
        columns: int = len(final_list)

        # create time vector
        # 1) get kinematic sampling frequency
        hz: int = reader.point_rate
        dt: float = 1 / hz
        init_time: float = init_frame / hz
        end_time: float = end_frame / hz

        print(f"Initial frame: {init_frame}")
        print(f"End frame: {end_frame}")


        print(f"Initial time: {init_time}")
        print(f"End time: {end_time}")

        time: ndarray = arange(init_time, end_time, dt, dtype=float64)[:, None]
        rows: int = time.shape[0]

        # let's add the time string to the label list
        write_list: List[str] = ["time"] + final_list
        arr: ndarray = zeros((rows + 1, columns + 1), dtype=float64)

        for i, points in enumerate(reader.read_frames()):
            c3d_line = concatenate([item[:3] for item in points[1]])
            c3d_data = expand_dims(c3d_line[index_data_markers], 0)

            if i + 1 > rows:
                # add a zero row
                zero_row: ndarray = zeros((1, 1), dtype=float64)
                time: ndarray = concatenate([time, zero_row], axis=0)
                time[i] = time[i - 1] + dt

            arr[i] = concatenate([time[i][:, None], c3d_data], axis=-1)

        df: DataFrame = DataFrame(data=arr, columns=write_list)

        return df