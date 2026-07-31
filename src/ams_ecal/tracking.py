from dataclasses import dataclass

import numpy as np

from ams_ecal.geometry import ECALGeometry


@dataclass(frozen=True)
class TrackState:
    x_mm: float
    y_mm: float
    z_mm: float
    theta_rad: float
    phi_rad: float

    @property
    def direction(self) -> np.ndarray:
        return np.array(
            [
                np.sin(self.theta_rad) * np.cos(self.phi_rad),
                np.sin(self.theta_rad) * np.sin(self.phi_rad),
                np.cos(self.theta_rad),
            ],
            dtype=float,
        )


@dataclass(frozen=True)
class TrackProjection:
    layer_z_mm: np.ndarray
    x_mm: np.ndarray
    y_mm: np.ndarray
    slant_depth_mm: np.ndarray
    inside_active_volume: np.ndarray


class TrackProjector:
    def __init__(self, geometry: ECALGeometry) -> None:
        self.geometry = geometry

    def project(self, track: TrackState) -> TrackProjection:
        direction = track.direction
        ux, uy, uz = direction

        if np.isclose(uz, 0.0):
            raise ValueError("Track direction is parallel to the ECAL front face.")

        layer_z = self.geometry.layer_centers_z_mm
        path_parameter = (layer_z - track.z_mm) / uz

        x = track.x_mm + path_parameter * ux
        y = track.y_mm + path_parameter * uy

        inside = (
            (x >= self.geometry.x_min_mm)
            & (x < self.geometry.x_max_mm)
            & (y >= self.geometry.y_min_mm)
            & (y < self.geometry.y_max_mm)
            & (path_parameter >= 0)
        )

        return TrackProjection(
            layer_z_mm=layer_z,
            x_mm=x,
            y_mm=y,
            slant_depth_mm=np.abs(path_parameter),
            inside_active_volume=inside,
        )