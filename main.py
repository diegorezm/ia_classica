from typing import List
from busca import BuscaEmGrafo, Grafo

test_text = []

with open("test2.txt", "r") as file:
    test_text = file.readlines()


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


grafo, nos = parse_graph(test_text)

b = BuscaEmGrafo()

print(f"NOS: {nos}")

inicio = input("INICIO: ").strip().upper()
fim = input("FIM: ").strip().upper()

amp_caminho = b.amplitude(inicio, fim, nos, grafo)
prof_caminho = b.profundidade(inicio, fim, nos, grafo)
prof_caminho_lim = b.prof_limitada(inicio, fim, nos, grafo, 2)
prof_caminho_ai = b.aprof_iterativo(inicio, fim, nos, grafo, 8)
bidirecional = b.bidirecional(inicio, fim, nos, grafo)


print(f"AMPLITUDE: {amp_caminho}")
print(f"PROFUNDIDADE: {prof_caminho}")
print(f"PROF_LIM: {prof_caminho_lim}")
print(f"AI: {prof_caminho_ai}")
print(f"BI: {bidirecional}")
