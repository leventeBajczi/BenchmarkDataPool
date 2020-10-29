import glob2
import pandas
import numpy
import sys
import os.path

from matplotlib import axis

if len(sys.argv) < 2:
    print('Specify the directory for validation, for example: ./validateAndMerge.py benchmark_files/2019')
    exit(1)


def validate_column(data_frame, column_name, constraint_regex, file_name):
    if not all(data_frame[column_name].str.contains(constraint_regex, case=True, regex=True)):
        print('ERROR in file "%s": column "%s" values don\'t match regex "%s"'
              % (file_name, column_name, constraint_regex))
        return False
    return True


def check_for_duplicates(data_frame, file_name):
    duplicate_bools = data_frame.duplicated()
    duplicate_df = data_frame[duplicate_bools.values]
    number_of_duplicates = len(duplicate_df)
    if number_of_duplicates > 0:
        print('ERROR in file "%s": data contains %s duplicated values' % (file_name, str(number_of_duplicates)))
        print(duplicate_df)
        return False
    return True


dir_to_validate = sys.argv[1]
path_pattern = os.path.join(dir_to_validate, '*.csv')
mergedPath = os.path.join(dir_to_validate, 'MERGED.csv')
dataFrames = []

headers = ['type', 'name', 'input_id', 'time', 'team', 'meas_id']
types = {
    'type': str,
    'name': str,
    'input_id': str,
    'time': numpy.float64,
    'team': str,
    'meas_id': str
}

for file_path in filter(lambda fn: not fn.endswith('MERGED.csv'), glob2.glob(path_pattern)):
    print('Processing file: %s' % file_path)
    df = pandas.read_csv(file_path, header=0, names=headers, low_memory=False, dtype=types)
    valid = True
    valid &= validate_column(df, 'type', '^(?:QUEUE|START|END)$', file_path)
    valid &= validate_column(df, 'name', '^(?:Tokenize|Collect|ComputeScalar|ComputeCosine)\d*$', file_path)
    valid &= validate_column(df, 'input_id', '^(?:Pride|Sense)[1-6](?:_(?:Pride|Sense)[1-6])?$', file_path)
    valid &= validate_column(df, 'meas_id', '^(?:Pride)[1-6]_(?:Sense)[1-6]$', file_path)
    valid &= check_for_duplicates(df, file_path)
    if valid:
        dataFrames.append(df)

if len(dataFrames) == 0:
    print('ERROR: No valid CSVs found in directory ' + dir_to_validate)
    exit(4)

mergedDf = pandas.concat(dataFrames)
check_for_duplicates(mergedDf, mergedPath)

mergedDf.to_csv(mergedPath, index=False)
print('Valid CSVs merged to ' + mergedPath)
