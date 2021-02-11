## Usage

Run the command:

```
python3 find_similar.py
```

## Additional Info

- If you install the latest versions of some of the packages (i.e. scikit-learn), you may need to downgrade them otherwise the code will raise an error.

- Although some intermediate files may be missing (such as keywords.edgelist), all the code that is needed to generate them is there. The initial arxiv-snapshot dataset used to construct graph can be found at
  https://www.kaggle.com/Cornell-University/arxiv?select=arxiv-metadata-oai-snapshot.json

* If you want to regenerate all data files, run the python scripts in this order:

```
construct_graph.py > create_embeddings.py > find_similar.py

```

If you only want regenerate the missing files, make sure all dependencies of the python script are present.
