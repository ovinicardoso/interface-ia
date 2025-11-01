from collections import deque
import heapq
from Node import Node
from problem_model import ProblemModel
import itertools

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
        """Busca em Amplitude."""
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
        """Busca em Profundidade."""
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
        """Busca de Custo Uniforme."""
        if inicio == fim: return [inicio], 0
        
        contador = itertools.count() 
        fila_prioridade = [(0, next(contador), Node(None, inicio, 0))]
        custos = {inicio: 0}

        while fila_prioridade:
            custo_atual, _, atual = heapq.heappop(fila_prioridade)

            if custo_atual > custos[atual.estado]:
                continue
            
            if atual.estado == fim:
                return self._exibir_caminho(atual), atual.v1

            for novo_estado, custo_acao, acao in self.problem_model.get_successors(atual.estado):
                novo_custo_g = atual.v1 + custo_acao
                
                if novo_estado not in custos or novo_custo_g < custos[novo_estado]:
                    custos[novo_estado] = novo_custo_g
                    heapq.heappush(fila_prioridade, (novo_custo_g, next(contador), Node(atual, novo_estado, novo_custo_g)))
        
        return None, 0

    def greedy(self, inicio, fim):
        """Busca Gulosa (Greedy Best-First Search)."""
        if inicio == fim: return [inicio], 0
        
        contador = itertools.count()
        heuristica_inicial = self.problem_model.heuristic(inicio, fim)
        fila_prioridade = [(heuristica_inicial, next(contador), Node(None, inicio, 0))]
        
        visitado = {inicio} 

        while fila_prioridade:
            _, _, atual = heapq.heappop(fila_prioridade)

            if atual.estado == fim:
                return self._exibir_caminho(atual), atual.v1

            for novo_estado, custo_acao, acao in self.problem_model.get_successors(atual.estado):
                if novo_estado not in visitado:
                    visitado.add(novo_estado)
                    novo_custo_g = atual.v1 + custo_acao
                    heuristica_filho = self.problem_model.heuristic(novo_estado, fim)
                    
                    novo_no = Node(atual, novo_estado, novo_custo_g)
                    heapq.heappush(fila_prioridade, (heuristica_filho, next(contador), novo_no))
        
        return None, 0

    def a_estrela(self, inicio, fim):
        """Busca A* (A-Estrela)."""
        if inicio == fim: return [inicio], 0
        
        contador = itertools.count()
        
        heuristica_inicial = self.problem_model.heuristic(inicio, fim)
        g_inicial = 0
        f_inicial = g_inicial + heuristica_inicial
        
        fila_prioridade = [(f_inicial, next(contador), Node(None, inicio, g_inicial))]
        
        custos_g = {inicio: g_inicial}

        while fila_prioridade:
            f_atual, _, atual = heapq.heappop(fila_prioridade)

            if atual.v1 > custos_g[atual.estado]:
                continue
            
            if atual.estado == fim:
                return self._exibir_caminho(atual), atual.v1

            for novo_estado, custo_acao, acao in self.problem_model.get_successors(atual.estado):
                novo_custo_g = atual.v1 + custo_acao
                
                if novo_estado not in custos_g or novo_custo_g < custos_g[novo_estado]:
                    custos_g[novo_estado] = novo_custo_g
                    heuristica_filho = self.problem_model.heuristic(novo_estado, fim)
                    novo_custo_f = novo_custo_g + heuristica_filho
                    
                    heapq.heappush(fila_prioridade, (novo_custo_f, next(contador), Node(atual, novo_estado, novo_custo_g)))
        
        return None, 0

    def aia_estrela(self, inicio, fim):
        """Busca A* por Aprofundamento Iterativo (AIA* / IDA*)."""
        
        def busca_dfs_limitada(no_atual, custo_g, limite_f):
            """Função auxiliar recursiva (DFS) limitada pelo f(n)."""
            
            estado_atual = no_atual.estado
            heuristica_atual = self.problem_model.heuristic(estado_atual, fim)
            f_atual = custo_g + heuristica_atual
            
            if f_atual > limite_f:
                return None, f_atual 

            if estado_atual == fim:
                return self._exibir_caminho(no_atual), custo_g

            proximo_limite_min = float('inf')

            for novo_estado, custo_acao, acao in self.problem_model.get_successors(estado_atual):
                # Evitar loops (voltar para o pai imediato)
                if no_atual.pai and no_atual.pai.estado == novo_estado:
                     continue

                novo_custo_g = custo_g + custo_acao
                novo_no = Node(no_atual, novo_estado, novo_custo_g)
                
                # Chamada recursiva
                caminho_encontrado, f_filho_ou_custo_final = busca_dfs_limitada(novo_no, novo_custo_g, limite_f)
                
                if caminho_encontrado:
                    # Propaga o caminho e o custo final (f_filho_ou_custo_final) para cima.
                    return caminho_encontrado, f_filho_ou_custo_final 
                
                # Armazena o menor f(n) que ultrapassou o limite atual
                proximo_limite_min = min(proximo_limite_min, f_filho_ou_custo_final)
                
            return None, proximo_limite_min

        # --- Loop principal do AIA* ---
        limite_f_atual = self.problem_model.heuristic(inicio, fim)
        no_inicial = Node(None, inicio, 0)
        
        while True:
            # Executa a busca limitada
            caminho, custo_ou_proximo_limite = busca_dfs_limitada(no_inicial, 0, limite_f_atual)
            
            if caminho:
                return caminho, custo_ou_proximo_limite
            
            if custo_ou_proximo_limite == float('inf'):
                return None, 0 # Falha
                
            limite_f_atual = custo_ou_proximo_limite