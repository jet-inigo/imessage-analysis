import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib import font_manager
import pandas as pd
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
_ = parser.add_argument("file")
_ = parser.add_argument("-o", "--output", default="./count.svg", help="Output file")
_ = parser.add_argument("--start", help="Start date cutoff (inclusive)")
_ = parser.add_argument("--end", help="End date cutoff (exclusive)")
args = parser.parse_args()

df = pd.read_csv(args.file)

df["timestamp"] = pd.to_datetime(df["timestamp"])

if args.start:
    df = df[df["timestamp"] >= args.start]
if args.end:
    df = df[df["timestamp"] < args.end]

df = df.set_index("timestamp")

monthly_cumsum = df.groupby("sender").resample("ME").size().unstack(level=0).fillna(0).cumsum()
monthly_cumsum["Total"] = monthly_cumsum["J"] + monthly_cumsum["K"]

fig, ax = plt.subplots(figsize=(12,6))

plt.plot(monthly_cumsum.index, monthly_cumsum["J"], label="J", marker="o", color="#fe942b")
plt.plot(monthly_cumsum.index, monthly_cumsum["K"], label="K", marker="o", color="#f150a8")
plt.plot(monthly_cumsum.index, monthly_cumsum["Total"], label="Total", linewidth=2, color="#1f6f9e")

ax.xaxis.set_major_locator(mdates.MonthLocator(interval=3))
ax.xaxis.set_major_formatter(mdates.DateFormatter("%b %Y"))

ax.tick_params(axis="x", bottom=False)

plt.xticks(rotation=45)
plt.legend()
plt.tight_layout()
plt.savefig(args.output)
plt.close()
