include .env

build:
	docker build -t dev/$(DOCKER_NAME) .

local:
	docker ps -aq -f'name=$(DOCKER_NAME)' | xargs --no-run-if-empty docker rm -f
	docker run -d \
		--name=$(DOCKER_NAME) \
		-e SMTP_USER=$(SMTP_USER) \
		-e SMTP_PASS=$(SMTP_PASS) \
		-e SMTP_FROM=$(SMTP_FROM) \
		-e SMTP_TO=$(SMTP_TO) \
		dev/$(DOCKER_NAME)

########## CLEANING ##########
prune:
	docker ps -aq -f'name=$(DOCKER_NAME)' | xargs --no-run-if-empty docker rm -f

cleanup:
	echo "cleaning up docker images on local machine"
	docker images --no-trunc --all --quiet --filter="dangling=true" | xargs --no-run-if-empty docker rmi