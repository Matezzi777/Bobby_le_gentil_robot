import random

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
