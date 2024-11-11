from dotenv import load_dotenv
import os
import tkinter as tk
import requests

# momenteel heeft het nog een vast api key. Later willen we implementeren dat je een api key kan invoeren en dan haalt hij het op
load_dotenv()
API_KEY = os.getenv('STEAM_API_KEY')  # laadt de API key vanuit de .env bestand

# vast steam id (van Julius' account)
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


# GUI instellen met achtergrondkleur en titel
root = tk.Tk()
root.title("Steam Dashboard")
root.configure(bg="#282C34")  # donkergrijze achtergrondkleur
root.geometry("400x400")  # resolutie gefixeerd op 400x400

# friendlist ophalen
def get_friend_list(steam_id):
    url = f"http://api.steampowered.com/ISteamUser/GetFriendList/v0001/?key={API_KEY}&steamid={steam_id}&relationship=friend"
    response = requests.get(url)
    data = response.json()
    
    if 'friendslist' in data and len(data['friendslist']['friends']) > 0:
        return data['friendslist']['friends']  # lijst van vrienden
    else:
        return []

# controleert of vriend online is
def get_friend_status(friend_ids):
    online_friends = 0
    for friend in friend_ids:
        url = f"http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key={API_KEY}&steamids={friend['steamid']}"
        response = requests.get(url)
        data = response.json()
        
        if 'players' in data['response'] and len(data['response']['players']) > 0:
            player = data['response']['players'][0]
            if player['personastate'] == 1:  # 1 betekent online
                online_friends += 1
    return online_friends

# functie om username te tonen
def display_user_data():
    # haalt gebruikersnaam op
    user_name = get_steam_user_data(STEAM_ID)
    
    # haalt vriendenlijst op
    friends = get_friend_list(STEAM_ID)
    total_friends = len(friends)
    
    # haalt aantal vrienden online op
    online_friends = get_friend_status(friends)
    
    # update GUI met de data
    user_label.config(
        text=f"{user_name}",  
        fg="white", font=("Helvetica", 18, "bold")  
    )
    
    result_label.config(
        text=f"Totaal aantal vrienden: {total_friends}\nVrienden online: {online_friends}",
        fg="white", font=("Helvetica", 12)  
    )


# knop
get_data_button = tk.Button(root, text="Haal data op", command=display_user_data, 
                            bg="#61AFEF", fg="white", font=("Helvetica", 12, "bold"), 
                            relief="raised", bd=5)  # blauwachtige knop
get_data_button.pack(pady=20)

# stijl voor de gebruikersnaam als soort koptekst
user_label = tk.Label(root, text="", bg="#282C34", fg="white", font=("Helvetica", 18, "bold"))  # grotere tekst voor gebruikersnaam
user_label.pack(pady=10)

# stijl voor het label met de resultaten
result_label = tk.Label(root, text="", bg="#282C34", fg="white", font=("Helvetica", 12))  # grotere tekst voor vriendeninformatie
result_label.pack(pady=10)

# start de applicatie
root.mainloop()
