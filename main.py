#	     ____     ______  ____     ____    __  __          __       ______          ____     ______  ____     ______  ________
#	    / __ |   / __  / / __ |   / __ |  / / / /         / /      / ____/         / __ |   / __  / / __ |   / __  / /__  ___/
#	   / /_/ /  / / / / / /_/ /  / /_/ / / /_/ /         / /      / /_            / /_/ /  / / / / / /_/ /  / / / /    / /
#	  / ___ |  / / / / / ___ |  / ___ |  |__  /         / /      / __/           / __  /  / / / / / ___ |  / / / /    / /
#	 / /__/ / / /_/ / / /__/ / / /__/ /    / /         / /____  / /___          / /  | | / /_/ / / /__/ / / /_/ /    / /
#	/______/ /_____/ /______/ /______/    /_/         /______/ /_____/         /_/  /_/ /_____/ /______/ /_____/    /_/

# IDÉES
# REPORT DES PARTIES (différent jeux pris en charge)
# HISTORIQUE DES PARTIES JOUEES (différent jeux pris en charge)
# STATISTIQUES (différents jeux pris en charge et stats liées au serveur)

#==================== INITIALISATION ====================
import discord
import discord.ui
from classes import Bot, BotEmbed, FeedbackForm
from config import TOKEN, SERVERS
from draft import *
from mapvote import *
from wordle import *
from utils import *
from civilization import *

bot = Bot()

#====================== CONSTANTES ======================

#======================== EVENTS ========================
@bot.event
async def on_ready():
    print("         ____     ______  ____     ____    __  __          __       ______          ____     ______  ____     ______  ________")
    print("        / __ |   / __  / / __ |   / __ |  / / / /         / /      / ____/         / __ |   / __  / / __ |   / __  / /__  ___/")
    print("       / /_/ /  / / / / / /_/ /  / /_/ / / /_/ /         / /      / /_            / /_/ /  / / / / / /_/ /  / / / /    / /")
    print("      / ___ |  / / / / / ___ |  / ___ |  |__  /         / /      / __/           / __  /  / / / / / ___ |  / / / /    / /")
    print("     / /__/ / / /_/ / / /__/ / / /__/ /    / /         / /____  / /___          / /  | | / /_/ / / /__/ / / /_/ /    / /")
    print("    /______/ /_____/ /______/ /______/    /_/         /______/ /_____/         /_/  /_/ /_____/ /______/ /_____/    /_/")
    return print(f"\n... est connecté.\nRock n'Roll !\n")



#=================== SLASH COMMANDES ====================
#Renvoit PONG si le bot est connecté
@bot.slash_command(guild_ids=SERVERS, name="ping", description="PONG !")
async def ping(interaction: discord.Interaction):
    print(f"COMMAND : /ping used by @{interaction.user.name} in {interaction.guild.name} (#{interaction.channel.name})")
    embed = BotEmbed(title="PONG", colour=discord.Colour.green())
    embed.remove_footer()
    await interaction.response.send_message(embed=embed, ephemeral=True)

#Renvoit une présentation du bot
@bot.slash_command(guild_ids=SERVERS, name="hello", description="Dis bonjour !")
async def hello(interaction: discord.Interaction):
    print(f"COMMAND : /hello used by @{interaction.user.name} in {interaction.guild.name} (#{interaction.channel.name})")
    embed = BotEmbed(title="SALUTATIONS", description=f"Bonjour maître {interaction.user.mention} !\nC'est un plaisir de faire votre connaissance !\n\nN'hésitez pas à faire appel à moi pour préparer vos parties de Civilization VI, jouer à Wordle ou garder une trace de vos résultats et de vos statistiques dans différent jeux.\n\nMon code est accessible [ici](https://github.com/Matezzi777/Bobby_le_gentil_robot).\n\nSi vous avez une idée pour m'améliorer, utilisez la commande ***/feedback*** pour faire une suggestion !")
    await interaction.response.send_message(embed=embed, ephemeral=True)

