import json
import logging

from flask import Flask, Response
import networkx as nx
from networkx.readwrite import json_graph
import wotgraph.wotgraph as wot

app = Flask(__name__)

logging.basicConfig(level=logging.INFO)

logging.info("Loading graph")
G = wot.read_wot(wot.latest_wot())
logging.info("Ready")


@app.route('/')
def hello():
    return 'Hello World!'


@app.route('/ego/<keyid>.json')
def ego(keyid):
    logging.info('Getting ego network for {}'.format(keyid))
    ego = nx.ego_graph(G, keyid, undirected=True)
    data = json_graph.node_link_data(ego)
    return Response(json.dumps(data), mimetype='application/json')
