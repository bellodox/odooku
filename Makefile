include /odooku/env.mk

PORT=8000
NUM=1
DB_USER=$(shell echo ${DATABASE_URL} | sed -e 's/^postgres:\/\/\(.*\):.*@.*:.*\/.*$$/\1/')
DB_PASSWORD=$(shell echo ${DATABASE_URL} | sed -e 's/^postgres:\/\/.*:\(.*\)@.*:.*\/.*$$/\1/')
DB_HOST=$(shell echo ${DATABASE_URL} | sed -e 's/^postgres:\/\/.*:.*@\(.*\):.*\/.*$$/\1/')
DB_PORT=$(shell echo ${DATABASE_URL} | sed -e 's/^postgres:\/\/.*:.*@.*:\(.*\)\/.*$$/\1/')
DB_NAME=$(shell echo ${DATABASE_URL} | sed -e 's/^postgres:\/\/.*:.*@.*:.*\/\(.*\)$$/\1/')
BUILDPACK_URL=https://github.com/adaptivdesign/odooku-buildpack

NEW_DATABASE:=$(shell cat /dev/urandom | tr -dc 'a-zA-Z0-9' | fold -w 32 | head -n 1)

define NEW_ENV
DATABASE_URL=postgres://odoo:odoo@localhost:5432/${NEW_DATABASE}
ADMIN_PASSWORD=${NEW_DATABASE}
REDIS_URL=redis://localhost:6379
S3_BUCKET=${NEW_DATABASE}
endef

export NEW_ENV


define RUN_ARGS
--net host \
-v /vagrant:/vagrant \
-v /odooku:/odooku \
-e DATABASE_URL="${DATABASE_URL}" \
-e REDIS_URL="${REDIS_URL}" \
-e S3_BUCKET="${S3_BUCKET}" \
-e S3_DEV_URL="http://localhost:4569" \
-e PORT="${PORT}" \
-e ODOOKU_ADMIN_PASSWORD="${ADMIN_PASSWORD}" \
gliderlabs/herokuish
endef


define BASH_INIT
echo '-----> Importing slug' \
;/bin/herokuish slug import < /odooku/slug.tar.gz \
;[[ -d /vagrant/addons ]] \
	&& echo '-----> Mounting addons' \
	&& rm -rf /app/addons \
	&& ln -s /vagrant/addons /app/addons \
	&& echo '-----> Enabling dev mode' \
	&& export ODOOKU_DEV=true
endef


new-env:
	@echo "Creating empty database ${NEW_DATABASE}"
	@docker exec postgres createdb -U odoo ${NEW_DATABASE}
	@echo "Creating empty s3 bucket ${NEW_DATABASE}"
	@mkdir -p /vagrant/data/s3/${NEW_DATABASE}
	@echo "Updating env"
	@echo "Admin password: ${NEW_DATABASE}"
	@echo "$$NEW_ENV" > /odooku/env.mk


build:
	@docker run \
		--rm \
		-it \
		-e BUILDPACK_URL="${BUILDPACK_URL}" \
		-v /vagrant:/tmp/app \
		-v /odooku/cache:/tmp/cache \
		-v /odooku:/odooku \
		gliderlabs/herokuish \
		bin/bash -c \
			"/bin/herokuish buildpack build \
			&& IMPORT_PATH=/nosuchpath /bin/herokuish slug generate \
			&& /bin/herokuish slug export > /odooku/slug.tar.gz"


run-web:
	-@docker rm -f -v web.1
	@docker run \
		-d \
		--name web.1 \
		${RUN_ARGS} \
		bin/bash -c \
			"${BASH_INIT} \
			;USER=herokuishuser /bin/herokuish procfile start web"
	@docker logs -f web.1


run-worker:
	-@docker rm -f  -v worker.1
	@docker run \
		-d \
		--name worker.1 \
		${RUN_ARGS} \
		bin/bash -c \
			"${BASH_INIT} \
			;USER=herokuishuser /bin/herokuish procfile start worker"
	@docker logs -f worker.1


shell:
	@docker run \
		--rm -it \
		--name shell \
		${RUN_ARGS} \
		bin/bash -c \
			"${BASH_INIT} \
			;USER=herokuishuser /bin/herokuish procfile exec /bin/bash"


psql:
	@docker run \
		--rm \
		-it \
		--net host \
		-v /vagrant/data:/tmp \
		-e PGPASSWORD=${DB_PASSWORD} \
		postgres:9.5 \
		psql -U ${DB_USER} -w -h ${DB_HOST} -p ${DB_PORT} -d ${DB_NAME}


pg-restore:
	@docker run \
		--rm \
		-it \
		--net host \
		-v /vagrant/data:/tmp \
		-e PGPASSWORD=${DB_PASSWORD} \
		postgres:9.5 \
		pg_restore -U ${DB_USER} -w -h ${DB_HOST} -p ${DB_PORT} -d ${DB_NAME} --no-owner /tmp/${DB_NAME}.dump
