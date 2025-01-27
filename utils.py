import requests

def spazio():
    r = requests.get('http://api.open-notify.org/astros.json')
    if r.status_code == 200:
        return r.json()
    else:
        return (f"Errore {r.status_code}")
        
def gatto():
    r = requests.get('https://catfact.ninja/fact')
    if r.status_code == 200:
        return r.json() 
    else:
        return (f"Errore {r.status_code}")