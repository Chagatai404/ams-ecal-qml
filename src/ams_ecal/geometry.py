from collections.abc import Mapping
from dataclasses import dataclass
from math import isclose, isfinite
from pathlib import Path
from typing import Literal

import yaml

EXPECTED_SCHEMA_VERSION = 2
EXPECTED_UNITS = {
    "length": "mm",
    "angle": "rad",
    "energy": "MeV",
    "density": "g/cm^3",
}

FiberAxis = Literal["x", "y"]
AbsorberMaterial = Literal["lead", "aluminum"]

class GeometryConfigError(ValueError):
    """Raised when a geometry configuration is malformed or unsupported."""

@dataclass(frozen=True, slots=True)
class ActiveVolume:
    """Ideal active ECAL readout volume."""

    width_x_mm: float
    width_y_mm: float
    depth_z_mm: float

    def __post_init__(self) -> None:
        for name, value in {
            "width_x_mm": self.width_x_mm,
            "width_y_mm": self.width_y_mm,
            "depth_z_mm": self.depth_z_mm,
        }.items():
            if isinstance(value, bool) or not isinstance(value, int | float):
                raise TypeError(f"{name} must be a real number")

            if not isfinite(value) or value <= 0:
                raise ValueError(f"{name} must be finite and positive")


@dataclass(frozen=True, slots=True)
class ReadoutGeometry:
    """Segmentation and optical readout topology of the ECAL."""

    number_of_superlayers: int
    number_of_layers: int
    cells_per_layer: int
    cell_pitch_mm: float

    photomultipliers: int
    anodes_per_photomultiplier: int
    approximate_fibers_per_cell: int

    superlayer_fiber_axes: tuple[FiberAxis, ...]

    def __post_init__(self) -> None:
        for name, value in {
            "number_of_superlayers": self.number_of_superlayers,
            "number_of_layers": self.number_of_layers,
            "cells_per_layer": self.cells_per_layer,
            "photomultipliers": self.photomultipliers,
            "anodes_per_photomultiplier": self.anodes_per_photomultiplier,
            "approximate_fibers_per_cell": self.approximate_fibers_per_cell,
        }.items():
            if isinstance(value, bool) or not isinstance(value, int):
                raise TypeError(f"{name} must be an integer")

            if value <= 0:
                raise ValueError(f"{name} must be positive")

        if (
            isinstance(self.cell_pitch_mm, bool)
            or not isinstance(self.cell_pitch_mm, int | float)
        ):
            raise TypeError("cell_pitch_mm must be a real number")

        if not isfinite(self.cell_pitch_mm) or self.cell_pitch_mm <= 0:
            raise ValueError("cell_pitch_mm must be finite and positive")

        if not isinstance(self.superlayer_fiber_axes, tuple):
            raise TypeError("superlayer_fiber_axes must be a tuple")

        if len(self.superlayer_fiber_axes) != self.number_of_superlayers:
            raise ValueError(
                "superlayer_fiber_axes must contain one axis per superlayer"
            )

        for axis in self.superlayer_fiber_axes:
            if axis not in {"x", "y"}:
                raise ValueError(
                    "each superlayer fiber axis must be either 'x' or 'y'"
                )

        expected_axes = tuple(
            "x" if index % 2 == 0 else "y"
            for index in range(self.number_of_superlayers)
        )

        if self.superlayer_fiber_axes != expected_axes:
            raise ValueError(
                "superlayer_fiber_axes must alternate starting with 'x'"
            )

        if self.number_of_layers != 2 * self.number_of_superlayers:
            raise ValueError(
                "number_of_layers must equal twice number_of_superlayers"
            )


