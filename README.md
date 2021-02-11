## Usage

Run the command:

```
python3 find_similar.py
```

## Additional Info

- If you install the latest versions of some of the packages (i.e. scikit-learn), you may need to downgrade them otherwise the code will raise an error.

- Although some intermediate files may be missing (such as keywords.edgelist), all the code that needed to generate them is there. In order to generate the intermediate files, run the files in this order:

```
construct_graph.py > create_embeddings.py > find_similar.py

```
