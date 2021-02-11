import networkx as nx
from nodevectors import Node2Vec

# Test Graph
model_name = "structwords"
graph_file = "data/keywords.edgelist"

# G = nx.read_weighted_edgelist(graph_file)
G = nx.read_weighted_edgelist(graph_file)

# Fit embedding model to graph
g2v = Node2Vec(neighbor_weight=3)

# way faster than other node2vec implementations
# Graph edge weights are handled automatically
g2v.fit(G)

# Save and load whole node2vec model
# Uses a smart pickling method to avoid serialization errors
# Don't put a file extension after the `.save()` filename, `.zip` is automatically added
g2v.save(model_name)
