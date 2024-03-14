import sys
import os
import shutil
args = sys.argv[1:]
if not args:
    raise Exception("Two arguments are required\n1: Directory\n2: Test run name\n")

root_dir = args[0]
test_run_name = args[1]
subdirectories = os.listdir(root_dir)
for subdirectory in subdirectories:
    subdirectory = root_dir + "/" + subdirectory
    if os.path.isdir(subdirectory):
        test_run_directory = subdirectory + "/" + test_run_name
        if os.path.isdir(test_run_directory):
            print("Deleting " + test_run_directory)
            shutil.rmtree(test_run_directory)
            
    
