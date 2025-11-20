"""
Module pour générer un PDF avec les données des chemins du curseur
"""
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.backends.backend_pdf import PdfPages
import config
import os
from datetime import datetime


class GenerateurPDF:
    """Classe pour générer un PDF avec les chemins du curseur"""
    
    def __init__(self):
        """Initialise le générateur de PDF"""
        pass
    
    def generer_pdf(self, donnees_chemins, nom_fichier=None):
        """
        Génère un PDF avec les données des chemins
        
        Args:
            donnees_chemins: Liste de dictionnaires contenant:
                - 'chemin': Liste de tuples (x, y) du chemin du curseur
                - 'cible': Tuple (x, y) de la position de la cible
                - 'point_traversee': Tuple (x, y) du point de traversée
            nom_fichier: Nom du fichier (sans extension). Si None, utilise un timestamp
        
        Returns:
            Chemin complet du fichier créé ou None en cas d'erreur
        """
        # Créer le dossier pdf s'il n'existe pas
        dossier_pdf = "pdf"
        if not os.path.exists(dossier_pdf):
            os.makedirs(dossier_pdf)
        
        # Créer le nom du fichier
        if nom_fichier is None or nom_fichier.strip() == "":
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            nom_fichier = f"donnees_chemins_{timestamp}"
        
        # Nettoyer le nom du fichier (enlever les caractères invalides)
        nom_fichier = "".join(c for c in nom_fichier if c.isalnum() or c in "._- ")
        if not nom_fichier:
            nom_fichier = f"donnees_chemins_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        # Ajouter l'extension et le chemin
        nom_fichier_complet = os.path.join(dossier_pdf, f"{nom_fichier}.pdf")
        
        # Créer le PDF avec matplotlib
        try:
            with PdfPages(nom_fichier_complet) as pdf:
                for i, donnees in enumerate(donnees_chemins):
                    # Créer une figure pour chaque chemin
                    fig, ax = plt.subplots(figsize=(8, 8))
                    
                    # Dessiner le cercle imaginaire
                    cercle = patches.Circle(
                        (config.CERCLE_CENTRE_X, config.CERCLE_CENTRE_Y),
                        config.CERCLE_RAYON,
                        fill=False,
                        edgecolor='gray',
                        linewidth=1,
                        linestyle='--'
                    )
                    ax.add_patch(cercle)
                    
                    # Dessiner le chemin du curseur
                    if donnees['chemin'] and len(donnees['chemin']) > 1:
                        chemin_x = [p[0] for p in donnees['chemin']]
                        chemin_y = [p[1] for p in donnees['chemin']]
                        ax.plot(chemin_x, chemin_y, 'b-', linewidth=2, alpha=0.7, label='Chemin du curseur')
                    
                    # Dessiner le point de départ (centre)
                    ax.plot(
                        config.CERCLE_CENTRE_X,
                        config.CERCLE_CENTRE_Y,
                        'go',
                        markersize=10,
                        label='Départ (centre)'
                    )
                    
                    # Dessiner la cible (cercle)
                    cible_x, cible_y = donnees['cible']
                    cercle_cible = patches.Circle(
                        (cible_x, cible_y),
                        config.RAYON_CIBLE,
                        fill=True,
                        edgecolor='red',
                        facecolor='lightcoral',
                        linewidth=2,
                        label='Cible'
                    )
                    ax.add_patch(cercle_cible)
                    
                    # Dessiner le point de traversée (croix)
                    if donnees['point_traversee']:
                        pt_x, pt_y = donnees['point_traversee']
                        ax.plot(pt_x, pt_y, 'r+', markersize=15, markeredgewidth=3, label='Point de traversée')
                    
                    # Configuration de l'axe
                    ax.set_aspect('equal')
                    ax.set_xlim(0, config.LARGEUR)
                    ax.set_ylim(config.HAUTEUR, 0)  # Inverser Y pour correspondre aux coordonnées pygame (0,0 en haut)
                    ax.set_title(f'Essai {i+1} / {len(donnees_chemins)}', fontsize=14, fontweight='bold')
                    ax.grid(True, alpha=0.3)
                    ax.legend(loc='upper right', fontsize=8)
                    
                    # Ajouter la page au PDF
                    plt.tight_layout()
                    pdf.savefig(fig, bbox_inches='tight')
                    plt.close(fig)
            
            print(f"PDF généré : {nom_fichier_complet}")
            print(f"Emplacement : {os.path.abspath(nom_fichier_complet)}")
            return os.path.abspath(nom_fichier_complet)
        except Exception as e:
            print(f"Erreur lors de la génération du PDF : {e}")
            return None

