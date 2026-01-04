# Standard Notes to Joplin Converter (ENEX)

This Python script facilitates the migration of notes from **Standard Notes** to **Joplin** (or any other note-taking app that supports the Evernote `.enex` format).

The main issue with standard exports from Standard Notes is the loss of metadata. This script ensures that **tags, creation dates, and modification dates** are preserved during the transfer.

## ✨ Features
- ✅ Converts decrypted JSON exports into a valid ENEX format.
- ✅ Preserves **Tags** and correctly links them to notes.
- ✅ Maintains timestamps (**Created & Updated** dates).
- ✅ Robust HTML/XML escaping to prevent import errors.
- ✅ Supports loading directly from a `.zip` archive or a raw `.json`/`.txt` file.

## 🚀 How to Use

### 1. Prepare your data (Standard Notes)
1. Open the Standard Notes Desktop app.
2. Go to **Settings** -> **Data Backups**.
3. Download the **Decrypted Backup** (it must be decrypted, otherwise the script cannot read the data).
4. Save the file as `notes.zip` (or extract it to get the `.txt`/`.json` file).

### 2. Run the Script
Ensure you have Python 3 installed.

1. Download the script (e.g., `convert.py`).
2. Place your exported file in the same folder as the script.
3. Run the following command in your terminal:
   ```bash
   python convert.py notes.zip



   # Standard Notes to Joplin Converter (ENEX)

Tento jednoduchý Python skript slouží k migraci poznámek z aplikace **Standard Notes** do **Joplinu** (nebo jiných aplikací podporujících formát Evernote .enex). 

Hlavním problémem běžného exportu ze Standard Notes je ztráta metadat. Tento skript zajišťuje, že se při přenosu **zachovají tagy (štítky), data vytvoření a data úprav**.

## ✨ Funkce
- ✅ Převod dešifrovaného JSON exportu na formát ENEX.
- ✅ Zachování **tagů** a jejich správné přiřazení k poznámkám.
- ✅ Zachování časových značek (**vytvořeno & upraveno**).
- ✅ Automatické ošetření HTML znaků pro bezproblémový import.
- ✅ Podpora pro načítání přímo ze souboru `.zip` nebo `.json`.

## 🚀 Jak to použít

### 1. Příprava dat (Standard Notes)
1. Otevřete Standard Notes (Desktop verzi).
2. Jděte do **Settings** -> **Data Backups**.
3. Stáhněte si **Download Decrypted Backup** (musí být dešifrovaný, jinak skript data nepřečte).
4. Soubor uložte jako `notes.zip` (nebo jej rozbalte a použijte .txt/.json soubor).

### 2. Spuštění skriptu
Ujistěte se, že máte nainstalovaný Python 3.

1. Stáhněte si tento skript (např. `convert.py`).
2. Umístěte váš exportovaný soubor do stejné složky.
3. Spusťte příkaz v terminálu:
   ```bash
   python convert.py notes.zip
