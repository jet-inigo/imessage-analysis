from matplotlib import font_manager
import pandas as pd
import argparse
from sklearn.feature_extraction.text import CountVectorizer
import matplotlib.pyplot as plt
import numpy as np
from nltk.corpus import stopwords
import nltk
import os
import re

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
_ = parser.add_argument("-o", "--output", default="./trigrams.svg", help="Output file")
args = parser.parse_args()

nltk.download("stopwords")

stop_words = stopwords.words("english")

df = pd.read_csv(args.file)

vectorizer = CountVectorizer(ngram_range=(3, 3), stop_words=stop_words)

def clean_text(text):
    # Lowercase
    text = text.lower()
    # Remove URLs
    text = re.sub(r"http\S+|www\S+", "", text)
    # Remove tokens with lots of numbers or mixed alphanumeric IDs
    text = " ".join([w for w in text.split() if w.isalpha()])
    return text

X = vectorizer.fit_transform(df["content"].dropna().apply(clean_text))

total_counts = X.sum(axis=0)

ngrams = vectorizer.get_feature_names_out()

total_counts_series = pd.Series(np.array(total_counts).flatten(), index=ngrams)
total_counts_series = total_counts_series.sort_values(ascending=False)

print(total_counts_series[:50])

fig, ax = plt.subplots(figsize=(12, 6))

total_counts_series[:5].plot.barh(color="#1f6f9e")
plt.gca().invert_yaxis()

ax.tick_params(axis="x", bottom=False)

plt.tight_layout()
plt.savefig(args.output)
plt.close()
