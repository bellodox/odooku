run-exec() {
  declare desc="Execute command inside a Herokuish container"
  declare cmd="$@"
  if [ -z "$cmd" ]; then
    exit 1
  fi

  docker run \
    --rm -i \
    $run_args \
    bin/bash -c \
      "$run_init \
      ;USER=herokuishuser IMPORT_PATH=/nosuchpath /bin/herokuish procfile exec $cmd"
}

run-shell() {
  declare desc="Start a shell inside a Herokuish container"
  docker run \
    --rm -it \
    $run_args \
    bin/bash -c \
      "$run_init \
      ;USER=herokuishuser IMPORT_PATH=/nosuchpath /bin/herokuish procfile exec /bin/bash"
}

run-process() {
  declare desc="Run Herokuish procfile process"
  declare process="${1:-web}"
  docker rm -f -v $process &> /dev/null || true
  declare container=`docker run \
		-d \
		--name $process \
		$run_args \
		bin/bash -c \
			"$run_init \
			;USER=herokuishuser IMPORT_PATH=/nosuchpath /bin/herokuish procfile start $process"`
  docker logs -f $process
}

run-web() {
  declare desc="Run Herokuish web process"
  run-process "web"
}

run-worker() {
  declare desc="Run Herokuish worker process"
  run-process "worker"
}
