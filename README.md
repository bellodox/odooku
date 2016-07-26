# odooku
Run Odoo on Heroku

[![Deploy](https://www.herokucdn.com/deploy/button.png)](https://heroku.com/deploy)

#

https://devcenter.heroku.com/articles/s3

$ heroku create --buildpack https://github.com/adaptivdesign/odooku-buildpack
$ heroku addons:create heroku-postgresql:hobby-dev
$ heroku config:set AWS_ACCESS_KEY_ID=<your_aws_key>
$ heroku config:set AWS_SECRET_ACCESS_KEY=<your_aws_secret>
$ heroku config:set S3_BUCKET=<your_s3_bucket_name>
$ git push heroku master
