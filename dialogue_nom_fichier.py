"""
Module pour afficher un dialogue demandant le nom du fichier PDF
"""
import pygame
import config
import string


class DialogueNomFichier:
    """Classe pour afficher un dialogue de saisie de nom de fichier"""
    
    def __init__(self, ecran):
        """
        Initialise le dialogue
        
        Args:
            ecran: Surface pygame de la fenêtre
        """
        self.ecran = ecran
        self.texte_saisi = ""
        self.actif = True
        
        # Dimensions de la fenêtre de dialogue
        self.largeur_dialogue = int(config.LARGEUR * 0.4)
        self.hauteur_dialogue = int(config.HAUTEUR * 0.2)
        self.x_dialogue = (config.LARGEUR - self.largeur_dialogue) // 2
        self.y_dialogue = (config.HAUTEUR - self.hauteur_dialogue) // 2
        
        # Zone de saisie
        self.hauteur_champ = int(self.hauteur_dialogue * 0.3)
        self.x_champ = self.x_dialogue + int(self.largeur_dialogue * 0.1)
        self.y_champ = self.y_dialogue + int(self.hauteur_dialogue * 0.4)
        self.largeur_champ = int(self.largeur_dialogue * 0.8)
        
        # Boutons
        self.hauteur_bouton = int(self.hauteur_dialogue * 0.25)
        self.largeur_bouton = int(self.largeur_dialogue * 0.3)
        self.y_bouton = self.y_dialogue + int(self.hauteur_dialogue * 0.65)
        
        # Bouton OK
        self.x_bouton_ok = self.x_dialogue + int(self.largeur_dialogue * 0.15)
        self.bouton_ok_rect = pygame.Rect(
            self.x_bouton_ok,
            self.y_bouton,
            self.largeur_bouton,
            self.hauteur_bouton
        )
        
        # Bouton Annuler
        self.x_bouton_annuler = self.x_dialogue + int(self.largeur_dialogue * 0.55)
        self.bouton_annuler_rect = pygame.Rect(
            self.x_bouton_annuler,
            self.y_bouton,
            self.largeur_bouton,
            self.hauteur_bouton
        )
        
        # Police
        taille_titre = int(config.HAUTEUR * 0.05)
        taille_texte = int(config.HAUTEUR * 0.04)
        self.font_titre = pygame.font.Font(None, taille_titre)
        self.font_texte = pygame.font.Font(None, taille_texte)
    
    def dessiner(self):
        """Dessine le dialogue"""
        # Overlay semi-transparent
        overlay = pygame.Surface((config.LARGEUR, config.HAUTEUR))
        overlay.set_alpha(180)
        overlay.fill(config.NOIR)
        self.ecran.blit(overlay, (0, 0))
        
        # Fond du dialogue
        dialogue_rect = pygame.Rect(
            self.x_dialogue,
            self.y_dialogue,
            self.largeur_dialogue,
            self.hauteur_dialogue
        )
        pygame.draw.rect(self.ecran, config.BLANC, dialogue_rect)
        pygame.draw.rect(self.ecran, config.NOIR, dialogue_rect, 3)
        
        # Titre
        titre = self.font_titre.render("Nom du fichier PDF", True, config.NOIR)
        titre_rect = titre.get_rect(center=(config.LARGEUR // 2, self.y_dialogue + int(self.hauteur_dialogue * 0.15)))
        self.ecran.blit(titre, titre_rect)
        
        # Champ de saisie
        champ_rect = pygame.Rect(
            self.x_champ,
            self.y_champ,
            self.largeur_champ,
            self.hauteur_champ
        )
        pygame.draw.rect(self.ecran, config.BLANC, champ_rect)
        pygame.draw.rect(self.ecran, config.NOIR, champ_rect, 2)
        
        # Texte saisi
        texte_affiche = self.texte_saisi if self.texte_saisi else "Entrez un nom..."
        couleur_texte = config.NOIR if self.texte_saisi else (150, 150, 150)
        texte_surface = self.font_texte.render(texte_affiche, True, couleur_texte)
        # Limiter la largeur du texte affiché
        if texte_surface.get_width() > self.largeur_champ - 10:
            # Tronquer le texte avec "..."
            while texte_surface.get_width() > self.largeur_champ - 30:
                texte_affiche = texte_affiche[:-1]
                texte_surface = self.font_texte.render(texte_affiche + "...", True, couleur_texte)
        self.ecran.blit(texte_surface, (self.x_champ + 5, self.y_champ + (self.hauteur_champ - texte_surface.get_height()) // 2))
        
        # Curseur clignotant
        if pygame.time.get_ticks() % 1000 < 500:
            curseur_x = self.x_champ + 5 + texte_surface.get_width()
            pygame.draw.line(
                self.ecran,
                config.NOIR,
                (curseur_x, self.y_champ + 5),
                (curseur_x, self.y_champ + self.hauteur_champ - 5),
                2
            )
        
        # Bouton OK
        pygame.draw.rect(self.ecran, config.VERT, self.bouton_ok_rect)
        pygame.draw.rect(self.ecran, config.NOIR, self.bouton_ok_rect, 2)
        texte_ok = self.font_texte.render("OK", True, config.BLANC)
        texte_ok_rect = texte_ok.get_rect(center=self.bouton_ok_rect.center)
        self.ecran.blit(texte_ok, texte_ok_rect)
        
        # Bouton Annuler
        pygame.draw.rect(self.ecran, config.ROUGE, self.bouton_annuler_rect)
        pygame.draw.rect(self.ecran, config.NOIR, self.bouton_annuler_rect, 2)
        texte_annuler = self.font_texte.render("Annuler", True, config.BLANC)
        texte_annuler_rect = texte_annuler.get_rect(center=self.bouton_annuler_rect.center)
        self.ecran.blit(texte_annuler, texte_annuler_rect)
    
    def gerer_evenement(self, event):
        """
        Gère les événements du dialogue
        
        Args:
            event: Événement pygame
            
        Returns:
            "ok" si OK cliqué, "annuler" si Annuler cliqué, None sinon
        """
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:
                if self.texte_saisi:
                    return "ok"
            elif event.key == pygame.K_ESCAPE:
                return "annuler"
            elif event.key == pygame.K_BACKSPACE:
                self.texte_saisi = self.texte_saisi[:-1]
            else:
                # Ajouter le caractère si c'est un caractère valide pour un nom de fichier
                caractere = event.unicode
                if caractere and (caractere.isalnum() or caractere in "._- "):
                    self.texte_saisi += caractere
        
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Clic gauche
                if self.bouton_ok_rect.collidepoint(event.pos):
                    if self.texte_saisi:
                        return "ok"
                elif self.bouton_annuler_rect.collidepoint(event.pos):
                    return "annuler"
        
        return None
    
    def obtenir_nom_fichier(self):
        """
        Obtient le nom du fichier saisi (sans extension .pdf)
        
        Returns:
            Nom du fichier ou None si annulé
        """
        return self.texte_saisi.strip() if self.texte_saisi.strip() else None

