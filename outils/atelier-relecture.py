#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Préparer l'atelier où l'on relit une classe soumise avec les outils DU MOTEUR.

Une classe soumise à la galerie est écrite par un inconnu : on n'exécute
jamais ses scripts. L'atelier est une copie de la classe (au commit relu) où
tout ce qui s'exécute sur notre machine est remplacé par la version de
confiance du moteur (encrine-ai/moteur) : scripts/ et referentiel/ (la liste
du programme et le calendrier officiel) viennent du moteur ; .agents/,
.claude/, .github/, .githooks/, les fichiers à la racine qui s'exécutent
(*.py, *.sh, Makefile…) sont retirés. Le reste — documents, cahiers HTML,
images, crédits, classe.yml, classe/ — n'est que lu.

    python3 -I outils/atelier-relecture.py <clone-de-la-classe> <clone-du-moteur> <atelier>
    cd <atelier>
    python3 -I scripts/couverture.py --manques   # le programme couvert
    python3 -I scripts/verifier-partage.py       # prénoms, images hors banques, textes recopiés
    python3 -I scripts/chercher-pictos.py verifier   # crédit et licence de chaque pictogramme

Ces trois contrôles ne lisent que des données (YAML, Markdown, HTML, JSON,
images). NE PAS lancer dans l'atelier `classe.py verifier|generer`,
`verifier-imagier.py`, `verifier-cartes-corpus.py` ni aucun `generer-*` : ils
exécutent les manifestes Python de la classe (classe/imagier.py,
classe/corpus.py, `classe.manifeste()`) ; ni `verifier-theme.py`, qui fait
tourner le gabarits.js du thème de la classe sous Node.

Refuse (code 1) un classe.yml dont `contenu` pointe hors de la classe, ou
dont `contenu.referentiel` n'est pas un fichier du moteur.
"""
import pathlib
import shutil
import sys

import yaml

RETIRES = {".git", ".agents", ".claude", ".github", ".githooks", ".husky", ".vscode",
           "scripts", "referentiel", "node_modules", "tests"}
EXECUTABLES = {".py", ".sh", ".bash", ".js", ".cjs", ".mjs", ".ts", ".pl", ".rb"}


def main():
    if len(sys.argv) != 4:
        sys.exit(__doc__)
    classe, moteur, atelier = (pathlib.Path(a).resolve() for a in sys.argv[1:])
    if atelier.exists():
        sys.exit("✘ %s existe déjà : un atelier neuf par relecture" % atelier)
    if not (moteur / "scripts" / "couverture.py").is_file():
        sys.exit("✘ %s n'est pas un clone du moteur" % moteur)
    # les liens symboliques ne sont pas suivis : un lien vers /etc ou vers ~ reste un lien mort
    shutil.copytree(classe, atelier, symlinks=True,
                    ignore=lambda d, noms: [n for n in noms if pathlib.Path(d) == classe and n in RETIRES])
    for f in list(atelier.iterdir()):
        if f.is_file() and (f.suffix.lower() in EXECUTABLES or f.name in ("Makefile", "package.json")):
            f.unlink()
    for lien in [p for p in atelier.rglob("*") if p.is_symlink()]:
        lien.unlink()
    shutil.copytree(moteur / "scripts", atelier / "scripts")
    shutil.copytree(moteur / "referentiel", atelier / "referentiel")

    anomalies = []
    c = yaml.safe_load((atelier / "classe.yml").read_text(encoding="utf-8")) or {}
    for cle, rel in (c.get("contenu") or {}).items():
        p = pathlib.PurePosixPath(str(rel))
        if p.is_absolute() or ".." in p.parts:
            anomalies.append("contenu.%s = %r sort de la classe" % (cle, rel))
    ref = str((c.get("contenu") or {}).get("referentiel", ""))
    if not (ref.startswith("referentiel/") and (moteur / ref).is_file()):
        anomalies.append("contenu.referentiel = %r n'est pas une liste du programme du moteur" % ref)
    for a in anomalies:
        print("✘ " + a)
    print("Atelier prêt : %s (scripts et référentiel du moteur, données de la classe)" % atelier
          if not anomalies else "Atelier refusé : %d anomalie(s)" % len(anomalies))
    sys.exit(1 if anomalies else 0)


if __name__ == "__main__":
    main()
