# NoSQL_Kafka_project_AirQuality

## Introduction
Projet à réaliser dans le cadre du cours de NoSQL de l'ESILV IBO A5 (réalisé par Thomas HUBERT, Thibault CHASSEFAIRE et Wael MUHIEDDINE)

Ce projet contient 3 parties : 
* un docker-compose pour l'nevironnement Kafka 
* un producer python qui envoie des données sur la qualité de l'air à kafka
* un consumer python qui lit en temps réel les données envoyées par le producer

L'api que nous utilisons est une api qui récolte la qualité de l'air à travers toutes les stations du monde et les rend accessible via ses api (site initial : https://aqicn.org/api/fr/). Comme il faut s'inscrire pour obtenir l'accès à l'api, je laisse volontairement (mauvaise pratique mais cela fait gagner du temps aux évaluateurs) ma clé d'api générée avec un compte de test.

___
## I. Préparer le service kafka

Pour commencer, il faut vérifier que docker et docker-compose soient bien installés :
```
docker -v
> Docker version 20.10.2, build 2291f61 
docker-compose -v
> docker-compose version 1.27.4, build 40524192
```

Puis on vérifie la version de python :
```
python --version
> Python 3.9.0
```

Enfin, il faut installer la library kafka de python (en utilisant pip par exemple) :
```
pip install kafka
```

___
## II. Lancer le service Kafka

Les différents services seront lancés à l'aide du docker-compose.yml. Dans ce docker-compose, on lance : 
* un container zookeeper
* 3 containers de kafka broker
* un container Kafdrop (UI pour visionner les données des topics)

La plupart des options sélectionnées pour les containers sont inspirées de l'article suivant : https://rmoff.net/2018/08/02/kafka-listeners-explained/.
Il y a des volumes qui permettent la persistance des données. D'où le fait qu'ils se retrouvent dans le .gitignore.

### a. Lancement des services

Pour lancer le service, tant que l'on est dans le même dossier, il faut juste taper :
```
docker-compose up
```

Maintenant que les services sont lancés, on peut vérifier qu'ils tournent bien avec :
```
docker container ls
```

### b. Création des topics

On récupère alors le nom du container du broker kafka 1 pour lancer la commande suivante afin de créer le topic "air-station-topic" : 
```
docker exec -it nosql_kafka_project_airquality_kafka1_1 kafka-topics --zookeeper zookeeper:2181 --create --topic air-station-topic --partitions 1 --replication-factor 3
```

Enfin, pour vérifier que la commande est bien passée, lancez dans un moteur de recherche :
```
localhost:9000
```
Cela va ouvrir l'interface de Kafdrop avec en bas l'ensemble des topics. En cliquant sur "air-station-topic", puis "voir messages", le topic est vide.

___
## III. Lancement du producer

Pour lancer le producer, il faut rentrer la commande suivante dans une nouvelle console : 
```
python producer-air-quality.py
```
Vont s'afficher alors les logs, les stations qui sont envoyés aux brokers sur la fenêtre. Le while (True) permet de faire tourner l'appel d'api indéfiniment.

Sur kafdrop, on observe les messages arriver dans le topic "air-station-topic"
____
## IV. Lancement du consumer

Tout en laissant le producer tourner, lancez une nouvelle console et, toujours dans le même répertoire, utilisez la commande : 
```
python consumer-air-quality.py
```

S'affiche alors le nom des stations météorologique dont l'indice AQI dépasse les 50 (valeur arbitraire mais assez haute par rapport à la moyenne pour obtenir des résultats).

____

PS : il peut y avoir des problèmes avec la bibliothèque python Kafka, il faudrait alors installer kafka-python.
