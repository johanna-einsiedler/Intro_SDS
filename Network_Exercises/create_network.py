import pandas as pd # pandas is a package that makes it easier to deal with dataframes
import matplotlib.pyplot as plt # matplotlib is python's standard package for data plotting
import seaborn as sns # seaborn will make your plots prettier
import networkx as nx
import itertools


def create_network(df,attribute):
     # this function converts everything to lowercase
    df = df.applymap(lambda s:s.lower()if type(s)==str else s)

    # get nodes
    dft = df.transpose()
    dft.columns = dft.iloc[0]
    nodes = dft.to_dict()

    #currently the hobbies are listed in a string variable - this code converts them to a list
    hobbies_list = df['hobbies'].str.split(',',n=2,expand=False)
    df = df.drop('hobbies',axis=1)
    df = pd.concat([df,hobbies_list],axis=1)

    # same for food
    food_list = df['food'].str.split(',',n=2,expand=False)
    df = df.drop('food',axis=1)
    df = pd.concat([df,food_list],axis=1)

    # same for social media
    sm_list = df['social_media'].str.split(',',n=2,expand=False)
    df = df.drop('social_media',axis=1)
    df = pd.concat([df,sm_list],axis=1)

    # create edge dataframe
    df_pairs = pd.DataFrame(list(itertools.combinations(df.nickname,2)))
    df_pairs.columns= ['from','to']
    df_pairs = df_pairs.merge(df, left_on='from',right_on='nickname',how='left')
    df_pairs = df_pairs.merge(df, left_on='to',right_on='nickname',how='left')

    # get attribute to create links from
    attr_x = attribute + '_x'
    attr_y = attribute + '_y'

    def compare_cols(x,y):
            return len(list(set(x).intersection(y)))>0

    if attribute == 'hobbies':
        same_hobbies = df_pairs.apply(lambda x: compare_cols(x.hobbies_x, x.hobbies_y),axis=1)
        edges = df_pairs[same_hobbies][['from','to']]

    if attribute == 'food':
        same_food = df_pairs.apply(lambda x: compare_cols(x.food_x, x.food_y),axis=1)
        edges = df_pairs[same_food][['from','to']]

    if attribute == 'social_media':
        same_sm = df_pairs.apply(lambda x: compare_cols(x.social_media_x, x.social_media_y),axis=1)
        edges = df_pairs[same_sm][['from','to']]
    
    else:
     

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