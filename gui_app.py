import tkinter as tk
from tkinter import ttk, messagebox
from problem_model import ProblemModel
from search_algorithms import SearchAlgorithms
import random

class PathfindingApp(tk.Tk):
    """
    Classe principal da aplicação com a interface gráfica.
    """
    def __init__(self, problem_model: ProblemModel, search_algorithms: SearchAlgorithms):
        super().__init__()
        self.title("Busca de Caminho para Veículos Autônomos")
        self.geometry("1200x800")

        self.problem_model = problem_model
        self.search_algorithms = search_algorithms
        self.current_path = None

        self.create_widgets()
        # Chama a função para garantir o estado visual inicial correto
        self.update_limit_entry_visibility()
        # Adiciona um pequeno delay para o primeiro desenho do grid para garantir que a janela tenha tamanho
        self.after(100, lambda: self.draw_grid())


    def create_widgets(self):
        """Cria e organiza os widgets na janela."""
        main_frame = ttk.Frame(self, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        main_frame.grid_rowconfigure(0, weight=1)
        main_frame.grid_columnconfigure(1, weight=1)

        controls_frame = ttk.LabelFrame(main_frame, text="Controles de Busca", padding="10")
        controls_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=5)
        controls_frame.grid_columnconfigure(0, weight=1)

        # --- ORDEM CORRIGIDA ---
        # 1. Primeiro, criamos os widgets de Limite
        self.limit_label = ttk.Label(controls_frame, text="Limite (Prof. Limitada/Aprof. Iterativo):")
        self.limit_entry = ttk.Entry(controls_frame)
        self.limit_entry.insert(0, "40") # Aumentado para o novo mapa

        # 2. Agora, criamos o menu que pode afetar a visibilidade dos widgets de Limite
        ttk.Label(controls_frame, text="Método de Busca:").grid(row=0, column=0, sticky="w", pady=5)
        self.search_method_var = tk.StringVar(self)
        search_methods = ["AMPLITUDE", "PROFUNDIDADE", "PROFUNDIDADE LIMITADA", "APROFUNDAMENTO ITERATIVO", "BIDIRECIONAL", "CUSTO UNIFORME"]
        # A função `update_limit_entry_visibility` será chamada sempre que o usuário mudar a opção
        search_method_menu = ttk.OptionMenu(controls_frame, self.search_method_var, search_methods[0], *search_methods, command=self.update_limit_entry_visibility)
        search_method_menu.grid(row=1, column=0, sticky="ew", pady=5)
        
        # Posiciona os widgets de limite na tela (eles serão escondidos/mostrados pela função de visibilidade)
        self.limit_label.grid(row=2, column=0, sticky="w", pady=5)
        self.limit_entry.grid(row=3, column=0, sticky="ew", pady=5)


        # Seleção do estado inicial
        ttk.Label(controls_frame, text="Estado Inicial (X, Y, orientação):").grid(row=4, column=0, sticky="w", pady=5)
        start_state_frame = ttk.Frame(controls_frame)
        start_state_frame.grid(row=5, column=0, sticky="ew", pady=5)
        self.start_x_entry = ttk.Entry(start_state_frame, width=5)
        self.start_x_entry.insert(0, "0") # INÍCIO X
        self.start_x_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
        self.start_y_entry = ttk.Entry(start_state_frame, width=5)
        self.start_y_entry.insert(0, "0") # INÍCIO Y
        self.start_y_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
        self.start_orientation_var = tk.StringVar(self)
        start_orientation_menu = ttk.OptionMenu(start_state_frame, self.start_orientation_var, self.problem_model.orientations[0], *self.problem_model.orientations)
        self.start_orientation_var.set(self.problem_model.orientations[1]) # 'Leste'
        start_orientation_menu.pack(side=tk.LEFT, fill=tk.X, expand=True)

        # Seleção do estado objetivo
        ttk.Label(controls_frame, text="Estado Objetivo (X, Y, orientação):").grid(row=6, column=0, sticky="w", pady=5)
        goal_state_frame = ttk.Frame(controls_frame)
        goal_state_frame.grid(row=7, column=0, sticky="ew", pady=5)
        self.goal_x_entry = ttk.Entry(goal_state_frame, width=5)
        self.goal_x_entry.insert(0, "14") # FIM X
        self.goal_x_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
        self.goal_y_entry = ttk.Entry(goal_state_frame, width=5)
        self.goal_y_entry.insert(0, "14") # FIM Y
        self.goal_y_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
        self.goal_orientation_var = tk.StringVar(self)
        goal_orientation_menu = ttk.OptionMenu(goal_state_frame, self.goal_orientation_var, self.problem_model.orientations[0], *self.problem_model.orientations)
        self.goal_orientation_var.set(self.problem_model.orientations[0])
        goal_orientation_menu.pack(side=tk.LEFT, fill=tk.X, expand=True)

        # Prioridade de Expansão
        ttk.Label(controls_frame, text="Prioridade de Expansão:").grid(row=8, column=0, sticky="w", pady=(10, 5))
        reorder_priority_frame = ttk.Frame(controls_frame)
        reorder_priority_frame.grid(row=9, column=0, sticky="ew", pady=5)
        self.priority_listbox = tk.Listbox(reorder_priority_frame, height=4, exportselection=False)
        for orientation in self.problem_model.orientations:
            self.priority_listbox.insert(tk.END, orientation)
        self.priority_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        button_frame = ttk.Frame(reorder_priority_frame)
        button_frame.pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="↑", command=self.move_priority_up, width=2).pack(pady=2)
        ttk.Button(button_frame, text="↓", command=self.move_priority_down, width=2).pack(pady=2)

        # Botão de busca
        search_button = ttk.Button(controls_frame, text="Iniciar Busca", command=self.run_search)
        search_button.grid(row=10, column=0, sticky="ew", pady=10)

        # Resultados
        ttk.Label(controls_frame, text="Custo do Caminho:").grid(row=11, column=0, sticky="w", pady=5)
        self.cost_label = ttk.Label(controls_frame, text="-", font=("Consolas", 10, "bold"))
        self.cost_label.grid(row=12, column=0, sticky="w", pady=5)
        ttk.Label(controls_frame, text="Caminho Encontrado:").grid(row=13, column=0, sticky="w", pady=5)
        self.path_text = tk.Text(controls_frame, height=10, state=tk.DISABLED, wrap=tk.WORD)
        self.path_text.grid(row=14, column=0, sticky="nsew", pady=5)
        controls_frame.grid_rowconfigure(14, weight=1)

        # Frame de visualização
        visualization_frame = ttk.LabelFrame(main_frame, text="Visualização do Problema", padding="10")
        visualization_frame.grid(row=0, column=1, sticky="nsew", padx=10, pady=5)
        visualization_frame.grid_rowconfigure(0, weight=1)
        visualization_frame.grid_columnconfigure(0, weight=1)

        self.canvas = tk.Canvas(visualization_frame, bg="white")
        self.canvas.grid(row=0, column=0, sticky="nsew")
        self.canvas.bind("<Configure>", self.on_canvas_resize)


    def move_priority_up(self):
        """Move o item selecionado na lista de prioridades para cima."""
        indices = self.priority_listbox.curselection()
        if not indices: return
        for index in indices:
            if index > 0:
                text = self.priority_listbox.get(index)
                self.priority_listbox.delete(index)
                self.priority_listbox.insert(index - 1, text)
                self.priority_listbox.selection_set(index - 1)

    def move_priority_down(self):
        """Move o item selecionado na lista de prioridades para baixo."""
        indices = self.priority_listbox.curselection()
        if not indices: return
        for index in reversed(indices):
            if index < self.priority_listbox.size() - 1:
                text = self.priority_listbox.get(index)
                self.priority_listbox.delete(index)
                self.priority_listbox.insert(index + 1, text)
                self.priority_listbox.selection_set(index + 1)

    def update_limit_entry_visibility(self, *args):
        """Mostra ou oculta o campo de limite, dependendo do método de busca selecionado."""
        if self.search_method_var.get() in ["PROFUNDIDADE LIMITADA", "APROFUNDAMENTO ITERATIVO"]:
            self.limit_label.grid()
            self.limit_entry.grid()
        else:
            self.limit_label.grid_remove()
            self.limit_entry.grid_remove()

    def on_canvas_resize(self, event):
        """Redesenha o grid quando o tamanho da janela é alterado."""
        self.draw_grid()

    def draw_grid(self):
        """Desenha o grid, obstáculos e o caminho no canvas."""
        self.canvas.delete("all")
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()
        if canvas_width < 50 or canvas_height < 50: return

        num_offset = 20
        cell_size = min((canvas_width - num_offset) / self.problem_model.grid_width, (canvas_height - num_offset) / self.problem_model.grid_height)
        
        for y in range(self.problem_model.grid_height):
            self.canvas.create_text(num_offset / 2, num_offset + y * cell_size + cell_size / 2, text=str(y), fill="black")
        for x in range(self.problem_model.grid_width):
            self.canvas.create_text(num_offset + x * cell_size + cell_size / 2, num_offset / 2, text=str(x), fill="black")

        for y in range(self.problem_model.grid_height):
            for x in range(self.problem_model.grid_width):
                x1, y1 = num_offset + x * cell_size, num_offset + y * cell_size
                x2, y2 = x1 + cell_size, y1 + cell_size
                color = "#555" if (x, y) in self.problem_model.obstacles else "white"
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="gray")
        
        if self.current_path:
            self.draw_path_on_grid(self.current_path, cell_size, num_offset)


    def draw_path_on_grid(self, path, cell_size, num_offset):
        """Desenha uma representação do caminho encontrado no grid."""
        if not path: return

        # Desenha as linhas do caminho
        for i in range(len(path) - 1):
            (x1, y1), _ = path[i]
            (x2, y2), _ = path[i+1]
            center1_x = num_offset + x1 * cell_size + cell_size / 2
            center1_y = num_offset + y1 * cell_size + cell_size / 2
            center2_x = num_offset + x2 * cell_size + cell_size / 2
            center2_y = num_offset + y2 * cell_size + cell_size / 2
            if x1 != x2 or y1 != y2: # Só desenha linha se houve movimento
                self.canvas.create_line(center1_x, center1_y, center2_x, center2_y, fill="#4287f5", width=3)

        # Desenha os nós (início, fim e intermediários)
        for i, state in enumerate(path):
            (x, y), orientation = state
            center_x = num_offset + x * cell_size + cell_size / 2
            center_y = num_offset + y * cell_size + cell_size / 2
            
            if i == 0: color = "green"  # Ponto inicial
            elif i == len(path) - 1: color = "red" # Ponto final
            else: color = "#4287f5" # Pontos intermediários

            # Desenha um triângulo para indicar a orientação
            arrow_length = cell_size * 0.3
            if orientation == 'Norte': points = [center_x, center_y - arrow_length, center_x - arrow_length, center_y + arrow_length, center_x + arrow_length, center_y + arrow_length]
            elif orientation == 'Leste': points = [center_x + arrow_length, center_y, center_x - arrow_length, center_y - arrow_length, center_x - arrow_length, center_y + arrow_length]
            elif orientation == 'Sul': points = [center_x, center_y + arrow_length, center_x - arrow_length, center_y - arrow_length, center_x + arrow_length, center_y - arrow_length]
            else: # Oeste
                points = [center_x - arrow_length, center_y, center_x + arrow_length, center_y - arrow_length, center_x + arrow_length, center_y + arrow_length]
            
            self.canvas.create_polygon(points, fill=color, outline='black')


    def run_search(self):
        """Executa o algoritmo de busca selecionado com os parâmetros da interface."""
        try:
            start_x, start_y = int(self.start_x_entry.get()), int(self.start_y_entry.get())
            start_orientation = self.start_orientation_var.get()
            start_state = ((start_x, start_y), start_orientation)

            goal_x, goal_y = int(self.goal_x_entry.get()), int(self.goal_y_entry.get())
            goal_orientation = self.goal_orientation_var.get()
            goal_state = ((goal_x, goal_y), goal_orientation)

            if not (0 <= start_x < self.problem_model.grid_width and 0 <= start_y < self.problem_model.grid_height) or (start_x, start_y) in self.problem_model.obstacles:
                messagebox.showerror("Erro de Entrada", f"Estado inicial ({start_x}, {start_y}) é inválido ou um obstáculo.")
                return
            if not (0 <= goal_x < self.problem_model.grid_width and 0 <= goal_y < self.problem_model.grid_height) or (goal_x, goal_y) in self.problem_model.obstacles:
                messagebox.showerror("Erro de Entrada", f"Estado objetivo ({goal_x}, {goal_y}) é inválido ou um obstáculo.")
                return

            search_method = self.search_method_var.get()
            limit = int(self.limit_entry.get()) if self.limit_entry.get() else 0

            priority_order = list(self.priority_listbox.get(0, tk.END))
            self.problem_model.set_expansion_priority(priority_order)

            path, cost = None, 0
            
            search_function_map = {
                "AMPLITUDE": self.search_algorithms.amplitude,
                "PROFUNDIDADE": self.search_algorithms.profundidade,
                "PROFUNDIDADE LIMITADA": lambda i, f: self.search_algorithms.prof_limitada(i, f, limit),
                "APROFUNDAMENTO ITERATIVO": lambda i, f: self.search_algorithms.aprof_iterativo(i, f, limit),
                "BIDIRECIONAL": self.search_algorithms.bidirecional,
                "CUSTO UNIFORME": self.search_algorithms.custo_uniforme
            }
            
            path, cost = search_function_map[search_method](start_state, goal_state)

            self.cost_label.config(text=f"{cost:.2f}" if path else "Não encontrado")
            self.path_text.config(state=tk.NORMAL)
            self.path_text.delete(1.0, tk.END)
            if path:
                path_str = " -> ".join([f"({s[0][0]},{s[0][1]},{s[1][0]})" for s in path])
                self.path_text.insert(tk.END, path_str)
                self.current_path = path
            else:
                self.path_text.insert(tk.END, "Nenhum caminho encontrado.")
                self.current_path = None
            
            self.path_text.config(state=tk.DISABLED)
            self.draw_grid()

        except ValueError:
            messagebox.showerror("Erro de Entrada", "As coordenadas X e Y devem ser números inteiros.")
        except Exception as e:
            messagebox.showerror("Erro Inesperado", f"Ocorreu um erro: {e}")

if __name__ == "__main__":
    # Carrega o modelo do problema com o grid estático
    problem_model = ProblemModel()
    search_algorithms = SearchAlgorithms(problem_model)

    app = PathfindingApp(problem_model, search_algorithms)
    app.mainloop()