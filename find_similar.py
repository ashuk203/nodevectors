import pickle
import numpy as np
import pandas as pd
from nodevectors import Node2Vec


model_name = "keywords_deep"
idx_file = "data/word_index.pickle"
keywords_file = "data/mag_cs_keywords.csv"


# Load in relevant data and modules
keywords_full_data = pd.read_csv(keywords_file)
keywords_full_data['normalizedName'] = keywords_full_data['normalizedName'].fillna('nan')
keywords_data = keywords_full_data['normalizedName']

with open(idx_file, 'rb') as f:
    word_to_idx = pickle.load(f)

keyword_embs = Node2Vec.load(model_name + ".zip")


# Process word queries
while True:
    print("Please enter a word to search: ")
    query_word = input()

    query_node_idx = -1
    query_node = None

    while query_node_idx < 0:
        try:
            query_node_idx = word_to_idx[query_word.lower()]
            query_node = keyword_embs.predict(query_node_idx)
        except:
            print("Unfortunately, that word is not in the database. Please try another word:")
            query_word = input()



    # Sorted list of tuples containing most similar nodes (using pickled dict)
    closest_nodes = []
    max_results = 10

    def add_node(idx, score):
        has_inserted = False
        elem = (idx, score)

        for i in range(min(max_results, len(closest_nodes))):
            if closest_nodes[i][1] < score:
                closest_nodes.insert(i, elem)
                has_inserted = True
                break

        if not has_inserted:
            closest_nodes.append(elem)

        if len(closest_nodes) > max_results:
            closest_nodes.pop()



    for node_idx in range(len(keywords_data)):
        if node_idx != query_node_idx:
            try:
                curr_node = keyword_embs.predict(node_idx)
                sim_score = np.inner(query_node, curr_node)
                # print("similarity to node " + str(node_idx) + " is " + str(sim_score))

                if len(closest_nodes) < max_results or closest_nodes[-1][1] < sim_score:
                    add_node(node_idx, sim_score)

            except:
                # Model does not have any data for this node
                pass

    print("Search results for '" + query_word + "' : ")
    for res in closest_nodes:
        print("\t" + keywords_data.iloc[res[0]])

    print("\n")
