"""
Module principal du jeu - Gère la boucle de jeu
"""
import math
import pygame
import sys
import config
from cible import Cible
from interface_fin import InterfaceFin


class Jeu:
    """Classe principale gérant le jeu"""
    
    def __init__(self, ecran):
        """
        Initialise le jeu
        
        Args:
            ecran: Surface pygame de la fenêtre (déjà créée)
        """
        self.ecran = ecran
        
        # Positionner le curseur au centre du cercle au démarrage du jeu
        pygame.mouse.set_pos(config.CURSEUR_X_APRES_CLIC, config.CURSEUR_Y_APRES_CLIC)
        
        # Position précédente du curseur pour détecter la traversée
        self.position_curseur_precedente = (config.CURSEUR_X_APRES_CLIC, config.CURSEUR_Y_APRES_CLIC)
        
        # Créer la cible initiale
        self.cible = Cible(
            config.POSITION_X_INITIALE,
            config.POSITION_Y_INITIALE,
            config.RAYON_CIBLE
        )
        # Positionner immédiatement la cible sur le cercle pour varier les apparitions
        self.cible.generer_nouvelle_position_sur_cercle()
        
        # Compteur de cibles
        self.nombre_cibles = 1  # On commence à 1 car on a déjà créé la première cible
        
        # État du jeu
        self.running = True
        self.en_affichage_resultat = False
        self.temps_debut_resultat = 0
        self.point_traversee = None  # Point (x, y) où le curseur a traversé la ligne
        self.cible_precedente = None  # Position de la cible précédente pour l'affichage
        self.fin_de_partie = False  # Indique si on a atteint le nombre max de cibles
        
        # Interface de fin de partie
        self.interface_fin = InterfaceFin(ecran)
    
    def gerer_evenements(self):
        """Gère les événements du jeu"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1 and self.fin_de_partie:  # Clic gauche pendant la fin de partie
                    action = self.interface_fin.gerer_clic(event.pos)
                    if action == "recommencer":
                        self.reinitialiser_jeu()
                    elif action == "quitter":
                        self.running = False
                    # action == "recuperer_donnees" ne fait rien pour le moment
    
    def detecter_traversee_cercle(self, position_actuelle):
        """
        Détecte si le curseur a traversé le cercle imaginaire
        
        Args:
            position_actuelle: Tuple (x, y) de la position actuelle du curseur
            
        Returns:
            Tuple (x, y) du point de traversée si traversée détectée, None sinon
        """
        if self.en_affichage_resultat:
            return None
        
        x0, y0 = self.position_curseur_precedente
        x1, y1 = position_actuelle
        if x0 == x1 and y0 == y1:
            return None
        
        cx, cy = config.CERCLE_CENTRE_X, config.CERCLE_CENTRE_Y
        r = config.CERCLE_RAYON
        
        dx = x1 - x0
        dy = y1 - y0
        fx = x0 - cx
        fy = y0 - cy
        
        a = dx * dx + dy * dy
        if a == 0:
            return None
        b = 2 * (fx * dx + fy * dy)
        c = fx * fx + fy * fy - r * r
        
        discriminant = b * b - 4 * a * c
        if discriminant < 0:
            return None
        
        sqrt_disc = math.sqrt(discriminant)
        t1 = (-b - sqrt_disc) / (2 * a)
        t2 = (-b + sqrt_disc) / (2 * a)
        
        for t in sorted((t1, t2)):
            if 0 <= t <= 1:
                x_traversee = x0 + t * dx
                y_traversee = y0 + t * dy
                return (int(x_traversee), int(y_traversee))
        
        return None
    
    def gerer_traversee(self, point_traversee):
        """
        Gère la traversée de la ligne par le curseur
        
        Args:
            point_traversee: Tuple (x, y) du point de traversée
        """
        # Sauvegarder la position de la cible actuelle
        self.cible_precedente = (self.cible.x, self.cible.y)
        
        # Sauvegarder le point de traversée
        self.point_traversee = point_traversee
        
        # Activer l'affichage du résultat
        self.en_affichage_resultat = True
        self.temps_debut_resultat = pygame.time.get_ticks()
        
        print(f"Traversée détectée au point: x={point_traversee[0]}, y={point_traversee[1]}")
        print(f"Cible était à: x={self.cible_precedente[0]}, y={self.cible_precedente[1]}")
    
    def mettre_a_jour(self):
        """Met à jour l'état du jeu"""
        # Si fin de partie, ne pas mettre à jour le jeu
        if self.fin_de_partie:
            return
        
        # Obtenir la position actuelle du curseur
        position_actuelle = pygame.mouse.get_pos()
        
        # Détecter la traversée du cercle
        point_traversee = self.detecter_traversee_cercle(position_actuelle)
        if point_traversee:
            self.gerer_traversee(point_traversee)
        
        # Mettre à jour la position précédente
        self.position_curseur_precedente = position_actuelle
        
        # Vérifier si on doit terminer l'affichage du résultat
        if self.en_affichage_resultat:
            temps_ecoule = pygame.time.get_ticks() - self.temps_debut_resultat
            if temps_ecoule >= config.DUREE_AFFICHAGE_RESULTAT:
                # Vérifier si on a atteint le nombre maximum de cibles
                if self.nombre_cibles >= config.NOMBRE_CIBLES_MAX:
                    self.fin_de_partie = True
                else:
                    # Générer une nouvelle cible sur le cercle
                    self.cible.generer_nouvelle_position_sur_cercle()
                    self.nombre_cibles += 1
                    print(f"Nouvelle cible à la position: x={self.cible.x}, y={self.cible.y}")
                    
                    # Réinitialiser l'état
                    self.en_affichage_resultat = False
                    self.point_traversee = None
                    self.cible_precedente = None
                    
                    # Repositionner le curseur au centre du cercle
                    pygame.mouse.set_pos(config.CURSEUR_X_APRES_CLIC, config.CURSEUR_Y_APRES_CLIC)
                    self.position_curseur_precedente = (config.CURSEUR_X_APRES_CLIC, config.CURSEUR_Y_APRES_CLIC)
    
    def dessiner(self):
        """Dessine tous les éléments du jeu"""
        # Remplir l'écran avec le fond
        self.ecran.fill(config.BLEU_CIEL)
        # Dessiner le cercle imaginaire (visible provisoirement)
        pygame.draw.circle(
            self.ecran,
            config.NOIR,
            (config.CERCLE_CENTRE_X, config.CERCLE_CENTRE_Y),
            config.CERCLE_RAYON,
            2
        )
        
        if self.en_affichage_resultat:
            # Mode affichage du résultat : afficher le point de traversée et la cible précédente
            if self.point_traversee:
                # Dessiner un point visible à l'endroit de la traversée
                pygame.draw.circle(self.ecran, config.VERT, self.point_traversee, 8)
                pygame.draw.circle(self.ecran, config.NOIR, self.point_traversee, 8, 2)
            
            # Dessiner la cible précédente (fantôme)
            if self.cible_precedente:
                cible_fantome = Cible(
                    self.cible_precedente[0],
                    self.cible_precedente[1],
                    config.RAYON_CIBLE
                )
                # Dessiner avec transparence (en gris clair)
                cible_fantome.dessiner_fantome(self.ecran)
        else:
            # Mode normal : dessiner la cible actuelle
            self.cible.dessiner(self.ecran)
        
        # Si fin de partie, dessiner l'interface
        if self.fin_de_partie:
            self.interface_fin.dessiner()
    
    def boucle_principale(self):
        """Boucle principale du jeu"""
        clock = pygame.time.Clock()
        
        while self.running:
            self.gerer_evenements()
            self.mettre_a_jour()
            self.dessiner()
            pygame.display.flip()
            clock.tick(60)  # Limiter à 60 FPS
        
        # Quitter pygame
        pygame.quit()
        sys.exit()
    
    def reinitialiser_jeu(self):
        """Réinitialise le jeu pour recommencer"""
        # Réinitialiser le compteur
        self.nombre_cibles = 1
        
        # Réinitialiser l'état
        self.en_affichage_resultat = False
        self.point_traversee = None
        self.cible_precedente = None
        self.fin_de_partie = False
        
        # Générer une nouvelle cible
        self.cible.generer_nouvelle_position_sur_cercle()
        
        # Repositionner le curseur au centre
        pygame.mouse.set_pos(config.CURSEUR_X_APRES_CLIC, config.CURSEUR_Y_APRES_CLIC)
        self.position_curseur_precedente = (config.CURSEUR_X_APRES_CLIC, config.CURSEUR_Y_APRES_CLIC)
