declare DATABASE_URL
declare db_host
declare db_port
declare db_name
declare db_user
declare db_password

parse-database-url() {
  db_user=`echo "$1" | sed -e 's/^postgres:\/\/\(.*\):.*@.*:.*\/.*$/\1/'`
  db_password=`echo "$1" | sed -e 's/^postgres:\/\/.*:\(.*\)@.*:.*\/.*$/\1/'`
  db_host=`echo "$1" | sed -e 's/^postgres:\/\/.*:.*@\(.*\):.*\/.*$/\1/'`
  db_port=`echo "$1" | sed -e 's/^postgres:\/\/.*:.*@.*:\(.*\)\/.*$/\1/'`
  db_name=`echo "$1" | sed -e 's/^postgres:\/\/.*:.*@.*:.*\/\(.*\)$/\1/'`
}

pg-run() {
  docker run \
		--rm \
		-i \
		--net host \
		-e PGPASSWORD=${db_password} \
    $2 \
		postgres:9.5 \
    $1
}

pg-psql() {
  declare desc="Start a psql shell for the configured database"
  source $local_env_file
  parse-database-url $DATABASE_URL
  pg-run "psql -U ${db_user} -w -h ${db_host} -p ${db_port} -d ${db_name}" "-t"
}

pg-createdb() {
  declare desc="Create the configured database"
  source $local_env_file
  parse-database-url $DATABASE_URL
  pg-run "createdb -U $db_user -w -h $db_host -p $db_port $db_name"
}

pg-dropdb() {
  declare desc="Drop the configured database"
  source $local_env_file
  parse-database-url $DATABASE_URL
  pg-run "dropdb -U $db_user -w -h $db_host -p $db_port $db_name"
}
