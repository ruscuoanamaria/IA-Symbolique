# IA-Symbolique
---- Explications ----

Pour ce projet nous avons d'abord créé une structure pour pouvoir représenter un jeu complet.
Nous utilisons des matrices (listes de listes) et des objets.

Dans le cas des matrices, chaque liste représente un pique. Elles sont utilisées comme des piles, ainsi le dernier élément de la liste est le sommet du pique, et donc le cube accessible sur celui-ci. Chaque cube est représenté par un numéro unique.

Dans le cas des objets, nous avons un objet rumba, ayant comme argument game, qui est une liste d'objet pikes (pique). Chaque pike contient lui-même un attribut cubes qui est une liste d'objet cube. Avec l'approche orientée objet, nous pouvons créer nos propres méthodes, et facilement prendre en compte l'ajout de poids différents pour chaque cube.

L'algorithme ida* est implémenté avec la fonction idaStarSearch. Le pseudo code a été adapté pour notre situation avec différentes fonctions crées pour le bon fonctionnement des recherches.
