.PHONY: clean push

play: vbuild
	. venv/bin/activate; python -m ftl.game

vbuild: venv
	. venv/bin/activate; python setup.py build

push:
	git commit -a
	git fetch
	git rebase
	git push

venv: venv/bin/activate
venv/bin/activate: requirements.txt
	test -d venv || virtualenv venv
	. venv/bin/activate; pip install -Ur requirements.txt
	touch venv/bin/activate

