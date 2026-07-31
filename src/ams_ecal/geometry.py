from collections.abc import Mapping
from dataclasses import dataclass
from math import isclose, isfinite
from pathlib import Path

import yaml


EXPECTED_SCHEMA_VERSION = 1
EXPECTED_UNITS = {
    "length": "mm",
    "angle": "rad",
    "energy": "MeV",
}


class GeometryConfigError(ValueError):
    """Raised when a geometry configuration is malformed or unsupported."""


@dataclass(frozen=True, slots=True)
class ECALGeometry:
    """Validated simplified geometry of the AMS-02 ECAL active volume."""

    width_x_mm: float
    width_y_mm: float
    depth_z_mm: float

    number_of_superlayers: int
    number_of_layers: int
    cells_per_layer: int
    cell_pitch_mm: float

    total_depth_x0: float
    total_depth_lambda_i: float

    origin: str
    positive_z_direction: str
    theta_reference_axis: str

    def __post_init__(self) -> None:
        positive_lengths = {
            "width_x_mm": self.width_x_mm,
            "width_y_mm": self.width_y_mm,
            "depth_z_mm": self.depth_z_mm,
            "cell_pitch_mm": self.cell_pitch_mm,
            "total_depth_x0": self.total_depth_x0,
            "total_depth_lambda_i": self.total_depth_lambda_i,
        }

        for name, value in positive_lengths.items():
            if isinstance(value, bool) or not isinstance(value, int | float):
                raise TypeError(f"{name} must be a real number")

            if not isfinite(value) or value <= 0:
                raise ValueError(f"{name} must be finite and positive")

        positive_counts = {
            "number_of_superlayers": self.number_of_superlayers,
            "number_of_layers": self.number_of_layers,
            "cells_per_layer": self.cells_per_layer,
        }

        for name, value in positive_counts.items():
            if isinstance(value, bool) or not isinstance(value, int):
                raise TypeError(f"{name} must be an integer")

            if value <= 0:
                raise ValueError(f"{name} must be positive")

        if self.number_of_layers != 2 * self.number_of_superlayers:
            raise ValueError(
                "number_of_layers must equal twice number_of_superlayers"
            )

        expected_width_mm = self.cells_per_layer * self.cell_pitch_mm

        if not isclose(self.width_x_mm, expected_width_mm):
            raise ValueError(
                "width_x_mm must equal cells_per_layer * cell_pitch_mm"
            )

        if not isclose(self.width_y_mm, expected_width_mm):
            raise ValueError(
                "width_y_mm must equal cells_per_layer * cell_pitch_mm"
            )

        expected_conventions = {
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

        for name, (actual, expected) in expected_conventions.items():
            if not isinstance(actual, str):
                raise TypeError(f"{name} must be a string")

            if actual != expected:
                raise ValueError(
                    f"{name} must be {expected!r}, got {actual!r}"
                )

    @property
    def total_cells(self) -> int:
        """Return the total number of readout cells."""

        return self.number_of_layers * self.cells_per_layer

    @property
    def mean_readout_slice_thickness_mm(self) -> float:
        """Return the active depth divided uniformly among readout layers.

        This is a simplified geometrical quantity, not the documented
        thickness of an individual physical material layer.
        """

        return self.depth_z_mm / self.number_of_layers

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
    """Load and validate an ECAL geometry from a versioned YAML file."""

    path = Path(config_path)

    if not path.is_file():
        raise FileNotFoundError(f"Geometry configuration not found: {path}")

    try:
        raw_config = yaml.safe_load(path.read_text(encoding="utf-8"))
    except yaml.YAMLError as exc:
        raise GeometryConfigError(
            f"Could not parse geometry configuration {path}: {exc}"
        ) from exc

    config = _require_mapping(raw_config, "geometry configuration root")
    _require_exact_keys(
        config,
        {
            "schema_version",
            "units",
            "active_volume",
            "readout",
            "material_depth",
            "coordinate_system",
        },
        "geometry configuration root",
    )

    schema_version = config["schema_version"]

    if isinstance(schema_version, bool) or not isinstance(schema_version, int):
        raise GeometryConfigError("schema_version must be an integer")

    if schema_version != EXPECTED_SCHEMA_VERSION:
        raise GeometryConfigError(
            "Unsupported geometry schema_version "
            f"{schema_version}; expected {EXPECTED_SCHEMA_VERSION}"
        )

    units = _require_mapping(config["units"], "units")
    _require_exact_keys(units, set(EXPECTED_UNITS), "units")

    if dict(units) != EXPECTED_UNITS:
        raise GeometryConfigError(
            f"units must equal {EXPECTED_UNITS}, got {dict(units)}"
        )

    active_volume = _require_mapping(config["active_volume"], "active_volume")
    readout = _require_mapping(config["readout"], "readout")
    material_depth = _require_mapping(
        config["material_depth"], "material_depth"
    )
    coordinate_system = _require_mapping(
        config["coordinate_system"], "coordinate_system"
    )

    _require_exact_keys(
        active_volume,
        {"width_x", "width_y", "depth_z"},
        "active_volume",
    )
    _require_exact_keys(
        readout,
        {
            "number_of_superlayers",
            "number_of_layers",
            "cells_per_layer",
            "cell_pitch",
        },
        "readout",
    )
    _require_exact_keys(
        material_depth,
        {"radiation_lengths", "interaction_lengths"},
        "material_depth",
    )
    _require_exact_keys(
        coordinate_system,
        {"origin", "positive_z_direction", "theta_reference_axis"},
        "coordinate_system",
    )

    try:
        return ECALGeometry(
            width_x_mm=active_volume["width_x"],
            width_y_mm=active_volume["width_y"],
            depth_z_mm=active_volume["depth_z"],
            number_of_superlayers=readout["number_of_superlayers"],
            number_of_layers=readout["number_of_layers"],
            cells_per_layer=readout["cells_per_layer"],
            cell_pitch_mm=readout["cell_pitch"],
            total_depth_x0=material_depth["radiation_lengths"],
            total_depth_lambda_i=material_depth["interaction_lengths"],
            origin=coordinate_system["origin"],
            positive_z_direction=coordinate_system["positive_z_direction"],
            theta_reference_axis=coordinate_system["theta_reference_axis"],
        )
    except (TypeError, ValueError) as exc:
        raise GeometryConfigError(
            f"Invalid geometry values in {path}: {exc}"
        ) from exc