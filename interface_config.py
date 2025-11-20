"""
Module pour gérer l'interface de configuration
"""
import pygame
import config
import re


class InterfaceConfig:
    """Classe gérant l'interface de configuration"""
    
    def __init__(self, ecran):
        """
        Initialise l'interface de configuration
        
        Args:
            ecran: Surface pygame de la fenêtre
        """
        self.ecran = ecran
        
        # Ajuster les tailles de police
        taille_titre = int(config.HAUTEUR * 0.08)
        taille_label = int(config.HAUTEUR * 0.04)
        taille_champ = int(config.HAUTEUR * 0.035)
        self.font_titre = pygame.font.Font(None, taille_titre)
        self.font_label = pygame.font.Font(None, taille_label)
        self.font_champ = pygame.font.Font(None, taille_champ)
        
        # Dimensions de la fenêtre de configuration
        self.largeur_fen = int(config.LARGEUR * 0.5)
        self.hauteur_fen = int(config.HAUTEUR * 0.7)
        self.x_fen = (config.LARGEUR - self.largeur_fen) // 2
        self.y_fen = (config.HAUTEUR - self.hauteur_fen) // 2
        
        # Dimensions des champs
        self.hauteur_champ = int(config.HAUTEUR * 0.05)
        self.largeur_champ = int(self.largeur_fen * 0.4)
        self.espacement = int(config.HAUTEUR * 0.08)
        
        # Position du titre
        self.titre_y = self.y_fen + int(self.hauteur_fen * 0.05)
        
        # Champs de configuration
        self.champs = []
        self.champ_actif = None
        
        # Définir les champs avec leurs labels et valeurs initiales
        self.definitions_champs = [
            ("RAYON_CIBLE", "Rayon de la cible", config.RAYON_CIBLE),
            ("DUREE_AFFICHAGE_RESULTAT", "Durée affichage résultat (ms)", config.DUREE_AFFICHAGE_RESULTAT),
            ("NOMBRE_CIBLES_MAX", "Nombre de cibles max", config.NOMBRE_CIBLES_MAX),
            ("CIBLE_DEBUT_DEVIATION", "Cible début déviation", config.CIBLE_DEBUT_DEVIATION),
            ("ANGLE_DEVIATION", "Angle de déviation (°)", config.ANGLE_DEVIATION),
        ]
        
        # Initialiser les champs
        y_debut = self.titre_y + int(self.hauteur_fen * 0.12)
        for i, (nom, label, valeur) in enumerate(self.definitions_champs):
            y_champ = y_debut + i * self.espacement
            self.champs.append({
                'nom': nom,
                'label': label,
                'valeur': str(valeur),
                'x_label': self.x_fen + int(self.largeur_fen * 0.1),
                'y_label': y_champ,
                'x_champ': self.x_fen + int(self.largeur_fen * 0.5),
                'y_champ': y_champ,
                'rect': pygame.Rect(
                    self.x_fen + int(self.largeur_fen * 0.5),
                    y_champ,
                    self.largeur_champ,
                    self.hauteur_champ
                )
            })
        
        # Boutons
        self.hauteur_bouton = int(config.HAUTEUR * 0.06)
        self.largeur_bouton = int(self.largeur_fen * 0.25)
        self.y_bouton = self.y_fen + int(self.hauteur_fen * 0.85)
        
        # Bouton Sauvegarder
        self.bouton_sauvegarder_rect = pygame.Rect(
            self.x_fen + int(self.largeur_fen * 0.15),
            self.y_bouton,
            self.largeur_bouton,
            self.hauteur_bouton
        )
        
        # Bouton Annuler
        self.bouton_annuler_rect = pygame.Rect(
            self.x_fen + int(self.largeur_fen * 0.6),
            self.y_bouton,
            self.largeur_bouton,
            self.hauteur_bouton
        )
    
    def dessiner(self):
        """Dessine l'interface de configuration"""
        # Overlay semi-transparent
        overlay = pygame.Surface((config.LARGEUR, config.HAUTEUR))
        overlay.set_alpha(180)
        overlay.fill(config.NOIR)
        self.ecran.blit(overlay, (0, 0))
        
        # Fond de la fenêtre
        fen_rect = pygame.Rect(
            self.x_fen,
            self.y_fen,
            self.largeur_fen,
            self.hauteur_fen
        )
        pygame.draw.rect(self.ecran, config.BLANC, fen_rect)
        pygame.draw.rect(self.ecran, config.NOIR, fen_rect, 3)
        
        # Titre
        titre = self.font_titre.render("Configuration", True, config.NOIR)
        titre_rect = titre.get_rect(center=(config.LARGEUR // 2, self.titre_y))
        self.ecran.blit(titre, titre_rect)
        
        # Dessiner les champs
        for champ in self.champs:
            # Label
            label = self.font_label.render(champ['label'], True, config.NOIR)
            self.ecran.blit(label, (champ['x_label'], champ['y_label']))
            
            # Champ de saisie
            couleur_bordure = config.ROUGE if self.champ_actif == champ else config.NOIR
            pygame.draw.rect(self.ecran, config.BLANC, champ['rect'])
            pygame.draw.rect(self.ecran, couleur_bordure, champ['rect'], 2)
            
            # Texte dans le champ
            texte_affiche = champ['valeur']
            if self.champ_actif == champ and pygame.time.get_ticks() % 1000 < 500:
                texte_affiche += "|"  # Curseur clignotant
            
            texte_surface = self.font_champ.render(texte_affiche, True, config.NOIR)
            # Limiter la largeur du texte
            if texte_surface.get_width() > self.largeur_champ - 10:
                while texte_surface.get_width() > self.largeur_champ - 30:
                    texte_affiche = texte_affiche[:-1]
                    texte_surface = self.font_champ.render(texte_affiche + "...", True, config.NOIR)
            
            self.ecran.blit(texte_surface, (champ['rect'].x + 5, champ['rect'].y + (self.hauteur_champ - texte_surface.get_height()) // 2))
        
        # Bouton Sauvegarder
        pygame.draw.rect(self.ecran, config.VERT, self.bouton_sauvegarder_rect)
        pygame.draw.rect(self.ecran, config.NOIR, self.bouton_sauvegarder_rect, 2)
        texte_sauvegarder = self.font_label.render("Sauvegarder", True, config.BLANC)
        texte_rect = texte_sauvegarder.get_rect(center=self.bouton_sauvegarder_rect.center)
        self.ecran.blit(texte_sauvegarder, texte_rect)
        
        # Bouton Annuler
        pygame.draw.rect(self.ecran, config.ROUGE, self.bouton_annuler_rect)
        pygame.draw.rect(self.ecran, config.NOIR, self.bouton_annuler_rect, 2)
        texte_annuler = self.font_label.render("Annuler", True, config.BLANC)
        texte_rect = texte_annuler.get_rect(center=self.bouton_annuler_rect.center)
        self.ecran.blit(texte_annuler, texte_rect)
    
    def gerer_evenement(self, event):
        """
        Gère les événements de l'interface
        
        Args:
            event: Événement pygame
            
        Returns:
            "sauvegarder", "annuler" ou None
        """
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Clic gauche
                # Vérifier si on clique sur un champ
                for champ in self.champs:
                    if champ['rect'].collidepoint(event.pos):
                        self.champ_actif = champ
                        return None
                
                # Vérifier si on clique sur un bouton
                if self.bouton_sauvegarder_rect.collidepoint(event.pos):
                    return "sauvegarder"
                elif self.bouton_annuler_rect.collidepoint(event.pos):
                    return "annuler"
                
                # Clic ailleurs : désélectionner le champ actif
                self.champ_actif = None
        
        elif event.type == pygame.KEYDOWN:
            if self.champ_actif:
                if event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:
                    # Passer au champ suivant ou sauvegarder
                    return None
                elif event.key == pygame.K_TAB:
                    # Passer au champ suivant
                    index = self.champs.index(self.champ_actif)
                    self.champ_actif = self.champs[(index + 1) % len(self.champs)]
                    return None
                elif event.key == pygame.K_BACKSPACE:
                    self.champ_actif['valeur'] = self.champ_actif['valeur'][:-1]
                elif event.key == pygame.K_ESCAPE:
                    return "annuler"
                else:
                    # Ajouter le caractère si c'est un chiffre ou un signe moins
                    caractere = event.unicode
                    if caractere and (caractere.isdigit() or caractere == '-'):
                        self.champ_actif['valeur'] += caractere
        
        return None
    
    def obtenir_valeurs(self):
        """
        Obtient les valeurs des champs sous forme de dictionnaire
        
        Returns:
            Dictionnaire avec les valeurs (ou None si invalide)
        """
        valeurs = {}
        for champ in self.champs:
            try:
                valeur = int(champ['valeur'])
                # Vérifier les limites raisonnables
                if champ['nom'] == 'RAYON_CIBLE' and (valeur < 10 or valeur > 200):
                    return None
                elif champ['nom'] == 'DUREE_AFFICHAGE_RESULTAT' and (valeur < 100 or valeur > 5000):
                    return None
                elif champ['nom'] == 'NOMBRE_CIBLES_MAX' and (valeur < 1 or valeur > 100):
                    return None
                elif champ['nom'] == 'CIBLE_DEBUT_DEVIATION' and (valeur < 1 or valeur > 100):
                    return None
                elif champ['nom'] == 'ANGLE_DEVIATION' and (valeur < 0 or valeur > 180):
                    return None
                valeurs[champ['nom']] = valeur
            except ValueError:
                return None
        return valeurs
    
    def sauvegarder_config(self):
        """
        Sauvegarde les valeurs dans config.py
        
        Returns:
            True si sauvegarde réussie, False sinon
        """
        valeurs = self.obtenir_valeurs()
        if valeurs is None:
            return False
        
        try:
            # Lire le fichier config.py
            with open('config.py', 'r', encoding='utf-8') as f:
                lignes = f.readlines()
            
            # Modifier les lignes correspondantes
            for nom, valeur in valeurs.items():
                for i, ligne in enumerate(lignes):
                    # Chercher la ligne qui définit cette variable (sans les espaces en début)
                    if re.match(rf'^{nom}\s*=', ligne.strip()):
                        lignes[i] = f"{nom} = {valeur}\n"
                        break
            
            # Écrire le fichier modifié
            with open('config.py', 'w', encoding='utf-8') as f:
                f.writelines(lignes)
            
            # Mettre à jour les valeurs dans le module config
            for nom, valeur in valeurs.items():
                setattr(config, nom, valeur)
            
            return True
        except Exception as e:
            print(f"Erreur lors de la sauvegarde : {e}")
            return False

