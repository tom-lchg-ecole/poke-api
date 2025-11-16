# PokéAPI - Projet de Cours

> Projet éducatif de manipulation d'API REST avec Python

## Description

Ce projet est un exercice de cours visant à apprendre la manipulation d'API REST en Python, la gestion d'erreurs robuste, et la programmation asynchrone. Il utilise l'API publique [PokeAPI](https://pokeapi.co/) pour récupérer et analyser des données sur les Pokémon.

## Fonctionnalités

### Version Synchrone (`main.py`)
- Affichage des statistiques détaillées d'un Pokémon
- Comparaison de deux Pokémon (HP, Attaque)
- Analyse de type de Pokémon avec calcul de moyenne des HP
- Simulation de combat entre deux Pokémon

### Version Asynchrone (`q2_commune.py`)
- Gestion de charges élevées (100, 1000, 5000 requêtes simultanées)
- Comparaison de Pokémon en mode asynchrone
- Analyse de type avec requêtes parallèles
- Test de performance synchrone vs asynchrone

### Gestion API Robuste (`q1_commune.py`)
- Système de retry avec backoff exponentiel
- Gestion complète des codes d'erreur HTTP (400, 401, 403, 404, 429, 500, 503)
- Gestion des timeouts et erreurs de connexion
- Logging des tentatives de reconnexion

## Prérequis

- Python 3.7+
- pip

## Installation

1. Cloner le dépôt :
```bash
git clone <url-du-repo>
cd poke-api
```

2. Installer les dépendances :
```bash
pip install -r requirements.txt
```

## Utilisation

### Lancer l'application principale (mode synchrone)
```bash
python main.py
```

### Lancer l'application asynchrone
```bash
python q2_commune.py
```

### Tester la gestion d'erreurs
```bash
python q1_commune.py
```

## Structure du Projet

```
poke-api/
├── main.py              # Application principale avec menu interactif
├── q1_commune.py        # Gestion robuste des appels API
├── q2_commune.py        # Version asynchrone avec aiohttp
├── requirements.txt     # Dépendances Python
└── README.md           # Ce fichier
```

## Dépendances

- `requests` : Requêtes HTTP synchrones
- `aiohttp` : Requêtes HTTP asynchrones

## Exemples d'utilisation

### Afficher les statistiques d'un Pokémon
```
Entrez le nom ou l'ID du Pokémon: pikachu
```

### Comparer deux Pokémon
```
Entrez le nom ou l'ID du premier Pokémon: charizard
Entrez le nom ou l'ID du deuxième Pokémon: blastoise
```

### Analyser un type
```
Entrez le type de Pokémon (ex: fire, water, dragon): dragon
```

## Concepts Abordés

- Consommation d'API REST
- Gestion d'erreurs et retry logic
- Programmation asynchrone avec `asyncio` et `aiohttp`
- Optimisation de performance avec requêtes parallèles
- Manipulation de données JSON
- Interface utilisateur en ligne de commande

## Auteur

Projet réalisé dans le cadre d'un cours de programmation Python.

## Licence

Projet éducatif - Utilisation libre à des fins d'apprentissage.

## Ressources

- [Documentation PokeAPI](https://pokeapi.co/docs/v2)
- [Documentation requests](https://docs.python-requests.org/)
- [Documentation aiohttp](https://docs.aiohttp.org/)
