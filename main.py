from typing import List
from busca import BuscaEmGrafo, Grafo, Node

test_text = []

with open("test.txt", "r") as file:
    test_text = file.readlines()

def parse_graph(text: list[str]):
    grafo: Grafo = []
    nos: List[str] = []

    for line in text:
        l = line.split(",")
        estado = l.pop(0).strip()

        if estado not in nos:
            nos.append(estado)

        parts: List[str] = [p.strip() for p in l]
        if parts:
            grafo.append(parts)
    return grafo, nos

grafo, nos = parse_graph(test_text)

b = BuscaEmGrafo()

inicio = input("INICIO: ").strip().upper()
fim = input("FIM: ").strip().upper()

amp_caminho = b.amplitude(inicio, fim, nos, grafo)
prof_caminho = b.profundidade(inicio, fim, nos, grafo)

print(f"AMPLITUDE: {amp_caminho}")
print(f"PROFUNDIDADE: {prof_caminho}")
