"""
Module pour générer un PDF avec les données des chemins du curseur
"""
import math
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.backends.backend_pdf import PdfPages
import config
import os
from datetime import datetime


def _intersection_segment_cercle(p0, p1, centre, rayon):
    """
    Retourne le point d'intersection du segment [p0, p1] avec le cercle (centre, rayon),
    en prenant le premier point rencontré en partant de p0 (ou None si pas d'intersection).
    """
    cx, cy = centre
    x0, y0 = p0
    x1, y1 = p1
    dx = x1 - x0
    dy = y1 - y0
    ex = x0 - cx
    ey = y0 - cy
    a = dx * dx + dy * dy
    if a < 1e-12:
        return None
    b = 2 * (ex * dx + ey * dy)
    c = ex * ex + ey * ey - rayon * rayon
    disc = b * b - 4 * a * c
    if disc < 0:
        return None
    t1 = (-b - math.sqrt(disc)) / (2 * a)
    t2 = (-b + math.sqrt(disc)) / (2 * a)
    for t in sorted([t1, t2]):
        if 0 <= t <= 1:
            return (x0 + t * dx, y0 + t * dy)
    return None


def _point_intersection_chemin_cercle(chemin, centre, rayon):
    """Retourne le premier point où le chemin (liste de (x,y)) croise le cercle, ou None."""
    if not chemin or len(chemin) < 2:
        return None
    for i in range(len(chemin) - 1):
        pt = _intersection_segment_cercle(chemin[i], chemin[i + 1], centre, rayon)
        if pt is not None:
            return pt
    return None


