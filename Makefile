start:
	twistd -ny eizzek/twistd.tac

start_daemon:
	twistd -y eizzek/twistd.tac

test:
	nosetests tests/ --with-coverage