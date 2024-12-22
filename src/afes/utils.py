from pathlib import Path

import numpy as np
import pandas as pd

from afes.config import SEPARATOR_NAMES, SEPARATORS, SIZE_UNITS


def get_human_readable_size(size: float, index: int = 0) -> str:
    """Returns the size given in bytes in a human readable unit."""
    if abs(size) < 1024.0:
        hr_size = f"{size:.1f} {SIZE_UNITS[index]}"
        return hr_size
    else:
        hr_size = get_human_readable_size(size / 1024.0, index + 1)
    return hr_size


def get_row_count(file: str | Path) -> int:
    """Returns the number of rows in a file."""
    # TODO - Add closing file
    return sum(1 for _ in open(file))


def get_character_count(line: str, character: str) -> int:
    """
    Returns the number of times a character is found in a line.
    """
    return sum(1 for char in line if char == character)


def compute_counters(data):
    """
    Returns the number of times a separator is in each line.
    """
    counters = np.zeros((len(data), len(SEPARATORS)))
    for i, line in enumerate(data):
        counters[i] = [get_character_count(line, sep) for sep in SEPARATORS]
    return counters


def compute_measures(counters: pd.DataFrame) -> list:
    """It computes statistics on the counters of the separators. To be used on
    the evaluation criteria.
    """
    sep_measures = []
    for i in range(len(counters.T)):
        mean = counters.T[:][i].mean()
        std = counters.T[:][i].std()
        var = counters.T[:][i].var()
        min_ = counters.T[:][i].min()
        max_ = counters.T[:][i].max()
        median = np.median(counters.T[:][i])
        sep_measures.append((SEPARATOR_NAMES[i], mean, std, var, min_, max_, median))
    return sep_measures


def evaluate_criteria(df: pd.DataFrame):
    """The evaluation criteria is to select the separator with less standard
    deviation and with mean above zero.
    """
    return df[df["mean"] > 0].sort_values(by="std").iloc[0]["name"]


def get_separator(file_path: Path, header=True) -> str:
    """Returns the separator of a given file.
    It counts the chars ['\t', ' ', ',', ';', '|'] per line in a matrix
    Then it compute the statistics: mean, std, var, min, max, median of the
    counts.
    The criteria is: The average of the counting is greater than 0.
    It selects the one with minumum standard deviation per evaluated separator.
    """
    data = open(file_path).readlines()
    if header is True:
        headers = data[0]
        data = data[1:]

    counters = compute_counters(data)
    sep_measures = compute_measures(counters)

    column_measures = ["name", "mean", "std", "var", "min_", "max_", "median"]
    df_separators = pd.DataFrame(sep_measures, columns=column_measures)
    sep = evaluate_criteria(df_separators)
    return sep
