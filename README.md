# celery-sync-example
A quick, functional example of how Celery can be used.

You define your tasks module style. That .py file or app/__init__.py module is
then run as a 'worker' that waits for tasks to be sent to it. The app defines
how the tasks are completed. Rabbitmq is the default backend, installing and
running it is enough to get a simple example up and running, no extra
configuration needed.

1 Install the default rabbitmq-server backend, Celery listens here for tasks
2 Define a Tasks.py file
3 Run `celery -A Tasks worker &`

You would then create a Python program that would generate the work to be sent
to the Celery worker. We use pymssql to talk directly to our SIS database and
periodically pull full exports of our GSuite domain to use a cache several
times a day.
