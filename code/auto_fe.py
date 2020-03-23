import os
import os.path
from os import listdir
from os.path import isfile, isdir, join
import pandas as pd
import numpy as np
from tqdm import tqdm
from pandas_profiling import ProfileReport

SUPPORTED_FORMATS = ('txt','csv','tab','dat','json','arff','xml')
PLAIN_FORMATS = ('txt','csv','tab','dat')
SIZE_UNITS = ['B', 'KiB', 'MiB', 'GiB', 'TiB', 'PiB', 'EiB', 'ZiB']
SEPARATORS = ['\t', ' ', ',', ';', '|']
SEPARATOR_NAMES = ['tab', 'space', 'comma', 'semi_colon', 'pipe']

def get_files_and_dirs(path):
    """
    Gets all the files and directories (and subdirectories) from a given path.
    """
    if path[-1] == '/':
        path = path[:-1]
    elif path[-1] == '\\':
        path = path[:-1]
        
    content = os.listdir(path)
    
    files = []
    directories = []
    
    for item in content:
        target_item = path + '/' + item
        if os.path.isfile(target_item):
            files.append(target_item)
        elif os.path.isdir(target_item):
            directories.append(target_item)
        else:
            pass
    return files, directories

def explore_recursevely(path):
    """
    It returns all the files in a given folder and subfolders.
    """
    files = []
    directories = []
    
    files, directories = get_files_and_dirs(path)
    
    if len(directories) == 0:
        return files
    else:
        for folder in directories:
            files_ = explore_recursevely(folder)
            files += files_
    return files

def get_file_basename(file):
    """Returns the name of a file given its path."""
    return os.path.basename(file)

def get_file_extension(file):
    """Returns the extension of a file give the file name and path."""
    return os.path.basename(file).split('.')[-1]

def get_file_size(file):
    """Returns the size of a file in bytes given the file name and path."""
    return os.stat(file).st_size

def get_lines_count(file):
    """Returns the number of lines in a file."""
    return sum(1 for line in open(file))

def filter_supported_formats(file_list):
    filtered_list = []
    for f in file_list:
        if file_extension.lower() in SUPPORTED_FORMATS:
            filtered_list.append(f)
    return filtered_list

def get_human_readable_size(size, index = 0):
    """Returns the size given in bytes in a human readable unit."""
    if abs(size) < 1024.0:
        hr_size = '{:.1f} {}'.format(size, SIZE_UNITS[index])
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
    return df[df['mean'] > 0].sort_values(by='std').iloc[0]['name']

def get_separator(file_path, header = True):
    """
    Returns the separator of a given file.
    """
    data = open(file_path).readlines()
    if header == True:
        headers = data[0]
        data = data[1:]
    
    counters = compute_counters(data)
    sep_measures = compute_measures(counters)
        
    column_measures = ['name','mean', 'std', 'var', 'min_', 'max_', 'median']
    df_separators = pd.DataFrame(sep_measures, columns = column_measures)
    sep = evaluate_criteria(df_separators)
    return sep

def export_reckon_report(df, extension = 'xlsx'):
    
    if extension == 'xlsx':
        file_name = 'files_explored.xlsx'
        df.to_excel(file_name, sheet_name = 'files')
    elif extension == 'csv':
        file_name = 'files_explored.csv'
        df.to_csv(file_name)
    
    pwd = os.getcwd()
    print('\n{} files explored. Check out the results in {} in: \n{}\n'.format(len(df), file_name, pwd))
    return

def reckon_phase(target_folder = '.', export_results = True):
    """
    In phase 1 the script collects all potential files to explore from a folder, it 
    will look recursevely all the subfolders in that path.
    
    It returns a pd.DataFrame with metadata around the files in the target_folder and subfolders.
    """
    # Gets all the files recursevely in the target_folder path.
    all_files = explore_recursevely(target_folder)
    
    # Creates a list to store temporal results about the files with its path, name,
    # extension, size, human readable size, and number of lines in the file.
    files = []
    columns = ['path', 'name', 'extension', 'size', 'human_readable', 'lines', 'sheet_name']
    print('Processing files...')
    for i, f in tqdm(enumerate(all_files), total = len(all_files)):
    #for i, f in enumerate(all_files):
        file_name = get_file_basename(f)
        file_extension = get_file_extension(f)
        file_size = get_file_size(f)
        hr_size = get_human_readable_size(file_size)

        if file_extension.lower() in SUPPORTED_FORMATS:
            if file_extension in PLAIN_FORMATS:
                lines_count = get_lines_count(f)
            elif file_extension == 'xlsx':
                excel_file = pd.ExcelFile(f)
                for sheet_name in excel_file.sheet_names:
                    df_sheet = pd.read_excel(f, sheet_name = sheet_name)
                    files.append((f, file_name, file_extension, file_size, hr_size, len(df_sheet), sheet_name))
            else:
                lines_count = None
            files.append((f, file_name, file_extension, file_size, hr_size, lines_count))
        else:
            pass
    
    # Creates a dataframe with the results of the files exploration.
    df = pd.DataFrame(files, columns = columns)

    # Creates and determine the separator in the plain file.
    print('Processing extensions...')
    df['separator'] = None
    for i in tqdm(range(len(df)), total=len(df)):
        if df.iloc[i]['extension'] in PLAIN_FORMATS:
            sep = get_separator(df.iloc[i]['path'])
            df.at[i, 'separator'] = sep
            
    if export_results:
        export_reckon_report(df)
        
    return df