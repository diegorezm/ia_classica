from flask import Flask, render_template, request

from busca import BuscaEmGrafo
from busca_ponderada import BuscaEmGrafoPonderada
from utils import draw_graph, parse_json_graph

app = Flask(__name__)

grafo, nos, custos = parse_json_graph("grafo_13.json")
b = BuscaEmGrafo(nos, grafo, custos)
bp = BuscaEmGrafoPonderada(nos, grafo, custos)


@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    img = None
    path = None
    custo = None

    if request.method == "POST":
        inicio = request.form.get("inicio", default="").strip().upper()
        fim = request.form.get("fim", default="").strip().upper()
        lim = request.form.get("lim", type=int)

        algoritmo = request.form.get("algoritmo")

        if algoritmo == "amplitude":
            path, custo = b.amplitude(inicio, fim)
        elif algoritmo == "profundidade":
            path, custo = b.profundidade(inicio, fim)
        elif algoritmo == "prof_limitada":
            path, custo = b.prof_limitada(inicio, fim, lim=lim if lim else 2)
        elif algoritmo == "aprof_iterativo":
            path, custo = b.aprof_iterativo(inicio, fim, lim_max=lim if lim else 4)
        elif algoritmo == "bidirecional":
            path = b.bidirecional(inicio, fim)
        elif algoritmo == "custo_uniforme":
            path, custo = bp.custo_uniforme(inicio, fim)
        elif algoritmo == "greedy":
            path, custo = bp.greedy(inicio, fim, nos)
        elif algoritmo == "a*":
            path, custo = bp.a_estrela(inicio, fim, nos)
        elif algoritmo == "aia*":
            path, custo = bp.aia_estrela(inicio, fim, nos)
        else:
            path = []

        if path is None:
            result = "Caminho não encontrado."
        else:
            result = " -> ".join(path)

    img = draw_graph(nos, grafo, costs=custos, path=path)

    return render_template("index.html", nos=nos, result=result, img=img, custo=custo)


if __name__ == "__main__":
    app.run(debug=True)
