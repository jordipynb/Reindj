# Freindj
This project aims to create a Search Engine with an Information Retrieval System.  
Three information retrieval models must be created based on three document collections and the pertinent metrics must be established to evaluate each model. 
  
| Author    | Implemented Model | Corpus     | State   | 
|---------- |-------------------|------------|---------|
| Jordan    | Vector            | Cranfield  | Done    |
| Felix     | Boolean           | TREC-Covid | Done    |
| Dianelys  | Latent Semantics  | Vaswani    | Done    |
                                      

To run the code: 
```
$ uvicorn main:app --reload
```
You must have python, uvicorn, nltk and numpy installed, check the requirements for more details.  
Requirements can be found in a ```requirements.txt``` inside the main project directory. Any code editor or IDE offers the facilities to satisfy such requirements.
