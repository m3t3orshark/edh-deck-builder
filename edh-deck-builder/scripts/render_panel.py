"""Génère le panneau de réglages (fragment HTML) à partir de PROFIL.md.

Usage : python render_panel.py [--profil PROFIL.md] [--export ManaBox_Collection.csv] [--langue fr|en] [--out panel.html]

Le fragment est prévu pour l'outil d'affichage interactif de Claude (variables CSS de l'hôte,
fonction sendPrompt). Le bouton « Enregistrer » envoie : « Enregistre mon profil EDH : {json} ».
Avec --export, les classeurs de l'export ManaBox sont proposés en plus de ceux du profil.
Le panneau est dans la langue du profil (`langue`, `fr` si absent) ; --langue l'impose, par exemple
pour un profil vierge, dans la langue du premier message de la personne. En anglais, le bouton envoie
« Save my EDH profile: {json} ».
"""
import argparse
import csv
import html
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from save_profile import read_profile  # noqa: E402

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

MANA = [("terrains", "Terrains"), ("rocks", "Rocks"), ("dorks", "Dorks"), ("tresors", "Trésors"),
        ("ramp", "Ramp"), ("tuteurs_de_terrain", "Tuteurs de terrain")]
BRACKETS = [("", "Aucun (demander)"), ("1", "1 · Exhibition"), ("2", "2 · Core"), ("3", "3 · Upgraded"),
            ("4", "4 · Optimized"), ("5", "5 · cEDH")]
DEVISES = [("EUR", "Euro (Cardmarket)"), ("USD", "Dollar (TCGplayer)")]
SYMBOLES = {"EUR": "€", "USD": "$"}
LANGUES = [("fr", "Français"), ("en", "English")]
# Libellés visibles du panneau : français → anglais (le français est la langue du gabarit).
EN = {
    "Profil": "Profile", "Propriétaire": "Owner", "Ton": "Form of address", "Tutoiement": "Tutoiement",
    "Vouvoiement": "Vouvoiement", "Langue": "Language",
    "Principes et valeurs par défaut": "Principles and defaults", "Jamais de combo infinie": "Never infinite combos",
    "Jamais de verrou": "Never locks", "Synergie avant puissance": "Synergy before raw power",
    "Bracket par défaut": "Default bracket", "Aucun (demander)": "None (ask)",
    "Puissance par défaut": "Default power", "Aucune (estimée seulement)": "None (estimated only)",
    "Détendu (1-3)": "Casual (1-3)", "Équilibré (4-7)": "Balanced (4-7)", "Affûté (8-10)": "Sharp (8-10)",
    "Budget par défaut (": "Default budget (", "Pistes inhabituelles": "Unusual ideas",
    "Ne pas proposer": "Don't suggest", "Proposer, sans imposer": "Suggest, never impose",
    "Mettre en avant": "Highlight", "Collection ManaBox": "ManaBox collection",
    "Ignorer les listes (envies)": "Ignore lists (wishlists)", "Compter les proxies comme possédés": "Count proxies as owned",
    "Aucun classeur connu": "No known binder", "La base de mana comprend": "The mana base includes",
    "Terrains": "Lands", "Trésors": "Treasures", "Tuteurs de terrain": "Land tutors", "Prix": "Prices",
    "Devise et référence": "Currency and source", "Signaler les cartes à partir de (": "Flag cards from (",
    "Enregistrer ↗": "Save ↗", "Indique un prénom pour le profil.": "Enter a name for the profile.",
}
PISTES = [("ne_pas_proposer", "Ne pas proposer"), ("proposer", "Proposer, sans imposer"),
          ("mettre_en_avant", "Mettre en avant")]


def opts(pairs, current):
    return "".join(f'<option value="{v}"{" selected" if str(current) == v else ""}>{html.escape(l)}</option>'
                   for v, l in pairs)


def chk(cls, value, label, checked, disabled=False):
    return (f'<label><input type="checkbox" class="{cls}" value="{html.escape(value)}"'
            f'{" checked" if checked else ""}{" disabled" if disabled else ""}>{html.escape(label)}</label>')


def binders_from_export(path):
    found = {}
    with open(path, encoding="utf-8-sig", newline="") as f:
        for row in csv.DictReader(f):
            if (row.get("Binder Type") or "").lower() != "list":
                found[row.get("Binder Name", "")] = True
    return [b for b in found if b]


