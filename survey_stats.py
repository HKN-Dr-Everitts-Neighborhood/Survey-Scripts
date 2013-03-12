#! python

import os, csv

data_path = "../Fall 2012 Survey Data"

files = [
            os.path.join(data_path, f) for f in os.listdir(data_path)
        ]
files = [f for f in files if os.path.isfile(f)]

for filename in files:
    if filename.endswith(".csv"):
        with open(filename, "r") as file:
            lines = [l for l in csv.reader(file)]
            print len(lines) - 1, "responses in", filename