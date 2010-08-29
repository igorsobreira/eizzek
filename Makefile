
start:
	twistd -ny eizzek/twistd.tac

unit:
	nosetests --nocapture tests/unit/

functional:
	trial tests/functional

clean:
	find . -name "*.pyc" -delete
	rm -rf .coverage
	rm -rf _trial_temp
	rm twistd.log