@dataclass(frozen=True, slots=True)
class SamplingStructure:
    """Physical absorber and scintillating-fiber sampling structure."""

    superlayer_thickness_mm: float

    absorber_foils_per_superlayer: int
    absorber_foil_thickness_mm: float

    fiber_planes_per_superlayer: int
    fiber_diameter_mm: float
    fiber_horizontal_pitch_mm: float
    fiber_row_spacing_mm: float
    adjacent_row_stagger_fraction: float

    standard_absorber_material: AbsorberMaterial
    terminal_foil_material: AbsorberMaterial

    def __post_init__(self) -> None:
        for name, value in {
            "superlayer_thickness_mm": self.superlayer_thickness_mm,
            "absorber_foil_thickness_mm": self.absorber_foil_thickness_mm,
            "fiber_diameter_mm": self.fiber_diameter_mm,
            "fiber_horizontal_pitch_mm": self.fiber_horizontal_pitch_mm,
            "fiber_row_spacing_mm": self.fiber_row_spacing_mm,
        }.items():
            if isinstance(value, bool) or not isinstance(value, int | float):
                raise TypeError(f"{name} must be a real number")

            if not isfinite(value) or value <= 0:
                raise ValueError(f"{name} must be finite and positive")

        for name, value in {
            "absorber_foils_per_superlayer":
                self.absorber_foils_per_superlayer,
            "fiber_planes_per_superlayer":
                self.fiber_planes_per_superlayer,
        }.items():
            if isinstance(value, bool) or not isinstance(value, int):
                raise TypeError(f"{name} must be an integer")

            if value <= 0:
                raise ValueError(f"{name} must be positive")

        if (
            isinstance(self.adjacent_row_stagger_fraction, bool)
            or not isinstance(
                self.adjacent_row_stagger_fraction,
                int | float,
            )
        ):
            raise TypeError(
                "adjacent_row_stagger_fraction must be a real number"
            )

        if not 0 <= self.adjacent_row_stagger_fraction < 1:
            raise ValueError(
                "adjacent_row_stagger_fraction must be in [0, 1)"
            )

        if self.standard_absorber_material != "lead":
            raise ValueError(
                "standard_absorber_material must be 'lead'"
            )

        if self.terminal_foil_material != "aluminum":
            raise ValueError(
                "terminal_foil_material must be 'aluminum'"
            )


@dataclass(frozen=True, slots=True)
class MaterialProperties:
    """Effective properties of the ECAL lead/fiber/glue composite."""

    average_density_g_cm3: float

    relative_volume_lead: float
    relative_volume_scintillating_fiber: float
    relative_volume_optical_glue: float

    effective_critical_energy_mev: float

    def __post_init__(self) -> None:
        for name, value in {
            "average_density_g_cm3": self.average_density_g_cm3,
            "relative_volume_lead": self.relative_volume_lead,
            "relative_volume_scintillating_fiber":
                self.relative_volume_scintillating_fiber,
            "relative_volume_optical_glue":
                self.relative_volume_optical_glue,
            "effective_critical_energy_mev":
                self.effective_critical_energy_mev,
        }.items():
            if isinstance(value, bool) or not isinstance(value, int | float):
                raise TypeError(f"{name} must be a real number")

            if not isfinite(value) or value <= 0:
                raise ValueError(f"{name} must be finite and positive")

    @property
    def normalized_volume_fractions(
        self,
    ) -> tuple[float, float, float]:
        total = (
            self.relative_volume_lead
            + self.relative_volume_scintillating_fiber
            + self.relative_volume_optical_glue
        )

        return (
            self.relative_volume_lead / total,
            self.relative_volume_scintillating_fiber / total,
            self.relative_volume_optical_glue / total,
        )


@dataclass(frozen=True, slots=True)
class MaterialDepth:
    """Integrated ideal material depth of the ECAL."""

    total_depth_x0: float
    total_depth_lambda_i: float

    def __post_init__(self) -> None:
        for name, value in {
            "total_depth_x0": self.total_depth_x0,
            "total_depth_lambda_i": self.total_depth_lambda_i,
        }.items():
            if isinstance(value, bool) or not isinstance(value, int | float):
                raise TypeError(f"{name} must be a real number")

            if not isfinite(value) or value <= 0:
                raise ValueError(f"{name} must be finite and positive")


@dataclass(frozen=True, slots=True)
class CoordinateSystem:
    """Coordinate conventions used throughout the ECAL package."""

    origin: str
    positive_z_direction: str
    theta_reference_axis: str

    def __post_init__(self) -> None:
        expected = {
            "origin": (self.origin, "front_face_center"),
            "positive_z_direction": (
                self.positive_z_direction,
                "into_ecal",
            ),
            "theta_reference_axis": (
                self.theta_reference_axis,
                "positive_z",
            ),
        }

        for name, (actual, expected_value) in expected.items():
            if not isinstance(actual, str):
                raise TypeError(f"{name} must be a string")

            if actual != expected_value:
                raise ValueError(
                    f"{name} must be {expected_value!r}, got {actual!r}"
                )


