# excel_to_mongo.py
import pandas as pd
from pymongo import MongoClient
import os
from datetime import datetime

# ────────────────────────────────────────────────
# CONFIGURATION – À MODIFIER SELON TON CAS
# ────────────────────────────────────────────────

EXCEL_FILE = "DB_Audit.xlsx"                  # chemin vers ton fichier

MONGO_URI = "mongodb+srv://admin:caca@cluster0.7xkbg3y.mongodb.net/?appName=Cluster0"

DATABASE_NAME = "audit_db"                  

SHEETS_TO_IMPORT = None
COLLECTION_PREFIX = ""
DROP_EXISTING = True

# ────────────────────────────────────────────────

def import_excel_to_mongo():
    print(f"[{datetime.now():%Y-%m-%d %H:%M:%S}] Début de l'import...")
    print(f"Fichier : {EXCEL_FILE}")
    print(f"Base MongoDB : {DATABASE_NAME}")
    print(f"URI : {MONGO_URI.split('@')[0]}@...")  # masque le mot de passe

    try:
        client = MongoClient(MONGO_URI)
        client.admin.command('ping')
        print("→ Connexion MongoDB OK")
    except Exception as e:
        print("ERREUR connexion MongoDB :", e)
        return

    db = client[DATABASE_NAME]

    # Lecture du fichier Excel
    try:
        xl = pd.ExcelFile(EXCEL_FILE)
        sheets = xl.sheet_names
        print(f"Feuilles trouvées : {sheets}")
    except Exception as e:
        print("ERREUR lecture Excel :", e)
        return

    if SHEETS_TO_IMPORT:
        sheets = [s for s in sheets if s in SHEETS_TO_IMPORT]

    imported_count = 0

    for sheet_name in sheets:
        print(f"\n→ Traitement feuille : {sheet_name}")

        try:
            df = pd.read_excel(
                EXCEL_FILE,
                sheet_name=sheet_name,
                dtype=str,               # tout en string au départ → évite beaucoup de problèmes
                parse_dates=True,        # tente de détecter les dates
                engine="openpyxl"        # ou "xlrd" si ancien .xls
            )

            # Nettoyage léger
            df = df.replace({pd.NA: None, "nan": None, "NaN": None})
            df.columns = [col.strip().replace(" ", "_").lower() for col in df.columns]

            # Conversion en liste de dictionnaires (format MongoDB)
            records = df.to_dict("records")

            collection_name = f"{COLLECTION_PREFIX}{sheet_name.lower().replace(' ', '_')}"
            collection = db[collection_name]

            if DROP_EXISTING:
                collection.drop()
                print(f"  Collection {collection_name} supprimée (DROP_EXISTING=True)")

            if records:
                result = collection.insert_many(records)
                print(f"  → {len(records)} documents insérés (collection: {collection_name})")
                imported_count += len(records)
            else:
                print("  → Aucune ligne à importer")

        except Exception as e:
            print(f"  ERREUR sur feuille {sheet_name} :", e)

    print(f"\nImport terminé ! {imported_count} documents importés au total.")
    client.close()


if __name__ == "__main__":
    if not os.path.exists(EXCEL_FILE):
        print(f"Erreur : le fichier {EXCEL_FILE} n'existe pas dans le dossier courant.")
    else:
        import_excel_to_mongo()