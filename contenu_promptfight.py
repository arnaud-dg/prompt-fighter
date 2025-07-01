#############################################################################
#############################      Partie 1     #############################
#############################################################################

Theorie_1 = """
## 1. Concepts clés

### ✅ Qu'est-ce qu'un bon prompt ?  
Un bon prompt est :
- **Clair** : sans ambiguïté  
- **Contextualisé** : il donne un cadre ou une situation  
- **Spécifique** : il précise ce qu'on attend (forme, ton, longueur)

### 🚫 Prompt vague vs ✅ Prompt clair  

| Type | Exemple de prompt | Pourquoi ? |
|------|-------------------|------------|
| ❌ Vague | *Parle-moi de la fièvre* | Trop large, pas de cible ni de contexte |
| ✅ Clair | *Explique les causes possibles de la fièvre chez l'enfant, en moins de 5 phrases, pour un parent sans connaissances médicales* | Ciblé, clair, orienté utilisateur |

---

## 2. Variantes d'une même requête

### Prompt initial :  
> *Quelle est l'influence de la température sur la santé ?*

### Variantes améliorées :  
-  *Explique comment les fortes chaleurs peuvent aggraver certaines pathologies respiratoires chez les personnes âgées.*  
-  *Rédige un paragraphe décrivant les effets de la température sur la santé cardiovasculaire, en t'appuyant sur des faits scientifiques.*  
-  *Rédige un message de prévention à destination du grand public pour les canicules estivales.*

---

## 3. La méthode TCREI : *Tous Ces Robots Ecrivent Incroyablement*

La méthode **TCREI** est un acronyme qui vous guide pour structurer vos prompts de manière efficace :

### 📋 **T - Tâche** 
Définissez ce dont vous avez besoin clairement.
- **Exemple :** "Écris un email professionnel de relance"
- **Conseil :** Soyez spécifique sur l'action attendue

### 🎭 **C - Contexte**
Ajoutez des informations de fond pour de meilleurs résultats.
- **Exemple :** "Pour un client qui n'a pas répondu depuis 2 semaines à notre proposition commerciale"
- **Conseil :** Donnez les détails pertinents pour la situation

### 🎯 **R - Référence**
Partagez des exemples ou des modèles.
- **Exemple :** "Utilise un ton similaire à cet email : [exemple]"
- **Conseil :** Montrez plutôt que d'expliquer quand c'est possible

### 🔧 **E - Évaluation**
Expliquez comment vous évaluerez le résultat.
- **Exemple :** "Le ton doit être engageant mais pas trop formel"
- **Conseil :** Précisez vos critères de qualité

### 🎨 **I - Itération**
Pensez à créer des vraies conversations avec l'IA !
- **Exemple :** "Rends-le plus fun et avec des emojis 🎉"
- **Conseil :** N'hésitez pas à demander des ajustements

---

### 💡 **Exemple complet TCREI :**

```
**Tâche :** Écris un post LinkedIn engageant
**Contexte :** Pour promouvoir notre nouveau produit SaaS de gestion de projet, ciblant les startups
**Référence :** Inspire-toi du style de posts viraux avec des listes à puces
**Évaluation :** Le post doit être informatif mais pas trop promotionnel
**Itération :** Ajoute des emojis et une question pour engager l'audience

"""

Enonce_1 = """
## Exercice pratique

**Contexte :**  
Nous allons utiliser une IA pour produire un message de prévention à diffuser dans une salle d'attente d'un cabinet médical en période de canicule.

**Énoncé :**  
➤ Rédiger un prompt volontairement vague sur le sujet.  
➤ Reformuler ce prompt en effectuant des variations de contexte (rôle, auditoire cible, contrainte) afin de message plus impactant.  
➤ Comparez les résultats générés. 
> Ex : 
> - médecin généraliste
> - infirmier en pédiatrie
> - pour un enfant de 10 ans  
> - pour une personne ne parlant pas bien français
> - ... etc
"""

#############################################################################
#############################      Partie 2     #############################
#############################################################################

