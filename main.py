"""
Point d'entrée principal du jeu
"""
import pygame
import sys
from menu import Menu
from jeu import Jeu
import config

if __name__ == "__main__":
    # Initialiser pygame
    pygame.init()
    
    # Obtenir les dimensions de l'écran et mettre à jour config
    config.LARGEUR, config.HAUTEUR = config.obtenir_dimensions_ecran()
    
    # Définir le cercle imaginaire (centré et proportionnel à l'écran)
    config.CERCLE_CENTRE_X = config.LARGEUR // 2
    config.CERCLE_CENTRE_Y = config.HAUTEUR // 2
    config.CERCLE_RAYON = int(min(config.LARGEUR, config.HAUTEUR) * 0.35)
    
    # Mettre à jour les positions liées au cercle
    config.POSITION_X_INITIALE = config.CERCLE_CENTRE_X + config.CERCLE_RAYON
    config.POSITION_Y_INITIALE = config.CERCLE_CENTRE_Y
    config.CURSEUR_X_APRES_CLIC = config.CERCLE_CENTRE_X
    config.CURSEUR_Y_APRES_CLIC = config.CERCLE_CENTRE_Y
    
    # Créer la fenêtre en plein écran
    ecran = pygame.display.set_mode((config.LARGEUR, config.HAUTEUR), pygame.FULLSCREEN)
    pygame.display.set_caption("Jeu de Cible")
    
    # Afficher le menu
    menu = Menu(ecran)
    demarrer_jeu = menu.boucle_menu()
    
    # Si l'utilisateur a cliqué sur Start, lancer le jeu
    if demarrer_jeu:
        jeu = Jeu(ecran)
        jeu.boucle_principale()
    else:
        # Quitter pygame
        pygame.quit()
        sys.exit()

