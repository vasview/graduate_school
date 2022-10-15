.PHONY: run setup activate

VENV = venv
PYTHON = ${VENV}\Scripts\python
PIP = ${VENV}\Scripts\pip
MANAGE = .\manage.py
APP_PROFILE = profiles
APP_FACULTY = faculties
APP_POSTGRADUATE = postgraduates
APP_STUDY_PLAN = study_plans
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
	${PYTHON} ${MANAGE} makemigrations

inspect_migration:
	${PYTHON} ${MANAGE} sqlmigrate ${APP_PROFILE}
	${PYTHON} ${MANAGE} sqlmigrate ${APP_FACULTY}
	${PYTHON} ${MANAGE} sqlmigrate ${APP_POSTGRADUATE}
	${PYTHON} ${MANAGE} sqlmigrate ${APP_STUDY_PLAN}
	
migrate:
	${PYTHON} ${MANAGE} migrate

rollback_all_migrations:
	${PYTHON} ${MANAGE} migrate ${APP_PROFILE} zero
	${PYTHON} ${MANAGE} migrate ${APP_FACULTY} zero
	${PYTHON} ${MANAGE} migrate ${APP_POSTGRADUATE} zero
	${PYTHON} ${MANAGE} migrate ${APP_STUDY_PLAN} zero

delete_migrations:
	find . -path "*/migrations/*.py" -not -name "__init__.py" -delete
	find . -path "*/migrations/*.pyc"  -delete

flush:
	${PYTHON} ${MANAGE} flush

load_data:
	${PYTHON} ${MANAGE} loaddata ${FIXTURE}\subject.json
	${PYTHON} ${MANAGE} loaddata ${FIXTURE}\faculty.json
	${PYTHON} ${MANAGE} loaddata ${FIXTURE}\department.json
	${PYTHON} ${MANAGE} loaddata ${FIXTURE}\academic_degree.json
	${PYTHON} ${MANAGE} loaddata ${FIXTURE}\academic_title.json

clean:
	find . -type f -name *.pyc -delete
	find . -type d -name __pycache__ -delete