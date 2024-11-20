
import psutil
import os

def monitor_resources(interval=1):
    """
    Surveille les ressources utilisées par le processus actuel.
    :param interval: Intervalle de temps (en secondes) entre chaque mesure.
    """
    pid = os.getpid()  # ID du processus actuel
    process = psutil.Process(pid)

    print(f"Surveillance des ressources pour le PID {pid}...")
    print("Appuyez sur Ctrl+C pour arrêter.")
    
    try:
        while True:
            # Utilisation du CPU (en pourcentage)
            cpu_usage = process.cpu_percent(interval=interval)

            # Utilisation de la mémoire (en bytes)
            memory_info = process.memory_info()
            memory_usage = memory_info.rss / (1024 * 1024)  # En Mo

            # Utilisation des fichiers temporaires (E/S disque)
            io_counters = process.io_counters()
            read_bytes = io_counters.read_bytes / (1024 * 1024)  # En Mo
            write_bytes = io_counters.write_bytes / (1024 * 1024)  # En Mo

            # Informations réseau (en cas de serveur Flask actif)
            net_io = psutil.net_io_counters()
            bytes_sent = net_io.bytes_sent / (1024 * 1024)  # En Mo
            bytes_recv = net_io.bytes_recv / (1024 * 1024)  # En Mo

            # Affichage des données
            print(f"CPU: {cpu_usage:.2f}% | Mémoire: {memory_usage:.2f} Mo | "
                  f"Lecture: {read_bytes:.2f} Mo | Écriture: {write_bytes:.2f} Mo | "
                  f"Envoi: {bytes_sent:.2f} Mo | Réception: {bytes_recv:.2f} Mo")
    except KeyboardInterrupt:
        print("\nSurveillance arrêtée.")
if __name__ == '__main__':
    monitor_resources()
