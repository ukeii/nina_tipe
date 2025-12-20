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
                - 'temps_chemin': Liste des temps relatifs en ms pour chaque point du chemin
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
                    # Calculer la durée du mouvement et échantillonner les points tous les 50 ms
                    duree_ms = 0
                    points_echantillones = []
                    
                    if 'temps_chemin' in donnees and donnees['temps_chemin']:
                        temps_chemin = donnees['temps_chemin']
                        chemin = donnees['chemin']
                        duree_ms = temps_chemin[-1] if temps_chemin else 0
                        
                        # Échantillonner les points tous les 50 ms
                        temps_echantillonnage = list(range(0, int(duree_ms) + 50, 50))
                        points_echantillones = []
                        
                        for t_ech in temps_echantillonnage:
                            # Trouver le point le plus proche de ce temps
                            if t_ech <= temps_chemin[-1]:
                                # Trouver l'index du point le plus proche
                                idx = min(range(len(temps_chemin)), 
                                         key=lambda i: abs(temps_chemin[i] - t_ech))
                                x, y = chemin[idx]
                                points_echantillones.append({
                                    'temps_ms': t_ech,
                                    'x': int(x),
                                    'y': int(y)
                                })
                    elif donnees['chemin']:
                        # Si pas de timestamps, utiliser une estimation basée sur le nombre de points
                        chemin = donnees['chemin']
                        # Estimer ~16ms par point (60 FPS)
                        duree_ms = len(chemin) * 16
                        # Échantillonner tous les 50ms
                        intervalle_points = max(1, len(chemin) // (int(duree_ms) // 50 + 1))
                        for idx in range(0, len(chemin), intervalle_points):
                            x, y = chemin[idx]
                            t_estime = idx * 16
                            points_echantillones.append({
                                'temps_ms': t_estime,
                                'x': int(x),
                                'y': int(y)
                            })
                    
                    # PAGE 1 : Créer la figure pour le graphique
                    fig_graph = plt.figure(figsize=(11, 8))
                    ax = fig_graph.add_subplot(111)
                    
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
                    
                    # Ajouter les axes avec graduations
                    ax.set_xlabel('Abscisse (X)', fontsize=10)
                    ax.set_ylabel('Ordonnée (Y)', fontsize=10)
                    ax.tick_params(axis='both', which='major', labelsize=8)
                    
                    # Activer la grille
                    ax.grid(True, alpha=0.3, linestyle='-', linewidth=0.5)
                    ax.set_axisbelow(True)
                    
                    # Afficher les coordonnées de la cible
                    info_texte = f"Cible: ({cible_x}, {cible_y})"
                    if donnees['point_traversee']:
                        pt_x, pt_y = donnees['point_traversee']
                        info_texte += f"\nPoint touché: ({pt_x}, {pt_y})"
                    
                    # Ajouter une boîte de texte avec les coordonnées
                    ax.text(0.02, 0.98, info_texte,
                           transform=ax.transAxes,
                           fontsize=9,
                           verticalalignment='top',
                           bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8),
                           family='monospace')
                    
                    # Annoter la cible avec ses coordonnées
                    ax.annotate(f'({cible_x}, {cible_y})',
                               xy=(cible_x, cible_y),
                               xytext=(10, 10),
                               textcoords='offset points',
                               fontsize=8,
                               bbox=dict(boxstyle='round,pad=0.3', facecolor='lightcoral', alpha=0.7),
                               arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=0', color='red', lw=1))
                    
                    # Annoter le point de traversée avec ses coordonnées
                    if donnees['point_traversee']:
                        ax.annotate(f'({pt_x}, {pt_y})',
                                   xy=(pt_x, pt_y),
                                   xytext=(10, -20),
                                   textcoords='offset points',
                                   fontsize=8,
                                   bbox=dict(boxstyle='round,pad=0.3', facecolor='lightgreen', alpha=0.7),
                                   arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=0', color='green', lw=1))
                    
                    ax.legend(loc='upper right', fontsize=8)
                    
                    # Afficher la durée dans le titre ou dans une boîte de texte
                    duree_texte = f"Durée du mouvement : {duree_ms:.0f} ms ({duree_ms/1000:.2f} s)"
                    ax.text(0.98, 0.02, duree_texte,
                           transform=ax.transAxes,
                           fontsize=10,
                           verticalalignment='bottom',
                           horizontalalignment='right',
                           bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.8),
                           family='monospace')
                    
                    # Sauvegarder la page du graphique
                    plt.tight_layout()
                    pdf.savefig(fig_graph, bbox_inches='tight')
                    plt.close(fig_graph)
                    
                    # PAGE 2 : Créer la figure pour le tableau
                    if points_echantillones:
                        fig_table = plt.figure(figsize=(11, 8))
                        ax_table = fig_table.add_subplot(111)
                        ax_table.axis('off')
                        
                        
                        # Préparer les données pour le tableau
                        # Limiter à un nombre raisonnable de lignes pour la lisibilité
                        max_lignes = 30
                        if len(points_echantillones) > max_lignes:
                            # Prendre les premiers et les derniers points
                            points_affiches = (points_echantillones[:max_lignes//2] + 
                                             points_echantillones[-max_lignes//2:])
                            # Ajouter une ligne de séparation
                            points_affiches.insert(max_lignes//2, {'temps_ms': '...', 'x': '...', 'y': '...'})
                        else:
                            points_affiches = points_echantillones
                        
                        # Créer le tableau
                        tableau_data = [['Temps (ms)', 'X', 'Y']]
                        for point in points_affiches:
                            tableau_data.append([
                                str(point['temps_ms']),
                                str(point['x']),
                                str(point['y'])
                            ])
                        
                        table = ax_table.table(cellText=tableau_data[1:],
                                              colLabels=tableau_data[0],
                                              cellLoc='center',
                                              loc='center',
                                              colWidths=[0.3, 0.35, 0.35])
                        
                        # Styliser le tableau
                        table.auto_set_font_size(False)
                        table.set_fontsize(9)
                        table.scale(1, 2)
                        
                        # Mettre en forme l'en-tête
                        for i in range(3):
                            table[(0, i)].set_facecolor('#4CAF50')
                            table[(0, i)].set_text_props(weight='bold', color='white')
                        
                        # Alterner les couleurs des lignes
                        for i in range(1, len(tableau_data)):
                            for j in range(3):
                                if i % 2 == 0:
                                    table[(i, j)].set_facecolor('#f0f0f0')
                                else:
                                    table[(i, j)].set_facecolor('white')
                        
                        # Ajouter la durée en bas du tableau
                        ax_table.text(0.5, 0.02, duree_texte,
                                     transform=ax_table.transAxes,
                                     fontsize=10,
                                     verticalalignment='bottom',
                                     horizontalalignment='center',
                                     bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.8),
                                     family='monospace')
                        
                        # Sauvegarder la page du tableau
                        plt.tight_layout()
                        pdf.savefig(fig_table, bbox_inches='tight')
                        plt.close(fig_table)
            
            print(f"PDF généré : {nom_fichier_complet}")
            print(f"Emplacement : {os.path.abspath(nom_fichier_complet)}")
            return os.path.abspath(nom_fichier_complet)
        except Exception as e:
            print(f"Erreur lors de la génération du PDF : {e}")
            return None

