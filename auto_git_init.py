import os
import subprocess

# === CONFIGURATION ===
repo_name = "UIED-Tesseract-Patch"
description = "Version patchée de UIED avec OCR Tesseract intégré (full local, no Google)."
private = False  # Mettre True si tu veux un dépôt privé

# === STRUCTURE ===
files = {
    "README.md": f"# {repo_name}\n\n{description}\n\n",
    "CHANGELOG.md": "## Changelog\n\n- Init repo\n- Intégration OCR Tesseract\n",
}
folders = ["doc"]

# === STEP 1: Créer fichiers & dossier doc ===
for file, content in files.items():
    with open(file, "w", encoding="utf-8") as f:
        f.write(content)
for folder in folders:
    os.makedirs(folder, exist_ok=True)

# === STEP 2: Git init + add + commit ===
subprocess.run(["git", "init"], check=True)
subprocess.run(["git", "add", "."], check=True)
subprocess.run(["git", "commit", "-m", "Initial commit"], check=True)

# === STEP 3: Créer dépôt GitHub via GH CLI ===
create_cmd = ["gh", "repo", "create", repo_name, "--source=.", "--push"]
if private:
    create_cmd.append("--private")
else:
    create_cmd.append("--public")

subprocess.run(create_cmd, check=True)

print("\n✅ Dépôt créé et poussé avec succès sur GitHub !")