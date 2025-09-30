from collections import deque
import heapq
from Node import Node
from problem_model import ProblemModel
import itertools # Importado para o contador

class SearchAlgorithms:
    """
    Implementa os algoritmos de busca para encontrar o caminho.
    """
    def __init__(self, problem_model: ProblemModel):
        self.problem_model = problem_model

    def _exibir_caminho(self, node):
        """Reconstrói o caminho a partir do nó objetivo."""
        caminho = []
        while node is not None:
            caminho.append(node.estado)
            node = node.pai
        caminho.reverse()
        return caminho

    def _exibir_caminho_bidirecional(self, encontro_estado, visitado1, visitado2):
        """Reconstrói o caminho para a busca bidirecional."""
        caminho1 = self._exibir_caminho(visitado1[encontro_estado])
        caminho2 = self._exibir_caminho(visitado2[encontro_estado])
        return caminho1 + list(reversed(caminho2[:-1]))

    def amplitude(self, inicio, fim):
        """Busca em Amplitude (BFS)."""
        if inicio == fim: return [inicio], 0
        fila = deque([Node(None, inicio, 0)])
        visitado = {inicio}
        while fila:
            atual = fila.popleft()
            if atual.estado == fim:
                return self._exibir_caminho(atual), atual.v1
            for novo_estado, custo_acao, acao in self.problem_model.get_successors(atual.estado):
                if novo_estado not in visitado:
                    visitado.add(novo_estado)
                    fila.append(Node(atual, novo_estado, atual.v1 + custo_acao))
        return None, 0

    def profundidade(self, inicio, fim):
        """Busca em Profundidade (DFS)."""
        if inicio == fim: return [inicio], 0
        pilha = deque([Node(None, inicio, 0)])
        visitado = {inicio}
        while pilha:
            atual = pilha.pop()
            if atual.estado == fim:
                return self._exibir_caminho(atual), atual.v1
            for novo_estado, custo_acao, acao in reversed(self.problem_model.get_successors(atual.estado)):
                if novo_estado not in visitado:
                    visitado.add(novo_estado)
                    pilha.append(Node(atual, novo_estado, atual.v1 + custo_acao))
        return None, 0

    def prof_limitada(self, inicio, fim, limite):
        """Busca em Profundidade Limitada."""
        if inicio == fim: return [inicio], 0
        pilha = deque([Node(None, inicio, 0)])
        visitado = {inicio: 0}
        while pilha:
            atual = pilha.pop()
            if atual.estado == fim:
                return self._exibir_caminho(atual), atual.v1
            if atual.v1 < limite:
                for novo_estado, custo_acao, acao in reversed(self.problem_model.get_successors(atual.estado)):
                    if novo_estado not in visitado or atual.v1 + 1 < visitado[novo_estado]:
                        visitado[novo_estado] = atual.v1 + 1
                        pilha.append(Node(atual, novo_estado, atual.v1 + 1))
        return None, 0

    def aprof_iterativo(self, inicio, fim, limite_max):
        """Busca em Aprofundamento Iterativo."""
        for limite in range(limite_max + 1):
            caminho, custo = self.prof_limitada(inicio, fim, limite)
            if caminho is not None:
                return caminho, custo
        return None, 0

    def bidirecional(self, inicio, fim):
        """Busca Bidirecional."""
        if inicio == fim: return [inicio], 0
        fila1, fila2 = deque([Node(None, inicio, 0)]), deque([Node(None, fim, 0)])
        visitado1, visitado2 = {inicio: fila1[0]}, {fim: fila2[0]}
        while fila1 and fila2:
            # Expansão a partir do início
            atual1 = fila1.popleft()
            for novo_estado, custo_acao, _ in self.problem_model.get_successors(atual1.estado):
                if novo_estado not in visitado1:
                    filho = Node(atual1, novo_estado, atual1.v1 + custo_acao)
                    visitado1[novo_estado] = filho
                    fila1.append(filho)
                    if novo_estado in visitado2:
                        return self._exibir_caminho_bidirecional(novo_estado, visitado1, visitado2), filho.v1 + visitado2[novo_estado].v1
            # Expansão a partir do fim
            atual2 = fila2.popleft()
            for novo_estado, custo_acao, _ in self.problem_model.get_successors(atual2.estado):
                if novo_estado not in visitado2:
                    filho = Node(atual2, novo_estado, atual2.v1 + custo_acao)
                    visitado2[novo_estado] = filho
                    fila2.append(filho)
                    if novo_estado in visitado1:
                        return self._exibir_caminho_bidirecional(novo_estado, visitado1, visitado2), filho.v1 + visitado1[novo_estado].v1
        return None, 0

    def custo_uniforme(self, inicio, fim):
        """Busca de Custo Uniforme (CORRIGIDO)."""
        if inicio == fim: return [inicio], 0
        
        contador = itertools.count() # Cria um contador único
        
        # Fila de prioridade armazena (custo, contador, nó)
        fila_prioridade = [(0, next(contador), Node(None, inicio, 0))]
        # Dicionário para rastrear o menor custo para cada estado
        custos = {inicio: 0}

        while fila_prioridade:
            custo_atual, _, atual = heapq.heappop(fila_prioridade)

            if custo_atual > custos[atual.estado]:
                continue
            
            if atual.estado == fim:
                return self._exibir_caminho(atual), atual.v1

            for novo_estado, custo_acao, acao in self.problem_model.get_successors(atual.estado):
                novo_custo = atual.v1 + custo_acao
                
                if novo_estado not in custos or novo_custo < custos[novo_estado]:
                    custos[novo_estado] = novo_custo
                    heapq.heappush(fila_prioridade, (novo_custo, next(contador), Node(atual, novo_estado, novo_custo)))
        
        return None, 0