# Automated File Exploration

## How to use `auto-fe`

You need to import the [auto_fe.py](../code/auto_fe.py) file and call it as follows. You can do it from a Python file or from a notebook.

```
import auto_fe as afe

df_files = afe.reckon_phase('<YOUR_FILE_PATH>')
```

Checkout the [example.py](../code/example.py) file and run it from a terminal with python.

```
python example.py
```

You can do the same from a Jupyter notebook.

The `reckon_phase()` function will generate an Excel file with the results of the exploration called `files_explored.xlsx`.