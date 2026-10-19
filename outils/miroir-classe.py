#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Recopier, depuis le site EN LIGNE d'une classe, ce que contrôle la pagination.

Deux usages : à la relecture, le site de l'enseignant au commit relu (ce que
fabrique son propre déploiement) ; après la publication et chaque nuit, la
copie relue servie par Encrine (https://encrine.ai/<id>/), telle que la voient
les visiteurs. Ce script télécharge son classe.json,
la page HTML de chaque cahier et chaque PDF qu'il annonce, dans un dossier
neuf, sans rien exécuter de la classe. Ensuite, l'outil de confiance du moteur :

    python3 -I outils/miroir-classe.py https://<propriétaire>.github.io/<dépôt>/ /tmp/relecture/<id>/site
    python3 -I /tmp/encrine-outils/scripts/verifier-pagination.py /tmp/relecture/<id>/site

classe.json est une donnée écrite par un inconnu : tout chemin qui sort du
site (« .. », adresse absolue, autre hôte) est refusé. Code 1 si un fichier
annoncé manque en ligne (un PDF absent est déjà un défaut de la classe).
"""
import json
import pathlib
import re
import sys
import urllib.parse
import urllib.request

SUR = re.compile(r"^[A-Za-z0-9._/-]+$")


def chemin_sur(rel):
    p = pathlib.PurePosixPath(rel)
    return bool(SUR.match(rel)) and not p.is_absolute() and ".." not in p.parts


def telecharger(url, dest):
    req = urllib.request.Request(url, headers={"User-Agent": "encrine-galerie-relecture"})
    with urllib.request.urlopen(req, timeout=60) as r:
        if r.status != 200:
            raise OSError("HTTP %d" % r.status)
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_bytes(r.read())


def main():
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    base = sys.argv[1].rstrip("/") + "/"
    if not base.startswith("https://"):
        sys.exit("✘ l'adresse du site doit commencer par https://")
    site = pathlib.Path(sys.argv[2])
    if site.exists() and any(site.iterdir()):
        sys.exit("✘ %s n'est pas vide : un dossier neuf par relecture" % site)
    site.mkdir(parents=True, exist_ok=True)
    telecharger(base + "classe.json", site / "classe.json")
    c = json.loads((site / "classe.json").read_text(encoding="utf-8"))
    fichiers = []
    for d in c.get("documents", []):
        if d.get("md"):
            fichiers.append("pdf/%s.pdf" % d["id"])
        if d.get("par_periode"):
            fichiers += ["pdf/%s-periode-%d.pdf" % (d["id"], n) for n in range(1, len(c["periodes"]) + 1)]
    for m in c.get("materiel", []):
        if "source" in m:
            for n in m.get("periodes", []):
                fichiers += [m["source"].replace("{n}", str(n)), m["pdf"].replace("{n}", str(n))]
    manques = 0
    for rel in fichiers:
        if not chemin_sur(rel):
            print("✘ chemin refusé dans classe.json : %r" % rel)
            manques += 1
            continue
        url = urllib.parse.urljoin(base, rel)
        if not url.startswith(base):
            print("✘ adresse hors du site refusée : %s" % url)
            manques += 1
            continue
        try:
            telecharger(url, site / rel)
        except Exception as e:  # 404, coupure…
            print("✘ %s : %s" % (url, e))
            manques += 1
    print("%d fichiers recopiés depuis %s, %d manquant(s)" % (len(fichiers) - manques, base, manques))
    sys.exit(1 if manques else 0)


if __name__ == "__main__":
    main()
