import pandas as pd
import argparse
import os
import re

FILE_NAME_REGEX: re.Pattern[str] = re.compile(r"[\w/._-]+\.(?:png|jpe?g|heic)", re.IGNORECASE)

parser = argparse.ArgumentParser("py " + os.path.basename(__file__))
_ = parser.add_argument("file")
_ = parser.add_argument("-o", "--output", default="./output_cleaned.csv", help="Output CSV file")
args = parser.parse_args()

df = pd.read_csv(args.file)

effects = df["content"].str.extractall(r"Sent with (?P<effect>[\w ]+)")
#print(effects.value_counts())

tapbacks = df["content"].str.extractall(r"Tapbacks:\n(?P<tapback>\w+) by (?P<name>[\w ]+)")
print(tapbacks.value_counts())

cleaned_df = df.copy(deep=True)
cleaned_df = cleaned_df[~cleaned_df["content"].str.contains("GamePigeon message", regex=False, na=False)]
cleaned_df = cleaned_df[~cleaned_df["content"].str.contains("Apple Cash transaction", regex=False, na=False)]
cleaned_df = cleaned_df[~cleaned_df["content"].str.contains("Messages Image", regex=False, na=False)]
cleaned_df = cleaned_df[~cleaned_df["content"].str.contains(r"Sticker from (?:[\w ]+)", regex=True, na=False)]
cleaned_df = cleaned_df[~cleaned_df["content"].str.contains("This message responded to an earlier message.", na=False)]
cleaned_df["content"] = cleaned_df["content"].str.replace("’", "'", regex=False)
cleaned_df["content"] = cleaned_df["content"].str.replace(r"Tapbacks:\n(?:\w+) by (?:[^\n]+)", "", regex=True)
cleaned_df["content"] = cleaned_df["content"].str.replace(r"Sent with (?P<effect>[^\n]+)", "", regex=True)
cleaned_df["content"] = cleaned_df["content"].str.replace(FILE_NAME_REGEX, "", regex=True)
cleaned_df["content"] = cleaned_df["content"].str.strip()

print(cleaned_df.shape)
cleaned_df.to_csv(args.output, index=False)
