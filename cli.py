from utils import parse_graph

from busca import BuscaEmGrafo

test_text = []

with open("test2.txt", "r") as file:
    test_text = file.readlines()


def main():
    # Load graph from file
    with open("test2.txt", "r") as file:
        test_text = file.readlines()

    grafo, nos = parse_graph(test_text)
    b = BuscaEmGrafo()

    print("Nós disponíveis:", ", ".join(nos))

    inicio = input("INICIO: ").strip().upper()
    fim = input("FIM: ").strip().upper()

    print("\n🔎 Resultados:")
    print("-" * 30)

    amp_caminho = b.amplitude(inicio, fim, nos, grafo)
    print(f"AMPLITUDE: {amp_caminho}")

    prof_caminho = b.profundidade(inicio, fim, nos, grafo)
    print(f"PROFUNDIDADE: {prof_caminho}")

    prof_caminho_lim = b.prof_limitada(inicio, fim, nos, grafo, 2)
    print(f"PROF_LIMITADA (lim=2): {prof_caminho_lim}")

    prof_caminho_ai = b.aprof_iterativo(inicio, fim, nos, grafo, 8)
    print(f"APROF_ITERATIVO (lim_max=8): {prof_caminho_ai}")

    bidirecional = b.bidirecional(inicio, fim, nos, grafo)
    print(f"BIDIRECIONAL: {bidirecional}")


if __name__ == "__main__":
    main()
