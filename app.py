from flask import Flask, render_template, request
from busca import BuscaEmGrafo
from utils import draw_graph, parse_graph

app = Flask(__name__)

with open("test2.txt", "r") as file:
    test_text = file.readlines()

grafo, nos = parse_graph(test_text)
b = BuscaEmGrafo()


@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    img = None
    path = None

    if request.method == "POST":
        inicio = request.form.get("inicio").strip().upper()
        fim = request.form.get("fim").strip().upper()
        lim = request.form.get("lim", type=int)

        algoritmo = request.form.get("algoritmo")

        if algoritmo == "amplitude":
            path = b.amplitude(inicio, fim, nos, grafo)
        elif algoritmo == "profundidade":
            path = b.profundidade(inicio, fim, nos, grafo)
        elif algoritmo == "prof_limitada":
            path = b.prof_limitada(inicio, fim, nos, grafo, lim=lim if lim else 2)
        elif algoritmo == "aprof_iterativo":
            path = b.aprof_iterativo(inicio, fim, nos, grafo, lim_max=lim if lim else 4)
        elif algoritmo == "bidirecional":
            path = b.bidirecional(inicio, fim, nos, grafo)
        else:
            path = []

        result = path

        if result is None:
            result = "Caminho não encontrado."

    img = draw_graph(nos, grafo, path)

    return render_template("index.html", nos=nos, result=result, img=img)


if __name__ == "__main__":
    app.run(debug=True)
