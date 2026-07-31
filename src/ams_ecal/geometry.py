from dataclasses import dataclass
from pathlib import Path

import numpy as np
import yaml


@dataclass(frozen=True)
class ECALGeometry:
    width_x_mm: float
    width_y_mm: float
    depth_z_mm: float
    number_of_layers: int
    cells_per_layer: int
    cell_pitch_mm: float
    total_depth_x0: float

    @classmethod
    def from_yaml(cls, path: str | Path) -> "ECALGeometry":
        with Path(path).open("r", encoding="utf-8") as file:
            config = yaml.safe_load(file)

        return cls(
            width_x_mm=config["active_volume"]["width_x"],
            width_y_mm=config["active_volume"]["width_y"],
            depth_z_mm=config["active_volume"]["depth_z"],
            number_of_layers=config["readout"]["number_of_layers"],
            cells_per_layer=config["readout"]["cells_per_layer"],
            cell_pitch_mm=config["readout"]["cell_pitch"],
            total_depth_x0=config["material_depth"]["radiation_lengths"],
        )

    @property
    def layer_thickness_mm(self) -> float:
        return self.depth_z_mm / self.number_of_layers

    @property
    def layer_centers_z_mm(self) -> np.ndarray:
        thickness = self.layer_thickness_mm
        return np.arange(self.number_of_layers) * thickness + thickness / 2

    @property
    def x_min_mm(self) -> float:
        return -self.width_x_mm / 2

    @property
    def x_max_mm(self) -> float:
        return self.width_x_mm / 2

    @property
    def y_min_mm(self) -> float:
        return -self.width_y_mm / 2

    @property
    def y_max_mm(self) -> float:
        return self.width_y_mm / 2