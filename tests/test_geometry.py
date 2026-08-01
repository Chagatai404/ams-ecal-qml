from pathlib import Path

import pytest
import yaml

from ams_ecal.geometry import (
    ECALGeometry,
    GeometryConfigError,
    load_geometry,
)

CONFIG_PATH = Path(__file__).parents[1] / "configs" / "geometry.yaml"


def valid_geometry_values() -> dict[str, object]:
    return {
        "width_x_mm": 648.0,
        "width_y_mm": 648.0,
        "depth_z_mm": 166.5,
        "number_of_superlayers": 9,
        "number_of_layers": 18,
        "cells_per_layer": 72,
        "cell_pitch_mm": 9.0,
        "total_depth_x0": 17.0,
        "total_depth_lambda_i": 0.6,
        "origin": "front_face_center",
        "positive_z_direction": "into_ecal",
        "theta_reference_axis": "positive_z",
    }


def write_modified_config(tmp_path: Path, change) -> Path:
    config = yaml.safe_load(CONFIG_PATH.read_text(encoding="utf-8"))
    change(config)
    path = tmp_path / "geometry.yaml"
    path.write_text(yaml.safe_dump(config), encoding="utf-8")
    return path


def test_loads_documented_geometry() -> None:
    geometry = load_geometry(CONFIG_PATH)

    assert geometry.width_x_mm == pytest.approx(648.0)
    assert geometry.width_y_mm == pytest.approx(648.0)
    assert geometry.depth_z_mm == pytest.approx(166.5)
    assert geometry.number_of_superlayers == 9
    assert geometry.number_of_layers == 18
    assert geometry.cells_per_layer == 72
    assert geometry.cell_pitch_mm == pytest.approx(9.0)
    assert geometry.total_depth_x0 == pytest.approx(17.0)
    assert geometry.total_depth_lambda_i == pytest.approx(0.6)


def test_derives_geometry_invariants() -> None:
    geometry = load_geometry(CONFIG_PATH)

    assert geometry.total_cells == 1296
    assert geometry.mean_readout_slice_thickness_mm == pytest.approx(9.25)
    assert len(geometry.uniform_layer_centers_z_mm) == 18
    assert geometry.uniform_layer_centers_z_mm[0] == pytest.approx(4.625)
    assert geometry.uniform_layer_centers_z_mm[-1] == pytest.approx(161.875)
    assert geometry.x_bounds_mm == pytest.approx((-324.0, 324.0))
    assert geometry.y_bounds_mm == pytest.approx((-324.0, 324.0))
    assert geometry.z_bounds_mm == pytest.approx((0.0, 166.5))


@pytest.mark.parametrize(
    ("field", "value", "error_type", "message"),
    [
        ("depth_z_mm", 0.0, ValueError, "finite and positive"),
        ("total_depth_x0", float("nan"), ValueError, "finite and positive"),
        ("cells_per_layer", True, TypeError, "must be an integer"),
        ("number_of_layers", 17, ValueError, "twice"),
        ("width_x_mm", 647.0, ValueError, "cells_per_layer"),
        ("origin", "center", ValueError, "front_face_center"),
    ],
)
def test_rejects_invalid_geometry_values(
    field: str,
    value: object,
    error_type: type[Exception],
    message: str,
) -> None:
    values = valid_geometry_values()
    values[field] = value

    with pytest.raises(error_type, match=message):
        ECALGeometry(**values)


def test_rejects_missing_config_file(tmp_path: Path) -> None:
    with pytest.raises(FileNotFoundError, match="not found"):
        load_geometry(tmp_path / "missing.yaml")


def test_rejects_malformed_yaml(tmp_path: Path) -> None:
    path = tmp_path / "geometry.yaml"
    path.write_text("active_volume: [", encoding="utf-8")

    with pytest.raises(GeometryConfigError, match="Could not parse"):
        load_geometry(path)


def test_rejects_unsupported_schema_version(tmp_path: Path) -> None:
    path = write_modified_config(
        tmp_path,
        lambda config: config.__setitem__("schema_version", 2),
    )

    with pytest.raises(GeometryConfigError, match="Unsupported"):
        load_geometry(path)


def test_rejects_wrong_units(tmp_path: Path) -> None:
    def change(config: dict[str, object]) -> None:
        config["units"]["length"] = "cm"

    path = write_modified_config(tmp_path, change)

    with pytest.raises(GeometryConfigError, match="units must equal"):
        load_geometry(path)


def test_rejects_missing_required_key(tmp_path: Path) -> None:
    def change(config: dict[str, object]) -> None:
        del config["readout"]["cell_pitch"]

    path = write_modified_config(tmp_path, change)

    with pytest.raises(GeometryConfigError, match="missing keys"):
        load_geometry(path)


def test_rejects_unexpected_key(tmp_path: Path) -> None:
    def change(config: dict[str, object]) -> None:
        config["active_volume"]["width_z"] = 123.0

    path = write_modified_config(tmp_path, change)

    with pytest.raises(GeometryConfigError, match="unexpected keys"):
        load_geometry(path)