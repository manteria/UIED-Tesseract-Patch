# 📊 Composants du projet

| Module/Fichier             | Description |
|----------------------------|-------------|
| `run_single.py`            | Lanceur principal sur une image unique |
| `ocr.py`                   | Gère Google OCR, Paddle OCR, et Tesseract OCR (patché) |
| `text_detection.py`        | Appelle l’OCR + visualise + export JSON |
| `Text.py`                  | Objet de représentation d’un élément OCR |
| `pytesseract`              | Wrapper Python de Tesseract OCR |
| `cv2`                      | OpenCV pour le traitement d’image |
| `data/input/`              | Contient les screenshots à analyser |
| `data/output/`             | Contient les résultats JSON et images |