@dataclass(frozen=True, slots=True)
class ECALGeometry:
    """Validated idealized geometry of the AMS-02 ECAL."""

    active_volume: ActiveVolume
    readout: ReadoutGeometry
    sampling_structure: SamplingStructure
    material_properties: MaterialProperties
    material_depth: MaterialDepth
    coordinate_system: CoordinateSystem

    def __post_init__(self) -> None:
        expected_depth_mm = (
            self.readout.number_of_superlayers
            * self.sampling_structure.superlayer_thickness_mm
        )

        if not isclose(
            self.active_volume.depth_z_mm,
            expected_depth_mm,
        ):
            raise ValueError(
                "active ECAL depth must equal "
                "number_of_superlayers * superlayer_thickness_mm"
            )

        expected_width_mm = (
            self.readout.cells_per_layer
            * self.readout.cell_pitch_mm
        )

        if not isclose(
            self.active_volume.width_x_mm,
            expected_width_mm,
        ):
            raise ValueError(
                "active width_x must equal cells_per_layer * cell_pitch_mm"
            )

        if not isclose(
            self.active_volume.width_y_mm,
            expected_width_mm,
        ):
            raise ValueError(
                "active width_y must equal cells_per_layer * cell_pitch_mm"
            )

        if self.total_cells != self.total_readout_anodes:
            raise ValueError(
                "ECAL cell count must equal total PMT anode count"
            )

# Old properties for backward compatibility with blocks 0 - 3.
    @property
    def width_x_mm(self) -> float:
        return self.active_volume.width_x_mm


    @property
    def width_y_mm(self) -> float:
        return self.active_volume.width_y_mm


    @property
    def depth_z_mm(self) -> float:
        return self.active_volume.depth_z_mm


    @property
    def number_of_superlayers(self) -> int:
        return self.readout.number_of_superlayers


    @property
    def number_of_layers(self) -> int:
        return self.readout.number_of_layers


    @property
    def cells_per_layer(self) -> int:
        return self.readout.cells_per_layer


    @property
    def cell_pitch_mm(self) -> float:
        return self.readout.cell_pitch_mm


    @property
    def superlayer_fiber_axes(self) -> tuple[FiberAxis, ...]:
        return self.readout.superlayer_fiber_axes


    @property
    def total_depth_x0(self) -> float:
        return self.material_depth.total_depth_x0


    @property
    def total_depth_lambda_i(self) -> float:
        return self.material_depth.total_depth_lambda_i

    @property
    def origin(self) -> str:
        return self.coordinate_system.origin


    @property
    def positive_z_direction(self) -> str:
        return self.coordinate_system.positive_z_direction


    @property
    def theta_reference_axis(self) -> str:
        return self.coordinate_system.theta_reference_axis
    
###################################################################

    @property
    def total_cells(self) -> int:
        """Return the total number of readout cells."""

        return self.number_of_layers * self.cells_per_layer

    @property
    def layer_fiber_axes(self) -> tuple[FiberAxis, ...]:
        """Expand each superlayer fiber axis to its two readout layers."""

        return tuple(
            axis
            for axis in self.superlayer_fiber_axes
            for _ in range(2)
        )
    
    @property
    def mean_readout_slice_thickness_mm(self) -> float:
        """Return the active depth divided uniformly among readout layers.

        This is a simplified geometrical quantity, not the documented
        thickness of an individual physical material layer.
        """

        return self.depth_z_mm / self.number_of_layers

    @property
    def mean_readout_slice_thickness_x0(self) -> float:
        return self.total_depth_x0 / self.number_of_layers

    @property
    def uniform_layer_centers_z_mm(self) -> tuple[float, ...]:
        """Return layer-center z coordinates under uniform spacing."""

        spacing_mm = self.mean_readout_slice_thickness_mm

        return tuple(
            (layer_index + 0.5) * spacing_mm
            for layer_index in range(self.number_of_layers)
        )

    @property
    def x_bounds_mm(self) -> tuple[float, float]:
        """Return the active-volume bounds along x."""

        half_width_mm = self.width_x_mm / 2
        return (-half_width_mm, half_width_mm)

    @property
    def y_bounds_mm(self) -> tuple[float, float]:
        """Return the active-volume bounds along y."""

        half_width_mm = self.width_y_mm / 2
        return (-half_width_mm, half_width_mm)

    @property
    def z_bounds_mm(self) -> tuple[float, float]:
        """Return the active-volume bounds along z."""

        return (0.0, self.depth_z_mm)

    @property
    def total_readout_anodes(self) -> int:
        return (
            self.readout.photomultipliers
            * self.readout.anodes_per_photomultiplier
        )


    @property
    def total_absorber_foil_positions(self) -> int:
        return (
            self.number_of_superlayers
            * self.sampling_structure.absorber_foils_per_superlayer
        )


    @property
    def number_of_lead_foils(self) -> int:
        return self.total_absorber_foil_positions - 1


    @property
    def number_of_aluminum_foils(self) -> int:
        return 1


