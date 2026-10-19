from .read import readTrc

def check_missing_markers_trc(trc_path: str, init: int, end: int):
    df = readTrc(trc_path)
    df.iloc[init:end + 1].reset_index(drop=True)  # end inclusive
    condition = df[df == 0].count()
    missing_markers = condition[condition > 0].index.array
    num_missing_frames = condition[condition > 0].array

    for i in range(missing_markers.size):
        print(f'marker {missing_markers[i]} is missing in {num_missing_frames[i]} frames')

    return missing_markers