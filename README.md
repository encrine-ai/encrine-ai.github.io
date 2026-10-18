# La page d'accueil d'Encrine

Le site https://encrine.ai : il explique le principe, guide l'enseignant qui veut créer sa classe, et montre « Les classes » que des enseignants ont choisi de partager. Une classe partagée reste dans le dépôt de son auteur, qui peut la retirer à tout moment ; cette page n'en garde qu'une fiche.

Site statique, sans étape de fabrication : `index.html`, `styles.css`, `classes.json` (les classes partagées), `assets/` (logos, icône), `fonts/` (Marelle, auto-hébergée). Unbounded et Figtree viennent de Google Fonts. Le style suit le design system Encrine, « Le parcours ».

## Mettre en ligne

1. Pousser ces fichiers à la racine du dépôt `encrine-ai.github.io` de l'organisation, branche `main`.
2. Dans les réglages du dépôt, *Pages* : source « Deploy from a branch », branche `main`, dossier `/` (root). Aucun workflow n'est nécessaire.
3. Le fichier `CNAME` contient `encrine.ai`. Chez le registraire du domaine, créer :
   - pour `encrine.ai` (domaine nu) quatre enregistrements `A` vers `185.199.108.153`, `185.199.109.153`, `185.199.110.153`, `185.199.111.153` (et, si possible, les `AAAA` `2606:50c0:8000::153` à `2606:50c0:8003::153`) ;
   - pour `www.encrine.ai` un `CNAME` vers `encrine-ai.github.io`.
4. Une fois le domaine vérifié par GitHub, cocher *Enforce HTTPS*.

Comme pour Ludea, le domaine n'est déclaré qu'une fois, sur ce dépôt : les autres dépôts Pages de l'organisation sont alors servis à `encrine.ai/<dépôt>/` sans réglage supplémentaire.

## Les sections de la page

Dans l’ordre : le héros, « Sur cette page » (le sommaire), Comment ça marche (les deux façons de commencer, puis les questions de l’entretien), Ce que vous recevez (neuf cases, chacune avec « Le détail » qui se déplie), Vos retours, Les classes (la galerie), Sous le capot (les quatorze skills du moteur), Les contrôles, Ce qui est prêt, l’appel final.

Chaque chose ne se dit qu’à un endroit. Les garanties (le programme couvert, une page par fiche, le choix des photos, les licences, les skills mesurés) ne se détaillent que dans Les contrôles ; ailleurs, un renvoi « voir Les contrôles ». La boucle des retours et la mise à jour du moteur vivent dans Vos retours, le partage dans Les classes : les cartes des skills correspondants, dans Sous le capot, y renvoient sans les répéter. L’ancre `#fonctionnalites` reste valable : elle mène à Ce que vous recevez.

Ce que vous recevez, Sous le capot et Les contrôles décrivent le moteur (`encrine-ai/moteur`) : chaque phrase y a été vérifiée dans son `README.md`, ses skills (`.claude/skills/*/SKILL.md`) et ses scripts. Quand le moteur change (un skill ajouté, un contrôle nouveau), ces trois sections se mettent à jour avec lui ; une chose prévue mais pas prête n’y entre pas. Les chiffres sont ceux du moteur, jamais ceux d’une classe (159 : les attendus de la liste de Grande Section, `referentiel/cycle1-gs.yml`).

## Les adresses à tenir à jour

En bas de `index.html`, l'objet `LIENS` porte le propriétaire et le nom du dépôt modèle (`encrine-ai` / `moteur`), le nom de ce dépôt (`encrine-ai.github.io`, pour « Signaler une classe », qui ouvre une issue ici) et l'adresse de la classe d'exemple, la démonstration, une classe à part (`encrine-ai/tour-du-monde`) (`https://encrine.ai/tour-du-monde/`). Les liens de la page sont réécrits depuis cet objet ; les adresses écrites en dur dans le HTML ne servent qu'aux navigateurs sans JavaScript, à aligner si l'on change l'objet.

## Les classes : `classes.json`

La section « Les classes » est une galerie construite à partir de `classes.json`. La classe d’exemple (`"exemple": true`) vient toujours en premier, avec le badge « Classe d’exemple » ; les classes partagées suivent. Chaque carte prend les couleurs **de son thème** (la frise de ses milieux), jamais celles d'Encrine, et propose deux actions : « Voir la classe » (le site de l'enseignant) et « Partir de cette classe ». Ce bouton ouvre un panneau unique (`<dialog id="partir">`, Échap pour fermer), rempli pour la carte : créer son dépôt depuis le modèle (lien construit depuis `LIENS`), activer le site, puis taper `/nouvelle-classe <site>` dans Claude Code, avec un bouton « Copier ».

```json
{
  "version": 1,
  "classes": [
    {
      "id": "cp-contes-2027-2028",                        // unique, minuscules et tirets
      "exemple": false,                                   // facultatif : true pour la classe d'exemple d'Encrine, montrée en premier
      "titre": "Il était une fois",
      "niveau": "CP",
      "annee": "2027-2028",
      "zone": "B",
      "accroche": "Un conte par période…",                // facultatif : une ou deux phrases sur la classe
      "milieux": [ { "nom": "les contes de randonnée", "couleur": "#7a4b9c", "semaines": 7 } ],  // une entrée par période, couleur du thème, semaines dans la zone
      "auteur": "M. Martin",                              // nom ou pseudonyme, au choix de l'auteur
      "licence": "CC BY-SA 4.0",                          // par défaut
      "licence_note": "sauf les pictogrammes ARASAAC, sous leur propre licence",  // facultatif : les exceptions
      "site": "https://…",                                // le site de la classe, et le lien donné à /nouvelle-classe
      "depot": "https://github.com/…",                    // le dépôt de la classe
      "verifie": { "attendus": "120/120", "pdf": 140, "pagination": true, "le": "2027-09-20" },  // facultatif (absent pour la classe d'exemple, en cours d'écriture)
      "partagee_le": "2027-09-21"                         // facultatif
    }
  ]
}
```

(Exemple fictif ; les commentaires ne sont qu'explicatifs : le fichier est du JSON strict. Aujourd'hui la liste ne contient que la classe d'exemple, « Le tour du monde » ; sous sa carte, un message dit que les premières classes partagées apparaîtront ici.)

### Ajouter une classe

1. L'enseignant le demande dans sa classe : le skill `partager-ma-classe` vérifie que l'année couvre le programme, que les PDF sont fabriqués et paginés, que chaque image et chaque texte a une licence qui permet le partage, et qu'aucune donnée d'élève n'y figure ; il prépare l'enregistrement de `classes.json`.
2. Il ouvre une **demande de fusion sur ce dépôt**, qui n'ajoute que cet enregistrement.
3. Une personne la relit (le contenu de la classe, ses licences, son ton) et le propriétaire de ce dépôt la fusionne. La carte apparaît au déploiement suivant.

### Retirer une classe

L'auteur le demande, ou retire lui-même son dépôt : son enregistrement est enlevé de `classes.json` par une demande de fusion, sans discussion. « Signaler une classe » ouvre une issue sur ce dépôt.

## Licences

Marelle, Unbounded et Figtree sont sous SIL Open Font License 1.1 (`fonts/LICENCE-Marelle.txt`). Le nom « encrine » du logo est tracé depuis Marelle.
