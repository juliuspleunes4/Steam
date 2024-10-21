from dotenv import load_dotenv
import os
import tkinter as tk
import requests

# API key moet nog worden aangepast
load_dotenv()
API_KEY = os.getenv('STEAM_API_KEY')  # laadt de API key vanuit de .env bestand

# vast steam id (ons steam project account)
STEAM_ID = '76561198209282153'  

# haalt user data op van Steam
def get_steam_user_data(steam_id):
    url = f"http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key={API_KEY}&steamids={steam_id}"
    response = requests.get(url)
    data = response.json()
    if 'players' in data['response'] and len(data['response']['players']) > 0:
        return data['response']['players'][0]['personaname']  # haalt username op
    else:
        return "Geen gegevens gevonden"

# GUI instellen
root = tk.Tk()
root.title("Steam Dashboard")

# functie om username te tonen
def display_user_data():
    user_name = get_steam_user_data(STEAM_ID)  # Gebruik vast Steam ID
    result_label.config(text=f"Gebruikersnaam: {user_name}")

# componenten voor interface
get_data_button = tk.Button(root, text="Haal data op", command=display_user_data)
get_data_button.pack()

result_label = tk.Label(root, text="")
result_label.pack()

root.mainloop()
