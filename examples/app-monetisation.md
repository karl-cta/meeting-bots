# Exemple: créer une appli, pas en TS, monétisable

**Invocation:**

```
/meeting-bots:meeting "Je veux créer une appli qui aide les freelances à tracker leurs revenus, je veux un plan, pas en typescript, et je veux la monétiser"
```

**Team auto-détectée:** `dev`

---

## Chair

Team dev convoquée: dev-boss, dev-pusher, dev-rookie, dev-watcher, dev-cynic. Ça te va ? (oui)

Sujet: app pour freelances qui tracke leurs revenus, pas en TypeScript, monétisable. Je lance.

---

## Round 1, ouvertures

**dev-boss**

Avant le plan, 2 questions de cadrage. "Freelances" c'est qui exactement, solo ou micro-agence, quel pays, quelle complexité fiscale ? Ça change tout. Ensuite, pas de TS, OK, mais dis-moi pourquoi. Si c'est pour aller vite, Python/FastAPI + HTMX ou Go + Templ te donneront un MVP solide. Si c'est pour bootstraper sans deps, Ruby on Rails reste le plus rapide pour un dev solo sur du CRUD avec facturation. Monétisation: SaaS récurrent 9-19€/mois, pas de freemium au début. Tu veux du feedback payant, pas du lurker gratuit.

**dev-pusher**

Go. Backend en Go + sqlite, zero config, binaire unique, tu déploies sur un VPS à 5€/mois et t'as plus jamais à y toucher. Frontend HTMX ou Alpine.js, pas de build step, pas de framework, pas de prise de tête. Tu itères vite, tu peux refactor en 2 jours quand t'as plus de clients. Pour la monét, direct Stripe Checkout, Paddle si tu veux pas gérer la TVA européenne. Ship en 3 semaines, pas 3 mois.

**dev-rookie**

Attends. Quand tu dis "tracker les revenus", ça veut dire quoi concrètement ? Juste lister les factures et les totaux ? Ou connecter le compte bancaire, classer les transactions, générer des rapports fiscaux ? Les deux mondes ont zero rapport niveau complexité. Et "monétiser" à quel stade ? Tu veux vendre ce truc à 100 freelances ou à 10k ? Combien t'as déjà interviewé de freelances pour savoir ce qu'il leur manque réellement par rapport à ce que fait Abby ou Indy ?

**dev-watcher**

Le marché des outils pour freelances français est blindé. Indy, Abby, Freebe, Henrri, Tiime. Ils ont des équipes, du SEO, des intégrations URSSAF. Ton MVP, c'est quoi la différence qui fait qu'un freelance quitte son outil actuel ? Deuxième scénario: data sensible. Si tu stockes des revenus ou pire, connectes une banque, tu touches DSP2, RGPD, chiffrement au repos, authentification forte. Ton VPS à 5€ avec SQLite en clair, c'est la première plainte CNIL quand t'as un client qui gueule.

**dev-cynic**

Alors on fait un concurrent à Indy, en Go, sans framework, tout seul, monétisable en 3 semaines. Je vais chercher les popcorns. Plus sérieusement: la vraie question c'est pas le langage, c'est "pourquoi toi, pourquoi maintenant". Si t'as pas une réponse qui tient en une phrase à ça, le stack on s'en fout, tu vas ramer.

---

## Round 2, rebuttals

**dev-boss**

Rookie et Watcher ont posé les bonnes questions. Cynic aussi. Avant tout le reste: Karl, quelle est ta traction actuelle ? T'as parlé à combien de freelances ? T'as une liste d'attente ? Si la réponse est zéro, le plan n'est pas technique, il est commercial. Un plan qui commence par du code pour un marché déjà saturé, c'est un projet perso déguisé en business. Pusher, ton plan tech est bon pour un MVP, pas pour un produit qu'on veut vendre à 10k personnes. Pour un premier test, il est parfait.

**dev-pusher**

Watcher a raison sur le marché saturé, mais c'est aussi pour ça que tu peux gagner: tout le monde fait la même chose. Une niche précise (freelances tech expat, freelances créatifs payés en USD, consultants qui facturent à la journée) mal servie, et tu prends ce segment. Sur la partie data sensible, d'accord, je retire le "pas de framework". Si tu touches banque, faut du sérieux, et un framework mature te couvre sur les basics.

**dev-rookie**

Ce qui me rassure pas c'est qu'on parle plan technique avant d'avoir cadré qui paie et pourquoi. Karl, t'as déjà montré une maquette à 5 freelances ? Qu'est-ce qu'ils ont dit ? Et niveau "pas de TypeScript", c'est un vrai critère produit ou c'est une préférence perso ? Si c'est la préférence, on la note, si c'est un critère produit, je comprends pas.

**dev-watcher**

Pusher concède la partie sensible, bien. Boss a raison, la question est commerciale. Ajoutons un angle: même avec une niche, l'acquisition est coûteuse. SEO demande du contenu, ads c'est 20-50€ le lead sur le segment freelance en France. Si tu vends à 15€/mois, il te faut 5-6 mois de rétention juste pour être à l'équilibre sur un lead. Un plan qui n'inclut pas l'acquisition, c'est la moitié du plan.

