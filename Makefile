.PHONY: clean

play: vbuild
	. venv/bin/activate; python -m ftl.game

vbuild: venv
	. venv/bin/activate; python setup.py build

venv: venv/bin/activate
venv/bin/activate: requirements.txt
	test -d venv || virtualenv venv
	. venv/bin/activate; pip install -Ur requirements.txt
	touch venv/bin/activate

