import sys
import os
import shutil
sys.path.append("../application")
from table_extractor import table_extractor
from file_manager import file_manager

args = sys.argv[1:]
if not args:
    raise Exception("Two arguments are required\n1: Directory\n2: Test run name\n")

root_dir = args[0]
test_run_name = args[1]
Vanilla = table_extractor()
file_manager_operative = file_manager()
subdirectories = os.listdir(root_dir)
total_defined_cells = 0
total_measured_cells = 0
rows_columns = file_manager_operative.load_rows_columns()
rows = int(rows_columns[0])
columns = int(rows_columns[1])
defined_cells = rows * columns
for subdirectory in subdirectories:
    subdirectory = root_dir + "/" + subdirectory
    if os.path.isdir(subdirectory):
        print("Working on " + subdirectory)
        for filename in os.listdir(subdirectory):
            filename = subdirectory + "/" + filename
            if os.path.isfile(filename):
                Vanilla.extract_cells(filename)
        measured_cells = Vanilla.get_measured_cell_number()
        total_measured_cells = total_measured_cells + measured_cells
        total_defined_cells = total_defined_cells + (defined_cells * Vanilla.get_number_of_pages())
        test_run_directory = subdirectory + "/" + test_run_name
        print("Cells detected: " + str(measured_cells) + "/" + str(defined_cells * Vanilla.get_number_of_pages()))
        if not os.path.isdir(test_run_directory):
            os.mkdir(test_run_directory)
        for filename in os.listdir(file_manager_operative.processed_page_path):
            shutil.copy(str(file_manager_operative.processed_page_path) + "/" + filename, test_run_directory)
        
print("Total cells detected: " + str(total_measured_cells) + "/" + str(total_defined_cells))
