import os
import os.path
from pathlib import Path

import numpy as np
import pandas as pd
from pandas_profiling import ProfileReport
from tqdm.auto import tqdm

SUPPORTED_FORMATS = (".txt", ".csv", ".tab", ".dat", ".json", ".arff", ".xml", ".xlsx")
PLAIN_FORMATS = (".txt", ".csv", ".tab", ".dat")
SIZE_UNITS = ["B", "KiB", "MiB", "GiB", "TiB", "PiB", "EiB", "ZiB"]
SEPARATORS = ["\t", " ", ",", ";", "|"]
SEPARATOR_NAMES = ["tab", "space", "comma", "semi_colon", "pipe"]
BIG_FILE = 104_857_600  # 100MB


def get_file_basename(file):
    """Returns the name of a file given its path."""
    return os.path.basename(file)


def get_lines_count(file):
    """Returns the number of lines in a file."""
    return sum(1 for line in open(file))


def get_human_readable_size(size, index=0):
    """Returns the size given in bytes in a human readable unit."""
    if abs(size) < 1024.0:
        hr_size = "{:.1f} {}".format(size, SIZE_UNITS[index])
        return hr_size
    else:
        hr_size = get_human_readable_size(size / 1024.0, index + 1)
    return hr_size


""" 
The next 5 functions determine the separator of a plain file.
It counts the chars ['\t', ' ', ',', ';', '|'] per line in a matrix
Then it compute the statistics: mean, std, var, min, max, median of the counts.
The criteria is:
The average of the counting is greater than 0.
It selects the one with minumum standard deviation per evaluated separator.
"""


def get_character_count(line, character):
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


