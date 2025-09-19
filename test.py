from busca import BuscaEmGrafo
from utils import parse_json_graph

b = BuscaEmGrafo()

grafo, nos, custos = parse_json_graph("data.json")
print(b.a_estrela("R1", "R11", nos, grafo, custos))
