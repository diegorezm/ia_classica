import json
from busca import Grafo, Custo
from typing import List
import networkx as nx
import matplotlib.pyplot as plt
import io
import base64


def parse_graph(text: list[str]):
    grafo: Grafo = []
    nos: List[str] = []

    for line in text:
        line_split = line.split(",")
        estado = line_split.pop(0).strip()

        if estado not in nos:
            nos.append(estado)

        parts: List[str] = [p.strip() for p in line_split]
        if parts:
            grafo.append(parts)
    return grafo, nos


def parse_json_graph(json_path: str):
    with open(json_path, "r") as f:
        data = json.load(f)
    grafo: Grafo = []
    nos: List[str] = []
    custos: Custo = {}

    for estado, vizinhos in data.items():
        if estado not in nos:
            nos.append(estado)
        grafo.append(list(vizinhos.keys()))

        for viz, custo in vizinhos.items():
            custos[(estado, viz)] = custo

    return grafo, nos, custos


def draw_graph(nos, grafo, costs=None, path=None):
    G = nx.Graph()

    # Build graph
    for i, estado in enumerate(nos):
        for viz in grafo[i]:
            G.add_edge(estado, viz)

    # Layout
    pos = nx.spring_layout(G, scale=3.0, k=1.0, iterations=50)

    # Draw nodes and edges
    nx.draw(
        G,
        pos,
        with_labels=True,
        node_color="lightblue",
        edge_color="gray",
        node_size=800,
        font_size=10,
    )

    if costs:
        edge_labels = {}
        for u, v in G.edges():
            edge_labels[(u, v)] = costs.get((u, v), costs.get((v, u), ""))
        nx.draw_networkx_edge_labels(
            G, pos, edge_labels=edge_labels, font_color="black"
        )

    if path:
        edges = list(zip(path, path[1:]))
        nx.draw_networkx_nodes(G, pos, nodelist=path, node_color="red")
        nx.draw_networkx_edges(G, pos, edgelist=edges, edge_color="red", width=2)

    # Save to base64
    buf = io.BytesIO()
    plt.savefig(buf, format="png")
    buf.seek(0)
    img_base64 = base64.b64encode(buf.read()).decode("utf-8")
    plt.close()
    return img_base64
