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
    def __init__(self, nos: List[Any], grafo: Grafo, custos: Optional[Custo] = None):
        self.nos = nos
        self.grafo = grafo
        self.custos = custos if custos is not None else {}

    def profundidade(self, inicio, fim):
        return self.__busca(inicio, fim, amplitude=False)

    def amplitude(
        self,
        inicio,
        fim,
    ):
        return self.__busca(inicio, fim, amplitude=True)

    def prof_limitada(self, inicio, fim, lim: int):
        return self.__busca(inicio, fim, amplitude=True, lim=lim)

    def aprof_iterativo(self, inicio, fim, lim_max: int):
        for lim in range(1, lim_max):
            res = self.__busca(inicio, fim, amplitude=True, lim=lim)
            if res is not None:
                return res
        return None

    def bidirecional(self, inicio, fim):
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
                ind = self.nos.index(atual.estado)
                filhos = self.__sucessores(ind, self.grafo, 1)

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
                ind = self.nos.index(atual.estado)
                filhos = self.__sucessores(ind, self.grafo, 1)

                for novo in filhos:
                    if novo not in visitado2:
                        filho = Node(atual, novo, atual.profundidade + 1)
                        visitado2[novo] = filho

                        # Encontrou encontro com a outra AMPLITUDE
                        if novo in visitado1:
                            return self.exibirCaminho1(novo, visitado1, visitado2)
                        fila2.append(filho)
        return None

    def custo_uniforme(self, inicio, fim):
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
        ## TODO: Heuristica
        aberto = [(self.__heuristica(), inicio)]
        heapq.heapify(aberto)

        custos_no = {inicio: 0}

        # Cria um dicionario de pais, este dicionario será utilizado para
        # reconstruir o caminho até o destino. (Já que neste caso não é possivel utilizar a classe Node, devido ao uso do heapq)
        pais: Dict[str, Optional[str]] = {inicio: None}

        # Criando um set de nós visitados
        visitados = set()

        while aberto:
            ## TODO: Heuristica
            _, atual = heapq.heappop(aberto)

            if atual in visitados:
                continue

            if atual == fim:
                return self.__reconstruir_caminho(pais, fim), custos_no[fim]

            visitados.add(atual)
            ind = nos.index(atual)

            for vizinho in self.grafo[ind]:
                if vizinho not in visitados:
                    custo_aresta = self.custos.get((atual, vizinho), 0)
                    novo_custo = custos_no[atual] + custo_aresta
                    custos_no[vizinho] = novo_custo
                    pais[vizinho] = atual
                    heapq.heappush(aberto, (self.__heuristica(), vizinho))
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

            for vizinho in self.grafo[ind]:
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
                    f_novo = g_novo + self.__heuristica()
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

            for vizinho in self.grafo[ind]:
                custo_aresta = self.custo_aresta(atual, vizinho)
                g_novo = custos_no[atual] + custo_aresta
                f_novo = g_novo + self.__heuristica()

                if vizinho not in custos_no or g_novo < custos_no[vizinho]:
                    custos_no[vizinho] = g_novo
                    pais[vizinho] = atual
                    heapq.heappush(abertos, (f_novo, vizinho))
        return melhor_solucao, melhor_custo

    """
    Método privado que faz a busca pela árvore.
    """

    def __busca(
        self,
        inicio: Any,
        fim: Any,
        amplitude=True,
        lim: Optional[int] = None,
    ):
        if inicio == fim:
            return [inicio]

        fila: deque[Node] = deque()
        custos_no = {inicio: 0}

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
                    ind = self.nos.index(atual.estado)  # grafo

                    # Todos os filhos do nó atual
                    filhos = self.__sucessores(ind, self.grafo, 1)

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

                            custo_aresta = self.custos.get((atual.estado, novo), 0)
                            custos_no[novo] = custos_no[atual.estado] + custo_aresta

                            if novo == fim:
                                caminho = self.exibirCaminho(filho)
                                return caminho, custos_no[novo]
        return None, None

    def __heuristica(self):
        return 0

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

    def custo_aresta(self, a1, a2):
        return (
            self.custos[(a1, a2)] if (a1, a2) in self.custos else self.custos[(a2, a1)]
        )

    def __sucessores(self, ind: int, grafo: Grafo, ordem: int):
        f = []
        for suc in grafo[ind][::ordem]:
            f.append(suc)
        return f
