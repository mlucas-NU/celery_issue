docker stop celery_worker celery_enqueue rabbitmq:3-management
docker rm celery_worker celery_enqueue rabbitmq:3-management
docker rmi celery_worker celery_enqueue rabbitmq:3-management
docker network rm rabbit_network
