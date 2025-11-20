"""
Module principal du jeu - Gère la boucle de jeu
"""
import math
import pygame
import sys
import config
from cible import Cible
from interface_fin import InterfaceFin
from generateur_pdf import GenerateurPDF
from dialogue_nom_fichier import DialogueNomFichier


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
        
        # Démarrer l'enregistrement du chemin pour la première cible
        self.enregistrement_chemin = True
        self.chemin_actuel = [(config.CURSEUR_X_APRES_CLIC, config.CURSEUR_Y_APRES_CLIC)]
        
        # État du jeu
        self.running = True
        self.en_affichage_resultat = False
        self.temps_debut_resultat = 0
        self.point_traversee = None  # Point (x, y) où le curseur a traversé la ligne
        self.cible_precedente = None  # Position de la cible précédente pour l'affichage
        self.fin_de_partie = False  # Indique si on a atteint le nombre max de cibles
        
        # Enregistrement des données pour le PDF
        self.donnees_chemins = []  # Liste de dictionnaires avec chemin, cible, point_traversee
        self.chemin_actuel = []  # Liste des positions du curseur pour la tentative actuelle
        self.enregistrement_chemin = False  # Indique si on enregistre le chemin actuellement
        
        # Interface de fin de partie
        self.interface_fin = InterfaceFin(ecran)
        
        # Dialogue et pop-up
        self.dialogue_actif = None
        self.popup_succes = None
        self.temps_popup = 0
    
    def gerer_evenements(self):
        """Gère les événements du jeu"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if self.dialogue_actif:
                    # Passer l'événement au dialogue
                    resultat = self.dialogue_actif.gerer_evenement(event)
                    if resultat == "ok":
                        nom_fichier = self.dialogue_actif.obtenir_nom_fichier()
                        self.dialogue_actif = None
                        if nom_fichier:
                            self.generer_pdf_donnees(nom_fichier)
                    elif resultat == "annuler":
                        self.dialogue_actif = None
                elif event.key == pygame.K_ESCAPE:
                    self.running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if self.dialogue_actif:
                    # Gérer les événements du dialogue
                    resultat = self.dialogue_actif.gerer_evenement(event)
                    if resultat == "ok":
                        nom_fichier = self.dialogue_actif.obtenir_nom_fichier()
                        self.dialogue_actif = None
                        if nom_fichier:
                            self.generer_pdf_donnees(nom_fichier)
                    elif resultat == "annuler":
                        self.dialogue_actif = None
                elif event.button == 1 and self.fin_de_partie:  # Clic gauche pendant la fin de partie
                    action = self.interface_fin.gerer_clic(event.pos)
                    if action == "recommencer":
                        self.reinitialiser_jeu()
                    elif action == "quitter":
                        self.running = False
                    elif action == "recuperer_donnees":
                        # Ouvrir le dialogue pour demander le nom
                        self.dialogue_actif = DialogueNomFichier(self.ecran)
    
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
        
        # Arrêter l'enregistrement du chemin et sauvegarder les données
        if self.enregistrement_chemin:
            # Ajouter le point de traversée au chemin
            self.chemin_actuel.append(point_traversee)
            # Sauvegarder les données de cette tentative
            self.donnees_chemins.append({
                'chemin': self.chemin_actuel.copy(),
                'cible': (self.cible.x, self.cible.y),
                'point_traversee': point_traversee
            })
            # Réinitialiser pour la prochaine tentative
            self.chemin_actuel = []
            self.enregistrement_chemin = False
        
        # Activer l'affichage du résultat
        self.en_affichage_resultat = True
        self.temps_debut_resultat = pygame.time.get_ticks()
        
        print(f"Traversée détectée au point: x={point_traversee[0]}, y={point_traversee[1]}")
        print(f"Cible était à: x={self.cible_precedente[0]}, y={self.cible_precedente[1]}")
    
    def mettre_a_jour(self):
        """Met à jour l'état du jeu"""
        # Si fin de partie, gérer le curseur au survol des boutons
        if self.fin_de_partie:
            if self.dialogue_actif:
                # Ne pas changer le curseur pendant le dialogue
                return
            position_souris = pygame.mouse.get_pos()
            if self.interface_fin.est_sur_bouton(position_souris):
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
            else:
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
            return
        
        # Obtenir la position actuelle du curseur
        position_actuelle = pygame.mouse.get_pos()
        
        # Enregistrer le chemin du curseur si on n'est pas en affichage de résultat
        if not self.en_affichage_resultat and self.enregistrement_chemin:
            # Ajouter la position actuelle au chemin (éviter les doublons si le curseur ne bouge pas)
            if (not self.chemin_actuel or 
                position_actuelle != self.chemin_actuel[-1]):
                self.chemin_actuel.append(position_actuelle)
        
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
                    
                    # Démarrer l'enregistrement du chemin pour la nouvelle tentative
                    self.enregistrement_chemin = True
                    self.chemin_actuel = [(config.CURSEUR_X_APRES_CLIC, config.CURSEUR_Y_APRES_CLIC)]
    
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
        
        # Dessiner le dialogue si actif
        if self.dialogue_actif:
            self.dialogue_actif.dessiner()
        
        # Dessiner la pop-up de succès si active
        if self.popup_succes:
            self.dessiner_popup_succes()
    
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
        
        # Réinitialiser les données
        self.donnees_chemins = []
        self.chemin_actuel = []
        self.enregistrement_chemin = False
        
        # Démarrer l'enregistrement pour la première cible
        self.enregistrement_chemin = True
        self.chemin_actuel = [(config.CURSEUR_X_APRES_CLIC, config.CURSEUR_Y_APRES_CLIC)]
    
    def generer_pdf_donnees(self, nom_fichier=None):
        """Génère le PDF avec les données des chemins"""
        if len(self.donnees_chemins) == 0:
            print("Aucune donnée à exporter")
            return
        
        generateur = GenerateurPDF()
        chemin_fichier = generateur.generer_pdf(self.donnees_chemins, nom_fichier)
        
        if chemin_fichier:
            # Afficher la pop-up de succès
            self.popup_succes = True
            self.temps_popup = pygame.time.get_ticks()
            print(f"PDF généré avec {len(self.donnees_chemins)} chemins")
        else:
            print("Erreur lors de la génération du PDF")
    
    def dessiner_popup_succes(self):
        """Dessine la pop-up de succès en haut à droite"""
        # Vérifier si on doit encore afficher la pop-up (5 secondes)
        temps_ecoule = pygame.time.get_ticks() - self.temps_popup
        if temps_ecoule >= 5000:
            self.popup_succes = None
            return
        
        # Dimensions de la pop-up
        largeur_popup = int(config.LARGEUR * 0.25)
        hauteur_popup = int(config.HAUTEUR * 0.08)
        x_popup = config.LARGEUR - largeur_popup - 20
        y_popup = 20
        
        # Fond de la pop-up
        popup_rect = pygame.Rect(x_popup, y_popup, largeur_popup, hauteur_popup)
        pygame.draw.rect(self.ecran, config.VERT, popup_rect)
        pygame.draw.rect(self.ecran, config.NOIR, popup_rect, 2)
        
        # Texte
        taille_texte = int(config.HAUTEUR * 0.04)
        font = pygame.font.Font(None, taille_texte)
        texte = font.render("PDF créé avec succès", True, config.BLANC)
        texte_rect = texte.get_rect(center=popup_rect.center)
        self.ecran.blit(texte, texte_rect)
