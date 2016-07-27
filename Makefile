build:
	tar cC /vagrant . | /vagrant/compile odooku

run:
	docker run \
		-d \
		--net host \
		--name web.1 \
		-e DATABASE_URL=${DATABASE_URL} \
		-e PORT=8000 \
		odooku /bin/bash -c "/start web"
