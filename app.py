from flask import Flask, render_template, request
from typing import List
from busca import BuscaEmGrafo, Grafo

app = Flask(__name__)


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


with open("test2.txt", "r") as file:
    test_text = file.readlines()

grafo, nos = parse_graph(test_text)
b = BuscaEmGrafo()


@app.route("/", methods=["GET", "POST"])
def index():
    result = None

    if request.method == "POST":
        inicio = request.form.get("inicio").strip().upper()
        fim = request.form.get("fim").strip().upper()

        algoritmo = request.form.get("algoritmo")

        if algoritmo == "amplitude":
            result = b.amplitude(inicio, fim, nos, grafo)
        elif algoritmo == "profundidade":
            result = b.profundidade(inicio, fim, nos, grafo)
        elif algoritmo == "prof_limitada":
            result = b.prof_limitada(inicio, fim, nos, grafo, 2)
        elif algoritmo == "aprof_iterativo":
            result = b.aprof_iterativo(inicio, fim, nos, grafo, 8)
        elif algoritmo == "bidirecional":
            result = b.bidirecional(inicio, fim, nos, grafo)
        else:
            result = "Algoritmo não reconhecido."

        print(result)

    return render_template("index.html", nos=nos, result=result)


if __name__ == "__main__":
    app.run(debug=True)
