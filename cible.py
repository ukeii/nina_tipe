"""
Module pour gérer la cible du jeu
"""
import math
import pygame
import random
import config

# 8 positions fixes sur le cercle, tous les 45° (0°, 45°, 90°, ..., 315°)
# En radians, angle 0 = droite (3h), sens trigonométrique
ANGLES_POSITIONS_FIXES = [i * (2 * math.pi / 8) for i in range(8)]


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
        # File des indices (0..7) pour le bloc de 8 en cours ; vidée au redémarrage
        self._indices_restants = []
    
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
    
    def reinitialiser_sequence(self):
        """Vide la file des positions (à appeler au redémarrage d'une partie)."""
        self._indices_restants = []

    def generer_nouvelle_position_sur_cercle(self):
        """
        Positionne la cible sur une des 8 positions fixes du cercle (tous les 45°).
        Toutes les 8 apparitions, chaque position est utilisée exactement une fois,
        l'ordre parmi les 8 étant aléatoire.
        """
        if not self._indices_restants:
            self._indices_restants = list(range(8))
            random.shuffle(self._indices_restants)
        index = self._indices_restants.pop()
        angle = ANGLES_POSITIONS_FIXES[index]
        self.x = int(config.CERCLE_CENTRE_X + config.CERCLE_RAYON * math.cos(angle))
        self.y = int(config.CERCLE_CENTRE_Y + config.CERCLE_RAYON * math.sin(angle))

