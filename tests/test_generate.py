import pandas as pd
import pytest

from afes.generate import generate_code, generate_pandas_code


@pytest.mark.parametrize(
    "file_name,extension,sep,expected",
    [
        ("test_csv.csv", ".csv", "comma", True),
        ("test_txt.csv", ".txt", "tab", True),
        ("test_txt.csv", ".txt", "pipe", True),
        ("test_txt.csv", ".txt", "semi_colon", True),
        ("test_txt.csv", ".txt", "tab", True),
        ("test_txt.csv", ".txt", "space", True),
        ("test_csv.xls", ".xls", None, True),
        ("test_csv.xlsx", ".xlsx", None, True),
        ("test_csv.json", ".json", None, False),
    ],
)
def test_generate_code(tmp_path, file_name, extension, sep, expected):
    file_name = "test_file.csv"
    code = generate_code(
        file_path=tmp_path, file_name=file_name, extension=extension, sep=sep
    )
    assert (len(code) > 1) == expected


def test_generate_pandas_code(tmp_path):
    file_path = tmp_path / "code.txt"
    df = pd.DataFrame()
    generate_pandas_code(df=df, verbose=False, python_file=file_path)
    assert file_path.exists()