#Distribue des leaders de civilization vi aux joueurs présents dans le salon vocal
@bot.slash_command(guild_ids=SERVERS, name="draft", description="Distribue des drafts pour Civilization VI.")
async def draft(interaction: discord.Interaction, nb_leaders = discord.Option(int, "Le nombre de leaders à distribuer à chaque joueur.", required=False, default=10)):
    print(f"COMMAND : /draft used by @{interaction.user.name} in {interaction.guild.name} (#{interaction.channel.name})")
    author = interaction.user
    if (not author.voice):
        print(f"    - ERREUR : Le joueur doit se trouver dans un salon vocal.")
        missing_voice_embed = BotEmbed(title=f"PLEASE JOIN A VOICE CHANNEL", description=f"Veuillez rejoindre un salon vocal avec les autres joueurs avant de réutiliser cette commande pour recevoir les drafts.")
        return await interaction.response.send_message(embed=missing_voice_embed, ephemeral=True)
    else:
        channel = author.voice.channel
        players = channel.members

    nb_players = len(players)
    if (nb_players < 2): #S'il n'y a pas assez de joueurs
        print(f"    - ERREUR : Nombre de joueurs insuffisant.")
        embed = BotEmbed(title=f"ERREUR", description=f"Au minimum 2 joueurs sont nécessaires pour générer une draft. Demandez aux autres joueurs de rejoindre votre salon vocal.", colour=discord.Colour.red())
        return await interaction.response.send_message(embed=embed, ephemeral=True)
    elif (nb_players > 25): #S'il y a trop de joueurs
        print(f"    - ERREUR : Nombre de joueurs trop élevé.")
        embed = BotEmbed(title=f"ERREUR", description=f"Les drafts ne supportent que 25 joueurs au maximum.", colour=discord.Colour.red())
        return await interaction.response.send_message(embed=embed, ephemeral=True)
    elif (nb_leaders > 15): #Si le nombre de leaders demandé est trop grand
        print(f"    - ERREUR : Nombre de leaders trop élevé.")
        embed = BotEmbed(title=f"ERREUR", description=f"Trop de leaders par joueur demandés (max. 15).", colour=discord.Colour.red())
        return await interaction.response.send_message(embed=embed, ephemeral=True)
    elif (nb_players * nb_leaders > 77): #S'il n'y a pas assez de leaders dans le jeu pour en fournir assez à chaque joueur
        print(f"    - ERREUR : Pas assez de leaders pour fournir tous les joueurs.")
        embed = BotEmbed(title=f"ERREUR", description=f"Le jeu ne comporte pas assez de leaders différents pour en fournir {nb_leaders} à {nb_players} joueurs.", colour=discord.Colour.red())
        return await interaction.response.send_message(embed=embed, ephemeral=True)
    else: #Si tous les paramètres sont valides
        message = ""
        i : int = 0
        while (i < len(players)):
            message = message + f"{players[i].mention} "
            i = i + 1
        draft = create_draft(nb_players, nb_leaders)
        embed_draft = BotEmbed(title="DRAFT", description=f"New draft for {nb_players} players with {nb_leaders} leaders by player.")
        i : int = 0
        while (i < nb_players):
            k : int = 0
            field_value : str = f"**{players[i].mention} :**\n"
            while (k < nb_leaders):
                field_value = field_value + f"{emote_from_id(draft[i*nb_leaders+k])} {leader_from_id(draft[i*nb_leaders+k])}\n"
                k = k + 1
            field_value = field_value[:-1]
            embed_draft.add_field(name=f"", value=field_value)
            i = i + 1
        print(f"    - SUCCES : Drafts distribuées.")
        await interaction.response.send_message(message)
        return await interaction.followup.send(embed=embed_draft)

@bot.slash_command(guild_ids=SERVERS, name="mapvote", description="Crée un mapvote pour Civilization VI.")
async def mapvote(interaction: discord.Interaction):
    print(f"COMMAND : /mapvote used by @{interaction.user.name} in {interaction.guild.name} (#{interaction.channel.name})")
    return await make_mapvote(interaction)

