import sys
import time
import os
import collector
import traitement

def octets_vers_go(octets):
    """
    Transforme des octets en Go avec deux décimales.
    """
    return f"{octets / (1024 ** 3):.2f} GB"

def afficher(m):
    """
    Affiche toutes les métriques collectées.
    """
    print("=> SysWatch v3.0")
    print("Timestamp:", m["timestamp"])
    print()
    
    print("=> Système")
    print("OS:", m["systeme"]["os"])
    print("Hostname:", m["systeme"]["hostname"])
    print()

    print("=> CPU")
    print(f"Utilisation: {m['cpu']['utilisation']:.1f}%")
    print()

    print("=> Mémoire")
    print("Total:", octets_vers_go(m["memoire"]["total"]))
    print("Disponible:", octets_vers_go(m["memoire"]["disponible"]))
    print(f"Utilisation: {m['memoire']['pourcentage']:.1f}%")
    print()

    print("=> Disques")
    for d in m["disques"]:
        print(f"{d['point_montage']} : {d['pourcentage']:.1f}%")
    print()

def collecter_en_continu(intervalle, nombre):
    """
    Collecte en boucle selon un intervalle donné.
    S'arrête avec Ctrl+C.
    """
    compteur = 0

    try:
        while True:
            met = collector.collecter_tout()
            afficher(met)
            try:
                traitement.exporter_csv(met, "historique.csv")
                traitement.exporter_json(met, "dernier.json")
            except Exception as e:
                print(f"Erreur lors de l'export : {e}")

            compteur += 1
            if nombre != 0 and compteur >= nombre:
                break

            time.sleep(intervalle)

    except KeyboardInterrupt:
        print("Arrêt demandé par l'utilisateur.")

def afficher_stats():
    """
    Affiche les statistiques chargées depuis le CSV.
    """
    if not os.path.exists("historique.csv"):
        print("Aucun fichier CSV trouvé.")
        return

    stats = traitement.calculer_moyennes("historique.csv")
    if not stats:
        print("Aucune donnée CSV disponible.")
        return

    print("=> Statistiques")
    print(f"CPU : min={stats['cpu_min']:.1f} | max={stats['cpu_max']:.1f} | moy={stats['cpu_moy']:.1f}")
    print(f"MEM : min={stats['mem_min']:.1f} | max={stats['mem_max']:.1f} | moy={stats['mem_moy']:.1f}")
    print()

if __name__ == "__main__":
    args = sys.argv[1:]

    # Pas d’arguments → collecte unique
    if args == []:
        m = collector.collecter_tout()
        afficher(m)
        try:
            traitement.exporter_csv(m, "historique.csv")
            traitement.exporter_json(m, "dernier.json")
        except Exception as e:
            print(f"Erreur lors de l'export : {e}")
        sys.exit()

    # Arguments
    intervalle = 10
    nombre = 0

    if "--intervalle" in args:
        i = args.index("--intervalle")
        intervalle = int(args[i + 1])

    if "--nombre" in args:
        i = args.index("--nombre")
        nombre = int(args[i + 1])

    if "--continu" in args:
        collecter_en_continu(intervalle, nombre)

    if "--stats" in args:
        afficher_stats()
