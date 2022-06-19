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

Setting up virtual environment
Note: Install virutalenv in local environment.(unix)

```
virutalenv env
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
```

Running psql command inside database

```
./manage.py compose exec db psql -U postgres -d application
```

Insert some values into the member table

```
insert into member (member_id, govt_id, id_type, fname, is_core, phone, email) values ('sample-111', 'gid-1111', 'AADHAAR' , 'sample' , false,  '99872000', 'email@sample');
```

Insert some values into the beneficiary table

```
insert into beneficiary (beneficiary_id,  fname, phone, email) values ('sample-301', 'sample' , '9946000', 'bemail@sample');
```

Insert some values into the case table (not complete - need to update the not null fields)

```
insert into case (case_id, title, purpose, contact_details) values ('case-111', 'edu 2rd grade', 'education' , '599872000');
```

open http://localhost:8080/members with your browser you will see a successful response, with data above.

You can follow also instructions from [this](https://www.thedigitalcatbooks.com/pycabook-chapter-08/)

#### Debugging

For now you can use the below code to print the logs to stderror

```
import sys

def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)

eprint("Some logging here")
```
