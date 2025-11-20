"""
Module pour gérer le menu de démarrage
"""
import pygame
import config


class Menu:
    """Classe gérant le menu de démarrage"""
    
    def __init__(self, ecran):
        """
        Initialise le menu
        
        Args:
            ecran: Surface pygame de la fenêtre
        """
        self.ecran = ecran
        # Ajuster les tailles de police selon la taille de l'écran
        taille_titre = int(config.HAUTEUR * 0.12)
        taille_bouton = int(config.HAUTEUR * 0.08)
        self.font_titre = pygame.font.Font(None, taille_titre)
        self.font_bouton = pygame.font.Font(None, taille_bouton)
        
        # Dimensions du bouton Start (proportionnelles à l'écran)
        self.bouton_largeur = int(config.LARGEUR * 0.25)
        self.bouton_hauteur = int(config.HAUTEUR * 0.1)
        self.bouton_x = config.LARGEUR // 2 - self.bouton_largeur // 2
        self.bouton_y = config.HAUTEUR // 2 + int(config.HAUTEUR * 0.08)
    
    def dessiner(self):
        """Dessine le menu"""
        # Fond
        self.ecran.fill(config.BLEU_CIEL)
        
        # Titre
        titre = self.font_titre.render("Jeu de Cible", True, config.NOIR)
        titre_rect = titre.get_rect(center=(config.LARGEUR // 2, config.HAUTEUR // 2 - 100))
        self.ecran.blit(titre, titre_rect)
        
        # Bouton Start
        bouton_rect = pygame.Rect(
            self.bouton_x,
            self.bouton_y,
            self.bouton_largeur,
            self.bouton_hauteur
        )
        pygame.draw.rect(self.ecran, config.ROUGE, bouton_rect)
        pygame.draw.rect(self.ecran, config.NOIR, bouton_rect, 3)
        
        # Texte du bouton
        texte_bouton = self.font_bouton.render("START", True, config.BLANC)
        texte_rect = texte_bouton.get_rect(center=bouton_rect.center)
        self.ecran.blit(texte_bouton, texte_rect)
    
    def est_sur_bouton(self, position):
        """
        Vérifie si la position est sur le bouton Start
        
        Args:
            position: Tuple (x, y) de la position
            
        Returns:
            True si la position est sur le bouton, False sinon
        """
        x, y = position
        bouton_rect = pygame.Rect(
            self.bouton_x,
            self.bouton_y,
            self.bouton_largeur,
            self.bouton_hauteur
        )
        return bouton_rect.collidepoint(x, y)
    
    def est_clique_sur_bouton(self, position_clic):
        """
        Vérifie si le clic est sur le bouton Start
        
        Args:
            position_clic: Tuple (x, y) de la position du clic
            
        Returns:
            True si le clic est sur le bouton, False sinon
        """
        return self.est_sur_bouton(position_clic)
    
    def boucle_menu(self):
        """
        Affiche le menu et attend un clic sur Start
        
        Returns:
            True si le jeu doit démarrer, False pour quitter
        """
        running = True
        
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        return False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  # Clic gauche
                        if self.est_clique_sur_bouton(event.pos):
                            return True
            
            # Gérer le curseur au survol du bouton
            position_souris = pygame.mouse.get_pos()
            if self.est_sur_bouton(position_souris):
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
            else:
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
            
            self.dessiner()
            pygame.display.flip()
        
        return False

