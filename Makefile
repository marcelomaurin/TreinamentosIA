IMAGE_NAME=treinamentosia
CONTAINER_NAME=treinamentosia-container

.PHONY: build run stop

build:
	docker build -t $(IMAGE_NAME) .

run:
	docker run --name $(CONTAINER_NAME) -d $(IMAGE_NAME)

stop:
	docker stop $(CONTAINER_NAME) || true
	docker rm $(CONTAINER_NAME) || true
