import csv
import os
import glob
from fplHelper import *
from readFPL import *



'''

------ Place fpl files to be analyzed in the folder /fplFiles

'''


file_path = "fpl.csv"



# Check if the file exists
if os.path.exists(file_path):
    # If it exists, delete the file
    os.remove(file_path)
    print(f'The old "{file_path}" has been removed')
    print('')
else:
    pass


# Get the directory of the script
script_dir = os.path.dirname(os.path.abspath(__file__))

# Relative path to the folder
folder_path = os.path.join(script_dir, "fplFiles")

# Find all files in the folder with the .igc extension
fpl_files = glob.glob(os.path.join(folder_path, "*.fpl"))

# Sort the list of file paths by the default Windows name sorting
#sorted_fpl_files = sorted(fpl_files)

# Sort the list of file paths by day number
fpl_files = sorted(fpl_files, key=get_day_number)

# Sort the list of file paths by the specified substring
#fpl_files = sorted(fpl_files, key=get_sort_key)

# Print the number of .igc files found
print(f"Number of .fpl files in {folder_path}: {len(fpl_files)}")


#file_name = fpl_files[0]

fpl_summary = {}
fpl_summary_list = []

# Loop through each file and analyze it
for fpl_file in fpl_files:
    fpl_summary = read_fpl_and_return(fpl_file)
    print(f'Processed {fpl_file}')
    if fpl_summary is not None:
        fpl_summary_list.append(fpl_summary)
    #print(detailed_summary_list)
#print('')
#print(f'Analyzed {len(fpl_file)} total .fpl files and generated {file_path}')


# Flatten the list of dictionaries while keeping the order
flattened_data = []
for item in fpl_summary_list:
    flattened_item = {}
    for key, value in item.items():
        if isinstance(value, dict):
            for sub_key, sub_value in value.items():
                flattened_item[f"{key}_{sub_key}"] = sub_value
        else:
            flattened_item[key] = value
    flattened_data.append(flattened_item)

# Transpose the data while keeping the order
transposed_data = {}
order_of_keys = []
for i, item in enumerate(flattened_data):
    for key, value in item.items():
        if key not in transposed_data:
            #transposed_data[key] = [f"{key.split('_')[1] if '_' in key else key}"]  # Write keys to the first column
            transposed_data[key] = [f"{key.split('~')[1] if '~' in key else key}"]  # Write keys to the first column
            order_of_keys.append(key)
        transposed_data[key].append(value)

# Write to CSV file
csv_file_path = 'fplAnalysis.csv'
with open(csv_file_path, 'w', newline='') as csv_file:
    writer = csv.writer(csv_file)
    
    # Write headers to the first row
    writer.writerow([''] + [f"File {i+1}" for i in range(len(fpl_summary_list))])

    # Write data
    for key in order_of_keys:
        writer.writerow(transposed_data[key])

print(f'Data written to {csv_file_path}')
