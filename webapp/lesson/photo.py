from flask import current_app
import requests 

def get_photo(query):
    try:
        res = requests.get(f"https://api.unsplash.com/search/photos?page=1&query={query}",
                    headers={"Authorization": f'Client-ID {current_app.config["YOUR_ACCESS_KEY"]}'}
                    ).json()
        return res['results'][2]['urls']['thumb']
    except:
        return "https://images.unsplash.com/photo-1530908295418-a12e326966ba?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=Mnw0MzU2MTl8MHwxfHNlYXJjaHwyfHxhaXJ8ZW58MHx8fHwxNjgxNDE2MzM5&ixlib=rb-4.0.3&q=80&w=200"

