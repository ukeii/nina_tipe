"""
Module pour gérer l'interface de fin de partie
"""
import pygame
import config


class InterfaceFin:
    """Classe gérant l'interface de fin de partie avec 3 boutons"""
    
    def __init__(self, ecran):
        """
        Initialise l'interface de fin
        
        Args:
            ecran: Surface pygame de la fenêtre
        """
        self.ecran = ecran
        
        # Ajuster les tailles de police selon la taille de l'écran
        taille_titre = int(config.HAUTEUR * 0.1)
        taille_bouton = int(config.HAUTEUR * 0.06)
        self.font_titre = pygame.font.Font(None, taille_titre)
        self.font_bouton = pygame.font.Font(None, taille_bouton)
        
        # Dimensions des boutons (proportionnelles à l'écran)
        self.bouton_largeur = int(config.LARGEUR * 0.2)
        self.bouton_hauteur = int(config.HAUTEUR * 0.08)
        espacement = int(config.HAUTEUR * 0.12)
        
        # Position du titre
        self.titre_y = int(config.HAUTEUR * 0.3)
        
        # Positions des boutons (centrés horizontalement, espacés verticalement)
        centre_x = config.LARGEUR // 2
        self.bouton_y_debut = int(config.HAUTEUR * 0.45)
        
        # Bouton "Récupérer les données"
        self.bouton_donnees_rect = pygame.Rect(
            centre_x - self.bouton_largeur // 2,
            self.bouton_y_debut,
            self.bouton_largeur,
            self.bouton_hauteur
        )
        
        # Bouton "Recommencer"
        self.bouton_recommencer_rect = pygame.Rect(
            centre_x - self.bouton_largeur // 2,
            self.bouton_y_debut + espacement,
            self.bouton_largeur,
            self.bouton_hauteur
        )
        
        # Bouton "Quitter"
        self.bouton_quitter_rect = pygame.Rect(
            centre_x - self.bouton_largeur // 2,
            self.bouton_y_debut + 2 * espacement,
            self.bouton_largeur,
            self.bouton_hauteur
        )
    
    def dessiner(self):
        """Dessine l'interface de fin de partie"""
        # Créer une surface semi-transparente pour l'overlay
        overlay = pygame.Surface((config.LARGEUR, config.HAUTEUR))
        overlay.set_alpha(200)
        overlay.fill(config.NOIR)
        self.ecran.blit(overlay, (0, 0))
        
        # Titre
        titre = self.font_titre.render("Partie terminée !", True, config.BLANC)
        titre_rect = titre.get_rect(center=(config.LARGEUR // 2, self.titre_y))
        self.ecran.blit(titre, titre_rect)
        
        # Bouton "Récupérer les données"
        pygame.draw.rect(self.ecran, config.VERT, self.bouton_donnees_rect)
        pygame.draw.rect(self.ecran, config.NOIR, self.bouton_donnees_rect, 3)
        texte_donnees = self.font_bouton.render("Données", True, config.BLANC)
        texte_rect = texte_donnees.get_rect(center=self.bouton_donnees_rect.center)
        self.ecran.blit(texte_donnees, texte_rect)
        
        # Bouton "Recommencer"
        pygame.draw.rect(self.ecran, config.ROUGE, self.bouton_recommencer_rect)
        pygame.draw.rect(self.ecran, config.NOIR, self.bouton_recommencer_rect, 3)
        texte_recommencer = self.font_bouton.render("Recommencer", True, config.BLANC)
        texte_rect = texte_recommencer.get_rect(center=self.bouton_recommencer_rect.center)
        self.ecran.blit(texte_recommencer, texte_rect)
        
        # Bouton "Quitter"
        pygame.draw.rect(self.ecran, config.ROUGE_FONCE, self.bouton_quitter_rect)
        pygame.draw.rect(self.ecran, config.NOIR, self.bouton_quitter_rect, 3)
        texte_quitter = self.font_bouton.render("Quitter", True, config.BLANC)
        texte_rect = texte_quitter.get_rect(center=self.bouton_quitter_rect.center)
        self.ecran.blit(texte_quitter, texte_rect)
    
    def est_sur_bouton(self, position):
        """
        Vérifie si la position est sur un des boutons
        
        Args:
            position: Tuple (x, y) de la position
            
        Returns:
            True si la position est sur un bouton, False sinon
        """
        x, y = position
        return (self.bouton_donnees_rect.collidepoint(x, y) or
                self.bouton_recommencer_rect.collidepoint(x, y) or
                self.bouton_quitter_rect.collidepoint(x, y))
    
    def gerer_clic(self, position_clic):
        """
        Gère les clics sur les boutons de l'interface
        
        Args:
            position_clic: Tuple (x, y) de la position du clic
            
        Returns:
            "recuperer_donnees", "recommencer", "quitter" ou None
        """
        clic_x, clic_y = position_clic
        
        if self.bouton_donnees_rect.collidepoint(clic_x, clic_y):
            # Pour le moment, ne fait rien mais retourne l'action
            return "recuperer_donnees"
        elif self.bouton_recommencer_rect.collidepoint(clic_x, clic_y):
            return "recommencer"
        elif self.bouton_quitter_rect.collidepoint(clic_x, clic_y):
            return "quitter"
        
        return None

