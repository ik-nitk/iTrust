# Development Guide

This Architecture is based on reference architecture presented [here](https://www.thedigitalcatbooks.com/pycabook-introduction/).
Highly recommend go through the tutorial and buy the book.

## Setup

Pulling code from git

```
Create a copy of
https://github.com/ik.nitk/iTrust

in your github account.
```

Upgrade to python 3.11

Setting up virtual environment
Note: Install virutalenv in local environment.(unix)

```
virutalenv env
or python3 -m venv env
source env/bin/activate
```

Setting up virtual environment
Note: Install virutalenv in local environment.(windows)

```
pip install virtualenv
virtualenv env
env/scripts/activate.bat
```

Install required dependencies

```
pip install -r requirements/dev.txt
```

## Testing

### Unit-Test

Running full test cases

```
pytest -svv --cov=. --cov-report=term-missing
```

Running unit test on single file

```
pytest -svv --cov=cms --cov-report=term-missing tests/domain/test_member.py
```

Running integration tests.

```
./manage.py test -- --integration
```

## Running application in docker

Note: Install docker in your environment.
Build the docker container

```
./manage.py compose build
for ubuntu add sudo PWD=${PWD} for all below command :
PWD=${PWD} ./manage.py compose build
```

If this is successful you can run Docker Compose

```
./manage.py compose up -d

to tear down
./manage.py compose down

```

and the output of docker ps should show three containers running

Init the database:

```
./manage.py init-postgres

tear down the server for database tables can be updated now.
./manage.py compose down

Bring it up again
./manage.py compose up -d

```

Create default admin
```
./manage.py add-admin-member -e itrust_test@gmail.com -n itrust_test
```

open http://localhost:8080/
click `login` to login as default.

You can follow also instructions from [this](https://www.thedigitalcatbooks.com/pycabook-chapter-08/)


### Running psql command inside database

```
./manage.py compose exec db psql -U postgres -d application
```
#### Debugging

For now you can use the below code to print the logs to stderror

```
import sys

def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)

eprint("Some logging here")
```
