"""Met à jour le skill avec une nouvelle version en gardant le profil de la personne.

Usage : python update_skill.py nouvelle_version.skill [--profil PROFIL.md] [--out <fichier .skill>]

Le profil actuel est celui du skill installé (le PROFIL.md à côté de ce script, sauf --profil).
Le script ouvre la nouvelle version, part de ses valeurs neutres (VIERGE de son save_profile.py),
y reporte chaque réglage du profil actuel, puis fait valider et empaqueter le tout par le
save_profile.py de la nouvelle version : c'est son code qui juge le profil. Le profil contenu dans
la nouvelle version (vierge ou celui d'une autre personne) n'est jamais repris.
Il affiche les réglages gardés, les réglages nouveaux (avec leur valeur neutre) et ceux que la
nouvelle version ne connaît plus.
"""
import argparse
import importlib.util
import json
import os
import subprocess
import sys
import shutil
import tempfile
import zipfile

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(HERE, "scripts"))
from save_profile import read_profile  # noqa: E402

PRIVES = ["A_FAIRE.md"]  # fichiers de développement absents de la copie publique, gardés à la mise à jour


def version(dossier):
    try:
        return open(os.path.join(dossier, "VERSION"), encoding="utf-8").read().strip() or "inconnue"
    except OSError:
        return "inconnue"


def load_module(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("nouvelle_version")
    ap.add_argument("--profil", default=os.path.join(HERE, "PROFIL.md"))
    ap.add_argument("--out", default="/mnt/user-data/outputs/edh-deck-builder.skill")
    a = ap.parse_args()
    sys.stdout.reconfigure(encoding="utf-8")

    actuel = read_profile(a.profil)
    if not actuel.get("proprietaire"):
        sys.exit("Le skill installé a un profil vierge : rien à garder. Installe directement la nouvelle version.")

    tmp = tempfile.mkdtemp()
    try:
        with zipfile.ZipFile(a.nouvelle_version) as z:
            z.extractall(tmp)
    except (zipfile.BadZipFile, FileNotFoundError) as exc:
        sys.exit(f"Fichier illisible ({exc}) : il faut le fichier .skill de la nouvelle version.")
    racines = [d for d in os.listdir(tmp) if os.path.isfile(os.path.join(tmp, d, "SKILL.md"))]
    if len(racines) != 1 or not os.path.isfile(os.path.join(tmp, racines[0], "scripts", "save_profile.py")):
        sys.exit("Ce fichier n'est pas une version du skill edh-deck-builder (SKILL.md ou save_profile.py absent).")
    nouveau_dir = os.path.join(tmp, racines[0])

    # Fichiers privés du skill installé (absents d'une copie publique) : gardés tels quels.
    prives_gardes = []
    for f in PRIVES:
        src = os.path.join(os.path.dirname(os.path.abspath(a.profil)), f)
        if os.path.isfile(src) and not os.path.exists(os.path.join(nouveau_dir, f)):
            shutil.copy2(src, os.path.join(nouveau_dir, f))
            prives_gardes.append(f)

    nouveau_sp = load_module(os.path.join(nouveau_dir, "scripts", "save_profile.py"), "save_profile_nouveau")
    neutre = json.loads(json.dumps(getattr(nouveau_sp, "VIERGE", {})))
    langue_ajoutee = actuel.get("langue") is None and "langue" in neutre
    if langue_ajoutee:
        actuel = {**actuel, "langue": "fr"}  # un profil antérieur au réglage de langue est en français

    fusion = dict(neutre)
    gardes, nouveaux, retires = [], [], []
    for k, v in actuel.items():
        if not neutre or k in neutre:
            if isinstance(v, dict) and isinstance(neutre.get(k), dict):
                fusion[k] = {**neutre[k], **v}  # sous-réglage nouveau : valeur neutre, le reste gardé
                nouveaux += [f"{k}.{s}" for s in neutre[k] if s not in v]
            else:
                fusion[k] = v
            gardes.append(k)
        else:
            retires.append(k)
    nouveaux += [k for k in neutre if k not in actuel]
    if langue_ajoutee:
        gardes.remove("langue")
        nouveaux.append("langue")

    proc = subprocess.run(
        [sys.executable, os.path.join(nouveau_dir, "scripts", "save_profile.py"),
         "--json", json.dumps(fusion, ensure_ascii=False), "--skill-dir", nouveau_dir, "--out", a.out],
        capture_output=True, text=True)
    if proc.returncode != 0 or "refusé" in proc.stdout:
        print(proc.stdout + proc.stderr)
        sys.exit("La nouvelle version refuse ce profil : rien n'a été produit. Corrige le réglage indiqué, "
                 "puis relance.")

    print(f"Profil de {actuel.get('proprietaire')} reporté dans la nouvelle version : {a.out}")
    print(f"Version : {version(os.path.dirname(os.path.abspath(a.profil)))} → {version(nouveau_dir)}")
    print("Réglages gardés : " + (", ".join(gardes) or "aucun"))
    print("Réglages nouveaux, à leur valeur neutre : "
          + (", ".join(f"{k} = {json.dumps(_get(fusion, k), ensure_ascii=False)}" for k in nouveaux) or "aucun"))
    if prives_gardes:
        print("Fichiers privés gardés : " + ", ".join(prives_gardes))
    if retires:
        print("Réglages que la nouvelle version ne connaît plus (abandonnés) : " + ", ".join(retires))


def _get(d, chemin):
    for part in chemin.split("."):
        d = d.get(part) if isinstance(d, dict) else None
    return d


if __name__ == "__main__":
    main()
