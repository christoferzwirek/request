# -*- coding: utf-8 -*-
"""
Created on Wed Jun  7 16:30:07 2023

@author: wr49442
"""
#from .formats import JSON
import requests,json



r = requests.get('https://lichess.org/api/user/radek8640',
                 headers={'Authorization': 'lip_4M09fZ192Ysehbmnhh26',
                          "Accept": "application/x-ndjson"})
print(r)
#print(r.text)
data=r.json()
#text=r.text
print(data['perfs']['bullet']['rating'])
print(data['perfs']['blitz']['rating'])
print(data['perfs']['rapid']['rating'])
token='lip_4M09fZ192Ysehbmnhh26'
#print(r.request)





def get_user_games(username,nr,tr=None):
    url = f"https://lichess.org/api/games/user/{username}"
    headers = {
        "Accept": "application/x-ndjson"  # Zmiana nagłówka na "application/x-ndjson"
    }
    params={"max":f"{nr}","pgnInJson":"true",
    "username":"radek8640",
    "rated":"true",
    "speed":"{tr}"}
    response = requests.get(url, headers=headers,params=params)
    if response.status_code == 200:
        games = []
        lines = response.text.split("\n")
        for line in lines:
            if line:
                game = json.loads(line)
                games.append(game)
        return games
    else:
        
        print(f"Request failed with status code {response.status_code}")
        return None

# Przykładowe użycie
#AinsOowl
#radek8640
username =input("podaj nazwę użytkownika ")
nr=3
tr="bullet"

user_games = get_user_games(username,nr)
if user_games:
    print(f"Number of games for {username}: {len(user_games)}")
    for słownik in user_games:
        for klucz, wartość in słownik.items():
            if(klucz=='speed'):
                print(f"\ntępo: {wartość}")
            if(klucz=='moves'):
                print(f"ruchy: {wartość}")


def get_game_id(username, access_token):
    url = f"https://lichess.org/api/user/{username}/activity"
    headers = {
        "Authorization": f"Bearer {access_token}"
    }

    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        activity_feed = response.json()
        for entry in activity_feed:
            print(entry)
            if "games" in entry:
                game_id = entry["games"]["id"]
                return game_id
        print("No game found in the activity feed.")
    else:
        print(f"Failed to retrieve user activity. Status code: {response.status_code}")

# Usage example



#game_id = get_game_id(username,token)
params = {
    'time': 10,
    'increment': 5,
    'variant': 'standard',
    'color': 'white',
    'level':'1'
}
headers={'Authorization': f'Bearer {token}',
           "Accept": "application/x-ndjson",
           
           }
#print("elo1")
response = requests.post('https://lichess.org/api/challenge/ai', headers=headers, data=params)
#print(response)
seek_id=None
data=[]
if response.status_code == 201:
    data = response.json()
    #print(data["id"])
    seek_id = data['id']
    print(f"Seek successfully created with ID: {seek_id}")
else:
    print(f"Failed to create the seek.{response.json()}")

#print(f"Game ID: {seek_id}")


def make_move(game_id, move, access_token):
    
    if move=="q":
        url=f"https://lichess.org/api/board/game/{game_id}/abort"
        headers = {
            "Authorization": f"Bearer {access_token}",
        }
        requests.post(f"https://lichess.org/api/board/game/{game_id}/resign",headers=headers)
        requests.post(url, headers=headers)
        return 0;
    else:
        url = f"https://lichess.org/api/board/game/{game_id}/move/{move}"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "scopes":"board:play",
        "userId": "radek8640",
        "Content-Type": "application/json"
    }
      
    
    response = requests.post(url, headers=headers)
    if response.status_code == 200:
        print("Move successfully made!")
    else:
        #h=requests.post(f"https://lichess.org/api/bot/game/{game_id}/abort", headers=headers,params=params)
        #print(h.json
        print(f"Failed to make the move. Status code: {response.json()}")

move="c2c4"
while(move!="q"):
    move=input("podaj ruch ")
    make_move(seek_id, move, token)





