# Crypto_currency_app
it's a simple cryptocurrency notification python app using the "CoinAPI" API

Application de Notifications sur les Cryptomonnaies:

Objectif du projet:

L'objectif principal de ce projet est de développer une application permettant d'envoyer des notifications à l'utilisateur lorsqu'il y a des changements dans
le prix des cryptomonnaies qu'il suit. L'application utilise le langage Python et l'API CoinAPI.io pour récupérer les informations des cryptomonnaies en temps réel.

Approche et mise en œuvre:

1. Analyse des fonctionnalités de l'API:

Avant de modéliser les données et de définir l'architecture de l'application, je me suis intéressée aux informations que l'API CoinAPI.io permet de récupérer. 
Grâce à la documentation officielle, j'ai pu identifier l'endpoint approprié pour obtenir des informations détaillées sur une cryptomonnaie précise.

2. Conception de l'interface utilisateur

L'interface utilisateur a été pensée de manière à permettre à l'utilisateur de se connecter, de s'inscrire, de choisir une cryptomonnaie à suivre, 
de définir un seuil de notification, et de gérer ses alertes via un tableau de bord. Les principales actions de l'utilisateur incluent :

    L'ajout d'une cryptomonnaie avec un seuil à surveiller.
    L'affichage et la gestion des alertes.
    La déconnexion.

3. Algorithmique derrière l'application:

Une fois l'utilisateur inscrit et connecté, l'algorithme fonctionne de la manière suivante :

    Mise à jour régulière de la table des cryptomonnaies via l'API.
    Lorsque l'utilisateur ajoute une cryptomonnaie à suivre, celle-ci est enregistrée dans la table des alertes.
    Le prix de la cryptomonnaie est comparé au seuil défini par l'utilisateur. Si le prix dépasse ce seuil, une notification est envoyée.

Structure de la Base de Données:

Voici à quoi ressemble la base de données une fois toutes les fonctionnalités implémentées :

    Users (id, email, password)
    Cryptomonnaies (id, cryptomonnaie, prix)
    Alertes (id, id_crypto*, id_user*, seuil)
    Notifications (id, crypto_id*, id_user*, type_alerte) (Note : Le champ "seuil" dans la table Notifications n'est pas nécessaire, car il peut être récupéré 
            directement depuis la table Alertes)
    Derniere_notification (id, id_crypto*, dernier_statut, date)

Les astérisques (*) représentent des clés étrangères.

Points à Améliorer:

Bien que l'application soit fonctionnelle, plusieurs améliorations sont encore nécessaires :

    -Respect des principes SOLID : Je souhaite revoir la structure de mon code pour appliquer les principes SOLID. Cela implique notamment d'assurer que chaque
            classe ait une seule responsabilité et que l'application soit évolutive.
    -Relier les tables avec chaque utilisateur : Il est encore nécessaire de lier correctement les tables avec chaque compte utilisateur afin de garantir que 
            les alertes soient envoyées une fois que l'utilisateur est connecté.
    -Envoi des notifications : Actuellement, l'application n'envoie pas encore de notifications par email ou par message, mais cette fonctionnalité est en cours
             de développement.
    -le nom des fonctions et variables

Organisation du Code:

Le projet est organisé en quatre fichiers principaux :

    api.py : Contient les fonctions pour envoyer des requêtes à l'API CoinAPI.io et récupérer les données.
    database.py : Gère la base de données et toutes les opérations associées à chaque table.
    interface.py : Définit l'interface graphique avec laquelle l'utilisateur interagit. (note: j'ai crée un exemple pour pouvoir tester le login: email:louise@gmail.com / password: moi)
    classuseful.py : Contient des objets et des fonctions utilitaires qui sont utilisées dans différentes parties du code.

Execution: pour pouvoir tester , il faut executer le fichier interface.py 

Conclusion:

Bien que le code ne soit pas encore parfait, ce projet m'a permis d'apprendre énormément, tant sur la manipulation des APIs que sur la gestion des bases de données. 
En m'attaquant à des concepts avancés comme la gestion des alertes en temps réel et l'intégration de services externes, j'ai pu développer mes compétences en architecture logicielle et en résolution de problèmes complexes.

Ce travail a renforcé ma passion pour le développement informatique, me rappelant chaque jour à quel point ce domaine est fascinant et en constante évolution. 
La capacité de résoudre des défis techniques tout en créant des outils utiles et innovants est ce qui m'inspire profondément. Ce projet m'a également confirmé que c'est dans cette voie que je souhaite m'investir à long terme.

La technologie m'émerveille toujours plus et chaque étape de ce projet, aussi modeste soit-elle, nourrit mon désir d'apprendre et de progresser. 
Je suis déterminée à aller au bout de ce projet, à l'améliorer sans relâche et à le rendre pleinement fonctionnel, tout en continuant à explorer de nouvelles technologies et à affiner mes compétences pour être prête à relever les défis à venir.




 
