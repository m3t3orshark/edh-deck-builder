"""Construit la copie publique du skill (dépôt GitHub et fichier joint aux releases).

Usage : python build_public.py --out <dossier de sortie> [--prenom <prénom de l'auteur>]

Produit dans le dossier de sortie :
  - edh-deck-builder.skill          le skill à publier : profil vierge, sans fichiers privés,
                                    journal anonymisé ;
  - edh-deck-builder.skill.sha256   son empreinte, vérifiée par check_update.py ;
  - edh-deck-builder/               le même contenu, à déposer dans le dépôt.
Fichiers privés retirés : PRIVES (A_FAIRE.md). Le prénom de l'auteur est remplacé par « l'auteur »
dans tous les fichiers texte ; le script refuse de produire quoi que ce soit s'il en reste une trace.
"""
import argparse
import hashlib
import json
import os
import re
import shutil
import sys
import tempfile

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(HERE, "scripts"))
import save_profile  # noqa: E402

PRIVES = ["A_FAIRE.md"]
MOTS_PERSO = "|".join(["compa" + "gne", "ma " + "femme"])  # écrits en morceaux pour ne pas se détecter eux-mêmes


def anonymise(texte, prenom):
    p = re.escape(prenom)
    texte = re.sub(rf"« Commun » et « {p} »", "« Commun » et un classeur personnel", texte)
    texte = re.sub(rf"\b[Dd]e {p}\b", lambda m: m.group(0)[0] + "e l'auteur", texte)
    texte = re.sub(rf"\b{p}\b", "l'auteur", texte)
    return texte


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True)
    ap.add_argument("--prenom", default=None, help="par défaut, le propriétaire du profil installé")
    a = ap.parse_args()
    sys.stdout.reconfigure(encoding="utf-8")
    prenom = a.prenom or save_profile.read_profile(os.path.join(HERE, "PROFIL.md")).get("proprietaire")

    tmp = tempfile.mkdtemp()
    dst = os.path.join(tmp, "edh-deck-builder")
    shutil.copytree(HERE, dst, ignore=shutil.ignore_patterns("__pycache__", "*.pyc", ".DS_Store", "evals"))
    for f in PRIVES:
        if os.path.exists(os.path.join(dst, f)):
            os.remove(os.path.join(dst, f))

    profil = os.path.join(dst, "PROFIL.md")
    texte = open(profil, encoding="utf-8").read()
    vierge = json.dumps(save_profile.VIERGE, ensure_ascii=False, indent=2)
    texte = re.sub(r"```json\s*\n.*?\n```", lambda m: "```json\n" + vierge + "\n```", texte, count=1, flags=re.S)
    open(profil, "w", encoding="utf-8").write(texte)

    restes = []
    for racine, _, fichiers in os.walk(dst):
        for f in fichiers:
            if not f.endswith((".md", ".py", ".txt", ".json", ".yaml")) and f != "VERSION":
                continue
            chemin = os.path.join(racine, f)
            t = open(chemin, encoding="utf-8").read()
            if prenom:
                t2 = anonymise(t, prenom)
                if t2 != t:
                    open(chemin, "w", encoding="utf-8").write(t2)
                if re.search(rf"\b{re.escape(prenom)}\b", t2):
                    restes.append(os.path.relpath(chemin, dst))
            if re.search(MOTS_PERSO, t2 if prenom else t, re.I):
                restes.append(os.path.relpath(chemin, dst) + " (mention personnelle)")
    if restes:
        sys.exit("Références personnelles restantes, rien n'est produit : " + ", ".join(restes))

    os.makedirs(a.out, exist_ok=True)
    sortie_dossier = os.path.join(a.out, "edh-deck-builder")
    if os.path.exists(sortie_dossier):
        shutil.rmtree(sortie_dossier)
    shutil.copytree(dst, sortie_dossier)
    skill = os.path.join(a.out, "edh-deck-builder.skill")
    save_profile.package(dst, skill)
    empreinte = hashlib.sha256(open(skill, "rb").read()).hexdigest()
    open(skill + ".sha256", "w", encoding="utf-8").write(f"{empreinte}  edh-deck-builder.skill\n")
    version = open(os.path.join(dst, "VERSION"), encoding="utf-8").read().strip()
    print(f"Copie publique {version} : {skill}")
    print(f"SHA-256 : {empreinte}")
    print(f"Fichiers privés retirés : {', '.join(PRIVES)} ; profil vierge ; prénom remplacé par « l'auteur ».")


if __name__ == "__main__":
    main()
