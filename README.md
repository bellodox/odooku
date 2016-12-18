![Odooku](https://cdn.rawgit.com/adaptivdesign/odooku/master/img.svg "Odooku")

# Odooku
Run Odoo on Heroku.

[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy)

```
$ heroku create --buildpack https://github.com/adaptivdesign/odooku-buildpack
$ heroku addons:create heroku-postgresql:hobby-basic
$ heroku addons:create heroku-redis:hobby-dev
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
$ heroku run odooku database preload [--demo-data]
```

### CRON tasks

CRON jobs can be run in 3 differents ways:

#### Along side the web process

This runs a somewhat slower polling cron worker. Ideal for most setups.

```
$ odooku wsgi --cron
```

#### Dedicated worker process

This should be used for installations with long running cron jobs
(like mass mailing).

```
$ odooku cron
```

#### Scheduled process

You can also make use of Heroku's scheduler, run Odooku as follows:

```
$ odooku cron --once
```

## Vagrant development machine
A vagrant machine is provivded for development purposes. It fully emulates
the Heroku environment. A random database, S3 bucket and admin password are
created by the 'new-env' command.

```
$ vagrant up
$ vagrant ssh
$ cd /vagrant
$ ./manage build
$ ./manage run web
```

### Run a worker in vagrant

```
$ ./manage run worker
```

### Enter a shell

```
$ ./manage run shell
```

### Execute a command

```
$ ./manage run exec <command>
```

### Psql access

```
$ ./manage pg psql
```

### Create new database and S3 bucket

```
$ ./manage env new
$ ./manage pg createdb
$ ./manage run exec odooku database preload
$ make run-web
```

## Database
Odooku can be run in single database mode, or Odoo's regular behaviour. If a
database is specified in DATABASE_URL, single database mode is enabled.

### Backup and Restore

```
$ heroku run odooku database dump --s3-file dump.zip
$ heroku run odooku database restore --s3-file dump.zip
```

Backup and restore from within the Vagrant development machine:

```
$ ./manage run exec odooku database dump > /vagrant/dump.zip
$ ./manage run exec odooku database restore < /vagrant/dump.zip
```

Restore into non empty database:

```
$ odooku database restore --truncate
```


### Admin password
Odooku disables the default admin password configuration entry used by Odoo.

```
$ heroku config:set ODOOKU_ADMIN_PASSWORD=<your_password>
```

## New Relic
Odooku can integrate with New Relic make sure to modify your requirements.txt.

The following environment variables are available:

- NEW_RELIC_LICENSE_KEY (required)
- NEW_RELIC_CONFIG_FILE

```
# requirements.txt
newrelic
...


$ heroku config:set NEW_RELIC_LICENSE_KEY=<your_newrelic_license_key>
$ ./manage env set NEW_RELIC_LICENSE_KEY=<your_newrelic_license_key>

```
