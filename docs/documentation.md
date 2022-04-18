# Automated File Exploration

## How to use `auto-fe`

You need to import the [auto_fe.py](../code/auto_fe.py) file and call it as follows. You can do it from a Python file or from a notebook.

```
import auto_fe as afe

# Gets a list of the files in the given folder and subfolder
df_files = afe.reckon_phase('<YOUR_FILE_PATH>')

# Generates python code to load the files using pandas
afe.generate_python_code(df_files)

# Generates pandas-profiling reports of the files found
afe.pandas_profile_files(df_files)

# Load the files to a database
afe.load_datasets_to_database(df, section="my_database")
```

Checkout the [example.py](../code/example.py) file and run it from a terminal with python.

```
python example.py
```

You can do the same from a Jupyter [notebook](../code/notebook-example.ipynb).

**Functions**

* The `reckon_phase()` function will generate an Excel file with the results of the exploration called `files_explored.xlsx`.

* The `generate_python_code()` function will generate python code to load the files using `pandas`. By default the code is printed to the standard output but also written by default to the `code.txt` file.

* The `pandas_profile_files(df_files)` function will load the files and run a [pandas-profiling](https://github.com/pandas-profiling/pandas-profiling) report per file. By default, it will process the files by size order starting with the smallest file. It will store the reports in the same directory where the code is running or it save them in a given directory with the `output_path  = '<YOUR_OUTPUT_PATH>'` argument.

* The `load_datasets_to_database(df_files, "section")` will automatically load the files in the `df_files` dataframe to a database that has the connection parameters defined in the `databases.ini` file.

## Database

The following is an example of a postgres database in a Docker containre. 

```bash
docker run -itd --name afes-db \
    -h afes-db \
    -e POSTGRES_PASSWORD=afes \
    -e POSTGRES_USER=afes \
    -e POSTGRES_DB=afes \
    -e PGDATA=/var/lib/postgresql/data/pgdata \
    -v ./data:/var/lib/postgresql/data \
    -p 5432:5432 \
    postgres:14.2
```

The `databases.ini` file should contain the following:

```ini
# databases.ini
[my_db_parameters]
db_engine = postgres
host = <IP_OF_THE_DOCKER_CONTAINER>
schema = public
catalog = afes
user = afes
password = afes
port = 5432
```

And the code to load the files to the database is the following:

```python
import auto_fe as afe
df_files = afe.reckon_phase('<YOUR_FILE_PATH>')
afe.load_datasets_to_database(df_files, "my_db_parameters")
```