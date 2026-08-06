"""Physics-informed tools for AMS-02 ECAL research."""

from ams_ecal.event import (
    EVENT_SCHEMA_VERSION,
    ECALEvent,
    EnergyGrid,
    EventProvenance,
    ParticleType,
    SimulationBackend,
)
from ams_ecal.geometry import (
    ECALGeometry,
    GeometryConfigError,
    load_geometry,
)
from ams_ecal.readout import (
    cell_index_for_layer_projection,
    coordinate_to_cell_index,
    measured_axis_for_fiber,
    project_track_to_cell_indices,
)
from ams_ecal.tracking import TrackState, project_track_to_z

__all__ = [
    "EVENT_SCHEMA_VERSION",
    "ECALEvent",
    "ECALGeometry",
    "EnergyGrid",
    "EventProvenance",
    "GeometryConfigError",
    "ParticleType",
    "SimulationBackend",
    "TrackState",
    "cell_index_for_layer_projection",
    "coordinate_to_cell_index",
    "load_geometry",
    "measured_axis_for_fiber",
    "project_track_to_cell_indices",
    "project_track_to_z",
]