import discord
import discord.ui
import sqlite3
from classes import *
from utils import *

ELO_NEW_PLAYER = 1200
THETA = 400

############ VIEWS ############
class ReportView(discord.ui.View):
    def __init__(self, embed, players: list[discord.Member]):
        super().__init__(timeout=None)
        self.embed = embed
        self.players: list[discord.Member] = players
        self.result: list[discord.Member] = []
        self.add_item(SelectPlayer(self.players, 1))

########### SELECTS ###########
class SelectPlayer(discord.ui.Select):
    def __init__(self, players: list[discord.Member], n: int):
        super().__init__(
            placeholder=f"Select the player as top{n}."
        )
        self.n = n
        for player in players:
            self.add_option(label=f"@{player.name}", value=f"{player.id}", description=f"Select @{player.name} as top{n}.")

    async def callback(self, interaction: discord.Interaction):
        chosen_member: discord.Member = interaction.guild.get_member(int(self.values[0]))
        self.view.result.append(chosen_member)
        self.view.players.remove(chosen_member)
        embed_content: str = ""
        i: int = 1
        for user in self.view.result:
            embed_content = f"{embed_content}- **{i} :** {user.mention}\n"
            i += 1
        new_embed = BotEmbed(title="REPORT", description=embed_content)
        self.view.children.pop(0)
        self.view.clear_items()
        if (len(self.view.players)!=0):
            self.view.add_item(SelectPlayer(self.view.players, self.n + 1))
        else:
            self.view.add_item(ConfirmReportButton(self.view.result))
            self.view.add_item(RestartReportButton(interaction.user, self.view.result))
            self.view.add_item(CancelReportButton(interaction.user))
        await interaction.response.edit_message(embed=new_embed, view=self.view)

########### BUTTONS ###########
class ConfirmReportButton(discord.ui.Button):
    def __init__(self, result: list[discord.Member]):
        super().__init__(style=discord.ButtonStyle.green,
                         label="Confirm Report",
                         disabled=False,
                         emoji="✅")
        self.users: list[discord.Member] = result

    async def callback(self, interaction: discord.Interaction):
        log_content: str = ""
        embed_content: str = ""
        i: int = 1
        for user in self.users:
            log_content = f"{log_content}        {i} : @{user.name}\n"
            embed_content = f"{embed_content}- **{i} :** {user.mention}\n"
            i += 1
        print(f"    Report validated")
        print(log_content)
        result_embed = BotEmbed(title="REPORT", description="Result confirmed and stored in the database.", colour=discord.Colour.green())
        result_embed.add_field(name="", value=embed_content, inline=False)
        await interaction.response.edit_message(embed=result_embed, view=None)
        store_report(self.users)
class RestartReportButton(discord.ui.Button):
    def __init__(self, user: discord.Member, players: list[discord.Member]):
        super().__init__(style=discord.ButtonStyle.blurple,
                         label="Restart",
                         disabled=False,
                         emoji="♻️")
        self.user: discord.Member = user
        self.players: list[discord.Member]= players

    async def callback(self, interaction: discord.Interaction):
        embed = BotEmbed(title="REPORT", description=f"Please follow the process to complete the report of this game for *{len(self.players)} players*.")
        await interaction.response.edit_message(embed=embed, view=ReportView(embed, self.players))
class CancelReportButton(discord.ui.Button):
    def __init__(self, user: discord.Member):
        super().__init__(style=discord.ButtonStyle.red,
                         label="Cancel",
                         disabled=False,
                         emoji="✖️")
        self.user: discord.Member = user

    async def callback(self, interaction: discord.Interaction):
        print(f"    Report Canceled")
        cancel_embed = BotEmbed(title="REPORT CANCELED", description="Report attempt aborted. Please use */report* again if you finaly want to make a report.", colour=discord.Colour.red())
        await interaction.response.edit_message(embed=cancel_embed, view=None)

