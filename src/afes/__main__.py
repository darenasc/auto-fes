from pathlib import Path

import pandas as pd
import typer

from afes.afe import explore_files, generate_code, profile_files

app = typer.Typer()


@app.command()
def explore(path: str) -> pd.DataFrame:
    """Explore files from the command line.

    Args:
        path (str): Path to the structured data files.

    Raises:
        Exception: Files not found.

    Returns:
        pd.DataFrame: List with metadata about the files explored.
    """
    path_to_explore = Path(path)
    if path_to_explore.exists():
        df = explore_files(path_to_explore)
    else:
        raise Exception(f"Path {path} not valid")
    print(df)
    return df


@app.command()
def generate(path: str, output_file: str = "code.txt") -> None:
    """Generate pandas code to load the files.

    Args:
        path (str): Path to the structured data files.
        output_file (str, optional): Path to the file to save the generated
            code. Defaults to "code.txt".
    """
    df = explore(path)
    generate_code(df=df, python_file=output_file)


@app.command()
def profile(
    path: str, output_path: str = ".", profile_tool: str = "ydata-profiling"
) -> None:
    """Profile the structured data.

    Args:
        path (str): Path to the structured data files.
        output_path (str): Path to save the HTML reports.
        profile_tool (str, optional): `ydata-profiling` or `sweetviz`.
            Defaults to "ydata-profiling".
    """
    df = explore(path)
    profile_files(df=df, output_path=output_path, profile_tool=profile_tool)


if __name__ == "__main__":
    app()
