import math

import pytest

from afes.utils import get_human_readable_size


@pytest.mark.parametrize(
    "size, expected",
    [
        (1, "1.0 B"),
        (1024, "1.0 KiB"),
        (math.pow(1024, 2), "1.0 MiB"),
        (math.pow(1024, 3), "1.0 GiB"),
        (math.pow(1024, 4), "1.0 TiB"),
        (math.pow(1024, 5), "1.0 PiB"),
        (math.pow(1024, 6), "1.0 EiB"),
        (math.pow(1024, 7), "1.0 ZiB"),
    ],
)
def test_get_human_readable_size(size, expected):
    returned = get_human_readable_size(size)
    assert returned == expected
