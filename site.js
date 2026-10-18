/* Encrine — le script commun aux pages du site. Aucun service extérieur :
 * il ne lit que les fichiers du site (classes.json).
 *
 * 1. L'en-tête, toujours visible : le filet et le resserrement, une fois la page descendue.
 * 2. Les adresses de la page, en un seul endroit (LIENS).
 * 3. Le panneau « Créer votre classe » / « Partir de cette classe », s'il est sur la page.
 * 4. La galerie des classes (classes.json), si la page en a une.
 */

/* Les adresses : le modèle de classe, la classe d’exemple (la démonstration
 * du modèle), et le dépôt de cette page (pour signaler une classe). */
var LIENS = {
  proprietaire: 'encrine-ai',
  modele: 'moteur',
  accueil: 'encrine-ai.github.io',
  exemple: 'https://encrine.ai/tour-du-monde/'
};
function gabarit(proprietaire, nom) { return 'https://github.com/new?template_owner=' + encodeURIComponent(proprietaire) + '&template_name=' + encodeURIComponent(nom); }
var MODELE = gabarit(LIENS.proprietaire, LIENS.modele);

/* 1. L'en-tête. Un témoin invisible, haut de ce qui s'efface de l'en-tête
 * (--entete-retrait), est posé en haut de la page : quand il sort de l'écran,
 * l'en-tête prend son filet et se resserre. Pas d'écoute du défilement. */
(function () {
  var entete = document.querySelector('.entete');
  if (!entete) return;
  var temoin = document.createElement('div');
  temoin.className = 'entete__temoin';
  temoin.setAttribute('aria-hidden', 'true');
  document.body.insertBefore(temoin, document.body.firstChild);
  function poser(descendu) { entete.classList.toggle('entete--descendu', descendu); }
  if ('IntersectionObserver' in window) {
    new IntersectionObserver(function (e) { poser(!e[e.length - 1].isIntersecting); }).observe(temoin);
  } else {
    var lire = function () { poser(window.pageYOffset > temoin.offsetHeight); };
    window.addEventListener('scroll', lire, { passive: true }); lire();
  }
})();

/* 1 bis. Le menu du téléphone et de la tablette : sous 1100 px, les sections
 * quittent l'en-tête (styles.css). Le bouton « Menu » ouvre un <dialog> modal
 * (le focus y est retenu, Échap le ferme) qui reprend le sommaire de l'accueil,
 * dans ses couleurs, « Créer ma classe » et GitHub. Sur les autres pages, les
 * liens mènent aux sections de l'accueil (../#…). La liste suit le sommaire
 * de index.html : une section ajoutée là s'ajoute ici. */
