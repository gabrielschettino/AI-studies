import pickle
import pandas as pd
from collections import defaultdict
from nltk.corpus import stopwords

dataset = pickle.load(open('cosplay.xxx', 'rb'))

top_n = 10

word_freq = defaultdict(int)
custom_words = {}


for title in dataset['title']:

    title = title.lower()
    words = title.split()

    stop_words = set(stopwords.words('english')).union(custom_words)
    words = [word for word in words if word not in stop_words]

    for word in words:
        word_freq[word] += 1

sorted_freq = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)

top_words = []
non_meaningful_words = set(stopwords.words('english'))

for word, freq in sorted_freq:
    if word not in non_meaningful_words:
        top_words.append(word)

    if len(top_words) == top_n:
        break

print(top_words)