**dev-cynic**

Résumé: on a un dev solo qui veut concurrencer Indy, sans y avoir mis 1 heure de discovery, qui choisit son stack sur une préférence personnelle, et qui veut qu'on "monétise" avant d'avoir un utilisateur. C'est pas un meeting, c'est un groupe de soutien. Karl, faut passer une semaine à parler à des freelances avant d'écrire une seule ligne. Sinon on se revoit dans 6 mois pour le post-mortem.

---

## Round 3, closing statements

### dev-boss

Ma position avant que j'écrive la synthèse : la discovery avant le code est l'étape non négociable. Les débats techno sont intéressants mais secondaires tant qu'on n'a pas validé un pain répété et un payeur identifié. Le marché est trop encombré pour partir sur un coup de tête technique.

### dev-pusher

Je concède : sans discovery, le stack Go + SQLite + HTMX reste un bon choix mais résout le mauvais problème. Nuance pour le plan : si Karl est lui-même freelance ultra frustré avec 3 idées précises, il a déjà fait sa discovery pour son propre cas. Ça change le calcul et on peut raccourcir à 2 semaines de code direct.

### dev-rookie

Je garde ma question centrale pour le Boss : "Qui paye concrètement, combien, et pourquoi eux ?". Les 3 points à vérifier en discovery doivent répondre à ça. Si après 10 interviews Karl n'a pas un profil précis de payeur, le plan ne tient pas, peu importe le stack.

### dev-watcher

Je recalibre : le single-provider risk et les détails d'infra ne sont pas prioritaires tant que le produit n'a pas de clients. Le vrai risque du mois 1 c'est de construire proprement un truc que personne ne veut. Chiffrement au repos oui dès le jour 1 (2 lignes de conf), multi-cloud non.

### dev-cynic

Concession : j'ai été dur. L'idée n'est pas mauvaise en soi, le problème c'est la séquence (coder avant de parler à 10 personnes). Si la discovery valide un pain répété, même moi je m'y mets. Sinon, on fait autre chose, c'est pas grave.

---

## Synthèse by dev-boss

**dev-boss (synthèse)**

Avant de coder quoi que ce soit, une semaine de discovery. Pas de contournement possible.

Pourquoi: le marché français des outils pour freelances est saturé (Indy, Abby, Freebe, Henrri, Tiime). Les concurrents ont des équipes, du SEO, des intégrations URSSAF. La question technique du stack est secondaire. La vraie question: quel freelance va quitter son outil actuel pour le tien, et pourquoi? Tant que la réponse n'est pas en une phrase concrète, le code ne résout rien.

Le plan:

Semaine 1, discovery. 10 interviews de 20 minutes avec des freelances, sur LinkedIn ou via ton réseau. Tu leur demandes comment ils trackent leurs revenus aujourd'hui, ce qui les fait râler, ce qu'ils payeraient pour résoudre le pain numéro 1. Zéro pitch produit, juste écouter et noter mot à mot.

Seuil de passage: si 3 personnes minimum décrivent le même vrai pain ET sont prêtes à être bêta-testeurs payants à 10 euros/mois, tu passes au MVP. Sinon, c'est pas le bon projet pour toi maintenant, pivote le sujet ou passe la main. C'est pas grave, c'est la meilleure économie que tu feras de l'année.

Semaines 2 à 4, MVP si validation OK. Stack: Go + SQLite + HTMX pour rester solo et véloce. Stripe Checkout pour la monétisation (Paddle si tu veux pas gérer la TVA européenne). VPS dédié, chiffrement au repos dès le jour 1 (2 lignes de conf, pas une option). Pas de connexion bancaire au MVP, saisie manuelle ou import CSV seulement. Déploiement visé: 2 à 3 semaines max de code.

Acquisition: canal organique uniquement au démarrage. Contenu technique sur blog ou LinkedIn, ciblé sur une niche précise (freelances tech expat, consultants payés en USD, une verticale spécifique). Les ads payantes à 20-50 euros le lead ne tiennent pas à 15 euros/mois de prix moyen, skip au début.

Questions ouvertes à trancher toi-même:

- "Pas en TypeScript" est une préférence perso ou un critère produit? Si c'est ta préférence, on note. Si c'est un critère, explique le pourquoi avant qu'on valide le stack définitivement.
- Quelle niche précise? "Tous les freelances français" = personne. Il faut un segment nommé et mesurable.
- Traction actuelle: 0, ou t'as déjà 5 personnes qui t'ont dit oui pour tester? La réponse change le plan.

Confiance: moyenne. Le plan tient si la discovery valide un pain répété, mais le marché est encombré et l'acquisition difficile à ton échelle. Ce qui la ferait monter à haute: tu es toi-même freelance ultra frustré par les outils existants avec 3 idées précises de différenciation. Ce qui la tuerait: 10 interviews en semaine 1 sans pain répété, ou Abby/Indy qui sortent la feature que tu comptais comme wedge dans les 3 prochains mois.

---

## Chair

Tu veux pousser un angle, contredire, ou c'est bon ? Réponds avec ton contre-argument pour relancer, ou "ok" pour clore.
