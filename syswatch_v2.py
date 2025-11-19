import collector

print("Début de l'exécution du script...")  # Vérifie que le script se lance

try:
    print("Test d'importation de 'collector' réussi")
    donnees = collector.collecter_tout()  # Collecte les données
    print("Données collectées avec succès !")
    print("Données collectées : ", donnees)  # Vérifie le contenu des données collectées
except Exception as e:
    print(f"Erreur lors de la collecte des données : {e}")

# Si l'import et la collecte réussissent, affiche les informations
if 'donnees' in locals():
    print("=> SysWatch v2.0")
    print("Date et heure :", donnees["timestamp"])
    print()

    print("Affichage des informations système...")
    # Affichage des informations
    def octets_vers_go(octets):
        """Convertit des octets en gigaoctets avec deux décimales."""
        go = octets / (1024 ** 3)
        return f"{go:.2f} GB"

    def afficher_systeme(data):
        """Affiche les informations générales du système."""
        print("=> Système")
        print("OS:", data["os"])
        print("Version:", data["version"])
        print("Architecture:", data["architecture"])
        print("Hostname:", data["hostname"])
        print()

    def afficher_cpu(data):
        """Affiche les informations sur le CPU."""
        print("=> CPU")
        print("Coeurs physiques:", data["coeurs_physiques"])
        print("Coeurs logiques:", data["coeurs_logiques"])
        print(f"Utilisation: {data['utilisation']:.1f}%")
        print()

    def afficher_memoire(data):
        """Affiche les infos sur la mémoire."""
        print("=> Mémoire")
        print("Total:", octets_vers_go(data["total"]))
        print("Disponible:", octets_vers_go(data["disponible"]))
        print(f"Utilisation: {data['pourcentage']:.1f}%")
        print()

    def afficher_disques(data):
        """Affiche l'utilisation des différentes partitions."""
        print("=> Disques")
        for d in data:
            total = octets_vers_go(d["total"])
            utilise = octets_vers_go(d["utilise"])
            print(f"{d['point_montage']} : {d['pourcentage']:.1f}% utilisé ({utilise}/{total})")
        print()

    afficher_systeme(donnees["systeme"])
    afficher_cpu(donnees["cpu"])
    afficher_memoire(donnees["memoire"])
    afficher_disques(donnees["disques"])

else:
    print("Les données n'ont pas été collectées.")