var SECTIONS = [
  ['comment', 'Comment ça marche', 'bleu'],
  ['recu', 'Ce que vous recevez', 'rose'],
  ['boucle', 'Vos retours', 'vert'],
  ['classes', 'Les classes', 'ocre'],
  ['capot', 'Sous le capot', 'violet'],
  ['controles', 'Les contrôles', 'turquoise'],
  ['aujourdhui', 'Ce qui est prêt', 'rouge']
];
(function () {
  var nav = document.querySelector('.entete .nav');
  var marque = document.querySelector('.entete .marque');
  if (!nav || !marque || typeof HTMLDialogElement !== 'function') return;
  var surAccueil = marque.getAttribute('href') === '#';
  var accueil = surAccueil ? '' : marque.getAttribute('href');
  var github = nav.querySelector('.nav__github');

  var bouton = document.createElement('button');
  bouton.type = 'button'; bouton.className = 'nav__menu';
  bouton.setAttribute('aria-expanded', 'false'); bouton.setAttribute('aria-controls', 'menu'); bouton.setAttribute('aria-haspopup', 'dialog');
  bouton.innerHTML = '<span class="nav__cases" aria-hidden="true"><i></i><i></i><i></i></span><span>Menu</span>';
  nav.insertBefore(bouton, github);

  var dlg = document.createElement('dialog');
  dlg.className = 'menu'; dlg.id = 'menu'; dlg.setAttribute('aria-labelledby', 'menu-titre');
  var html = '<div class="menu__tete"><p class="menu__titre" id="menu-titre">' + (surAccueil ? 'Sur cette page' : 'Sur l’accueil') + '</p>' +
    '<button class="partir__fermer" type="button" data-fermer aria-label="Fermer le menu">×</button></div><nav aria-label="Menu"><ol class="menu__liste">';
  SECTIONS.forEach(function (s) {
    html += '<li><a href="' + accueil + '#' + s[0] + '"><span class="sommaire__case" style="background:var(--case-' + s[2] + ')" aria-hidden="true"></span>' + s[1] + '</a></li>';
  });
  html += '</ol></nav><div class="menu__actions">' +
    (surAccueil ? '<button class="bouton bouton--principal" type="button" data-menu-creer>Créer ma classe</button>'
                : '<a class="bouton bouton--principal" href="' + accueil + '#creer">Créer ma classe</a>') +
    '<a class="nav__github" href="' + (github ? github.getAttribute('href') : 'https://github.com/encrine-ai') + '">' + (github ? github.querySelector('svg').outerHTML : '') + '<span>GitHub</span></a></div>';
  dlg.innerHTML = html;
  document.body.appendChild(dlg);

  function rendre() { document.documentElement.classList.remove('menu-ouvert'); bouton.setAttribute('aria-expanded', 'false'); }
  function fermer() { if (dlg.open) dlg.close(); rendre(); }
  bouton.addEventListener('click', function () {
    dlg.showModal();
    document.documentElement.classList.add('menu-ouvert');
    bouton.setAttribute('aria-expanded', 'true');
  });
  dlg.addEventListener('close', function () { rendre(); bouton.focus(); });
  dlg.addEventListener('click', function (e) {
    var r = dlg.getBoundingClientRect();
    var dehors = e.target === dlg && (e.clientX < r.left || e.clientX > r.right || e.clientY < r.top || e.clientY > r.bottom);
    if (dehors || e.target.closest('[data-fermer]') || e.target.closest('a')) fermer();
    if (e.target.closest('[data-menu-creer]')) {
      fermer();
      if (window.panneau) window.panneau.ouvrir('creer', bouton); else location.href = MODELE;
    }
  });
  /* Revenu à la largeur d'un ordinateur, le menu n'a plus lieu d'être ouvert. */
  if (window.matchMedia) {
    var large = window.matchMedia('(min-width: 1101px)');
    var suivre = function () { if (large.matches) fermer(); };
    if (large.addEventListener) large.addEventListener('change', suivre);
  }
})();

document.querySelectorAll('[data-lien="modele"]').forEach(function (a) { a.href = MODELE; });
document.querySelectorAll('[data-lien="exemple"]').forEach(function (a) { a.href = LIENS.exemple; });
document.querySelectorAll('[data-lien="signaler"]').forEach(function (a) {
  a.href = 'https://github.com/' + LIENS.proprietaire + '/' + LIENS.accueil + '/issues/new?title=' + encodeURIComponent('Signaler une classe');
});

/* 3. Le panneau : un seul <dialog>, rempli selon le bouton qui l’ouvre. « Créer
 * ma classe » l’ouvre pour le modèle (partir de zéro), « Partir de cette
 * classe » pour la classe de la carte, elle-même un modèle GitHub. Sans
 * JavaScript, « Créer ma classe » garde son lien direct vers le modèle. */
