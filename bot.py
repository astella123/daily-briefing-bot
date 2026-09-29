import os
import json
from datetime import datetime
import requests
import unicodedata

# 1. Carica le variabili d'ambiente
BOT_TOKEN = os.environ['BOT_TOKEN']
CHAT_ID = os.environ['CHAT_ID']

# 2. Carica il calendario
with open('schedule.json', 'r', encoding='utf-8') as f:
    schedule = json.load(f)

# 3. Scopri che giorno è oggi (blindata: ignora gli accenti)
def normalizza(testo):
    return ''.join(
        c for c in unicodedata.normalize('NFD', testo)
        if unicodedata.category(c) != 'Mn'
    )

giorni_chiave   = ["Lunedi", "Martedi", "Mercoledi", "Giovedi", "Venerdi", "Sabato", "Domenica"]
giorni_display  = ["Lunedì", "Martedì", "Mercoledì", "Giovedì", "Venerdì", "Sabato", "Domenica"]

indice         = datetime.today().weekday()
oggi_display   = giorni_display[indice]
oggi_chiave    = normalizza(giorni_chiave[indice])
schedule_norm  = {normalizza(k): v for k, v in schedule.items()}

# 4. Prepara il messaggio del calendario
messaggio = f"📅 *Buongiorno André - {oggi_display}*\n\n"

if oggi_chiave in schedule_norm:
    for item in schedule_norm[oggi_chiave]:
        messaggio += f"🕐 {item['ora']}\n📌 {item['testo']}\n\n"
else:
    messaggio += "Nessuna attività specifica programmata.\n\n"

# 5. Aggiungi la frase motivazionale
motivational_quotes = [
    "Ogni giorno è una nuova opportunità per costruire il tuo impero. 🚀",
    "La disciplina batte il talento quando il talento non ha disciplina. 💪",
    "Piccoli passi quotidiani portano a grandi risultati. 🎯",
    "Il successo è la somma di piccoli sforzi ripetuti giorno dopo giorno. 🔥",
    "Oggi è il giorno perfetto per fare un passo avanti. ⚡",
]

day_of_year = datetime.now().timetuple().tm_yday
quote = motivational_quotes[day_of_year % len(motivational_quotes)]
messaggio += f"✨ _{quote}_"

# 6. Invia il messaggio su Telegram
url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
payload = {
    "chat_id": CHAT_ID,
    "text": messaggio,
    "parse_mode": "Markdown"
}
requests.post(url, json=payload)
