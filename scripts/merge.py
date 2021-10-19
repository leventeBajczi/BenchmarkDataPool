import glob2
import pandas
import numpy
import sys
import os.path

# CSV schema constraints
csv_header = ['type', 'name', 'input_id', 'time', 'team', 'meas_id']
column_types = {
    'type': str,
    'name': str,
    'input_id': str,
    'time': numpy.float64,
    'team': str,
    'meas_id': str
}
unique_columns = ['team', 'meas_id', 'name', 'input_id', 'type']

def check_for_duplicates(data_frame):
    duplicate_df = data_frame[data_frame.duplicated()]
    num_of_duplicates = len(duplicate_df)
    if num_of_duplicates > 0:
        print(f'ERROR: Contains the following {num_of_duplicates} duplicated rows')
        print(duplicate_df)
        return False
    return True

dir_to_validate = sys.argv[1] if len(sys.argv) == 2 else './csvs'
path_pattern = os.path.join(dir_to_validate, '*.csv')
merged_csv_path = os.path.join('./', 'MERGED.csv')
processed_data_frames = []

for file_path in glob2.glob(path_pattern):
    print(f'Loading file "{file_path}"')
    df = pandas.read_csv(file_path, header=0, names=csv_header, low_memory=False, dtype=column_types)
    processed_data_frames.append(df)

if len(processed_data_frames) == 0:
    print(f'ERROR: No CSVs found in directory "{dir_to_validate}" for pattern "{path_pattern}"')
    exit(1)

print('Merging CSVs')
merged_df = pandas.concat(processed_data_frames)

if not check_for_duplicates(merged_df[unique_columns]):
    exit(1)

print('Checking pivot')
print(merged_df.pivot_table(index=['team', 'meas_id', 'name', 'input_id'], columns='type', values='time').reset_index())

merged_df.to_csv(merged_csv_path, index=False)
print(f'Merged CSV saved as "{merged_csv_path}"')
exit(0)
