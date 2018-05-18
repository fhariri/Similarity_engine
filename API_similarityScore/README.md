# API_similarityScore

Api that takes two strings and returns the computed similarity score

# Installation
```sh
$pip3 install -r requirements.txt --user
```

# Use
```python
#retrieve the similarity score between two names based on the
#computed results
from requests import get

r=get('http://localhost:5000/score/Elie Yaffa/Booba')
score=r.json()['score']

print (score)
```

# Running an example
```
$ python3 API_similarityScore.py
In Firefox:
Use the following URL syntax http://localhost:5000/score/name1/name2
http://localhost:5000/score/Dr. Dre/Andre Romelle Young
http://localhost:5000/score/Elie Yaffa/Booba

In Insomnia
Create a GET request and use the URL syntax:
http://localhost:5000/score/name1/name2
e.g. http://localhost:5000/score/Elie Yaffa/Booba and click SEND


In python3: 
$ python3
>>> from requests import get
>>> r=get('http://localhost:5000/score/Elie Yaffa/Booba')
>>> r.json()
{'score': ['0.9634284925575057']}
>>> r=get('http://localhost:5000/score/Eminem/Elie Yaffa')
>>> r.json()
{'score': ['0.7384044828722635']}
>>> r.json()['score']
['0.7384044828722635']
```

