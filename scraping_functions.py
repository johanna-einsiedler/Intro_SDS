import requests # we will need requests to
import time 
import tqdm
from bs4 import BeautifulSoup  
from wordcloud import WordCloud, STOPWORDS # Need an install! 
import matplotlib.pyplot as plt
import seaborn as sns
from scraping_functions import *





##########################################################################################################
# Code for scraping ######################################################################################
##########################################################################################################

def make_query(query_term,page_num=1,iter_=5,wait=0.5):
   ## Add iterations for reliability in case of standard http errors
    response = False
    time.sleep(wait)
    for i in range(iter_):
        try:
            response = requests.get('https://www.allrecipes.com/element-api/content-proxy/faceted-searches-load-more?search=%s&page=%d'%(query_term,page_num))
      #, headers=headers, params=params, cookies=cookies)
            if response.ok:
                return response
        except:
            continue
    return response
def check_response(response):
    try:
        response_d = response.json()
    except:
        return {'error':True}
    if 'error' in response_d:
        print(response_d)
    return response_d

def page_data(query,result_count):
    results = []

    response_length = 24
    for page_num in tqdm.tqdm(range(result_count//response_length)):
        page_num+=1
        response = make_query(query,page_num=page_num)
        response_d = check_response(response)

        if 'error' in response_d:
            break
        results.append(response_d['html'])
        if response_d['hasNext']==False:
            break
    return results

def scrape_recipes(query) :
    response = make_query(query)
    response_d = check_response(response)
    count = response_d['totalResults']
    return page_data(query,count), count

##########################################################################################################
# Code for formatting dataframe ##########################################################################
##########################################################################################################

alt_vars = {'recipe_link':('a class="card__titleLink manual-link-behavior"','href'),
            'author_link':('a class="card__authorNameLink"','href')}

def parse_recipe_item(item, var2tags):
    d = {}
    for name,tag_attr in var2tags.items():
        tag,attr = tag_attr.split(maxsplit=1)
        class_name,identifier = attr.strip('"').split('="')
        identifier = {class_name:identifier}
        val = item.find(tag,attrs=identifier)
  # print(name,val)
        try:
            val = str(val.text.strip())
        except:
            continue
        d[name]= val
    for name,(tag_attr,key) in alt_vars.items():
        try :
            tag,attr = tag_attr.split(maxsplit=1)
            class_name,identifier = attr.strip('"').split('="')
            identifier = {class_name:identifier}
            val = item.find(tag,attrs=identifier)
            d[name] = str(val[key])
        except :
            continue
    return d

def get_recipes(html, var2tags):
    soup = BeautifulSoup(html,features="html.parser") # Beautifulsoup reads html data
    item_locs = soup.find_all('div',attrs={'class':'component card card__recipe card__facetedSearchResult'})
    data = []
    for item in item_locs:
        data.append(parse_recipe_item(item, var2tags))
    return data



def get_title_words(df):

    #Collect all the titles into one large string
    # we first create an empty variable 
    title_words='' 
    
    for val in df.title:
        
        # typecaste each val to string
        val = str(val)
    
        # split the value
        tokens = val.split()
        
        # Converts each token into lowercase
        for i in range(len(tokens)):
            tokens[i] = tokens[i].lower()
        
        title_words += " ".join(tokens)+" "
        
    return(title_words)