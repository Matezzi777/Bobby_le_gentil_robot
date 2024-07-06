# Bobby le robot gentil est là !

Bobby le robot gentil est à votre service !
Il dispose des commandes suivantes :
- /ping
- /hello
- /feedback
- /civ_draft

## How to get Bobby on your server ?
### 1. Clone the project
```git clone https://github.com/Matezzi777/Bobby_le_gentil_robot```
### 2. Create a virtual environment
```sh
python -m venv env
source env/bin/activate
```
### 3. Add the needed libraries
```sh
pip install py-cord
```
### 4. Create config.py file
```sh
touch config.py
```
Edit the file as follow :
```py
TOKEN : str = "your_bot_token"
ID_ADMIN : int = "your_discord_id (integer)" 
SERVERS = [id_server_1 : int, id_server_2 : int, ...]
VERSION = "X.X"
```
### 5. Run the bot
```sh
python main.py
```