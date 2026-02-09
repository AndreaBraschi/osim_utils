import os
from pandas import DataFrame

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