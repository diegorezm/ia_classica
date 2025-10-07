import json
from warnings import deprecated
from busca import Grafo, Custo
from typing import List
import networkx as nx
import matplotlib

matplotlib.use(
    "SVG"
)  # https://matplotlib.org/stable/users/explain/figure/backends.html#static-backends
import matplotlib.pyplot as plt
import io
import base64


@deprecated("Não é utilizado mais.")
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


def gerar_problema_json(json_path: str):
    """
    Recebe o caminho para um json e retorna um grafo, uma lista de nós e um dicionário de
    custos.
    O formato do json deve ser:
        Node: {
            Conexão: Valor
        }
    Portando um node deve conter um dicionario com todas as suas conexões e seus respectivos custos.
    """
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


def gerar_grafo(nos, grafo, costs=None, path=None):
    """
    Retorna uma string base64 que representa o grafo.
    """
    G = nx.Graph()

    # Adicionando as conexões
    for i, estado in enumerate(nos):
        for viz in grafo[i]:
            G.add_edge(estado, viz)

    # Layout
    pos = nx.spring_layout(G, k=1.0, iterations=70, seed=50)

    # Desenhando na tela
    nx.draw(
        G,
        pos,
        with_labels=True,
        node_color="lightblue",
        edge_color="gray",
        node_size=800,
        font_size=10,
    )

    # Marcando um caminho de vermelho
    if path:
        edges = list(zip(path, path[1:]))
        nx.draw_networkx_nodes(G, pos, nodelist=path, node_color="red")
        nx.draw_networkx_edges(G, pos, edgelist=edges, edge_color="red", width=2)

    # Se o dicionario de custos existir, use-o
    ## TODO: Melhorar a exibição dos custos.
    if costs:
        edge_labels = {}
        for u, v in G.edges():
            edge_labels[(u, v)] = costs.get((u, v), costs.get((v, u), ""))
        nx.draw_networkx_edge_labels(
            G, pos, edge_labels=edge_labels, font_color="black"
        )

    # Criando um string base64 para poder exibir o grafo no jinja
    buf = io.BytesIO()
    plt.savefig(buf, format="png")
    buf.seek(0)
    img_base64 = base64.b64encode(buf.read()).decode("utf-8")
    plt.close()
    return img_base64
