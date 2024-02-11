import time
from collections import deque
import random


class Cell:
    def __init__(self):
        self.is_wall = True  # Booléen du mur : intact ou cassé
        self.visited = False  # Booléen de la visite ou non


# Fonction qui permet de voir si le mur de la case est cassé ou non.
def wall_intact(line, col, m):
    return m[line][col].is_wall


# Fonction de création du labyrinthe
def creation_labyrinthe(total_columns, total_lines):
    # Fonction qui permet de voir si la case est dans le labyrinthe.
    def in_maze(line, col):
        return 0 <= col < total_columns and 0 <= line < total_lines

    # Remplissage du labyrinthe avec des objets de type Cell.
    laby = [[Cell() for _ in range(total_columns)] for _ in range(total_lines)]

    # Cassage des murs de l'entrée et de la sortie.
    laby[1][0].is_wall = False
    laby[total_lines - 2][total_columns - 1].is_wall = False

    def create_path(current_l, current_c):
        # Cassage di mur de la case courante
        laby[current_l][current_c].is_wall = False
        directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]  # Droite, Haut, Gauche, Bas.
        # Mélange du tableau contenant les directions.
        random.shuffle(directions)
        # Parcours les cases voisines
        for direction_c, direction_l in directions:
            # x2 est nécessaire pour créer les couloirs sinon on a un labyrinthe imparfait.
            # x1 = Pas de mur.
            # x3 ou plus = Pas de chemin.
            # En résumée, on supprime le mur entre la case actuelle et la case choisie
            next_c = current_c + direction_c * 2
            next_l = current_l + direction_l * 2
            if in_maze(next_l, next_c) and wall_intact(next_l, next_c, laby):
                # Si la case n'est pas un mur donc on la creuse.
                # Exemple : si notre position est x,y = 3,3
                # et la direction est 1,0 (on va à l'est) alors 4,3 n'est plus un mur.
                laby[current_l + direction_l][current_c + direction_c].is_wall = False
                # Appel récursif avec les prochaines coordonnées.
                create_path(next_l, next_c)  #

    create_path(1, 1)  # Point de départ
    return laby


# Affichage du labyrinthe dans la console.
def affichage_labyrinthe(laby, current_position):
    line = len(laby)
    cols = len(laby[0])
    print("\n" + "------------------------------------------------------")
    for i in range(line):
        for j in range(cols):
            if (i, j) == current_position:
                print('\033[93m' + "." + '\033[0m', end=" ")  # Case actuelle (jaune).
            elif laby[i][j].is_wall:
                print("#", end=" ")  # Mur en blanc.
            else:
                if laby[i][j].visited:
                    print('\033[91m' + "." + '\033[0m', end=" ")  # Chemin visité (rouge).
                else:
                    print('\033[92m' + "." + '\033[0m', end=" ")  # Chemin non visité (vert).
        print()  # On revient à la ligne.
    time.sleep(0.5)  # Temps entre les affichages


def main_droite(laby):
    lines = len(laby)
    cols = len(laby[0])
    # Point de départ en haut à gauche.
    start = (1, 0)
    # Point d'arrivée en bas à droite.
    end = (lines - 2, cols - 1)
    #  Initialisation de la position actuelle avec les coordonnées de l'entrée
    current_position = start
    # Direction du haut par défaut
    current_direction = (0, 1)
    # Tant que la position actuelle n'est pas celle d'arrivée.
    while current_position != end:
        # Actualisation du booleen de visite de la case.
        laby[current_position[0]][current_position[1]].visited = True
        # Actuatlisation de la droite
        right_direction = (current_direction[1], -current_direction[0])
        # Initialisation de la case de droite en fonction de la position actuelle et de la direction actuelle.
        right_cell = (current_position[0] + right_direction[0], current_position[1] + right_direction[1])
        # S'il n'y a pas un mur à droite :
        if not wall_intact(right_cell[0], right_cell[1], laby):
            # On met à jour la rotation à droite et on avance
            current_direction = right_direction
            current_position = (current_position[0] + current_direction[0], current_position[1] + current_direction[1])
        # S'il y a pas de un mur en face et un mur à droite :
        elif not wall_intact(current_position[0] + current_direction[0], current_position[1] + current_direction[1],
                             laby):
            # On avance en face
            current_position = (current_position[0] + current_direction[0], current_position[1] + current_direction[1])
        else:  # S'il y a un mur à droite et en face, rotation de 180°.
            current_direction = (-current_direction[1], current_direction[0])
        # Affichage progressif du labyrinthe en fonction des cases visités ou non.
        affichage_labyrinthe(laby, current_position)
    # Mise à jour du booléen de la dernière case pour signifier qu'on l'a visité
    laby[lines - 2][cols - 1].visited = True
    # Dernier affichage
    affichage_labyrinthe(laby, current_position)
    print("Labyrinthe résolu!")


