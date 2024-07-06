import sqlite3
from random import randint

#Distribue les civilizations
def create_draft(players : int, nb_civs : int) -> list:
    i = 0
    draft = []
    
    while (i < players):
        j = 0
        while (j < nb_civs):
            id = 0
            while (id == 0 or is_n_in_list(id, draft)):
                id : int = randint(1, 77)
            draft.append(id)
            j = j + 1
        i = i + 1
    return (draft)

#Récupère l'émote associée à l'id d'un leader
def emote_from_id(id : int) -> str:
    connexion = sqlite3.connect('db_leaders.sqlite')
    cursor = connexion.cursor()
    request : str = "SELECT Emoji FROM Leaders WHERE ID="+str(id)
    cursor.execute(request)
    connexion.commit()
    result = cursor.fetchone()
    connexion.close()
    return (trim(str(result)))

#Récupère le nom associé à l'id d'un leader
def leader_from_id(id : int) -> str:
    connexion = sqlite3.connect('db_leaders.sqlite')
    cursor = connexion.cursor()
    request : str = "SELECT Name FROM Leaders WHERE ID="+str(id)
    cursor.execute(request)
    connexion.commit()
    result = cursor.fetchone()
    connexion.close()
    return (trim(str(result)))

#Formate le résultat de la requète SQL
def trim(s : str) -> str:
    result = ""
    i = 0
    while (i < len(s)):
        if (not (s[i] == "(" or s[i] == "'" or s[i] == "," or s[i] == ")")):
            result = result + s[i]
        i = i + 1
    return (result)

#Vérifie la présence d'un élément dans la draft
def is_n_in_list(id : int, liste_totale : list) -> bool:
    i = 0
    while (i < len(liste_totale)):
        if (liste_totale[i] == id):
            return True
        i = i + 1
    return False