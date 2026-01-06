import argparse
import re
import csv
from datetime import datetime

DATE_FORMAT_PATTERN = "%b %d, %Y %I:%M:%S %p"

parser = argparse.ArgumentParser("./clean")
parser.add_argument("file", help="Filepath of a resulting .txt export from imessage-exporter")
parser.add_argument("-o", "--output", action='store_const', default='./format.csv')
args = parser.parse_args()

countDate = 0
countNonDate = 0
with open(args.file, "r") as file:
    for line in file:
        try:
            datetime.strptime(line[:24], DATE_FORMAT_PATTERN)
            countDate += 1
        except:
            countNonDate += 1
print(countDate)
print(countNonDate)
