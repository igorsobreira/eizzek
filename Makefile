
start:
	twistd -ny eizzek/twistd.tac

test:
	@nosetests --with-coverage --cover-package=eizzek tests/

test_unit:
	@nosetests tests/unit/

test_functional:
	@nosetests tests/functional

clean:
	@find . -name "*.pyc" -delete
	@rm -rf .coverage