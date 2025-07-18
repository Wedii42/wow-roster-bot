from flask import Flask
import threading
import bot  # <- ton fichier bot.py doit contenir la fonction run_bot()

app = Flask(__name__)

@app.route('/')
def home():
    return "Bot Discord WoW actif 🎮"

def start_bot():
    bot.run_bot()  # <- cette fonction doit être définie dans bot.py

if __name__ == '__main__':
    threading.Thread(target=start_bot).start()
    app.run(host='0.0.0.0', port=8080)