def _require_mapping(value: object, context: str) -> Mapping[object, object]:
    if not isinstance(value, Mapping):
        raise GeometryConfigError(f"{context} must be a YAML mapping")

    return value


def _require_exact_keys(
    mapping: Mapping[object, object],
    expected_keys: set[str],
    context: str,
) -> None:
    actual_keys = set(mapping)
    missing_keys = expected_keys - actual_keys
    unexpected_keys = actual_keys - expected_keys

    problems: list[str] = []

    if missing_keys:
        problems.append(f"missing keys: {sorted(missing_keys)}")

    if unexpected_keys:
        problems.append(
            f"unexpected keys: {sorted(map(str, unexpected_keys))}"
        )

    if problems:
        raise GeometryConfigError(f"{context} has " + "; ".join(problems))


def load_geometry(config_path: str | Path) -> ECALGeometry:
    """Load and validate an AMS-02 ECAL geometry from versioned YAML."""

    path = Path(config_path)

    if not path.is_file():
        raise FileNotFoundError(
            f"Geometry configuration not found: {path}"
        )

    try:
        raw_config = yaml.safe_load(
            path.read_text(encoding="utf-8")
        )
    except yaml.YAMLError as exc:
        raise GeometryConfigError(
            f"Could not parse geometry configuration {path}: {exc}"
        ) from exc

    config = _require_mapping(
        raw_config,
        "geometry configuration root",
    )

    _require_exact_keys(
        config,
        {
            "schema_version",
            "units",
            "active_volume",
            "readout",
            "sampling_structure",
            "material_properties",
            "material_depth",
            "coordinate_system",
        },
        "geometry configuration root",
    )

    # ------------------------------------------------------------------
    # Schema version
    # ------------------------------------------------------------------

    schema_version = config["schema_version"]

    if (
        isinstance(schema_version, bool)
        or not isinstance(schema_version, int)
    ):
        raise GeometryConfigError(
            "schema_version must be an integer"
        )

    if schema_version != EXPECTED_SCHEMA_VERSION:
        raise GeometryConfigError(
            "Unsupported geometry schema_version "
            f"{schema_version}; "
            f"expected {EXPECTED_SCHEMA_VERSION}"
        )

    # ------------------------------------------------------------------
    # Units
    # ------------------------------------------------------------------

    units = _require_mapping(
        config["units"],
        "units",
    )

    _require_exact_keys(
        units,
        set(EXPECTED_UNITS),
        "units",
    )

    if dict(units) != EXPECTED_UNITS:
        raise GeometryConfigError(
            f"units must equal {EXPECTED_UNITS}, "
            f"got {dict(units)}"
        )

    # ------------------------------------------------------------------
    # Sections
    # ------------------------------------------------------------------

    active_volume = _require_mapping(
        config["active_volume"],
        "active_volume",
    )

    readout = _require_mapping(
        config["readout"],
        "readout",
    )

    sampling_structure = _require_mapping(
        config["sampling_structure"],
        "sampling_structure",
    )

    material_properties = _require_mapping(
        config["material_properties"],
        "material_properties",
    )

    material_depth = _require_mapping(
        config["material_depth"],
        "material_depth",
    )

    coordinate_system = _require_mapping(
        config["coordinate_system"],
        "coordinate_system",
    )

    # ------------------------------------------------------------------
    # Validate section keys
    # ------------------------------------------------------------------

    _require_exact_keys(
        active_volume,
        {
            "width_x",
            "width_y",
            "depth_z",
        },
        "active_volume",
    )

    _require_exact_keys(
        readout,
        {
            "number_of_superlayers",
            "number_of_layers",
            "cells_per_layer",
            "cell_pitch",
            "photomultipliers",
            "anodes_per_photomultiplier",
            "approximate_fibers_per_cell",
            "superlayer_fiber_axes",
        },
        "readout",
    )

    _require_exact_keys(
        sampling_structure,
        {
            "superlayer_thickness",
            "absorber_foils_per_superlayer",
            "absorber_foil_thickness",
            "fiber_planes_per_superlayer",
            "fiber_diameter",
            "fiber_horizontal_pitch",
            "fiber_row_spacing",
            "adjacent_row_stagger_fraction",
            "standard_absorber_material",
            "terminal_foil_material",
        },
        "sampling_structure",
    )

    _require_exact_keys(
        material_properties,
        {
            "average_density",
            "relative_volume",
            "effective_critical_energy",
        },
        "material_properties",
    )

    _require_exact_keys(
        material_depth,
        {
            "radiation_lengths",
            "interaction_lengths",
        },
        "material_depth",
    )

    _require_exact_keys(
        coordinate_system,
        {
            "origin",
            "positive_z_direction",
            "theta_reference_axis",
        },
        "coordinate_system",
    )

    # ------------------------------------------------------------------
    # Nested material composition
    # ------------------------------------------------------------------

    relative_volume = _require_mapping(
        material_properties["relative_volume"],
        "material_properties.relative_volume",
    )

    _require_exact_keys(
        relative_volume,
        {
            "lead",
            "scintillating_fiber",
            "optical_glue",
        },
        "material_properties.relative_volume",
    )

    # ------------------------------------------------------------------
    # Fiber-axis sequence
    # ------------------------------------------------------------------

    raw_fiber_axes = readout["superlayer_fiber_axes"]

    if not isinstance(raw_fiber_axes, list):
        raise GeometryConfigError(
            "readout.superlayer_fiber_axes "
            "must be a YAML sequence"
        )

    superlayer_fiber_axes = tuple(raw_fiber_axes)

    # ------------------------------------------------------------------
    # Construct immutable geometry components
    # ------------------------------------------------------------------

    try:
        return ECALGeometry(
            active_volume=ActiveVolume(
                width_x_mm=active_volume["width_x"],
                width_y_mm=active_volume["width_y"],
                depth_z_mm=active_volume["depth_z"],
            ),
            readout=ReadoutGeometry(
                number_of_superlayers=(
                    readout["number_of_superlayers"]
                ),
                number_of_layers=readout["number_of_layers"],
                cells_per_layer=readout["cells_per_layer"],
                cell_pitch_mm=readout["cell_pitch"],
                photomultipliers=readout["photomultipliers"],
                anodes_per_photomultiplier=(
                    readout["anodes_per_photomultiplier"]
                ),
                approximate_fibers_per_cell=(
                    readout["approximate_fibers_per_cell"]
                ),
                superlayer_fiber_axes=superlayer_fiber_axes,
            ),
            sampling_structure=SamplingStructure(
                superlayer_thickness_mm=(
                    sampling_structure[
                        "superlayer_thickness"
                    ]
                ),
                absorber_foils_per_superlayer=(
                    sampling_structure[
                        "absorber_foils_per_superlayer"
                    ]
                ),
                absorber_foil_thickness_mm=(
                    sampling_structure[
                        "absorber_foil_thickness"
                    ]
                ),
                fiber_planes_per_superlayer=(
                    sampling_structure[
                        "fiber_planes_per_superlayer"
                    ]
                ),
                fiber_diameter_mm=(
                    sampling_structure["fiber_diameter"]
                ),
                fiber_horizontal_pitch_mm=(
                    sampling_structure[
                        "fiber_horizontal_pitch"
                    ]
                ),
                fiber_row_spacing_mm=(
                    sampling_structure[
                        "fiber_row_spacing"
                    ]
                ),
                adjacent_row_stagger_fraction=(
                    sampling_structure[
                        "adjacent_row_stagger_fraction"
                    ]
                ),
                standard_absorber_material=(
                    sampling_structure[
                        "standard_absorber_material"
                    ]
                ),
                terminal_foil_material=(
                    sampling_structure[
                        "terminal_foil_material"
                    ]
                ),
            ),
            material_properties=MaterialProperties(
                average_density_g_cm3=(
                    material_properties["average_density"]
                ),
                relative_volume_lead=relative_volume["lead"],
                relative_volume_scintillating_fiber=(
                    relative_volume["scintillating_fiber"]
                ),
                relative_volume_optical_glue=(
                    relative_volume["optical_glue"]
                ),
                effective_critical_energy_mev=(
                    material_properties[
                        "effective_critical_energy"
                    ]
                ),
            ),
            material_depth=MaterialDepth(
                total_depth_x0=(
                    material_depth["radiation_lengths"]
                ),
                total_depth_lambda_i=(
                    material_depth["interaction_lengths"]
                ),
            ),
            coordinate_system=CoordinateSystem(
                origin=coordinate_system["origin"],
                positive_z_direction=(
                    coordinate_system[
                        "positive_z_direction"
                    ]
                ),
                theta_reference_axis=(
                    coordinate_system[
                        "theta_reference_axis"
                    ]
                ),
            ),
        )

    except (TypeError, ValueError) as exc:
        raise GeometryConfigError(
            f"Invalid geometry values in {path}: {exc}"
        ) from exc