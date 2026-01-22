# excel_to_mongo.py
import pandas as pd
from pymongo import MongoClient
import os
from datetime import datetime

# ────────────────────────────────────────────────
# CONFIGURATION – À MODIFIER SELON TON CAS
# ────────────────────────────────────────────────
EXCEL_FILE = "DB_Audit.xlsx"
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
                dtype=str,
                parse_dates=True,
                engine="openpyxl"
            )

            df = df.replace({pd.NA: None, "nan": None, "NaN": None})
            df.columns = [col.strip().replace(" ", "_").lower() for col in df.columns]

            if sheet_name == "Sheet1":
                # ─── On traite Sheet1 uniquement pour splitter farms + sensors ───
                # PAS d'import direct de Sheet1

                # FARMS
                farms_cols = ['farm_id', 'farm_name', 'country', 'latitude', 'longitude', 'crop_type']
                df_farms = df[farms_cols].copy()
                df_farms['farm_id'] = [f"F{i:04d}" for i in range(1, len(df_farms) + 1)]
                df_farms = df_farms.drop_duplicates(subset=['farm_id'])

                # SENSORS
                sensors_cols = ['farm_id', 'soil_humidity', 'soil_ph', 'air_temperature', 'ndvi']
                df_sensors = df[sensors_cols].copy()
                df_sensors['sensor_id'] = [f"S{i:04d}" for i in range(1, len(df_sensors) + 1)]
                df_sensors['farm_id'] = [f"F{i:04d}" for i in range(1, len(df_sensors) + 1)]
                df_sensors = df_sensors[['sensor_id', 'farm_id', 'soil_humidity', 'soil_ph', 'air_temperature', 'ndvi']]

                # Import farms
                coll_farms = db["farms"]
                if DROP_EXISTING:
                    coll_farms.drop()
                    print(f"  Collection farms supprimée")
                records_f = df_farms.to_dict("records")
                if records_f:
                    coll_farms.insert_many(records_f)
                    print(f"  → {len(records_f)} fermes insérées (F0001 → F{len(records_f):04d})")
                    imported_count += len(records_f)

                # Import sensors
                coll_sensors = db["sensors"]
                if DROP_EXISTING:
                    coll_sensors.drop()
                    print(f"  Collection sensors supprimée")
                records_s = df_sensors.to_dict("records")
                if records_s:
                    coll_sensors.insert_many(records_s)
                    print(f"  → {len(records_s)} capteurs insérés (S0001 → S{len(records_s):04d})")
                    imported_count += len(records_s)

            else:
                # ─── Import normal pour toutes les autres feuilles ───
                records = df.to_dict("records")
                collection_name = f"{COLLECTION_PREFIX}{sheet_name.lower().replace(' ', '_')}"
                collection = db[collection_name]

                if DROP_EXISTING:
                    collection.drop()
                    print(f"  Collection {collection_name} supprimée")

                if records:
                    collection.insert_many(records)
                    print(f"  → {len(records)} documents insérés ({collection_name})")
                    imported_count += len(records)
                else:
                    print(f"  → Aucune ligne dans {sheet_name}")

        except Exception as e:
            print(f"  ERREUR sur feuille {sheet_name} : {e}")

    print(f"\nImport terminé ! {imported_count} documents importés au total.")
    client.close()


if __name__ == "__main__":
    if not os.path.exists(EXCEL_FILE):
        print(f"Erreur : le fichier {EXCEL_FILE} n'existe pas.")
    else:
        import_excel_to_mongo()