"""Mean longitudinal electromagnetic-shower development in the AMS ECAL.

The gamma profile implemented here is a phenomenological description of the
mean energy deposition. It is not a first-principles QED theorem. The physical
chain is bremsstrahlung and pair production, followed by a branching cascade,
followed by a gamma-profile approximation calibrated against simulation/data.

This block intentionally models only the mean electron/positron profile.
Shower-to-shower fluctuations and sampling-calorimeter corrections belong to
the stochastic FastMC block, where their correlations can be handled together.
"""

from dataclasses import dataclass
from math import exp, isfinite, lgamma, log
from typing import Literal

from scipy.special import gammainc

from ams_ecal.fastmc_config import LongitudinalEMConfig
from ams_ecal.geometry import ECALGeometry

ElectromagneticParticleType = Literal["electron", "positron"]

_SUPPORTED_PARTICLES = {"electron", "positron"}


def _validate_primary_energy(primary_energy_mev: object) -> float:
    """Return a finite positive primary energy as a float."""

    if isinstance(primary_energy_mev, bool) or not isinstance(
        primary_energy_mev,
        int | float,
    ):
        raise TypeError("primary_energy_mev must be a real number")

    if not isfinite(primary_energy_mev):
        raise ValueError("primary_energy_mev must be finite")

    if primary_energy_mev <= 0:
        raise ValueError("primary_energy_mev must be positive")

    return float(primary_energy_mev)


def _validate_particle_type(
    particle_type: object,
) -> ElectromagneticParticleType:
    """Require an electron or positron for the electromagnetic model."""

    if not isinstance(particle_type, str):
        raise TypeError("particle_type must be a string")

    if particle_type not in _SUPPORTED_PARTICLES:
        raise ValueError("particle_type must be 'electron' or 'positron'")

    return particle_type


@dataclass(frozen=True, slots=True)
class AMSLongitudinalGammaModel:
    """Detector-specific mean longitudinal model for electron/positron showers.

    AMS describes the longitudinal profile with a gamma distribution and finds
    a detector-specific constant rate beta = 0.65. For a primary energy E, the
    mean shower maximum is predicted using the PDG electron relation

        T = ln(E / E_c) - 0.5,

    with the configurable offset written generally. The gamma shape is then
    alpha = 1 + beta*T, ensuring that its mode (alpha - 1)/beta equals T.

    The continuous unit-normalized profile is integrated over the geometry's
    finite layer intervals. Fractions are never renormalized to the 17 X_0
    detector depth, so the missing tail remains physical longitudinal leakage.
    """

    config: LongitudinalEMConfig
    geometry: ECALGeometry

    def __post_init__(self) -> None:
        if not isinstance(self.config, LongitudinalEMConfig):
            raise TypeError("config must be a LongitudinalEMConfig")

        if not isinstance(self.geometry, ECALGeometry):
            raise TypeError("geometry must be an ECALGeometry")

    @property
    def critical_energy_mev(self) -> float:
        """Return the effective ECAL critical energy from detector geometry."""

        return self.geometry.material_properties.effective_critical_energy_mev

    def shower_max_depth_x0(self, primary_energy_mev: float) -> float:
        """Return the predicted mean shower-maximum depth in X_0."""

        energy_mev = _validate_primary_energy(primary_energy_mev)
        shower_max_x0 = (
            log(energy_mev / self.critical_energy_mev)
            + self.config.shower_max_offset_x0
        )

        # The PDG high-energy approximation is not a valid cascade model when
        # it predicts a maximum at or before the calorimeter front face.
        if shower_max_x0 <= 0:
            raise ValueError(
                "primary_energy_mev is below the valid domain of the "
                "longitudinal gamma model"
            )

        return shower_max_x0

    def shape_parameter(self, primary_energy_mev: float) -> float:
        """Return gamma shape alpha for the requested primary energy.
           Since gamma profile uses T = (α − 1)/β, then α = 1 + βT.
        """

        return 1.0 + (
            self.config.gamma_rate
            * self.shower_max_depth_x0(primary_energy_mev)
        )

    def energy_density(
        self,
        depth_x0: float,
        primary_energy_mev: float,
    ) -> float:
        """Return normalized mean energy-deposition density at one depth.

        The result is a fractional energy density per radiation length. The
        logarithmic evaluation avoids overflow for large shape parameters.
        """

        if isinstance(depth_x0, bool) or not isinstance(
            depth_x0,
            int | float,
        ):
            raise TypeError("depth_x0 must be a real number")

        if not isfinite(depth_x0):
            raise ValueError("depth_x0 must be finite")

        if depth_x0 < 0:
            raise ValueError("depth_x0 must be nonnegative")

        alpha = self.shape_parameter(primary_energy_mev)

        if depth_x0 == 0:
            # The validated model domain guarantees alpha > 1.
            return 0.0

        beta = self.config.gamma_rate
        log_density = (
            log(beta)
            + (alpha - 1.0) * log(beta * depth_x0)
            - beta * depth_x0
            - lgamma(alpha)
        )
        return exp(log_density)

    def layer_energy_fractions(
        self,
        primary_energy_mev: float,
        particle_type: ElectromagneticParticleType = "electron",
    ) -> tuple[float, ...]:
        """Integrate the mean profile over every finite readout interval."""

        _validate_particle_type(particle_type)
        alpha = self.shape_parameter(primary_energy_mev)
        beta = self.config.gamma_rate

        fractions = tuple(
            float(
                gammainc(alpha, beta * upper_x0)
                - gammainc(alpha, beta * lower_x0)
            )
            for lower_x0, upper_x0 in self.geometry.uniform_layer_bounds_x0
        )

        # Small negative roundoff is not expected from monotonic CDF values;
        # fail loudly rather than hiding a numerical problem by clipping.
        if any(not isfinite(value) or value < 0 for value in fractions):
            raise ArithmeticError(
                "computed layer fractions must be finite and nonnegative"
            )

        return fractions

    def mean_layer_energies_mev(
        self,
        primary_energy_mev: float,
        particle_type: ElectromagneticParticleType = "electron",
    ) -> tuple[float, ...]:
        """Return ideal mean energy assigned to each longitudinal sampling."""

        energy_mev = _validate_primary_energy(primary_energy_mev)
        return tuple(
            energy_mev * fraction
            for fraction in self.layer_energy_fractions(
                energy_mev,
                particle_type,
            )
        )

    def contained_fraction(
        self,
        primary_energy_mev: float,
        particle_type: ElectromagneticParticleType = "electron",
    ) -> float:
        """Return mean longitudinal energy fraction inside the finite ECAL."""

        return sum(
            self.layer_energy_fractions(primary_energy_mev, particle_type)
        )

    def leakage_fraction(
        self,
        primary_energy_mev: float,
        particle_type: ElectromagneticParticleType = "electron",
    ) -> float:
        """Return the mean profile tail beyond the finite ECAL depth."""

        return 1.0 - self.contained_fraction(
            primary_energy_mev,
            particle_type,
        )
