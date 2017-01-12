Clone the Odooku repository or create your own repository. Odooku is like
any other Heroku project, however the Odooku buildpack also requires
an `odooku.json` file.

## Project structure

### Procfile ###

Tell Heroku what to run:

```
web: odooku wsgi $PORT
```

### odooku.json ###

The Odooku buildpack needs to know which Odoo and `Odooku compat` version
to fetch.
```
{
  "odoo": {
    "repo": "odoo/odoo",
    "branch": "10.0",
    "commit": null
  },
  "compat": {
    "repo": "adaptivdesign/odooku-compat",
    "branch": "10.0",
    "commit": null
  }
}

```

### addons ###

Place your addons under `/addons`


## First deployment

```
$ heroku create --buildpack https://github.com/adaptivdesign/odooku-buildpack
$ heroku addons:create heroku-postgresql:hobby-basic
$ heroku addons:create heroku-redis:hobby-dev
$ heroku config:set AWS_ACCESS_KEY_ID=<your_aws_key>
$ heroku config:set AWS_SECRET_ACCESS_KEY=<your_aws_secret>
$ heroku config:set S3_BUCKET=<your_s3_bucket_name>
$ git push heroku master
```
