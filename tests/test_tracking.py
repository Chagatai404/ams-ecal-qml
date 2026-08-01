from dataclasses import FrozenInstanceError
from math import pi, radians, sqrt, tau

import pytest

from ams_ecal.tracking import TrackState


def valid_track_values() -> dict[str, float]:
    return {
        "x0_mm": 10.0,
        "y0_mm": -20.0,
        "z0_mm": 0.0,
        "theta_rad": radians(10.0),
        "phi_rad": radians(30.0),
    }


def test_stores_reconstructed_track_state() -> None:
    track = TrackState(**valid_track_values())

    assert track.x0_mm == pytest.approx(10.0)
    assert track.y0_mm == pytest.approx(-20.0)
    assert track.z0_mm == pytest.approx(0.0)
    assert track.theta_rad == pytest.approx(radians(10.0))
    assert track.phi_rad == pytest.approx(radians(30.0))


def test_derives_unit_direction_vector() -> None:
    track = TrackState(**valid_track_values())

    direction_x, direction_y, direction_z = (
        track.direction_unit_vector
    )

    assert direction_x == pytest.approx(0.1503837332)
    assert direction_y == pytest.approx(0.0868240888)
    assert direction_z == pytest.approx(0.9848077530)

    magnitude = sqrt(
        direction_x**2 + direction_y**2 + direction_z**2
    )

    assert magnitude == pytest.approx(1.0)


def test_derives_transverse_slopes_wrt_z() -> None:
    track = TrackState(**valid_track_values())

    slope_x, slope_y = track.slopes_wrt_z

    assert slope_x == pytest.approx(0.1527036447)
    assert slope_y == pytest.approx(0.0881634904)


def test_vertical_track_has_zero_transverse_slopes() -> None:
    track = TrackState(
        x0_mm=10.0,
        y0_mm=-20.0,
        z0_mm=0.0,
        theta_rad=0.0,
        phi_rad=radians(120.0),
    )

    assert track.direction_unit_vector == pytest.approx(
        (0.0, 0.0, 1.0)
    )
    assert track.slopes_wrt_z == pytest.approx((0.0, 0.0))


def test_track_state_is_immutable() -> None:
    track = TrackState(**valid_track_values())

    with pytest.raises(FrozenInstanceError):
        track.x0_mm = 25.0


@pytest.mark.parametrize(
    ("field", "value", "error_type", "message"),
    [
        ("x0_mm", float("nan"), ValueError, "must be finite"),
        ("y0_mm", float("inf"), ValueError, "must be finite"),
        ("z0_mm", True, TypeError, "must be a real number"),
        ("theta_rad", -0.01, ValueError, "0 <= theta_rad"),
        ("theta_rad", pi / 2, ValueError, "0 <= theta_rad"),
        ("phi_rad", -0.01, ValueError, "0 <= phi_rad"),
        ("phi_rad", tau, ValueError, "0 <= phi_rad"),
    ],
)
def test_rejects_invalid_track_values(
    field: str,
    value: object,
    error_type: type[Exception],
    message: str,
) -> None:
    values = valid_track_values()
    values[field] = value

    with pytest.raises(error_type, match=message):
        TrackState(**values)