def matrix_distance(laby):
    lines = len(laby)
    cols = len(laby[0])
    # Remplissage de notre matrice avec des valeurs infinie pour chaque case.
    distances = [[float('inf')] * cols for _ in range(lines)]
    # Premier élement à 0.
    distances[0][0] = 0
    # Création d'une collection deque pour gérer la file des coordonnées sous forme de tuples
    coordinates = deque([(0, 0)])
    while coordinates:
        # On enlève chaque partie du tuple parcouru et on attribue ses élements à x et y
        x, y = coordinates.popleft()
        # Directions : Droite, Haut, Gauche, Bas.
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        # Parcours de la liste des directions.
        for direction_x, direction_y in directions:
            # Variables qui correspond à la case voisine selon la direction.
            x2 = x + direction_x
            y2 = y + direction_y
            # Tant que les coordonnées ne correspondent pas à un mur et est dans le labyrinthe.
            if 0 <= x2 < lines and 0 <= y2 < cols and not laby[x2][y2].is_wall:
                # Si la case de la matrice est égale à une valeur infinie.
                if distances[x2][y2] == float('inf'):
                    # On y ajoute la valeur de la case précédente +1. Cela correspond aux nombres de cases parcourues.
                    distances[x2][y2] = distances[x][y] + 1
                    # Ajout des coordonnées de la case suivante.
                    coordinates.append((x2, y2))
    return distances


def path_liste(matrix):
    lines = len(matrix)
    cols = len(matrix[0])
    path = []
    # Position actuelle = la sortie
    current_position = (lines - 2, cols - 1)
    # Tant que la position n'est pas arrivée au point de départ.
    while current_position != (0, 0):
        # Ajout des coordonnées de la position actuelle.
        path.append(current_position)
        # Attribution des coordonnées.
        x, y = current_position
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]  # Directions
        for direction_x, direction_y in directions:
            # Variables qui correspond à la case voisine selon la direction.
            x2 = x + direction_x
            y2 = y + direction_y
            # Il faut que les coordonnées x2 et y2 soit dans le labyrinthe, qu'elle ne correspondent pas à une valeur
            # infinie. Les coordonnées doivent être adjacentes à la case actuelle.
            # Sinon on regarde une autre direction jusqu'à qu'on trouve un voisin adéquat.
            if (0 <= x2 < lines and 0 <= y2 < cols and not matrix[x2][y2] == float('inf')
                    and matrix[x2][y2] == matrix[x][y] - 1):
                # Mise à jour de la position actuelle
                current_position = (x2, y2)
    # Ajout des oordonnées de la case départ
    path.append((0, 0))
    # Renvoi de la liste inversée
    return path[::-1]


# Instruction pour la génération
c_input = input("Veuillez choisir un nombre impair pour les colonnes : ")
l_input = input("Veuillez choisir un nombre impair pour les lignes : ")
total_col = int(c_input)
total_line = int(l_input)
# Warning
print("Selon les dimensions, l'affichage peut être brisé à cause de la résolution de l'écran de votre ordinateur.")
print("\n" + "Un nombre très élevé peut ne pas lancer les fonctions,(trop d'appel récursif)")
time.sleep(1.5)
# La graine aléatoire permet d'éviter la génération de la labyrinthe identique
random.seed()
# Création du labyrinthe
labyrinthe = creation_labyrinthe(total_col, total_line)
# Affichage du parcours avec la règle de la main droite
main_droite(labyrinthe)
# Matrice de la distance
liste_distance = matrix_distance(labyrinthe)
for a in liste_distance:
    print(a)
# Liste des coordonnées pour un parcours du labyrinthe optimal
pathlist = path_liste(liste_distance)
# Affichage de la liste des coordonnées
for b in pathlist:
    print(b, end=" ")
