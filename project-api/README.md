Description
============

Ce projet est une API REST construite avec le Framework FastAPI.

L'API intègre les fonctionnalités suivantes :

- Requêtes asynchrones vers une base de donnée PostGreSQL ;
- Requêtes asynchrones vers des services distribués via le Framework Celery ;
- Websocket (asynchrone);
- Authentification oauth2 ;
- Découpage de l'API avec une partie publique et une autre partie privée.

Requirements
============

Vous avez besoin de [Docker](https://www.docker.com/products/docker-desktop) pour créer l'ensemble de l'environnement sur votre machine.
Une fois Docker exécuté, vérifier qu'il est bien lancé en mode Linux ! 

Vous avez besoin d'[Anaconda (MiniConda)](https://docs.conda.io/en/latest/miniconda.html) pour créer l'environnement virtuel qui permettra de charger localement le projet en suivant ce readme.

Quick Start
============

1. Créer un environnement virtuel de travail pour le projet API avec [Anaconda (MiniConda)](https://docs.conda.io/en/latest/miniconda.html):

```
conda create -n api310 python=3.10
conda activate api310
```

2. Cloner le projet avec [git](https://git-scm.com/downloads) ou le télécharger directement ([ici](https://github.com/christophe-deleuze/full-stack-fastapi-celery/archive/refs/heads/dev.zip)) :

```
git clone https://github.com/christophe-deleuze/full-stack-fastapi-celery.git
```

3. Charger toute l'architecture avec docker sans project-api (car on va le lancer nous même) :

```
cd ../full-stack-fastapi-celery/
docker-compose -p local-dev up -d
docker-compose -p local-dev stop project-api
```

4. Installer les dépendances du projet API :

```
cd ../full-stack-fastapi-celery/project-api/
pip install -r requirements
```

5. lancer manuellement l'API en mode reload pour aider au développement (--reload) :

```
cd ../full-stack-fastapi-celery/project-api/project-api/
uvicorn api:app --host 0.0.0.0 --port 5000 --workers 1 --reload
```

6. Vérifier que l'API est bien chargée en allant voir la documentation à l'url suivante : [API](http://127.0.0.1:5000/docs).

Quelques mots sur l'API
============

Une API REST fournit une interface à des clients qui ont besoins d'exploiter des services.
Le rôle de l'API est tout simplement de distribuer des tâches / requêtes et d'en retourner les résultats à ceux qui les ont demandés.

Il existe deux approches fonctionnelles pour construire une API :
- L'approche Synchrone ;
- L'approche Asynchrone.

## L'approche Synchrone

L'approche synchrone consiste à traiter des tâches (fonctions, requêtes, ou autre) par ordre d'arrivée.

En Python, le Framework qui permet de construire des API REST Synchrone le plus utilisé est [Flask](https://flask.palletsprojects.com/).

## L'approche Asynchrone

L'approche Asynchrone consiste à mettre à profit les temps morts des tâches (fonctions, requêtes, ou autre), qui sont généralement des temps d'attentes, afin de libérer la capacité de calcul CPU pour que celui-ci puisse traiter d'autres demandes en parallèles.

En Python, le Framework qui permet de construire des API REST Asynchrone le plus utilisé est [FastAPI](https://fastapi.tiangolo.com/).

En général, si le Framework permet de faire de l'asynchrone, il peut aussi faire du synchrone. 

## Les workers

Que l'on travaille avec une API asynchrone ou synchrone, si on veut améliorer la capacité de l'API à gérer de la charge, il faudra utiliser plusieurs instances de celle-ci, on parle de workers.

De plus, dans le cas d'une API synchrone, utiliser des workers permet d'améliorer la scalabilité et de palier aux problématiques de tâches longues qui s'alterneraient avec des tâches rapides.

qui s'alterneraient avec des tâches rapides, la solution la plus efficace consiste à utiliser en parallèle plusieurs instances de l'API, on parle de workers.

## La documentation

Comme une API est une interface consommée par des services tiers, il faut fournir aux développeurs de ces services tiers une documentation qui les aidera à utiliser votre API.

Or, l'une des forces de FastAPI consiste à auto-générer cette documentation en respectant les recommandations de [Swagger](https://swagger.io/).
De plus, un des avantages les plus intéressants de cette documentation, en plus de vous simplifiez le travail pour la créer, est de vous fournir la possibilité de tester directement, via la documentation, les appels à l'API !
Donc si vous avez une url à retenir, c'est bien celle-ci : [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs).

## L'architecture de l'API

Encore une fois, l'API est juste une interface dont le rôle est d'appelé d'autres composants (on parle d'applications) qui eux feront des traitements et retourneront des résultats à l'API qui elle, les mettra à disposition des clients.

Ainsi, de manière générique, l'API est architecturée autour d'applications ([dossier app](project-api/app)).
Ce qu'il faut retenir, c'est que dans la structure du projet il y a quasiment toujours :
- Une application ([dossier app/api](project-api/app/api)) qui définit les endpoints et les versions de l'API ;
- Une application ([dossier app/core](project-api/app/core)) qui définit les composants essentiels à l'API.

Dans notre projet, les composants essentiels sont :
- Une intégration asynchrone du Framework Celery ;
- La gestion des paramètres générique de l'API par des variables d'environnement (avec pydantic).

## Les métriques

Dans une architecture distribuée, tout service doit retourner des métriques afin de permettre d'évaluer la santé du service.
L'API n'échappe pas à cette règle. Ainsi, toutes les requêtes et les ressources utilisées par l'API doivent être monitorées.
Le composant qui retourne les métriques se place au milieu de l'API (middleware) afin de pouvoir collecter l'ensemble des informations nécessaires.
Dans notre projet, les métriques sont exposées à l'endpoint [http://127.0.0.1:8000/metrics](http://127.0.0.1:8000/metrics).

Détails fichier par fichier du projet
============

## [app.core.config.py](project-api/app/core/config.py)

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

## [app.core.celery.async_celery.py](project-api/app/core/celery/async_celery.py)

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

## [app.core.celery.schemas.py](project-api/app/core/celery/schemas.py)

Ce fichier sert à définir les schemas de validation génériques à utiliser pour manipuler des tâches celery asynchrones.

- AsyncTask est le modèle de réponse utilisé pour retourner l'id d'une tâche ;
- AsyncTaskStatus est le modèle de réponse utilisé pour retourner le status d'une tâche (id, status, result).