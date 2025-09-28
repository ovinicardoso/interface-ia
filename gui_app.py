import tkinter as tk
from tkinter import ttk, messagebox
from problem_model import ProblemModel
from search_algorithms import SearchAlgorithms
import random

class PathfindingApp(tk.Tk):
    def __init__(self, problem_model: ProblemModel, search_algorithms: SearchAlgorithms):
        super().__init__()
        self.title("Busca de Caminho para Veículos Autônomos")
        self.geometry("1200x800")

        self.problem_model = problem_model
        self.search_algorithms = search_algorithms

        self.create_widgets()
        self.update_limit_entry_visibility()

    def create_widgets(self):
        # Frame principal para organizar os elementos
        main_frame = ttk.Frame(self, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Configurar redimensionamento para o main_frame
        main_frame.grid_rowconfigure(0, weight=1)
        main_frame.grid_columnconfigure(0, weight=0) # controls_frame
        main_frame.grid_columnconfigure(1, weight=1) # visualization_frame

        # Frame para controles de busca
        controls_frame = ttk.LabelFrame(main_frame, text="Controles de Busca", padding="10")
        controls_frame.grid(row=0, column=0, sticky=tk.NSEW, padx=10, pady=5)

        # Configurar redimensionamento para o controls_frame
        for i in range(20): # Increased range to accommodate new widgets
            controls_frame.grid_rowconfigure(i, weight=0)
        controls_frame.grid_rowconfigure(18, weight=1) # path_text should expand
        controls_frame.grid_columnconfigure(0, weight=1) # Allow elements to expand horizontally

        # Seleção do método de busca
        ttk.Label(controls_frame, text="Método de Busca:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.search_method_var = tk.StringVar(self)
        search_methods = [
            "AMPLITUDE",
            "PROFUNDIDADE",
            "PROFUNDIDADE LIMITADA",
            "APROFUNDAMENTO ITERATIVO",
            "BIDIRECIONAL",
            "CUSTO UNIFORME"
        ]
        search_method_menu = ttk.OptionMenu(controls_frame, self.search_method_var, search_methods[0], *search_methods, command=self.update_limit_entry_visibility)
        self.search_method_var.set(search_methods[0]) # Explicitly set after creation
        search_method_menu.grid(row=1, column=0, sticky=tk.EW, pady=5)

        # Limite para Profundidade Limitada e Aprofundamento Iterativo
        self.limit_label = ttk.Label(controls_frame, text="Limite (Prof. Limitada/Aprof. Iterativo):")
        self.limit_label.grid(row=2, column=0, sticky=tk.W, pady=5)
        self.limit_entry = ttk.Entry(controls_frame)
        self.limit_entry.insert(0, "10") # Valor padrão
        self.limit_entry.grid(row=3, column=0, sticky=tk.EW, pady=5)

        # Seleção do estado inicial
        ttk.Label(controls_frame, text="Estado Inicial (X, Y, orientação):").grid(row=4, column=0, sticky=tk.W, pady=5)
        
        start_state_frame = ttk.Frame(controls_frame)
        start_state_frame.grid(row=5, column=0, sticky=tk.EW, pady=5)
        start_state_frame.grid_columnconfigure(0, weight=1)
        start_state_frame.grid_columnconfigure(1, weight=1)
        start_state_frame.grid_columnconfigure(2, weight=1)
        
        self.start_x_entry = ttk.Entry(start_state_frame)
        self.start_x_entry.insert(0, "2")
        self.start_x_entry.grid(row=0, column=0, sticky=tk.EW, padx=(0, 5))
        
        self.start_y_entry = ttk.Entry(start_state_frame)
        self.start_y_entry.insert(0, "5")
        self.start_y_entry.grid(row=0, column=1, sticky=tk.EW, padx=(0, 5))
        
        self.start_orientation_var = tk.StringVar(self)
        start_orientation_menu = ttk.OptionMenu(start_state_frame, self.start_orientation_var, self.problem_model.orientations[0], *self.problem_model.orientations)
        self.start_orientation_var.set(self.problem_model.orientations[0])
        start_orientation_menu.grid(row=0, column=2, sticky=tk.EW)

        # Seleção do estado objetivo
        ttk.Label(controls_frame, text="Estado Objetivo (X, Y, orientação):").grid(row=6, column=0, sticky=tk.W, pady=5)
        
        goal_state_frame = ttk.Frame(controls_frame)
        goal_state_frame.grid(row=7, column=0, sticky=tk.EW, pady=5)
        goal_state_frame.grid_columnconfigure(0, weight=1)
        goal_state_frame.grid_columnconfigure(1, weight=1)
        goal_state_frame.grid_columnconfigure(2, weight=1)
        
        self.goal_x_entry = ttk.Entry(goal_state_frame)
        self.goal_x_entry.insert(0, "28") # Adjusted for 30x30 grid
        self.goal_x_entry.grid(row=0, column=0, sticky=tk.EW, padx=(0, 5))
        
        self.goal_y_entry = ttk.Entry(goal_state_frame)
        self.goal_y_entry.insert(0, "28") # Adjusted for 30x30 grid
        self.goal_y_entry.grid(row=0, column=1, sticky=tk.EW, padx=(0, 5))
        
        self.goal_orientation_var = tk.StringVar(self)
        goal_orientation_menu = ttk.OptionMenu(goal_state_frame, self.goal_orientation_var, self.problem_model.orientations[0], *self.problem_model.orientations)
        self.goal_orientation_var.set(self.problem_model.orientations[0])
        goal_orientation_menu.grid(row=0, column=2, sticky=tk.EW)

        # --- NOVA Seção para Prioridade de Expansão (Reordenável) ---
        ttk.Label(controls_frame, text="Prioridade de Expansão (Orientações):").grid(row=8, column=0, sticky=tk.W, pady=5)
        
        reorder_priority_frame = ttk.Frame(controls_frame)
        reorder_priority_frame.grid(row=9, column=0, sticky=tk.EW, pady=5)
        reorder_priority_frame.grid_columnconfigure(0, weight=1) # Listbox
        reorder_priority_frame.grid_columnconfigure(1, weight=0) # Buttons

        self.priority_listbox = tk.Listbox(reorder_priority_frame, height=4, exportselection=False)
        self.priority_listbox.grid(row=0, column=0, sticky=tk.NSEW)
        for orientation in self.problem_model.orientations:
            self.priority_listbox.insert(tk.END, orientation)
        self.priority_listbox.selection_set(0) # Select the first item by default

        button_frame = ttk.Frame(reorder_priority_frame)
        button_frame.grid(row=0, column=1, sticky=tk.NS, padx=5)

        up_button = ttk.Button(button_frame, text="Subir", command=self.move_priority_up)
        up_button.pack(pady=2, fill=tk.X)

        down_button = ttk.Button(button_frame, text="Descer", command=self.move_priority_down)
        down_button.pack(pady=2, fill=tk.X)

        # Botão de busca
        search_button = ttk.Button(controls_frame, text="Iniciar Busca", command=self.run_search)
        search_button.grid(row=10, column=0, sticky=tk.EW, pady=10)

        # Exibição do custo
        ttk.Label(controls_frame, text="Custo do Caminho:").grid(row=11, column=0, sticky=tk.W, pady=5)
        self.cost_label = ttk.Label(controls_frame, text="-")
        self.cost_label.grid(row=12, column=0, sticky=tk.W, pady=5)

        # Exibição do caminho
        ttk.Label(controls_frame, text="Caminho Encontrado:").grid(row=13, column=0, sticky=tk.W, pady=5)
        self.path_text = tk.Text(controls_frame, height=15, state=tk.DISABLED, wrap=tk.WORD) # Increased height and added word wrap
        self.path_text.grid(row=14, column=0, sticky=tk.NSEW, pady=5)

        # Frame para visualização do problema
        visualization_frame = ttk.LabelFrame(main_frame, text="Visualização do Problema", padding="10")
        visualization_frame.grid(row=0, column=1, sticky=tk.NSEW, padx=10, pady=5)
        visualization_frame.grid_rowconfigure(0, weight=1)
        visualization_frame.grid_columnconfigure(0, weight=1)

        self.canvas = tk.Canvas(visualization_frame, bg="white")
        self.canvas.grid(row=0, column=0, sticky=tk.NSEW)

        # Bind resize event for dynamic resizing
        self.canvas.bind("<Configure>", self.on_canvas_resize)

        self.draw_grid()

    def move_priority_up(self):
        selected_indices = self.priority_listbox.curselection()
        if not selected_indices:
            return

        for index in selected_indices:
            if index > 0:
                text = self.priority_listbox.get(index)
                self.priority_listbox.delete(index)
                self.priority_listbox.insert(index - 1, text)
                self.priority_listbox.selection_set(index - 1)

    def move_priority_down(self):
        selected_indices = self.priority_listbox.curselection()
        if not selected_indices:
            return

        # Reverse order to handle multiple selections correctly
        for index in reversed(selected_indices):
            if index < self.priority_listbox.size() - 1:
                text = self.priority_listbox.get(index)
                self.priority_listbox.delete(index)
                self.priority_listbox.insert(index + 1, text)
                self.priority_listbox.selection_set(index + 1)

    def update_limit_entry_visibility(self, *args):
        selected_method = self.search_method_var.get()
        if selected_method in ["PROFUNDIDADE LIMITADA", "APROFUNDAMENTO ITERATIVO"]:
            self.limit_label.grid(row=2, column=0, sticky=tk.W, pady=5)
            self.limit_entry.grid(row=3, column=0, sticky=tk.EW, pady=5)
        else:
            self.limit_label.grid_remove()
            self.limit_entry.grid_remove()

    def on_canvas_resize(self, event):
        self.draw_grid(path_to_draw=self.current_path if hasattr(self, 'current_path') else None)

    def draw_grid(self, path_to_draw=None):
        self.canvas.delete("all")
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()

        if canvas_width == 1 or canvas_height == 1: # Avoid division by zero or drawing on minimal size
            return

        # Adjust cell_size to fit the grid and numbering
        num_offset = 30 # Space for numbers
        
        cell_size_w = (canvas_width - num_offset) / self.problem_model.grid_width
        cell_size_h = (canvas_height - num_offset) / self.problem_model.grid_height
        cell_size = min(cell_size_w, cell_size_h)

        # Draw column numbers (X-axis)
        for x_coord in range(self.problem_model.grid_width):
            self.canvas.create_text(
                num_offset + x_coord * cell_size + cell_size / 2,
                num_offset / 2, text=str(x_coord), fill="black", font=("Arial", 8)
            )
        # Draw row numbers (Y-axis)
        for y_coord in range(self.problem_model.grid_height):
            self.canvas.create_text(
                num_offset / 2,
                num_offset + y_coord * cell_size + cell_size / 2, text=str(y_coord), fill="black", font=("Arial", 8)
            )

        for y_coord in range(self.problem_model.grid_height):
            for x_coord in range(self.problem_model.grid_width):
                x1, y1 = num_offset + x_coord * cell_size, num_offset + y_coord * cell_size
                x2, y2 = x1 + cell_size, y1 + cell_size
                color = "lightgray" if (x_coord, y_coord) in self.problem_model.obstacles else "white"
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="gray", tags="grid_cell")
        
        if path_to_draw:
            self.draw_path_on_grid(path_to_draw, cell_size, num_offset)

    def draw_path_on_grid(self, path, cell_size, num_offset):
        if path:
            for i, state in enumerate(path):
                (x_coord, y_coord), orientation = state
                center_x = num_offset + x_coord * cell_size + cell_size / 2
                center_y = num_offset + y_coord * cell_size + cell_size / 2

                self.canvas.create_oval(
                    center_x - cell_size/4, center_y - cell_size/4,
                    center_x + cell_size/4, center_y + cell_size/4,
                    fill="blue" if i == 0 else ("red" if i == len(path) - 1 else "green"),
                    outline="black", tags="path_node"
                )

                arrow_length = cell_size / 3
                if orientation == 'Norte':
                    self.canvas.create_line(center_x, center_y + arrow_length, center_x, center_y - arrow_length, arrow=tk.LAST, tags="path_arrow")
                elif orientation == 'Leste':
                    self.canvas.create_line(center_x - arrow_length, center_y, center_x + arrow_length, center_y, arrow=tk.LAST, tags="path_arrow")
                elif orientation == 'Sul':
                    self.canvas.create_line(center_x, center_y - arrow_length, center_x, center_y + arrow_length, arrow=tk.LAST, tags="path_arrow")
                elif orientation == 'Oeste':
                    self.canvas.create_line(center_x + arrow_length, center_y, center_x - arrow_length, center_y, arrow=tk.LAST, tags="path_arrow")

                if i > 0:
                    prev_state = path[i-1]
                    (prev_x_coord, prev_y_coord), _ = prev_state
                    prev_center_x = num_offset + prev_x_coord * cell_size + cell_size / 2
                    prev_center_y = num_offset + prev_y_coord * cell_size + cell_size / 2
                    self.canvas.create_line(prev_center_x, prev_center_y, center_x, center_y, fill="blue", width=2, tags="path_line")

    def run_search(self):
        try:
            start_x = int(self.start_x_entry.get())
            start_y = int(self.start_y_entry.get())
            start_orientation = self.start_orientation_var.get()
            start_state = ((start_x, start_y), start_orientation)

            goal_x = int(self.goal_x_entry.get())
            goal_y = int(self.goal_y_entry.get())
            goal_orientation = self.goal_orientation_var.get()
            goal_state = ((goal_x, goal_y), goal_orientation)

            search_method = self.search_method_var.get()
            limit = int(self.limit_entry.get()) if self.limit_entry.get() else 0

            # Get expansion priority from the reorderable listbox
            priority_order = list(self.priority_listbox.get(0, tk.END))
            self.problem_model.set_expansion_priority(priority_order)

            path = None
            cost = 0

            if not (0 <= start_x < self.problem_model.grid_width and 0 <= start_y < self.problem_model.grid_height):
                messagebox.showerror("Erro", f"Coordenadas iniciais ({start_x}, {start_y}) fora dos limites da grade.")
                return
            if not (0 <= goal_x < self.problem_model.grid_width and 0 <= goal_y < self.problem_model.grid_height):
                messagebox.showerror("Erro", f"Coordenadas objetivo ({goal_x}, {goal_y}) fora dos limites da grade.")
                return

            if (start_x, start_y) in self.problem_model.obstacles:
                messagebox.showerror("Erro", f"Estado inicial ({(start_x, start_y)}) é um obstáculo.")
                return
            if (goal_x, goal_y) in self.problem_model.obstacles:
                messagebox.showerror("Erro", f"Estado objetivo ({(goal_x, goal_y)}) é um obstáculo.")
                return

            if search_method == "AMPLITUDE":
                path, cost = self.search_algorithms.amplitude(start_state, goal_state)
            elif search_method == "PROFUNDIDADE":
                path, cost = self.search_algorithms.profundidade(start_state, goal_state)
            elif search_method == "PROFUNDIDADE LIMITADA":
                path, cost = self.search_algorithms.prof_limitada(start_state, goal_state, limit)
            elif search_method == "APROFUNDAMENTO ITERATIVO":
                path, cost = self.search_algorithms.aprof_iterativo(start_state, goal_state, limit)
            elif search_method == "BIDIRECIONAL":
                path, cost = self.search_algorithms.bidirecional(start_state, goal_state)
            elif search_method == "CUSTO UNIFORME":
                path, cost = self.search_algorithms.custo_uniforme(start_state, goal_state)

            self.cost_label.config(text=f"{cost:.2f}" if path else "Caminho não encontrado")
            self.path_text.config(state=tk.NORMAL)
            self.path_text.delete(1.0, tk.END)
            if path:
                self.path_text.insert(tk.END, " -> ".join(str(s) for s in path))
                self.current_path = path
                self.draw_grid(path_to_draw=path)
            else:
                self.path_text.insert(tk.END, "Nenhum caminho encontrado.")
                self.current_path = None
                self.draw_grid()
            self.path_text.config(state=tk.DISABLED)

        except ValueError:
            messagebox.showerror("Erro de Entrada", "Por favor, insira valores numéricos válidos.")
        except Exception as e:
            messagebox.showerror("Erro", f"Ocorreu um erro: {e}")


if __name__ == "__main__":
    grid_width = 30
    grid_height = 30
    num_obstacles = 100

    initial_coords = (2, 5)
    goal_coords = (28, 28)
    forbidden_coords = {initial_coords, goal_coords}

    problem_model = ProblemModel(grid_width=grid_width, grid_height=grid_height, num_obstacles=num_obstacles, forbidden_coords=forbidden_coords)
    search_algorithms = SearchAlgorithms(problem_model)

    app = PathfindingApp(problem_model, search_algorithms)
    app.mainloop()