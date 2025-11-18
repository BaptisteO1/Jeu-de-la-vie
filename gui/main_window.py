import logging
import sys
from pathlib import Path
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QGridLayout, QSlider, QFrame, QSpacerItem,
    QSizePolicy, QComboBox, QFileDialog
)
from PyQt6.QtCore import Qt, QTimer
from core.config import Config
from core.game import GameOfLife
from .cell_widget import CellWidget
from .pattern_manager import PatternManager
from core.version import get_version

logger = logging.getLogger(__name__)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Jeu de la Vie — Patterns Sauvegardés")
        self.setGeometry(100, 100, 1000, 600)

        self.rows, self.cols = 20, 20
        self.game = GameOfLife(self.rows, self.cols)

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_generation)
        self.pattern_manager = PatternManager()

        # --- Layout principal ---
        central_widget = QWidget()
        self.main_layout = QHBoxLayout()
        central_widget.setLayout(self.main_layout)
        self.setCentralWidget(central_widget)

        self.setWindowTitle(f"Jeu de la Vie — v{get_version()}")

        # ============================================================
        #                     GRILLE GRAPHIQUE
        # ============================================================
        self.grid_frame = QFrame()
        self.grid_frame.setFrameShape(QFrame.Shape.StyledPanel)
        self.grid_layout = QGridLayout()
        self.grid_layout.setSpacing(1)
        self.grid_frame.setLayout(self.grid_layout)
        self.cells = []

        for r in range(self.rows):
            row_cells = []
            for c in range(self.cols):
                cell = CellWidget(r, c, self.on_cell_clicked)
                self.grid_layout.addWidget(cell, r, c)
                row_cells.append(cell)
            self.cells.append(row_cells)

        # ============================================================
        #                       DASHBOARD
        # ============================================================
        self.dashboard = QFrame()
        self.dashboard.setFixedWidth(280)
        self.dashboard.setFrameShape(QFrame.Shape.StyledPanel)
        dash_layout = QVBoxLayout()
        dash_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.dashboard.setLayout(dash_layout)

        dash_layout.addWidget(QLabel("Contrôles du Jeu de la Vie"))

        # --- Boutons Start / Reset ---
        self.start_button = QPushButton("▶️ Démarrer")
        self.start_button.clicked.connect(self.toggle_simulation)

        self.reset_button = QPushButton("🔄 Réinitialiser")
        self.reset_button.clicked.connect(self.reset_grid)

        dash_layout.addWidget(self.start_button)
        dash_layout.addWidget(self.reset_button)

        # ============================================================
        # DEBUG → Boutons Précédent / Suivant
        # ============================================================
        if Config.DEBUG:
            dash_layout.addWidget(QLabel("Mode Debug"))

            # Boutons
            self.back_button = QPushButton("⏪ Précédent")
            self.back_button.clicked.connect(self.go_previous)

            self.forward_button = QPushButton("⏩ Suivant")
            self.forward_button.clicked.connect(self.go_forward)

            dash_layout.addWidget(self.back_button)
            dash_layout.addWidget(self.forward_button)

            # --- Slider timeline ---
            dash_layout.addWidget(QLabel("Historique :"))
            self.timeline_slider = QSlider(Qt.Orientation.Horizontal)
            self.timeline_slider.setMinimum(0)
            self.timeline_slider.setMaximum(0)
            self.timeline_slider.setValue(0)
            self.timeline_slider.valueChanged.connect(self.on_timeline_changed)
            dash_layout.addWidget(self.timeline_slider)


        # ============================================================
        #               Vitesse de simulation
        # ============================================================
        dash_layout.addWidget(QLabel("Vitesse (ms):"))
        self.speed_slider = QSlider(Qt.Orientation.Horizontal)
        self.speed_slider.setMinimum(50)
        self.speed_slider.setMaximum(1000)
        self.speed_slider.setValue(200)
        self.speed_slider.valueChanged.connect(self.change_speed)
        dash_layout.addWidget(self.speed_slider)

        # ============================================================
        #                  Patterns prédéfinis
        # ============================================================
        dash_layout.addWidget(QLabel("Charger un Pattern:"))
        self.pattern_combo = QComboBox()
        self.pattern_combo.addItems(self.pattern_manager.get_builtin_patterns())
        self.pattern_combo.currentTextChanged.connect(self.load_pattern)
        dash_layout.addWidget(self.pattern_combo)

        # ============================================================
        #          Sauvegarde/Chargement Patterns JSON
        # ============================================================
        self.save_button = QPushButton("💾 Sauvegarder Pattern")
        self.save_button.clicked.connect(self.save_pattern)

        self.load_file_button = QPushButton("📂 Charger Pattern")
        self.load_file_button.clicked.connect(self.load_pattern_file)

        dash_layout.addWidget(self.save_button)
        dash_layout.addWidget(self.load_file_button)

        dash_layout.addItem(QSpacerItem(20, 40, QSizePolicy.Policy.Minimum,
                                        QSizePolicy.Policy.Expanding))

        # Assemble layout
        self.main_layout.addWidget(self.grid_frame)
        self.main_layout.addWidget(self.dashboard)

    # ============================================================
    #                     MISE À JOUR GRILLE
    # ============================================================

    def refresh_cells(self):
        """Met à jour l'UI selon l'état de self.game.grid."""
        for r in range(self.rows):
            for c in range(self.cols):
                alive = bool(self.game.grid[r][c])
                self.cells[r][c].alive = alive
                self.cells[r][c].update_color()

    # ============================================================
    #                     ÉVÉNEMENTS UI
    # ============================================================

    def on_cell_clicked(self, row, col, alive):
        self.game.set_cell(row, col, 1 if alive else 0)
        self.refresh_cells()

    def toggle_simulation(self):
        if self.timer.isActive():
            self.timer.stop()
            self.start_button.setText("▶️ Démarrer")
        else:
            self.timer.start(self.speed_slider.value())
            self.start_button.setText("⏸️ Pause")

    def update_generation(self):
        alive = self.game.next_generation()

        # Stop si grille morte
        if alive is False:
            self.timer.stop()
            self.start_button.setText("▶️ Démarrer")

        self.refresh_cells()

        # Mise à jour slider sans déclencher on_timeline_changed()
        if Config.DEBUG:
            self.timeline_slider.blockSignals(True)
            self.timeline_slider.setMaximum(len(self.game.history) - 1)
            self.timeline_slider.setValue(self.game.current_index)
            self.timeline_slider.blockSignals(False)

    def on_timeline_changed(self, index):
        if not Config.DEBUG:
            return

        self.timer.stop()
        self.game.restore_state(index)
        self.refresh_cells()


    def reset_grid(self):
        self.timer.stop()
        self.start_button.setText("▶️ Démarrer")
        self.game = GameOfLife(self.rows, self.cols)
        self.refresh_cells()

    def change_speed(self):
        if self.timer.isActive():
            self.timer.start(self.speed_slider.value())

    # ============================================================
    #               CONTROLES DEBUG (⏪ / ⏩)
    # ============================================================

    def go_previous(self):
        self.timer.stop()
        self.game.previous_generation()
        self.refresh_cells()

        if Config.DEBUG:
            self.timeline_slider.setValue(self.game.current_index)

    def go_forward(self):
        self.timer.stop()

        # Si nous sommes à la fin → calcule une nouvelle génération
        if self.game.current_index == len(self.game.history) - 1:
            alive = self.game.next_generation()
            if alive is False:
                # grille morte → stopper
                return
        else:
            self.game.restore_state(self.game.current_index + 1)

        self.refresh_cells()

        if Config.DEBUG:
            self.timeline_slider.setMaximum(len(self.game.history) - 1)
            self.timeline_slider.setValue(self.game.current_index)


    # ============================================================
    #                GESTION DES PATTERNS
    # ============================================================

    def load_pattern(self, name):
        self.reset_grid()
        coords = self.pattern_manager.get_builtin_pattern(name)

        start_row = self.rows // 2 - 2
        start_col = self.cols // 2 - 2

        for r, c in coords:
            row = start_row + r
            col = start_col + c
            if 0 <= row < self.rows and 0 <= col < self.cols:
                self.cells[row][col].alive = True
                self.cells[row][col].update_color()
                self.game.set_cell(row, col, 1)

        self.refresh_cells()

    def save_pattern(self):
        coords = []
        for r, row in enumerate(self.cells):
            for c, cell in enumerate(row):
                if cell.alive:
                    coords.append((r, c))

        if not coords:
            return

        filename, _ = QFileDialog.getSaveFileName(
            self, "Sauvegarder Pattern",
            str(self.pattern_manager.data_dir),
            "JSON Files (*.json)"
        )

        if filename:
            self.pattern_manager.save_pattern(coords, Path(filename).name)

    def load_pattern_file(self):
        saved = self.pattern_manager.list_saved_patterns()
        if not saved:
            return

        filename, _ = QFileDialog.getOpenFileName(
            self, "Charger Pattern",
            str(self.pattern_manager.data_dir),
            "JSON Files (*.json)"
        )

        if filename:
            coords = self.pattern_manager.load_pattern(Path(filename).name)
            self.reset_grid()

            for r, c in coords:
                if 0 <= r < self.rows and 0 <= c < self.cols:
                    self.cells[r][c].alive = True
                    self.cells[r][c].update_color()
                    self.game.set_cell(r, c, 1)

            self.refresh_cells()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