#Renvoit un formulaire pour émettre des suggestions d'amélioration du bot
@bot.slash_command(guild_ids=SERVERS, name="feedback", description="Formulaire pour envoyer une suggestion d'amélioration.")
async def feedback(interaction: discord.Interaction):
    print(f"COMMAND : /feedback used by @{interaction.user.name} in {interaction.guild.name} (#{interaction.channel.name})")
    return await interaction.response.send_modal(FeedbackForm())

#Lance une partie de Wordle
@bot.slash_command(guild_ids=SERVERS, name="wordle", description="Lance une partie de Wordle.")
async def wordle(interaction: discord.Interaction, nb_lettres: int = discord.Option(int, "Le nombre de lettres du mot à deviner.", required=False, default=5), nb_essais: int = discord.Option(int, "Le nombre d'essais maximum pour deviner'.", required=False, default=6)):
    author : discord.Member = interaction.user
    print(f"COMMAND : /wordle used by @{author.name} in {interaction.guild.name} (#{interaction.channel.name})")
    #Affiche un embed pour le chargement
    embed_waiting = BotEmbed(title="WORDLE", description="<a:icons8sablierfond:1261108677679780033> Je cherche un mot <a:icons8sablierfond:1261108677679780033>")
    message = await interaction.response.send_message(embed=embed_waiting)
    #Trouve un mot du bon nombre de lettres
    mot: str = get_word(nb_lettres)
    print(f"    Mot à trouver : {mot}")
    #Prépare le jeu
    embed = BotEmbed(title="WORDLE", description=f"Essayez de trouver ce mot de {nb_lettres} lettres en moins de {nb_essais} essais.\nAttention à ne pas mettre d'accents !")
    embed_content : list[str] = initialize_embed_content(nb_lettres, nb_essais)
    embed.add_field(name="", value=get_str_from_list(embed_content), inline=False)
    embed.add_field(name="", value=f"**Encore {nb_essais} essais.\nEntrez *end_game* pour arrêter la partie.**", inline=False)
    #Affiche par le jeu
    await message.edit(embed=embed)
    i: int = 0
    while (i < nb_essais):
        #Attends pour une réponse
        guess: discord.Message = await bot.wait_for('message', check=lambda message: message.channel == interaction.channel)
        proposition: str = f"{guess.content.upper().strip()}"
        if (proposition == "END_GAME"):
            print("    ABANDON")
            await guess.delete()
            embed_response = BotEmbed(title="PARTIE ABANDONNÉE", description=f"Partie abandonnée.\nLe mot était : {mot}.")
            update_wordle_stats(author, "GiveUp")
            return await interaction.followup.send(embed=embed_response)
        #Vérifie la réponse
        new_line: str = check_guess_validity(proposition, mot)
        if (new_line == "MISSING"):
            embed_response = BotEmbed(title="MOT INTROUVABLE", colour=discord.Colour.red(), description=f"Le mot {proposition} n'est pas dans le dictionnaire. Vérifiez l'orthographe du mot.")
            await guess.delete()
            await interaction.followup.send(embed=embed_response,ephemeral=True)
        elif (new_line == "INVALIDE"):
            embed_response = BotEmbed(title="LONGUEUR INCORRECTE", colour=discord.Colour.red(), description=f"Vous recherchez une mot de {nb_lettres} lettres.\n'{proposition}' fait {len(proposition)} lettres.")
            await guess.delete()
            await interaction.followup.send(embed=embed_response, ephemeral=True)
        elif (new_line == "FOUND"):
            print("    VICTOIRE")
            new_embed = BotEmbed(title="WORDLE")
            line: str = ""
            z: int = 0
            while (z < len(proposition)):
                line = f"{line}🟩 "
                z = z + 1
            embed_content[i] = f"{line} --- {mot}"
            new_embed.add_field(name="Historique :", value=get_str_from_list(embed_content), inline=False)
            embed_response = BotEmbed(title="MOT TROUVÉ", colour=discord.Colour.green(), description=f"Félicitations ! Vous avez trouvé le mot {mot} en {i+1} essais !")
            await guess.delete()
            await message.edit(embed=new_embed)
            update_wordle_stats(author, "Victory")
            return await interaction.followup.send(embed=embed_response)
        else:
            new_embed = BotEmbed(title="WORDLE", description=f"Essayez de trouver ce mot de {nb_lettres} lettres en moins de {nb_essais} essais.\nAttention à ne pas mettre d'accents !")
            embed_content[i] = new_line
            new_embed.add_field(name="", value=get_str_from_list(embed_content), inline=False)
            new_embed.add_field(name="", value=f"**{nb_essais-i-1} essais restants.\nEntrez *end_game* pour arrêter la partie.**", inline=False)
            await guess.delete()
            await message.edit(embed=new_embed)
            i = i + 1
    print("    DÉFAITE")
    embed_response = BotEmbed(title="WORDLE", colour=discord.Colour.red(), description=f"GAME OVER ! Le mot à trouver était {mot}.")
    update_wordle_stats(author, "Lose")
    return await interaction.followup.send(embed=embed_response)

