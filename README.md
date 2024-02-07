# calc_serv
calc_python en socket server dockerisé

## README

Ce document fournit des instructions pour tester le projet en récupérant une image Docker et en utilisant un Docker Compose.

## Prérequis 

### LINUX

- Avoir Docker installé sur votre machine. Pour l'installation, suivez les instructions sur [Docker](https://docs.docker.com/get-docker/).
- Avoir Docker Compose installé. Pour l'installation, consultez [Docker Compose](https://docs.docker.com/compose/install/).

### WINDOWS

- Docker installé sur votre machine Windows.
- **- UN TERMINAL GITBASH pour executez toutes les commandes**

## GUIDE INSTALLATION & LANCEMENT PROJET

### 1: Récupérer le Repository GitHub

Clonez le repository GitHub contenant les fichiers nécessaires dans un dossier vide :

```bash
git clone https://github.com/fyleeds/calc_serv.git

```

### 2: Lancez Docker

#### SUR WINDOWS : 

Double-Clickez sur l'icone de Docker Desktop et attendez son chargement

#### SUR LINUX : 

```bash
sudo systemctl start docker
```

### 3: Renseignez CALC_PORT dans docker-compose.yml

```
version: '3'

services:
  calc:
    build: .
    volumes:
      - ../:/app
    environment:
      - CALC_PORT= 5000
```

### 4: Lancez le conteneur depuis un terminal

Restez sur le terminal et naviguez vers le dossier "docker" dans le projet : 
```bash
cd chemin/vers/dossier_de_clone/calc_build
```
Puis déployez le site avec la commande : 
```bash
docker compose up 
```
### 5: Accès services 

Après avoir exécuté la commande, Docker Compose va démarrer les services.

- Accédez à localhost:"CALC_PORT" pour interagir avec l'application calc

### 6 Quittez le projet

Dans le dossier docker executez : 
```bash
docker compose down 
```
![CATDANCEEDM](./calculator_achievement.gif)
