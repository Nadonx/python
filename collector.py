import platform
import psutil
from datetime import datetime
 
 
def collecter_info_systeme():
    """
    Retourne les informations générales du système sous forme de dictionnaire.
    """
    return {
        "os": platform.system(),
        "version": platform.release(),
        "architecture": platform.machine(),
        "hostname": platform.node()
    }
 
 
def collecter_cpu():
    """
    Retourne les informations liées au CPU :
    coeurs physiques, logiques et utilisation.
    """
    return {
        "coeurs_physiques": psutil.cpu_count(logical=False),
        "coeurs_logiques": psutil.cpu_count(logical=True),
        "utilisation": psutil.cpu_percent(interval=1)
    }
 
 
def collecter_memoire():
    """
    Retourne les données mémoire sous forme d'un dictionnaire :
    total, disponible et pourcentage.
    """
    mem = psutil.virtual_memory()
 
    return {
        "total": mem.total,
        "disponible": mem.available,
        "pourcentage": mem.percent
    }
 
 
def collecter_disques():
    """
    Retourne une liste contenant les informations des partitions accessibles.
    """
    partitions = psutil.disk_partitions()
    resultats = []
 
    for p in partitions:
        try:
            usage = psutil.disk_usage(p.mountpoint)
            resultats.append({
                "point_montage": p.mountpoint,
                "total": usage.total,
                "utilise": usage.used,
                "pourcentage": usage.percent
            })
        except PermissionError:
            # On ignore les partitions non accessibles
            pass
 
    return resultats
 
 
def collecter_tout():
    """
    Rassemble toutes les métriques système dans un seul dictionnaire.
    Ajoute aussi un timestamp.
    """
    return {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "systeme": collecter_info_systeme(),
        "cpu": collecter_cpu(),
        "memoire": collecter_memoire(),
        "disques": collecter_disques()
    }