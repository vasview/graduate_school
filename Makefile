.PHONY: run setup activate

VENV = venv
PYTHON = ${VENV}\Scripts\python
PIP = ${VENV}\Scripts\pip
MANAGE = .\manage.py
APP_PROFILE = profiles
APP_FACULTY = faculties
APP_POSTGRADUATE = postgraduates
APP_STUDY_PLAN = study_plans
APP_APPLICATION = applications
FIXTURE = .\graduateschool\fixtures

${VENV}\Scripts\activate: requirements.txt
	python -m venv venv
	${VENV}\Scripts\pip install -r requirements.txt

setup: requirements.txt
	python -m venv ${VENV}
	${PIP} install -r requirements.txt

run:
	${PYTHON} ${MANAGE} runserver

migrations:
	${PYTHON} ${MANAGE} makemigrations ${APP_PROFILE}
	${PYTHON} ${MANAGE} makemigrations ${APP_FACULTY}
	${PYTHON} ${MANAGE} makemigrations ${APP_POSTGRADUATE}
	${PYTHON} ${MANAGE} makemigrations ${APP_STUDY_PLAN}
	${PYTHON} ${MANAGE} makemigrations ${APP_APPLICATION}

inspect_migration:
	${PYTHON} ${MANAGE} sqlmigrate ${APP_PROFILE}
	${PYTHON} ${MANAGE} sqlmigrate ${APP_FACULTY}
	${PYTHON} ${MANAGE} sqlmigrate ${APP_POSTGRADUATE}
	${PYTHON} ${MANAGE} sqlmigrate ${APP_STUDY_PLAN}
	${PYTHON} ${MANAGE} sqlmigrate ${APP_APPLICATION}
	
migrate:
	${PYTHON} ${MANAGE} migrate

rollback_all_migrations:
	${PYTHON} ${MANAGE} migrate ${APP_PROFILE} zero
	${PYTHON} ${MANAGE} migrate ${APP_FACULTY} zero
	${PYTHON} ${MANAGE} migrate ${APP_POSTGRADUATE} zero
	${PYTHON} ${MANAGE} migrate ${APP_STUDY_PLAN} zero
	${PYTHON} ${MANAGE} migrate ${APP_APPLICATIO} zero

delete_migrations:
	find . -path "*/migrations/*.py" -not -name "__init__.py" -delete
	find . -path "*/migrations/*.pyc"  -delete

flush:
	${PYTHON} ${MANAGE} flush

static:
	${PYTHON} ${MANAGE} collectstatic

load_data:
	${PYTHON} ${MANAGE} loaddata ${FIXTURE}\subject.json
	${PYTHON} ${MANAGE} loaddata ${FIXTURE}\specialty.json
	${PYTHON} ${MANAGE} loaddata ${FIXTURE}\faculty.json
	${PYTHON} ${MANAGE} loaddata ${FIXTURE}\department.json
	${PYTHON} ${MANAGE} loaddata ${FIXTURE}\academic_degree.json
	${PYTHON} ${MANAGE} loaddata ${FIXTURE}\academic_title.json
	${PYTHON} ${MANAGE} loaddata ${FIXTURE}\work.json
	${PYTHON} ${MANAGE} loaddata ${FIXTURE}\work_scope.json
	${PYTHON} ${MANAGE} loaddata ${FIXTURE}\country.json
	${PYTHON} ${MANAGE} loaddata ${FIXTURE}\study_plan_type.json
	${PYTHON} ${MANAGE} loaddata ${FIXTURE}\education_level.json
	
clean:
	find . -type f -name *.pyc -delete
	find . -type d -name __pycache__ -delete