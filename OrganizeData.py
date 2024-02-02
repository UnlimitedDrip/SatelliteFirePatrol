import os
import re
import shutil
from datetime import date

def create_month_folder(base_folder, year, month):
    # Create the year folder
    year_folder = os.path.join(base_folder, str(year))
    if not os.path.exists(year_folder):
        os.makedirs(year_folder)

    # Create the month folder
    month_folder = os.path.join(year_folder, str(month))
    if not os.path.exists(month_folder):
        os.makedirs(month_folder)

    return month_folder

def readFileName(file_path):
    # Extract filename from the file path
    filename = os.path.basename(file_path)

    # Regex to find date in the filename
    date_pattern = re.compile(r'(\d{4})(\d{2})\d{2}')
    match = date_pattern.search(filename)

    if match:
        year, month = match.groups()
        # Call to organize by date
        month_folder = create_month_folder("ProcessedData", year, month)
        input_folder = "ProcessedData"
        output_folder_1 = "H5"
        output_folder_2 = "GeoJSON"
        file_types_1 = {".h5"}
        file_types_2 = {".geojson"}

        organize_data_by_type(input_folder, month_folder, output_folder_1, output_folder_2, file_types_1, file_types_2)
    else:
        return None

def organize_data_by_type(input_folder, destination_folder, output_folder_1, output_folder_2, file_types_1, file_types_2):
    # Iterate through files in the input folder
    for root, _, files in os.walk(input_folder):
        for file in files:
            file_path = os.path.join(root, file)
            _, file_extension = os.path.splitext(file)

            # Extract date from the filename
            date_match = re.search(r'(\d{4})(\d{2})\d{2}', file)
            if date_match:
                year, month = date_match.groups()
                date_folder = destination_folder
                
                # Checks the extension and adds their destination based on type
                if file_extension.lower() in file_types_1:
                    output_folder = os.path.join(date_folder, output_folder_1)
                elif file_extension.lower() in file_types_2:
                    output_folder = os.path.join(date_folder, output_folder_2)
                else:
                    # Skip files with unknown extensions
                    continue

                # Create output folder if it doesn't exist
                os.makedirs(output_folder, exist_ok=True)

                # Move the file to the folder
                destination_path = os.path.join(output_folder, file)
                shutil.move(file_path, destination_path)
            else:
                # Skip files without a valid date in the filename
                continue

            
