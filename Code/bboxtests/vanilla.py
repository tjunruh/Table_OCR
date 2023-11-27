#!/usr/bin/env python

import sys
sys.path.append("../tools")
sys.path.append("../application")
from bboxbenchmark import bboxbenchmark, get_metrics
from predict import predict

class Vanilla(predict):
    ...

args = sys.argv[1:]
if not args:
    raise Exception("No directory given")
root_dir = args[0]
result_file = bboxbenchmark(Vanilla, root_dir)
get_metrics(root_dir + "/" + result_file)
