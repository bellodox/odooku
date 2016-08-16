![Odooku](https://cdn.rawgit.com/adaptivdesign/odooku/master/img.svg "Odooku")

# Odooku
Run Odoo on Heroku.

[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy)

```
$ heroku create --buildpack https://github.com/adaptivdesign/odooku-buildpack
$ heroku addons:create heroku-postgresql:hobby-basic
$ heroku config:set AWS_ACCESS_KEY_ID=<your_aws_key>
$ heroku config:set AWS_SECRET_ACCESS_KEY=<your_aws_secret>
$ heroku config:set S3_BUCKET=<your_s3_bucket_name>
$ git push heroku master
```

## Heroku installation

### S3 Storage
The Odoo filestore is mirrored in a S3 bucket. Enabling Odooku to use S3
requiresthat the Dyno's have access to the AWS credentials as well as the
name of the bucket to store files.

Odooku exposes 3 environment variables that need to be configured:

```
$ heroku config:set AWS_ACCESS_KEY_ID=<your_aws_key>
$ heroku config:set AWS_SECRET_ACCESS_KEY=<your_aws_secret>
$ heroku config:set S3_BUCKET=<your_s3_bucket_name>
```

Your S3 credentials can be found on the Security Credentials section of the
AWS “My Account/Console” menu.

### Redis (optional)
Redis is only required if you're running multiple web dyno's. Odooku needs a way
to maintain session data between all dyno's.

```
$ heroku addons:create heroku-redis:hobby-dev
```

### Preloading database
When running against a new database, it's recommended to preload the database
usign the 'odooku preload' command. Database initialization using a web worker
is possible however.

```
$ heroku run odooku preload [--demo-data]
```

### CRON worker

CRON tasks are not running on web instance, so a worker instance is required.
Simply run Odooku as follows:

```
$ odooku cron
```

You can also make use of Heroku's scheduler, run Odooku as follows:

```
$ odooku cron --once
```

## Vagrant development machine
A vagrant machine is provivded for development purposes. It fully emulates
the Heroku environment.

```
$ vagrant up
$ vagrant ssh
$ cd /vagrant
$ make build
$ make run-web
```

### Run a worker in vagrant

```
$ make run-worker
```

### Enter a shell

```
$ make shell
```

### Psql access

```
$ make psql
```

### Create new database and S3 bucket

```
$ make new-env
$ make shell
$$ odooku preload
$ make run-web
```
