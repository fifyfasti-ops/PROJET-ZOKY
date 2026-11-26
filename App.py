from flask import Flask, request
import requests

app = Flask(__name__)

# --- CONFIG ---
VERIFY_TOKEN = "legion2024"
ACCESS_TOKEN = "COLLE_ICI_TON_JETON_EAA..."  # Le gros jeton de Étape 1
PHONE_NUMBER_ID = "1468134532128867"
# --- FIN CONFIG ---

# --- TES 6 CATEGORIES - MODIFIE ICI ---
# C'est ici que tu mets tes vrais textes de La Légion

def send_whatsapp(to, payload):
    url = f"https://graph.facebook.com/v20.0/{PHONE_NUMBER_ID}/messages"
    headers = {"Authorization": f"Bearer {ACCESS_TOKEN}", "Content-Type": "application/json"}
    r = requests.post(url, headers=headers, json=payload)
    print("META RESPONSE:", r.text)
    return r

def send_menu(to):
    # Menu principal avec boutons liste (parfait pour 6 catégories)
    payload = {
        "messaging_product": "whatsapp",
        "to": to,
        "type": "interactive",
        "interactive": {
            "type": "list",
            "body": {"text": "Salama ! Bienvenue à La Légion 👋\nChoisissez une catégorie:"},
            "footer": {"text": "La Légion - Antananarivo"},
            "action": {
                "button": "Voir les 6 catégories",
                "sections": [{
                    "title": "Nos services",
                    "rows": [
                        {"id": "CAT_1", "title": "1. Présentation", "description": "Qui est La Légion ?"},
                        {"id": "CAT_2", "title": "2. Formations", "description": "Liste des formations"},
                        {"id": "CAT_3", "title": "3. Inscription", "description": "Comment s'inscrire"},
                        {"id": "CAT_4", "title": "4. Tarifs", "description": "Nos prix"},
                        {"id": "CAT_5", "title": "5. Localisation", "description": "Où nous trouver"},
                        {"id": "CAT_6", "title": "6. Humain", "description": "Parler à un conseiller"}
                    ]
                }]
            }
        }
    }
    send_whatsapp(to, payload)

def send_reponse(to, cat_id):
    reponses = {
        "CAT_1": "📚 *La Légion* est un centre de formation d'anglais à Tana depuis... \n\nTapez MENU pour revenir.",
        "CAT_2": "🎓 *Formations*:\n- Débutant\n- Intermédiaire\n- Avancé\n- IELTS\n\nTapez MENU.",
        "CAT_3": "📝 *Inscription*: CIN + photo + frais. Prochaine rentrée: Décembre.\nTapez MENU.",
        "CAT_4": "💰 *Tarifs*: à partir de 150k Ar/mois. Réduction si paiement complet.\nTapez MENU.",
        "CAT_5": "📍 *Antananarivo* - Près de... Horaires 8h-17h. Google Maps: [lien]\nTapez MENU.",
        "CAT_6": "👤 Un conseiller va vous répondre sur ce numéro 0332603059. Laissez votre nom svp."
    }
    text = reponses.get(cat_id, "Catégorie non trouvée. Tapez MENU")
    payload = {
        "messaging_product": "whatsapp",
        "to": to,
        "type": "text",
        "text": {"body": text}
    }
    send_whatsapp(to, payload)

@app.route("/webhook", methods=["GET"])
def verify():
    if request.args.get("hub.verify_token") == VERIFY_TOKEN:
        return request.args.get("hub.challenge")
    return "Erreur token", 403

@app.route("/webhook", methods=["POST"])
def incoming():
    data = request.get_json()
    print(data)
    try:
        value = data["entry"][0]["changes"][0]["value"]
        if "messages" in value:
            msg = value["messages"][0]
            from_number = msg["from"]
            
            # Si bouton cliqué
            if msg.get("type") == "interactive":
                cat_id = msg["interactive"]["list_reply"]["id"]
                send_reponse(from_number, cat_id)
            else:
                body = msg.get("text", {}).get("body", "").lower()
                if body in ["bonjour","salut","menu","hello","0"]:
                    send_menu(from_number)
                else:
                    send_menu(from_number)
    except Exception as e:
        print(f"Erreur: {e}")
    return "OK", 200

@app.route("/")
def home():
    return "Bot La Legion OK"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)