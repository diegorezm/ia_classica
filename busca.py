import heapq
from collections import deque
from typing import Dict, Optional, List, Any, Tuple


class Node:
    def __init__(
        self,
        pai: "Node | None" = None,
        estado: Optional[Any] = None,
        profundidade: Optional[int] = None,
    ):
        self.pai = pai
        self.estado = estado
        self.profundidade = profundidade

    def __str__(self) -> str:
        estado = str(self.estado) if self.estado is not None else "Nó"
        pai = (
            str(self.pai.estado)
            if self.pai is not None and self.pai.estado is not None
            else "Pai"
        )
        profundidade = str(self.profundidade) if self.profundidade is not None else 0
        return (
            "{"
            + f"'estado': '{estado}', 'pai': '{pai}', 'profundidade': {profundidade}"
            + "}"
        )

    def __repr__(self) -> str:
        return self.__str__()


Grafo = List[List[Any]]
Busca = Optional[List[Optional[Node]]]
# ex. {(A,B): 4} ou conexão entre A e B tem custo 4
Custo = Dict[Tuple[str, str], int]


class BuscaEmGrafo:
    def profundidade(self, inicio, fim, nos: List[Any], grafo: Grafo):
        return self.__busca(inicio, fim, nos, grafo, amplitude=False)

    def amplitude(self, inicio, fim, nos: List[Any], grafo: Grafo):
        return self.__busca(inicio, fim, nos, grafo, amplitude=True)

    def prof_limitada(self, inicio, fim, nos: List[Any], grafo: Grafo, lim: int):
        return self.__busca(inicio, fim, nos, grafo, amplitude=True, lim=lim)

    def aprof_iterativo(self, inicio, fim, nos: List[Any], grafo: Grafo, lim_max: int):
        for lim in range(1, lim_max):
            res = self.__busca(inicio, fim, nos, grafo, amplitude=True, lim=lim)
            if res is not None:
                return res
        return None

    def bidirecional(self, inicio, fim, nos: List[Any], grafo: Grafo):
        if inicio == fim:
            return [inicio]

        # Lista para árvore de busca a partir da origem - FILA
        fila1 = deque()

        # Lista para árvore de busca a partir do destino - FILA
        fila2 = deque()

        # Inclui início e fim como nó raíz da árvore de busca
        raiz = Node(None, inicio, 0)
        fila1.append(raiz)

        raiz = Node(None, fim, 0)
        fila2.append(raiz)

        # Visitados mapeando estado -> Node (para reconstruir o caminho)
        visitado1 = {inicio: fila1[0]}
        visitado2 = {fim: fila2[0]}

        nivel = 0

        while fila1 and fila2:
            # ****** Executa AMPLITUDE a partir da ORIGEM *******
            # Quantidade de nós no nível atual
            nivel = len(fila1)
            for _ in range(nivel):
                # Remove o primeiro da FILA
                atual = fila1.popleft()

                # Gera sucessores
                ind = nos.index(atual.estado)
                filhos = self.__sucessores(ind, grafo, 1)

                # Gera sucessores a partir do grid
                # filhos = self.sucessores_grid(atual.estado,nx,ny,mapa) # grid

                for novo in filhos:
                    # t_novo = tuple(novo)       # grid
                    # if t_novo not in visitado1: # grid
                    if novo not in visitado1:
                        filho = Node(atual, novo, atual.profundidade + 1)
                        visitado1[novo] = filho

                        # Encontrou encontro com a outra AMPLITUDE
                        if novo in visitado2:
                            return self.exibirCaminho1(novo, visitado1, visitado2)

                        # Insere na FILA
                        fila1.append(filho)

            # ****** Executa AMPLITUDE a partir do OBJETIVO *******
            # Quantidade de nós no nível atual
            nivel = len(fila2)
            for _ in range(nivel):
                # Remove o primeiro da FILA
                atual = fila2.popleft()

                # Gera sucessores
                ind = nos.index(atual.estado)
                filhos = self.__sucessores(ind, grafo, 1)

                for novo in filhos:
                    if novo not in visitado2:
                        filho = Node(atual, novo, atual.profundidade + 1)
                        visitado2[novo] = filho

                        # Encontrou encontro com a outra AMPLITUDE
                        if novo in visitado1:
                            return self.exibirCaminho1(novo, visitado1, visitado2)
                        fila2.append(filho)
        return None

    def custo_uniforme(self, inicio, fim, nos: List[Any], grafo: Grafo, custos: Custo):
        # custo, atual
        fila = [(0, inicio)]
        heapq.heapify(fila)

        custos_no = {inicio: 0}
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

            ind = nos.index(atual)

            filhos = self.__sucessores(ind, grafo, 1)
            for vizinho in filhos:
                if vizinho not in visitados:
                    custo_aresta = custos[(atual, vizinho)]
                    novo_custo = custo_atual + custo_aresta
                    if vizinho not in custos_no or novo_custo < custos_no[vizinho]:
                        custos[vizinho] = novo_custo
                        pais[vizinho] = atual
                        heapq.heappush(fila, (novo_custo, vizinho))
        return None, None

    def greedy(self, inicio, fim, nos: List[Any], grafo: Grafo, custos: Custo):
        aberto = [(self.heuristica(inicio, fim, custos), inicio)]
        heapq.heapify(aberto)

        pais: Dict[str, Optional[str]] = {inicio: None}
        visitados = set()

        while aberto:
            _, atual = heapq.heappop(aberto)

            if atual in visitados:
                continue

            if atual == fim:
                return self.__reconstruir_caminho(pais, fim)

            visitados.add(atual)
            ind = nos.index(atual)
            for vizinho in grafo[ind]:
                if vizinho not in visitados:
                    pais[vizinho] = atual
                    heapq.heappush(
                        aberto, (self.heuristica(vizinho, fim, custos), vizinho)
                    )
        return None

    def a_estrela(self, inicio, fim, nos: List[Any], grafo: Grafo, custos: Custo):
        abertos = [(self.heuristica(inicio, fim, custos), 0, inicio)]
        heapq.heapify(abertos)

        pais: Dict[str, Optional[str]] = {inicio: None}
        custos_no = {inicio: 0}
        visitados = set()

        while abertos:
            _, g_atual, atual = heapq.heappop(abertos)

            if atual in visitados:
                continue

            visitados.add(atual)

            if atual == fim:
                return self.__reconstruir_caminho(pais, fim), g_atual

            ind = nos.index(atual)

            for vizinho in grafo[ind]:
                custo_aresta = custos[(atual, vizinho)]
                g_novo = g_atual + custo_aresta
                f_novo = g_novo + self.heuristica(vizinho, fim, custos)
                if vizinho not in custos_no or g_novo < custos_no[vizinho]:
                    custos_no[vizinho] = g_novo
                    pais[vizinho] = atual
                    heapq.heappush(abertos, (f_novo, g_novo, vizinho))

        return None, float("inf")

    def ida_star(self, inicio, fim, nos: List[Any], grafo: Grafo, custos: Custo):
        limite = self.heuristica(inicio, fim, custos)

        def dfs(atual, g_atual, limite, pais, visitados):
            f_atual = g_atual + self.heuristica(atual, fim, custos)
            if f_atual > limite:
                return f_atual
            if atual == fim:
                return True
            visitados.add(atual)
            min_excedido = float("inf")
            ind = nos.index(atual)
            for vizinho in grafo[ind]:
                if vizinho not in visitados:
                    pais[vizinho] = atual
                    custo_aresta = custos[(atual, vizinho)]
                    res = dfs(vizinho, g_atual + custo_aresta, limite, pais, visitados)
                    if res is True:
                        return True
                    if res < min_excedido:
                        min_excedido = res
            visitados.remove(atual)
            return min_excedido

        while True:
            pais: Dict[str, Optional[str]] = {inicio: None}
            visitados = set()
            res = dfs(inicio, 0, limite, pais, visitados)
            if res is True:
                return self.__reconstruir_caminho(pais, fim)
            if res == float("inf"):
                return None
            limite = res

    """
    Método privado que faz a busca pela árvore.
    """

    def __busca(
        self,
        inicio: Any,
        fim: Any,
        nos: List[Any],
        grafo: Grafo,
        amplitude=True,
        lim: Optional[int] = None,
    ) -> Busca:
        if inicio == fim:
            return [inicio]

        fila: deque[Node] = deque()

        # Inclui início como nó raíz da árvore de busca
        raiz = Node(None, inicio, 0)  # grafo
        fila.append(raiz)

        # Dicionário com os nós que já foram visitados
        visitados = {inicio: raiz}

        while fila:
            # Remove algum item da fila dependendo do tipo de busca.
            atual = fila.popleft() if amplitude else fila.pop()
            if lim is None or (
                atual.profundidade is not None and atual.profundidade < lim
            ):
                if atual.estado is not None:
                    # Gera sucessores a partir do grafo
                    ind = nos.index(atual.estado)  # grafo

                    # Todos os filhos do nó atual
                    filhos = self.__sucessores(ind, grafo, 1)

                    for novo in filhos:
                        if novo not in visitados:
                            p = (
                                atual.profundidade
                                if atual.profundidade is not None
                                else 0
                            )
                            filho = Node(atual, novo, p + 1)
                            fila.append(filho)
                            visitados[novo] = filho
                            if novo == fim:
                                return self.exibirCaminho(filho)
        return None

    # Considerando que os custos entre cada nó é a mesma coisa que a distancia entre eles, esta função
    # retorna o custo total de ir de um nó para outro
    def heuristica(self, inicio, fim, custos: Custo):
        fila = deque()
        fila.append((inicio, 0))

        visitados = set()

        while fila:
            atual, custo_acc = fila.popleft()
            if atual == fim:
                return custo_acc
            for (n1, n2), custo in custos.items():
                if n1 == atual and n2 not in visitados:
                    fila.append((n2, custo_acc + custo))
                elif n2 == atual and n1 not in visitados:
                    fila.append((n1, custo_acc + custo))

            visitados.add(atual)

        return float("inf")

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

    """
    Retorna todos os nós que estão conectados ao nó atual.
    """

    def exibirCaminho(self, no: Optional[Node]):
        caminho = []

        while no is not None:
            caminho.append(no.estado)
            no = no.pai

        caminho.reverse()
        return caminho

    def exibirCaminho1(self, encontro, visitado1, visitado2):
        # nó do lado do início
        encontro1 = visitado1[encontro]
        # nó do lado do objetivo
        encontro2 = visitado2[encontro]

        caminho1 = self.exibirCaminho(encontro1)
        caminho2 = self.exibirCaminho(encontro2)

        # Inverte o caminho
        caminho2 = list(reversed(caminho2[:-1]))

        return caminho1 + caminho2

    def __sucessores(self, ind: int, grafo: Grafo, ordem: int):
        f = []
        for suc in grafo[ind][::ordem]:
            f.append(suc)
        return f
