import pandas as pd # pandas is a package that makes it easier to deal with dataframes
import matplotlib.pyplot as plt # matplotlib is python's standard package for data plotting
import seaborn as sns # seaborn will make your plots prettier
from scraping_functions import * # we have prepared some functions in a separate file that will make your life easier which we are importing here
import networkx as nx
import itertools



def create_network(df,attribute):
    # create edge dataframe
    df_pairs = pd.DataFrame(list(itertools.combinations(df.nickname,2)))
    df_pairs.columns= ['from','to']
    df_pairs = df_pairs.merge(df, left_on='from',right_on='nickname',how='left')
    df_pairs = df_pairs.merge(df, left_on='to',right_on='nickname',how='left')


    if attribute == 'hobbies':

        def compare_cols(x,y):
            return len(list(set(x).intersection(y)))>0
        
        same_hobbies =df_pairs.apply(lambda x: compare_cols(x.hobbies_x, x.hobbies_y),axis=1)
        edges = df_pairs[same_hobbies][['from','to']]
    
    else:
        # get attribute to create links from
        attr_x = attribute + '_x'
        attr_y = attribute + '_y'

        edges = df_pairs[df_pairs[attr_x]==df_pairs[attr_y]][['from','to']]
    edges = edges.to_records(index=False)

    df = df.drop('hobbies',axis=1)

    # get nodes
    dft = df.transpose()
    dft.columns = dft.iloc[1,]
    nodes = dft.to_dict()


    # create graph
    G = nx.DiGraph()

    # add nodes
    G.add_edges_from(edges)
    G.add_nodes_from(nodes.items())
    return G