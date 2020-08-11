# celery-sync-example
A quick, functional example of how
[Celery](https://docs.celeryproject.org/en/stable/getting-started/introduction.html)
can be used. Our district uses Celery to perform synchronization between our
SIS and several peripheral systems. I started with this stack before Python3's
async was released, but feel that this stack provides and easier way to think
about atomic synchronization operations. It helps separate work creation from
work execution.

You define your tasks module style. That .py file or app/\_\_init\_\_.py module
is then run as a 'worker' that waits for tasks to be sent to it. The app
defines how the tasks are completed. Rabbitmq is the default job messanger,
installing and running it is enough to get a simple example up and running, no
extra configuration needed.

* Install the default rabbitmq-server backend, Celery listens here for tasks
* Define a Tasks.py file
* Run `celery -A Tasks worker &`

You would then create a Python program that would generate the work to be sent
to the Celery worker. We use pymssql to talk directly to our SIS database and
periodically pull full exports of our GSuite domain to use a cache several
times a day. We cache GSuite data to prevent running into quota problems.
