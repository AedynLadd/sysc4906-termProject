# This is just a helper file to move data from our data analysis section and store it in usable dashboard style data because im lazy :)
from enum import unique
from importlib.resources import path
import json
import logging
from sqlite3 import Row
import pandas as pd
from pathlib import Path
import networkx as nx


logger = logging.getLogger("Dashboard compiler")

project_dir = "./"

def compile_historical_data():
    try:
        f = open("{}/data/raw/coinmarketcap/historical_data.json".format(project_dir))
        compiled_historical_data = json.load(f)
        try:
            new_f = open("{}/dashboard/data/historical_data.js".format(project_dir), "w")
            new_f.write("const historical_coin_data = {}".format(compiled_historical_data))
        except:
            new_f = open("{}/dashboard/data/historical_data.js".format(project_dir), "x")
            new_f.write("const historical_coin_data = {}".format(compiled_historical_data))
        return 200
    except Exception as e:
        logger.info(e)
        return 400

def compile_reddit_summary_data():
    try:
        f = open("{}/data/processed/reddit_summary_subs.json".format(project_dir))
        compiled_reddit_summary = json.load(f)
        try:
            new_f = open("{}/dashboard/data/reddit_summary_subs.js".format(project_dir), "w")
            new_f.write("const reddit_summary = {}".format(compiled_reddit_summary))
        except:
            new_f = open("{}/dashboard/data/reddit_summary_subs.js".format(project_dir), "x")
            new_f.write("const reddit_summary = {}".format(compiled_reddit_summary))
        return 200
    except Exception as e:
        logger.info(e)
        return 400

def compile_top_coin_data():
    try:
        f = open("{}/data/raw/coinmarketcap/top_100_coins.json".format(project_dir))
        compiled_coin_data = json.load(f)
        try:
            new_f = open("{}/dashboard/data/top_100_coins.js".format(project_dir), "w")
            new_f.write("const top_100_coins = {}".format(compiled_coin_data["coins"]))
        except:
            new_f = open("{}/dashboard/data/top_100_coins.js".format(project_dir), "x")
            new_f.write("const top_100_coins = {}".format(compiled_coin_data["coins"]))
        return 200
    except Exception as e:
        logger.info(e)
        return 400

def create_network_formatted_data():
    # The format our data has to be in is as follow.
    # {
    #   "nodes": [
    #     {
    #       "id": 1,
    #       "name": "A"
    #     } .....
    #   ],
    #   "links": [
    #     {
    #       "source": 1, ie the appropriate id
    #       "target": 2
    #     }
    #     ]
    # }
    #
    # We can use this to create our list of nodes
    our_reddit_data = pd.read_json(open("{}/data/interim/reddit_processed.json".format(project_dir)))
    split_df = pd.DataFrame(our_reddit_data["keywords"])

    unique_nodes = set()
    node_links = dict()
    for row in range(0,len(split_df)):
        row = split_df.iloc[row][0]
        try:
            if(len(row) > 0):
                for x in row:
                    unique_nodes.add(x)
                    for y in row:
                        try:
                            node_links[x].append(y)
                        except:
                            node_links[x] = []
                            node_links[x].append(y)
        except Exception as e:
            print(e)

    OurNodes = []
    OurLinks = []
    id = 0
    node_count_list = {}
    G = nx.Graph()

    node_link_list = {}

    for node in unique_nodes:
        id += 1
        node_link_list[id] = []

    id = 0
    for node in unique_nodes:
        id += 1
        OurNodes.append({
            "id": id,
            "name": node
        })
        node_count_list[node] = {}
        link_df = pd.DataFrame(node_links[node])
        count_df = pd.DataFrame(link_df.value_counts())
        for element, count in count_df.iterrows():

            node_count_list[node][str(element[0])] = int(count)
            end_id = list(unique_nodes).index(element[0]) + 1

            if(id != end_id):
                
                G.add_edge(id, end_id)

                if(not(id in node_link_list[end_id] and end_id in node_link_list[id])):
                    node_link_list[end_id].append(id)
                    node_link_list[id].append(end_id)

                    OurLinks.append({
                        "source": id,
                        "target": end_id,
                        "value": int(count)
                    })

    degree_centrality = nx.degree_centrality(G)
    
    betweeness_centrality = nx.betweenness_centrality(G, normalized=False)

    betweeness_centrality_normalized = nx.betweenness_centrality(G)

    def validate_ref(id, ref_dict):
        try: 
            return ref_dict[int(id)]
        except Exception as e:
            return 0
        
    OurNodes = [{"id": ThisNode["id"],
                 "name": ThisNode["name"], 
                 "data": {
                        "degree":  validate_ref(ThisNode["id"], degree_centrality),
                        "betweeness":  validate_ref(ThisNode["id"], betweeness_centrality),
                        "normalized_betweeness": validate_ref(ThisNode["id"], betweeness_centrality_normalized)
                    }   
                } for ThisNode in OurNodes ]


    data = {"nodes": OurNodes, "links": OurLinks}

    try:
        new_f = open("{}/dashboard/data/keyword_network_data.js".format(project_dir), "w")
        new_f.write("const network_data = {}".format(data))
    except:
        new_f = open("{}/dashboard/data/keyword_network_data.js".format(project_dir), "x")
        new_f.write("const network_data = {}".format(data))

    try:
        new_f = open("{}/dashboard/data/keyword_count_data.js".format(project_dir), "w")
        new_f.write("const network_keyword_count = {}".format(node_count_list))
    except:
        new_f = open("{}/dashboard/data/keyword_count_data.js".format(project_dir), "x")
        new_f.write("const network_keyword_count = {}".format(node_count_list))

    return 200


if __name__ == '__main__':
    try:
        project_dir = Path(__file__).resolve().parents[2]

        log_fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        logging.basicConfig(level=logging.INFO, format=log_fmt,
                            handlers= [
                                logging.FileHandler("{}/logs/dashboard_compile.log".format(project_dir), mode = "w"),
                                logging.StreamHandler()
                            ])

        logger.info("Running in {}".format(project_dir))
        
        compile_historical_data()
        compile_reddit_summary_data()
        compile_top_coin_data()
        create_network_formatted_data()

        logger.info("Dashboard compilation completed - - - Exiting")
    except Exception as e:
        logger.error(e)

