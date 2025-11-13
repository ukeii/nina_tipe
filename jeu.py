"""
Module principal du jeu - Gère la boucle de jeu
"""
import pygame
import sys
import config
from cible import Cible


class Jeu:
    """Classe principale gérant le jeu"""
    
    def __init__(self, ecran):
        """
        Initialise le jeu
        
        Args:
            ecran: Surface pygame de la fenêtre (déjà créée)
        """
        self.ecran = ecran
        
        # Positionner le curseur en bas de la fenêtre au démarrage du jeu
        pygame.mouse.set_pos(config.CURSEUR_X_APRES_CLIC, config.CURSEUR_Y_APRES_CLIC)
        
        # Position précédente du curseur pour détecter la traversée
        self.position_curseur_precedente = (config.CURSEUR_X_APRES_CLIC, config.CURSEUR_Y_APRES_CLIC)
        
        # Créer la cible initiale
        self.cible = Cible(
            config.POSITION_X_INITIALE,
            config.POSITION_Y_INITIALE,
            config.RAYON_CIBLE
        )
        
        # État du jeu
        self.running = True
        self.en_affichage_resultat = False
        self.temps_debut_resultat = 0
        self.point_traversee = None  # Point (x, y) où le curseur a traversé la ligne
        self.cible_precedente = None  # Position de la cible précédente pour l'affichage
    
    def gerer_evenements(self):
        """Gère les événements du jeu"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
    
    def detecter_traversee_ligne(self, position_actuelle):
        """
        Détecte si le curseur a traversé la ligne horizontale au niveau de la cible
        
        Args:
            position_actuelle: Tuple (x, y) de la position actuelle du curseur
            
        Returns:
            Tuple (x, y) du point de traversée si traversée détectée, None sinon
        """
        if self.en_affichage_resultat:
            return None
        
        x_actuel, y_actuel = position_actuelle
        x_precedent, y_precedent = self.position_curseur_precedente
        y_ligne = self.cible.y
        
        # Vérifier si le curseur a traversé la ligne horizontale
        # Le curseur démarre en bas, donc on détecte principalement quand il monte au-dessus
        if y_precedent != y_actuel:  # Éviter division par zéro
            # Cas 1: Le curseur monte et traverse la ligne (de bas en haut)
            if y_precedent > y_ligne and y_actuel <= y_ligne:
                # Calculer le point exact de traversée (interpolation linéaire)
                t = (y_ligne - y_precedent) / (y_actuel - y_precedent)
                x_traversee = x_precedent + t * (x_actuel - x_precedent)
                return (int(x_traversee), int(y_ligne))
            # Cas 2: Le curseur descend et traverse la ligne (de haut en bas)
            elif y_precedent < y_ligne and y_actuel >= y_ligne:
                # Calculer le point exact de traversée (interpolation linéaire)
                t = (y_ligne - y_precedent) / (y_actuel - y_precedent)
                x_traversee = x_precedent + t * (x_actuel - x_precedent)
                return (int(x_traversee), int(y_ligne))
        
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
        # Obtenir la position actuelle du curseur
        position_actuelle = pygame.mouse.get_pos()
        
        # Détecter la traversée de la ligne
        point_traversee = self.detecter_traversee_ligne(position_actuelle)
        if point_traversee:
            self.gerer_traversee(point_traversee)
        
        # Mettre à jour la position précédente
        self.position_curseur_precedente = position_actuelle
        
        # Vérifier si on doit terminer l'affichage du résultat
        if self.en_affichage_resultat:
            temps_ecoule = pygame.time.get_ticks() - self.temps_debut_resultat
            if temps_ecoule >= config.DUREE_AFFICHAGE_RESULTAT:
                # Générer une nouvelle cible
                self.cible.generer_nouvelle_position_x()
                print(f"Nouvelle cible à la position: x={self.cible.x}, y={self.cible.y}")
                
                # Réinitialiser l'état
                self.en_affichage_resultat = False
                self.point_traversee = None
                self.cible_precedente = None
                
                # Repositionner le curseur en bas de la fenêtre
                pygame.mouse.set_pos(config.CURSEUR_X_APRES_CLIC, config.CURSEUR_Y_APRES_CLIC)
                self.position_curseur_precedente = (config.CURSEUR_X_APRES_CLIC, config.CURSEUR_Y_APRES_CLIC)
    
    def dessiner(self):
        """Dessine tous les éléments du jeu"""
        # Remplir l'écran avec le fond
        self.ecran.fill(config.BLEU_CIEL)
        
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
