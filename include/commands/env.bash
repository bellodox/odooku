env-new() {
	declare desc="Create a new environment"
	declare unique=$(cat /dev/urandom | tr -dc 'a-z0-9' | fold -w 32 | head -n 1)
	declare database_url="postgres://odoo:odoo@localhost:5432/$unique"
	ensure-dirs
	title "Creating new environment"
	echo "Admin password: $unique" | indent
	echo "Database url: $database_url" | indent
	tee $local_env_file > /dev/null <<EOF
export DATABASE_URL=$database_url
export ADMIN_PASSWORD=$unique
export REDIS_URL=redis://localhost:6379
export S3_BUCKET=$unique
export S3_ENDPOINT_URL=http://localhost:4569
export S3_CUSTOM_DOMAIN=http://$unique.localhost:4569
export AWS_ACCESS_KEY_ID=foobar
export AWS_SECRET_ACCESS_KEY=foobar
EOF
}

env-set() {
	declare desc="Set environment variables"
	for var in "$@"
	do
		tee -a $local_env_file > /dev/null <<EOF
export $var
EOF
	done
}

env-print() {
	declare desc="Print environment variables"
	echo `$local_env_file > cat`
}
