# Automated File Exploration System

Automated exploration of files in a folder structure to extract metadata and 
potential usage of information.

If you have a bunch of sctructured data in plain files, this library is for you.

# Installation

```bash
pip install -q git+https://github.com/darenasc/auto-fes.git
pip install -q ydata_profiling sweetviz # to make profiling tools work
```

## How to use it
```python
from afes import afe

# Path to folder with files to be explored
TARGET_FOLDER = "<PATH_TO_FILES_TO_EXPLORE>"
OUTPUT_FOLDER = "<PATH_TO_OUTPUTS>"

# Run exploration on the files
df_files = afe.explore(TARGET_FOLDER)

# Generate pandas code to load the files
afe.generate(df_files)

# Run profiling on each file
afe.profile(df_files, profile_tool="ydata-profiling", output_path=OUTPUT_FOLDER)
afe.profile(df_files, profile_tool="sweetviz", output_path=OUTPUT_FOLDER)
```

# What can you do with AFES

* Explore
* Generate code
* Profile

## Explore

```python
from afes import afe

# Path to folder with files to be explored
TARGET_FOLDER = "<PATH_TO_FILES_TO_EXPLORE>"

# Run exploration on the files
df_files = afe.explore(TARGET_FOLDER)
df_files
```

The `df_files` dataframe will look like the following table, depending on the 
files you plan to explore.

```
|      | path                                              | name                     | extension |    size | human_readable |  rows | separator |
| ---: | :------------------------------------------------ | :----------------------- | :-------- | ------: | :------------- | ----: | :-------- |
|    1 | /content/sample_data/auto_mpg.csv                 | auto_mpg                 | .csv      |   20854 | 20.4 KiB       |   399 | comma     |
|    2 | /content/sample_data/car_evaluation.csv           | car_evaluation           | .csv      |   51916 | 50.7 KiB       |  1729 | comma     |
|    3 | /content/sample_data/iris.csv                     | iris                     | .csv      |    4606 | 4.5 KiB        |   151 | comma     |
|    4 | /content/sample_data/wine_quality.csv             | wine_quality             | .csv      |  414831 | 405.1 KiB      |  6498 | comma     |
|    5 | /content/sample_data/california_housing_test.csv  | california_housing_test  | .csv      |  301141 | 294.1 KiB      |  3001 | comma     |
|    6 | /content/sample_data/california_housing_train.csv | california_housing_train | .csv      | 1706430 | 1.6 MiB        | 17001 | comma     |
```

## Generate code

Using the dataframe `df_files` generated in the explore phase, you can generate 
working python pandas code to be used. 

the function `generate()` will generate python code to load the files using 
`pandas`.

```python
from afes import afe

# Path to folder with files to be explored
TARGET_FOLDER = "<PATH_TO_FILES_TO_EXPLORE>"
OUTPUT_FOLDER = "<PATH_TO_OUTPUTS>"

df_files = afe.explore(TARGET_FOLDER)
afe.generate(df_files)
```

The generated code will look like this:

```bash
### Start of the code ###
import pandas as pd

df_auto_mpg = pd.read_csv('/content/sample_data/auto_mpg.csv', sep = ',')
df_car_evaluation = pd.read_csv('/content/sample_data/car_evaluation.csv', sep = ',')
df_iris = pd.read_csv('/content/sample_data/iris.csv', sep = ',')
df_wine_quality = pd.read_csv('/content/sample_data/wine_quality.csv', sep = ',')
df_california_housing_test = pd.read_csv('/content/sample_data/california_housing_test.csv', sep = ',')
df_california_housing_train = pd.read_csv('/content/sample_data/california_housing_train.csv', sep = ',')

### End of the code ###

"code.txt" has the generated Python code to load the files.
```

By default the code is printed to the standard output but also written by 
default to the `./code.txt` file.

> Note: you can replace the `.txt`  extension by `.py` to make it a working 
> Python script.

### Profile

Using the dataframe `df_files` generated in the explore phase, the function 
`profile(df_files)` will automatically load and profiline the files using 
[ydata-profiling](https://github.com/ydataai/ydata-profiling) or 
[sweetviz](https://github.com/fbdesignpro/sweetviz).

```python
# Path to folder with files to be explored
TARGET_FOLDER = "<PATH_TO_FILES_TO_EXPLORE>"
OUTPUT_FOLDER = "<PATH_TO_OUTPUTS>"

# Run exploration on the files
df_files = afe.explore(TARGET_FOLDER)

afe.profile(df_files, profile_tool="ydata-profiling", output_path=OUTPUT_FOLDER) # or
afe.profile(df_files, profile_tool="sweetviz", output_path=OUTPUT_FOLDER)
```

By default, it will process the files using `ydata-profiling` by size order 
starting with the smallest file. It will create the reports and export them in 
HTML format. It will store the reports in the same directory where the code is 
running or it save them in a given directory with the 
`output_path  = '<YOUR_OUTPUT_PATH>'` argument.

# Contributing

* Open an [issue](https://github.com/darenasc/auto-fes/issues) to request more functionalities or feedback.