# R12 — Identifiabilité active : moyenne collective et interactions par paires

**Statut :** démonstration mathématique élémentaire et calculs rationnels finis.  
**Nature :** modèle synthétique à trois variables ; **aucune validation physique ni revendication de nouveauté universelle**.  
**Date :** 19 octobre 2026.  
**Cadre exploratoire :** TTM / Tⁿ / comparaison de deux descriptions dynamiques.

## Définition des deux mécanismes

Pour (x=(a,b,c)inmathbb{Q}^3), posons (m=(a+b+c)/3).

- (H(x)=(m,m,m)), mise à jour collective simultanée de trois composantes ;
- (P(x)), composition des moyennes sur les paires ((a,b)), puis ((b,c)), puis ((a,c)).

La matrice de la transformation (P) est :

[
P =
\begin{pmatrix}
3/8 & 3/8 & 1/4\\
1/4 & 1/4 & 1/2\\
3/8 & 3/8 & 1/4
\end{pmatrix}.
]

Ces deux mécanismes utilisent les mêmes trois nœuds et possèdent la même *2-section* de graphe ; leurs opérations sont néanmoins différentes.

## Proposition 1 — Condition d'indiscernabilité passive

[
P(x)-H(x)=\frac{a+b-2c}{24}(1,-2,1).
]

Donc (P(x)=H(x)) **si et seulement si** (a+b=2c).

**Preuve.** Soustraire la matrice constante (H_{ij}=1/3) de la matrice de (P). Toutes les lignes de la différence sont proportionnelles au vecteur ((1,1,-2)). Le résidu est de rang 1 et le noyau est un plan de dimension 2. (square)

Avec (E(z)=z_1^2+z_2^2+z_3^2), on a aussi :

[
E(P(x))-E(H(x))=\frac{(a+b-2c)^2}{96}.
]

## Proposition 2 — Deux interventions suffisent dans ce modèle

Considérons (x_+=x+delta e_3) et (x_-=x-delta e_3), avec (delta
eq 0).

[
\max_{sigmain\{-1,+1\}}
\lVert P(x+sigmadelta e_3)-H(x+sigmadelta e_3)\rVert_\infty
\geq \frac{|\delta|}{6}.
]

**Preuve.** Écrivons (w=a+b-2c). Les deux interventions remplacent (w) par (w-2delta) et (w+2delta). Par l'inégalité triangulaire, (max(|w-2delta|,|w+2delta|)geq2|delta|). Le vecteur ((1,-2,1)/24) a une norme infinie égale à (1/12). La borne s'ensuit. Elle est atteinte pour (w=0). (square)

## Proposition 3 — Condition robuste pour un bruit borné

Supposons des états initiaux identiques et reproductibles, des prédictions (H,P) exactement connues, et un bruit additif sur les mesures de sortie tel que chaque vecteur d'erreur ait une norme (ell_\infty) au plus (arepsilon).

La séparation garantie des ensembles de mesures possibles des deux mécanismes par le protocole précédent est obtenue lorsque :

[
|\delta|>12\varepsilon.
]

Au seuil ( |\delta|=12\varepsilon ), choisir (w=0) produit des observations admissibles communes, construites comme le point milieu des deux prédictions. La borne est donc aiguë dans ce protocole et pour ce modèle de bruit.

## Calculs indépendants (nombres rationnels exacts)

Trois programmes séparés ont été exécutés dans des environnements indépendants, avec reçus de calcul :

- **Exploration de sondages :** 343 états initiaux, 4 amplitudes, 1 372 paires d'interventions contrôlées.
- **Contradiction / bruit :** 250 cas adversariaux classifiés à (delta=1/2), (arepsilon=1/32), et contre-exemple au seuil (arepsilon=1/24).
- **Vérification matricielle indépendante :** 125 états et reconstruction rationnelle de (P) ; 13 états passivement indiscernables sur cette grille.

Ces décomptes sont des tests sur un ensemble **fini**, non une expérimentation scientifique externe.

## Limites et prochaines questions

Les conclusions reposent sur une paire de mécanismes spécifiés, sur une intervention reproductible, sur l'exactitude des calculs et sur la forme du bruit. Elles ne s'appliquent pas automatiquement aux champs fractals, mycéliens, tensoriels, aux données naturelles, ni à des mécanismes inconnus.

Questions ouvertes : quels journaux d'événements permettent de distinguer les 13 cas passivement ambigus ? La méthode reste-t-elle identifiable avec bruit sur les entrées, paramètres inconnus, interventions imparfaites, ou davantage de mécanismes candidats ?

**Publication de preuve mathématique, pas déploiement logiciel, validation de théorie physique ni certification d'une découverte originale.**
