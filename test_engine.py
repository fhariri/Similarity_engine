from Similarity_names_with_DDG.similarityEngine import NameSearch

def test_NameSearch():
    
    # compute similarity score between two search query terms.
    doc1 = NameSearch('marshall bruce mathers')
    doc2 = NameSearch('Eminem')
    score=doc1.get_similarity_score(doc2, metric='max')
    assert score==1

    




