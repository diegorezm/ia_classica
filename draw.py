import networkx as nx
import matplotlib.pyplot as plt
import io
import base64


def draw_graph(nos, grafo, path=None):
    G = nx.Graph()

    # Build graph
    for i, estado in enumerate(nos):
        for viz in grafo[i]:
            G.add_edge(estado, viz)

    # Layout for nodes
    pos = nx.spring_layout(G)

    # Draw all nodes and edges
    nx.draw(
        G,
        pos,
        with_labels=True,
        node_color="lightblue",
        edge_color="gray",
        node_size=800,
        font_size=10,
    )

    # If path exists, highlight it
    if path:
        edges = list(zip(path, path[1:]))  # consecutive pairs
        nx.draw_networkx_nodes(G, pos, nodelist=path, node_color="red")
        nx.draw_networkx_edges(G, pos, edgelist=edges, edge_color="red", width=2)

    # Save to base64 for Flask template
    buf = io.BytesIO()
    plt.savefig(buf, format="png")
    buf.seek(0)
    img_base64 = base64.b64encode(buf.read()).decode("utf-8")
    plt.close()
    return img_base64
