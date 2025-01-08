# Area Media Players

[![hacs_badge](https://img.shields.io/badge/HACS-Custom-orange.svg)](https://github.com/custom-components/hacs) 

## Description

L'intégration **Area Media Players** permet de gérer les lecteurs multimédias par zone dans Home Assistant. Vous pouvez exclure certains lecteurs de chaque zone et surveiller l'état des lecteurs dans chaque zone. De plus, vous pouvez allumer ou éteindre tous les lecteurs multimédias d'une zone à l'aide d'un switch.

## Installation

### Via HACS (Home Assistant Community Store) 

1. Ajoutez ce dépôt à HACS en tant que dépôt personnalisé.
2. Recherchez "Area Media Players" dans HACS et installez l'intégration.
3. Redémarrez Home Assistant.

### Manuel

1. Téléchargez les fichiers de ce dépôt.
2. Copiez le dossier `area_media_players` dans le répertoire `custom_components` de votre configuration Home Assistant.
3. Redémarrez Home Assistant.

## Configuration

### Via l'interface utilisateur

1. Allez dans `Configuration` > `Intégrations`.
2. Cliquez sur le bouton `+ Ajouter une intégration`.
3. Recherchez "Area Media Players" et suivez les instructions à l'écran pour configurer l'intégration.

### Via YAML

Non supporté.

## Utilisation

### Capteurs et Switches

L'intégration crée des capteurs et des switches pour chaque zone avec les attributs suivants :

- `count`: Nombre de lecteurs actifs.
- `total`: Nombre total de lecteurs.
- `count_of`: Nombre de lecteurs actifs sur le total.
- `players_active`: Liste des lecteurs actifs.
- `players_inactive`: Liste des lecteurs inactifs.
- `excluded_players`: Liste des lecteurs exclus.

### Exclusion de lecteurs

Vous pouvez exclure des lecteurs spécifiques de chaque zone via l'interface de configuration de l'intégration.

## Support

Pour toute question ou problème, veuillez utiliser le [suivi des problèmes](https://github.com//Nemesis24/area_media_players/issues).

## Contribuer

Les contributions sont les bienvenues ! Veuillez lire le fichier [CONTRIBUTING.md](https://github.com//Nemesis24/area_media_players/blob/main/CONTRIBUTING.md) pour plus d'informations.

## Licence

Ce projet est sous licence MIT. Voir le fichier [LICENSE](https://github.com//Nemesis24/area_media_players/blob/main/LICENSE) pour plus de détails.