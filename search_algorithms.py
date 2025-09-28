
from collections import deque
import heapq
from Node import Node
from problem_model import ProblemModel

class SearchAlgorithms:
    def __init__(self, problem_model: ProblemModel):
        self.problem_model = problem_model

    def _exibir_caminho(self, node):
        caminho = []
        while node is not None:
            caminho.append(node.estado)
            node = node.pai
        caminho.reverse()
        return caminho

    def _exibir_caminho_bidirecional(self, encontro_estado, visitado1, visitado2):
        node1 = visitado1[encontro_estado]
        node2 = visitado2[encontro_estado]

        caminho1 = self._exibir_caminho(node1)
        caminho2 = self._exibir_caminho(node2)

        # O caminho2 está do objetivo para o ponto de encontro, então precisa ser invertido
        # E o ponto de encontro é duplicado, então removemos um
        caminho2 = list(reversed(caminho2[:-1]))

        return caminho1 + caminho2

    def amplitude(self, inicio, fim):
        if inicio == fim:
            return [inicio], 0

        fila = deque()
        raiz = Node(None, inicio, 0, None, None)
        fila.append(raiz)
        visitado = {inicio: raiz}

        while fila:
            atual = fila.popleft()

            # Sucessores já são ordenados por prioridade no problem_model
            for (novo_estado, custo_acao, acao) in self.problem_model.get_successors(atual.estado):
                if novo_estado not in visitado:
                    filho = Node(atual, novo_estado, atual.v1 + custo_acao, None, None)
                    fila.append(filho)
                    visitado[novo_estado] = filho

                    if novo_estado == fim:
                        return self._exibir_caminho(filho), filho.v1
        return None, 0

    def profundidade(self, inicio, fim):
        if inicio == fim:
            return [inicio], 0

        pilha = deque()
        raiz = Node(None, inicio, 0, None, None)
        pilha.append(raiz)
        visitado = {inicio: raiz}

        while pilha:
            atual = pilha.pop()

            # Se o estado atual já foi visitado por um caminho mais curto, pular
            if atual.estado in visitado and visitado[atual.estado].v1 < atual.v1:
                continue

            # Sucessores já são ordenados por prioridade no problem_model
            # Para DFS, queremos que os 'primeiros' sucessores (maior prioridade) sejam explorados primeiro
            # Como pop() pega o último, precisamos adicionar na ordem inversa da prioridade desejada
            sucessores = self.problem_model.get_successors(atual.estado)
            for (novo_estado, custo_acao, acao) in reversed(sucessores):
                if novo_estado not in visitado or visitado[novo_estado].v1 > atual.v1 + custo_acao:
                    filho = Node(atual, novo_estado, atual.v1 + custo_acao, None, None)
                    pilha.append(filho)
                    visitado[novo_estado] = filho

                    if novo_estado == fim:
                        return self._exibir_caminho(filho), filho.v1
        return None, 0

    def prof_limitada(self, inicio, fim, limite):
        if inicio == fim:
            return [inicio], 0

        pilha = deque()
        raiz = Node(None, inicio, 0, None, None)
        pilha.append(raiz)
        visitado = {inicio: raiz}

        while pilha:
            atual = pilha.pop()

            if atual.v1 > limite:
                continue

            if atual.estado in visitado and visitado[atual.estado].v1 < atual.v1:
                continue

            # Sucessores já são ordenados por prioridade no problem_model
            # Para DFS, queremos que os 'primeiros' sucessores (maior prioridade) sejam explorados primeiro
            # Como pop() pega o último, precisamos adicionar na ordem inversa da prioridade desejada
            sucessores = self.problem_model.get_successors(atual.estado)
            for (novo_estado, custo_acao, acao) in reversed(sucessores):
                if novo_estado not in visitado or visitado[novo_estado].v1 > atual.v1 + custo_acao:
                    filho = Node(atual, novo_estado, atual.v1 + custo_acao, None, None)
                    pilha.append(filho)
                    visitado[novo_estado] = filho

                    if novo_estado == fim:
                        return self._exibir_caminho(filho), filho.v1
        return None, 0

    def aprof_iterativo(self, inicio, fim, limite_max):
        for limite in range(limite_max + 1):
            caminho, custo = self.prof_limitada(inicio, fim, limite)
            if caminho is not None:
                return caminho, custo
        return None, 0

    def bidirecional(self, inicio, fim):
        if inicio == fim:
            return [inicio], 0

        fila1 = deque()
        fila2 = deque()

        raiz1 = Node(None, inicio, 0, None, None)
        raiz2 = Node(None, fim, 0, None, None)

        fila1.append(raiz1)
        fila2.append(raiz2)

        visitado1 = {inicio: raiz1}
        visitado2 = {fim: raiz2}

        while fila1 and fila2:
            # Expansão da busca a partir do início
            atual1 = fila1.popleft()
            for (novo_estado1, custo_acao1, acao1) in self.problem_model.get_successors(atual1.estado):
                if novo_estado1 not in visitado1:
                    filho1 = Node(atual1, novo_estado1, atual1.v1 + custo_acao1, None, None)
                    visitado1[novo_estado1] = filho1
                    fila1.append(filho1)

                    if novo_estado1 in visitado2:
                        return self._exibir_caminho_bidirecional(novo_estado1, visitado1, visitado2), filho1.v1 + visitado2[novo_estado1].v1

            # Expansão da busca a partir do fim
            atual2 = fila2.popleft()
            for (novo_estado2, custo_acao2, acao2) in self.problem_model.get_successors(atual2.estado):
                if novo_estado2 not in visitado2:
                    filho2 = Node(atual2, novo_estado2, atual2.v1 + custo_acao2, None, None)
                    visitado2[novo_estado2] = filho2
                    fila2.append(filho2)

                    if novo_estado2 in visitado1:
                        return self._exibir_caminho_bidirecional(novo_estado2, visitado1, visitado2), filho2.v1 + visitado1[novo_estado2].v1

        return None, 0

    def custo_uniforme(self, inicio, fim):
        if inicio == fim:
            return [inicio], 0

        # Fila de prioridade (min-heap) para armazenar nós (custo_total, nó)
        fila_prioridade = []
        heapq.heappush(fila_prioridade, (0, Node(None, inicio, 0, None, None)))

        # Dicionário para armazenar o nó com o menor custo encontrado para cada estado
        custos_visitados = {inicio: 0}
        nos_visitados = {inicio: Node(None, inicio, 0, None, None)}

        while fila_prioridade:
            custo_atual, atual = heapq.heappop(fila_prioridade)

            if atual.estado == fim:
                return self._exibir_caminho(atual), atual.v1

            # Se já encontramos um caminho mais barato para este estado, ignorar
            if custo_atual > custos_visitados.get(atual.estado, float("inf")):
                continue

            for (novo_estado, custo_acao, acao) in self.problem_model.get_successors(atual.estado):
                novo_custo = atual.v1 + custo_acao

                if novo_estado not in custos_visitados or novo_custo < custos_visitados[novo_estado]:
                    custos_visitados[novo_estado] = novo_custo
                    filho = Node(atual, novo_estado, novo_custo, None, None)
                    nos_visitados[novo_estado] = filho
                    heapq.heappush(fila_prioridade, (novo_custo, filho))

        return None, 0

