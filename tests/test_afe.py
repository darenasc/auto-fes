from collections.abc import Iterable

import pandas as pd

from afes.afe import _get_descriptions, _get_files, explore_files


def test__get_files(get_sample_data_path):
    files = list(_get_files(get_sample_data_path))
    assert isinstance(files, Iterable)
    assert "auto_mpg.csv" in [x.name for x in files]
    assert "car_evaluation.csv" in [x.name for x in files]
    assert "iris.csv" in [x.name for x in files]
    assert "wine_quality.csv" in [x.name for x in files]


def test__get_descriptions(get_sample_data_path):
    df = _get_descriptions(_get_files(get_sample_data_path))
    assert isinstance(df, pd.DataFrame)
    assert "path" in df.columns
    assert "name" in df.columns
    assert "extension" in df.columns
    assert "size" in df.columns
    assert "human_readable" in df.columns
    assert "rows" in df.columns


def test_explore(get_sample_data_path):
    df = explore_files(get_sample_data_path)
    assert isinstance(df, pd.DataFrame)
    assert "separator" in df.columns