#Lance une pièce
@bot.slash_command(guild_ids=SERVERS, name="head_or_tail", description="Lance une pièce.")
async def head_or_tail(interaction: discord.Interaction):
    print(f"COMMAND : /head_or_tail used by @{interaction.user.name} in {interaction.guild.name} (#{interaction.channel.name})")
    return await interaction.response.send_message(embed=BotEmbed(title=random_pick_str(["HEAD (FACE)", "TAIL (PILE)"])))

#Commande de test
@bot.slash_command(guild_ids=SERVERS, name="report", description="Report a Civilization VI game result.")
async def report(interaction: discord.Interaction,
               p1: discord.Member = discord.Option(discord.Member, description="Joueur 1", required=True),
               p2: discord.Member = discord.Option(discord.Member, description="Joueur 2", required=True),
               p3: discord.Member = discord.Option(discord.Member, description="Joueur 3", required=False, default=None),
               p4: discord.Member = discord.Option(discord.Member, description="Joueur 4", required=False, default=None),
               p5: discord.Member = discord.Option(discord.Member, description="Joueur 5", required=False, default=None),
               p6: discord.Member = discord.Option(discord.Member, description="Joueur 6", required=False, default=None),
               p7: discord.Member = discord.Option(discord.Member, description="Joueur 7", required=False, default=None),
               p8: discord.Member = discord.Option(discord.Member, description="Joueur 8", required=False, default=None)):
    field_value: str = ""
    args: list[discord.Member] = [p1, p2, p3, p4, p5, p6, p7, p8]
    players: list[discord.Member] = []
    for user in args:
        if ((user != None) and (not user in players)):
            players.append(user)
            field_value = f"{field_value}- {user.mention}\n"
    embed = BotEmbed(title="REPORT", description=f"Please follow the process to complete the report of this game for *{len(players)} players*.")
    await interaction.response.send_message(embed=embed, view=ReportView(embed, players))

#IDEES
# Pierre feuille ciseau

#==================== USER COMMANDES ====================
#Affiche les statistiques de cet utilisateur
@bot.user_command(guild_ids=SERVERS, name="Stats")
async def stats(interaction: discord.Interaction, member: discord.Member):
    print(f"USER COMMAND : Stats used by @{interaction.user.name} in {interaction.guild.name} (#{interaction.channel.name})")
    if (not is_user_in_db(member, "Wordle")):
        add_user_in_wordle_db(member)
    embed = BotEmbed(title="STATS", description=f"{member.mention}'s stats:")
    embed.add_field(name="Wordle", value=display_wordle_user_stats(member))
    return await interaction.response.send_message(embed=embed)

#================== MESSAGES COMMANDES ==================
#Répète un message
@bot.message_command(guild_ids=SERVERS, name="repeat")
async def repeat(interaction : discord.Interaction, message : discord.Message):
    print(f"MESSAGE COMMAND : Repeat used by @{interaction.user.name} in {interaction.guild.name} (#{interaction.channel.name})")
    embed = BotEmbed(title="REPEAT", description=f"{message.created_at}")
    embed.add_field(name=f"", value=f"**{message.author.mention} said :**\n{message.content}")
    return await interaction.response.send_message(embed=embed)

#Traduis un message

#========================= RUN ==========================
bot.run(TOKEN)