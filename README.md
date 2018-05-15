# Similarity_names_with_ddg

Similarity engine to match artist pseudonyms with their real names
using the duckduckgo API (https://duckduckgo.com/api)
More generally, it can match any two string queries based on the search
results and the associated similarity value.

# Installation
```sh
$pip3 install -r ./requirements.txt --user
$python3 -m spacy download en
$python3 -m spacy validate

```

# Use
```python
#compute the similarity score between two names based on the string
#query search results.

from Similarity_names_with_DDG.similarityEngine import NameSearch

doc1 = NameSearch('Booba')
doc2 = NameSearch('Elie Yaffa')

#Extract the similarity score between the 2 names
matrixscore=doc1.get_similarity_score(doc2, metric='max')
print (matrixscore)
```

# Test
```sh
$pytest
```
# Running an example
```
$python3 pseudo_real_matching.py
```
