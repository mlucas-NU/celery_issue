# Build and run the Celery worker (pulls task from above server)
docker build -f docker/Dockerfile_enqueue -t celery_enqueue .
docker run -d --name=celery_enqueue --network=rabbit_network celery_enqueue
