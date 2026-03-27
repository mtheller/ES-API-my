# --------- IMPORTS ---------
import os
import csv
from pathlib import Path
import FlowAPI
from dotenv import load_dotenv


# --------- INIT ---------
env_path = Path(__file__).parent / "cred.env"
load_dotenv(env_path)

metadata_api = FlowAPI.Metadata.create_gateway_instance(
    os.environ["FLOW_USER"], os.environ["FLOW_PASSWORD"], os.environ["FLOW_HOST"]
)

csv_path = Path(__file__).parent / "result.csv"
fieldnames = [
    "Clipname", "Project", "Captured", "Modified", "Media Space", "Status",
    "File Type", "Video Codec", "Width", "Height", "Frame Rate",
    "Audio File Type", "Audio Bit Depth", "Audio Sample Rate",
    "Start", "End", "Duration", "Comment",
    "01 LOOKS ID", "003b Mapping Identifier", "006 Source PROGRESS",
    "007 Collection PROGRESS", "19 Sound", "049 Rights Owner",
    "073b Country Of Production English", "080 Production Year",
    "084 Decade", "101a Genre German", "101b Genre English",
    "104 Internal Notes", "116 Accounting Article Range",
    "118 Accounting ID Licence Holder", "122 ClipID", "123 AssetID",
    "126 UUID", "128 Mapped", "128 Mapping Status",
]


# --------- CONFIG ---------
limit = metadata_api.numClips()
#limit = 100
offset = 0

# --------- FUNC ---------
def duration_tc_ms(start_tc: str, end_tc: str) -> str:
    if start_tc is not None and end_tc is not None:
        # NUM/DEN abschneiden
        start_hmsm, _ = start_tc.rsplit(":", 1)
        end_hmsm, _   = end_tc.rsplit(":", 1)

        # HH:MM:SS:MS zerlegen
        sh, sm, ss, sms = start_hmsm.split(":")
        eh, em, es, ems = end_hmsm.split(":")

        # Alles in Millisekunden
        start_ms = ((int(sh) * 3600 + int(sm) * 60 + int(ss)) * 1000) + int(sms)
        end_ms   = ((int(eh) * 3600 + int(em) * 60 + int(es)) * 1000) + int(ems)

        diff = end_ms - start_ms

        hours, rem = divmod(diff, 3600 * 1000)
        mins, rem  = divmod(rem, 60 * 1000)
        secs, ms   = divmod(rem, 1000)

        return f"{hours:02d}:{mins:02d}:{secs:02d}:{ms+1:02d}"
    else:
        return None


def get_medaspace_name(clip_metadata: dict) -> str:
    media_space_name = None
    media_type = "video" if clip_metadata.get("has_video") else "audio"
    media_space_name = clip_metadata.get(media_type, [{}])[0].get("file", {}).get("archive_locations", [{}])[0].get("media_space_name")
    return media_space_name


def get_fps(clip_metadata: str) -> str:
    raw_fps = clip_metadata.get("video", [{}])[0].get("frame_rate", None)
    fps = raw_fps.split("/")[0] if raw_fps else None
    return str(fps)


def remove_newline(row: dict) -> dict:
    cleaned = {}
    for k, v in row.items():
        if isinstance(v, str):
            cleaned[k] = v.replace("\r\n", " ").replace("\n", " ").replace("\r", " ")
        else:
            cleaned[k] = v
    return cleaned


# --------- MAIN ---------
all_clips = metadata_api.clips(offset=offset, limit=limit)
custom_field_definitions = metadata_api.getCustomMetadataFields()
custom_field_key_to_name = {f["db_key"]: f["name"] for f in custom_field_definitions}

file_exists = csv_path.exists()
if not file_exists:
    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()

