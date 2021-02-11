import re
import copy
import json
import math
import pickle
import pandas as pd
from trie import Trie


# Input data
idx_file = 'data/word_index.pickle'
edgelist_file = "graph/sample.edgelist"

def get_paper_data():
    with open('data/arxiv-metadata-oai-snapshot.json', 'r') as f:
        for line in f:
            yield line

keywords_full_data = pd.read_csv('data/mag_cs_keywords.csv')
keywords_full_data['normalizedName'] = keywords_full_data['normalizedName'].fillna('nan')
keywords_data = keywords_full_data['normalizedName']


# Trie regexp for efficient unioning
def construct_re():
    trie = Trie()
    for keyword in keywords_data:
        trie.add(keyword)
    return re.compile(r"\b" + trie.pattern() + r"\b", re.IGNORECASE)

keywords_re = construct_re()
num_words = keywords_data.shape[0]


# Inverted index dict for keywords
word_to_idx = {}
try:
    with open(idx_file, 'rb') as f:
        word_to_idx = pickle.load(f)
except:
    for i in range(num_words):
        word_to_idx[keywords_data.iloc[i]] = i

    with open(idx_file, 'wb') as handle:
        pickle.dump(word_to_idx, handle, protocol=pickle.HIGHEST_PROTOCOL)


# Implementation of graph to keep track of co-occurences of papers
adjacency_dict = {}

def increment_edge(word1, word2):
    word_idx1 = word_to_idx[word1]
    word_idx2 = word_to_idx[word2]

    smaller_idx = min(word_idx1, word_idx2)
    larger_idx = max(word_idx1, word_idx2)

    if larger_idx not in adjacency_dict:
        adjacency_dict[larger_idx] = {}

    if smaller_idx not in adjacency_dict[larger_idx]:
        adjacency_dict[larger_idx][smaller_idx] = 1
    else:
        adjacency_dict[larger_idx][smaller_idx] += 1


# Parse data from papers (keyword search)
papers = get_paper_data()

p_i = 0
for paper in papers:
    paper_abstract = json.loads(paper)['abstract']
    keyword_matches = re.finditer(keywords_re, paper_abstract)
    keyword_matches = list(set(map(lambda s : s.group().lower(), keyword_matches)))

    for i in range(len(keyword_matches)):
        for j in range(i + 1, len(keyword_matches)):
            increment_edge(keyword_matches[i], keyword_matches[j])

    p_i += 1


# print(adjacency_dict)

# Write graph data out to file
# f = open(edgelist_file, "w")
# for u in adjacency_dict.keys():
#     for v in adjacency_dict[u].keys():
#         f.write(str(u) + " " + str(v) + " " + str(adjacency_dict[u][v]) + "\n")
