#!/usr/bin/env python3

"""
Initialize labels.csv for a folder with images, if file exists, keep original
data and append new entries

Usage:
> python initlabels.py /path/to/dir/with/images
"""

from pathlib import Path
import csv
import re


def natural_sort_key(s, _nsre=re.compile('([0-9]+)')):
    return [int(text) if text.isdigit() else text.lower()
            for text in _nsre.split(str(s))]


supported_ext = [
    # https://docs.opencv.org/3.4/d4/da8/group__imgcodecs.html
    "bmp", "dib",
    "jpeg", "jpg", "jpe",
    "jp2",
    "png",
    "webp",
    "pbm", "pgm", "ppm", "pxm", "pnm",
    "sr", "ras",
    "tiff", "tif",
    "exr",
    "hdr", "pic",
]
supported_ext = ["." + a for a in supported_ext]


def main(args):
    if not args:
        raise Exception("No directory given")
    arg = args[0]
    root_dir = Path(arg).resolve()
    if not root_dir.is_dir():
        raise Exception(f"{arg} is not a directory")
    labels_file = root_dir / "labels.csv"
    img_files = sorted([f.name for f in root_dir.iterdir()
                        if f.suffix.casefold() in supported_ext],
                       key=natural_sort_key)
    labels = {}
    if labels_file.exists():
        with labels_file.open("r") as f:
            reader = csv.reader(f)
            for row in reader:
                labels[row[0]] = row[1]
    with labels_file.open("w+") as f:
        writer = csv.writer(f)
        for img in img_files:
            if img in labels:
                writer.writerow([img, labels[img]])
            else:
                writer.writerow([img, ""])


if __name__ == '__main__':
    import sys

    main(sys.argv[1:])
