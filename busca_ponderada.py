import heapq
from typing import Dict, Optional, List, Any
from busca import Custo, Grafo


class BuscaEmGrafoPonderada:
    def __init__(self, nos: List[Any], grafo: Grafo, custos: Optional[Custo] = None):
        self.nos = nos
        self.grafo = grafo
        self.custos = custos if custos is not None else {}
        self.h = self.__gerar_heuristica()
        self.h = self.__gerar_heuristica()

    def custo_uniforme(self, inicio, fim):
        if inicio == fim:
            return [inicio], 0
        # custo, atual
        fila = [(0, inicio)]
        heapq.heapify(fila)

        custos_no = {inicio: 0}
        ## Guardando os pais para poder reconstruir o caminho
        pais: Dict[str, Optional[str]] = {inicio: None}
        visitados = set()

        while fila:
            custo_atual, atual = heapq.heappop(fila)

            if atual in visitados:
                continue

            visitados.add(atual)

            if atual == fim:
                caminho = self.__reconstruir_caminho(pais, fim)
                return caminho, custo_atual

            ind = self.nos.index(atual)

            filhos = self.__sucessores(ind, self.grafo, 1)
            for vizinho in filhos:
                if vizinho not in visitados:
                    custo_aresta = self.custos.get((atual, vizinho), 0)
                    novo_custo = custo_atual + custo_aresta
                    if vizinho not in custos_no or novo_custo < custos_no[vizinho]:
                        # self.custos[vizinho] = novo_custo
                        pais[vizinho] = atual
                        heapq.heappush(fila, (novo_custo, vizinho))
        return None, None

    def greedy(self, inicio, fim, nos: List[Any]):
        if inicio == fim:
            return [inicio], 0

        aberto = [(self.__heuristica(inicio, fim), inicio)]
        heapq.heapify(aberto)

        custos_no = {inicio: 0}

        # Cria um dicionario de pais, este dicionario será utilizado para
        # reconstruir o caminho até o destino. (Já que neste caso não é possivel utilizar a classe Node, devido ao uso do heapq)
        pais: Dict[str, Optional[str]] = {inicio: None}

        # Criando um set de nós visitados
        visitados = set()

        while aberto:
            _, atual = heapq.heappop(aberto)

            if atual in visitados:
                continue

            visitados.add(atual)

            if atual == fim:
                return self.__reconstruir_caminho(pais, fim), custos_no[fim]

            ind = nos.index(atual)

            for vizinho in self.grafo[ind]:
                if vizinho not in visitados:
                    custo_aresta = self.custos.get((atual, vizinho), 0)
                    novo_custo = custos_no[atual] + custo_aresta
                    custos_no[vizinho] = novo_custo
                    pais[vizinho] = atual
                    h_novo = self.__heuristica(fim, vizinho)
                    heapq.heappush(aberto, (h_novo, vizinho))
        return None, None

    def a_estrela(self, inicio, fim, nos: List[Any]):
        # fila de prioridade, começa com o nó inicial (custo 0)
        abertos = [(0, inicio)]
        heapq.heapify(abertos)

        pais: Dict[str, Optional[str]] = {inicio: None}
        # Custo acumulado
        custos_no = {inicio: 0}
        visitados = set()

        while abertos:
            _, atual = heapq.heappop(abertos)

            if atual in visitados:
                continue

            visitados.add(atual)

            if atual == fim:
                return self.__reconstruir_caminho(pais, fim), custos_no[fim]

            ind = nos.index(atual)
            vizinhos = self.__sucessores(ind, self.grafo, 1)

            for vizinho in vizinhos:
                custo_aresta = (
                    self.custos[(atual, vizinho)]
                    if (atual, vizinho) in self.custos
                    else self.custos[(vizinho, atual)]
                )
                g_novo = custos_no[atual] + custo_aresta
                # Se for a primeira vez que a gente vê esse vizinho
                # ou se achamos um caminho mais barato até ele, atualiza
                if vizinho not in custos_no or g_novo < custos_no.get(
                    vizinho, float("inf")
                ):
                    custos_no[vizinho] = g_novo
                    pais[vizinho] = atual
                    ## TODO: Heuristica
                    f_novo = g_novo + self.__heuristica(fim, vizinho)
                    heapq.heappush(abertos, (f_novo, vizinho))
        return None, None

    def aia_estrela(self, inicio, fim, nos: List[Any]):
        # fila de prioridade, começa com o nó inicial (custo 0)
        abertos = [(0, inicio)]
        heapq.heapify(abertos)

        pais: Dict[str, Optional[str]] = {inicio: None}
        custos_no = {inicio: 0}

        # Melhor solução/custo até agora
        melhor_solucao = None
        melhor_custo = float("inf")

        while abertos:
            f_atual, atual = heapq.heappop(abertos)

            if atual == fim:
                caminho = self.__reconstruir_caminho(pais, fim)
                if f_atual < melhor_custo:
                    melhor_custo = f_atual
                    melhor_solucao = caminho
                    return melhor_solucao, melhor_custo

            ind = nos.index(atual)
            vizinhos = self.__sucessores(ind, self.grafo, 1)
            for vizinho in vizinhos:
                custo_aresta = self.custos.get(
                    (atual, vizinho),
                    self.custos.get((vizinho, atual), 1),
                )

                g_novo = custos_no[atual] + custo_aresta
                f_novo = g_novo + self.__heuristica(fim, vizinho)

                if vizinho not in custos_no or g_novo < custos_no[vizinho]:
                    custos_no[vizinho] = g_novo
                    pais[vizinho] = atual
                    heapq.heappush(abertos, (f_novo, vizinho))
        return melhor_solucao, melhor_custo

    # Reconstruindo o caminho percorrido através de um
    # dicionário
    def __reconstruir_caminho(
        self, pais: Dict[str, Optional[str]], destino: str
    ) -> List[str]:
        caminho = []
        atual = destino
        while atual is not None:
            caminho.append(atual)
            atual = pais.get(atual)
        caminho.reverse()
        return caminho

    def __heuristica(self, inicio, destino):
        i_dest = self.nos.index(destino)
        i_inicio = self.nos.index(inicio)
        return self.h[i_dest][i_inicio]

    # A ideia desta função é gerar a matriz
    # de heuristica utilizando o dijkstra
    def __gerar_heuristica(self):
        matriz = []
        for destino in self.nos:
            dist = self.dijkstra(destino)
            linha = [dist[n] for n in self.nos]
            matriz.append(linha)
        return matriz

    def dijkstra(self, inicio: Any):
        dist = {n: float("inf") for n in self.nos}
        dist[inicio] = 0

        pq = [(0, inicio)]
        heapq.heapify(pq)

        while pq:
            custo_atual, atual = heapq.heappop(pq)
            ind = self.nos.index(atual)
            vizinhos = self.__sucessores(ind, self.grafo, 1)
            for vizinho in vizinhos:
                custo_aresta = self.custos.get(
                    (atual, vizinho),
                    self.custos.get((vizinho, atual), 1),
                )

                novo_custo = custo_atual + custo_aresta
                if novo_custo < dist[vizinho]:
                    dist[vizinho] = novo_custo
                    heapq.heappush(pq, (novo_custo, vizinho))
        return dist

    def __sucessores(self, ind: int, grafo: Grafo, ordem: int):
        f = []
        for suc in grafo[ind][::ordem]:
            f.append(suc)
        return f
