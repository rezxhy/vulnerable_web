# vulnerable_web

Etape 1 : Aller dans le répertoire !
- "cd vulnerable_web"

Etape 2 : Configurer son environnement venv
- "python -m venv venv"
- "source venv/bin/activate"
- "pip install pandas openpyxl pymongo"
- "pip install requests pymongo colorama tqdm beautifulsoup4 aiohttp python-dotenv"

Etape 3 : Lancer 
- "cd /backend" + "python3 import_db.py"
- "cd .." + "docker-compose build --no-cache"
- "docker-compose up -d"
- utilisation de ngrok - création d'un compte ngrok - récupérer le authtoken.
- ngrok config add-authtoken "token"

Etape 4 : Récuperer le lien ngrok et rentrer sur le site  
- "ngrok http 80" = pour lancer la platforme web.

Etape 5 : Maintenance 
- docker-compose restart backend
- docker-compose restart frontend
# ou
- docker-compose down
- docker-compose build --no-cache
- docker-compose up -d
