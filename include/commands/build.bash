build() {
	declare desc="Build the Herokuish Docker image"
	declare commit=`(git rev-parse HEAD)`
	ensure-dirs

	title "Starting build"
	echo "Removing stale Docker containers and images" | indent
	docker rm -f -v $identifier &> /dev/null || true
	docker rmi -f $identifier/$identifier:latest &> /dev/null || true
	echo "Using local commit $commit" | indent
	rm -rf $local_app_dir
	mkdir -p $local_app_dir
	git archive --format=tar $commit | (cd $local_app_dir/ && tar xf -)
	title "Building slug"
	touch $local_slug_file
  docker run \
		--rm \
		-e BUILDPACK_URL=$buildpack_path \
		-v $local_slug_file:$container_slug_file \
		-v $local_app_dir:/tmp/app \
		-v $local_cache_dir:/tmp/cache \
		gliderlabs/herokuish \
		bin/bash -c \
			"USER=herokuishuser /bin/herokuish buildpack build \
			&& USER=herokuishuser IMPORT_PATH=/nosuchpath /bin/herokuish slug generate \
			&& USER=herokuishuser /bin/herokuish slug export > $container_slug_file"

	title "Building Docker image"
	echo "Importing slug" | indent
	docker run \
		-i \
		--name $identifier \
    gliderlabs/herokuish \
    bin/bash -c \
      "USER=herokuishuser /bin/herokuish slug import <&0" < $local_slug_file

	echo "Writing new Docker image" | indent
	docker commit $identifier $identifier/$identifier:latest &> /dev/null || true
	echo "Cleaning up" | indent
	docker rm -f -v $identifier &> /dev/null || true
}

clean() {
	remove-dirs
	ensure-dirs
}
