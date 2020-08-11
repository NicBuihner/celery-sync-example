#!/usr/bin/env python3

from celery import group

# Task Definition Import
import GoogleTasks


# This is a minimal example of a user object required by the Google Python APIs
# for creating a user.
Example_User = {
    'name': {
        'givenName': student['FirstName'],
        'familyName': '{} (Student {})'.format(
            'LastName',
            'School',
        ),
    },
    'primaryEmail': 'Student@Domain.edu',
    'password': hashlib.sha1('ABadPassword').hexdigest(),
    'hashFunction': 'SHA-1',
    'orgUnitPath': '/path/to/your/org',
}
Users_To_Create = [Example_User]


def main():
    # This hands off a single task to Celery to execute. The program will exit
    # immediately while Celery runs the job.
    GoogleTasks.user_create.s(Example_User).apply_async()

    # This specifies a group of tasks to be executed in parallel. This is
    # useful when you need to block for tasks that need to happen in order, etc
    group(GoogleTasks.user_create.s(user) for user in Users_To_Create)()


if __name__ == '__main__':
    main()
