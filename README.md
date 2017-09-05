## Issue description

Calls to the Google Cloud Vision API through the google-cloud-vision python module do not work within certain distributed task setups. This issue is not limited to Celery workers, but this repository demonstrates how a Celery project cannot make calls to the the GCV API using the google-cloud-vision module.

### Expected behavior:

On first launching this Celery worker, it should make a correct call to Google Cloud Vision and log a list of returned labels for `cat.jpg`.

Then, whenever the Enqueuer is launched, the Celery worker should execute `add(3,4)` and make an API request to Google Cloud Vision again for labels of `cat.jpg`.

### Actual behavior:

The first call to Google Cloud Vision from within the startup script succeeds.

Once the Enqueuer is launched, the worker's first call to `add(3,4)` succeeds as well. Once the Celery Worker calls Google Cloud Vision's API from within a Celery task, the entire process hangs permanently without generating any known logs.

## Duplicating the issue

### 1. Create a JSON API keyfile

If you don't already have one, create a Google Cloud Platform project at https://console.cloud.google.com/. Then, navigate to the project's dashboard -- you can change projects using the dropdown navigation at the top of the window.

Next, create an API credentials file for the project that will allow it to connect to Google Cloud Vision:

1) On the left navigate to APIs & Services > Credentials.
2) Click "Create Credentials" at the top.
3) Select "Service Account Key" and create a JSON key. This may require the creation of a service account that is capable of interacting with Google Cloud Vision.
4) Download the JSON api credentials and put it in this project's root directory as `google_creds.json`.

### 2. Launch the Celery worker

From the command line, you can build and start the Celery worker by running

``` bash
bash launch-worker.sh
```

(Optional) You can monitor the logs of the worker using

``` bash
docker logs -f celery_worker
```

##### Explanation

The `launch-worker.sh` script will:
* Create a Docker virtual network for this project.
* Download and launch a Docker container for a [RabbitMQ task manager](https://www.rabbitmq.com/) (works very well for dispatching tasks to Celery workers).
* Build and launch the Celery worker Docker container according to `docker/Dockerfile_worker`

The worker itself is specified in `celery_project/worker.py`. When the worker is launched, it sets up the following functions:

* A local function called `gcv_label_cat()` that can only be called internally. The function uploads `cat.jpg` to Google Cloud Vision's image annotation service and prints the returned labels.
* A Celery task called `add(x,y)`, which will return x+y
* A Celery task called `gcv_task()`, which simply calls `gcv_label_cat()` directly.

Launching the worker also runs an initial call to `gcv_label_cat()`, which works without issue as can be seen in the logs (a list of cat-related features are visible 


### 3. Enqueue the same GCV call using a Celery Task

Running the following will enqueue two tasks:
``` bash
bash enqueue.sh
```

##### Explanation

First, a call for `add(3,4)` will be enqueued to RabbitMQ. This script will briefly wait until the Celery worker sends the result back via RabbitMQ (with the sum, 7).

Then, the enqueuer will add a call to `gcv_task()`.

The enqueueing script's logs can be viewed by running the following, which will update as the enqueuer creates tasks and receives results:
``` bash
docker logs -f celery_enqueue
```

### Cleaning up

All docker containers, images, and networks pertaining to this project can be deleted by running:

``` bash
bash cleanup.sh
```
