start:
	twistd -ny eizzek/twistd.tac

test:
	nosetests tests/ 

clean:
	find . -name "*.pyc" -delete
	rm -rf .coverage