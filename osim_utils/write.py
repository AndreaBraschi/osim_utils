from pandas import DataFrame
from numpy import ndarray

def writeMotFromDatFrame(df: DataFrame, output_path: str, inDegrees: str = "yes"):
    """
        This function writes a .mot file using from a pandas DataFrame.

        Args:
            df: the DataFrame to write.
            output_path: the path to write the to.
            inDegrees: "yes" or "no", this flag is to tell whether the coordinates are being written in degrees or radians.

    """

    row_1 = output_path
    row_2 = 'version=1'
    nRows: int = df.shape[0]
    nColumns: int = df.shape[1]  # +1 because of time vector

    row_3, row_4 = f'nRows={nRows}', f'nColumns={nColumns}'
    row_5 = f'inDegrees={inDegrees}'
    row_6 = 'endheader'

    columns_list = df.columns.values.tolist()
    data_str = '\t'.join(columns_list)
    headers = '\n'.join([row_1, row_2, row_3, row_4, row_5, row_6, data_str])
    full_data: ndarray = df.values

    with open(output_path, 'w') as mot_file:
        mot_file.write(headers + '\n')
        for n in range(nRows):
            line_arr: ndarray = full_data[n]
            mot_line: str = '\t'.join(map(str, line_arr))
            mot_file.write(mot_line + '\n')

    print(f"Finished writing file at {output_path}")
