"""Validated configuration for the physics-informed FastMC.

Only parameters needed by implemented FastMC blocks belong here. Detector and
material properties remain in the geometry configuration so that scientific
quantities such as the effective critical energy have one source of truth.
"""

from collections.abc import Mapping
from dataclasses import dataclass
from math import isfinite
from pathlib import Path

import yaml

EXPECTED_FASTMC_SCHEMA_VERSION = 2


class FastMCConfigError(ValueError):
    """Raised when a FastMC configuration is malformed or unsupported."""


def _validate_positive_real(value: object, name: str) -> None:
    """Require a finite, strictly positive real model parameter."""

    if isinstance(value, bool) or not isinstance(value, int | float):
        raise TypeError(f"{name} must be a real number")

    if not isfinite(value) or value <= 0:
        raise ValueError(f"{name} must be finite and positive")


def _validate_finite_real(value: object, name: str) -> None:
    """Require a finite real model parameter."""

    if isinstance(value, bool) or not isinstance(value, int | float):
        raise TypeError(f"{name} must be a real number")

    if not isfinite(value):
        raise ValueError(f"{name} must be finite")


@dataclass(frozen=True, slots=True)
class LongitudinalEMConfig:
    """Scientific parameters for the mean electromagnetic shower profile.

    ``gamma_rate`` is the detector-specific beta parameter reported by AMS.
    ``shower_max_offset_x0`` is the additive electron/positron correction in
    ``t_max = ln(E / E_c) + offset``.
    """

    gamma_rate: float
    shower_max_offset_x0: float

    def __post_init__(self) -> None:
        _validate_positive_real(self.gamma_rate, "gamma_rate")
        _validate_finite_real(
            self.shower_max_offset_x0,
            "shower_max_offset_x0",
        )


@dataclass(frozen=True, slots=True)
class LateralEMConfig:
    """Scientific parameters for the mean electromagnetic lateral profile.

    The parameters reproduce the AMS test-beam relation

    ``R_layer = (p0 * ln(E / E_unit) + p1) * layer_index**2 + B``.

    ``R_layer`` is expressed in calibration-cell units.  The calibration paper
    describes one such cell as approximately half a Moliere radius, which is
    recorded explicitly by ``calibration_cell_moliere_fraction``.
    """

    scale_log_slope: float
    scale_log_intercept: float
    entrance_scale_cells: float
    calibration_cell_moliere_fraction: float
    calibration_energy_unit_mev: float

    def __post_init__(self) -> None:
        _validate_finite_real(self.scale_log_slope, "scale_log_slope")
        _validate_finite_real(
            self.scale_log_intercept,
            "scale_log_intercept",
        )
        _validate_positive_real(
            self.entrance_scale_cells,
            "entrance_scale_cells",
        )
        _validate_positive_real(
            self.calibration_cell_moliere_fraction,
            "calibration_cell_moliere_fraction",
        )
        _validate_positive_real(
            self.calibration_energy_unit_mev,
            "calibration_energy_unit_mev",
        )


@dataclass(frozen=True, slots=True)
class FastMCConfig:
    """Top-level configuration for the implemented FastMC components."""

    longitudinal_em: LongitudinalEMConfig
    lateral_em: LateralEMConfig

    def __post_init__(self) -> None:
        if not isinstance(self.longitudinal_em, LongitudinalEMConfig):
            raise TypeError("longitudinal_em must be a LongitudinalEMConfig")

        if not isinstance(self.lateral_em, LateralEMConfig):
            raise TypeError("lateral_em must be a LateralEMConfig")


def _require_mapping(value: object, context: str) -> Mapping[object, object]:
    """Require a YAML mapping at one named configuration location."""

    if not isinstance(value, Mapping):
        raise FastMCConfigError(f"{context} must be a YAML mapping")

    return value


def _require_exact_keys(
    mapping: Mapping[object, object],
    expected_keys: set[str],
    context: str,
) -> None:
    """Reject missing or unknown keys in the strict scientific schema."""

    actual_keys = set(mapping)
    missing_keys = expected_keys - actual_keys
    unexpected_keys = actual_keys - expected_keys
    problems: list[str] = []

    if missing_keys:
        problems.append(f"missing keys: {sorted(missing_keys)}")

    if unexpected_keys:
        problems.append(f"unexpected keys: {sorted(map(str, unexpected_keys))}")

    if problems:
        raise FastMCConfigError(f"{context} has " + "; ".join(problems))


def load_fastmc_config(config_path: str | Path) -> FastMCConfig:
    """Load and validate the versioned FastMC configuration."""

    path = Path(config_path)

    if not path.is_file():
        raise FileNotFoundError(f"FastMC configuration not found: {path}")

    try:
        raw_config = yaml.safe_load(path.read_text(encoding="utf-8"))
    except yaml.YAMLError as exc:
        raise FastMCConfigError(
            f"Could not parse FastMC configuration {path}: {exc}"
        ) from exc

    config = _require_mapping(raw_config, "FastMC configuration root")
    _require_exact_keys(
        config,
        {"schema_version", "longitudinal_em", "lateral_em"},
        "FastMC configuration root",
    )

    schema_version = config["schema_version"]

    if isinstance(schema_version, bool) or not isinstance(schema_version, int):
        raise FastMCConfigError("schema_version must be an integer")

    if schema_version != EXPECTED_FASTMC_SCHEMA_VERSION:
        raise FastMCConfigError(
            "Unsupported FastMC schema_version "
            f"{schema_version}; expected {EXPECTED_FASTMC_SCHEMA_VERSION}"
        )

    longitudinal_em = _require_mapping(
        config["longitudinal_em"],
        "longitudinal_em",
    )
    _require_exact_keys(
        longitudinal_em,
        {"gamma_rate", "shower_max_offset_x0"},
        "longitudinal_em",
    )

    lateral_em = _require_mapping(
        config["lateral_em"],
        "lateral_em",
    )
    _require_exact_keys(
        lateral_em,
        {
            "scale_log_slope",
            "scale_log_intercept",
            "entrance_scale_cells",
            "calibration_cell_moliere_fraction",
            "calibration_energy_unit_mev",
        },
        "lateral_em",
    )

    return FastMCConfig(
        longitudinal_em=LongitudinalEMConfig(
            gamma_rate=longitudinal_em["gamma_rate"],
            shower_max_offset_x0=longitudinal_em["shower_max_offset_x0"],
        ),
        lateral_em=LateralEMConfig(
            scale_log_slope=lateral_em["scale_log_slope"],
            scale_log_intercept=lateral_em["scale_log_intercept"],
            entrance_scale_cells=lateral_em["entrance_scale_cells"],
            calibration_cell_moliere_fraction=lateral_em[
                "calibration_cell_moliere_fraction"
            ],
            calibration_energy_unit_mev=lateral_em["calibration_energy_unit_mev"],
        ),
    )
