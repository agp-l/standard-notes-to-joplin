import json
import html
import datetime
import re
import sys
import zipfile
import os

# 1. Nastavení vstupního souboru
source = sys.argv[1] if len(sys.argv) > 1 else 'notes.zip'

if not os.path.exists(source):
    print(f"Chyba: Soubor '{source}' nebyl nalezen.")
    sys.exit(1)

print(f"🚀 Zahajuji konverzi souboru: {source}")

# 2. Načtení dat (ze ZIPu nebo přímo z JSONu)
try:
    if source.endswith('.zip'):
        with zipfile.ZipFile(source, 'r') as zip_ref:
            # Standard Notes obvykle pojmenovává soubor takto:
            filename = 'Standard Notes Backup and Import File.txt'
            if filename not in zip_ref.namelist():
                # Pokud se jmenuje jinak, vezmeme první .txt nebo .json soubor
                filename = [n for n in zip_ref.namelist() if n.endswith(('.txt', '.json'))][0]
            
            print(f"Rozbaluji metadata z: {filename}")
            content = zip_ref.read(filename).decode('utf-8')
            data = json.loads(content)
    else:
        with open(source, 'r', encoding='utf-8') as f:
            data = json.load(f)
except Exception as e:
    print(f"Chyba při čtení souboru: {e}")
    sys.exit(1)

def format_text_to_enml(text):
    """Převede čistý text na ENML formát (Evernote XML)"""
    if not text:
        return ""
    # Úprava speciálních znaků pro XML
    safe_text = html.escape(text)
    # Převod konců řádků na HTML breaky
    safe_text = safe_text.replace('\n', '<br/>')
    return safe_text

# 3. Mapování tagů na poznámky
tag_notes_links = {}
tags_count = 0

print("Zpracovávám tagy...")
for item in data.get('items', []):
    if item.get('content_type') == 'Tag':
        tags_count += 1
        tag_title = item['content'].get('title', 'unnamed-tag')
        for reference in item['content'].get('references', []):
            uuid = reference.get('uuid')
            if uuid:
                if uuid not in tag_notes_links:
                    tag_notes_links[uuid] = []
                tag_notes_links[uuid].append(html.escape(tag_title))

print(f"Nalezeno {tags_count} tagů.")

# 4. Generování ENEX souboru
enex_header = '''<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE en-export SYSTEM "http://xml.evernote.com/pub/evernote-export3.dtd">
<en-export application="Evernote" version="Evernote Mac 6.13.3">
'''

notes_body = ""
notes_count = 0

print("Konvertuji poznámky...")
for item in data.get('items', []):
    if item.get('content_type') == 'Note':
        notes_count += 1
        content_data = item.get('content', {})
        
        title = html.escape(content_data.get('title', 'Bez názvu'))
        text = format_text_to_enml(content_data.get('text', ''))
        
        # Tagy pro tuhle konkrétní poznámku
        note_tags = tag_notes_links.get(item['uuid'], [])
        tag_xml = "".join([f"<tag>{t}</tag>" for t in note_tags])
        
        # Časy (odstranění milisekund pro standard ENEX)
        def format_date(date_str):
            try:
                return datetime.datetime.strptime(date_str[0:19], '%Y-%m-%dT%H:%M:%S').strftime('%Y%m%dT%H%M%SZ')
            except:
                return datetime.datetime.now().strftime('%Y%m%dT%H%M%SZ')

        created = format_date(item.get('created_at', ''))
        updated = format_date(item.get('updated_at', ''))

        # Sestavení XML bloku poznámky
        notes_body += f'''<note>
<title>{title}</title>
<content>
<![CDATA[<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<!DOCTYPE en-note SYSTEM "http://xml.evernote.com/pub/enml2.dtd">
<en-note>{text}</en-note>]]>
</content>
<created>{created}</created>
<updated>{updated}</updated>
{tag_xml}
<note-attributes/>
</note>'''

        if notes_count % 10 == 0:
            print(f"   Zpracováno {notes_count} poznámek...")

enex_footer = '</en-export>'

# 5. Uložení výsledku
output_filename = "standard_notes_to_joplin.enex"
try:
    with open(output_filename, "w", encoding='utf-8') as f:
        f.write(enex_header + notes_body + enex_footer)
    print("\n" + "="*30)
    print(f"HOTOVO! Soubor byl vytvořen.")
    print(f"Název: {output_filename}")
    print(f"Celkem poznámek: {notes_count}")
    print(f"Nyní v Joplinu zvolte: File -> Import -> ENEX - Evernote Export File")
    print("="*30)
except Exception as e:
    print(f"Chyba při zápisu souboru: {e}")
