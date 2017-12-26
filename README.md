# Odooku

> Odoo en la plataforma Heroku

```sh
HEROKU_PROJECT="erste-staging"

# Crear proyecto en Heroku
heroku create $HEROKU_PROJECT

# Agregar buildpacks
heroku buildpacks:add https://github.com/adaptivdesign/odooku-buildpack.git#10.0 --index 1 --app $HEROKU_PROJECT
heroku buildpacks:add https://github.com/SectorLabs/heroku-buildpack-git-submodule.git --index 2 --app $HEROKU_PROJECT

# Configurar variables de entorno
heroku --app $HEROKU_PROJECT config:set GIT_REPO_URL=git@github.com:Prescrypto/odooku
heroku --app $HEROKU_PROJECT config:set GIT_SSH_KEY="<id_rsa>"
heroku --app $HEROKU_PROJECT config:set AWS_ACCESS_KEY_ID=<key_de_aws>
heroku --app $HEROKU_PROJECT config:set AWS_SECRET_ACCESS_KEY=<secreto_de_aws>
heroku --app $HEROKU_PROJECT config:set AWS_REGION=<region_de_aws>
heroku --app $HEROKU_PROJECT config:set S3_BUCKET=<bucket_de_s3>


# agregar addons requeridos
$ heroku addons:create heroku-postgresql:hobby-basic
$ heroku addons:create heroku-redis:hobby-dev

# deploy
git push heroku master
```

# add rest api module
