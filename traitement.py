import csv
import json
import os

def exporter_csv(metriques, fichier):
    """
    Ajoute les métriques dans un fichier CSV.
    Crée le fichier avec en-têtes s'il n'existe pas.
    """
    colonnes = [
        "timestamp",
        "hostname",
        "cpu_percent",
        "mem_total_gb",
        "mem_dispo_gb",
        "mem_percent",
        "disk_root_percent"
    ]
 
    # Préparation des données à écrire
    ligne = {
        "timestamp": metriques["timestamp"],
        "hostname": metriques["systeme"]["hostname"],
        "cpu_percent": metriques["cpu"]["utilisation"],
        "mem_total_gb": round(metriques["memoire"]["total"] / (1024 ** 3), 2),
        "mem_dispo_gb": round(metriques["memoire"]["disponible"] / (1024 ** 3), 2),
        "mem_percent": metriques["memoire"]["pourcentage"],
        "disk_root_percent": metriques["disques"][0]["pourcentage"]
    }

    # Vérifie si le fichier existe
    existe = os.path.exists(fichier)

    # Ouvre le fichier en mode 'append'
    with open(fichier, "a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=colonnes)

        # Si le fichier n'existe pas, écrit les en-têtes
        if not existe:
            writer.writeheader()

        # Écrit la ligne de données
        writer.writerow(ligne)

def exporter_json(metriques, fichier):
    """
    Sauvegarde les métriques complètes dans un fichier JSON.
    """
    with open(fichier, "w", encoding="utf-8") as f:
        json.dump(metriques, f, indent=2)

def calculer_moyennes(fichier_csv):
    """
    Calcule les stats basiques (min, max, moyenne)
    pour le CPU et la mémoire.
    """
    cpu_vals = []
    mem_vals = []
 
    try:
        with open(fichier_csv, "r", encoding="utf-8") as f:
            lecteur = csv.DictReader(f)
            for ligne in lecteur:
                cpu_vals.append(float(ligne["cpu_percent"]))
                mem_vals.append(float(ligne["mem_percent"]))
    except FileNotFoundError:
        return None

    # Vérifie si les listes sont vides avant de calculer
    if not cpu_vals or not mem_vals:
        return None

    return {
        "cpu_min": min(cpu_vals),
        "cpu_max": max(cpu_vals),
        "cpu_moy": sum(cpu_vals) / len(cpu_vals),
        "mem_min": min(mem_vals),
        "mem_max": max(mem_vals),
        "mem_moy": sum(mem_vals) / len(mem_vals)
    }

def detecter_pics(fichier_csv, seuil_cpu, seuil_mem):
    """
    Retourne les lignes où le CPU ou la mémoire dépassent un seuil.
    """
    resultats = []

    try:
        with open(fichier_csv, "r", encoding="utf-8") as f:
            lecteur = csv.DictReader(f)
            for ligne in lecteur:
                cpu = float(ligne["cpu_percent"])
                mem = float(ligne["mem_percent"])

                if cpu > seuil_cpu or mem > seuil_mem:
                    resultats.append({
                        "timestamp": ligne["timestamp"],
                        "cpu": cpu,
                        "mem": mem
                    })
    except FileNotFoundError:
        return []

    return resultats
