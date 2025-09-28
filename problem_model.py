
import math
import random

class ProblemModel:
    def __init__(self, grid_width, grid_height, num_obstacles=0, forbidden_coords=None):
        self.grid_width = grid_width
        self.grid_height = grid_height
        self.obstacles = self._generate_random_obstacles(num_obstacles, forbidden_coords)
        self.orientations = ["Norte", "Leste", "Sul", "Oeste"]
        # Default expansion priority for orientations
        self.expansion_priority = {orientation: i for i, orientation in enumerate(self.orientations)}

    def _generate_random_obstacles(self, num_obstacles, forbidden_coords):
        obstacles = set()
        if forbidden_coords is None:
            forbidden_coords = set()

        all_possible_coords = []
        for y in range(self.grid_height):
            for x in range(self.grid_width):
                if (x, y) not in forbidden_coords:
                    all_possible_coords.append((x, y))

        # Ensure num_obstacles does not exceed available non-forbidden cells
        num_obstacles = min(num_obstacles, len(all_possible_coords))

        obstacles = set(random.sample(all_possible_coords, num_obstacles))
        return obstacles

    def is_valid_state(self, x, y):
        # x is column, y is row
        return 0 <= x < self.grid_width and 0 <= y < self.grid_height and (x, y) not in self.obstacles

    def get_all_states(self):
        states = []
        for y in range(self.grid_height):
            for x in range(self.grid_width):
                if self.is_valid_state(x, y):
                    for orientation in self.orientations:
                        states.append(((x, y), orientation))
        return states

    def set_expansion_priority(self, priority_list):
        # priority_list example: ["Norte", "Leste", "Sul", "Oeste"]
        # Assigns a numerical priority based on the order in the list
        self.expansion_priority = {item: i for i, item in enumerate(priority_list)}

    def get_successors(self, state):
        (x, y), orientation = state
        potential_successors = []

        # Mover para frente
        next_x, next_y = x, y
        if orientation == "Norte":
            next_y -= 1  # Move up (decrease y)
        elif orientation == "Leste":
            next_x += 1  # Move right (increase x)
        elif orientation == "Sul":
            next_y += 1  # Move down (increase y)
        elif orientation == "Oeste":
            next_x -= 1  # Move left (decrease x)

        if self.is_valid_state(next_x, next_y):
            potential_successors.append((((next_x, next_y), orientation), 1.0, "mover_frente")) # Custo 1 para mover

        # Virar à direita
        current_orientation_index = self.orientations.index(orientation)
        new_orientation_index = (current_orientation_index + 1) % 4
        new_orientation_right = self.orientations[new_orientation_index]
        potential_successors.append((((x, y), new_orientation_right), 1.5, "virar_direita")) # Custo 1.5 para virar

        # Virar à esquerda
        new_orientation_index = (current_orientation_index - 1 + 4) % 4
        new_orientation_left = self.orientations[new_orientation_index]
        potential_successors.append((((x, y), new_orientation_left), 1.5, "virar_esquerda")) # Custo 1.5 para virar

        # Sort successors based on the orientation of the *new state* (s[0][1])
        # Actions with lower priority value (earlier in the list) come first
        # If the successor is a 'move_forward' action, its orientation is the same as the current state's orientation.
        # If it's a 'turn' action, its orientation is the new orientation after turning.
        # We need to prioritize based on the resulting orientation of the successor state.
        # The key for sorting should be the orientation of the resulting state.
        sorted_successors = sorted(potential_successors, key=lambda s: self.expansion_priority.get(s[0][1], 999))
        
        return sorted_successors

    def get_cost(self, state1, action, state2):
        # O custo já é retornado pela função get_successors
        # Esta função é mais para consistência ou se o custo for dinâmico
        # Para este problema, o custo é fixo por ação.
        if "mover_frente" in action:
            return 1.0
        elif "virar_direita" in action or "virar_esquerda" in action:
            return 1.5
        return float("inf") # Custo infinito para ações desconhecidas

    def heuristic(self, state, goal_state):
        # Heurística de Distância de Manhattan (apenas para a posição, ignorando orientação)
        (x1, y1), _ = state
        (x2, y2), _ = goal_state
        return abs(x1 - x2) + abs(y1 - y2)