var panneau = (function () {
  var dlg = document.getElementById('partir');
  if (!dlg) return null;
  var titre = document.getElementById('partir-titre');
  var lien = document.getElementById('partir-lien');
  var origine = document.getElementById('partir-origine');
  var commande = document.getElementById('partir-commande');
  var copier = document.getElementById('partir-copier');
  var ouvreur = null;

  function ouvrir(mode, bouton, c) {
    ouvreur = bouton;
    dlg.querySelectorAll('[data-pour]').forEach(function (el) { el.hidden = el.getAttribute('data-pour') !== mode; });
    if (mode === 'classe') {
      titre.textContent = 'Partir de « ' + c.titre + ' »';
      origine.textContent = '« ' + c.titre + ' »';
      lien.href = gabarit(c.depot.proprietaire, c.depot.nom);
    } else {
      titre.textContent = 'Créer votre classe';
      lien.href = MODELE;
    }
    commande.textContent = '/nouvelle-classe';
    copier.textContent = 'Copier';
    if (typeof dlg.showModal === 'function') dlg.showModal(); else dlg.setAttribute('open', '');
  }
  function fermer() {
    if (!dlg.open) return;
    if (dlg.close) dlg.close(); else { dlg.removeAttribute('open'); if (ouvreur) ouvreur.focus(); }
  }
  dlg.addEventListener('close', function () { if (ouvreur) ouvreur.focus(); });
  dlg.addEventListener('click', function (e) { if (e.target === dlg || e.target.closest('[data-fermer]')) fermer(); });
  dlg.addEventListener('keydown', function (e) { if (e.key === 'Escape' && !dlg.close) fermer(); });
  function selectionner() { var r = document.createRange(); r.selectNodeContents(commande); var sel = window.getSelection(); sel.removeAllRanges(); sel.addRange(r); }
  copier.addEventListener('click', function () {
    var fini = function () { copier.textContent = 'Copié'; setTimeout(function () { copier.textContent = 'Copier'; }, 1800); };
    try { navigator.clipboard.writeText(commande.textContent).then(fini, selectionner); } catch (e) { selectionner(); }
  });

  /* « Créer ma classe » : le panneau ; un clic avec Ctrl, Cmd ou Maj garde le lien direct. */
  document.querySelectorAll('[data-panneau="creer"]').forEach(function (a) {
    a.setAttribute('aria-haspopup', 'dialog'); a.setAttribute('aria-controls', 'partir');
    a.addEventListener('click', function (e) {
      if (e.ctrlKey || e.metaKey || e.shiftKey || e.altKey || e.button !== 0) return;
      e.preventDefault(); ouvrir('creer', a);
    });
  });
  /* Les autres pages (contact, mentions légales…) mènent ici par « #creer ». */
  if (location.hash === '#creer') {
    var premier = document.querySelector('[data-panneau="creer"]');
    if (history.replaceState) history.replaceState(null, '', location.pathname + location.search);
    if (premier) ouvrir('creer', premier);
  }
  return { ouvrir: ouvrir };
})();

/* 4. La galerie : classes.json (l’adresse est dans data-source). La classe
 * d’exemple d’abord (exemple: true), puis les classes partagées. Chaque carte
 * prend les couleurs de son thème. « Partir de cette classe » n’apparaît que si
 * la fiche donne son dépôt (`depot`) et une licence qui permet la reprise
 * (CC BY ou CC BY-SA). data-limite ne montre que les premières cartes (la page
 * Design system n’en montre qu’une). */
