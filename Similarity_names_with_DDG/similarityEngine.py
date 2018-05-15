import spacy
import requests
import time
from json.decoder import JSONDecodeError
from googletrans import Translator
from .duckduckgo import duckduckgo
from lxml import html
from bs4 import BeautifulSoup

nlp = spacy.load('en')

class NameSearch:
    '''
        Class description:
        Based on a string query, a NameSearch object, an instance of this class will be created with the
        the following attributes:
        -self.searchKeyword:=this is the string query to be used to retrieve search results with the duckduckgo API
        -self.features:= this is a dictionary of the associated features with keys  ['abstract_text', 'abstract_url',
        'image_url', 'heading']
        
       *The class variable  _ElementDict={}: class variable where all the created instances of this class during a session
       will be stored. This is a dictionary with (key, value) pairs defined as
                            (key,value)={query keyword: dictionary of associated features}
        '''
    
    _ElementDict={}
   
    def __init__(self, string_query):
        
        self.searchKeyword=string_query
        self.features= self.get_features(self.searchKeyword)
        if self.searchKeyword not in NameSearch._ElementDict.keys():
            NameSearch._ElementDict[self.searchKeyword]=self.features
    


##########################################################################
#  Applying natural language processing through spacy's nlp method to the features of each
# search query to prepare them for similarity calculations. The tokenization nlp(argument)
# returns a list of tokens with attributes such as token.text
# Example:  t=nlp('Hello World!') items are Hello, World and !
##########################################################################

    def nlp_extracted_feature(self):
        token_features={}
        for key in self.features:
            token_features[key]=nlp(self.features[key])
        return token_features
    
    
    
##########################################################################
#  Extracting features associated with the string query using duckduckgo2 lib method
#  duckduckgo.query() first, retrieving results in english or in french and translating them to
#  english if no direct good result was found in english. In case of failure to have meaningful
#   results, it switches to google results through duckduckgo bangs feature
##########################################################################

    def get_features(self,string):
        # Extracting features associated with the string query in english
        response= duckduckgo.query(string)
        if response.abstract.text:
            features = {
                'abstract_text': response.abstract.text,
                'abstract_url': response.abstract.url,
                'image_url': response.image.url.split('/')[-1],         #removes usual DDG address prefix
                'heading': response.heading
            }
    

        # If nothing found in english => get the french version and translate it into english.
        #We have many local french artists in the names list. Other languages can be used too.
        else:
            response = duckduckgo.query(string, kad='fr_Fr')
            gtrans = Translator()
            features = {
                'abstract_text': gtrans.translate(response.abstract.text, dest='en').text,
                'abstract_url': response.abstract.url,
                'image_url': response.image.url.split('/')[-1],
                'heading': response.heading
                        }
        
        #switching to google results through duckduckgo bangs feature
        if not features['abstract_text']:
            print("Executing self.get_bangresult \n")
            features=self.get_bangresult(string)
            if len(features)==0:
                print ('ERROR: No results associated with the search keyword '+string+str(" were found!"))

        return features
            
            
            
            
            
    ##########################################################################################
    #Extracting features by scraping and parsing google HTML results obtained through duckduckgo bangs feature
    ###########################################################################################
    def get_bangresult(self,string):
        USER_AGENT = {'User-Agent':'Mozilla/5.0 (X11; Linux i686) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.83 Safari/535.11'}
        r=duckduckgo.query('!g '+string)
        
        '''
        looks like https://google.com/search?hl=en&q=string
        '''
        google_search_link= r.redirect.url
        number_results=10
        
        #formatting search link and choosing number of results desired
        escaped_search_term = google_search_link.replace(' ', '+')
        escaped_search_term = escaped_search_term.replace('%20', '+')
        google_url = google_search_link+'&num={}'.format( number_results)
        
        #Extracting the response and its html
        response = requests.get(google_url, headers=USER_AGENT)
        response.raise_for_status()
        html=response.text
        soup = BeautifulSoup(html, 'html.parser')
        result_block = soup.find_all('div', attrs={'class': 'g'})
        
        #Retrieving features
        for result in result_block:
            link = result.a['href']
            title = result.find('h3', attrs={'class': 'r'})
            title=str(title.get_text())
            description = result.find('span', attrs={'class': 'st'})
            if link and description:
                features = {
                    'abstract_text': description.get_text(),
                    'abstract_url': link,
                    'image_url': '',
                    'heading': title[0:title.rfind('-')]
                    }
                break
        return features
                


##########################################################################
#               To extract all instances processed
##########################################################################
    @classmethod
    def get_instances(cls):
        return cls._ElementDict
    
##########################################################################
#   Calculate similarity among 2 query features (after tokenization with nlp()) using spaCy
# built-in function, which does a semantic similarity estimate over the object's feature. This
# is by default a cosine similarity calculated using the corresponding vectors (an algorithm
# generates vectors for tokens)
##########################################################################
    
    def calculate_similarity_matrix(self, query2_result):
        similarity_values=[]
        token_nlp_features=self.nlp_extracted_feature()
        item2_nlp_features=query2_result.nlp_extracted_feature()
        #return matrix with similarity value for each feature comparison
        for name in ['abstract_text', 'abstract_url', 'heading']:
            if(token_nlp_features[name] and item2_nlp_features[name]):
                token_nlp_features[name].similarity(item2_nlp_features[name])
                similarity_values.append(token_nlp_features[name].similarity(item2_nlp_features[name]))
        return similarity_values

##########################################################################
#               Get the final similarity score to associate with query1-query2 comparison
##########################################################################
    def get_similarity_score(self, query2_result, metric='mean'):
        similarity_values=self.calculate_similarity_matrix(query2_result)
        allowed_metrics = ['mean', 'max', 'min']    #min can be used for dissimilarity studies
        if metric not in allowed_metrics:
            raise ValueError('metric must be either {}.'.format(' ,'.join(allowed_metrics)))
        if metric == 'mean':
            return sum(similarity_values) / len(similarity_values)
        elif metric == 'max':
            return max(similarity_values)
        else:
            return min(similarity_values)
        return
##########################################################################
##########################################################################
