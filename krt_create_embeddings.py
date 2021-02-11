import pickle
import networkx as nx
from karateclub import Node2Vec

task_name = "sample"
graph_file = "data/" + task_name + ".edgelist"
embedding_file = "data/" + task_name + ".emb"


# G = nx.read_weighted_edgelist(graph_file)
G = nx.read_weighted_edgelist(graph_file, nodetype=int)

# nSketch = NodeSketch(iterations=3, decay=0.2)
nSketch = Node2Vec(p=0.5)
nSketch.fit(G)


# Save and load whole node2vec model
# Uses a smart pickling method to avoid serialization errors
# Don't put a file extension after the `.save()` filename, `.zip` is automatically added
embeddings = nSketch.get_embedding()

with open(embedding_file, 'wb') as f:
    pickle.dump(embeddings, f)
