Description
============

Ce projet présente une API REST qui sert d'interface pour interroger une base de données PostGreSQL (ou autre...) ainsi que des services tiers.
Cette API est elle même consommée par un service dont le rôle est de créer une dashboard pour visualiser des données.

L'objectif de ce projet est didactique : monitoring, tests, métriques, documentation et bonnes pratiques sont disséminées partout. Au travers des README.md du projet, vous apprendrez des tips en Python mais aussi sur l'ensemble des Frameworks et librairies utilisées.

Prenez le temps de lire chaque README.md et de regarder chaque fichier pour comprendre comment l'ensemble des services interagissent entre eux.

## Par où commencer ?

Commençons par illustrer de manière simplifiée le projet :
[![Project docs](img/project-synthese-architecture.png)](https://github.com/christophe-deleuze/full-stack-fastapi-celery)

Ce que nous voyons ici, est une architecture découpée en deux partie : front / back. 
Front et back font références à des réseaux distincts.
Le réseau du front est accessible à des utilisateurs (couleur verte) tandis que le réseau du back ne l'est pas (couleur rouge).

Ainsi, la communication entre les services du back ne sont pas accessibles à un utilisateur externe, cela pour des raisons de sécurité évidente.

Une nouvelle fois, le schéma précédent peut encore êtres simplifié de la façon suivante :
[![Project docs](img/project-synthese-architecture-simplifiee.png)](https://github.com/christophe-deleuze/full-stack-fastapi-celery)

### Le backend

Le backend est composé d'une base de données PostgresSQL et de divers services qui ne sont pas accessible directement pour un utilisateur externe.

C'est donc l'API qui va avoir le rôle d'interroger les services du back et de mettre à disposition des utilisateurs externes, qui ont accès au front, les réponses retournées par les services du back.

On comprend intuitivement que le rôle de l'API, à cheval entre le front et le back va nécessairement impliquer des notions de sécurité et de scalabilité.

### Le frontend

Le front ,quant à lui, est composé d'un service (Dashboard) qui n'accède qu'au réseau frontal et dont le rôle est d'utiliser l'API pour générer une dashboard afin de visualiser des données.

L'utilisateur accède aussi bien au service dashboard qu'à l'API en elle-même. En général, l'API est consommée par d'autres services, tel que le projet dashboard tandis que l'utilisateur final lui ce contentera d'utiliser les services exploitant cette API.

A noter toutefois que l'API possède aussi une partie documentation qui sera elle, utilisée directement par les développeurs de services comme, par exemple, la dashboard.

## La question des besoins

Dans une architecture en microservices, chaque service vient avec ses propres besoins. 
Par exemple, la base de données nécessitera toujours de pouvoir être administrée. Dans notre cas, nous allons utiliser l'outil pgadmin.
Voici comment évolue notre schéma en ajoutant pgadmin :

[![Project docs](img/project-synthese-architecture-simplifiee-administree.png)](https://github.com/christophe-deleuze/full-stack-fastapi-celery)

De manière plus globale, un autre besoin important va se dégager pour l'ensemble des services, celui de pouvoir monitorer la santé des services.
Le monitoring est une interface visuelle dont le rôle est de nous permettre de rapidement savoir si tous les services fonctionnent correctement.

Implicitement, cela induit le fait que chaque service doit fournir des informations à l'interface visuelle du monitoring.

La solution retenue dans notre projet consiste à utiliser une base de données spécialisée dans la collecte de métriques (Prometheus) et son outil pour visualiser les métriques qu'elle à collecter (Grafana).
La collecte des métriques par Prometheus se fait à l'aide d'une requête HTTP l'endpoint /metrics. Ainsi, pour fournie des données à Prometheus, chaque service doit pouvoir répondre à une requête HTTP de type GET sur /metrics.

Pour l'API REST, rien de compliqué, il suffit d'ajouter un endpoint /metrics à celle-ci. Pour la base de donnée, comme elle ne sait pas nativement gérer des requêtes HTTP, il faudra faire appel à un service intermédiaire qui va collecter des métriques et les mettres à disposition de Prometheus. Ce type de service est appelé : Exporter.

Mettons à jour le schéma :
[![Project docs](img/project-synthese-architecture-simplifiee-administree-monitoree-partiellement.png)](https://github.com/christophe-deleuze/full-stack-fastapi-celery)

On remarque dans notre schéma, que je n'ai pas illustré l'exporter demétriques par les services tiers. Cela s'explique par le fait qu'ils ne sont pas forcément adaptés pour retourner des métriques.
Dans ce cas, on peut s'en tirer en distribuant les tâches aux services à l'aide d'intermédiaires (middlewares).


...


Schéma final du projet :
[![Project docs](img/project-synthese-architecture-archi-complet.png)](https://github.com/christophe-deleuze/full-stack-fastapi-celery)

## Vision par service

Ne nous attardons pas sur la complexité du schéma précédent. Gardons simplement une vision par services et de comment nous allons les manipuler :

[![Project docs](img/services-urls.png)](https://github.com/christophe-deleuze/full-stack-fastapi-celery)




## Retour sur la stack complète

La stack comprend :
 - Prometheus: Base de données de métriques. Elle collecte elle même les métriques de differents services ;
 - Grafana: Monitoring des métriques collectées par prometheus ;
 - Node-Exporter: Exporte des métriques de la machine pour Prometheus ;
 - PostgreSQL: Base de données relationnelle ;
 - postgres-exporter: Exporte des métriques de PostgreSQL vers Prometheus ;
 - pgAdmin: Administration de la base de données relationnelle ;
 - RabbitMQ: Broker pour les tâches Celery (RabbitMQ met à disposition nativement ses métriques pour Prometheus) ;
 - Redis: Result Backend utilisé pour stocker en mémoire les résultats de tâches Celery ;
 - redis-exporter: Exporte des métriques de Redis pour Prometheus ;
 - project-api (FastAPI): API REST entièrement asynchrone (IO bound) construite à l'aide du Framework FastAPI, l'export des métriques est assuré par l'api elle-même ;
 - project-worker (Celery): Projet contenant des tâches distribuées à l'aide du Framework Celery, très pratique pour une grande scalabilité ;
 - Flower: Monitoring des workers et tâches celery, ainsi qu'export de métriques pour Prometheus.

Ils ne sont pas encore intégrés :
 - Elasticsearch: Moteur d'indexation et d'analyse de données ;
 - Kibana: Outil basé sur Elasticsearch et qui sera utilisé pour visualiser et analyser des logs ;
 - Projet Dash: pour exploiter l'API Rest et créer de super dashboards en python.

Requirements
============

Vous avez besoin de [Docker](https://www.docker.com/products/docker-desktop) pour créer l'ensemble de l'environnement sur votre machine.
Une fois Docker exécuté, vérifier qu'il est bien lancé en mode Linux ! 

Quick Start
============

1. Lancer le projet :

```
git clone https://github.com/christophe-deleuze/full-stack-fastapi-celery.git
cd full-stack-fastapi-celery
docker-compose -p local-dev up -d
```

2. Jouer avec les urls :

- [API](http://127.0.0.1:5000/docs)
- [Flower - task monitoring](http://127.0.0.1:5555)
- [RabbitMQ - queues monitoring(guest/guest)](http://127.0.0.1:15672)
- [Prometheus - collect metrics](http://127.0.0.1:9090/)
- [PGAdmin - Postgresql Administration (postgres/postgres/postgres)](http://127.0.0.1:5050/)
- [Grafana - Services monitoring](http://127.0.0.1:3000/)

Additionnal Informations
============

1. Stopper l'environnement :

```
docker-compose -p local-dev down
```


2. Nettoyer les volumes (Attention à ne pas supprimer les volumes de vos propres projets):

```
docker volume prune
```

3. Créer un environnement virtuel de travail avec [Anaconda](https://www.anaconda.com/products/individual):

```
conda create -n py310 python=3.10
conda activate py310
```

4. Charger l'environnement docker sans project-api & project-worker:

```
docker-compose -p local-dev down
docker-compose -p local-dev stop project-api
docker-compose -p local-dev stop project-worker
```

4. Créer un environnement virtuel pour l'api, installer ses dépendances et la charger:

```
conda create -n api310 python=3.10
conda activate api310
cd full-stack-fastapi-celery/project-api
pip install -r requirements
cd project-api

uvicorn api:app --host 0.0.0.0 --port 5000 --workers 1 --reload
```

Tips : --reload permet de recharger automatiquement l'API à chaque modification de son code.

5. Créer un environnement virtuel pour le worker, installer ses dépendances et le charger:

```
conda create -n worker310 python=3.10
conda activate worker310
cd full-stack-fastapi-celery/project-worker
pip install -r requirements
cd project-worker

# Si votre OS est windows 
set FORKED_BY_MULTIPROCESSING=1

celery -A tasks:app worker --pool prefork -Q project-worker --concurrency=1 -n worker@%h
```

Roadmap
============

- project-api (FastAPI) :
--- Finir la documentation fichier par fichier
--- Implémenter des tâches celery : avec argument / sans argument / avec une serialisation pickle
--- Implémenter dans l'api une app qui fait des requêtes crud asynchrone avec PostgreSQL
--- Implémenter les tests pour l'api
--- Implémenter un websocket
--- Implémenter une authentification oauth2
--- Implémenter une partie privée / publique à l'API

- project-worker (Celery) :
--- Finir la documentation fichier par fichier
--- Implémenter les tests pour le worker celery

- monitoring-workflow (celery + celery-director ???) :
--- Monitorer un workflow

- project-dash (plotly/dash) :
--- Implémenter une dashboard avec plotly/dash et qui consomme l'API Rest

Détails fichier par fichier de l'ensemble du projet
============

## [docker-compose.yml](docker-compose.yml)

Le docker-compose est un fichier yaml qui décrit l'ensemble des micro-services ainsi que leurs relations entre eux au sein d'un même environnement.
C'est le point d'entrée du projet. Pas de magie vaudou ici, tout est question de description. Pour maitriser un `docker-compose` il suffit de comprendre ce que l'on va décrire.

Ce fichier se décompose principalement en 3 grandes sections :

```
volumes:

networks:

services:
```

- `volumes` décrit les volumes qui seront persistés physiquement sur la machine hôte ;
- `networks` décrit l'architecture réseau ;
- `services` décrit l'ensemble des services qui seront charger.

#### Les `volumes` :

- les données des bases de données sont persistées pour être représentatif de ce que vous auriez en production ;
- Les données des middleware (RabbitMQ & Redis) ne sont pas persitées, mais elle pourraient l'être.

#### Les `networks` :

- Deux réseaux distincts ont été créé `front-tier` & `back-tier` ;
- `front-tier` fait référence au réseau qui sera exposé à des utilisateurs tiers ;
- `back-tier` fait référence au réseau protégé accessible qu'avec des droits très restreints ;
- Seulement 2 services sont exposés sur le réseau `front-tier`: l'API REST (FastAPI) & le monitoring des métriques (Grafana).

#### Les `services` :

Par défaut, la description d'un service ne nécessite pas de définir beaucoup d'informations.
Toutefois, à des fins didactiques, chaque point important a été décrit explicitement pour faciliter la compréhension (PEP 20 : Explicit is better than implicit.).

Prenons l'exemple du service `node-exporter` :

```
node-exporter:
  image: prom/node-exporter:latest
  hostname: node-exporter
  container_name: node-exporter
  deploy:
    replicas: 1
  ports:
    - 9100:9100
  networks:
    - back-tier
  restart: always
```

En détails :
- `image` : Fait référence à l'image du service qui se trouve sur le [hub public de docker](https://hub.docker.com/) ;
- `hostname` : Attribut un nom sur le réseau au service. Dans notre cas, cela illustre très bien l'utilisation d'un DNS. Le DNS permet de remplacer l'usage direct de l'IP par un nom. Utiliser un DNS est une bonne pratique qui rend résiliant aux problématiques de changement d'IP ;
- `replicas` : Définit le nombre de répliques du service qui seront chargées dans l'environnement. Répliquer un service est une pratique courante notamment pour gérer des problématiques de charges et de backup. Les répliques s'accompagnent souvent d'outils complémentaires pour pouvoir gérer l'interraction entre les copies et la gestion dynamique du nombre de répliques. Par exemple, si le service répliqué est une API REST, la répartition des appels entre les répliques se fera à l'aide d'un LoadBalancer et la gestion dynamique du nombre de réplique (AutoScaling) sera basé sur des métriques personnalisées (I/O, cpu, mémoire, ...) ;
- `ports` : Map l'ip Externe avec l'IP interne ;
- `networks` : Définit les réseaux accessibles par le service.
- `restart` : Politique de redémarrage.

Evidemment, l'exemple du `node-exporter` fait référence à un service externe. Si on souhaite ajouter un service qui existe au sein du projet, il suffira de substituer la section `image` par `context` comme dans cet exemple avec l'API REST :

```
  project-api:
    build:
      context: ./project-api
    hostname: project-api
    container_name: project-api
    deploy:
      replicas: 1
    command: [
      "uvicorn", 
      "api:app", 
      "--host", 
      "0.0.0.0", 
      "--port", 
      "5000", 
      "--workers", 
      "2", 
      "--log-level", 
      "info"]
    environment:
      POSTGRES_DATABASE_URL: postgresql+asyncpg://postgres:postgres@postgres/postgres
      CELERY_BROKER_URL: pyamqp://guest:guest@rabbitmq:5672//
      CELERY_RESULT_BACKEND_URL: redis://redis:6379/0 
    ports:
      - 5000:5000
    networks:
      - back-tier
      - front-tier
    depends_on:
      - rabbitmq
      - redis
    restart: always
```

Pour finir, ce dernier exemple illustre parfaitement d'autres sections qui ont leur intérêt :
- `context` : Définit la localisation service qui sera compilé avec un `Dockerfile` ;
- `command` : Définit la commande qui sera executée au lancement du conteneur. A noter que si une commande est définie à la dernière ligne d'un `Dockerfile`, celle définit dans le docker-compose l'écrasera. Généralement, la commande définie à la fin des `Dockerfile` servira principalement pour lancer unitairement le service tandis que la commande définie dans le docker-compose sera adaptée à l'environnement ;
- `environment` : Définit les variables d'environnement à charger dans le service. L'utilisation de variables d'environnements (à bon escient) dans les services permet une plus grande modularité des services par rapport à leur utilisation dans différents environnements.
- `depends` : Définit la relation de dépendance du service par rapport à d'autres services.
