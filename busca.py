from collections import deque
from typing import Optional, List, Any

class Node:
    def __init__(self, pai: "Node | None" = None, estado: Optional[Any] = None, profundidade: Optional[int] = None):
        self.pai = pai
        self.estado = estado
        self.profundidade = profundidade

    def __str__(self) -> str:
        estado =  str(self.estado) if self.estado is not None else "Nó"
        pai = str(self.pai.estado) if self.pai is not None and self.pai.estado is not None else "Pai"
        profundidade = str(self.profundidade) if self.profundidade is not None else 0
        return "{" + f"'estado': '{estado}', 'pai': '{pai}', 'profundidade': {profundidade}" + "}"

    def __repr__(self) -> str:
        return self.__str__()

Grafo = List[List[Any]]
Busca = Optional[List[Optional[Node]]]

class BuscaEmGrafo:
    def profundidade(self, inicio: Any, fim: Any, nos: List[Any], grafo: Grafo):
        return self.__busca(inicio,fim,nos,grafo, amplitude=False)


    def amplitude(self, inicio: Any, fim: Any, nos: List[Any], grafo: Grafo):
        return self.__busca(inicio,fim,nos,grafo, amplitude=True)


    """
    Método privado que faz a busca pela árvore.
    """
    def __busca(self, inicio: Any, fim: Any, nos: List[Any], grafo: Grafo, amplitude=True) -> Busca:
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

            if atual.estado is not None:
                # Gera sucessores a partir do grafo
                ind = nos.index(atual.estado)  # grafo

                # Todos os filhos do nó atual
                filhos = self.__sucessores(ind, grafo, 1)

                for novo in filhos:
                    if novo not in visitados:
                        p = atual.profundidade if atual.profundidade is not None else 0
                        filho = Node(atual,novo,p + 1)
                        fila.append(filho)
                        visitados[novo] = filho
                        if novo == fim:
                            return self.exibirCaminho(filho)
        return None


    """
    Retorna todos os nós que estão conectados ao nó atual.
    """
    def __sucessores(self, ind: int, grafo: Grafo, ordem: int):
        f = []
        for suc in grafo[ind][::ordem]:
            f.append(suc)
        return f

    def exibirCaminho(self, no: Optional[Node]):
        caminho = []

        while no is not None:
            caminho.append(no.estado)
            no = no.pai

        caminho.reverse()
        return caminho
