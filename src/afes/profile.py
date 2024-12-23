from pathlib import Path

import pandas as pd

from afes.config import BIG_FILE, PLAIN_FORMATS, SEPARATOR_NAMES, SEPARATORS


def get_separator_char(sep: str | None) -> str:
    """
    Returns the char used as separator.
    """
    for i, r in enumerate(SEPARATOR_NAMES):
        if sep == r:
            return SEPARATORS[i]
    return ","


def profile_with_ydata_profiling(
    df_to_profile: pd.DataFrame, output_path: str | Path, file_name: str, file_size: int
):
    """Profile dataframe using ydata-profiling and saves ther report to disk.

    Args:
        df_to_profile (pd.DataFrame): Data to be profiled.
        output_path (str | Path): Folder to save the report.
        file_name (str): File name.
        file_size (int): File size.
    """
    from ydata_profiling import ProfileReport

    output_path = Path(output_path)

    if file_size > BIG_FILE:
        profile = ProfileReport(df_to_profile, minimal=True)
    else:
        profile = ProfileReport(df_to_profile)
    report_path = output_path / f"{file_name}_ydata.html"
    profile.to_file(report_path)
    return


def load_file_with_pandas(
    file_path: str, file_name: str, extension: str, sep: str | None = None
) -> pd.DataFrame:
    """Read data from file using pandas.

    Args:
        file_path (str): Folder where the structure data is.
        file_name (str): Name of the file.
        extension (str): Extension of the file.
        sep (str | None, optional): Separator of the plain text file.. Defaults
            to None.

    Returns:
        pd.DataFrame: DataFrame with the data read.
    """
    try:
        if extension in PLAIN_FORMATS:
            separator = get_separator_char(sep)
            df = pd.read_csv(file_path, sep=separator)
            return df
        elif extension in [".xlsx", ".xls"]:
            excel_name = Path(file_path).name
            excel_name += "_" + file_name
            df = pd.read_excel(file_path, sheet_name=file_name)
            return df
        else:
            return
    except Exception as e:
        print(e)
        print(f"Error with {file_path}")
        return


def profile_with_sweetviz(
    df_to_profile: pd.DataFrame, file_name: str, output_path: str | Path = "."
):
    """Generate exploratory report using sweetviz

    Args:
        df_to_profile (pd.DataFrame): Data to be profiled.
        file_name (str): Name of the file.
        output_path (str | Path, optional): Folder to save the HTML report.
            Defaults to ".".
    """
    import sweetviz as sv

    output_path = Path(output_path)

    my_report = sv.analyze(df_to_profile)
    my_report.show_html(
        filepath=output_path / f"{file_name}_sweetviz.html", open_browser=False
    )
