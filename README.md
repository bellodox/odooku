# odooku
Run Odoo on Heroku

#

'''
heroku create --buildpack https://github.com/adaptivdesign/odooku-buildpack
heroku addons:create heroku-postgresql:hobby-dev
git push heroku master
'''
