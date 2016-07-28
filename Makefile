DB_USER=$(shell echo $$DATABASE_URL | sed -e 's/^postgres:\/\/\(.*\):.*@.*:.*\/.*$$/\1/')
DB_PASSWORD=$(shell echo $$DATABASE_URL | sed -e 's/^postgres:\/\/.*:\(.*\)@.*:.*\/.*$$/\1/')
DB_HOST=$(shell echo $$DATABASE_URL | sed -e 's/^postgres:\/\/.*:.*@\(.*\):.*\/.*$$/\1/')
DB_PORT=$(shell echo $$DATABASE_URL | sed -e 's/^postgres:\/\/.*:.*@.*:\(.*\)\/.*$$/\1/')
DB_NAME=$(shell echo $$DATABASE_URL | sed -e 's/^postgres:\/\/.*:.*@.*:.*\/\(.*\)$$/\1/')


build:
	@docker run \
		--rm \
		-it \
		-v /vagrant:/tmp/app \
		-v /odooku/cache:/tmp/cache \
		-v /odooku:/odooku \
		gliderlabs/herokuish \
		bin/bash -c \
			"/bin/herokuish buildpack build \
			&& IMPORT_PATH=/nosuchpath /bin/herokuish slug generate \
			&& /bin/herokuish slug export > /odooku/slug.tar.gz"


run:
	@docker run \
		--rm \
		-it \
		--net host \
		--name web.1 \
		-v /vagrant:/vagrant \
		-v /odooku:/odooku \
		-v /odooku/filestore:/tmp/filestore \
		-e DATABASE_URL=${DATABASE_URL} \
		-e PORT=${PORT} \
		gliderlabs/herokuish \
		bin/bash -c \
			"/bin/herokuish slug import < /odooku/slug.tar.gz \
			;[[ -d /vagrant/addons ]] && cp -R /vagrant/addons /app/addons \
			;chown -R herokuishuser /tmp/filestore \
			;USER=herokuishuser /bin/herokuish procfile start web"


psql:
	@docker run \
		--rm \
		-it \
		--net host \
		-e PGPASSWORD=${DB_PASSWORD} \
		postgres:9.5 \
		psql -U ${DB_USER} -w -h ${DB_HOST} -p ${DB_PORT} -d ${DB_NAME}
