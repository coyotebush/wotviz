import json
import logging

from flask import Flask, Response, render_template
import networkx as nx
from networkx.readwrite import json_graph
import wotgraph.wotgraph as wot

app = Flask(__name__)

logging.basicConfig(level=logging.INFO)

logging.info("Loading graph")
G = wot.read_wot(wot.latest_wot())
logging.info("Ready")


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/ego/<keyid>.json')
def ego(keyid):
    logging.info('Getting ego network for {}'.format(keyid))
    ego = nx.ego_graph(G, keyid, undirected=True, radius=2)
    logging.info('Computing layout')
    layout = nx.spring_layout(ego)
    data = json_graph.node_link_data(ego)
    data['layout'] = [x.tolist() for x in layout.values()]
    return Response(json.dumps(data), mimetype='application/json')
