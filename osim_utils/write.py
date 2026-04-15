from pandas import DataFrame
from numpy import ndarray, ones
from typing import List


def writeMotFromDataFrame(df: DataFrame, output_path: str, inDegrees: str = "yes"):
    """
        This function writes a .mot file using from a pandas DataFrame.

        Args:
            df: the DataFrame to write.
            output_path: the path to write the to.
            inDegrees: "yes" or "no", this flag is to tell whether the coordinates are being written in degrees or radians.

    """

    row_1 = output_path
    row_2 = 'version=1'
    full_data: ndarray = df.values

    nRows: int = full_data.shape[0]
    nColumns: int = full_data.shape[1]  # +1 because of time vector

    row_3, row_4 = f'nRows={nRows}', f'nColumns={nColumns}'
    row_5 = f'inDegrees={inDegrees}'
    row_6 = 'endheader'

    columns_list = df.columns.values.tolist()
    data_str = '\t'.join(columns_list)
    headers = '\n'.join([row_1, row_2, row_3, row_4, row_5, row_6, data_str])

    with open(output_path, 'w') as mot_file:
        mot_file.write(headers + '\n')
        for n in range(nRows):
            line_arr: ndarray = full_data[n]
            mot_line: str = '\t'.join(map(str, line_arr))
            mot_file.write(mot_line + '\n')

    print(f"Finished writing file at {output_path}")


def writeTrc(time: ndarray, marker_arr: ndarray, labels: List[str], trc_path: str,
              frame_rate: int = 100) -> None:

    init_frame: int = 0
    end_frame: int = len(marker_arr)

    row_1 = 'PathFileType\t4\t(X/Y/Z)\t' + trc_path
    dictionary = {}
    dictionary['DataRate'] = str(frame_rate)
    dictionary['CameraRate'] = str(frame_rate)
    dictionary['NumFrames'] = str(end_frame - init_frame)
    dictionary['NumMarkers'] = str(marker_arr.shape[-1] / 3)
    dictionary['Units'] = 'mm'
    dictionary['OrigDataRate'] = str(frame_rate)
    dictionary['OrigDataStartFrame'] = str(1)
    dictionary['OrigNumFrames'] = dictionary['NumFrames']

    row_4 = 'Frame#\tTime\t' + '\t\t\t'.join([marker.strip() for marker in labels]) + '\t\t'
    row_5 = '\t\t' + '\t'.join([f'X{i + 1}\tY{i + 1}\tZ{i + 1}' for i, _ in enumerate(labels)])

    headers = '\t'.join(dictionary.keys())
    values = '\t'.join(dictionary.values())
    # separate first rows
    full_headers = '\n'.join([row_1, headers, values, row_4, row_5])

    # -----------------------
    # write .trc file
    # -----------------------
    print('Writing .trc file ...')
    with open(trc_path, 'w') as trc:
        trc.write(full_headers + '\n')  # add an extra space between headers and data

        for i in range(len(time)):

            array_line: ndarray = marker_arr[i]
            t = time[i]

            trc_line = f'{i + 1}\t{t}\t' + '\t'.join(map(str, array_line))
            trc.write(trc_line + '\n')

    print(f'File printed at: {trc_path}')