def translate(out, langue):
    """Traduit les libellés visibles (texte entre balises, placeholder) ; le script et les valeurs ne changent pas."""
    if langue != "en":
        return out
    head, sep, script = out.partition("<script>")
    for fr, en in sorted(EN.items(), key=lambda kv: -len(kv[0])):
        head = head.replace(f">{fr}<", f">{en}<")
    head = (head.replace('placeholder="Ton prénom"', 'placeholder="Your name"')
                .replace('placeholder="Aucun"', 'placeholder="None"').replace(" (partagé)<", " (shared)<"))
    return head + sep + script


def render(p, extra_binders, langue=None):
    langue = langue or (p.get("langue") if p.get("langue") in dict(LANGUES) else "fr")
    pr = p.get("principes", {})
    col = p.get("collection", {})
    binders = list(dict.fromkeys(col.get("classeurs", []) + extra_binders))
    shared = set(col.get("classeurs_partages", []))
    prix = p.get("prix", {})
    devise = prix.get("devise") if prix.get("devise") in SYMBOLES else "EUR"
    sym = SYMBOLES[devise]
    puissance = [("", "Aucune (estimée seulement)"), ("detendu", "Détendu (1-3)"), ("equilibre", "Équilibré (4-7)"), ("affute", "Affûté (8-10)")]
    binder_html = "".join(chk("bd", b, b + (" (partagé)" if b in shared else ""), b in col.get("classeurs", []))
                          for b in binders) or '<span style="color:var(--text-muted)">Aucun classeur connu</span>'
    mana_html = "".join(chk("mb", v, l, v in p.get("base_de_mana", []), v == "terrains") for v, l in MANA)
    return f'''<h2 class="sr-only">{("EDH skill settings panel for " + html.escape(p.get("proprietaire") or "a new user") + ": profile, principles, collection, mana base and prices, with a save button.") if langue == "en" else ("Panneau de réglages du skill EDH de " + html.escape(p.get("proprietaire") or "un nouvel utilisateur") + " : profil, principes, collection, base de mana et prix, avec un bouton pour enregistrer.")}</h2>
<style>
.sec{{background:var(--surface-2);border:0.5px solid var(--border);border-radius:12px;padding:1rem 1.25rem;margin-bottom:12px}}
.sec h3{{margin:0 0 10px;font-size:15px;display:flex;align-items:center;gap:8px}}
.row{{display:flex;align-items:center;justify-content:space-between;gap:12px;padding:6px 0;font-size:14px}}
.row label{{color:var(--text-secondary)}}
.chk{{display:flex;flex-wrap:wrap;gap:8px 16px;font-size:14px}}
.chk label{{display:flex;align-items:center;gap:6px;color:var(--text-primary)}}
</style>
<div style="padding:0.5rem 0">
<div class="sec"><h3><i class="ti ti-user" aria-hidden="true"></i>Profil</h3>
<div class="row"><label for="owner">Propriétaire</label><input id="owner" value="{html.escape(p.get("proprietaire") or "")}" placeholder="Ton prénom" style="width:220px"></div>
<p id="err" style="font-size:13px;color:var(--text-danger);margin:0;display:none">Indique un prénom pour le profil.</p>
<div class="row"><label for="lang">Langue</label><select id="lang" style="width:220px">{opts(LANGUES, langue)}</select></div>
<div class="row" id="row-tone"{' style="display:none"' if langue == "en" else ""}><label for="tone">Ton</label><select id="tone" style="width:220px">{opts([("tutoiement", "Tutoiement"), ("vouvoiement", "Vouvoiement")], p.get("ton", "tutoiement"))}</select></div>
</div>
<div class="sec"><h3><i class="ti ti-shield-check" aria-hidden="true"></i>Principes et valeurs par défaut</h3>
<div class="chk">{chk("pr", "pas_de_combo_infinie", "Jamais de combo infinie", pr.get("pas_de_combo_infinie"))}{chk("pr", "pas_de_verrou", "Jamais de verrou", pr.get("pas_de_verrou"))}{chk("pr", "synergie_avant_puissance", "Synergie avant puissance", pr.get("synergie_avant_puissance"))}</div>
<div class="row"><label for="br">Bracket par défaut</label><select id="br" style="width:220px">{opts(BRACKETS, p.get("bracket_defaut") or "")}</select></div>
<div class="row"><label for="pw">Puissance par défaut</label><select id="pw" style="width:220px">{opts(puissance, p.get("puissance_defaut") or "")}</select></div>
<div class="row"><label for="bud">Budget par défaut (<span class="sym">{sym}</span>)</label><input id="bud" type="number" min="0" step="1" placeholder="Aucun" value="{p.get("budget_defaut") or ""}" style="width:220px"></div>
<div class="row"><label for="odd">Pistes inhabituelles</label><select id="odd" style="width:220px">{opts(PISTES, p.get("pistes_inhabituelles", "proposer"))}</select></div>
</div>
<div class="sec"><h3><i class="ti ti-cards" aria-hidden="true"></i>Collection ManaBox</h3>
<div class="chk">{binder_html}</div>
<div class="chk" style="margin-top:8px">{chk("li", "ignorer_listes", "Ignorer les listes (envies)", col.get("ignorer_listes", True))}{chk("px", "proxies_possedes", "Compter les proxies comme possédés", col.get("proxies_possedes", False))}</div>
</div>
<div class="sec"><h3><i class="ti ti-droplet" aria-hidden="true"></i>La base de mana comprend</h3>
<div class="chk">{mana_html}</div>
</div>
<div class="sec"><h3><i class="ti ti-coin" aria-hidden="true"></i>Prix</h3>
<div class="row"><label for="dev">Devise et référence</label><select id="dev" style="width:220px">{opts(DEVISES, devise)}</select></div>
<div class="row"><label for="seuil">Signaler les cartes à partir de (<span class="sym">{sym}</span>)</label><input id="seuil" type="number" min="0" step="1" value="{prix.get("seuil_mise_en_evidence", 30)}" style="width:220px"></div>
</div>
<div style="display:flex;justify-content:flex-end;margin-top:4px"><button id="save">Enregistrer ↗</button></div>
</div>
<script>
const base={json.dumps(p, ensure_ascii=False)};
const shared={json.dumps(sorted(shared), ensure_ascii=False)};
const $=id=>document.getElementById(id);
const vals=c=>[...document.querySelectorAll('.'+c)].filter(x=>x.checked).map(x=>x.value);
$('owner').addEventListener('input',()=>{{$('err').style.display='none'}});
$('lang').addEventListener('change',()=>{{$('row-tone').style.display=$('lang').value==='fr'?'':'none'}});
$('dev').addEventListener('change',()=>{{document.querySelectorAll('.sym').forEach(e=>{{e.textContent=$('dev').value==='USD'?'$':'€'}})}});
$('save').addEventListener('click',()=>{{
const o=$('owner').value.trim();
if(!o){{$('err').style.display='block';return}}
const pr=vals('pr');const b=$('bud').value.trim();const s=$('seuil').value.trim();
const prof=Object.assign({{}},base,{{
proprietaire:o,ton:$('tone').value,langue:$('lang').value,
principes:{{pas_de_combo_infinie:pr.includes('pas_de_combo_infinie'),pas_de_verrou:pr.includes('pas_de_verrou'),synergie_avant_puissance:pr.includes('synergie_avant_puissance')}},
bracket_defaut:$('br').value?Number($('br').value):null,
puissance_defaut:$('pw').value||null,
budget_defaut:b?Math.round(Number(b)):null,
pistes_inhabituelles:$('odd').value,
base_de_mana:vals('mb'),
collection:{{classeurs:vals('bd'),classeurs_partages:shared,ignorer_listes:vals('li').length>0,proxies_possedes:vals('px').length>0}},
prix:Object.assign({{}},base.prix||{{}},{{devise:$('dev').value,seuil_mise_en_evidence:s?Math.round(Number(s)):30}})
}});
sendPrompt(($('lang').value==='en'?'Save my EDH profile: ':'Enregistre mon profil EDH : ')+JSON.stringify(prof));
}});
</script>'''


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--profil", default=os.path.join(HERE, "PROFIL.md"))
    ap.add_argument("--export", default=None)
    ap.add_argument("--out", default=None)
    ap.add_argument("--langue", choices=["fr", "en"], default=None)
    a = ap.parse_args()
    sys.stdout.reconfigure(encoding="utf-8")
    p = read_profile(a.profil)
    extra = binders_from_export(a.export) if a.export else []
    langue = a.langue or (p.get("langue") if p.get("langue") in ("fr", "en") else "fr")
    out = translate(render(p, extra, langue), langue)
    if a.out:
        with open(a.out, "w", encoding="utf-8") as f:
            f.write(out)
        print(f"Panneau écrit dans {a.out}")
    else:
        print(out)


if __name__ == "__main__":
    main()
