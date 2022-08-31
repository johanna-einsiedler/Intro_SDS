import pandas as pd # pandas is a package that makes it easier to deal with dataframes
import matplotlib.pyplot as plt # matplotlib is python's standard package for data plotting
import seaborn as sns # seaborn will make your plots prettier
import networkx as nx
import itertools
import numpy as np


def create_network(df,attribute):
     # this function converts everything to lowercase
    df = df.applymap(lambda s:s.lower()if type(s)==str else s)
    

    if attribute in ['hobbies','food','social_media','study']:

        # create Graph
        G = nx.Graph()

        # add nodes of type 1 (i.e. people)
        dft = df.transpose()
        dft.columns = dft.iloc[0]
        nodes = dft.to_dict()
        G.add_nodes_from(nodes, bipartite=1)

        
        hlist = df[attribute].str.split(',',expand=False).values.tolist()
        hlist = [item for sublist in hlist for item in sublist]
        hlist = [i.strip() for i in hlist]
        # add nodes of type 0
        G.add_nodes_from(np.unique(hlist),bipartite=0)
    

        hobbies_list = df[attribute].str.split(',',expand=False)
        df = df.drop(attribute,axis=1)
        df = pd.concat([df,hobbies_list],axis=1)

        edges = df.explode(attribute).reset_index(drop=True)
        edges[attribute] = edges[attribute].str.strip()
        G.add_edges_from(edges[['nickname',attribute]].to_records(index=False))
        
        return G
    
    else:
        # get nodes
        dft = df.transpose()
        dft.columns = dft.iloc[0]
        nodes = dft.to_dict()

        # create edge dataframe
        df_pairs = pd.DataFrame(list(itertools.combinations(df.nickname,2)))
        df_pairs.columns= ['from','to']
        df_pairs = df_pairs.merge(df, left_on='from',right_on='nickname',how='left')
        df_pairs = df_pairs.merge(df, left_on='to',right_on='nickname',how='left')

        # get attribute to create links from
        attr_x = attribute + '_x'
        attr_y = attribute + '_y'

        #def compare_cols(x,y):
         #       return len(list(set(x).intersection(y)))>0
        

        edges = df_pairs[df_pairs[attr_x]==df_pairs[attr_y]][['from','to']]
        edges = edges.to_records(index=False)

        #df = df.drop('hobbies',axis=1)
        #df = df.drop('social_media',axis=1)
        #df = df.drop('food',axis=1)




        # create graph
        G = nx.DiGraph()

        # add nodes
        G.add_edges_from(edges)
        G.add_nodes_from(nodes.items())
        return G