Theorie_2 = """
## 1. Les formats de sortie : structurer pour mieux communiquer

### 🎯 Pourquoi spécifier un format ?
L'IA peut produire différents types de contenus selon vos besoins :
- **Tableau** : pour comparer des éléments
- **Liste à puces** : pour énumérer des points
- **Email** : pour une communication professionnelle
- **Script** : pour une présentation orale
- **Fiche synthèse** : pour résumer l'essentiel

### Exemples de formats courants

| Format | Utilisation | Exemple de demande |
|--------|-------------|-------------------|
| 📋 **Checklist** | Actions à suivre | *"Présente sous forme de checklist étape par étape"* |
| 📊 **Tableau** | Comparaison | *"Organise en tableau avec colonnes : Avantages/Inconvénients/Prix"* |
| ✉️ **Email** | Communication pro | *"Rédige un email formel avec objet, introduction, corps, conclusion"* |
| 🎤 **Script** | Présentation | *"Écris un script de 3 minutes avec accroches et transitions"* |
| 📄 **Fiche synthèse** | Résumé exécutif | *"Résume en 5 points clés avec actions concrètes à la fin"* |

---

## 2. La structure adaptée pour spécifier les formats

**"Présente [CONTENU] sous forme de [FORMAT] avec [CONTRAINTES SPÉCIFIQUES]"**

### Exemples de contraintes spécifiques :
- **Longueur** : "en 200 mots maximum"
- **Structure** : "avec introduction, 3 parties, conclusion"
- **Ton** : "professionnel mais accessible"
- **Éléments** : "avec emojis et appels à l'action"

---

## 3. Formats avancés pour le monde professionnel

### 📈 **Rapport exécutif**
```
Structure : Résumé exécutif + Contexte + Recommandations + Plan d'action
Longueur : 1 page maximum
Ton : Factuel et orienté décision
```

### 💼 **Proposition commerciale**
```
Structure : Problème + Solution + Bénéfices + Tarifs + Prochaines étapes
Format : Email ou document PDF
Ton : Persuasif mais professionnel
```

### 🎯 **Plan de formation**
```
Structure : Objectifs + Programme + Méthodes + Évaluation
Format : Tableau avec timing
Ton : Pédagogique et clair
```

---

## 4. Conseils pour optimiser vos formats

### ✅ Bonnes pratiques :
- **Soyez précis** sur la structure attendue
- **Indiquez la longueur** souhaitée
- **Mentionnez le canal** de diffusion (email, présentation, affichage)

### ❌ Erreurs à éviter :
- Demander plusieurs formats à la fois
- Ne pas indiquer le niveau de formalité
- Mélanger contenu et format dans la même phrase

"""

Enonce_2 = """
## Exercice pratique : Construction d'un plan de développement

**Contexte :**  
Vous êtes responsables d'équipes sur un site fabriquant de produits pharmaceutiques.
Vous recherchez des formations existantes en Data et IA pour vos équipes afin de compléter leur montée en compétences.

**Énoncé :**  
➤ **Étape 1 :** Commencez par un prompt basique sans aucune spécification de format : *Donne moi 10 recommandations de formations en Data / IA*  
➤ **Étape 2 :** Optimisez ce prompt en utilisant le framework TCREI ET en spécifiant un format de sortie adapté :

> Ex :
> **Format 1 - Tableau avec des propositions justifiées/éclairées**  
> *Pour vous aider à la prise de décision*  
> → Structure : Propositions + Propriétés (durée, complexité) + Avantages/Inconvénients

> **Format 2 - Email synthétique à l'attention des RH**  
> *Pour expliciter vos idées*  
> → Structure : texte littéral avec intitulé, objectif pédagogique et retour sur investissement. 

**➤ Étape 3 :** Comparez la qualité et l'adaptation de chaque format au contexte d'usage
"""

#############################################################################
#############################      Partie 3     #############################
#############################################################################

