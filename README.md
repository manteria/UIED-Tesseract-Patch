# UIED-Tesseract-Patch

Version modifiée de [UIED](https://github.com/MulongXie/UIED) avec support OCR local via **Tesseract**, sans dépendance à Google OCR.

## 📦 Objectif

Transformer UIED en outil 100% offline :
- 🔍 Scanner des interfaces utilisateur (UI) via screenshots
- ✍️ Extraire les textes présents (OCR)
- 🧠 Analyser les éléments graphiques (boutons, zones, etc.)
- 💾 Exporter au format JSON + image annotée

## ⚙️ Fonctionnalités

- Support de `tesseract` OCR intégré (`pytesseract`)
- Génération de JSON pour chaque capture
- Génération d’image annotée
- Compatible Windows (Python 3.11+)

## 🛠 Installation rapide

```bash
pip install -r requirements.txt
python run_single.py