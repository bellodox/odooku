web: odooku --database-maxconn 8 --redis-maxconn 8 wsgi $PORT --workers 2
worker: odooku --database-maxconn 2 --redis-maxconn 2 cron --workers 2
