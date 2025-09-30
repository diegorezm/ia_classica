from flask import Flask, render_template, request
from busca import BuscaEmGrafo
from utils import draw_graph, parse_json_graph

app = Flask(__name__)

grafo, nos, custos = parse_json_graph("data.json")
b = BuscaEmGrafo(nos, grafo, custos)


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
            path, c = b.amplitude(inicio, fim)
            custo = c
        elif algoritmo == "profundidade":
            path, c = b.profundidade(inicio, fim)
            custo = c
        elif algoritmo == "prof_limitada":
            path, c = b.prof_limitada(inicio, fim, lim=lim if lim else 2)
            custo = c
        elif algoritmo == "aprof_iterativo":
            path = b.aprof_iterativo(inicio, fim, lim_max=lim if lim else 4)
        elif algoritmo == "bidirecional":
            path = b.bidirecional(inicio, fim)
        elif algoritmo == "custo_uniforme":
            path, c = b.custo_uniforme(inicio, fim)
            custo = c
        elif algoritmo == "greedy":
            path, c = b.greedy(inicio, fim, nos)
            custo = c
        elif algoritmo == "a*":
            path, c = b.a_estrela(inicio, fim, nos)
            custo = c
        elif algoritmo == "aia*":
            path, c = b.aia_estrela(inicio, fim, nos)
            custo = c
        else:
            path = []

        result = path

        if result is None:
            result = "Caminho não encontrado."

    img = draw_graph(nos, grafo, costs=custos, path=path)

    return render_template("index.html", nos=nos, result=result, img=img, custo=custo)


if __name__ == "__main__":
    app.run(debug=True)
