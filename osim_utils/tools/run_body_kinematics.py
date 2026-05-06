import os
from osim_utils.read import readStoFile
from ..filters.deterministic import butterworth
from opensim import Model, State, AnalyzeTool, BodyKinematics, Storage, StdVectorString

# type hinting imports
from pandas import DataFrame, Series
from numpy import ndarray
from typing import Optional, List


def run_body_kinematics(model_filepath: str, filepath: str, filename: str):
    """
        This function aims at simplifying how the BodyKinematics tool is called and constructed, so that it can be done
        easily also from python scripting or with a CLI extension.

        Args:
            model_filepath: Path to the .osim file
            filepath: path to the file that contains model coordinates. This file could be a motion (.mot) file, containing
                      only the model coordinates or a storage file (.sto) which contains the full state vector.
            list_of_bodies: optional input in case the user were to be interested in the kinematics of only a subset of bodies.
    """
    # where to print all the outputs
    if os.path.split(filepath) == '':
        output_dir: str = os.getcwd()
    else:
        output_dir: str = os.path.split(filepath)[-2]


    # Read file and get initial and final time
    motTime: Series = readStoFile(filepath)["time"]
    init: int = motTime[0]
    end: int = motTime[len(motTime) - 1]


    model: Model = Model(model_filepath)
    model.set_assembly_accuracy(1e-7)
    state: State = model.initSystem()

    # let's check whether the current file is a .sto or a .mot file.
    if filepath.split(".")[-1] in '.mot':
        file: Storage = Storage(filepath)
    else:
        file = filepath


    # Construct empty AnalyzeKinematics tool
    analyzeTool = AnalyzeTool()
    analyzeTool.updAnalysisSet().cloneAndAppend(BodyKinematics())
    analyzeTool.setModel(model)

    analyzeTool.setName(filename)

    file_storage: Storage = Storage(filepath)

    # let's check whether the current file is a .sto or a .mot file.
    if filepath.split(".")[-1] in '.mot':
        analyzeTool.setCoordinatesFileName(filepath)
        analyzeTool.setStatesFromMotion(state, file_storage, True)
    else:
        analyzeTool.setStatesStorage(file_storage)

    analyzeTool.setInitialTime(init)
    analyzeTool.setFinalTime(end)

    # define output directory to print BodyKinematics results
    output_dir = os.path.join(output_dir, "bodyKinematics")
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    analyzeTool.setResultsDir(output_dir)
    analyzeTool.run()
