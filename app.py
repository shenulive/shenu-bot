from flask import Flask, request
import requests, os
app = Flask(__name__)

VERIFY_TOKEN = os.environ.get("VERIFY_TOKEN", "shenu123")
ACCESS_TOKEN = os.environ.get("ACCESS_TOKEN")
PHONE_NUMBER_ID = os.environ.get("PHONE_NUMBER_ID")
OWNER_NUMBER = "94722472083" # ඔයාගේ number එක

MENU = """🔥 *SHENU LIVE ACC STORE* 🔥
Welcome machan!

📦 *Items:*
1️⃣ FREE FIRE ACCOUNT - Price inbox
2️⃣ FACEBOOK PAGE - Followers අනුව
3️⃣ TIKTOK PAGE - Followers අනුව
4️⃣ YOUTUBE CHANNEL - Subs අනුව

Order දාන්න මේ විදිහට type කරන්න:
Ex: `FF Acc ekak ona`
Ex: `FB Page 10k`
Ex: `YT Channel monetized`

Price list eka ewanna 'price' kiyala type karanna.
"""

def send(to, text):
    url = f"https://graph.facebook.com/v20.0/{PHONE_NUMBER_ID}/messages"
    headers = {"Authorization": f"Bearer {ACCESS_TOKEN}"}
    data = {"messaging_product":"whatsapp","to":to,"type":"text","text":{"body":text}}
    requests.post(url, headers=headers, json=data)

@app.route("/webhook", methods=["GET"])
def verify():
    if request.args.get("hub.verify_token") == VERIFY_TOKEN:
        return request.args.get("hub.challenge")
    return "fail"

@app.route("/webhook", methods=["POST"])
def hook():
    try:
        val = request.json['entry'][0]['changes'][0]['value']
        if 'messages' in val:
            m = val['messages'][0]
            frm = m['from']
            txt = m['text']['body'].lower()

            if any(x in txt for x in ["hi","hello","menu","oy","mcn"]):
                send(frm, MENU)

            elif "price" in txt:
                send(frm, "💰 *Price List*\n\nFF Acc - Rs.3500 ඉදන්\nFB Page 10k - Rs.5000\nTikTok 10k - Rs.6000\nYT 1k Subs - Rs.8000\n\nExact price එකට acc eka kiyanna, ss ekak ewannam.")

            elif any(x in txt for x in ["ff","free fire","fb","facebook","tiktok","tt","youtube","yt"]):
                send(frm, f"Super! {m['text']['body']} එක note kala ✅\n\nBudget eka kiyada? Saha payment method eka - Bank / USDT?")
                # ඔයාට notification එකක්
                send(OWNER_NUMBER, f"🔔 NEW ORDER - SHENU LIVE\nFrom: {frm}\nWants: {m['text']['body']}")

            else:
                # address / budget වගේ දෙයක් දැම්මම
                if len(txt) > 5:
                    send(frm, f"Got it! ✅\n\nOrder: {txt}\n\nMama tikakin ss saha details ewannam. Payment eka confirm karala acc eka denna puluwan. - SHENU LIVE")
                    send(OWNER_NUMBER, f"🔔 Customer Reply\nFrom: {frm}\nMsg: {m['text']['body']}")

    except Exception as e:
        print(e)
    return "ok", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
