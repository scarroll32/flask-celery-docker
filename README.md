# Docker Flask Celery Redis

A basic [Docker Compose](https://docs.docker.com/compose/) template for orchestrating a [Flask](http://flask.pocoo.org/) application & a [Celery](http://www.celeryproject.org/) queue with [Redis](https://redis.io/)

### Installation

```bash
git clone git@gitlab.com:sfcarroll/flask-celery-docker.git
cp .env.example .env
```

### Build & Launch

```bash
docker-compose up -d --build
```

This will expose the Flask application's endpoints on port `5000` as well as a [Flower](https://github.com/mher/flower) server for monitoring workers on port `5555`

To add more workers:
```bash
docker-compose up -d --scale worker=5 --no-recreate
```

To shut down:

```bash
docker-compose down
```

Start, stop, delete
```bash
stop all containers:
docker kill $(docker ps -q) &&  docker rm $(docker ps -a -q) && docker rmi $(docker images -q)

remove all containers
docker rm $(docker ps -a -q)

remove all docker images
docker rmi $(docker images -q)

```

To change the endpoints, update the code in [api/app.py](api/app.py)

Task changes should happen in [queue/tasks.py](celery-queue/tasks.py)


## Initial build

```
git clone https://github.com/seanfcarroll/flask-celery-docker.git
docker-compose build
docker-compose up -d
```

## Get status and logs
```
docker-compose ps
docker ps
docker logs 7b7ff37ed2d5
```


## Rebuild a specific container
```
docker-compose ps
docker-compose stop web
docker-compose rm web
docker-compose up -d
```


### Start, stop, delete
```
stop all containers:
docker kill $(docker ps -q) &&  docker rm $(docker ps -a -q) && docker rmi $(docker images -q)

remove all containers
docker rm $(docker ps -a -q)

remove all docker images
docker rmi $(docker images -q)
```

### Shell into container
```
sudo docker exec -i -t 665b4a1e17b6 /bin/bash
```


## Scaling

```
docker-compose scale worker=5
```
This will create 4 more containers each running a worker. http://your-dockermachine-ip:5555 should now show 5 workers waiting for some jobs!


## Helpful

https://gist.github.com/amatellanes/a986f6babb9cf8556e36

https://stackoverflow.com/questions/50798281/register-multiple-tasks-with-celery

https://stackoverflow.com/questions/43920621/celery-tasks-on-multiple-machines

https://stackoverflow.com/questions/19853378/how-to-keep-multiple-independent-celery-queues