def _angle_entre_vecteurs_deg(centre, p1, p2):
    """Angle en degrés entre (centre->p1) et (centre->p2), dans [0, 360)."""
    x0, y0 = centre
    ux = p1[0] - x0
    uy = p1[1] - y0
    vx = p2[0] - x0
    vy = p2[1] - y0
    norm_u = math.hypot(ux, uy)
    norm_v = math.hypot(vx, vy)
    if norm_u < 1e-10 or norm_v < 1e-10:
        return None
    cos_a = (ux * vx + uy * vy) / (norm_u * norm_v)
    cos_a = max(-1, min(1, cos_a))
    return math.degrees(math.acos(cos_a))


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
                # ----- Page 1 : Page de garde -----
                fig_cover = plt.figure(figsize=(11, 8))
                ax_cover = fig_cover.add_subplot(111)
                ax_cover.set_xlim(0, 1)
                ax_cover.set_ylim(0, 1)
                ax_cover.axis('off')

                # Fond discret
                fig_cover.patch.set_facecolor('#f8f9fa')
                ax_cover.set_facecolor('#f8f9fa')

                # Titre principal : PDF des données de [nom du fichier]
                nom_affiché = nom_fichier.replace('.pdf', '') if nom_fichier.endswith('.pdf') else nom_fichier
                ax_cover.text(0.5, 0.70, "Rapport des données",
                              transform=ax_cover.transAxes, fontsize=26, fontweight='bold',
                              ha='center', va='center', color='#2c3e50')
                ax_cover.text(0.5, 0.58, f"Données de : {nom_affiché}",
                              transform=ax_cover.transAxes, fontsize=18, style='italic',
                              ha='center', va='center', color='#34495e',
                              bbox=dict(boxstyle='round,pad=0.5', facecolor='white', edgecolor='#bdc3c7', alpha=0.9))

                # Bloc paramètres de l'expérience
                ax_cover.text(0.5, 0.42, "Paramètres de l'expérience",
                              transform=ax_cover.transAxes, fontsize=16, fontweight='bold',
                              ha='center', va='center', color='#2c3e50')

                params_texte = (
                    f"• Cible à partir de laquelle la déviation a commencé : {config.CIBLE_DEBUT_DEVIATION}\n\n"
                    f"• Angle de déviation : {config.ANGLE_DEVIATION}°\n\n"
                    f"• Durée d'affichage du résultat : {config.DUREE_AFFICHAGE_RESULTAT} ms ({config.DUREE_AFFICHAGE_RESULTAT / 1000:.2f} s)"
                )
                ax_cover.text(0.5, 0.22, params_texte,
                              transform=ax_cover.transAxes, fontsize=13,
                              ha='center', va='center', color='#34495e',
                              bbox=dict(boxstyle='round,pad=0.8', facecolor='white', edgecolor='#3498db', alpha=0.95),
                              family='monospace')

                plt.tight_layout()
                pdf.savefig(fig_cover, bbox_inches='tight', facecolor=fig_cover.get_facecolor())
                plt.close(fig_cover)

                # ----- Pages suivantes : graphiques par essai -----
                for i, donnees in enumerate(donnees_chemins):
                    # Calculer la durée du mouvement (pour l'affichage sur le graphique)
                    duree_ms = 0
                    if 'temps_chemin' in donnees and donnees['temps_chemin']:
                        temps_chemin = donnees['temps_chemin']
                        duree_ms = temps_chemin[-1] if temps_chemin else 0
                    elif donnees.get('chemin'):
                        duree_ms = len(donnees['chemin']) * 16  # estimation ~60 FPS
                    
                    # Créer la figure pour le graphique (seule page par essai)
                    fig_graph = plt.figure(figsize=(11, 8))
                    ax = fig_graph.add_subplot(111)
                    
                    centre = (config.CERCLE_CENTRE_X, config.CERCLE_CENTRE_Y)
                    rayon_petit = config.CERCLE_RAYON / 10

                    # Dessiner le cercle imaginaire (grand)
                    cercle = patches.Circle(
                        centre,
                        config.CERCLE_RAYON,
                        fill=False,
                        edgecolor='gray',
                        linewidth=1,
                        linestyle='--'
                    )
                    ax.add_patch(cercle)

                    # Dessiner le 2e cercle (orange), même centre, 1/10 du rayon
                    cercle_orange = patches.Circle(
                        centre,
                        rayon_petit,
                        fill=False,
                        edgecolor='orange',
                        linewidth=2,
                        linestyle='-'
                    )
                    ax.add_patch(cercle_orange)
                    
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

                    # Intersection chemin / cercle orange, droites centre->intersection et centre->cible, angle
                    cible_x, cible_y = donnees['cible']
                    pt_intersection = None
                    if donnees['chemin'] and len(donnees['chemin']) > 1:
                        pt_intersection = _point_intersection_chemin_cercle(
                            donnees['chemin'], centre, rayon_petit
                        )
                    if pt_intersection is not None:
                        ix, iy = pt_intersection
                        ax.plot(ix, iy, 'o', color='orange', markersize=10, markeredgecolor='darkorange',
                                markeredgewidth=2, label='Intersection cercle orange')
                        ax.plot([centre[0], ix], [centre[1], iy], 'o-', color='orange', linewidth=2,
                                label='Centre → intersection')
                        ax.plot([centre[0], cible_x], [centre[1], cible_y], 'k-', linewidth=1.5,
                                label='Centre → cible')
                        angle_deg = _angle_entre_vecteurs_deg(centre, pt_intersection, (cible_x, cible_y))
                        if angle_deg is not None:
                            angle_texte = f"Angle entre les deux droites : {angle_deg:.1f}°"
                            ax.text(0.02, 0.90, angle_texte,
                                   transform=ax.transAxes,
                                   fontsize=11,
                                   verticalalignment='top',
                                   bbox=dict(boxstyle='round', facecolor='orange', alpha=0.5),
                                   family='monospace')
                    
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
                    
                    # Sauvegarder la page du graphique (seule page du PDF)
                    plt.tight_layout()
                    pdf.savefig(fig_graph, bbox_inches='tight')
                    plt.close(fig_graph)
            
            print(f"PDF généré : {nom_fichier_complet}")
            print(f"Emplacement : {os.path.abspath(nom_fichier_complet)}")
            return os.path.abspath(nom_fichier_complet)
        except Exception as e:
            print(f"Erreur lors de la génération du PDF : {e}")
            return None

