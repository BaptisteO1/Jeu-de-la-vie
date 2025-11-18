from core.game import GameOfLife


def test_initial_grid_is_empty():
    """La grille doit être vide au départ."""
    game = GameOfLife(5, 5)
    assert all(cell == 0 for row in game.grid for cell in row)


def test_set_cell_changes_state():
    """set_cell() doit activer ou désactiver une cellule."""
    game = GameOfLife(3, 3)
    game.set_cell(1, 1, 1)
    assert game.grid[1][1] == 1
    game.set_cell(1, 1, 0)
    assert game.grid[1][1] == 0


def test_count_neighbors():
    """Test du comptage des voisins vivants."""
    game = GameOfLife(3, 3)
    game.set_cell(0, 1, 1)
    game.set_cell(1, 0, 1)
    game.set_cell(1, 2, 1)
    assert game.count_neighbors(1, 1) == 3
    assert game.count_neighbors(0, 0) == 2


def test_blinker_pattern():
    """Test du pattern oscillateur 'blinker'."""
    game = GameOfLife(5, 5)
    # État initial (horizontal)
    game.set_cell(2, 1, 1)
    game.set_cell(2, 2, 1)
    game.set_cell(2, 3, 1)
    # Première génération : devrait devenir vertical
    game.next_generation()
    expected = [
        [0, 0, 0, 0, 0],
        [0, 0, 1, 0, 0],
        [0, 0, 1, 0, 0],
        [0, 0, 1, 0, 0],
        [0, 0, 0, 0, 0],
    ]
    assert game.grid == expected