for clip_counter, clip in enumerate(all_clips, start=1):
    clip_metadata = metadata_api.get_clip(clip)
    asset_custom = clip_metadata.get("asset", {}).get("custom", {})

    custom_values = {
        custom_field_key_to_name.get(db_key, db_key): value
        for db_key, value in asset_custom.items()
    }

    tc_start = clip_metadata.get("metadata", {}).get("timecode_start", None)
    tc_end = clip_metadata.get("metadata", {}).get("timecode_end", None)
    dur = duration_tc_ms(tc_start, tc_end)

    row = {
        "Clipname": clip_metadata.get("metadata", {}).get("clip_name_with_extension", None),
        "Project": clip_metadata.get("capture", {}).get("project", None),
        "Captured": clip_metadata.get("metadata", {}).get("captured"),
        "Modified": clip_metadata.get("metadata", {}).get("modified"),
        "Media Space": get_medaspace_name(clip_metadata),
        "Status": clip_metadata.get("status_text", None),
        "File Type": clip_metadata.get("display_filetype"),
        "Video Codec": clip_metadata.get("display_video_codec", None),
        "Width": clip_metadata.get("video", [{}])[0].get("width", None),
        "Height": clip_metadata.get("video", [{}])[0].get("height", None),
        "Frame Rate": get_fps(clip_metadata),
        "Audio File Type": clip_metadata.get("audio", [{}])[0].get("compression", None),
        "Audio Bit Depth": clip_metadata.get("audio", [{}])[0].get("bit_depth", None),
        "Audio Sample Rate": clip_metadata.get("audio", [{}])[0].get("sample_rate", None),
        "Start": tc_start,
        "End": tc_end,
        "Duration": dur,
        "Comment": clip_metadata.get("asset", {}).get("comment", None),
# falsche ID - es muss 001 ID sein! "01 LOOKS ID": custom_values.get("01 LOOKS ID", None),
        "003b Mapping Identifier": custom_values.get("003b Mapping Identifier", None),
        "006 Source PROGRESS": custom_values.get("006 Source PROGRESS", None),
        "007 Collection PROGRESS": custom_values.get("007 Collection PROGRESS", None),
        "19 Sound": custom_values.get("19 Sound", None),
        "049 Rights Owner": custom_values.get("049 Rights Owner", None),
        "073b Country Of Production English": custom_values.get("073b Country Of Production English", None),
        "080 Production Year": custom_values.get("080 Production Year", None),
        "084 Decade": custom_values.get("084 Decade", None),
        "101a Genre German": custom_values.get("101a Genre German", None),
        "101b Genre English": custom_values.get("101b Genre English", None),
        "104 Internal Notes": custom_values.get("104 Internal Notes", None),
        "116 Accounting Article Range": custom_values.get("116 Accounting Article Range", None),
        "118 Accounting ID Licence Holder": custom_values.get("118 Accounting ID Licence Holder", None),
        "122 ClipID": custom_values.get("122 ClipID", None),
        "123 AssetID": custom_values.get("123 AssetID", None),
        "126 UUID": custom_values.get("126 UUID", None),
        "128 Mapped": custom_values.get("128 Mapped", None),
        "128 Mapping Status": custom_values.get("128 Mapping Status", None),
    }

    with open(csv_path, "a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writerow(remove_newline(row))

    print(f"✓ Clip {clip_counter} von {len(all_clips)} angehängt")













 # ------  OLD CODE SNIPPETS -------
"""

txt_path = Path(__file__).parent / "full_metadata.txt"
with open(txt_path, 'w', encoding='utf-8') as f:
    f.write(json.dumps(full_metadata, indent=2, ensure_ascii=False))
print(f"✓ OK!")


txt_path = Path(__file__).parent / "clip_metadata.txt"
with open(txt_path, 'w', encoding='utf-8') as f:
    f.write(json.dumps(clip_metadata, indent=2, ensure_ascii=False))
print(f"✓ Metadaten gespeichert: {txt_path}")

    clip_id = clip_metadata.get("clip_id", None)
    asset_id = clip_metadata.get("asset", None).get("asset_id", None)
    if clip_metadata.get("has_video"):
        video = clip_metadata.get("video", None)
        file_id = video[0].get("file_id")
    elif clip_metadata.get("has_audio"):
        audio = clip_metadata.get("audio", None)
        file_id = audio[0].get("file_id")
    else:
        file_id = None



url_base = f"https://{os.environ['FLOW_HOST']}:8006/api/v2/metadata/export/assets/"
to_save = clip_metadata
    
Speichere Metadaten als TXT-Datei



    url = url_base + f"{asset_id}" + "?export_format=csv&asset_metadata=true&export_asset_custom_metadata=true&file_details=true&location_details=false&backup_details=false&markers=false&csv_framerates=false&csv_comments=false&csv_bom=false"

    # HTTP Request zur API machen und CSV-Daten abrufen
    try:
        response = requests.get(
            url, 
            auth=(os.environ["FLOW_USER"], os.environ["FLOW_PASSWORD"]),
            verify=False
        )
        response.raise_for_status()
        
        # CSV-Daten aus der Response parsen
        csv_reader = csv.DictReader(StringIO(response.text))
        csv_data = list(csv_reader)
        
        # Daten zum full_metadata Array hinzufügen
        for row in csv_data:
            full_metadata.append(row)
    except Exception as e:
        print(f"ERROR: Fehler beim Abrufen der CSV-Daten für Asset {asset_id}: {e}")
        continue

    # CSV nach jedem Durchlauf speichern
    if full_metadata:
        csv_path = Path(__file__).parent / "result.csv"
        fieldnames = list(full_metadata[0].keys())
        with open(csv_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(full_metadata)
    
    print(f"OK: Clip {clip_counter} von {len(all_clips)} verarbeitet.")

 """
