"""Enregistre un nouveau profil et reconstruit le fichier .skill à installer.

Usage :
  python save_profile.py --json '<profil JSON>' [--skill-dir <dossier du skill>] [--out <fichier .skill>]
  python save_profile.py --vierge [--out <fichier .skill>]   copie à partager, profil vierge (premier usage)

Le skill installé est en lecture seule : le script en copie le dossier, remplace seulement le
bloc JSON de PROFIL.md, vérifie le profil, puis empaquette le tout dans un fichier .skill
(archive zip, sans __pycache__ ni evals). L'utilisateur l'installe ensuite d'un clic.
Sans --skill-dir, le dossier est celui qui contient ce script.
"""
import argparse
import json
import os
import re
import shutil
import sys
import tempfile
import zipfile

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BLOCK = re.compile(r"```json\s*\n(.*?)\n```", re.S)

PISTES = {"ne_pas_proposer", "proposer", "mettre_en_avant"}
VIERGE = {
    # langue : None = pas encore connue ; le skill prend celle du premier message de la personne.
    "proprietaire": None, "langue": None, "ton": "tutoiement",
    # Par défaut, les règles officielles des brackets : combos et verrous ne sont interdits que par
    # le bracket. La synergie avant la puissance reste un parti pris du skill (désactivable).
    "principes": {"pas_de_combo_infinie": False, "pas_de_verrou": False, "synergie_avant_puissance": True},
    "bracket_defaut": None, "puissance_defaut": None, "budget_defaut": None,
    "pistes_inhabituelles": "proposer",
    "base_de_mana": ["terrains"],
    "collection": {"classeurs": [], "classeurs_partages": [], "ignorer_listes": True, "proxies_possedes": False},
    "prix": {"devise": "EUR", "reference": "prix de tendance Cardmarket", "seuil_mise_en_evidence": 30},
}
REFERENCES = {"EUR": "prix de tendance Cardmarket", "USD": "prix de marché TCGplayer"}
MANA = {"terrains", "rocks", "dorks", "tresors", "ramp", "tuteurs_de_terrain"}


def read_profile(path):
    text = open(path, encoding="utf-8").read()
    m = BLOCK.search(text)
    if not m:
        raise ValueError(f"Aucun bloc JSON trouvé dans {path}")
    return json.loads(m.group(1))


def validate(p):
    errors = []
    if not str(p.get("proprietaire", "")).strip():
        errors.append("proprietaire vide")
    if p.get("langue", "fr") not in ("fr", "en"):
        errors.append("langue : fr ou en")
    if p.get("ton") not in ("tutoiement", "vouvoiement"):
        errors.append("ton : tutoiement ou vouvoiement")
    pr = p.get("principes", {})
    for k in ("pas_de_combo_infinie", "pas_de_verrou", "synergie_avant_puissance"):
        if not isinstance(pr.get(k), bool):
            errors.append(f"principes.{k} doit valoir true ou false")
    if p.get("bracket_defaut") not in (None, 1, 2, 3, 4, 5):
        errors.append("bracket_defaut : null ou 1 à 5")
    if p.get("puissance_defaut") not in (None, "detendu", "equilibre", "affute"):
        errors.append("puissance_defaut : null, detendu (1-3), equilibre (4-7) ou affute (8-10)")
    b = p.get("budget_defaut")
    if b is not None and (not isinstance(b, (int, float)) or b < 0):
        errors.append("budget_defaut : null ou un montant positif")
    if p.get("pistes_inhabituelles") not in PISTES:
        errors.append("pistes_inhabituelles : " + ", ".join(sorted(PISTES)))
    mb = set(p.get("base_de_mana", []))
    if "terrains" not in mb or not mb <= MANA:
        errors.append("base_de_mana : doit contenir terrains, et seulement " + ", ".join(sorted(MANA)))
    prix = p.get("prix", {})
    if prix.get("devise") not in REFERENCES:
        errors.append("prix.devise : EUR (Cardmarket) ou USD (TCGplayer)")
    s = prix.get("seuil_mise_en_evidence")
    if not isinstance(s, (int, float)) or isinstance(s, bool) or s < 0:
        errors.append("prix.seuil_mise_en_evidence : un montant positif")
    col = p.get("collection", {})
    if not isinstance(col.get("classeurs", []), list) or not isinstance(col.get("ignorer_listes", True), bool) \
            or not isinstance(col.get("proxies_possedes", False), bool):
        errors.append("collection : classeurs (liste), ignorer_listes et proxies_possedes (true/false)")
    return errors


def write_profile(path, p):
    text = open(path, encoding="utf-8").read()
    new = "```json\n" + json.dumps(p, ensure_ascii=False, indent=2) + "\n```"
    with open(path, "w", encoding="utf-8") as f:
        f.write(BLOCK.sub(lambda _: new, text, count=1))


def package(src, out):
    name = os.path.basename(os.path.normpath(src))
    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as z:
        for root, dirs, files in os.walk(src):
            dirs[:] = [d for d in dirs if d not in ("__pycache__", "evals")]
            for f in files:
                if f.endswith(".pyc"):
                    continue
                full = os.path.join(root, f)
                z.write(full, os.path.join(name, os.path.relpath(full, src)))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--json", default=None)
    ap.add_argument("--vierge", action="store_true", help="produire une copie à partager, avec un profil vierge")
    ap.add_argument("--export", action="store_true",
                    help="afficher le profil actuel en une ligne à conserver (« Enregistre mon profil EDH : {…} »)")
    ap.add_argument("--skill-dir", default=HERE)
    ap.add_argument("--out", default="/mnt/user-data/outputs/edh-deck-builder.skill")
    a = ap.parse_args()
    sys.stdout.reconfigure(encoding="utf-8")

    current = read_profile(os.path.join(a.skill_dir, "PROFIL.md"))
    if a.export:
        exp = dict(current)
        exp.setdefault("langue", "fr")
        print("Enregistre mon profil EDH : " + json.dumps(exp, ensure_ascii=False, separators=(",", ":")))
        return
    if a.vierge:
        merged = dict(VIERGE)
        errors = []
    else:
        if not a.json:
            sys.exit("Indique --json '<profil>' ou --vierge.")
        try:
            new = json.loads(a.json)
        except json.JSONDecodeError as exc:
            sys.exit(f"Profil illisible (JSON invalide) : {exc}")
        current.setdefault("langue", "fr")  # un profil antérieur au réglage de langue est en français
        merged = {**current, **new}
        prix = merged.get("prix") or {}
        if prix.get("devise") in REFERENCES:  # la référence suit toujours la devise
            merged["prix"] = {**prix, "reference": REFERENCES[prix["devise"]]}
        errors = validate(merged)
    if errors:
        print("Profil refusé :")
        for e in errors:
            print(f"- {e}")
        sys.exit(1)

    tmp = tempfile.mkdtemp()
    build = os.path.join(tmp, os.path.basename(os.path.normpath(a.skill_dir)))
    shutil.copytree(a.skill_dir, build, ignore=shutil.ignore_patterns("__pycache__", "*.pyc", "evals"))
    write_profile(os.path.join(build, "PROFIL.md"), merged)
    os.makedirs(os.path.dirname(a.out), exist_ok=True)
    package(build, a.out)

    if a.vierge:
        print("Copie à partager produite, avec un profil vierge : le skill proposera ses réglages à la première utilisation.")
    else:
        changes = [k for k in merged if merged.get(k) != current.get(k)]
        print("Profil enregistré. Réglages modifiés : " + (", ".join(changes) if changes else "aucun"))
    print(f"Skill reconstruit : {a.out}")


if __name__ == "__main__":
    main()
