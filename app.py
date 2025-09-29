from flask import Flask, render_template, request
from busca import BuscaEmGrafo
from utils import draw_graph, parse_json_graph

app = Flask(__name__)

grafo, nos, custos = parse_json_graph("data.json")
b = BuscaEmGrafo()


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
            path = b.amplitude(inicio, fim, nos, grafo)
        elif algoritmo == "profundidade":
            path = b.profundidade(inicio, fim, nos, grafo)
        elif algoritmo == "prof_limitada":
            path = b.prof_limitada(inicio, fim, nos, grafo, lim=lim if lim else 2)
        elif algoritmo == "aprof_iterativo":
            path = b.aprof_iterativo(inicio, fim, nos, grafo, lim_max=lim if lim else 4)
        elif algoritmo == "bidirecional":
            path = b.bidirecional(inicio, fim, nos, grafo)
        elif algoritmo == "custo_uniforme":
            path, custo = b.custo_uniforme(inicio, fim, nos, grafo, custos)
        elif algoritmo == "greedy":
            path = b.greedy(inicio, fim, nos, grafo)
        elif algoritmo == "a*":
            path = b.a_estrela(inicio, fim, nos, grafo, custos)
        elif algoritmo == "aia*":
            path, _ = b.aia_estrela(inicio, fim, nos, grafo, custos)
        else:
            path = []

        result = path

        if result is None:
            result = "Caminho não encontrado."

    img = draw_graph(nos, grafo, costs=custos, path=path)

    return render_template("index.html", nos=nos, result=result, img=img, custo=custo)


if __name__ == "__main__":
    app.run(debug=True)
