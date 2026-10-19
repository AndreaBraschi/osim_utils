import numpy as np
from .read import readTrc

def check_missing_markers_trc(trc_path: str, init: float, end: float):
    df = readTrc(trc_path)
    t = df["Time"].to_numpy()

    i0 = int(np.abs(t - init).argmin())  # frame nearest to init
    i1 = int(np.abs(t - end).argmin())  # frame nearest to end

    df = df.iloc[i0:i1 + 1].reset_index(drop=True)  # end frame included
    condition = df[df == 0].count()
    missing_markers = condition[condition > 0].index.array
    num_missing_frames = condition[condition > 0].array

    for i in range(missing_markers.size):
        print(f'marker {missing_markers[i]} is missing in {num_missing_frames[i]} frames')

    return missing_markers