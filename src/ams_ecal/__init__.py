"""Physics-informed tools for AMS-02 ECAL research."""

from ams_ecal.event import (
    EVENT_SCHEMA_VERSION,
    ECALEvent,
    EnergyGrid,
    EventProvenance,
    ParticleType,
    SimulationBackend,
)
from ams_ecal.fastmc_config import (
    EXPECTED_FASTMC_SCHEMA_VERSION,
    FastMCConfig,
    FastMCConfigError,
    LongitudinalEMConfig,
    load_fastmc_config,
)
from ams_ecal.geometry import (
    AbsorberMaterial,
    ActiveVolume,
    CoordinateSystem,
    ECALGeometry,
    FiberAxis,
    GeometryConfigError,
    MaterialDepth,
    MaterialProperties,
    ReadoutGeometry,
    SamplingStructure,
    load_geometry,
)
from ams_ecal.longitudinal import (
    AMSLongitudinalGammaModel,
    ElectromagneticParticleType,
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
    "EXPECTED_FASTMC_SCHEMA_VERSION",
    "AMSLongitudinalGammaModel",
    "AbsorberMaterial",
    "ActiveVolume",
    "CoordinateSystem",
    "ECALEvent",
    "ECALGeometry",
    "ElectromagneticParticleType",
    "EnergyGrid",
    "EventProvenance",
    "FastMCConfig",
    "FastMCConfigError",
    "FiberAxis",
    "GeometryConfigError",
    "LongitudinalEMConfig",
    "MaterialDepth",
    "MaterialProperties",
    "ParticleType",
    "ReadoutGeometry",
    "SamplingStructure",
    "SimulationBackend",
    "TrackState",
    "cell_index_for_layer_projection",
    "coordinate_to_cell_index",
    "load_fastmc_config",
    "load_geometry",
    "measured_axis_for_fiber",
    "project_track_to_cell_indices",
    "project_track_to_z",
]
