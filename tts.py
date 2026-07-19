#tts.py

import os
import sys
import torch
import torchaudio


import soundfile as sf

from pocket_tts import TTSModel


from pypdf import PdfReader
import re

from ebooklib import epub, ITEM_DOCUMENT
from bs4 import BeautifulSoup


# --------------------
# Einstellungen
# --------------------


###
print("CUDA:", torch.cuda.is_available())


if torch.cuda.is_available():
    print("Gerät:", torch.cuda.get_device_name(0))

###



if len(sys.argv) < 2:
    print("Aufruf: python3 tts2.py datei.pdf/epub/txt stimme_name_ohne_endung ")
    exit()

datei = sys.argv[1]
auswahl = sys.argv[2]

basis = os.path.splitext(datei)[0]

FINAL = basis + ".wav"
TEXTDATEI = basis + ".txt"

endung = os.path.splitext(datei)[1].lower()

PDF = datei
EPUB = datei

####################################################




VOICE = "stimmen/"+ auswahl+".wav"

if not os.path.exists(VOICE):
    print("Stimme fehlt. als 2 parameter übergeben nur name", VOICE)
    exit()




LANGUAGE = "german_24l"

BLOCK_GROESSE = 80
GESCHWINDIGKEIT = 0.60

text = ""

 
#########################################################
if endung == ".epub":
    print("Lese:", EPUB)
    
    
    buch = epub.read_epub(EPUB)
    
   
    
    
    for item in buch.get_items():
    
        if item.get_type() == ITEM_DOCUMENT:
    
            html = item.get_content()
    
            soup = BeautifulSoup(
                html,
                "html.parser"
            )
    
            seite = soup.get_text(
                "\n",
                strip=True
            )
    
            text += seite + "\n\n"
    
    
    # einfache Bereinigung
    
    text = text.replace("\xa0", " ")
    
    while "\n\n\n" in text:
        text = text.replace(
            "\n\n\n",
            "\n\n"
        )
    
    
    with open(TEXTDATEI, "w", encoding="utf-8") as f:
        f.write(text)
    
#######################################################

if endung == ".pdf":
    
    
    print("Lese PDF...")
    reader = PdfReader(PDF)
    text = ""
    for i, seite in enumerate(reader.pages):
        print("Seite", i + 1)
    
        seiten_text = seite.extract_text()
    
        if seiten_text:
            text += seiten_text + "\n\n"
    
    
    
    print("Bereinige Text...")
    
    # Trennstriche am Zeilenende entfernen
    text = re.sub(r"-\n", "", text)
    
    # einzelne Zeilen zusammenführen
    text = re.sub(r"(?<!\n)\n(?!\n)", " ", text)
    
    # Mehrfach-Leerzeichen entfernen
    text = re.sub(r"[ \t]+", " ", text)
    
    # zu viele Leerzeilen reduzieren
    text = re.sub(r"\n{3,}", "\n\n", text)
    
    
    with open(TEXTDATEI, "w", encoding="utf-8") as f:
        f.write(text)
    
###
if endung == ".txt":

    print("Lese TXT...")

    TEXTDATEI = datei

    with open(TEXTDATEI, "r", encoding="utf-8") as f:
        text = f.read()








print("Datei:", TEXTDATEI)
print("Existiert:", os.path.exists(TEXTDATEI))
print("Größe:", os.path.getsize(TEXTDATEI), "Bytes")


# --------------------
# Pocket TTS laden
# --------------------

print("Lade Modell...")

tts_model = TTSModel.load_model(
    language=LANGUAGE
)

print("Lade Stimme...")

voice_state = tts_model.get_state_for_audio_prompt(
    VOICE
)


print(tts_model.device)

# --------------------
# Text aufteilen
# --------------------

teile = []


###### limitiern auf 20 zeilen


#text = text[:10000]
print("Testtext:", text)

########


rest = text

while len(rest) > 0:

    block = rest[:BLOCK_GROESSE]

    pos = max(
        block.rfind("."),
        block.rfind("!"),
        block.rfind("?"),
        block.rfind(","),
        block.rfind(" ")
    )
    
    if pos > 50:
        block = block[:pos+1]

    original_laenge = len(block)

    block = block.strip()

    if block:
        teile.append(block)

    rest = rest[original_laenge:]


print("Anzahl Textteile:", len(teile))

# --------------------
# Sprache erzeugen
# --------------------

with sf.SoundFile(
    FINAL,
    mode="w",
    samplerate=tts_model.sample_rate,
    channels=1,
    subtype="FLOAT"
) as wav:

    for i, teil in enumerate(teile):

        print(
            f"Erzeuge Teil {i+1}/{len(teile)} "
            f"({len(teil)} Zeichen)"
        )

        for audio in tts_model.generate_audio_stream(
            model_state=voice_state,
            text_to_generate=teil,
            max_tokens=100
        ):
        
            #print("AUDIO:")
            #print(type(audio))
        
            #if hasattr(audio, "shape"):
                #print("Shape:", audio.shape)
        
            #print("MIN:", audio.min().item())
            #print("MAX:", audio.max().item())
            
            audio = audio / GESCHWINDIGKEIT
            daten = audio.detach().cpu().numpy()
            
            wav.write(
                daten.reshape(-1, 1)
            )
print()
print("Fertig:")
print(FINAL)





































