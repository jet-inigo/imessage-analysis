# Generate statistic files from cleaned text message CSV

from matplotlib import font_manager
from collections import defaultdict
#import pandas as pd
#import advertools as adv
import matplotlib as mpl
import matplotlib.pyplot as plt
import argparse
import json
import os

plt.rcParams.update({
    "font.size": 16,
    "font.family": "SF Pro",
    "svg.fonttype": "none",
})

font_path = "/home/jet/.local/share/fonts/SF-Pro.ttf"
sfpro = font_manager.FontProperties(fname=font_path)

emoji_fp = font_manager.FontProperties(
    family="Apple Color Emoji"
)

parser = argparse.ArgumentParser("py " + os.path.basename(__file__))
#_ = parser.add_argument("file")
args = parser.parse_args()

#df = pd.read_csv(args.file)

""" Only use once to create emoji breakdown
emoji_summary = adv.extract_emoji(text_content)

print(emoji_summary["top_emoji"])

with open("emojis.json", "w") as file:
    json.dump(emoji_summary, file, indent=4)
"""

emoji_summary = json.load(open("emojis.json", "r"))
emoji_summary_j = json.load(open("emojis_j.json", "r"))
emoji_summary_k = json.load(open("emojis_k.json", "r"))

# Get emoji count dictionaries
emoji_counts: dict[str, int] = defaultdict(int)
emoji_counts_j: dict[str, int] = defaultdict(int)
emoji_counts_k: dict[str, int] = defaultdict(int)

for emoji, count in emoji_summary_j["top_emoji"]:
    emoji_counts[emoji] += count
    emoji_counts_j[emoji] += count

for emoji, count in emoji_summary_k["top_emoji"]:
    emoji_counts[emoji] += count
    emoji_counts_k[emoji] += count

all_emojis = set(emoji_counts_j) | set(emoji_counts_k)

sorted_emojis = sorted(
    all_emojis,
    key=lambda e: emoji_counts_j[e] + emoji_counts_k[e],
    reverse=True,
)

top_n = 10
emojis = sorted_emojis[:top_n]

counts = [emoji_counts[e] for e in emojis]
j_counts = [emoji_counts_j[e] for e in emojis]
k_counts = [emoji_counts_k[e] for e in emojis]

fig, ax = plt.subplots(figsize=(12, 6))

j_bars = ax.bar(emojis, j_counts, label="J", color="#fe942b")
k_bars = ax.bar(emojis, k_counts, bottom=j_counts, label="K", color="#f150a8")
ax.bar_label(k_bars, labels=counts, label_type="edge")

ax.tick_params(axis="x", bottom=False)

ax.legend()

for label in ax.get_xticklabels():
    label.set_fontproperties(emoji_fp)
    label.set_fontsize(32)

plt.tight_layout()
plt.savefig("emoji_stacked.svg", format="svg")
plt.close()