(function () {
  var liste = document.getElementById('liste-classes');
  if (!liste) return;
  var source = liste.getAttribute('data-source') || 'classes.json';
  var limite = parseInt(liste.getAttribute('data-limite'), 10) || 0;

  function texte(balise, classe, contenu) {
    var el = document.createElement(balise);
    if (classe) el.className = classe;
    if (contenu != null) el.textContent = contenu;
    return el;
  }
  function date(iso) {
    try { return new Intl.DateTimeFormat('fr-FR', { day: 'numeric', month: 'long', year: 'numeric', timeZone: 'UTC' }).format(new Date(iso + 'T00:00:00Z')); }
    catch (e) { return iso; }
  }
  /* « propriétaire/dépôt », ou l’adresse https://github.com/propriétaire/dépôt. */
  function depot(d) {
    if (typeof d !== 'string') return null;
    var m = d.trim().replace(/^https?:\/\/github\.com\//i, '').replace(/\/+$/, '').replace(/\.git$/, '').match(/^([A-Za-z0-9-]+)\/([A-Za-z0-9._-]+)$/);
    return m ? { proprietaire: m[1], nom: m[2] } : null;
  }
  /* CC BY ou CC BY-SA : ni NC, ni ND. */
  function reprenable(licence) { return /^CC BY(-SA)?(\s|$)/i.test(licence || ''); }

  function carte(c) {
    var art = texte('article', 'classe' + (c.exemple ? ' classe--exemple' : ''));
    var frise = texte('div', 'frise'); frise.setAttribute('aria-hidden', 'true');
    var legende = texte('div', 'frise-legende'); legende.setAttribute('aria-hidden', 'true');
    c.milieux.forEach(function (m) {
      var b = document.createElement('span'); b.style.flex = m.semaines; b.style.background = m.couleur; frise.appendChild(b);
      var l = texte('span', null, m.nom); l.style.flex = m.semaines; legende.appendChild(l);
    });
    art.appendChild(frise); art.appendChild(legende);
    if (c.exemple) art.appendChild(texte('p', 'classe__badge', 'Classe d’exemple'));
    art.appendChild(texte('h3', 'classe__titre', c.titre));
    art.appendChild(texte('p', 'classe__sous', c.niveau + ' · ' + c.annee + ' · zone ' + c.zone));
    if (c.accroche) art.appendChild(texte('p', 'classe__accroche', c.accroche));
    art.appendChild(texte('p', 'cache', 'Les périodes : ' + c.milieux.map(function (m) { return m.nom; }).join(', ') + '.'));
    if (c.verifie) {
      var faits = texte('ul', 'classe__faits');
      [c.verifie.attendus ? c.verifie.attendus + ' attendus du programme couverts' : null, c.verifie.pdf ? c.verifie.pdf + ' PDF' : null,
       c.verifie.pagination ? 'une page par fiche, vérifiée' : null].forEach(function (f) { if (f) faits.appendChild(texte('li', null, f)); });
      if (faits.children.length) art.appendChild(faits);
    }
    var meta = 'Par ' + c.auteur + ' · licence ' + c.licence + (c.licence_note ? ' (' + c.licence_note + ')' : '');
    if (c.partagee_le) meta += ' · partagée le ' + date(c.partagee_le);
    art.appendChild(texte('p', 'classe__meta', meta));
    var actions = texte('div', 'boutons classe__actions');
    var voir = texte('a', 'bouton bouton--principal bouton--petit', 'Voir la classe'); voir.href = c.site; actions.appendChild(voir);
    var d = depot(c.depot);
    if (d && reprenable(c.licence) && panneau) {
      var partir = texte('button', 'bouton bouton--petit', 'Partir de cette classe'); partir.type = 'button';
      partir.setAttribute('aria-haspopup', 'dialog'); partir.setAttribute('aria-controls', 'partir');
      partir.addEventListener('click', function () { panneau.ouvrir('classe', partir, { titre: c.titre, depot: d }); });
      actions.appendChild(partir);
    }
    art.appendChild(actions);
    return art;
  }

  fetch(source).then(function (r) { if (!r.ok) throw new Error(r.status); return r.json(); }).then(function (d) {
    liste.textContent = '';
    var classes = d.classes.slice().sort(function (a, b) { return (b.exemple ? 1 : 0) - (a.exemple ? 1 : 0); });
    if (limite) classes = classes.slice(0, limite);
    classes.forEach(function (c) { liste.appendChild(carte(c)); });
    if (!limite && !classes.some(function (c) { return !c.exemple; })) {
      liste.appendChild(texte('p', 'classes__attente', 'Les premières classes partagées apparaîtront ici. Une fois votre classe prête, l’outil vous propose de la partager : rien n’est mis en ligne sans votre accord.'));
    }
  }).catch(function () {
    liste.textContent = '';
    var p = texte('p', 'classes__attente', 'La liste des classes ne s’est pas chargée. ');
    var a = texte('a', null, 'Voir une classe d’exemple'); a.href = LIENS.exemple; p.appendChild(a);
    liste.appendChild(p);
  });
})();
