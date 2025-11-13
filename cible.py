"""
Module pour gérer la cible du jeu
"""
import pygame
import random
import config


class Cible:
    """Classe représentant une cible dans le jeu"""
    
    def __init__(self, x, y, rayon):
        """
        Initialise une cible
        
        Args:
            x: Position x du centre de la cible
            y: Position y du centre de la cible
            rayon: Rayon de la cible
        """
        self.x = x
        self.y = y
        self.rayon = rayon
    
    def dessiner(self, surface):
        """
        Dessine la cible sur la surface
        
        Args:
            surface: Surface pygame sur laquelle dessiner
        """
        # Cercle extérieur (rouge)
        pygame.draw.circle(surface, config.ROUGE, (self.x, self.y), self.rayon)
        pygame.draw.circle(surface, config.ROUGE_FONCE, (self.x, self.y), self.rayon, 2)
        
        # Cercle moyen (blanc)
        rayon_moyen = int(self.rayon * 0.7)
        pygame.draw.circle(surface, config.BLANC, (self.x, self.y), rayon_moyen)
        pygame.draw.circle(surface, config.ROUGE_FONCE, (self.x, self.y), rayon_moyen, 2)
        
        # Cercle intérieur (rouge)
        rayon_interieur = int(self.rayon * 0.4)
        pygame.draw.circle(surface, config.ROUGE, (self.x, self.y), rayon_interieur)
        pygame.draw.circle(surface, config.ROUGE_FONCE, (self.x, self.y), rayon_interieur, 2)
        
        # Centre (noir)
        rayon_centre = max(3, int(self.rayon * 0.15))
        pygame.draw.circle(surface, config.NOIR, (self.x, self.y), rayon_centre)
    
    def dessiner_fantome(self, surface):
        """
        Dessine la cible en mode fantôme (gris clair) pour l'affichage du résultat
        
        Args:
            surface: Surface pygame sur laquelle dessiner
        """
        GRIS_FANTOME = (150, 150, 150)  # Couleur grise pour le fantôme
        
        # Cercle extérieur (gris)
        pygame.draw.circle(surface, GRIS_FANTOME, (self.x, self.y), self.rayon)
        pygame.draw.circle(surface, config.NOIR, (self.x, self.y), self.rayon, 2)
        
        # Cercle moyen (gris clair)
        rayon_moyen = int(self.rayon * 0.7)
        pygame.draw.circle(surface, (200, 200, 200), (self.x, self.y), rayon_moyen)
        pygame.draw.circle(surface, config.NOIR, (self.x, self.y), rayon_moyen, 2)
        
        # Cercle intérieur (gris)
        rayon_interieur = int(self.rayon * 0.4)
        pygame.draw.circle(surface, GRIS_FANTOME, (self.x, self.y), rayon_interieur)
        pygame.draw.circle(surface, config.NOIR, (self.x, self.y), rayon_interieur, 2)
        
        # Centre (noir)
        rayon_centre = max(3, int(self.rayon * 0.15))
        pygame.draw.circle(surface, config.NOIR, (self.x, self.y), rayon_centre)
    
    def est_clique(self, clic_x, clic_y):
        """
        Vérifie si un clic est dans la cible
        
        Args:
            clic_x: Position x du clic
            clic_y: Position y du clic
            
        Returns:
            True si le clic est dans la cible, False sinon
        """
        distance = ((clic_x - self.x) ** 2 + (clic_y - self.y) ** 2) ** 0.5
        return distance <= self.rayon
    
    def generer_nouvelle_position_x(self):
        """Génère une nouvelle position x aléatoire (y reste inchangé)"""
        self.x = random.randint(self.rayon, config.LARGEUR - self.rayon)

