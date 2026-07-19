
# Pocket-TTS Hörbuch-Generator

## Beschreibung

Dieses Programm wandelt Textdateien, PDF-Dokumente und EPUB-Bücher automatisch in gesprochene WAV-Audiodateien um.
Es verwendet das Pocket-TTS Sprachmodell zur KI-basierten Spracherzeugung und ermöglicht die Verwendung eigener Sprachaufnahmen als Stimmenvorlage.

## Funktionen
- PDF-Dateien auslesen und in Text umwandeln
- EPUB-Bücher auslesen
- TXT-Dateien direkt verarbeiten
- Automatische Textbereinigung
- Entfernung von PDF-Trennungen und Formatierungsfehlern
- Aufteilung langer Texte in verarbeitbare Textblöcke
- KI-Spracherzeugung mit Pocket-TTS
- Unterstützung eigener Stimmenvorlagen
- Streaming-Erzeugung der Audiodaten
- Direkte Ausgabe als WAV-Datei
- Unterstützung verschiedener Eingabestimmen

## Verwendung

Aufruf:

```bash
python3 tts2.py datei.pdf stimme


python3 tts2.py bibel.pdf heidi


stimmen/heidi.wav







###########################################

#
# in python einbauen beispiel
#

import subprocess

subprocess.run(
    ["ffmpeg", "-i", "video.mkv", "-vn", "-ac", "1", "-ar", "16000",
     "-c:a", "pcm_s16le", "stimme.wav"]
)








-----------------

import subprocess

text = "Hallo, ich bin Fred."

subprocess.run([
    "pocket-tts",
    "generate",
    "--text", text,
    "--language", "german_24l",
    "--voice", "stimmen/heidi.wav"
])

----------------

result = subprocess.run(
    ["pocket-tts", "generate",
     "--text", "Test",
     "--language", "german_24l"],
    capture_output=True,
    text=True
)

print(result.stdout)
print(result.stderr)






#
# datei umwandel video zu wav
#



ffmpeg -i heidi.mkv -vn -ac 1 -ar 16000 -c:a pcm_s16le heidi.wav



#
# pdf to wave und umwandel 
#

sudo apt install poppler-utils

pdftotext datei.pdf datei.txt


sed -i 's/"//g' datei.txt
sed -i "s/'//g" datei.txt
sed -i 's/["'\'']//g' datei.txt



#tonspur lauter machen
ffmpeg -i java.wav -af "loudnorm" 2.wav

#aus video ne wav machen
ffmpeg -i elvis.mkv -ac 1 -ar 16000  elvis.wav



ffmpeg \
-i teresa1.wav \
-i teresa2.wav \
-i teresa3.wav \
-i teresa4.wav \
-filter_complex "[0:a][1:a][2:a][3:a]concat=n=4:v=0:a=1[out]" \
-map "[out]" teresa.wav















































