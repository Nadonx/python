import platform
import psutil

# Fonction d'affichage des informations système
def afficher_info_systeme():
    print("=== Système ===")
    print(f"OS: {platform.system()}")
    print(f"Version: {platform.version()}")
    print(f"Architecture: {platform.architecture()[0]}")
    print(f"Hostname: {platform.node()}")
    print(f"Python: {platform.python_version()}")

# Fonction d'affichage des informations CPU
def afficher_info_cpu():
    print("\n=== CPU ===")
    print(f"Coeurs physiques: {psutil.cpu_count(logical=False)}")
    print(f"Coeurs logiques: {psutil.cpu_count(logical=True)}")
    print(f"Utilisation: {psutil.cpu_percent(interval=1.0)}%")

# Fonction d'affichage de la mémoire
def afficher_info_mem():
    print("\n=== Mémoire ===")
    mem = psutil.virtual_memory()
    total_gb = round(mem.total / (1024 ** 3), 2)
    disponible_gb = round(mem.available / (1024 ** 3), 2)
    utilisation_percent = round(mem.percent, 2)
    
    print(f"Total: {total_gb} GB")
    print(f"Disponible: {disponible_gb} GB")
    print(f"Utilisation: {utilisation_percent}%")

# Fonction d'affichage des informations des disques
def afficher_info_disques():
    print("\n=== Disques ===")
    partitions = psutil.disk_partitions()
    
    for partition in partitions:
        try:
            usage = psutil.disk_usage(partition.mountpoint)
            usage_percent = round(usage.percent, 2)
            print(f"{partition.device}: {usage_percent}% utilisé")
        except PermissionError:
            print(f"{partition.device}: Accès refusé")

# Point d'entrée
if __name__ == "__main__":
    print("=== SysWatch v1.0 ===")
    
    afficher_info_systeme()
    afficher_info_cpu()
    afficher_info_mem()
    afficher_info_disques()
