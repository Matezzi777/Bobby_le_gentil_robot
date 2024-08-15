# Bobby le robot gentil est là !

Bobby le robot gentil est à votre service !
Il dispose des commandes suivantes :
- Slash commandes :
    - /ping
    - /hello
    - /feedback
    - /draft
    - /wordle
- Commandes de message :
    - Repeat
- Commandes d'utilisateur :
    - Stats

## How to get Bobby on your server ?
### 1. Clone the project
```git clone https://github.com/Matezzi777/Bobby_le_gentil_robot```
### 2. Create a virtual environment
```sh
python3 -m venv venv
source venv/bin/activate
```
### 3. Add the needed libraries
```sh
pip install py-cord
pip install sqlite3
```
### 4. Create config.py file
```sh
touch config.py
```
Edit the file as follow :
```py
TOKEN : str = "your_bot_token"
ID_ADMIN : int = "your_discord_id" 
SERVERS : list[int] = ["id_server_1", "id_server_2", ...]
VERSION : str = "X.X"
```
### 5. Run the bot
```sh
python main.py
```