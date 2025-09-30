import math
import random

class ProblemModel:
    """
    Modela o problema do veículo autônomo na fábrica.

    Atributos:
        grid_width (int): A largura do grid que representa a fábrica.
        grid_height (int): A altura do grid.
        obstacles (set): Um conjunto de tuplas (x, y) representando os obstáculos.
        orientations (list): As possíveis orientações do veículo.
        expansion_priority (dict): Um dicionário que define a prioridade de expansão dos sucessores.
    """
    def __init__(self):
        self.obstacles, self.grid_width, self.grid_height = self._create_static_grid()
        self.orientations = ["Norte", "Leste", "Sul", "Oeste"]
        # Prioridade de expansão padrão para as orientações
        self.expansion_priority = {orientation: i for i, orientation in enumerate(self.orientations)}

    def _create_static_grid(self):
        """
        Cria um grid estático de 15x15 para o mapa da fábrica.
        '9' representa um obstáculo.
        """
        grid = [
            [0,0,0,9,9,0,0,0,9,0,0,0,0,9,0],
            [0,9,0,0,0,0,9,0,0,9,0,0,0,0,0],
            [0,0,0,9,0,0,9,9,0,0,0,9,0,0,9],
            [9,0,9,0,0,9,0,0,0,9,0,0,9,0,0],
            [0,0,0,0,9,0,0,9,0,0,9,0,0,9,0],
            [0,9,9,0,0,0,0,9,0,0,0,0,0,0,0],
            [0,0,0,0,9,9,0,0,0,9,9,0,9,0,0],
            [9,0,9,0,0,0,0,9,0,0,0,0,0,0,9],
            [0,0,0,0,9,0,0,9,0,0,9,0,0,0,0],
            [0,9,0,0,0,0,9,0,0,0,0,9,0,0,0],
            [0,0,9,0,9,0,0,0,9,9,0,0,0,9,0],
            [9,0,0,0,0,9,9,0,0,0,0,9,0,0,0],
            [0,0,9,9,0,0,0,9,0,9,0,0,9,9,0],
            [0,9,0,0,9,0,0,0,0,0,9,0,0,0,0],
            [0,0,0,0,0,9,0,9,0,0,0,9,9,0,0]
        ]

        obstacles = set()
        grid_height = len(grid)
        grid_width = len(grid[0]) if grid_height > 0 else 0

        for y, row in enumerate(grid):
            for x, cell in enumerate(row):
                if cell == 9:
                    obstacles.add((x, y))
        
        return obstacles, grid_width, grid_height

    def is_valid_state(self, x, y):
        """Verifica se um estado (x, y) é válido (dentro do grid e não é um obstáculo)."""
        return 0 <= x < self.grid_width and 0 <= y < self.grid_height and (x, y) not in self.obstacles

    def get_all_states(self):
        """Retorna uma lista de todos os estados possíveis no grid."""
        states = []
        for y in range(self.grid_height):
            for x in range(self.grid_width):
                if self.is_valid_state(x, y):
                    for orientation in self.orientations:
                        states.append(((x, y), orientation))
        return states

    def set_expansion_priority(self, priority_list):
        """Define a prioridade de expansão com base em uma lista de orientações."""
        self.expansion_priority = {item: i for i, item in enumerate(priority_list)}

    def get_successors(self, state):
        """Gera os sucessores válidos a partir de um estado, com base nas ações possíveis."""
        (x, y), orientation = state
        potential_successors = []

        # Mover para frente
        next_x, next_y = x, y
        if orientation == "Norte": next_y -= 1
        elif orientation == "Leste": next_x += 1
        elif orientation == "Sul": next_y += 1
        elif orientation == "Oeste": next_x -= 1

        if self.is_valid_state(next_x, next_y):
            potential_successors.append((((next_x, next_y), orientation), 1.0, "mover_frente"))

        # Virar à direita
        current_orientation_index = self.orientations.index(orientation)
        new_orientation_index_right = (current_orientation_index + 1) % 4
        new_orientation_right = self.orientations[new_orientation_index_right]
        potential_successors.append((((x, y), new_orientation_right), 0.5, "virar_direita"))

        # Virar à esquerda
        new_orientation_index_left = (current_orientation_index - 1 + 4) % 4
        new_orientation_left = self.orientations[new_orientation_index_left]
        potential_successors.append((((x, y), new_orientation_left), 0.5, "virar_esquerda"))
        
        # Ordena os sucessores com base na prioridade de expansão definida
        sorted_successors = sorted(potential_successors, key=lambda s: self.expansion_priority.get(s[0][1], 999))
        
        return sorted_successors

    def get_cost(self, state1, action, state2):
        """Retorna o custo de uma ação."""
        if "mover_frente" in action: return 1.0
        elif "virar_direita" in action or "virar_esquerda" in action: return 1.5
        return float("inf")

    def heuristic(self, state, goal_state):
        """Calcula a heurística da Distância de Manhattan."""
        (x1, y1), _ = state
        (x2, y2), _ = goal_state

        return abs(x1 - x2) + abs(y1 - y2)
