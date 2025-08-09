import ipaddress
import os
import sys
import pytest

# Ensure the repository root is on the import path when tests are executed.
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from Network_Calculator import NetworkCalculator


def create_calc():
    """Helper to create a /16 network calculator for tests."""
    return NetworkCalculator("10.0.0.0", "16")


@pytest.mark.parametrize(
    "host_index,expected",
    [
        (255, "10.0.0.255"),
        (256, "10.0.1.0"),
        (257, "10.0.1.1"),
        (511, "10.0.1.255"),
        (512, "10.0.2.0"),
        (513, "10.0.2.1"),
    ],
)
def test_get_host_values(host_index, expected):
    calc = create_calc()
    assert calc.get_host(host_index) == expected


@pytest.mark.parametrize("host_index", [255, 256, 257, 511, 512, 513])
def test_get_host_returns_valid_ip(host_index):
    """Ensure get_host generates syntactically valid IPv4 addresses."""
    calc = create_calc()
    ipaddress.ip_address(calc.get_host(host_index))