############ FONCTIONS ############
def store_report(users: list[discord.Member]):
    nb_players: int = len(users)
    actual_elos: list[int] = []
    for user in users: #Vérifie la présence de chaque utilisateur dans la base de données
        if (not is_player_in_civ_database(user)):
            add_user_in_civ_database(user)
        actual_elos.append(get_civ_elo(user))
    i: int = 0
    while (i < nb_players): #Mets à jours les Top1, Wins, Lost et Date
        player: discord.Member = users[i]
        if (i == 0):
            if (nb_players > 2):
                update_civ_top1(player)
            update_civ_wins(player)
        elif(i < (nb_players // 2) and nb_players >= 4):
            update_civ_wins(player)
        else:
            update_civ_lost(player)
        update_civ_date(player)
        i += 1
    i: int = 0
    while (i < nb_players): #Mets à jour les Elos
        player: discord.Member = users[i]
        player_actual_elo: int = actual_elos[i]
        elo_variation: int = 0
        games_played_by_user = get_civ_games_played(user)

        if (player_actual_elo >= 2300): #Sélectionne la variation maximale
            max_change: int = 10
        elif (games_played_by_user <= 15):
            max_change: int = 40
        else:
            max_change: int = 20

        j: int = 0
        while (j < nb_players):
            if (i != j):
                if (i < j):
                    result: int = 1
                else:
                    result: int = 0
                opponent_elo: int = actual_elos[j]
                delta: int = player_actual_elo - opponent_elo
                proba_to_win: float = 1 / (1 + 10**(-delta/THETA))
                elo_variation = elo_variation + (max_change * (result - proba_to_win))
            j += 1
        elo_variation: int = elo_variation / (nb_players - 1)
        new_elo: int = round(player_actual_elo + elo_variation)
        update_civ_elo(player, new_elo)
        i += 1
    print(f"    Players' statistics updated.")

def display_civ_user_stats(user: discord.Member) -> str:
    rank: int = get_civ_rank(user)
    elo: int = get_civ_elo(user)
    top: int = get_civ_top1(user)
    wins: int = get_civ_wins(user)
    lost: int = get_civ_lost(user)
    date: str = get_civ_date(user)
    string: str = f"`Rank                 ` : `{rank}`\n`Elo                  ` : `{elo}`\n`Parties jouées       ` : `{wins+lost}`\n`Top 1                ` : `{top}`\n`Victoires            ` : `{wins}`\n`Défaites             ` : `{lost}`\n`Dernière partie jouée` : `{date[0]}{date[1]}/{date[2]}{date[3]}/{date[4]}{date[5]}{date[6]}{date[7]}`"
    return (string)

############ FONCTIONS UTILITAIRES ############
def is_player_in_civ_database(user: discord.Member) -> bool:
    connexion = sqlite3.connect('db_stats.sqlite')
    cursor = connexion.cursor()
    request : str = f"SELECT * FROM CivilizationVI WHERE User_ID='{user.id}'"
    cursor.execute(request)
    result : int = cursor.fetchone()
    connexion.close()
    if result:
        return True
    else:
        return False
def add_user_in_civ_database(user: discord.Member) -> int:
    if (is_player_in_civ_database(user)):
        print(f"    {user.name} already stored in the database.")
        return (0)
    else:
        connexion = sqlite3.connect('db_stats.sqlite')
        cursor = connexion.cursor()
        request : str = f"INSERT INTO CivilizationVI VALUES ('{user.id}', {ELO_NEW_PLAYER}, 0, 0, 0, '00000000')"
        cursor.execute(request)
        connexion.commit()
        connexion.close()
        if (is_player_in_civ_database(user)):
            print(f"    {user.name} added to CivilizationVI database.")
            return (1)
        else:
            print(f"    Error in the INSERT request.")
            return (0)
def get_civ_games_played(user: discord.Member) -> int:
    connexion = sqlite3.connect('db_stats.sqlite')
    cursor = connexion.cursor()
    request_get_win : str = f"SELECT Wins FROM CivilizationVI WHERE User_ID='{user.id}'"
    cursor.execute(request_get_win)
    wins : int = cursor.fetchone()[0]
    request_get_lost : str = f"SELECT Lost FROM CivilizationVI WHERE User_ID='{user.id}'"
    cursor.execute(request_get_lost)
    lost : int = cursor.fetchone()[0]
    games_played : int = wins + lost
    connexion.close()
    return (games_played)
def get_civ_elo(user: discord.Member) -> int:
    connexion = sqlite3.connect('db_stats.sqlite')
    cursor = connexion.cursor()
    request : str = f"SELECT Elo FROM CivilizationVI WHERE User_ID='{user.id}'"
    cursor.execute(request)
    connexion.commit()
    result : int = cursor.fetchone()[0]
    connexion.close()
    return (result)
def get_civ_top1(user : discord.Member) -> int:
    connexion = sqlite3.connect('db_stats.sqlite')
    cursor = connexion.cursor()
    request : str = f"SELECT Top1 FROM CivilizationVI WHERE User_ID='{user.id}'"
    cursor.execute(request)
    connexion.commit()
    result : int = cursor.fetchone()[0]
    connexion.close()
    return (result)
def get_civ_wins(user : discord.Member) -> int:
    connexion = sqlite3.connect('db_stats.sqlite')
    cursor = connexion.cursor()
    request : str = f"SELECT Wins FROM CivilizationVI WHERE User_ID='{user.id}'"
    cursor.execute(request)
    connexion.commit()
    result : int = cursor.fetchone()[0]
    connexion.close()
    return (result)
def get_civ_lost(user : discord.Member) -> int:
    connexion = sqlite3.connect('db_stats.sqlite')
    cursor = connexion.cursor()
    request : str = f"SELECT Lost FROM CivilizationVI WHERE User_ID='{user.id}'"
    cursor.execute(request)
    connexion.commit()
    result : int = cursor.fetchone()[0]
    connexion.close()
    return (result)
def get_civ_date(user : discord.Member) -> str:
    connexion = sqlite3.connect('db_stats.sqlite')
    cursor = connexion.cursor()
    request : str = f"SELECT Date FROM CivilizationVI WHERE User_ID='{user.id}'"
    cursor.execute(request)
    connexion.commit()
    result : str = str(cursor.fetchone()[0])
    connexion.close()
    return (result)
def get_civ_rank(user : discord.Member) -> int:
    connexion = sqlite3.connect('db_stats.sqlite')
    cursor = connexion.cursor()
    request : str = "SELECT User_ID, Elo, Top1, Wins, Lost FROM CivilizationVI ORDER BY Elo DESC"
    cursor.execute(request)
    connexion.commit()
    result : list = cursor.fetchall()
    connexion.close()
    rank : int = 0
    while (rank < len(result)):
        user_id = result[rank][0]
        if (int(user_id) == int(user.id)):
            return (rank+1)
        rank = rank + 1
    return (-1)
def update_civ_top1(user: discord.Member) -> None:
    connexion = sqlite3.connect("db_stats.sqlite")
    cursor = connexion.cursor()
    request_get : str = f"SELECT Top1 FROM CivilizationVI WHERE User_ID='{user.id}'"
    cursor.execute(request_get)
    top1 : int = cursor.fetchone()[0]
    top1 += 1
    request_write : str = f"UPDATE CivilizationVI SET Top1={top1} WHERE User_ID='{user.id}'"
    cursor.execute(request_write)
    connexion.commit()
    connexion.close()
    return
def update_civ_wins(user: discord.Member) -> None:
    connexion = sqlite3.connect("db_stats.sqlite")
    cursor = connexion.cursor()
    request_get : str = f"SELECT Wins FROM CivilizationVI WHERE User_ID='{user.id}'"
    cursor.execute(request_get)
    wins : int = cursor.fetchone()[0]
    wins = wins + 1
    request_write : str = f"UPDATE CivilizationVI SET Wins={wins} WHERE User_ID='{user.id}'"
    cursor.execute(request_write)
    connexion.commit()
    connexion.close()
    return
def update_civ_lost(user: discord.Member) -> None:
    connexion = sqlite3.connect("db_stats.sqlite")
    cursor = connexion.cursor()
    request_get : str = f"SELECT Lost FROM CivilizationVI WHERE User_ID='{user.id}'"
    cursor.execute(request_get)
    lost : int = cursor.fetchone()[0]
    lost = lost + 1
    request_write : str = f"UPDATE CivilizationVI SET Lost={lost} WHERE User_ID='{user.id}'"
    cursor.execute(request_write)
    connexion.commit()
    connexion.close()
    return
def update_civ_date(user: discord.Member) -> None:
    date = get_parsed_date()
    connexion = sqlite3.connect('db_stats.sqlite')
    cursor = connexion.cursor()
    request: str = f"UPDATE CivilizationVI SET Date='{date}' WHERE User_ID='{user.id}'"
    cursor.execute(request)
    connexion.commit()
    connexion.close()
def update_civ_elo(user: discord.Member, new_elo: int) -> None:
    connexion = sqlite3.connect('db_stats.sqlite')
    cursor = connexion.cursor()
    request_write : str = f"UPDATE CivilizationVI SET Elo={new_elo} WHERE User_ID='{user.id}'"
    cursor.execute(request_write)
    connexion.commit()
    connexion.close()
    return