import pandas as pd
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from Similarity_names_with_DDG.similarityEngine import NameSearch
import seaborn as sb

if __name__=='__main__':
    #Reading the csv score matrix input file to generate a pandas data frame
    columnNames=['pseudo', 'Andre Romelle Young', 'Bruno Beausir', 'Bruno Lopes', 'Didier Morville',\
                 'Dwayne Johnson', 'Elie Yaffa', 'Gary Grice', 'Marshall Mathers', 'Mathias Crochon','Patrick Benguigui',\
                 'Shawn Corey Carter']
    scoreList = pd.read_csv('data/score_matrixMax.csv', index_col='pseudo', names=columnNames)
    
    #####################################################################
    #           Creating the dictionary required for the seaborn heatmap
    ######################################################################
    '''
    #Creating the dictionary to be used for the dataframe required for the heatmap plot
    #with seaborn. dico format is as follows:
    dico['pseudo']=vrow   where vrow is a list containing all the row values i.e. pseudonyms
    dico['real']=vCol         where vCol is a list containing all column values i.e. real names
    dico['value']=vValue    where vValue is a list containg score values of (pseudo,real) pair
    '''
    dico={}
    vrow=[]
    vCol=[]
    vValue=[]
    
    #####################################################################
    #           Filling dico, vrow, vCol and vValue with appropriate entries
    ######################################################################
    '''
    #Reading the generated n_pseudo x n_real data frame entries with the corresponding
    #similarity score. Number pseudonyms= Number real names=len(columnNames)-1
    We start with the second entry in scoreList.index since scoreList.index[0]='pseudo'
    >>> scoreList.index
        Index(['pseudo', 'Booba', 'Doc Gyneco', 'Dr. Dre', 'Eminem', 'GZA', 'Jay-Z',
               'Joey Starr', 'Kool Shen', 'Patrick Bruel', 'Rockin' Squat',
               'The Rock'],
              dtype='object', name='pseudo')
    >>> scoreList.columns
            Index(['Andre Romelle Young', 'Bruno Beausir', 'Bruno Lopes',
                     'Didier Morville', 'Dwayne Johnson', 'Elie Yaffa', 'Gary Grice',
                     'Marshall Mathers', 'Mathias Crochon', 'Patrick Benguigui',
                     'Shawn Corey Carter'],
                    dtype='object')
    '''
    for i in range(1,len(columnNames)):
        for real in scoreList.columns:
            vrow.append(scoreList.index[i])
            vCol.append(real)
            vValue.append(round(float(scoreList.loc[scoreList.index[i], real]),3))
    
    dico['pseudo']=vrow
    dico['real']=vCol
    dico['value']=vValue

    #####################################################################
    #           Plotting the seaborn heatmap from a DataFrame with dico
    ######################################################################
    df = pd.DataFrame(dico)
    result = df.pivot(index='real', columns='pseudo', values='value')

    f, ax = plt.subplots()
    plt.setp(ax.get_xticklabels(), rotation=45, ha="right",
         rotation_mode="anchor")
    
    sb.heatmap(result, annot=True, fmt="g", linewidths=.5, ax=ax)
    plt.show()
  
    #####################################
   


