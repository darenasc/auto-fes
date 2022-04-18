# Automated File Exploration System

Automated exploration of files in a folder structure to extract metadata and potential usage of information.

**Features include:**

* [x] Recursive approach to get all files in a directory
* [x] Extracting formats and size of the files
* [x] Number of lines when a file is plain text
* [x] Supporting formats such as: `txt`, `csv`, `tab`, `dat`, `excel`.
* [ ] Pending supported formats `arff`, `json`, `xml`.
* [x] Identifies separator and quote character for text files
* [x] Loading the files in memory
* [x] Loading the files to a database
* [ ] Format conversion 
* [ ] Logging

It works in three phases:

* Phase 1: Reckon of the files. Generates a dataframe with a summary of the files
* Phase 2: Execution. Generates python code to load the files to memory. 
* Phase 3: [Optional] Sends the files to a database.

Read the [documentation](docs/documentation.md) to know how to use it or check out the [notebook-example](code/notebook-example.ipynb).

## Phase 1

You need to import the [auto_fe.py](code/auto_fe.py) file and call it as follows.

```python
import auto_fe as afe

df_files = afe.reckon_phase('<YOUR_FILE_PATH>')
```

Checkout the [example.py](code/example.py) file and then run it from a terminal with python as the following code, or using a Jupyter [notebook](code/notebook-example.ipynb).

```python
python example.py
```

The `reckon_phase` function will generate an Excel file with the results of the exploration called `files_explored.xlsx`.

## Phase 2

### Generate code to load files

Using the dataframe `df_files` generated in the reckon phase, the function `generate_python_code()` will generate python code to load the files using `pandas`.

```python
afe.generate_python_code(df_files)
```

By default the code is printed to the standard output but also written by default to the `code.txt` file.

### Profile the files

Using the dataframe `df_files` generated in the reckon phase, the function `pandas_profile_files(df_files)` will load the files and run a [pandas-profiling](https://github.com/pandas-profiling/pandas-profiling) report.

```python
afe.pandas_profile_files(df_files)
```

By default, it will process the files by size order starting with the smallest file. It will create the reports and export them in HTML format. It will store the reports in the same directory where the code is running or it save them in a given directory with the `output_path  = '<YOUR_OUTPUT_PATH>'` argument.

## Phase 3

Automatic load of data from plain files to a database. 

```python
afe.load_datasets_to_database(df, "section")
```

Where `"section"` is the name of a section in the `databases.ini` file where the 

```
[<section>]
db_engine = postgres
host = <IP_OR_HOSTNAME>
schema = <DATABASE_SCHEMA>
catalog = <DATABASE_CATALOG>
user = <DATABASE_USER>
password = <DATABASE_PASSWORD>
port = <DATABASE_PORT>
```

<!--Using pandas and a database connection it will insert all the data to a database. The exploratory analysis on the database can be done with [auto-eda](https://github.com/darenasc/auto-eda).-->

Currently only supports Postgres but create an [issue](https://github.com/darenasc/auto-fes/issues) if you want to use it with other databases.

## Contributing

* Open an [issue](https://github.com/darenasc/auto-fes/issues) to request more functionalities or feedback.