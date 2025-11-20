"""
Configuration du jeu - Constantes et paramètres
"""
import pygame

def obtenir_dimensions_ecran():
    """Obtient les dimensions de l'écran"""
    info_ecran = pygame.display.Info()
    return info_ecran.current_w, info_ecran.current_h

# Dimensions de la fenêtre (seront définies après l'initialisation de pygame)
LARGEUR = 1920  # Valeur par défaut, sera mise à jour
HAUTEUR = 1080  # Valeur par défaut, sera mise à jour

# Paramètres du cercle imaginaire (définis après l'initialisation)
CERCLE_CENTRE_X = None
CERCLE_CENTRE_Y = None
CERCLE_RAYON = None

# Couleurs
BLANC = (255, 255, 255)
ROUGE = (255, 0, 0)
ROUGE_FONCE = (139, 0, 0)
NOIR = (0, 0, 0)
BLEU_CIEL = (135, 206, 235)  # Couleur de fond
VERT = (0, 255, 0)  # Couleur pour le point de traversée

# Paramètres de la cible
RAYON_CIBLE = 50
# POSITION_Y_INITIALE, POSITION_X_INITIALE, CURSEUR_X_APRES_CLIC, CURSEUR_Y_APRES_CLIC
# seront calculées dans main.py après avoir obtenu les dimensions de l'écran
POSITION_Y_INITIALE = None  # Sera calculée
POSITION_X_INITIALE = None  # Sera calculée
CURSEUR_X_APRES_CLIC = None  # Sera calculée
CURSEUR_Y_APRES_CLIC = None  # Sera calculée

# Durée d'affichage du résultat (en millisecondes)
DUREE_AFFICHAGE_RESULTAT = 500

