class GameOfLife:
    # Moteur du Jeu de la Vie, avec historique pour debug.

    def __init__(self, rows: int, cols: int):
        self.rows = rows
        self.cols = cols
        self.grid = [[0 for _ in range(cols)] for _ in range(rows)]

        # --- Historique ---
        self.history = []
        self.current_index = -1
        self.save_state()  # enregistre l’état initial

    # ---------------------------
    # Gestion de l'historique
    # ---------------------------

    def save_state(self):
        """Enregistre une copie de la grille dans l’historique."""
        # Si on a reculé puis modifié : supprimer le futur
        if self.current_index < len(self.history) - 1:
            self.history = self.history[:self.current_index + 1]

        # Ne pas enregistrer si identique au précédent
        if self.history and self.grid == self.history[-1]:
            return
        
        # Sauvegarde profonde
        self.history.append([row[:] for row in self.grid])
        self.current_index += 1

    def restore_state(self, index: int):
        """Restaure un état précédent."""
        if 0 <= index < len(self.history):
            self.current_index = index
            self.grid = [row[:] for row in self.history[index]]

    def previous_generation(self):
        """Revenir à la génération précédente."""
        if self.current_index > 0:
            self.restore_state(self.current_index - 1)

    # ---------------------------
    # Logique du Jeu de la Vie
    # ---------------------------

    def display(self):
        for row in self.grid:
            print(" ".join("■" if cell else "." for cell in row))
        print()

    def set_cell(self, row: int, col: int, state: int):
        if 0 <= row < self.rows and 0 <= col < self.cols:
            self.grid[row][col] = 1 if state else 0
            # Important : on enregistre le changement manuel dans l’historique
            self.save_state()

    def count_neighbors(self, row: int, col: int) -> int:
        directions = [
            (-1, -1), (-1, 0), (-1, 1),
            (0, -1),          (0, 1),
            (1, -1),  (1, 0), (1, 1)
        ]
        count = 0
        for dr, dc in directions:
            r, c = row + dr, col + dc
            if 0 <= r < self.rows and 0 <= c < self.cols:
                count += self.grid[r][c]
        return count

    def next_generation(self):
        """Calcul de la génération suivante + enregistrement dans l’historique."""
        new_grid = [[0 for _ in range(self.cols)] for _ in range(self.rows)]
        alive_found = False

        for r in range(self.rows):
            for c in range(self.cols):
                neighbors = self.count_neighbors(r, c)

                if self.grid[r][c] == 1:
                    new_state = 1 if neighbors in (2, 3) else 0
                else:
                    new_state = 1 if neighbors == 3 else 0

                new_grid[r][c] = new_state
                if new_state == 1:
                    alive_found = True

        # Si aucune cellule vivante → fin automatique
        if not alive_found:
            return False  # renvoie False pour signaler "mort totale"

        self.grid = new_grid
        self.save_state()
        return True
