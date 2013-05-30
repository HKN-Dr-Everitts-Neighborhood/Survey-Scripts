#! python

import os, csv, sys

def print_stats(data_path):
    files = [
                os.path.join(data_path, f) for f in os.listdir(data_path)
            ]
    files = [f for f in files if os.path.isfile(f)]

    for filename in files:
        if filename.endswith(".csv"):
            with open(filename, "r") as file:
                lines = [l for l in csv.reader(file)]
                print len(lines) - 1, "responses in", filename

def main():
    if len(sys.argv) != 2:
        print "Usage:", sys.argv[0], "<path of survey data>"
        return

    print_stats(sys.argv[1])

if __name__ == '__main__':
    main()
