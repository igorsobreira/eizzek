
start:
	twistd -ny eizzek/twistd.tac

functional:
	trial tests/functional
unit:
	py.test tests/unit/

clean:
	find . -name "*.pyc" -delete
	rm -rf _trial_temp twistd.log