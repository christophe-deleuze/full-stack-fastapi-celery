Description
============

Ce projet présente une stack complète composée d'une API REST (FastAPI) et d'un worker (Celery).
L'objectif de ce projet est didactique : monitoring, tests, métriques, documentation et bonnes pratiques sont disséminées partout.
Prenez le temps de regarder chaque fichier pour comprendre comment l'ensemble des services interagissent entre eux.

Voici un aperçu visuel du projet :

[![Project docs](img/project-architecture.png)](https://github.com/christophe-deleuze/full-stack-fastapi-celery)

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

- Implémenter des tâches celery : avec argument / sans argument / avec une serialisation pickle
- Implémenter dans l'api une app qui fait du crud asynchrone avec PostgreSQL
- Implémenter les tests pour l'api
- Implémenter les tests pour le worker celery
- Finir la documentation fichier par fichier

Détails fichier par fichier du projet
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

## [app.core.config.py](/app/core/config.py)

Fichier de configuration qui sert à gérer les variables d'environnements.

Au démarrage de l'application, la librairie Pydantic lit les variables d'environnements et remplace la valeur par défaut de chaque attribut de classe ayant le même nom qu'une variable d'environnement. 

Bonne pratique :
- Pas de donnée confidentielle dans les Settings ;
- Typer les variables ;
- Définir les hosts par défaut à 127.0.0.1 pour qu'ils accèdent nativement aux autres services chargés sur votre environnement de dev.

Ce que l'on y met :
- Nom de l'API
- Version de l'API
- Description de l'API
- Host
- User
- Password
- Broker
- Result Backend
- Timeout
- ...

## [app.core.celery.async_celery.py](project-api/project-api/app/core/celery/async_celery.py)

Celery est un framework de distribution de tâches asynchrones.
Il faut distinguer le producer qui génère des tâches et le worker qui traite des tâches.
Pour distribuer les tâches, Celery à besoin d'un broker et d'un result_backend.
Le broker est le messager qui enregistre les tâches.
Le result_backend est la base de données en mémoire qui stocke temporairement le résultat des tâches.
Le découplage broker / result_backend permet d'optimiser leurs travails respectifs.

Dans notre environnement :
- broker : RabbitMQ ;
- result_backend : Redis ;
- producer : FastAPI.

Celery n'est pas (encore) nativement compatible avec asyncio.
Par conséquent, pour tirer au maximum partie des capacités asynchrones de FastAPI il est nécessaire d'adapter Celery.
Seul les fonctionnalités qui servent à produire des tâches ont besoin d'être wrapper.

A noter que Celery permet de produire des tâches de deux façons.
- On connait la tâche : Il suffit de l'importer ;
- On ne connait pas la tâche : Il suffit de réecrire une signature.

Pour découpler l'API des dépendances des tâches, seul la seconde approche est à retenir.

Les fonctions à wrapper sont donc :
- Celery().send_task()
- AsyncResult.get()

En complément du wrap des fonctions précédentes, le fichier possède une fonction qui permet d'attendre la mise à disposition d'un résultat d'une tâche distribuée avec le framework Celery. L'attente de type 'exponential backoff'.

NB : AsyncResult.get() étant bloquant, un timeout est systématiquement employé avec l'appel de la méthode.

Voici les deux cinématiques de tâches implémentées dans l'API:

```
##### Cinématique 'synchrone'
# Envoi de la tâche
async_result = await send_task(*args, **kwargs)
# Attente du résultat
await task_ready(async_result)
# Récupération du résultat
resultat = await task_result(async_result)

##### Cinématique 'asynchrone'
### Etape 1: Générer une tâche et récupérer son identifiant
# Envoi de la tâche
async_result = await send_task(*args, **kwargs)
# Retourner l'UUID unique de la tâche
task_id = async_result.id

### Etape 2: Récupérer le résultat d'une tâche à partir de son identifiant
# Attente du résultat
async_result = await task_async_result(task_id)
# Récupération du résultat
resultat = await task_result(async_result)
```

Pour transformer les fonctions synchrones en fonction asynchrones, j'utilise la librairie asgiref qui est nativement disponible avec FastAPI.

```
from asgiref.sync import sync_to_async
```

Tips :
- Par défaut la serialisation des tâches se fait au format json ;
- Dans un environnement sécurisé, il est possible d'ajouter la serialisation pickle à Celery afin de permettre de transiter n'importe quel objet python natif d'un service à un autre ;
```
app.conf.update(
    accept_content = ['application/json', 'application/x-python-serialize']
)
```
- Pour définir la serialisation à utiliser lors de l'envois d'une tâche on utilisera serializer='json' / serializer='pickle' : 
- Sécuriser les connections avec le broker (confirmer la publication des tâches) & le backend (garder la connection en vie) :
```
app.conf.update(
    broker_transport_options = {
        "confirm_publish": True,
        "max_retries": 5 },
    redis_socket_keepalive=True
)
```
- A chaque service autonome, sa propre file d'attente (queue). Le nom de la file d'attente sera le nom du type de service et le nom des tâches sera le nom des fonctions ;
- NB : Le nom des tâches pourrait être précédé du nom du service pour faciliter la lecture des logs.

Bonne pratique :
- Définir explicitement une tâche avec son nom, sa serialisation et sa file d'attente ;
- Expirer automatiquement une tâche celery avec un timeout et révoquer la tâche après timeout ;
- Supprimer automatiquement un résultat après récupération ;
- Executer des tâches de manières asynchrone en récupérant leur UUID qui pourrait être utilisé plus tard pour récupérer le résultat.

## [app.core.celery.schemas.py](project-api/project-api/app/core/celery/schemas.py)

Ce fichier sert à définir les schemas de validation génériques à utiliser pour manipuler des tâches celery asynchrones.

- AsyncTask est le modèle de réponse utilisé pour retourner l'id d'une tâche ;
- AsyncTaskStatus est le modèle de réponse utilisé pour retourner le status d'une tâche (id, status, result).