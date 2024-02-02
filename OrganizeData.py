import os
import re
import shutil
from datetime import date


def readFileName(filename):
    # regex to find date in file name
    date_pattern = re.compile(r'(\d{4})(\d{2})(\d{2})')
    match = date_pattern.search(filename)

    if match:

        year, month, day = match.groups()
        #call to organize by date
        OrganizeDataByDate(year, month, day)
    else:
        return None

def OrganizeDataByDate(year, month, day):

    base_folder = "ProcessedData"

    # Create the year folder
    year_folder = os.path.join(base_folder, str(year))
    if not os.path.exists(year_folder):
        os.makedirs(year_folder)

    # Create the month folder
    month_folder = os.path.join(year_folder, str(month))
    if not os.path.exists(month_folder):
        os.makedirs(month_folder)

    # Create the day folder
    day_folder = os.path.join(month_folder, str(day))
    if not os.path.exists(day_folder):
        os.makedirs(day_folder)

    #information for call
    input_folder = "ProcessedData"
    output_folder_1 = "H5"
    output_folder_2 = "GeoJSON"
    file_types_1 = {".h5"}
    file_types_2 = {".geojson"}

    #call to organize by data type
    organize_data_by_type(input_folder, output_folder_1, output_folder_2, file_types_1, file_types_2, day_folder)

def organize_data_by_type(input_folder, output_folder_1, output_folder_2, file_types_1, file_types_2, destination_folder):
    for root, _, files in os.walk(input_folder):
        for file in files:
            file_path = os.path.join(root, file)
            _, file_extension = os.path.splitext(file)

            #checks the extension and adds their destination based on type
            if file_extension.lower() in file_types_1:
                output_folder = os.path.join(destination_folder, output_folder_1)
            elif file_extension.lower() in file_types_2:
                output_folder = os.path.join(destination_folder, output_folder_2)
            else:
                # Skip files with unknown extensions
                continue

            # Create output folder if it doesn't exist
            os.makedirs(output_folder, exist_ok=True)

            # Move the file to the folder
            destination_path = os.path.join(output_folder, file)
            shutil.move(file_path, destination_path)


