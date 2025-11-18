import os
import time
from core.game import GameOfLife


def clear_console():
    """Efface l’écran du terminal (compatible Windows / Linux / Mac)."""
    os.system('cls' if os.name == 'nt' else 'clear')


def main():
    # Crée une instance du jeu avec une grille 10x10
    game = GameOfLife(20, 20)

    # Exemple : un "oscillateur" (blinker)
    game.set_cell(4, 3, 1) #Active manuellement certaines cellules pour créer un pattern.
    game.set_cell(4, 4, 1)
    game.set_cell(4, 5, 1)

    # Exemple : un petit carré stable (bloc)
    game.set_cell(7, 3, 1)
    game.set_cell(7, 4, 1)
    game.set_cell(8, 3, 1)
    game.set_cell(8, 4, 1)

    # Boucle principale du jeu
    try:
        while True:
            clear_console() #Efface l’écran entre chaque génération pour l’effet “animation”.
            game.display() #Affiche la grille actuelle (. pour morts, ■ pour vivants).
            game.next_generation() #Calcule la génération suivante.
            time.sleep(0.5)  # Attends 0,5 secondes pour rendre l’animation fluide.
    except KeyboardInterrupt: #Permet d’arrêter avec Ctrl + C proprement.
        print("\nSimulation arrêtée par l’utilisateur.")


if __name__ == "__main__":
    main()
