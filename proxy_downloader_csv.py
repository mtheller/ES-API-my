# --------- IMPORTS ---------
import os
import csv
import re
from pathlib import Path
import FlowAPI
from dotenv import load_dotenv

# --------- INIT ---------
env_path = Path(__file__).parent / "cred.env"
load_dotenv(env_path)

metadata_api = FlowAPI.Metadata.create_gateway_instance(
    os.environ["FLOW_USER"], os.environ["FLOW_PASSWORD"], os.environ["FLOW_HOST"]
)

# --------- CONFIG ---------
csv_path = Path(__file__).parent / "Results" / "result_all_metadata_all_clips.csv"
download_path = 
clip_list_path = Path(__file__).parent / "Results" / "clip_list.csv"













# meta = MetadataConnection.createinstance("10.0.77.14", "username", "password")

# Schritt 1: Clip-Metadaten holen - proxy_path ist direkt enthalten
all_clips   = metadata_api.clips(offset=offset, limit=limit)

for clip_counter, clip in enumerate(all_clips, start=1):
    
    clip_metadata = metadata_api.get_clip(clip)

    print(clip_metadata )
    
    if clip_metadata:
        proxy_path = str(clip_metadata.get("proxy_path", {}))
     #print(proxy_path)
     # Ergibt z.B.: "proxy/proxy-b0/8d784326-837d-4b3a-8cc9-ee7e9628d4b0.mp4"

 # Schritt 2: Vollständigen UNC-Pfad zusammenbauen
        # unc_base = r"\\10.0.77.14\RAIDS\RAID_1\flow\files"
        # full_proxy_path = os.path.join(unc_base, proxy_path.replace("/", "\\"))

        #  # Schritt 3: Datei lokal in Zielordner kopieren
        # local_destination = r"C:\Users\Thao-Nhi Hoang\Documents\Code\ES-API-Call-proxy_path\result_test"  # <- deinen Zielpfad hier einsetzen
        # os.makedirs(local_destination, exist_ok=True)
        # shutil.copy(full_proxy_path, local_destination)

        # print(f"Proxy kopiert: {full_proxy_path}")
        # print(f"Ziel: {local_destination}")