Theorie_3 = """
## 1. Le Few-Shot Prompting : apprendre par l'exemple

### 🎯 Qu'est-ce que le Few-Shot Prompting ?
Le **Few-Shot Prompting** consiste à donner des exemples concrets à l'IA pour qu'elle comprenne exactement le style, le format et le ton attendus.

**Principe :** *"Montrer plutôt que d'expliquer"*

### 📚 Les différents types

| Type | Nombre d'exemples | Usage |
|------|-------------------|-------|
| 🎯 **Zero-Shot** | 0 exemple | Instructions directes |
| 🎯 **One-Shot** | 1 exemple | Format simple à reproduire |
| 🎯 **Few-Shot** | 2-5 exemples | Styles complexes, nuances |

---

## 2. Quand utiliser le Few-Shot ?

### ✅ **Cas d'usage recommandés :**
- **Style spécifique** : ton, vocabulaire, structure particulière
- **Format complexe** : templates avec plusieurs variables
- **Nuances subtiles** : ironie, humour, registre de langue
- **Cohérence** : série de contenus avec le même style
- **Domaines techniques** : jargon professionnel spécifique

### ❌ **Quand ce n'est PAS nécessaire :**
- Demandes simples et directes
- Formats standards (email classique, liste simple)
- Contenus factuels sans style particulier

---

## 3. Structure d'un prompt Few-Shot efficace

### 🏗️ **Template type :**
```
[INSTRUCTION GÉNÉRALE]

Exemples :

Exemple 1 :
Input: [données d'entrée]
Output: [résultat attendu]

Exemple 2 :
Input: [données d'entrée]
Output: [résultat attendu]

Maintenant, applique le même style à :
Input: [votre cas]
Output:
```

---

## 4. Bonnes pratiques du Few-Shot

### ✅ **À faire :**
- **2-3 exemples** suffisent généralement
- **Variez les exemples** pour montrer la flexibilité
- **Restez cohérent** dans le style entre exemples
- **Soyez précis** dans vos instructions d'accompagnement

### ❌ **À éviter :**
- Trop d'exemples (plus de 5) → confusion
- Exemples contradictoires entre eux
- Exemples trop similaires → manque de nuance
- Oublier l'instruction générale

---

## 5. Exemple concret : Newsletter entreprise

### Sans Few-Shot (vague) :
*"Écris une newsletter pour notre entreprise"*

### Avec Few-Shot (précis) :
```
Écris une newsletter dans le style décontracté de notre startup tech.

Exemples :

Sujet 1: Nouvelle fonctionnalité
Output: 🚀 On a une surprise pour vous ! Notre nouvelle fonction "Smart Sync" 
débarque demain. Finies les galères de synchronisation ! 
Plus d'infos → [lien]

Sujet 2: Événement équipe  
Output: 🎉 L'équipe part en team building vendredi ! Au programme : 
escape game et barbecue. On vous montrera nos talents cachés 😄
Suivez nos aventures sur Insta !

Maintenant, écris pour le sujet : Recrutement d'un nouveau développeur. 
"""

Enonce_3 = """
## Exercice pratique : Few-Shot en action

**Contexte :**  
Votre startup "TechFlow" a un style de communication très particulier sur les réseaux sociaux : décontracté, avec des emojis, des références pop culture, et toujours une pointe d'humour. Vous devez créer des posts cohérents avec cette identité.

**Énoncé :**  
➤ **Étape 1 :** Commencez par un prompt classique sans exemple  
➤ **Étape 2 :** Créez un prompt Few-Shot avec 2-3 exemples de posts dans le style "TechFlow"  
➤ **Étape 3 :** Testez votre prompt Few-Shot sur différents sujets  

**🎯 Exemples à inclure dans votre Few-Shot :**

> **Sujet 1 :** Lancement nouvelle feature  
> **Style TechFlow :** *"Plot twist ! 🎬 Notre nouvelle fonction 'AutoMagic' débarque demain et elle va révolutionner votre workflow comme Thanos a révolutionné l'univers Marvel (mais en mieux, promis) ✨ #TechLife #Innovation"*

> **Sujet 2 :** Bug résolu  
> **Style TechFlow :** *"Bug de ce matin = officiellement éliminé ! 🐛💥 Notre équipe de ninjas-développeurs a frappé plus vite que l'éclair ⚡ Merci pour votre patience, vous êtes les meilleurs ! ❤️ #TeamWork #FixItFast"*

**➤ Étape 4 :** Comparez la qualité et la cohérence stylistique entre les deux approches

**💡 Testez sur ces nouveaux sujets :**
- Recrutement d'un stagiaire
- Maintenance serveur prévue
- Partenariat avec une autre startup
"""