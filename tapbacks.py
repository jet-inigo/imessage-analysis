from collections import Counter
from matplotlib import font_manager
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import argparse
import os

plt.rcParams.update({
    "font.size": 16,
    "font.family": "SF Pro",
    "svg.fonttype": "none",
})

font_path = "/home/jet/.local/share/fonts/SF-Pro.ttf"
sfpro = font_manager.FontProperties(fname=font_path)

plt.rcParams["font.family"] = sfpro.get_name()

parser = argparse.ArgumentParser("py " + os.path.basename(__file__))
_ = parser.add_argument("file", help="Tapbacks CSV input file")
_ = parser.add_argument("-o", "--output", default="./tapbacks.svg", help="Output file")
args = parser.parse_args()

tapback_order = [
    "Loved",
    "Liked",
    "Emphasized",
    "Questioned",
    "Disliked",
    "Laughed",
]

df = pd.read_csv(args.file)

j_df = df[df["name"] == "J"]
k_df = df[df["name"] == "K"]

j_counts = Counter(j_df["tapback"])
k_counts = Counter(k_df["tapback"])

j_values = [j_counts.get(t, 0) for t in tapback_order]
k_values = [k_counts.get(t, 0) for t in tapback_order]

N = len(tapback_order)

angles = np.linspace(0, 2 * np.pi, N, endpoint=False)
angles = np.concatenate([angles, [angles[0]]])  # close loop

j_values = j_values + [j_values[0]]
k_values = k_values + [k_values[0]]

fig, ax = plt.subplots(subplot_kw={"polar": True}, figsize=(12, 6))

ax.plot(angles, j_values, linewidth=2, color="#fe942b")
ax.fill(angles, j_values, alpha=0.25, color="#fe942b")

ax.set_xticks(angles[:-1])
ax.set_xticklabels(tapback_order)

ax.plot(angles, k_values, linewidth=2, color="#f150a8")
ax.fill(angles, k_values, alpha=0.25, color="#f150a8")

ax.set_xticks(angles[:-1])
ax.set_xticklabels(tapback_order)

ax.set_yticks([])
ax.set_yticklabels([])

plt.tight_layout()
plt.savefig(args.output)
plt.close()
