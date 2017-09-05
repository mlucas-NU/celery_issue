# Create a docker network to connect the RabbitMQ server and Celery worker containers
docker network create -d bridge --subnet 172.25.0.0/16 rabbit_network

# Run the RabbitMQ task server as a docker container
docker pull rabbitmq:3-management
docker run -d --name=rabbitmq --network=rabbit_network --ip=172.25.1.0 -p :5672 -p :15672 rabbitmq:3-management

# Build and run the Celery worker (pulls task from above server)
docker build -f docker/Dockerfile_worker -t celery_worker .
docker run -d --name=celery_worker --network=rabbit_network celery_worker
