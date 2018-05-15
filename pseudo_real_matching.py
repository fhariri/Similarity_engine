import pandas as pd
from Similarity_names_with_DDG.similarityEngine import NameSearch

if __name__=='__main__':
    #Reading the csv input files and creating pseudonym x real_name Data Frame to serve as similarity score matrix
    pseudonymList = pd.read_csv('data/pseudonym.csv', names=['pseudo'])
    realNamesList  = pd.read_csv('data/real_name.csv', names=['real'])
    score = pd.concat([pseudonymList, realNamesList], axis=1)
    score = pd.DataFrame(score, score.pseudo, score.real)

    ##############################################################
    #Retrieving similarity score value for each entry in the data frame score
    #and exporting the results to a csv file
   ##############################################################
    #Filling the generated n_real x n_pseudo data frame entries with the corresponding
    #similarity score
    for pseudo in score.index:          #looping over rows
        for real in score.columns:      #looping over columns
            #metric values='mean', 'max' (and 'min' if we are focusing on dissimilarity)
            score.loc[pseudo, real] = NameSearch(pseudo).get_similarity_score(NameSearch(real), metric='mean')

    #Exporting results to csv score files
    score.to_csv('data/score_matrix.csv')


    ##########################################################
    #Exporting features to a csv file
    #Each items in NameSearch.get_instances() follows the format:
    #(key, value)={query keyword: dictionary of associated features}
    ##########################################################
    itemsWithFeatures=[]
    groupedSearches=NameSearch.get_instances()
    for querySearch in groupedSearches:
        itemsWithFeatures.append(pd.DataFrame(groupedSearches[querySearch], index=[querySearch]))
    features = pd.concat(itemsWithFeatures)
    features.to_csv('data/features.csv')

