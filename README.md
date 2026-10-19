# La page d'accueil d'Encrine

Le site https://encrine.ai : il explique le principe, guide l'enseignant qui veut créer sa classe, et montre « Les classes » que des enseignants ont choisi de partager. Une classe partagée reste dans le dépôt de son auteur, qui peut la retirer à tout moment ; cette page n'en garde qu'une fiche.

Site statique, sans étape de fabrication : `index.html`, `styles.css`, `site.js` (le script commun aux pages : l'en-tête, le menu du téléphone, le panneau, la galerie), `classes.json` (les classes partagées), les trois pages `contact/`, `mentions-legales/` et `confidentialite/`, la page `design/` (le design system), `assets/` (logos ; `icone-onglet.svg`, l'icône d'onglet, les trois cases sans fond ; `icone-encrine.svg`, la même sur fond ardoise, pour `apple-touch-icon`, où un fond est obligatoire), `fonts/` (Marelle, Unbounded et Figtree, toutes servies par le site : aucune requête vers un service tiers, ce que la page Confidentialité affirme). Le style suit le design system Encrine, « Le parcours ».

## Mettre en ligne

1. Pousser ces fichiers à la racine du dépôt `encrine-ai.github.io` de l'organisation, branche `main`.
2. Dans les réglages du dépôt, *Pages* : source « Deploy from a branch », branche `main`, dossier `/` (root). Aucun workflow n'est nécessaire.
3. Le fichier `CNAME` contient `encrine.ai`. Chez le registraire du domaine, créer :
   - pour `encrine.ai` (domaine nu) quatre enregistrements `A` vers `185.199.108.153`, `185.199.109.153`, `185.199.110.153`, `185.199.111.153` (et, si possible, les `AAAA` `2606:50c0:8000::153` à `2606:50c0:8003::153`) ;
   - pour `www.encrine.ai` un `CNAME` vers `encrine-ai.github.io`.
4. Une fois le domaine vérifié par GitHub, cocher *Enforce HTTPS*.

Comme pour Ludea, le domaine n'est déclaré qu'une fois, sur ce dépôt : les autres dépôts Pages de l'organisation sont alors servis à `encrine.ai/<dépôt>/` sans réglage supplémentaire.

## Les sections de la page

Dans l’ordre : l’en-tête (le logo, le menu, GitHub), le héros, « Sur cette page » (le sommaire), Comment ça marche (les deux façons de commencer, puis les questions de l’entretien), Ce que vous recevez (neuf cases, chacune avec « Le détail » qui se déplie), Vos retours, Les classes (la galerie), Sous le capot (les quatorze skills du moteur), Les contrôles, Ce qui est prêt, l’appel final, le pied de page (les liens vers les trois autres pages).

Chaque chose ne se dit qu’à un endroit. Les garanties (le programme couvert, une page par fiche, le choix des photos, les licences, les skills mesurés) ne se détaillent que dans Les contrôles ; ailleurs, un renvoi « voir Les contrôles ». La boucle des retours et la mise à jour du moteur vivent dans Vos retours, le partage dans Les classes : les cartes des skills correspondants, dans Sous le capot, y renvoient sans les répéter. L’ancre `#fonctionnalites` reste valable : elle mène à Ce que vous recevez.

Ce que vous recevez, Sous le capot et Les contrôles décrivent le moteur (`encrine-ai/moteur`) : chaque phrase y a été vérifiée dans son `README.md`, ses skills (`.claude/skills/*/SKILL.md`) et ses scripts. Quand le moteur change (un skill ajouté, un contrôle nouveau), ces trois sections se mettent à jour avec lui ; une chose prévue mais pas prête n’y entre pas. Les chiffres sont ceux du moteur, jamais ceux d’une classe (159 : les attendus de la liste de Grande Section, `referentiel/cycle1-gs.yml`).

## L'en-tête et le menu

L'en-tête est **toujours visible** (`position: sticky`) sur les cinq pages. Une fois la page descendue, `site.js` lui pose la classe `entete--descendu` : un filet fin en bas, et il se resserre sans que rien ne saute (sa boîte garde `--entete-haut`, il remonte de `--entete-retrait` sous le bord de l'écran, le logo rapetisse ; pas d'animation si l'appareil demande moins de mouvement). Les ancres placent leurs titres juste dessous (`scroll-margin-top`, calculé sur ces deux valeurs). Le lien d'évitement « Aller au contenu » et les panneaux `<dialog>` passent au-dessus.

