import pytest

from afes.config import ROOT_DIR


@pytest.fixture(scope="session")
def get_sample_data_path():
    return ROOT_DIR / "tests" / "fixtures" / "data"
