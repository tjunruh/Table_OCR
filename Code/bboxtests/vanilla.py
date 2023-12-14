#!/usr/bin/env python3

import sys
import os
sys.path.append("../tools")
sys.path.append("../application")
from bboxbenchmark import bboxbenchmark, get_metrics
#from ConnCompBtrMorph import ConnCompBtrMorph
from contours import contours
#from xysplit import XYsplit

class Vanilla(contours):
    ...

args = sys.argv[1:]
if not args:
    raise Exception("Three arguments are required\n1: Directory\n2: Recursive analysis (True/False)\n3: Generate metrics (True/False)")

if not len(args) == 3:
    raise Exception("Three arguments are required\n1: Directory\n2: Recursive analysis (True/False)\n3: Generate metrics (True/False)")
root_dir = args[0]
recursive = args[1]
generate_metrics = args[2]
result_files = []
if recursive == "True":
    subdirectories = os.listdir(root_dir)
    for subdirectory in subdirectories:
        subdirectory = root_dir + "/" + subdirectory
        if os.path.isdir(subdirectory):
            print("working on " + subdirectory)
            if generate_metrics == "True":
                result_files.append(subdirectory + "/" + bboxbenchmark(Vanilla, subdirectory))
            elif generate_metrics == "False":
                for filename in os.listdir(root_dir + "/" + subdirectory):
                    f = root_dir + "/" + subdirectory + "/" + filename
                    if os.path.isfile(f) and "Vanilla" in f:
                        result_files.append(f)
            else:
                raise Exception("Third parameter must be True or False")
                
elif recursive == "False":
    if generate_metrics == "True":
        result_files.append(root_dir + "/" + bboxbenchmark(Vanilla, root_dir))
    elif generate_metrics == "False":
        for filename in os.listdir(root_dir):
                f = root_dir + "/" + filename
                if os.path.isfile(f) and "Vanilla" in f:
                    result_files.append(f)
    else:
        raise Exception("Third parameter must be True or False")
else:
    raise Exception("Second parameter must be True or False")

get_metrics(result_files)
