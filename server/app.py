from flask import Flask, render_template, request, redirect, url_for, send_from_directory
import os
import subprocess
import uuid

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
RECEIVED_FOLDER = 'received'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Assure que les dossiers existent
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(RECEIVED_FOLDER, exist_ok=True)

# Route pour la page d'accueil
@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        # Vérifie si un fichier a été soumis dans la requête POST
        if 'file' not in request.files:
            return redirect(request.url)
        file = request.files['file']
        # Vérifie si le fichier est vide
        if file.filename == '':
            return redirect(request.url)
        
        if file:
            # Enregistre l'image téléchargée dans le dossier "uploads" avec un chemin absolu
            filename = os.path.join(os.getcwd(), app.config['UPLOAD_FOLDER'], file.filename)
            file.save(filename)

            # Supprime tous les fichiers existants dans le dossier "received"
            for received_file in os.listdir(RECEIVED_FOLDER):
                if received_file.endswith('.jpg'):
                    received_file_path = os.path.join(RECEIVED_FOLDER, received_file)
                    os.remove(received_file_path)

            # Exécute le script serveur en tant que sous-processus
            subprocess.run(["python", "server.py", filename])

            # Récupère les images dans le dossier "received"
            received_images = []
            for received_file in os.listdir(RECEIVED_FOLDER):
                if received_file.endswith('.jpg'):
                    received_images.append(received_file)
            return render_template('resullt.html', received_images=received_images)

    return render_template('index.html')

# Route pour servir les images reçues
@app.route('/received/<filename>')
def serve_received_image(filename):
    return send_from_directory(RECEIVED_FOLDER, filename)





if __name__ == '__main__':
    import threading
    import psutil
    import time

    def log_metrics(interval=1):
        """
        Enregistre les métriques pendant l'exécution du serveur Flask.
        """
        pid = os.getpid()
        process = psutil.Process(pid)

        with open("resource_usage.log", "w") as log_file:
            log_file.write("Temps, CPU(%), Mémoire(Mo)\n")

            while True:
                # Capture des métriques
                cpu_usage = process.cpu_percent(interval=interval)
                memory_usage = process.memory_info().rss / (1024 * 1024)

                # Enregistrement dans le fichier
                log_file.write(f"{time.time()}, {cpu_usage:.2f}, {memory_usage:.2f}\n")
                log_file.flush()

    # Lancement de la surveillance en parallèle
    monitor_thread = threading.Thread(target=log_metrics, daemon=True)
    monitor_thread.start()

    app.run(host='0.0.0.0', port=5000)
