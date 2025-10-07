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
        path, c = self.__busca(inicio, fim, amplitude=True)
        return path, c

    def prof_limitada(self, inicio, fim, lim: int):
        path, c = self.__busca(inicio, fim, amplitude=True, lim=lim)
        return path, c

    def aprof_iterativo(self, inicio, fim, lim_max: int):
        for lim in range(1, lim_max):
            path, c = self.__busca(inicio, fim, amplitude=True, lim=lim)
            if path is not None:
                return path, c
        return None, None

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
            return [inicio], 0

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
