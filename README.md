![odooku](https://cloud.githubusercontent.com/assets/51578/13712821/b68a42ce-e793-11e5-96b0-d8eb978137ba.png)

# Odooku
Run Odoo on Heroku

![odooku](img.svg?raw=true "Odooku")

## Run on Heroku

```
$ heroku create --buildpack https://github.com/adaptivdesign/odooku-buildpack
$ heroku addons:create heroku-postgresql:hobby-basic
$ heroku config:set AWS_ACCESS_KEY_ID=<your_aws_key>
$ heroku config:set AWS_SECRET_ACCESS_KEY=<your_aws_secret>
$ heroku config:set S3_BUCKET=<your_s3_bucket_name>
$ git push heroku master
```

## S3
All attachments are mirrored in a S3 storage, dyno's do not persist data.
Attachments are cached however.

## Redis
Redis is only required if you're running multiple web instances. Odooku can
store sessions in Redis, so that they can be shared by multiple instances.

```
$ heroku addons:create heroku-redis:hobby-basic
```


## Preloading database

When running against a new database, it's recommended to preload the database
usign the 'odooku preload' command. Database initialization using a web worker
is possible however.

```
$ heroku run bin/bash
$ odooku preload
```

## CRON worker

CRON tasks are not running on web instance, so a worker instance is required.
Simply run Odooku as follows:

```
$ odooku cron
```

You can also make use of Heroku's scheduler, run Odooku as follows:

```
$ odooku cron --once
```

# Vagrant
A vagrant machine is provivded for development purposes. It fully emulates
the Heroku environment.

```
$ vagrant up
$ vagrant ssh
$ cd /vagrant
$ make build
$ make run-web
```

## Run a worker in vagrant

```
$ make run-worker
```

## Enter a shell

```
$ make shell
```


## Psql access

```
$ make psql
```
