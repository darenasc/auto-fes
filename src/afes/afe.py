from pathlib import Path
from typing import Iterable

import pandas as pd
from tqdm.auto import tqdm

from afes.config import PLAIN_FORMATS, SUPPORTED_FORMATS
from afes.generate import generate_pandas_code
from afes.profile import (
    load_file_with_pandas,
    profile_with_sweetviz,
    profile_with_ydata_profiling,
)
from afes.utils import get_human_readable_size, get_row_count, get_separator


def _get_files(path: Path) -> Iterable:
    """Returns all the files in a directory.

    Args:
        path (Path): Path to read files.

    Raises:
        Exception: If the path is not valid.

    Returns:
        Iterable: An iterable with all the files in the folder and subfolders.
    """
    if path.is_dir():
        return path.rglob("*")
    elif path.is_file():
        return [path]
    else:
        raise Exception("path not valid.")


def _get_descriptions(all_files: Iterable) -> pd.DataFrame:
    """Returns a list with ["path", "name", "extension", "size",
    "human_readable", "rows"]

    Args:
        all_files (Iterable): List for files to describe.

    Returns:
        pd.DataFrame: DataFrame with description of the files.
    """
    files = []
    pbar = tqdm(enumerate(list(all_files)), total=len(list(all_files)), unit="files")
    for _, f in pbar:
        pbar.set_description(f.name)
        file_name = f.stem
        file_extension = f.suffix
        file_size = f.stat().st_size
        hr_size = get_human_readable_size(file_size)

        if file_extension.lower() in SUPPORTED_FORMATS:
            if file_extension in PLAIN_FORMATS:
                row_count: int | None = get_row_count(f)
                files.append(
                    (f, file_name, file_extension, file_size, hr_size, row_count)
                )
            elif file_extension == ".xlsx":
                excel_file = pd.ExcelFile(f)
                for sheet_name in excel_file.sheet_names:
                    df_sheet = pd.read_excel(f, sheet_name=sheet_name)
                    files.append(
                        (
                            f,
                            sheet_name,
                            file_extension,
                            file_size,
                            hr_size,
                            len(df_sheet),
                        )
                    )
            else:
                row_count = None
                files.append(
                    (f, file_name, file_extension, file_size, hr_size, row_count)
                )
        else:
            pass

    # Creates a dataframe with the results of the files exploration.
    columns = ["path", "name", "extension", "size", "human_readable", "rows"]
    df = pd.DataFrame(files, columns=columns)
    return df


def explore_files(path: str | Path) -> pd.DataFrame:
    """Return a dataframe with all the files.

    Args:
        path (str | Path): Path the file or to the directory with files.

    Returns:
        pd.DataFrame: DataFrame with description of the files.
    """
    path = Path(path)
    all_files = _get_files(path)
    df = _get_descriptions(all_files=all_files)

    # Determine the separator
    df["separator"] = None
    pbar = tqdm(range(len(df)), total=len(df))
    for i in pbar:
        pbar.set_description(f"{df.iloc[i]['name']} ({df.iloc[i]['rows']:,} records)")
        if df.iloc[i]["extension"] in PLAIN_FORMATS:
            sep = get_separator(df.iloc[i]["path"])
            df.at[i, "separator"] = sep

    return df


def generate_code(
    df: pd.DataFrame,
    python_file: str = "code.txt",
    verbose: bool = True,
):
    """Generate pandas code to load the files.

    Args:
        df (pd.DataFrame): DataFrame with the explored files.
        python_file (str, optional): Name of the file to save the code.
            Defaults to "code.txt".
        verbose (bool, optional): Flag to print the code. Defaults to True.
    """
    generate_pandas_code(df, python_file=python_file, verbose=verbose)


def profile_files(
    df: pd.DataFrame,
    output_path: str | Path = ".",
    profile_tool: str = "ydata-profiling",
):
    """Profile the structured data.

    Args:
        df (pd.DataFrame): DataFrame with the files to be profiled.
        output_path (str | Path, optional): Folder to save the HTML reports.
            Defaults to ".".
        profile_tool (str, optional): Select which profiling too to use.
            Defaults to "ydata-profiling".
    """
    output_path = Path(output_path)
    output_path.mkdir(parents=True, exist_ok=True)
    df.sort_values(by="size", inplace=True)
    print(
        f"Profiling files with {profile_tool} and generating reports in folder {output_path}"
    )
    pbar = tqdm(df.iterrows(), total=len(df))
    for _, r in pbar:
        pbar.set_description(f"Profiling {r['name']} ({r['rows']:,} records)")
        if r.rows > 0:
            df_to_profile = load_file_with_pandas(
                file_path=r["path"],
                file_name=r["name"],
                extension=r["extension"],
                sep=r["separator"],
            )
            if profile_tool == "ydata-profiling":
                profile_with_ydata_profiling(
                    output_path=output_path,
                    df_to_profile=df_to_profile,
                    file_name=r["name"],
                    file_size=r["size"],
                )
            elif profile_tool == "sweetviz":
                profile_with_sweetviz(
                    df_to_profile=df_to_profile,
                    output_path=output_path,
                    file_name=r["name"],
                )

    print(f'\nCheck out all the reports in "{output_path.resolve()}"\n')
    return
