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
        
        # Dimensions des boutons (proportionnelles à l'écran)
        self.bouton_largeur = int(config.LARGEUR * 0.25)
        self.bouton_hauteur = int(config.HAUTEUR * 0.1)
        self.bouton_x = config.LARGEUR // 2 - self.bouton_largeur // 2
        self.bouton_y_start = config.HAUTEUR // 2 + int(config.HAUTEUR * 0.08)
        self.espacement_boutons = int(config.HAUTEUR * 0.05)
        self.bouton_y_config = self.bouton_y_start + self.bouton_hauteur + self.espacement_boutons
    
    def dessiner(self):
        """Dessine le menu"""
        # Fond
        self.ecran.fill(config.BLEU_CIEL)
        
        # Titre
        titre = self.font_titre.render("Jeu de Cible", True, config.NOIR)
        titre_rect = titre.get_rect(center=(config.LARGEUR // 2, config.HAUTEUR // 2 - 100))
        self.ecran.blit(titre, titre_rect)
        
        # Bouton Start
        bouton_start_rect = pygame.Rect(
            self.bouton_x,
            self.bouton_y_start,
            self.bouton_largeur,
            self.bouton_hauteur
        )
        pygame.draw.rect(self.ecran, config.ROUGE, bouton_start_rect)
        pygame.draw.rect(self.ecran, config.NOIR, bouton_start_rect, 3)
        
        # Texte du bouton Start
        texte_start = self.font_bouton.render("START", True, config.BLANC)
        texte_rect = texte_start.get_rect(center=bouton_start_rect.center)
        self.ecran.blit(texte_start, texte_rect)
        
        # Bouton Config
        bouton_config_rect = pygame.Rect(
            self.bouton_x,
            self.bouton_y_config,
            self.bouton_largeur,
            self.bouton_hauteur
        )
        pygame.draw.rect(self.ecran, (100, 100, 200), bouton_config_rect)  # Bleu
        pygame.draw.rect(self.ecran, config.NOIR, bouton_config_rect, 3)
        
        # Texte du bouton Config
        texte_config = self.font_bouton.render("CONFIG", True, config.BLANC)
        texte_rect = texte_config.get_rect(center=bouton_config_rect.center)
        self.ecran.blit(texte_config, texte_rect)
    
    def est_sur_bouton(self, position):
        """
        Vérifie si la position est sur un des boutons
        
        Args:
            position: Tuple (x, y) de la position
            
        Returns:
            "start", "config" ou None
        """
        x, y = position
        bouton_start_rect = pygame.Rect(
            self.bouton_x,
            self.bouton_y_start,
            self.bouton_largeur,
            self.bouton_hauteur
        )
        bouton_config_rect = pygame.Rect(
            self.bouton_x,
            self.bouton_y_config,
            self.bouton_largeur,
            self.bouton_hauteur
        )
        
        if bouton_start_rect.collidepoint(x, y):
            return "start"
        elif bouton_config_rect.collidepoint(x, y):
            return "config"
        return None
    
    def est_clique_sur_bouton(self, position_clic):
        """
        Vérifie si le clic est sur le bouton Start
        
        Args:
            position_clic: Tuple (x, y) de la position du clic
            
        Returns:
            "start" si clic sur Start, None sinon
        """
        resultat = self.est_sur_bouton(position_clic)
        return resultat == "start"
    
    def boucle_menu(self):
        """
        Affiche le menu et attend un clic sur Start ou Config
        
        Returns:
            True si le jeu doit démarrer, False pour quitter
        """
        from interface_config import InterfaceConfig
        
        running = True
        interface_config = None
        
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return False
                elif event.type == pygame.KEYDOWN:
                    if interface_config:
                        # Gérer les événements de l'interface de config
                        resultat = interface_config.gerer_evenement(event)
                        if resultat == "sauvegarder":
                            if interface_config.sauvegarder_config():
                                interface_config = None
                            # Sinon, rester dans l'interface (erreur de validation)
                        elif resultat == "annuler":
                            interface_config = None
                    elif event.key == pygame.K_ESCAPE:
                        if interface_config:
                            interface_config = None
                        else:
                            return False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  # Clic gauche
                        if interface_config:
                            # Gérer les événements de l'interface de config
                            resultat = interface_config.gerer_evenement(event)
                            if resultat == "sauvegarder":
                                if interface_config.sauvegarder_config():
                                    interface_config = None
                            elif resultat == "annuler":
                                interface_config = None
                        else:
                            # Vérifier les boutons du menu
                            bouton = self.est_sur_bouton(event.pos)
                            if bouton == "start":
                                return True
                            elif bouton == "config":
                                interface_config = InterfaceConfig(self.ecran)
            
            # Gérer le curseur au survol des boutons
            if not interface_config:
                position_souris = pygame.mouse.get_pos()
                if self.est_sur_bouton(position_souris):
                    pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
                else:
                    pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
            
            self.dessiner()
            if interface_config:
                interface_config.dessiner()
            pygame.display.flip()
        
        return False

