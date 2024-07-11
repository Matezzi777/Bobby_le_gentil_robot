import random
import sqlite3
import datetime
import discord

#Tire un mot au hasard du nombre de lettres spécifié
def get_word(nb_lettres: int) -> str:
    dictionnaire = open("assets/dictionnaire_fr.txt", "r")
    content = dictionnaire.read()
    mot: str = ""
    while (len(mot) != nb_lettres):
        mot = ""
        indice: int = random.randint(0, 78854)
        i: int = 0
        nb_return: int = 0
        while (nb_return < indice):
            if (content[i] == '\n'):
                nb_return = nb_return + 1
            i = i + 1
        while (content[i] != '\n' and content[i != '\0']):
            mot = f"{mot}{content[i]}"
            i = i + 1
    dictionnaire.close()
    return (mot)

#Génère une grille de ⬛ de nb_lettres de large et nb_essais de hauteur
def initialize_embed_content(nb_lettres: int, nb_essais: int) -> list[str]:
    content_tab : list[str] = []
    i: int = 0
    while (i < nb_essais):
        j: int = 0
        new_line: str = ""
        while (j < nb_lettres):
            new_line = f"⬛ {new_line}"
            j = j + 1
        content_tab.append(new_line)
        i = i + 1
    return (content_tab)

#Récupère une string à afficher à partir de la liste de strings
def get_str_from_list(embed_content: list[str]) -> str:
    i: int = 0
    nb_lines: int = len(embed_content)
    result: str = ""
    while (i < nb_lines):
        result = f"{result}{embed_content[i]}\n"
        i = i + 1
    return (result)

#Vérifie la présence d'un mot dans le dictionnaire
def is_word_in_dict(mot: str) -> bool:
    dictionnaire = open("assets/dictionnaire_fr.txt", "r")
    lines = dictionnaire.readlines()
    for line in lines:
        if (line == f"{mot}\n"):
            return True
    return False

#Renvoit une liste contenant chaque lettre du mot
def get_list_from_word(mot: str) -> list[str]:
    liste : list[str] = []
    i: int = 0
    while (i < len(mot)):
        liste.append(mot[i])
        i = i + 1
    return (liste)

#Renvoit un code 🟨🟩 en fonction de la réponse proposée, "INVALIDE" si la réponse n'est pas valide ou "MISSING" si la proposition n'est pas dans le dictionnaire.
def check_guess_validity(guess: str, mot: str) -> str:
    tab_mot : list[str] = get_list_from_word(mot)
    if (len(guess) != len(mot)):
        return ("INVALIDE")
    if (not is_word_in_dict(guess)):
        return ("MISSING")
    if (guess == mot):
        return ("FOUND")
    i: int = 0
    while (i < len(guess)):
        if (tab_mot[i] == guess[i]):
            tab_mot.pop(i)
            tab_mot.insert(i, "")
        i = i + 1
    string: str = ""
    i = 0
    while (i < len(guess)):
        if (guess[i] == mot[i]):
            string = f"{string}🟩 "
        elif (guess[i] in tab_mot):
            string = f"{string}🟨 "
            index: int = tab_mot.index(guess[i])
            tab_mot.pop(index)
            tab_mot.insert(index, "")
        else:
            string = f"{string}⬛ "
        i = i + 1
    string = f"{string} --- {guess}"
    return (string)

#Met à jour les stats du joueur
def update_wordle_stats(author: discord.User, result: str):
    #Si le joueur n'es pas dans la BDD, crée une entrée formattée pour lui
    if (not is_user_in_db(author, "Wordle")):
        add_user_in_wordle_db(author)
    update_user_wordle_stat(author, "Played")
    update_user_wordle_stat(author, result)
    update_user_wordle_stat(author, "LastGame")
    return

#Vérifie la présence d'un utilisateur dans la base de donnée Wordle
def is_user_in_db(user: discord.User, table: str) -> bool:
    connexion = sqlite3.connect('db_stats.sqlite')
    cursor = connexion.cursor()
    request : str = f"SELECT * FROM {table} WHERE User_ID='{user.id}'"
    cursor.execute(request)
    result : int = cursor.fetchone()
    connexion.close()
    if result:
        return True
    else:
        return False

#Ajoute un nouvel utilisateur avec des valeurs par défaut à la base de donnée Wordle
def add_user_in_wordle_db(user: discord.User) -> int:
    if (is_user_in_db(user, "Wordle")):
        print(f"  {user.name} already stored in the database.")
        return (0)
    else:
        connexion = sqlite3.connect('db_stats.sqlite')
        cursor = connexion.cursor()
        request : str = f"INSERT INTO Wordle VALUES ('{user.id}', 0, 0, 0, 0, '00000000')"
        cursor.execute(request)
        connexion.commit()
        connexion.close()
        if (is_user_in_db(user, "Wordle")):
            print(f"  {user.name} added to Wordle database.")
            return (1)
        else:
            print(f"  Error in the INSERT request.")
            return (0)
        
#Met à jour une statistique spécifique du joueur dans la table Wordle
def update_user_wordle_stat(user: discord.User, stat: str) -> None:
    if (stat == "LastGame"):
        date = get_parsed_date()
        connexion = sqlite3.connect('db_stats.sqlite')
        cursor = connexion.cursor()
        request: str = f"UPDATE Wordle SET {stat}='{date}' WHERE User_ID='{user.id}'"
        cursor.execute(request)
        connexion.commit()
        connexion.close()
        return
    elif (stat == "Played" or stat == "Victory" or stat == "Lose" or stat == "GiveUp"):
        stat_value : int = int(get_user_wordle_stat(user, stat))
        stat_value = stat_value + 1
        connexion = sqlite3.connect('db_stats.sqlite')
        cursor = connexion.cursor()
        request: str = f"UPDATE Wordle SET {stat}='{stat_value}' WHERE User_ID='{user.id}'"
        cursor.execute(request)
        connexion.commit()
        connexion.close()
        return
    else:
        print(f"    Statistique {stat} introuvable dans la table Wordle.")
        return

#Récpère la valeur d'une statistique du joueur dans la table Wordle
def get_user_wordle_stat(user: discord.User, stat: str) -> str:
    connexion = sqlite3.connect('db_stats.sqlite')
    cursor = connexion.cursor()
    request: str = f"SELECT {stat} FROM Wordle WHERE User_ID='{user.id}'"
    cursor.execute(request)
    connexion.commit()
    value : str = str(cursor.fetchone()[0])
    connexion.close()
    return (value)

#Récupère la date d'aujourd'hui et la renvoit sous forme de string de format DDMMYYYY
def get_parsed_date() -> str:
    today: str = datetime.date.today().isoformat()
    day: str = f"{today[8]}{today[9]}"
    month: str = f"{today[5]}{today[6]}"
    year: str = f"{today[0]}{today[1]}{today[2]}{today[3]}"
    return (f"{day}{month}{year}")