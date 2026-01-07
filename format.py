from datetime import datetime
from tqdm import tqdm
import argparse
import csv
import re
import os

DATE_FORMAT_PATTERN = "%b %d, %Y %I:%M:%S %p"
READ_DELAY_REGEX = re.compile(
    r"(?P<value>\d+)\s*(?P<unit>day|hour|minute|second)s?"
)

class Message:
    def __init__(self, message_id: int, timestamp: datetime, read_delay_seconds: int):
        self.message_id: int = message_id
        self.timestamp: datetime = timestamp
        self.read_delay_seconds: int = read_delay_seconds
        self.sender: str = ""
        self.content: str = ""

    def add_content(self, line: str):
        self.content += line

    def get_dict(self):
        return {
            "message_id": self.message_id,
            "timestamp": self.timestamp,
            "read_delay_seconds": self.read_delay_seconds,
            "sender": self.sender,
            "content": self.content.strip(),
        }

def parse_read_delay_seconds(line: str) -> int:
    total = 0
    for m in READ_DELAY_REGEX.finditer(line):
        value = int(m.group("value"))
        unit = m.group("unit")
        total += value * {
            "day": 86400,
            "hour": 3600,
            "minute": 60,
            "second": 1,
        }[unit]
    return total

def parse_timestamp(line: str) -> datetime:
    timestamp_str = line.split("(", 1)[0].strip()
    return datetime.strptime(timestamp_str, DATE_FORMAT_PATTERN)

parser = argparse.ArgumentParser("py " + os.path.basename(__file__))
_ = parser.add_argument("file")
_ = parser.add_argument("-o", "--output", default="./output.csv", help="Output CSV file")
args = parser.parse_args()

with open(args.file, mode="r", encoding="utf-8") as infile, \
    open(args.output, mode="w", newline="", encoding="utf-8") as outfile:

    infile_line_count = sum(1 for _ in open(args.file))

    writer = csv.DictWriter(
        outfile,
        fieldnames=[
            "message_id",
            "timestamp",
            "read_delay_seconds",
            "sender",
            "content",
        ],
        dialect="unix"
    )
    writer.writeheader()

    current_msg = None
    expecting_sender = False
    message_id = 0

    for line in tqdm(infile, total=infile_line_count, desc="Processing input file", unit=" line"):
        line = line.strip()

        try:
            timestamp = parse_timestamp(line)

            if current_msg:
                writer.writerow(current_msg.get_dict())

            read_delay_seconds = parse_read_delay_seconds(line)
            current_msg = Message(message_id, timestamp, read_delay_seconds)
            message_id += 1
            expecting_sender = True
            continue

        except ValueError:
            pass

        if current_msg and expecting_sender:
            current_msg.sender = line.strip()
            expecting_sender = False
            continue

        if current_msg and line.strip():
            current_msg.add_content(line + "\n")

    if current_msg:
        writer.writerow(current_msg.get_dict())

