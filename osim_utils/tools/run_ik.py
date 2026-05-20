import os
from opensim import Model
from opensim import InverseKinematicsTool
from typing import Optional, List

def run_ik(model: Model, trc_filepath: str, mot_filepath: str, output_dir: str, init: float, end: float,
           setup_file: Optional[str] = None, markers_not_to_track: Optional[List[str]] = None) -> None:

    """
        This function abstracts away the use of the InverseKinematics tool using the OpenSim API.

        Args:
            model: .osim Model object
            trc_filepath: path to the .trc file that contains the 3D marker coordinates.
            mot_filepath: path to the .mot file that will be saved.
            output_dir: directory to save the output files.
            init: initial time
            end: final time
            setup_file: path to the IK Tool setup file
            markers_not_to_track: list of markers to not track
    """

    if setup_file is not None:
        ikTool = InverseKinematicsTool(setup_file)
    else:
        ikTool = InverseKinematicsTool()

    if markers_not_to_track is not None:
        taskIK = ikTool.getIKTaskSet()
        for marker in markers_not_to_track:
            taskIK.get(marker).setApply(False)

    ikTool.setModel(model)
    ikTool.set_marker_file(trc_filepath)
    ikTool.set_accuracy(1e-04)
    ikTool.set_report_errors(True)
    ikTool.set_report_marker_locations(True)
    ikTool.setResultsDir(output_dir)

    ikTool.setStartTime(init)
    ikTool.setEndTime(end)

    ikTool.setOutputMotionFileName(mot_filepath)
    ikTool.run()