Sous 1100 px (téléphone et tablette), l'en-tête ne garde que le logo et le bouton « Menu » (un burger), et il garde sa taille en défilant : seuls le filet et le fond apparaissent. Le bouton, posé par `site.js`, ouvre un panneau qui reprend en liste sobre le sommaire de l'accueil (la liste `SECTIONS` de `site.js`, à tenir alignée sur le sommaire de `index.html`), puis « Créer ma classe » et GitHub. Le sommaire en cases du haut de l'accueil s'efface alors (le menu fait le même travail), et la marelle du héros passe en filigrane derrière le texte (contraste du texte mesuré au-dessus de 4,5:1). Sur les autres pages, les liens du menu mènent à l'accueil (`../#…`).

## La page Design system

`design/index.html` : le style de la marque (le logo, les couleurs, les polices, les espaces et les formes, les composants, le ton). Elle montre les **vrais** composants, avec les classes de `styles.css` (les règles `ds-…` ne servent qu'à ses planches), et son script relit `styles.css`, les SVG d'`assets/` et les licences de `fonts/` pour écrire les valeurs : un code de couleur, une graisse, un angle ne s'y recopient jamais à la main. Un composant ajouté à l'accueil s'y ajoute ; le panneau `<dialog id="partir">` y est recopié, à aligner sur celui de l'accueil.

## Les autres pages

Trois pages de texte, avec le même en-tête et le même pied que l'accueil, et `styles.css` (les règles `.texte`) :

- `contact/` : hello@encrine.ai ; un problème dans une classe de la galerie, le mode retours pour l'enseignant qui a sa classe, le moteur et ses issues pour les développeurs ;
- `mentions-legales/` : l'éditeur (NORRECRAFT), le directeur de la publication, l'hébergeur (GitHub Pages), la propriété intellectuelle, le signalement d'un contenu ;
- `confidentialite/` : la politique de confidentialité (RGPD). Elle affirme que le site n'a ni compte, ni formulaire, ni cookie, ni mesure d'audience, ni publicité, ni service tiers : tout ajout d'un script, d'une police ou d'un outil extérieur doit d'abord la mettre à jour.

Le pied de page (Contact · Mentions légales · Confidentialité · Design system · GitHub · © 2026 Encrine) et l'en-tête sont recopiés dans les cinq pages : une modification se fait partout. Dans les trois pages, « Créer ma classe » mène à `../#creer`, qui ouvre le panneau sur l'accueil.

## Les adresses à tenir à jour

En haut de `site.js`, l'objet `LIENS` porte le propriétaire et le nom du dépôt modèle (`encrine-ai` / `moteur`), le nom de ce dépôt (`encrine-ai.github.io`, pour « Signaler une classe », qui ouvre une issue ici) et l'adresse de la classe d'exemple, la démonstration, une classe à part (`encrine-ai/tour-du-monde`) (`https://encrine.ai/tour-du-monde/`). Les liens de la page sont réécrits depuis cet objet ; les adresses écrites en dur dans le HTML ne servent qu'aux navigateurs sans JavaScript, à aligner si l'on change l'objet.

## Les classes : `classes.json`

La section « Les classes » est une galerie construite à partir de `classes.json`. La classe d’exemple (`"exemple": true`) vient toujours en premier, avec le badge « Classe d’exemple » ; les classes partagées suivent. Chaque carte prend les couleurs **de son thème** (la frise de ses milieux), jamais celles d'Encrine, et propose deux actions : « Voir la classe » (le site de l'enseignant) et « Partir de cette classe ». Les deux voies passent par le même panneau (`<dialog id="partir">`, un seul pour toute la page, rempli selon le bouton qui l'ouvre ; Échap pour fermer, le focus revient au bouton) :

- **« Créer ma classe »** (en-tête, haut de page, appel final) l'ouvre pour le modèle `moteur`, « Créer votre classe » : créer son dépôt depuis le modèle (lien construit depuis `LIENS`), activer le site (*Settings* → *Pages* → *Source* : *GitHub Actions*), puis taper `/nouvelle-classe` dans Claude Code, avec un bouton « Copier ». Sans JavaScript, le bouton reste un lien direct vers le modèle sur GitHub.
- **« Partir de cette classe »** l'ouvre pour la carte. Chaque classe partagée est elle-même un modèle GitHub : on crée son dépôt depuis **celle-ci** (`github.com/new?template_owner=<propriétaire>&template_name=<dépôt>`, tiré du champ `depot`), on active le site, puis on tape `/nouvelle-classe`, sans adresse : l'agent voit de quelle classe il part, annonce ce qu'il garde et cite la classe d'origine.

Avec un `apercu`, la carte prend toute la ligne : la capture de l'accueil du site sur un ordinateur, le téléphone posé devant, puis la fiche de la classe et la mention « S'installe comme une appli », qui renvoie au bloc `#appli` de l'accueil. Les captures se font sur le site en ligne, avec Playwright, à 1280 × 800 et à 390 × 844, sans l'invitation à installer (poser avant le chargement la clé `localStorage` `encrine-invitation:/<dépôt>/` à `fermee`) et sans service worker (`serviceWorkers: 'block'`) ; le site ne doit plus afficher « Chargement… ». Les chemins des images partent de la racine de ce site.

Le bouton « Partir de cette classe » n'apparaît que si la fiche a un `depot` et une licence qui permet la reprise : CC BY ou CC BY-SA (ni NC, ni ND). Le dépôt d'une classe partagée doit donc être marqué *Template repository* dans ses réglages.

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
      "apercu": {                                         // facultatif : l'accueil du site de la classe, en captures (WebP, moins de 150 Ko chacune, dans assets/classes/)
        "ordinateur": "assets/classes/il-etait-une-fois-ordinateur.webp",  // 1280 × 800
        "telephone": "assets/classes/il-etait-une-fois-telephone.webp",    // 390 × 844
        "alt": "L'accueil du site « Il était une fois » : …"              // ce que montre la capture
      },
      "icone": "assets/classes/il-etait-une-fois-icone.png", // facultatif : l'icône d'appli de la classe, montrée en petit à côté du titre ; vide ou absent, rien n'est montré
      "milieux": [ { "nom": "les contes de randonnée", "couleur": "#7a4b9c", "semaines": 7 } ],  // une entrée par période, couleur du thème, semaines dans la zone
      "auteur": "M. Martin",                              // nom ou pseudonyme, au choix de l'auteur
      "licence": "CC BY-SA 4.0",                          // par défaut ; CC BY ou CC BY-SA pour que la classe puisse être reprise
      "licence_note": "sauf les pictogrammes ARASAAC, sous leur propre licence",  // facultatif : les exceptions
      "site": "https://…",                                // le site de la classe (« Voir la classe »)
      "depot": "martin/il-etait-une-fois",                // facultatif : le dépôt de la classe, « propriétaire/dépôt », marqué Template repository ; sans lui, pas de « Partir de cette classe »
      "verifie": { "attendus": "120/120", "pdf": 140, "pagination": true, "le": "2027-09-20" },  // facultatif (absent pour la classe d'exemple, en cours d'écriture)
      "partagee_le": "2027-09-21"                         // facultatif
    }
  ]
}
```

(Exemple fictif ; les commentaires ne sont qu'explicatifs : le fichier est du JSON strict. Aujourd'hui la liste ne contient que la classe d'exemple, « Le tour du monde », avec `"depot": "encrine-ai/tour-du-monde"` ; sous sa carte, un message dit que les premières classes partagées apparaîtront ici.)

### Ajouter une classe

1. L'enseignant le demande dans sa classe : le skill `partager-ma-classe` vérifie que l'année couvre le programme, que les PDF sont fabriqués et paginés, que chaque image et chaque texte a une licence qui permet le partage, et qu'aucune donnée d'élève n'y figure ; il prépare l'enregistrement de `classes.json`.
2. Il ouvre une **demande de fusion sur ce dépôt**, qui n'ajoute que cet enregistrement.
3. Une personne la relit (le contenu de la classe, ses licences, son ton) et le propriétaire de ce dépôt la fusionne. La carte apparaît au déploiement suivant.

### Retirer une classe

L'auteur le demande, ou retire lui-même son dépôt : son enregistrement est enlevé de `classes.json` par une demande de fusion, sans discussion. « Signaler une classe » ouvre une issue sur ce dépôt.

## Licences

Marelle, Unbounded et Figtree sont sous SIL Open Font License 1.1 (`fonts/LICENCE-Marelle.txt`, `fonts/LICENCE-Unbounded.txt`, `fonts/LICENCE-Figtree.txt`). Unbounded et Figtree sont les fichiers de Google Fonts (sous-ensembles latin et latin étendu), copiés dans `fonts/`. Le nom « encrine » du logo est tracé depuis Marelle.
