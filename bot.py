import requests
import json
import os
from datetime import datetime

# 1. Credenziali (ora le prendiamo dalla cassaforte di GitHub)
TOKEN = os.environ.get('TELEGRAM_TOKEN')
chat_id = "8582302114"
GNEWS_API_KEY = os.environ.get('GNEWS_API_KEY')

# 2. Leggi il calendario
with open("schedule.json", encoding="utf-8") as file:
    schedule = json.load(file)

# 3. Scopri che giorno è oggi
giorni = ["Lunedì", "Martedì", "Mercoledì", "Giovedì", "Venerdì", "Sabato", "Domenica"]
oggi = giorni[datetime.today().weekday()]

# 4. Prepara il messaggio del calendario
messaggio = f"📅 *Buongiorno André - {oggi}*\n\n"

if oggi in schedule:
    for item in schedule[oggi]:
        messaggio += f"⏰ {item['ora']}\n"
        messaggio += f"📌 {item['testo']}\n\n"
else:
    messaggio += " Nessuna attività specifica programmata.\n\n"

# 5. Recupera le News (Geopolitica/Mondo/Mercati)
messaggio += "🌍 *NEWS DEL GIORNO*\n"
url_news = f"https://gnews.io/api/v4/top-headlines?country=it&category=general&lang=it&max=5&apikey={GNEWS_API_KEY}"

try:
    risposta_news = requests.get(url_news)
    print(f"Status code GNews: {risposta_news.status_code}")
    print(f"Risposta grezza: {risposta_news.text[:200]}")
    
    articoli = risposta_news.json().get("articles", [])
    print(f"Numero articoli trovati: {len(articoli)}")
    
    # Filtra duplicati e prendi solo i primi 3 unici
    titoli_visti = set()
    conteggio = 1
    
    for articolo in articoli:
        titolo = articolo.get("title", "Senza titolo")
        if titolo in titoli_visti:
            continue
            
        titoli_visti.add(titolo)
        descrizione = articolo.get("description", "")
        url_articolo = articolo.get("url", "")
        
        messaggio += f"{conteggio}. *{titolo}*\n"
        if descrizione:
            messaggio += f"   {descrizione}\n"
        if url_articolo:
            messaggio += f"   🔗 [Leggi tutto]({url_articolo})\n"
        messaggio += "\n"
        
        conteggio += 1
        if conteggio > 3:
            break
            
    if conteggio == 1:
        messaggio += "Nessuna news trovata oggi.\n"
        
except Exception as e:
    messaggio += f"️ Errore nel recupero news: {str(e)}\n"

# 6. Invia a Telegram
url_telegram = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
dati = {
    "chat_id": chat_id,
    "text": messaggio,
    "parse_mode": "Markdown"
}

risposta = requests.post(url_telegram, json=dati)
print(risposta.json())
