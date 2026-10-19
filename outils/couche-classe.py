#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""La frontière entre la classe et le moteur, dans la copie d'une classe de la galerie.

Une classe acceptée est copiée dans l'organisation (encrine-ai/<id>) au
commit relu. Sur cette copie, deux couches, et deux règles :

- **la classe** (classe.yml, classe/, les documents 0*-…, les cahiers, les
  images et leurs crédits, le thème, le projet, LICENCE-CONTENU.md…) est
  TOUJOURS exactement celle du commit relu de l'enseignant — personne ne la
  retouche sur la copie ;
- **le moteur** (scripts/, referentiel/, le code du site, le socle de la
  charte, les skills, le déploiement, AGENTS.md et CLAUDE.md) est celui
  d'encrine-ai/moteur, posé par le skill synchroniser-moteur — jamais le code
  de l'enseignant.

Les couches suivent le tableau « Ce qui bouge, ce qui ne bouge jamais » du
skill synchroniser-moteur du moteur : à tenir aligné sur lui.

    python3 -I outils/couche-classe.py ecarts <clone-de-la-copie> <commit-relu>
        Ce qui, dans la couche classe, diffère entre le commit relu et la tête
        de la copie. Code 1 si une SOURCE de la classe a changé (le contenu
        publié n'est plus celui qui a été relu). Les fichiers que le moteur
        refait depuis les sources (classe.json, classe.js, cahiers de
        l'imagier et des cartes-corpus, bloc de tête du README,
        moteur.version) sont signalés, sans erreur : synchroniser-moteur les
        régénère.

    python3 -I outils/couche-classe.py appliquer <clone-de-la-copie> <commit>
        Rend la couche classe de la copie identique à celle de <commit> (déjà
        récupéré dans le clone : git fetch https://github.com/<source> <commit>) :
        fichiers repris tels quels, fichiers disparus retirés, la couche
        moteur et moteur.version de la copie gardés. Rien n'est committé :
        relire `git status`, puis régénérer et contrôler (skill relire-classe).

Le script ne lance que git : aucun code de la classe n'est exécuté.
"""
import fnmatch
import re
import subprocess
import sys

# La couche moteur : posée par synchroniser-moteur depuis encrine-ai/moteur.
MOTEUR_DOSSIERS = ("scripts/", "referentiel/", ".agents/", ".claude/", ".github/", "tests/",
                   "site/charte/polices/", "site/marque/")
MOTEUR_FICHIERS = ("AGENTS.md", "CLAUDE.md", "LICENSE", ".gitignore",
                   "site/charte/socle.css", "site/charte/composants.css",
                   "site/fiches/fiches.css", "site/imagier/imagier.css",
                   "site/cartes-corpus/cartes-corpus.css")
# Fabriqués par le moteur (classe.py generer, generer-icones.py) : jamais copiés.
FABRIQUES = ("site/charte/charte.css", "site/charte/gabarits.js", "site/charte/icones.svg",
             "site/manifest.webmanifest", "site/sw.js", "site/favicon.ico", "site/icones/*")
# De la classe, mais refaits par le moteur depuis ses sources.
REFAITS = ("site/classe.json", "site/classe.js", "site/imagier/periode-*.html",
           "site/cartes-corpus/periode-*.html")
BLOC_README = re.compile(r"<!-- encrine:debut -->.*?<!-- encrine:fin -->", re.S)
VERSION_MOTEUR = re.compile(r"(^moteur:[ \t]*\n(?:[ \t]+.*\n)*?[ \t]+version:[ \t]*)([^\n]*)", re.M)


def couche(chemin):
    if chemin.startswith(MOTEUR_DOSSIERS) or chemin in MOTEUR_FICHIERS:
        return "moteur"
    if "/" not in chemin.removeprefix("site/") and chemin.startswith("site/") \
            and chemin.endswith((".js", ".html", ".css")) and chemin != "site/classe.js":
        return "fabrique" if chemin == "site/sw.js" else "moteur"   # site/*.js, *.html, *.css
    if any(fnmatch.fnmatch(chemin, m) for m in FABRIQUES):
        return "fabrique"
    if any(fnmatch.fnmatch(chemin, m) for m in REFAITS):
        return "refait"
    return "classe"


def git(depot, *args, binaire=False):
    r = subprocess.run(["git", "-C", depot, *args], capture_output=True)
    if r.returncode:
        sys.exit("✘ git %s : %s" % (" ".join(args), r.stderr.decode(errors="replace").strip()))
    return r.stdout if binaire else r.stdout.decode("utf-8", errors="replace")


def fichiers(depot, ref):
    return set(git(depot, "ls-tree", "-r", "--name-only", "-z", ref).split("\0")) - {""}


def montrer(depot, ref, chemin):
    return git(depot, "show", "%s:%s" % (ref, chemin), binaire=True)


def sans_version(texte):
    return VERSION_MOTEUR.sub(lambda m: m.group(1) + "<version>", texte)


def ecarts(depot, commit):
    avant, apres = fichiers(depot, commit), fichiers(depot, "HEAD")
    sources, refaits = [], []
    for f in sorted(avant | apres):
        k = couche(f)
        if k in ("moteur", "fabrique"):
            continue
        a = montrer(depot, commit, f) if f in avant else None
        b = montrer(depot, "HEAD", f) if f in apres else None
        if a == b:
            continue
        if f == "classe.yml" and a and b and sans_version(a.decode()) == sans_version(b.decode()):
            refaits.append("classe.yml (moteur.version seulement)")
            continue
        if f == "README.md" and a and b and BLOC_README.sub("", a.decode()) == BLOC_README.sub("", b.decode()):
            refaits.append("README.md (bloc de tête seulement)")
            continue
        etat = "ajouté" if a is None else "retiré" if b is None else "modifié"
        (refaits if k == "refait" else sources).append("%s (%s)" % (f, etat))
    for f in refaits:
        print("· refait par le moteur : " + f)
    for f in sources:
        print("✘ contenu changé depuis le commit relu : " + f)
    print("%d source(s) de la classe changée(s) depuis %s, %d fichier(s) refait(s) par le moteur"
          % (len(sources), commit[:7], len(refaits)))
    return 1 if sources else 0


def appliquer(depot, commit):
    if git(depot, "status", "--porcelain").strip():
        sys.exit("✘ l'arbre de travail de %s n'est pas propre" % depot)
    voulu, present = fichiers(depot, commit), fichiers(depot, "HEAD")
    reprendre = sorted(f for f in voulu if couche(f) in ("classe", "refait"))
    retirer = sorted(f for f in present - voulu if couche(f) in ("classe", "refait"))
    version = VERSION_MOTEUR.search(montrer(depot, "HEAD", "classe.yml").decode()) if "classe.yml" in present else None
    for i in range(0, len(reprendre), 200):
        git(depot, "checkout", commit, "--", *reprendre[i:i + 200])
    for i in range(0, len(retirer), 200):
        git(depot, "rm", "-q", "--", *retirer[i:i + 200])
    if version and "classe.yml" in voulu:
        chemin = git(depot, "rev-parse", "--show-toplevel").strip() + "/classe.yml"
        with open(chemin, encoding="utf-8") as f:
            texte = f.read()
        texte = VERSION_MOTEUR.sub(lambda m: m.group(1) + version.group(2), texte, count=1)
        with open(chemin, "w", encoding="utf-8") as f:
            f.write(texte)
        git(depot, "add", "classe.yml")
    print("Couche classe de %s : %d fichier(s) repris, %d retiré(s) ; moteur et moteur.version de la copie gardés"
          % (commit[:7], len(reprendre), len(retirer)))
    print(git(depot, "status", "--short") or "(rien n'a changé)")
    return 0


def main():
    if len(sys.argv) != 4 or sys.argv[1] not in ("ecarts", "appliquer"):
        sys.exit(__doc__)
    action, depot, commit = sys.argv[1:]
    commit = git(depot, "rev-parse", "--verify", commit + "^{commit}").strip()
    sys.exit((ecarts if action == "ecarts" else appliquer)(depot, commit))


if __name__ == "__main__":
    main()
