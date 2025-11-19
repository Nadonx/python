import argparse
import time
import os
from datetime import datetime
import collector
import traitement

# Fonction de collecte continue
def collecter_en_continu(intervalle, nombre):
    """
    Collecte continue des métriques pendant un intervalle spécifié.
    """
    count = 0
    while nombre == 0 or count < nombre:
        print(f"Collecte {count + 1}...")
        donnees = collector.collecter_tout()
        print(f"Timestamp: {donnees['timestamp']}")

        # Exportation CSV et JSON
        traitement.exporter_csv(donnees, 'donnees.csv')
        traitement.exporter_json(donnees, 'donnees.json')

        # Attente avant la prochaine collecte
        time.sleep(intervalle)
        count += 1

# Fonction de traitement des arguments en ligne de commande
def traiter_arguments():
    parser = argparse.ArgumentParser(description="Collecte et traitement des données système")

    # Arguments pour la collecte continue
    parser.add_argument('--continu', action='store_true', help="Collecte continue des données")
    parser.add_argument('--intervalle', type=int, default=30, help="Intervalle entre chaque collecte (en secondes)")
    parser.add_argument('--nombre', type=int, default=0, help="Nombre de collectes (0 pour infini)")
    parser.add_argument('--stats', action='store_true', help="Affiche les statistiques du fichier CSV")

    args = parser.parse_args()

    return args

def main():
    args = traiter_arguments()

    if args.stats:
        # Affichage des statistiques
        stats = traitement.calculer_moyennes('donnees.csv')
        print(f"Statistiques : {stats}")
        return

    if args.continu:
        # Collecte continue
        collecter_en_continu(args.intervalle, args.nombre)
    else:
        # Collecte unique
        donnees = collector.collecter_tout()
        print(f"Timestamp: {donnees['timestamp']}")
        traitement.exporter_csv(donnees, 'donnees.csv')
        traitement.exporter_json(donnees, 'donnees.json')

if __name__ == "__main__":
    main()
