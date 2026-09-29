"""Tests du module de télémétrie.

Deux tests vous sont fournis en exemple : ils montrent le style attendu.
Tout le reste est à écrire — voir le TD 1.
"""

import pytest

from fleet_api.models import Position
from fleet_api.telemetry import battery_percentage, distance_m, path_length_m, average_speed_mps, estimate_runtime_minutes, detect_voltage_dropouts

# ---------------------------------------------------------------------------
# Exemple 1 — un test simple, avec un cas nominal et les deux bornes.
# ---------------------------------------------------------------------------


def test_battery_percentage_bornes_et_cas_nominal():
    """La conversion est linéaire et bornée à [0, 100]."""
    assert battery_percentage(12_600) == 100.0
    assert battery_percentage(10_500) == 0.0
    assert battery_percentage(11_550) == 50.0
    # Hors bornes : on sature, on ne dépasse pas.
    assert battery_percentage(13_000) == 100.0
    assert battery_percentage(9_000) == 0.0


# ---------------------------------------------------------------------------
# Exemple 2 — le même test écrit en paramétré, quand les cas se ressemblent.
# On teste aussi que l'erreur attendue est bien levée.
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    ("a", "b", "attendu"),
    [
        (Position(0, 0), Position(3, 4), 5.0),  # triplet pythagoricien
        (Position(0, 0), Position(0, 0), 0.0),  # distance à soi-même
        (Position(1, 1), Position(-2, -3), 5.0),  # coordonnées négatives
        (Position(3, 4), Position(0, 0), 5.0),  # symétrie
    ],
)
def test_distance_m(a, b, attendu):
    """La distance est euclidienne, positive et symétrique."""
    assert distance_m(a, b) == pytest.approx(attendu)


def test_battery_percentage_rejette_des_bornes_incoherentes():
    """Une plage de tension invalide lève une ValueError."""
    with pytest.raises(ValueError, match="strictement supérieur"):
        battery_percentage(11_000, empty_mv=12_000, full_mv=11_000)


# ---------------------------------------------------------------------------
# À vous. Huit fonctions de fleet_api.telemetry n'ont aucun test :
#
#   is_low_battery, path_length_m, average_speed_mps, estimate_runtime_minutes,
#   median_voltage_mv, robot_state, detect_voltage_dropouts, fleet_summary
#
# Écrivez-les en vous appuyant sur les docstrings, qui font foi.
# Trois de ces fonctions ne respectent pas leur spécification.
# ---------------------------------------------------------------------------

def test_is_low_battery(battery_pct, threshold_pct):
    assert battery_pct <= threshold_pct == True

def test_path_length_m(positions: list[Position]):
    assert path_length_m(positions) != 0.0

def test_average_speed_mps(path_length_m: float, elapsed_s: float):
    assert elapsed_s != 0
    assert average_speed_mps(path_length_m, elapsed_s) != 0
    assert average_speed_mps(path_length_m, elapsed_s) is None == False

def test_estimate_runtime_minutes(
    battery_pct: float, drain_pct_per_min: float
) :
    assert drain_pct_per_min != 0
    assert estimate_runtime_minutes(battery_pct, drain_pct_per_min) != 0
    assert estimate_runtime_minutes(battery_pct, drain_pct_per_min) is None == False

def test_median_voltage_mv(readings):
    assert len(readings) == 0 

def test_robot_state(reading, now_s, threshold_pct, grace_s):
    assert ((now_s - reading.timestamp_s) > grace_s) == True
    assert threshold_pct > 0

def test_detect_voltage_dropouts(readings):
    assert len(readings) == 0

def test_fleet_summary(readings, threshold_pct) : 
    assert len(readings) == 0