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
    print('Specify the year for validation, for example: ./validateAndMerge.py 2018')
    exit(1)


def validate_column(data_frame, column_name, constraint_regex, file_name):
    if not all(data_frame[column_name].str.contains(constraint_regex, case=True, regex=True)):
        print(file_name + ': column \'' + column_name + '\' is not valid!')
        exit(2)


year = sys.argv[1]
path = os.path.join('benchmark_files', year, '*.csv')
mergedPath = os.path.join('benchmark_files', year, 'MERGED.csv')
dataFrames = []

headers = ['kind', 'name', 'id', 'time', 'team']
types = {
    'kind': str,
    'name': str,
    'id': str,
    'time': numpy.float64,
    'team': str
}

for filename in glob2.glob(path):
    df = pandas.read_csv(filename, header=0, names=headers, low_memory=False, dtype=types)
    validate_column(df, 'kind', '^(?:Start|End)$', filename)
    validate_column(df, 'name', '^(?:Tokenize|Collect|ComputeScalar|ComputeCosine)$', filename)
    validate_column(df, 'id', '^(?:Pride|Sense)[1-6](?:_(?:Pride|Sense)[1-6])?$', filename)
    dataFrames.append(df)

if len(dataFrames) == 0:
    print('No CSVs found in' + os.path.join('benchmark_files', year))
    exit(3)

mergedDf = pandas.concat(dataFrames)
mergedDf.to_csv(mergedPath, index=False)
print('CSVs are valid. Merged data saved to ' + mergedPath)
