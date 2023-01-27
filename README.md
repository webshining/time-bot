# <p align="center">Telegram time-avatar</p>

## Navigate
* [Getting started](#getting-started)
    * [Create project](#create-project)
    * [Environment Variables](#environment-variables)
    * [Run project locally](#run-project-locally)
* [Docker](#docker)
    * [Build](#build)
    * [Get app logs](#get-app-logs)
    * [Rebuild](#rebuild)

## Getting started
---
## Create project
```bach
$ git clone https://github.com/webshining/time-bot project-name
$ cd project-name
$ cp .env.ren .env
$ pip install -r requirements.txt
```
## Environment Variables
`API_ID` - your telegram app api_id

`API_HASH` - your telegram app api_hash

## Run project locally
```bash
$ python main.py
# or
$ make run
```
---
## Docker
---
## Build
```bash
$ docker-compose up -d
# or 
$ make compose
```
## Rebuild
```bash
$ docker-compose up -d --force-recreate --no-deps --build
# or
$ make rebuild
```
## Get app logs
```bash
$ docker-compose logs app
# or
$ make logs
```