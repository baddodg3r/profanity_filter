import json
import sys

txt_file_path = 'other_files/profanity.txt'
json_file_path = 'other_files/profanity.json'

def try_read_lines(file_path, encodings):
    for encoding in encodings:
        try:
            with open(file_path, 'r', encoding=encoding) as file:
                print(f"Datei {file_path} wird mit der Kodierung {encoding} gelesen.")
                for line in file:
                    yield line.strip().lower(), encoding
            break
        except UnicodeDecodeError:
            print(f"UnicodeDecodeError mit Kodierung {encoding}. Versuche die nächste Kodierung.")
            continue
    else:
        raise UnicodeDecodeError(f"Konnte die Datei {file_path} nicht mit den Kodierungen {encodings} lesen.")

data = {'profanity_words': []}

try:
    with open(json_file_path, 'r', encoding='utf-8') as json_file:
        data = json.load(json_file)
        if 'profanity_words' not in data:
            data['profanity_words'] = []
except FileNotFoundError:
    print(f"Die Datei {json_file_path} wurde nicht gefunden. Eine neue Datei wird erstellt.")
except PermissionError:
    print(f"Zugriffsrechte-Fehler: Das Skript hat keine Berechtigung, {json_file_path} zu lesen.")
    sys.exit(1)

try:
    for line, encoding_used in try_read_lines(txt_file_path, ['utf-8', 'latin1', 'windows-1252']):
        if line and line not in data['profanity_words']:
            data['profanity_words'].append(line)
except (FileNotFoundError, PermissionError, UnicodeDecodeError) as e:
    print(e)
    sys.exit(1)

try:
    with open(json_file_path, 'w', encoding='utf-8') as json_file:
        json.dump(data, json_file, ensure_ascii=False, indent=4)
except PermissionError:
    print(f"Zugriffsrechte-Fehler: Das Skript hat keine Berechtigung, {json_file_path} zu schreiben.")
    sys.exit(1)

print('Die Liste der Schimpfwörter wurde erfolgreich aktualisiert.')