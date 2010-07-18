
start:
	twistd -ny eizzek/twistd.tac

test:
	@nosetests --with-coverage --nocapture --cover-package=eizzek tests/

test_unit:
	@nosetests --nocapture tests/unit/

test_functional:
	@nosetests --nocapture tests/functional/

clean:
	@find . -name "*.pyc" -delete
	@rm -rf .coverage