import os
import shutil
from datetime import datetime

SRC_DIR = 'src'
DIST_DIR = 'dist'

# 1. Build-Ordner vorbereiten (leeren und neu befüllen)
if os.path.exists(DIST_DIR):
    shutil.rmtree(DIST_DIR)
shutil.copytree(SRC_DIR, DIST_DIR)

# 2. HTML-Dateien nach Unterordnern (Themen) gruppieren
topics = {}
for root, dirs, files in os.walk(DIST_DIR):
    # Ordnernamen als Thema nutzen, bei Dateien im Hauptverzeichnis "Allgemein"
    topic_name = os.path.basename(root)
    if root == DIST_DIR:
        topic_name = "Allgemein"
        
    html_files = [f for f in files if f.endswith('.html') and f != 'index.html']
    
    if html_files:
        if topic_name not in topics:
            topics[topic_name] = []
        for f in html_files:
            # Relativen Pfad für den Link berechnen und Backslashes korrigieren
            rel_path = os.path.relpath(os.path.join(root, f), DIST_DIR).replace("\\", "/")
            topics[topic_name].append((f, rel_path))

# Wenn der Allgemein-Ordner leer ist, entfernen wir ihn
if "Allgemein" in topics and not topics["Allgemein"]:
    del topics["Allgemein"]

# 3. Zeitstempel generieren (wird auf der Startseite angezeigt)
timestamp = datetime.now().strftime("%d.%m.%Y um %H:%M:%S Uhr")

# 4. HTML-Inhalt für die Startseite zusammenbauen
html_content = f"""<!DOCTYPE html>
<html lang="de">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Meine Arbeitsblätter</title>
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@picocss/pico@2/css/pico.min.css">
    <style>
        body {{ padding-top: 2rem; }}
        .timestamp {{ color: var(--pico-muted-color); font-size: 0.9em; }}
        .card-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(340px, 1fr));
            gap: 1.5rem;
            margin-top: 1.5rem;
        }}
        .card {{
            background: var(--pico-card-background-color);
            border: 1px solid var(--pico-muted-border-color);
            border-radius: var(--pico-border-radius);
            padding: 1.25rem 1.5rem;
        }}
        .card h2 {{
            margin-top: 0;
            font-size: 1.1rem;
            border-bottom: 1px solid var(--pico-muted-border-color);
            padding-bottom: 0.5rem;
            margin-bottom: 0.75rem;
        }}
        .card ul {{
            margin: 0;
            padding-left: 1.2rem;
        }}
        .card ul li {{
            margin-bottom: 0.3rem;
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
        }}
    </style>
</head>
<body>
    <main class="container">
        <h1>Übersicht</h1>
        <p class="timestamp">Letzter Build: {timestamp}</p>
        <hr>
        <div class="card-grid">
"""

# Themen und Links alphabetisch sortiert in die HTML einfügen
for topic, files in sorted(topics.items()):
    clean_topic = topic.replace('-', ' ').title() # Macht aus "mein-thema" -> "Mein Thema"
    html_content += f'<div class="card"><h2>{clean_topic}</h2><ul>'

    for file_name, file_path in sorted(files):
        # Dateinamen hübscher machen für die Anzeige
        clean_name = file_name.replace('.html', '').replace('-', ' ').replace('_', ' ').title()
        html_content += f'<li><a href="{file_path}" title="{clean_name}">{clean_name}</a></li>'

    html_content += "</ul></div>"

html_content += """
        </div>
    </main>
</body>
</html>
"""

# 5. Generierte index.html in den dist-Ordner schreiben
with open(os.path.join(DIST_DIR, 'index.html'), 'w', encoding='utf-8') as f:
    f.write(html_content)

print("Build erfolgreich: Startseite wurde generiert.")
