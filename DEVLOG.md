
# 🧾 DEVLOG — UIED-Tesseract-Patch

## 📆 2025-07-20

- Clonage du repo original `UIED`
- Remplacement de `time.clock()` (deprecated)
- Suppression de la dépendance à Google OCR
- Ajout d’une fonction `ocr_detection_tesseract()` dans `ocr.py`
- Conversion des résultats bruts Tesseract en objets `Text`
- Patch `visualize_texts()` pour supporter `dict` + `Text`
- Génération réussie d’un JSON et d’une image annotée à partir de screenshot
- Création du dépôt GitHub : https://github.com/manteria/UIED-Tesseract-Patch