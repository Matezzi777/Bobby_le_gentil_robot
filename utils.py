import random
import datetime

def random_pick_str(liste:list[str]) -> str:
	return (liste[random.randint(0, len(liste)-1)])

#Récupère la date d'aujourd'hui et la renvoit sous forme de string de format DDMMYYYY
def get_parsed_date() -> str:
    today: str = datetime.date.today().isoformat()
    day: str = f"{today[8]}{today[9]}"
    month: str = f"{today[5]}{today[6]}"
    year: str = f"{today[0]}{today[1]}{today[2]}{today[3]}"
    return (f"{day}{month}{year}")