def compute_measures(counters):
    """
    It computes statistics on the counters of the separators. To be used on the evaluation criteria.
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


def evaluate_criteria(df):
    """
    The evaluation criteria is to select the separator with less standard deviation and with mean above zero.
    """
    return df[df["mean"] > 0].sort_values(by="std").iloc[0]["name"]


def get_separator(file_path, header=True):
    """
    Returns the separator of a given file.
    """
    data = open(file_path).readlines()
    if header == True:
        headers = data[0]
        data = data[1:]

    counters = compute_counters(data)
    sep_measures = compute_measures(counters)

    column_measures = ["name", "mean", "std", "var", "min_", "max_", "median"]
    df_separators = pd.DataFrame(sep_measures, columns=column_measures)
    sep = evaluate_criteria(df_separators)
    return sep


def export_reckon_report(df, extension=".xlsx"):
    """
    This function exports the results of the reckon phase to an excel file.
    """
    if extension == ".xlsx":
        file_name = "files_explored.xlsx"
        df.to_excel(file_name, sheet_name="files", index=False)
    elif extension == ".csv":
        file_name = "files_explored.csv"
        df.to_csv(file_name, index=False)

    pwd = os.getcwd()
    print(
        "\n{} files explored. Check out the results in {} in: \n{}\n".format(
            len(df), file_name, pwd
        )
    )
    return


def reckon_phase(target_folder=".", export_results: bool = True) -> pd.DataFrame:
    """
    In phase 1 the script collects all potential files to explore from a folder, it
    will look recursevely all the subfolders in that path.

    It returns a pd.DataFrame with metadata around the files in the target_folder and subfolders.

    Args:
        target_folder: The folder where the script will look for files to explore.
        export_results (bool): If True, the results of the reckon phase will be exported to an excel file.

    Returns:
        df (pd.DataFrame): A pd.DataFrame with metadata about the files in the target_folder and subfolders.
    """
    # TODO - Compute number of columnss
    target_folder = Path(target_folder)
    # Gets all the files recursevely in the target_folder path.
    all_files = target_folder.rglob("*")

    # Creates a list to store temporal results about the files with its path, name,
    # extension, size, human readable size, and number of lines in the file.
    files = []
    columns = ["path", "name", "extension", "size", "human_readable", "lines"]
    print(f"Processing files in {target_folder}")
    for i, f in tqdm(enumerate(list(all_files)), total=len(list(all_files))):
        file_name = f.stem
        file_extension = f.suffix
        file_size = f.stat().st_size
        hr_size = get_human_readable_size(file_size)

        if file_extension.lower() in SUPPORTED_FORMATS:
            if file_extension in PLAIN_FORMATS:
                lines_count = get_lines_count(f)
                files.append(
                    (f, file_name, file_extension, file_size, hr_size, lines_count)
                )
            elif file_extension == "xlsx":
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
                lines_count = None
                files.append(
                    (f, file_name, file_extension, file_size, hr_size, lines_count)
                )
        else:
            pass

    # Creates a dataframe with the results of the files exploration.
    df = pd.DataFrame(files, columns=columns)

    # Creates and determine the separator in the plain file.
    print("Processing extensions...")
    df["separator"] = None
    pbar = tqdm(range(len(df)), total=len(df))
    for i in pbar:
        pbar.set_description(f"{df.iloc[i]['name']} ({df.iloc[i]['lines']:,} records)")
        if df.iloc[i]["extension"] in PLAIN_FORMATS:
            sep = get_separator(df.iloc[i]["path"])
            df.at[i, "separator"] = sep

    if export_results:
        export_reckon_report(df)

    return df


# PHASE 2


def get_separator_char(sep: str) -> str:
    """
    Returns the char used as separator.
    """
    for i, r in enumerate(SEPARATOR_NAMES):
        if sep == r:
            return SEPARATORS[i]
    return ","


def profile_file(file_path, file_name, extension, file_size, output_path, sep=None):
    """
    This function will load the given file using pandas and then will create a report using pandas-profiling.

    Args:
        file_path: The path of the file to be profiled.
        file_name: The name of the file to be profiled.
        extension: The extension of the file to be profiled.
        output_path: The path where the report will be saved.
        sep: The separator used in the file.

    Returns:
        A pandas-profiling report.
    """

    def get_profile(df, file_size):
        if file_size > BIG_FILE:
            profile = ProfileReport(df, minimal=True)
        else:
            profile = ProfileReport(df)
        return profile

    # output_path.mkdir(exist_ok=True)
    output_path.mkdir(parents=True, exist_ok=True)
    try:
        if extension in PLAIN_FORMATS:
            separator = get_separator_char(sep)
            df = pd.read_csv(file_path, sep=separator)
            profile = get_profile(df, file_size)
            report_path = output_path / "{}.html".format(file_name)
            profile.to_file(report_path)
            return
        elif extension == [".xlsx", ".xls"]:
            excel_name = get_file_basename(file_path)
            excel_name += "_" + file_name
            df = pd.read_excel(file_path, sheet_name=file_name)
            profile = get_profile(df, file_size)
            report_path = output_path / "{}.html".format(excel_name)
            profile.to_file(report_path)
        else:
            return
    except Exception as e:
        print(e)
        print(f"Error with {file_path}")
        return


def generate_code(
    file_path, file_name, extension, output_path=".", sep=None, prefix="df_"
):
    """
    This function returns generated python code to load the files to memory using pandas.
    """

    def get_separator_char(sep):
        if sep == "space":
            separator = " "
        elif sep == "tab":
            separator = "\\t"
        elif sep == "semi_colon":
            separator = ";"
        elif sep == "comma":
            separator = ","
        elif sep == "pipe":
            separator = "|"
        else:
            separator = ","
        return separator

    df_name = file_name.split(".")[0].replace(" ", "_").replace("-", "_")
    if extension in PLAIN_FORMATS:
        separator = get_separator_char(sep)
        code = (
            f"""{prefix}{df_name} = pd.read_csv('{file_path}', sep = '{separator}')\n"""
        )
        return code
    elif extension == "xlsx":
        excel_name = get_file_basename(file_path).split(".")[0]
        excel_name += "_" + file_name
        code = """"""
        excel_name = excel_name.replace(" ", "_").replace("-", "_")
        code = f"""{prefix}{excel_name} = pd.read_excel('{file_path}', sheet_name = '{file_name}')\n"""
        return code
    else:
        return ""


def generate_python_code(df, verbose=True, python_file="code.txt"):
    """
    This functions receives the dataframe generated in the reckon phase and will generate python code to load each file.
    It will write a 'code.txt' file with the scripts.
    The verbose option is to print the code to the standard output.
    """
    print('Generating python code and saving it to "{}"'.format(python_file))
    code = """import pandas as pd\n\n"""
    for i, r in tqdm(df.iterrows(), total=len(df)):
        if r.lines > 0:
            code += generate_code(r.path, r["name"], r.extension, sep=r.separator)

    with open(python_file, "w") as f:
        f.write(code)
    if verbose:
        print("### Start of the code ###")
        print(code)
        print("### End of the code ###")

    print(
        '\n"{}" has the generated Python code to load the files.\n'.format(python_file)
    )
    return


def pandas_profile_files(
    df: pd.DataFrame, output_path: str = ".", only_small_files=False
):
    """
    This function receives the dataframe created in the reckon phase and will create a pandas-profiling report per file.

    Args:
        df: The dataframe created in the reckon phase.
        output_path: The path where the report will be saved.
        only_small_files: If True, only the files with less than BIG_FILE will be profiled.

    Returns:
        A pandas-profiling report.
    """
    output_path = Path(output_path)
    df.sort_values(by="size", inplace=True)
    # if only_small_files:
    #     df = df[df["size"] < 10_000]
    print(f"Profiling files and generating reports in folder {output_path}")
    pbar = tqdm(df.iterrows(), total=len(df))
    for i, r in pbar:
        pbar.set_description(f"Profiling {r['name']} ({r['lines']:,} records)")
        if r.lines > 0:
            profile_file(
                r["path"],
                r["name"],
                extension=r["extension"],
                file_size=r["size"],
                output_path=output_path,
                sep=r["separator"],
            )

    print('\nCheck out all the reports in "{}"\n'.format(output_path))
    return
