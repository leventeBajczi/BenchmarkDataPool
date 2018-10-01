#!/usr/bin/env conda-execute

# conda execute
# env:
#  - python >=3
#  - pandas
#  - numpy
#  - glob2
# run_with: python3

import glob2
import pandas
import numpy
import sys
import os.path

if len(sys.argv) < 2:
    print('Specify the directory for validation, for example: ./validateAndMerge.py benchmark_files/2018')
    exit(1)


def validate_column(data_frame, column_name, constraint_regex, file_name):
    if not all(data_frame[column_name].str.contains(constraint_regex, case=True, regex=True)):
        print('ERROR: ' + file_name + ': column \'' + column_name + '\' is not valid!')
        exit(2)


def check_for_duplicates(data_frame, file_name):
    duplicate_bools = data_frame.duplicated(['kind', 'name', 'id', 'team', 'combination_id'])
    number_of_duplicates = len(data_frame[duplicate_bools.values])
    if number_of_duplicates > 0:
        print('ERROR: ' + file_name + ': ' + str(number_of_duplicates) + ' duplicate items found')
        exit(3)


dir_to_validate = sys.argv[1]
path_pattern = os.path.join(dir_to_validate, '*.csv')
mergedPath = os.path.join(dir_to_validate, 'MERGED.csv')
dataFrames = []

headers = ['kind', 'name', 'id', 'time', 'team', 'combination_id']
types = {
    'kind': str,
    'name': str,
    'id': str,
    'time': numpy.float64,
    'team': str,
    'combination_id': numpy.int32
}

for file_path in filter(lambda fn: not fn.endswith('MERGED.csv'), glob2.glob(path_pattern)):
    print('Processing ' + file_path + '...')
    df = pandas.read_csv(file_path, header=0, names=headers, low_memory=False, dtype=types)
    validate_column(df, 'kind', '^(?:Start|End)$', file_path)
    validate_column(df, 'name', '^(?:Tokenize|Collect|ComputeScalar|ComputeCosine)$', file_path)
    validate_column(df, 'id', '^(?:Pride|Sense)[1-6](?:_(?:Pride|Sense)[1-6])?$', file_path)
    check_for_duplicates(df, file_path)
    dataFrames.append(df)

if len(dataFrames) == 0:
    print('ERROR: No CSVs found in' + dir_to_validate)
    exit(4)

mergedDf = pandas.concat(dataFrames)
check_for_duplicates(mergedDf, mergedPath)

mergedDf.to_csv(mergedPath, index=False)
print('CSVs are valid. Merged data saved to ' + mergedPath)
