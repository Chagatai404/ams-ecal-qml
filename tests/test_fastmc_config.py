from dataclasses import FrozenInstanceError, replace
from pathlib import Path

import pytest

from ams_ecal.fastmc_config import (
    EXPECTED_FASTMC_SCHEMA_VERSION,
    FastMCConfig,
    FastMCConfigError,
    LongitudinalEMConfig,
    load_fastmc_config,
)

CONFIG_PATH = Path(__file__).parents[1] / "configs" / "fastmc.yaml"


def test_loads_versioned_longitudinal_configuration() -> None:
    config = load_fastmc_config(CONFIG_PATH)

    assert isinstance(config, FastMCConfig)
    assert config.longitudinal_em.gamma_rate == pytest.approx(0.65)
    assert config.longitudinal_em.shower_max_offset_x0 == pytest.approx(-0.5)


def test_longitudinal_configuration_is_immutable() -> None:
    config = load_fastmc_config(CONFIG_PATH)

    with pytest.raises(FrozenInstanceError):
        config.longitudinal_em.gamma_rate = 0.5


@pytest.mark.parametrize(
    ("field_name", "invalid_value", "error_type", "message"),
    [
        ("gamma_rate", True, TypeError, "must be a real number"),
        ("gamma_rate", "0.65", TypeError, "must be a real number"),
        ("gamma_rate", float("nan"), ValueError, "finite and positive"),
        ("gamma_rate", float("inf"), ValueError, "finite and positive"),
        ("gamma_rate", 0.0, ValueError, "finite and positive"),
        ("gamma_rate", -0.1, ValueError, "finite and positive"),
        (
            "shower_max_offset_x0",
            True,
            TypeError,
            "must be a real number",
        ),
        (
            "shower_max_offset_x0",
            float("nan"),
            ValueError,
            "must be finite",
        ),
    ],
)
def test_rejects_invalid_longitudinal_parameters(
    field_name: str,
    invalid_value: object,
    error_type: type[Exception],
    message: str,
) -> None:
    config = load_fastmc_config(CONFIG_PATH).longitudinal_em

    with pytest.raises(error_type, match=message):
        replace(config, **{field_name: invalid_value})


def test_rejects_invalid_top_level_component_type() -> None:
    with pytest.raises(
        TypeError,
        match="longitudinal_em must be a LongitudinalEMConfig",
    ):
        FastMCConfig(longitudinal_em=None)


def test_rejects_missing_configuration_file(tmp_path: Path) -> None:
    missing_path = tmp_path / "missing.yaml"

    with pytest.raises(FileNotFoundError, match="FastMC configuration"):
        load_fastmc_config(missing_path)


@pytest.mark.parametrize(
    ("contents", "message"),
    [
        (
            "schema_version: 1\n",
            "missing keys:.*longitudinal_em",
        ),
        (
            "schema_version: 1\nlongitudinal_em: {}\n",
            "missing keys",
        ),
        (
            "schema_version: 1\nlongitudinal_em: {gamma_rate: 0.65, shower_max_offset_x0: -0.5, typo: 1}\n",
            "unexpected keys:.*typo",
        ),
        (
            "schema_version: 2\nlongitudinal_em: {gamma_rate: 0.65, shower_max_offset_x0: -0.5}\n",
            "Unsupported FastMC schema_version 2",
        ),
    ],
)
def test_rejects_invalid_schema(
    tmp_path: Path,
    contents: str,
    message: str,
) -> None:
    config_path = tmp_path / "fastmc.yaml"
    config_path.write_text(contents, encoding="utf-8")

    with pytest.raises(FastMCConfigError, match=message):
        load_fastmc_config(config_path)


def test_exposes_expected_schema_version() -> None:
    assert EXPECTED_FASTMC_SCHEMA_VERSION == 1
    assert isinstance(
        LongitudinalEMConfig(gamma_rate=0.65, shower_max_offset_x0=-0.5),
        LongitudinalEMConfig,
    )
